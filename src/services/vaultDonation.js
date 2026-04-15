/**
 * VaultDonation service — instantiates the compiled CashScript contract,
 * derives the vault address, and manages automated withdrawals.
 *
 * The funding transaction is a normal P2PKH spend (signed via WalletConnect)
 * that sends the deposit to the vault's P2SH20 address.  Withdrawals are
 * executed automatically by this service — the withdraw() function is
 * permissionless (no signature needed) so the app can call it directly
 * once the time-lock interval has elapsed.
 */

import { Contract, ElectrumNetworkProvider, TransactionBuilder } from 'cashscript'
import artifact from '../contracts/VaultDonation.json'
import { getAddressHash160 } from './bchChipnet.js'
import { getAddressUtxos } from './electrumClient.js'
import { api } from '../boot/axios.js'
import { useNetworkStore } from '../stores/network-store.js'
import { isValidTxid } from '../utils/bchUtils.js'

const VAULT_STORAGE_KEY = 'cryptocare.vaults'

let providerInstance = null
let providerNetwork = null
let providerCreatedAt = 0
const PROVIDER_MAX_AGE_MS = 5 * 60 * 1000

const getProvider = () => {
  let network
  try {
    const networkStore = useNetworkStore()
    network = networkStore.electrumNetwork
  } catch {
    network = 'chipnet'
  }

  const now = Date.now()
  const isStale = providerInstance && now - providerCreatedAt > PROVIDER_MAX_AGE_MS
  const isWrongNetwork = providerInstance && providerNetwork !== network

  if (!providerInstance || isStale || isWrongNetwork) {
    if (providerInstance) {
      try {
        providerInstance.disconnect?.()
      } catch {
        /* ignore */
      }
    }
    providerInstance = new ElectrumNetworkProvider(network)
    providerNetwork = network
    providerCreatedAt = now
  }
  return providerInstance
}

const resetProvider = () => {
  if (providerInstance) {
    try {
      providerInstance.disconnect?.()
    } catch {
      /* ignore */
    }
  }
  providerInstance = null
  providerNetwork = null
  providerCreatedAt = 0
}

// Allow the network store to reset the singleton when the network changes
window.__cryptocare_resetElectrumProvider = resetProvider

const bytesToHex = (bytes) =>
  Array.from(bytes)
    .map((b) => b.toString(16).padStart(2, '0'))
    .join('')

/**
 * Build a vault record from backend payout data so executeWithdraw() can
 * reconstruct the contract without relying on localStorage.
 */
export const buildVaultRecordFromBackend = ({
  recipientAddress,
  funderAddress,
  withdrawalSatoshis,
  intervalBlocks,
  vaultAddress,
}) => {
  const recipientHash = getAddressHash160(recipientAddress)
  const funderHash = getAddressHash160(funderAddress)
  if (!recipientHash || !funderHash) return null
  return {
    recipientAddress,
    vaultAddress,
    contractParams: {
      recipientHash: bytesToHex(recipientHash),
      funderHash: bytesToHex(funderHash),
    },
    withdrawalSatoshis,
    intervalBlocks,
  }
}

/**
 * Instantiate a VaultDonation contract and return its P2SH20 address.
 *
 * @param {Object} params
 * @param {string} params.recipientAddress  — address of the charity
 * @param {string} params.funderAddress     — address of the donor
 * @param {bigint} params.withdrawalAmount  — satoshis per withdrawal cycle
 * @param {number} params.intervalBlocks    — blocks between withdrawals (1 ≈ 10 min)
 * @returns {{ address: string, contract: Contract, params: Object, network: string }}
 */
export const createVaultContract = ({
  recipientAddress,
  funderAddress,
  withdrawalAmount,
  intervalBlocks,
}) => {
  const recipientHash = getAddressHash160(recipientAddress)
  if (!recipientHash) {
    throw new Error(`Cannot derive hash160 for recipient: "${recipientAddress}"`)
  }

  const funderHash = getAddressHash160(funderAddress)
  if (!funderHash) {
    throw new Error(`Cannot derive hash160 for funder: "${funderAddress}"`)
  }

  const provider = getProvider()

  const contract = new Contract(
    artifact,
    [
      bytesToHex(recipientHash),
      bytesToHex(funderHash),
      BigInt(withdrawalAmount),
      BigInt(intervalBlocks),
    ],
    { provider, addressType: 'p2sh20' },
  )

  return {
    address: contract.address,
    contract,
    network: providerNetwork || 'chipnet',
    params: {
      recipientHash: bytesToHex(recipientHash),
      funderHash: bytesToHex(funderHash),
      withdrawalAmount: withdrawalAmount.toString(),
      intervalBlocks,
    },
  }
}

/**
 * Save vault details to localStorage so withdrawals can be triggered later.
 */
export const saveVaultRecord = (record) => {
  const existing = getAllStoredVaults()
  localStorage.setItem(VAULT_STORAGE_KEY, JSON.stringify([record, ...existing]))
}

export const getStoredVaults = () => {
  try {
    const raw = localStorage.getItem(VAULT_STORAGE_KEY)
    if (!raw) return []
    const parsed = JSON.parse(raw)
    if (!Array.isArray(parsed)) return []

    // Filter to the active network; legacy vaults without a network field are treated as chipnet
    let activeNetwork
    try {
      const networkStore = useNetworkStore()
      activeNetwork = networkStore.activeNetwork
    } catch {
      activeNetwork = 'chipnet'
    }
    return parsed.filter((v) => (v.network || 'chipnet') === activeNetwork)
  } catch {
    return []
  }
}

/**
 * Get ALL stored vaults regardless of network (used internally for saving).
 */
const getAllStoredVaults = () => {
  try {
    const raw = localStorage.getItem(VAULT_STORAGE_KEY)
    if (!raw) return []
    const parsed = JSON.parse(raw)
    return Array.isArray(parsed) ? parsed : []
  } catch {
    return []
  }
}

const updateVaultRecord = (donationId, partial) => {
  const vaults = getAllStoredVaults()
  const updated = vaults.map((v) =>
    v.donationId === donationId ? { ...v, ...partial, updatedAt: new Date().toISOString() } : v,
  )
  localStorage.setItem(VAULT_STORAGE_KEY, JSON.stringify(updated))
}

/**
 * Re-instantiate a vault Contract from a stored record.
 */
const contractFromRecord = (record) => {
  const provider = getProvider()
  return new Contract(
    artifact,
    [
      record.contractParams.recipientHash,
      record.contractParams.funderHash,
      BigInt(record.withdrawalSatoshis),
      BigInt(record.intervalBlocks),
    ],
    { provider, addressType: 'p2sh20' },
  )
}

const MINER_FEE = 1000n

/**
 * Check if the vault has spendable UTXOs and whether they are mature.
 * Uses Watchtower REST API to fetch UTXO block heights, then compares
 * against the current chain tip to determine BIP68 eligibility.
 *
 * Returns { eligible, utxo } on success,
 *         { eligible: false, reason: 'no-utxos' | 'too-young' } otherwise.
 */
export const checkVaultUtxo = async (contract, intervalBlocks) => {
  const utxos = await contract.getUtxos()

  if (!utxos.length) {
    return { eligible: false, reason: 'no-utxos' }
  }

  // Pick the largest UTXO (the vault output)
  const vaultUtxo = utxos.reduce((a, b) => (a.satoshis > b.satoshis ? a : b))

  // Pre-check maturity via Watchtower block heights to avoid futile broadcasts
  try {
    const wtUtxos = await getAddressUtxos(contract.address)
    const provider = getProvider()
    const currentHeight = await provider.getBlockHeight()

    // Match Watchtower UTXO to the CashScript UTXO by txid + vout
    const wtMatch = wtUtxos.find((u) => u.tx_hash === vaultUtxo.txid && u.tx_pos === vaultUtxo.vout)

    if (wtMatch && wtMatch.height > 0 && intervalBlocks > 0) {
      const confirmations = currentHeight - wtMatch.height
      if (import.meta.env.DEV) {
        console.info('[CrypToCare][vault-utxo:maturity]', {
          utxo: `${vaultUtxo.txid}:${vaultUtxo.vout}`,
          block: wtMatch.height,
          currentHeight,
          confirmations,
          needed: intervalBlocks,
        })
      }
      if (confirmations < intervalBlocks) {
        return { eligible: false, reason: 'too-young', confirmations, needed: intervalBlocks }
      }
    }
  } catch (err) {
    // Watchtower pre-check failed — fall through and let the network enforce BIP68
    if (import.meta.env.DEV) {
      console.warn('[CrypToCare][vault-utxo:maturity-fallback]', err?.message)
    }
  }

  return { eligible: true, utxo: vaultUtxo }
}

/**
 * Check if a vault is eligible for reclaim (age >= interval * 3).
 */
export const checkReclaimEligibility = async (record) => {
  const contract = contractFromRecord(record)
  const intervalBlocks = Number(record.intervalBlocks)
  const reclaimAge = intervalBlocks * 3

  const utxos = await contract.getUtxos()
  if (!utxos.length) {
    return { eligible: false, reason: 'no-utxos' }
  }

  const vaultUtxo = utxos.reduce((a, b) => (a.satoshis > b.satoshis ? a : b))
  const balance = vaultUtxo.satoshis

  const check = await checkVaultUtxo(contract, reclaimAge)
  if (!check.eligible) {
    return {
      eligible: false,
      reason: check.reason,
      confirmations: check.confirmations,
      needed: check.needed,
      balance,
    }
  }

  return { eligible: true, utxo: vaultUtxo, balance }
}

/**
 * Execute the reclaim() function on a vault contract.
 * Sends all remaining funds (minus miner fee) back to the original donor.
 */
export const executeReclaim = async (record) => {
  const contract = contractFromRecord(record)
  const intervalBlocks = Number(record.intervalBlocks)
  const reclaimAge = intervalBlocks * 3

  const check = await checkVaultUtxo(contract, reclaimAge)
  if (!check.eligible) {
    return {
      success: false,
      reason: check.reason,
      confirmations: check.confirmations,
      needed: check.needed,
    }
  }

  const vaultUtxo = check.utxo
  const currentValue = vaultUtxo.satoshis
  const reclaimAmount = currentValue - MINER_FEE

  if (reclaimAmount <= 0n) {
    return { success: false, reason: 'insufficient-balance' }
  }

  const reclaimUnlocker = contract.unlock.reclaim()
  const sequence = reclaimAge
  const funderAddress = record.funderAddress

  const tx = new TransactionBuilder({ provider: getProvider() })
    .addInput(vaultUtxo, reclaimUnlocker, { sequence })
    .addOutput({ to: funderAddress, amount: reclaimAmount })

  const sendResult = await tx.send()
  const txid = sendResult.txid

  if (import.meta.env.DEV) {
    console.info('[CrypToCare][vault-reclaim:success]', {
      txid,
      amount: reclaimAmount.toString(),
      funderAddress,
      donationId: record.donationId,
    })
  }

  updateVaultRecord(record.donationId, {
    status: 'reclaimed',
    reclaimTxid: txid,
    reclaimedAt: new Date().toISOString(),
    reclaimedAmount: reclaimAmount.toString(),
  })

  return { success: true, txid, amount: reclaimAmount, vaultBalanceBefore: currentValue }
}

/**
 * Attempt a single withdraw() call against a vault.
 * If the UTXO is too young the network will reject with a BIP68 error,
 * which the auto-withdraw scheduler handles by retrying after the interval.
 * Returns { success, txid, drained } or { success: false, reason }.
 */
export const executeWithdraw = async (record) => {
  const contract = contractFromRecord(record)
  const intervalBlocks = Number(record.intervalBlocks)

  // --- Check that the vault has UTXOs to spend ---
  const check = await checkVaultUtxo(contract, intervalBlocks)

  if (!check.eligible) {
    return { success: false, reason: check.reason }
  }

  const vaultUtxo = check.utxo
  const currentValue = vaultUtxo.satoshis
  const withdrawalAmount = BigInt(record.withdrawalSatoshis)
  const remaining = currentValue - withdrawalAmount - MINER_FEE

  const withdrawUnlocker = contract.unlock.withdraw()

  // sequence must be >= interval for OP_CHECKSEQUENCEVERIFY (BIP68)
  const sequence = intervalBlocks

  const recipientAddress = record.recipientAddress

  let tx

  if (remaining <= withdrawalAmount + MINER_FEE) {
    // Drain: send everything minus fee to recipient
    const drainAmount = currentValue - MINER_FEE
    tx = new TransactionBuilder({ provider: getProvider() })
      .addInput(vaultUtxo, withdrawUnlocker, { sequence })
      .addOutput({ to: recipientAddress, amount: drainAmount })

    const sendResult = await tx.send()
    const txid = sendResult.txid

    if (import.meta.env.DEV) {
      console.info('[CrypToCare][vault-withdraw:drain]', { txid, amount: drainAmount.toString() })
    }

    return {
      success: true,
      txid,
      drained: true,
      amount: drainAmount,
      vaultBalanceBefore: currentValue,
    }
  }

  // Normal cycle: withdrawal to recipient, change back to vault
  tx = new TransactionBuilder({ provider: getProvider() })
    .addInput(vaultUtxo, withdrawUnlocker, { sequence })
    .addOutput({ to: recipientAddress, amount: withdrawalAmount })
    .addOutput({ to: contract.address, amount: remaining })

  const sendResult = await tx.send()
  const txid = sendResult.txid

  if (import.meta.env.DEV) {
    console.info('[CrypToCare][vault-withdraw:cycle]', {
      txid,
      toRecipient: withdrawalAmount.toString(),
      remaining: remaining.toString(),
    })
  }

  return {
    success: true,
    txid,
    drained: false,
    amount: withdrawalAmount,
    vaultBalanceBefore: currentValue,
  }
}

// ---- Auto-withdraw scheduler ----

// Use window-level Map so HMR doesn't create duplicate timers
if (!window.__cryptocare_vaultTimers) {
  window.__cryptocare_vaultTimers = new Map()
}
const activeTimers = window.__cryptocare_vaultTimers

// Track pending approval IDs per cycle to avoid duplicate email requests
if (!window.__cryptocare_pendingApprovals) {
  window.__cryptocare_pendingApprovals = new Map()
}
const pendingApprovals = window.__cryptocare_pendingApprovals

/**
 * Handle the inbox-approval flow for a single cycle:
 * 1. Check UTXO readiness
 * 2. Request approval (sends email) or reuse existing pending approval
 * 3. Poll approval status until approved/expired
 *
 * Returns: { skip, waiting, expired, approved, approvalId, delayMs }
 */
const handleInboxApproval = async (record, cycleNumber, currentBalanceSats = null) => {
  // First check if the UTXO is ready
  const contract = contractFromRecord(record)
  const intervalBlocks = Number(record.intervalBlocks)
  const check = await checkVaultUtxo(contract, intervalBlocks)

  if (!check.eligible) {
    if (check.reason === 'too-young') {
      const blocksLeft = (check.needed || 1) - (check.confirmations || 0)
      return { skip: true, delayMs: Math.max(blocksLeft * BLOCK_TIME_MS, 60_000) }
    }
    return { skip: true, delayMs: POLL_INTERVAL_MS * 2 }
  }

  const idempotencyKey = `${record.donationId}:cycle:${cycleNumber}`

  // Check if we already have a pending approval for this cycle
  let approvalId = pendingApprovals.get(idempotencyKey)

  if (!approvalId) {
    // Request a new approval — this triggers the email
    try {
      const res = await api.post('payouts/request/', {
        donation_id: record.donationId,
        donor_email: record.donorEmail,
        donor_name: record.donorName || '',
        recipient_address: record.recipientAddress,
        vault_address: record.vaultAddress,
        payout_amount_satoshis: record.withdrawalSatoshis,
        coin: record.coin || 'BCH',
        interval_label: record.intervalLabel || '',
        interval_blocks: record.intervalBlocks,
        cycle_number: cycleNumber,
        total_cycles:
          record.totalCycles ||
          Math.floor(
            Number(record.depositSatoshis) /
              (Number(record.withdrawalSatoshis) + Number(MINER_FEE)),
          ) ||
          1,
        vault_balance_satoshis: currentBalanceSats !== null ? Number(currentBalanceSats) : null,
      })

      approvalId = res.data.id
      pendingApprovals.set(idempotencyKey, approvalId)

      if (import.meta.env.DEV) {
        console.info('[CrypToCare][vault-approval:requested]', {
          donationId: record.donationId,
          approvalId,
          cycle: cycleNumber,
        })
      }
    } catch (err) {
      if (import.meta.env.DEV) {
        console.warn('[CrypToCare][vault-approval:request-failed]', err?.message)
      }
      return { skip: true, delayMs: POLL_INTERVAL_MS * 2 }
    }
  }

  // Poll the approval status
  try {
    const statusRes = await api.get(`payouts/${approvalId}/`)
    const status = statusRes.data.status

    if (status === 'approved' || status === 'executed') {
      return { approved: true, approvalId }
    }
    if (status === 'expired' || status === 'failed') {
      pendingApprovals.delete(idempotencyKey)
      return { expired: true, delayMs: POLL_INTERVAL_MS }
    }
    // Still pending — check again soon
    return { waiting: true, approvalId, delayMs: 10_000 }
  } catch (err) {
    if (import.meta.env.DEV) {
      console.warn('[CrypToCare][vault-approval:poll-failed]', err?.message)
    }
    return { waiting: true, approvalId, delayMs: POLL_INTERVAL_MS }
  }
}

/**
 * Report a successful payout execution to the backend.
 */
const reportExecution = async (approvalId, txid) => {
  if (!isValidTxid(txid)) {
    if (import.meta.env.DEV) {
      console.error('[CrypToCare][vault-approval:invalid-txid]', { approvalId, txid })
    }
    return
  }
  try {
    await api.post(`payouts/${approvalId}/execute/`, { txid })
  } catch (err) {
    if (import.meta.env.DEV) {
      console.warn('[CrypToCare][vault-approval:report-failed]', err?.message)
    }
  }
}

const POLL_INTERVAL_MS = 30_000
const BLOCK_TIME_MS = 10 * 60 * 1000

const fmtTime = () =>
  new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', second: '2-digit' })

const satsToBch = (sats) => (Number(sats) / 1e8).toFixed(8)

const calcFundedPct = (currentSats, depositSats) => {
  const dep = Number(depositSats)
  if (!dep) return '—'
  const withdrawn = dep - Number(currentSats)
  const pct = Math.round((withdrawn / dep) * 100)
  return `${Math.max(0, Math.min(100, pct))}%`
}

/**
 * Start auto-withdrawing from a vault. Polls until the vault is drained,
 * waiting for each interval to pass before calling withdraw().
 *
 * @param {Object}   record  — a stored vault record
 * @param {Function} [onCycle] — optional callback({ txid, amount, drained, cycleNumber })
 * @returns {Function} stop — call to cancel the auto-withdraw loop
 */
export const startAutoWithdraw = (record, onCycle) => {
  const id = record.donationId
  if (activeTimers.has(id)) {
    return activeTimers.get(id).stop
  }

  let stopped = false
  let cycleNumber = 0
  let noUtxoStreak = 0
  const MAX_NO_UTXO_RETRIES = 20
  let timer = null

  const sendReclaimWarningEmail = async (currentBalanceSats) => {
    if (!record.donorEmail) return
    try {
      await api.post('payouts/reclaim-warning/', {
        donor_email: record.donorEmail,
        donor_name: record.donorName || '',
        vault_address: record.vaultAddress || '',
        recipient_address: record.recipientAddress || '',
        vault_balance_satoshis: currentBalanceSats !== null ? Number(currentBalanceSats) : 0,
        coin: record.coin || 'BCH',
        interval_label: record.intervalLabel || '',
      })
      if (import.meta.env.DEV) {
        console.info('[CrypToCare][vault-reclaim-warning:sent]', {
          donationId: record.donationId,
          donorEmail: record.donorEmail,
        })
      }
    } catch (err) {
      if (import.meta.env.DEV) {
        console.warn('[CrypToCare][vault-reclaim-warning:failed]', err?.message)
      }
    }
  }

  const stop = () => {
    stopped = true
    if (timer) clearTimeout(timer)
    activeTimers.delete(id)
  }

  const scheduleNext = (delayMs) => {
    if (stopped) return
    timer = setTimeout(run, delayMs)
  }

  const run = async () => {
    if (stopped) return

    // Snapshot vault balance for logging
    let currentBalanceSats = null
    try {
      const contract = contractFromRecord(record)
      const utxos = await contract.getUtxos()
      currentBalanceSats = utxos.reduce((sum, u) => sum + u.satoshis, 0n)
    } catch (balErr) {
      if (
        /socket|connection|Cannot initiate|ECONNREFUSED|ETIMEDOUT/i.test(
          String(balErr?.message || ''),
        )
      ) {
        resetProvider()
      }
    }

    if (import.meta.env.DEV) {
      const modeLabel =
        record.payoutMode === 'inbox_approval'
          ? 'vault-approval:cycle'
          : 'vault-autowithdraw:attempt'
      console.info(`[CrypToCare][${modeLabel}]`, {
        status: record.payoutMode === 'inbox_approval' ? 'Checking approval' : 'Attempting',
        timeSent: fmtTime(),
        donationId: id,
        vaultAddress: record.vaultAddress,
        payoutMode: record.payoutMode || 'smart',
        vaultBalance: currentBalanceSats !== null ? satsToBch(currentBalanceSats) : 'unknown',
        fundPercentage:
          currentBalanceSats !== null
            ? calcFundedPct(currentBalanceSats, record.depositSatoshis)
            : '—',
      })
    }
    try {
      // ── Empty vault check: stop permanently if vault can't cover a withdrawal ──
      if (currentBalanceSats !== null) {
        const minNeeded = BigInt(record.withdrawalSatoshis) + MINER_FEE
        if (currentBalanceSats < minNeeded) {
          if (import.meta.env.DEV) {
            console.info(
              '%c[CrypToCare] Vault empty — stopping permanently',
              'color: #ff9800; font-weight: bold',
              {
                donationId: id,
                vaultBalance: satsToBch(currentBalanceSats),
                minNeeded: satsToBch(minNeeded),
              },
            )
          }
          updateVaultRecord(id, { status: 'drained' })
          stop()
          return
        }
      }

      // ── Inbox Approval mode: request email approval before withdrawing ──
      if (record.payoutMode === 'inbox_approval') {
        const approval = await handleInboxApproval(record, cycleNumber + 1, currentBalanceSats)

        if (approval.skip) {
          scheduleNext(approval.delayMs)
          return
        }
        if (approval.waiting) {
          if (import.meta.env.DEV) {
            console.info('[CrypToCare][vault-approval:waiting]', {
              donationId: id,
              approvalId: approval.approvalId,
              cycle: cycleNumber + 1,
            })
          }
          scheduleNext(approval.delayMs)
          return
        }
        if (approval.expired) {
          if (import.meta.env.DEV) {
            console.warn('[CrypToCare][vault-approval:expired]', {
              donationId: id,
              cycle: cycleNumber + 1,
            })
          }
          // Wait a full interval before re-requesting (a fresh email will be sent)
          const waitMs = Number(record.intervalBlocks) * BLOCK_TIME_MS + POLL_INTERVAL_MS
          scheduleNext(waitMs)
          return
        }

        // Approved — execute the withdrawal
        if (import.meta.env.DEV) {
          console.info('[CrypToCare][vault-approval:approved]', {
            donationId: id,
            approvalId: approval.approvalId,
            cycle: cycleNumber + 1,
          })
        }

        // ── Cycle limit check (inbox_approval) ──
        const maxCycles = record.totalCycles || 0
        if (maxCycles > 0 && cycleNumber >= maxCycles) {
          if (import.meta.env.DEV) {
            console.info(
              '%c[CrypToCare] All cycles completed — stopping vault',
              'color: #4caf50; font-weight: bold',
              {
                donationId: id,
                totalCycles: maxCycles,
              },
            )
          }
          updateVaultRecord(id, { status: 'completed' })
          stop()
          return
        }

        try {
          const result = await executeWithdraw(record)
          if (result.success) {
            await reportExecution(approval.approvalId, result.txid)
            const nextCycle = cycleNumber + 1
            cycleNumber = nextCycle
            noUtxoStreak = 0

            // Build withdrawal history entry
            const currentVault = getAllStoredVaults().find((v) => v.donationId === id)
            const withdrawalHistory = currentVault?.withdrawalHistory || []
            withdrawalHistory.push({
              cycleNumber,
              txid: result.txid,
              amount: result.amount.toString(),
              drained: result.drained,
              timestamp: new Date().toISOString(),
            })

            updateVaultRecord(id, {
              lastWithdrawTxid: result.txid,
              lastWithdrawAt: new Date().toISOString(),
              cyclesCompleted: cycleNumber,
              status: result.drained ? 'drained' : 'withdrawing',
              withdrawalHistory,
            })

            // Report withdrawal to backend as a donation record (best-effort)
            if (isValidTxid(result.txid)) {
              api
                .post('donations/', {
                  txid: result.txid,
                  recipient: record.recipientAddress,
                  amount: (Number(result.amount) / 1e8).toFixed(8),
                  coin: record.coin || 'BCH',
                  cause: record.cause || '',
                  donor_name: record.donorName || '',
                  donor_email: record.donorEmail || '',
                  contract: record.vaultAddress || '',
                  interval: record.intervalLabel || '',
                  interval_blocks: record.intervalBlocks || 0,
                  wallet_address: (record.funderAddress || '').toLowerCase(),
                  payout_mode: record.payoutMode || 'smart',
                })
                .catch((err) => {
                  if (import.meta.env.DEV) {
                    console.warn('[CrypToCare][withdrawal-post:failed]', err?.message)
                  }
                })
            }
            if (import.meta.env.DEV) {
              console.info('[CrypToCare][vault-autowithdraw:success]', {
                status: result.drained ? 'Successful (final drain)' : 'Successful',
                timeSent: fmtTime(),
                donationId: id,
                txid: result.txid,
                amount: result.amount.toString(),
                cycle: cycleNumber,
                drained: result.drained,
              })
            }
            if (result.drained) {
              stop()
              return
            }
            const waitMs = Number(record.intervalBlocks) * BLOCK_TIME_MS + POLL_INTERVAL_MS
            scheduleNext(waitMs)
          } else {
            // Withdrawal failed after approval — retry
            scheduleNext(POLL_INTERVAL_MS)
          }
          return
        } catch (execErr) {
          const rawMsg = String(execErr?.message || '')
          const msg = rawMsg.replace(/\s*WARNING:.*Bitauth URI:.*$/s, '').trim()
          const isBip68 = /non-BIP68-final|non-final|mandatory-script-verify-flag|sequence/i.test(
            msg,
          )
          if (isBip68) {
            // BIP68 not final after approval — re-save approval and retry
            const key = `${record.donationId}:cycle:${cycleNumber + 1}`
            pendingApprovals.set(key, approval.approvalId)
            if (import.meta.env.DEV) {
              console.info('[CrypToCare][vault-approval:bip68-retry]', {
                donationId: id,
                approvalId: approval.approvalId,
              })
            }
            scheduleNext(60_000)
          } else {
            scheduleNext(POLL_INTERVAL_MS * 2)
          }
          return
        }
      }

      // ── Cycle limit check (smart mode) ──
      const smartMaxCycles = record.totalCycles || 0
      if (smartMaxCycles > 0 && cycleNumber >= smartMaxCycles) {
        if (import.meta.env.DEV) {
          console.info(
            '%c[CrypToCare] All cycles completed — stopping vault',
            'color: #4caf50; font-weight: bold',
            {
              donationId: id,
              totalCycles: smartMaxCycles,
            },
          )
        }
        updateVaultRecord(id, { status: 'completed' })
        stop()
        return
      }

      // ── Smart (auto) mode: withdraw directly ──
      const result = await executeWithdraw(record)

      if (!result.success) {
        // Send reclaim warning after 2nd consecutive failed withdrawal cycle
        if (cycleNumber >= 1) {
          const storedVaults = getAllStoredVaults()
          const currentVault = storedVaults.find((v) => v.donationId === id)
          if (!currentVault?.reclaimWarningSentAt) {
            sendReclaimWarningEmail(currentBalanceSats)
            updateVaultRecord(id, { reclaimWarningSentAt: new Date().toISOString() })
          }
        }
        if (result.reason === 'no-utxos') {
          noUtxoStreak++
          if (noUtxoStreak >= MAX_NO_UTXO_RETRIES) {
            // Vault appears to be empty after many attempts
            updateVaultRecord(id, { status: 'drained' })
            if (import.meta.env.DEV) {
              console.info('[CrypToCare][vault-autowithdraw:drained]', {
                status: 'Drained (no UTXOs after max retries)',
                timeSent: fmtTime(),
                donationId: id,
              })
            }
            stop()
            return
          }
          // Funding tx may still be unconfirmed — retry after a delay
          if (import.meta.env.DEV) {
            console.info('[CrypToCare][vault-autowithdraw:no-utxos]', {
              status: 'Waiting (no UTXOs yet)',
              timeSent: fmtTime(),
              donationId: id,
              attempt: noUtxoStreak,
            })
          }
          scheduleNext(POLL_INTERVAL_MS * 2)
          return
        }
        if (result.reason === 'too-young') {
          // UTXO not yet mature — schedule retry based on remaining blocks
          const blocksLeft = (result.needed || 1) - (result.confirmations || 0)
          const waitMs = Math.max(blocksLeft * BLOCK_TIME_MS, 60_000)
          if (import.meta.env.DEV) {
            console.info('[CrypToCare][vault-autowithdraw:too-young]', {
              status: 'Waiting (UTXO too young)',
              timeSent: fmtTime(),
              donationId: id,
              confirmations: result.confirmations,
              needed: result.needed,
              retryMs: waitMs,
            })
          }
          scheduleNext(waitMs)
          return
        }
        // Unknown failure — retry after poll interval
        if (import.meta.env.DEV) {
          console.warn('[CrypToCare][vault-autowithdraw:failed]', {
            status: 'Failed (unknown)',
            timeSent: fmtTime(),
            donationId: id,
            reason: result.reason,
          })
        }
        scheduleNext(POLL_INTERVAL_MS)
        return
      }

      cycleNumber++
      noUtxoStreak = 0

      // Build withdrawal history entry
      const currentVault = getAllStoredVaults().find((v) => v.donationId === id)
      const withdrawalHistory = currentVault?.withdrawalHistory || []
      withdrawalHistory.push({
        cycleNumber,
        txid: result.txid,
        amount: result.amount.toString(),
        drained: result.drained,
        timestamp: new Date().toISOString(),
      })

      updateVaultRecord(id, {
        lastWithdrawTxid: result.txid,
        lastWithdrawAt: new Date().toISOString(),
        cyclesCompleted: cycleNumber,
        status: result.drained ? 'drained' : 'withdrawing',
        withdrawalHistory,
      })

      // ── Record this cycle's unique txid to the backend (smart mode) ──
      if (isValidTxid(result.txid)) {
        // Single call: creates an already-executed record with the real blockchain txid
        api
          .post('payouts/record/', {
            donation_id: record.donationId,
            donor_email: record.donorEmail || '',
            donor_name: record.donorName || '',
            recipient_address: record.recipientAddress,
            vault_address: record.vaultAddress || '',
            payout_amount_satoshis: record.withdrawalSatoshis,
            coin: record.coin || 'BCH',
            interval_label: record.intervalLabel || '',
            interval_blocks: record.intervalBlocks,
            cycle_number: cycleNumber,
            total_cycles:
              record.totalCycles ||
              Math.floor(
                Number(record.depositSatoshis) /
                  (Number(record.withdrawalSatoshis) + Number(MINER_FEE)),
              ) ||
              1,
            txid: result.txid,
          })
          .catch((err) => {
            if (import.meta.env.DEV) {
              console.warn('[CrypToCare][smart-payout:record-failed]', err?.message)
            }
          })

        // Also save to Donation table (best-effort, for donor history)
        api
          .post('donations/', {
            txid: result.txid,
            recipient: record.recipientAddress,
            amount: (Number(result.amount) / 1e8).toFixed(8),
            coin: record.coin || 'BCH',
            cause: record.cause || '',
            donor_name: record.donorName || '',
            donor_email: record.donorEmail || '',
            contract: record.vaultAddress || '',
            interval: record.intervalLabel || '',
            interval_blocks: record.intervalBlocks || 0,
            wallet_address: (record.funderAddress || '').toLowerCase(),
            payout_mode: record.payoutMode || 'smart',
          })
          .catch((err) => {
            if (import.meta.env.DEV) {
              console.warn('[CrypToCare][withdrawal-post:failed]', err?.message)
            }
          })
      }

      if (import.meta.env.DEV) {
        console.info('[CrypToCare][vault-autowithdraw:success]', {
          status: result.drained ? 'Successful (final drain)' : 'Successful',
          timeSent: fmtTime(),
          donationId: id,
          txid: result.txid,
          amount: result.amount.toString(),
          vaultBalance: satsToBch(result.vaultBalanceBefore - result.amount - MINER_FEE),
          fundPercentage: calcFundedPct(
            result.vaultBalanceBefore - result.amount - MINER_FEE,
            record.depositSatoshis,
          ),
          cycle: cycleNumber,
          drained: result.drained,
        })
      }

      if (typeof onCycle === 'function') {
        try {
          onCycle({
            txid: result.txid,
            amount: result.amount,
            drained: result.drained,
            cycleNumber,
          })
        } catch {
          /* callback error ignored */
        }
      }

      if (result.drained) {
        if (import.meta.env.DEV) {
          console.info(
            '%c[CrypToCare] Vault Empty — Fund is now Complete',
            'color: #4caf50; font-weight: bold; font-size: 14px',
            {
              timeSent: fmtTime(),
              donationId: id,
              vaultAddress: record.vaultAddress,
              totalCycles: cycleNumber,
            },
          )
        }
        stop()
        return
      }

      // Wait for the next interval (block time * interval blocks) + buffer
      const waitMs = Number(record.intervalBlocks) * BLOCK_TIME_MS + POLL_INTERVAL_MS
      scheduleNext(waitMs)
    } catch (error) {
      // Send reclaim warning after 2nd consecutive failed cycle (catch path)
      if (cycleNumber >= 1) {
        const storedVaults = getAllStoredVaults()
        const currentVault = storedVaults.find((v) => v.donationId === id)
        if (!currentVault?.reclaimWarningSentAt) {
          sendReclaimWarningEmail(currentBalanceSats)
          updateVaultRecord(id, { reclaimWarningSentAt: new Date().toISOString() })
        }
      }
      const rawMsg = String(error?.message || '')
      // Strip CashScript Bitauth debug URI from error messages
      const msg = rawMsg.replace(/\s*WARNING:.*Bitauth URI:.*$/s, '').trim()

      const isSocketError = /socket|connection|ECONNREFUSED|ETIMEDOUT|Cannot initiate/i.test(msg)
      if (isSocketError) {
        resetProvider()
        if (import.meta.env.DEV) {
          console.warn('[CrypToCare][vault-autowithdraw:socket-reset]', {
            donationId: id,
            error: msg,
          })
        }
        scheduleNext(120_000)
        return
      }

      const isBip68 = /non-BIP68-final|non-final|mandatory-script-verify-flag|sequence/i.test(msg)
      const isContractRequire = /Require statement failed/i.test(msg)

      if (import.meta.env.DEV) {
        console.warn('[CrypToCare][vault-autowithdraw:error]', {
          status: isBip68 ? 'Waiting (BIP68 not final)' : 'Error',
          timeSent: fmtTime(),
          donationId: id,
          error: msg,
        })
      }

      if (isBip68) {
        // UTXO hasn't aged enough blocks — retry every 60s (chipnet blocks can be fast)
        scheduleNext(60_000)
      } else if (isContractRequire) {
        // Contract logic error — likely UTXO state changed mid-flight, retry soon
        scheduleNext(POLL_INTERVAL_MS)
      } else {
        // Other errors — retry after a moderate delay
        scheduleNext(POLL_INTERVAL_MS * 2)
      }
    }
  }

  activeTimers.set(id, { stop })

  // First attempt: wait for the interval to pass from funding time
  const createdAt = new Date(record.createdAt).getTime()
  const firstWithdrawAt = createdAt + Number(record.intervalBlocks) * BLOCK_TIME_MS
  const now = Date.now()
  const initialDelay = Math.max(0, firstWithdrawAt - now)

  if (import.meta.env.DEV) {
    console.info('[CrypToCare][vault-autowithdraw:start]', {
      status: 'Scheduled',
      timeSent: fmtTime(),
      donationId: id,
      vaultAddress: record.vaultAddress,
      initialDelayMs: initialDelay,
      intervalBlocks: record.intervalBlocks,
    })
  }

  scheduleNext(initialDelay)

  return stop
}

/**
 * Push locally-cached withdrawal txids to the backend so the nonprofit
 * Dashboard shows the correct per-cycle txids even if the vault is drained
 * and the auto-scheduler can no longer re-report them.
 */
export const syncCachedWithdrawalHistory = async () => {
  const vaults = getAllStoredVaults()
  for (const vault of vaults) {
    const history = vault.withdrawalHistory
    if (!Array.isArray(history) || !history.length) continue
    if (!vault.vaultAddress) continue
    for (const entry of history) {
      if (!isValidTxid(entry.txid) || !entry.cycleNumber) continue
      try {
        await api.post('payouts/record/', {
          donation_id: vault.donationId,
          donor_email: vault.donorEmail || '',
          donor_name: vault.donorName || '',
          recipient_address: vault.recipientAddress,
          vault_address: vault.vaultAddress,
          payout_amount_satoshis: vault.withdrawalSatoshis,
          coin: vault.coin || 'BCH',
          interval_label: vault.intervalLabel || '',
          interval_blocks: vault.intervalBlocks || 1,
          cycle_number: entry.cycleNumber,
          total_cycles: vault.totalCycles || 1,
          txid: entry.txid,
        })
      } catch {
        // best-effort — ignore 404s and other errors
      }
    }
  }
}

/**
 * Resume auto-withdraw for all active (non-drained) vaults in localStorage.
 * Call this on app startup / page load.
 *
 * @param {Function} [onCycle] — optional callback for each withdrawal cycle
 * @returns {Function} stopAll — stops all running auto-withdrawers
 */
export const resumeAllAutoWithdraws = (onCycle) => {
  // Sync any locally-cached txids that the backend may be missing
  syncCachedWithdrawalHistory().catch(() => {})

  const vaults = getStoredVaults()
  let staggerIndex = 0
  for (const vault of vaults) {
    if (vault.status === 'drained' || vault.status === 'reclaimed') continue
    // Skip legacy vaults without an explicit payoutMode
    if (!vault.payoutMode) continue
    const delay = staggerIndex * 5000
    setTimeout(() => startAutoWithdraw(vault, onCycle), delay)
    staggerIndex++
  }

  return () => {
    for (const { stop } of activeTimers.values()) {
      stop()
    }
  }
}

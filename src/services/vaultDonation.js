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

const VAULT_STORAGE_KEY = 'bitohelp.vaults'

let providerInstance = null

const getProvider = () => {
  if (!providerInstance) {
    providerInstance = new ElectrumNetworkProvider('chipnet')
  }
  return providerInstance
}

const bytesToHex = (bytes) =>
  Array.from(bytes)
    .map((b) => b.toString(16).padStart(2, '0'))
    .join('')

/**
 * Instantiate a VaultDonation contract and return its chipnet P2SH20 address.
 *
 * @param {Object} params
 * @param {string} params.recipientAddress  — chipnet address of the charity
 * @param {string} params.funderAddress     — chipnet address of the donor
 * @param {bigint} params.withdrawalAmount  — satoshis per withdrawal cycle
 * @param {number} params.intervalBlocks    — blocks between withdrawals (1 ≈ 10 min)
 * @returns {{ address: string, contract: Contract, params: Object }}
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
  const existing = getStoredVaults()
  localStorage.setItem(VAULT_STORAGE_KEY, JSON.stringify([record, ...existing]))
}

export const getStoredVaults = () => {
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
  const vaults = getStoredVaults()
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
const checkVaultUtxo = async (contract, intervalBlocks) => {
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
        console.info('[BitoHelp][vault-utxo:maturity]', {
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
      console.warn('[BitoHelp][vault-utxo:maturity-fallback]', err?.message)
    }
  }

  return { eligible: true, utxo: vaultUtxo }
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
      console.info('[BitoHelp][vault-withdraw:drain]', { txid, amount: drainAmount.toString() })
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
    console.info('[BitoHelp][vault-withdraw:cycle]', {
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
if (!window.__bitohelp_vaultTimers) {
  window.__bitohelp_vaultTimers = new Map()
}
const activeTimers = window.__bitohelp_vaultTimers

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
    } catch {
      /* ignore */
    }

    if (import.meta.env.DEV) {
      console.info('[BitoHelp][vault-autowithdraw:attempt]', {
        status: 'Attempting',
        timeSent: fmtTime(),
        donationId: id,
        vaultAddress: record.vaultAddress,
        vaultBalance: currentBalanceSats !== null ? satsToBch(currentBalanceSats) : 'unknown',
        fundPercentage:
          currentBalanceSats !== null
            ? calcFundedPct(currentBalanceSats, record.depositSatoshis)
            : '—',
      })
    }
    try {
      const result = await executeWithdraw(record)

      if (!result.success) {
        if (result.reason === 'no-utxos') {
          noUtxoStreak++
          if (noUtxoStreak >= MAX_NO_UTXO_RETRIES) {
            // Vault appears to be empty after many attempts
            updateVaultRecord(id, { status: 'drained' })
            if (import.meta.env.DEV) {
              console.info('[BitoHelp][vault-autowithdraw:drained]', {
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
            console.info('[BitoHelp][vault-autowithdraw:no-utxos]', {
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
            console.info('[BitoHelp][vault-autowithdraw:too-young]', {
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
          console.warn('[BitoHelp][vault-autowithdraw:failed]', {
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
      updateVaultRecord(id, {
        lastWithdrawTxid: result.txid,
        lastWithdrawAt: new Date().toISOString(),
        cyclesCompleted: cycleNumber,
        status: result.drained ? 'drained' : 'withdrawing',
      })

      if (import.meta.env.DEV) {
        console.info('[BitoHelp][vault-autowithdraw:success]', {
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
            '%c[BitoHelp] Vault Empty — Fund is now Complete',
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
      const msg = String(error?.message || '')
      const isBip68 = /non-BIP68-final|non-final|mandatory-script-verify-flag|sequence/i.test(msg)
      const isContractRequire = /Require statement failed/i.test(msg)

      if (import.meta.env.DEV) {
        console.warn('[BitoHelp][vault-autowithdraw:error]', {
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
    console.info('[BitoHelp][vault-autowithdraw:start]', {
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
 * Resume auto-withdraw for all active (non-drained) vaults in localStorage.
 * Call this on app startup / page load.
 *
 * @param {Function} [onCycle] — optional callback for each withdrawal cycle
 * @returns {Function} stopAll — stops all running auto-withdrawers
 */
export const resumeAllAutoWithdraws = (onCycle) => {
  const vaults = getStoredVaults()
  for (const vault of vaults) {
    if (vault.status === 'drained' || vault.status === 'reclaimed') continue
    startAutoWithdraw(vault, onCycle)
  }

  return () => {
    for (const { stop } of activeTimers.values()) {
      stop()
    }
  }
}

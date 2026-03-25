import { decode as decodeCashAddress, encode as encodeCashAddress } from 'cashaddrjs'
import { getAddressUtxos, broadcastTransaction, getTransaction } from './electrumClient.js'

const SATOSHIS_PER_BCH = 100000000n
const BCH_DUST_SATOSHIS = 546n
const DEFAULT_FEE_RATE = 1.2
const DEFAULT_CONFIRMATION_TIMEOUT_MS = 600000
const DEFAULT_CONFIRMATION_POLL_MS = 30000
const DEFAULT_CONFIRMATION_INITIAL_DELAY_MS = 60000

const getEnvValue = (key, fallback = '') => {
  const fromProcess = typeof process !== 'undefined' ? process?.env?.[key] : undefined
  if (fromProcess !== undefined && fromProcess !== null && String(fromProcess).trim()) {
    return String(fromProcess).trim()
  }
  return fallback
}

export const getBchRuntimeConfig = () => {
  const network = getEnvValue('BCH_NETWORK', 'chipnet').toLowerCase()

  return {
    network,
    isChipnet: network === 'chipnet',
    explorerBaseUrl: getEnvValue('BCH_EXPLORER_BASE_URL', ''),
    feeRateSatsPerByte: Number.parseFloat(
      getEnvValue('BCH_FEE_RATE_SATS_PER_BYTE', `${DEFAULT_FEE_RATE}`),
    ),
  }
}

const hexToBytes = (hexValue) => {
  const sanitized = String(hexValue || '')
    .replace(/^0x/i, '')
    .trim()
  if (!sanitized || sanitized.length % 2 !== 0 || /[^a-fA-F0-9]/.test(sanitized)) {
    throw new Error('Invalid hexadecimal value.')
  }

  const bytes = new Uint8Array(sanitized.length / 2)
  for (let index = 0; index < bytes.length; index += 1) {
    bytes[index] = Number.parseInt(sanitized.slice(index * 2, index * 2 + 2), 16)
  }
  return bytes
}

export const normalizeChipnetAddress = (value) => {
  const raw = String(value ?? '').trim()
  if (!raw) {
    return ''
  }

  // Extract just the hash payload — take everything after the last colon.
  // This handles bare hashes, 'bchtest:qq...', 'bitcoincash:qq...', and even
  // malformed CAIP segments like 'bch:chipnet:bchtest:qq...'.
  const baseHash = raw.includes(':') ? raw.slice(raw.lastIndexOf(':') + 1) : raw
  if (!baseHash) {
    return ''
  }

  // Chipnet uses the 'bchtest' CashAddr prefix exclusively.
  // Only accept addresses that validate against that prefix.
  const candidate = `bchtest:${baseHash}`
  try {
    const decoded = decodeCashAddress(candidate)
    if (decoded?.prefix === 'bchtest') {
      return candidate.toLowerCase()
    }
  } catch {
    // invalid CashAddr checksum for chipnet
  }

  return ''
}

export const isValidChipnetAddress = (value) => Boolean(normalizeChipnetAddress(value))

export const getAddressHash160 = (address) => {
  const normalized = normalizeChipnetAddress(address)
  if (!normalized) return null
  try {
    const decoded = decodeCashAddress(normalized)
    const hash = decoded?.hash
    const hashBytes = hash instanceof Uint8Array ? hash : Uint8Array.from(hash || [])
    if (hashBytes.length !== 20) return null
    return hashBytes
  } catch {
    return null
  }
}

export const decimalBchToSatoshis = (value) => {
  const normalized = String(value ?? '').trim()
  if (!/^\d+(\.\d+)?$/.test(normalized)) {
    return null
  }

  const [wholePart = '0', fractionPart = ''] = normalized.split('.')
  if (fractionPart.length > 8) {
    return null
  }

  const paddedFraction = `${fractionPart}00000000`.slice(0, 8)

  try {
    const satoshis = BigInt(wholePart) * SATOSHIS_PER_BCH + BigInt(paddedFraction)
    if (satoshis <= 0n) {
      return null
    }
    return satoshis
  } catch {
    return null
  }
}

export const fetchAddressUtxos = async ({ address }) => {
  const normalizedAddress = normalizeChipnetAddress(address)
  if (!normalizedAddress) {
    throw new Error(`Invalid BCH chipnet address: "${address}"`)
  }

  const result = await getAddressUtxos(normalizedAddress)

  if (!Array.isArray(result)) {
    throw new Error('Electrum server returned invalid UTXO data.')
  }

  const utxos = []
  for (const item of result) {
    const txid = String(item?.tx_hash || '').trim()
    const vout = Number(item?.tx_pos)
    const valueSatoshis = BigInt(item?.value || 0)

    if (!txid || !Number.isInteger(vout) || vout < 0 || valueSatoshis <= 0n) {
      continue
    }

    utxos.push({
      txid,
      vout,
      valueSatoshis,
      block: Number(item?.height || 0),
    })
  }

  return utxos
}

const estimateP2pkhTxSizeBytes = ({ inputsCount, outputsCount }) => {
  return 10 + inputsCount * 148 + outputsCount * 34
}

const estimateFeeSatoshis = ({ inputsCount, outputsCount, feeRateSatsPerByte }) => {
  const txBytes = estimateP2pkhTxSizeBytes({ inputsCount, outputsCount })
  return BigInt(Math.ceil(txBytes * feeRateSatsPerByte))
}

export const selectInputsAndBuildPlan = ({ utxos, amountSatoshis, feeRateSatsPerByte }) => {
  if (!Array.isArray(utxos) || utxos.length === 0) {
    throw new Error('No spendable BCH UTXOs found for this wallet address.')
  }

  const selected = []
  let totalIn = 0n

  const sorted = [...utxos].sort((a, b) => Number(b.valueSatoshis - a.valueSatoshis))

  for (const utxo of sorted) {
    selected.push(utxo)
    totalIn += utxo.valueSatoshis

    const maybeFeeTwoOutputs = estimateFeeSatoshis({
      inputsCount: selected.length,
      outputsCount: 2,
      feeRateSatsPerByte,
    })

    if (totalIn < amountSatoshis + maybeFeeTwoOutputs) {
      continue
    }

    let fee = maybeFeeTwoOutputs
    let change = totalIn - amountSatoshis - fee

    if (change > 0n && change < BCH_DUST_SATOSHIS) {
      const feeOneOutput = estimateFeeSatoshis({
        inputsCount: selected.length,
        outputsCount: 1,
        feeRateSatsPerByte,
      })
      const oneOutputChange = totalIn - amountSatoshis - feeOneOutput

      if (oneOutputChange >= BCH_DUST_SATOSHIS) {
        fee = maybeFeeTwoOutputs
        change = oneOutputChange - (maybeFeeTwoOutputs - feeOneOutput)
      } else {
        fee = feeOneOutput
        change = 0n
      }
    }

    if (change < 0n) {
      continue
    }

    return {
      inputs: selected,
      totalIn,
      fee,
      change,
      outputsCount: change >= BCH_DUST_SATOSHIS ? 2 : 1,
    }
  }

  throw new Error('Insufficient BCH balance for amount plus network fee.')
}

const toLockingBytecode = (address) => {
  let decoded
  try {
    decoded = decodeCashAddress(address)
  } catch {
    throw new Error('Invalid BCH cash address.')
  }

  const hash = decoded?.hash
  const hashBytes = hash instanceof Uint8Array ? hash : Uint8Array.from(hash || [])

  if (decoded.type === 'P2PKH' && hashBytes.length === 20) {
    return new Uint8Array([0x76, 0xa9, 0x14, ...hashBytes, 0x88, 0xac])
  }

  if (decoded.type === 'P2SH' && hashBytes.length === 20) {
    // P2SH20: OP_HASH160 <20-byte hash> OP_EQUAL
    return new Uint8Array([0xa9, 0x14, ...hashBytes, 0x87])
  }

  if (decoded.type === 'P2SH' && hashBytes.length === 32) {
    // P2SH32: OP_HASH256 <32-byte hash> OP_EQUAL
    return new Uint8Array([0xaa, 0x20, ...hashBytes, 0x87])
  }

  throw new Error('Unsupported BCH address type for donation outputs.')
}

// const reverseBytes = (bytes) => {
//   const copy = new Uint8Array(bytes)
//   copy.reverse()
//   return copy
// }

const bytesToHex = (bytes) =>
  Array.from(bytes)
    .map((b) => b.toString(16).padStart(2, '0'))
    .join('')

const normalizeBytesLike = (value) => {
  if (value instanceof Uint8Array) {
    return value
  }

  if (typeof value === 'string') {
    const match = value.trim().match(/^<Uint8Array:\s*0x([a-fA-F0-9]*)>$/)
    if (!match) {
      return null
    }
    return hexToBytes(match[1])
  }

  if (value && typeof value === 'object') {
    const entries = Object.values(value)
    if (
      entries.length > 0 &&
      entries.every((item) => Number.isInteger(item) && item >= 0 && item <= 255)
    ) {
      return Uint8Array.from(entries)
    }
  }

  return null
}

export const lockingBytecodeToAddressVariants = (value) => {
  const lockingBytecode = normalizeBytesLike(value)
  if (!lockingBytecode) {
    return null
  }

  let type = null
  let hash = null

  if (
    lockingBytecode.length === 25 &&
    lockingBytecode[0] === 0x76 &&
    lockingBytecode[1] === 0xa9 &&
    lockingBytecode[2] === 0x14 &&
    lockingBytecode[23] === 0x88 &&
    lockingBytecode[24] === 0xac
  ) {
    type = 'P2PKH'
    hash = lockingBytecode.slice(3, 23)
  } else if (
    lockingBytecode.length === 23 &&
    lockingBytecode[0] === 0xa9 &&
    lockingBytecode[1] === 0x14 &&
    lockingBytecode[22] === 0x87
  ) {
    type = 'P2SH'
    hash = lockingBytecode.slice(2, 22)
  } else if (
    lockingBytecode.length === 35 &&
    lockingBytecode[0] === 0xaa &&
    lockingBytecode[1] === 0x20 &&
    lockingBytecode[34] === 0x87
  ) {
    // P2SH32
    type = 'P2SH'
    hash = lockingBytecode.slice(2, 34)
  }

  if (!type || !hash) {
    return null
  }

  const mainnet = encodeCashAddress('bitcoincash', type, hash).toLowerCase()
  const chipnet = encodeCashAddress('bchtest', type, hash).toLowerCase()

  return {
    type,
    payload: mainnet.split(':')[1],
    bitcoincash: mainnet,
    bchtest: chipnet,
  }
}

// Paytaca revives BCH WalletConnect payloads from tagged strings like:
//   <Uint8Array: 0x...>
//   <bigint: 123n>
// Keep the payload JSON-serializable while preserving the original BCH types.
const toExtendedJsonUint8Array = (bytes) => `<Uint8Array: 0x${bytesToHex(bytes)}>`

const toExtendedJsonBigInt = (value) => `<bigint: ${value}n>`

export const buildWalletConnectBchSignPayload = ({
  plan,
  senderAddress,
  charityAddress,
  changeAddress,
  amountSatoshis,
  userPrompt,
  signingAccount,
  includeInlineSourceOutputs = false,
}) => {
  const senderLockingBytecode = toLockingBytecode(senderAddress)
  const charityLockingBytecode = toLockingBytecode(charityAddress)
  const changeLockingBytecode = toLockingBytecode(changeAddress)
  const emptyUnlockingBytecode = '<Uint8Array: 0x>'
  // Paytaca's own WalletConnect example uses sequenceNumber 0.
  // Using 0xfffffffe caused 'missing-inputs' in some combos.
  const walletConnectSequenceNumber = 0

  const sourceOutputs = plan.inputs.map((utxo) => ({
    outpointIndex: utxo.vout,
    // Watchtower API returns txid in display (big-endian) order.
    // libauth internally uses little-endian, but Paytaca's parseSessionRequest
    // only compares bytes via binToHex for matching — order doesn't matter
    // for matching.  Try display order first (no reversal); if signing
    // still fails with "missing-inputs", the byte order isn't the cause.
    outpointTransactionHash: toExtendedJsonUint8Array(hexToBytes(utxo.txid)),
    sequenceNumber: walletConnectSequenceNumber,
    unlockingBytecode: emptyUnlockingBytecode,
    lockingBytecode: toExtendedJsonUint8Array(senderLockingBytecode),
    valueSatoshis: toExtendedJsonBigInt(utxo.valueSatoshis),
  }))

  const inputs = plan.inputs.map((utxo, index) => {
    const input = {
      outpointIndex: utxo.vout,
      outpointTransactionHash: toExtendedJsonUint8Array(hexToBytes(utxo.txid)),
      sequenceNumber: walletConnectSequenceNumber,
      unlockingBytecode: emptyUnlockingBytecode,
    }

    if (includeInlineSourceOutputs) {
      input.sourceOutput = sourceOutputs[index]
    }

    return input
  })

  const outputs = [
    {
      lockingBytecode: toExtendedJsonUint8Array(charityLockingBytecode),
      valueSatoshis: toExtendedJsonBigInt(amountSatoshis),
    },
  ]

  if (plan.change >= BCH_DUST_SATOSHIS) {
    outputs.push({
      lockingBytecode: toExtendedJsonUint8Array(changeLockingBytecode),
      valueSatoshis: toExtendedJsonBigInt(plan.change),
    })
  }

  const payload = {
    transaction: {
      version: 2,
      locktime: 0,
      inputs,
      outputs,
    },
    sourceOutputs,
    broadcast: false,
    userPrompt,
  }

  const normalizedAccount = normalizeChipnetAddress(signingAccount || senderAddress)
  if (normalizedAccount) {
    payload.account = normalizedAccount
  }

  return payload
}

export const extractWalletSignedTransaction = (result) => {
  if (!result) {
    throw new Error('Wallet returned an empty signing response.')
  }

  if (typeof result === 'string') {
    const rawTxHex = result
    return {
      rawTxHex,
      signedTxid: null,
    }
  }

  const signedTxHex =
    result?.signedTransaction ||
    result?.transaction ||
    result?.rawTransaction ||
    result?.txHex ||
    result?.hex ||
    null

  if (!signedTxHex || typeof signedTxHex !== 'string') {
    throw new Error('Wallet did not return a signed BCH transaction hex.')
  }

  const signedTxid = result?.signedTransactionHash || result?.txid || result?.hash || null

  return {
    rawTxHex: signedTxHex,
    signedTxid,
  }
}

export const broadcastRawTransaction = async ({ rawTxHex }) => {
  const txid = await broadcastTransaction(rawTxHex)

  if (!txid || typeof txid !== 'string') {
    throw new Error('Transaction broadcast failed — no txid returned.')
  }

  return {
    txid,
    raw: { txid },
  }
}

export const fetchTransactionConfirmations = async ({ txid }) => {
  try {
    const payload = await getTransaction(txid)
    const confirmations = Number(payload?.confirmations || 0)
    return {
      confirmations: confirmations > 0 ? confirmations : 0,
      payload,
    }
  } catch {
    return {
      confirmations: 0,
      payload: null,
    }
  }
}

const sleep = (ms) => new Promise((resolve) => window.setTimeout(resolve, ms))

export const waitForConfirmations = async ({
  txid,
  minConfirmations = 1,
  timeoutMs = DEFAULT_CONFIRMATION_TIMEOUT_MS,
  pollMs = DEFAULT_CONFIRMATION_POLL_MS,
  initialDelayMs = DEFAULT_CONFIRMATION_INITIAL_DELAY_MS,
}) => {
  const start = Date.now()

  // Give the indexer time to see the tx before hitting it in a loop
  if (initialDelayMs > 0) {
    await sleep(initialDelayMs)
  }

  let currentPollMs = pollMs
  while (Date.now() - start <= timeoutMs) {
    const { confirmations } = await fetchTransactionConfirmations({ txid })
    if (confirmations >= minConfirmations) {
      return { confirmed: true, confirmations }
    }
    await sleep(currentPollMs)
    // Exponential backoff: double interval each cycle, cap at 2 minutes
    currentPollMs = Math.min(currentPollMs * 2, 120000)
  }

  return {
    confirmed: false,
    confirmations: 0,
  }
}
export const fetchAddressBalance = async ({ address }) => {
  try {
    const utxos = await fetchAddressUtxos({ address })
    const totalSatoshis = utxos.reduce((sum, utxo) => sum + utxo.valueSatoshis, 0n)
    return Number(totalSatoshis) / 100000000
  } catch (error) {
    throw new Error(`Failed to fetch BCH balance: ${error.message}`)
  }
}

// Re-encode a chipnet (bchtest:) address as its mainnet (bitcoincash:) equivalent.
// The 20-byte hash is identical — only the network prefix changes.
export const chipnetAddressToMainnet = (address) => {
  const normalized = normalizeChipnetAddress(address)
  if (!normalized) {
    return ''
  }
  try {
    const decoded = decodeCashAddress(normalized)
    return encodeCashAddress('bitcoincash', decoded.type, decoded.hash).toLowerCase()
  } catch {
    return ''
  }
}

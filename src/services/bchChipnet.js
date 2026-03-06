import { decode as decodeCashAddress, encode as encodeCashAddress } from 'cashaddrjs'

const SATOSHIS_PER_BCH = 100000000n
const BCH_DUST_SATOSHIS = 546n
const DEFAULT_FEE_RATE = 1.2
const DEFAULT_API_BASE = 'https://chipnet.watchtower.cash/api/'
const DEFAULT_CONFIRMATION_TIMEOUT_MS = 180000
const DEFAULT_CONFIRMATION_POLL_MS = 5000

const normalizeApiBaseUrl = (value) => {
  const fallback = DEFAULT_API_BASE
  const source = String(value || fallback).trim()
  if (!source) {
    return fallback
  }
  return source.endsWith('/') ? source : `${source}/`
}

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
    apiBaseUrl: normalizeApiBaseUrl(getEnvValue('BCH_CHIPNET_API_URL', DEFAULT_API_BASE)),
    explorerBaseUrl: getEnvValue('BCH_EXPLORER_BASE_URL', ''),
    feeRateSatsPerByte: Number.parseFloat(
      getEnvValue('BCH_FEE_RATE_SATS_PER_BYTE', `${DEFAULT_FEE_RATE}`),
    ),
  }
}

const isFinitePositiveInteger = (value) => Number.isInteger(value) && value > 0

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

const sanitizeUtxo = (item) => {
  const txid = String(item?.txid || item?.tx_hash || '').trim()
  const vout = Number(item?.vout ?? item?.tx_pos)
  // Watchtower may return 'amount' (BCH decimal string e.g. "0.10000000"),
  // or 'value' / 'satoshis' (integer satoshis from Fulcrum-style APIs).
  const valueRaw = item?.amount ?? item?.value ?? item?.satoshis

  if (!txid || !Number.isInteger(vout) || vout < 0 || valueRaw === undefined || valueRaw === null) {
    console.warn('[BitoHelp][bch-utxo] sanitizeUtxo: rejected (missing fields)', {
      item,
      txid,
      vout,
      valueRaw,
    })
    return null
  }

  let valueSatoshis
  try {
    const asStr = String(valueRaw).trim()
    if (asStr.includes('.')) {
      // Decimal BCH value (e.g. "0.10000000") → convert to satoshis
      const [whole = '0', frac = ''] = asStr.split('.')
      const paddedFrac = (frac + '00000000').slice(0, 8)
      valueSatoshis = BigInt(whole) * 100000000n + BigInt(paddedFrac)
    } else {
      valueSatoshis = BigInt(asStr)
    }
  } catch (e) {
    console.warn('[BitoHelp][bch-utxo] sanitizeUtxo: rejected (value parse error)', {
      item,
      valueRaw,
      error: String(e),
    })
    return null
  }

  if (valueSatoshis <= 0n) {
    console.warn('[BitoHelp][bch-utxo] sanitizeUtxo: rejected (zero/negative value)', {
      item,
      valueSatoshis: String(valueSatoshis),
    })
    return null
  }

  return {
    txid,
    vout,
    valueSatoshis,
    block: Number(item?.block || item?.height || 0),
  }
}

export const fetchAddressUtxos = async ({ apiBaseUrl, address }) => {
  const normalizedAddress = normalizeChipnetAddress(address)
  if (!normalizedAddress) {
    throw new Error(`Invalid BCH chipnet address: "${address}"`)
  }

  const plainAddress = normalizedAddress.split(':')[1]
  // Watchtower chipnet expects the full bchtest: CashAddr in the route.
  // Keep the bare-hash value only for diagnostics in DEV logs.
  const addressCandidates = [normalizedAddress]
  if (import.meta.env.DEV && plainAddress) {
    console.info('[BitoHelp][bch-utxo] skipping plain address candidate', { plainAddress })
  }
  // Query without params fetches all UTXOs; confirmed=false adds mempool UTXOs
  // explicitly (some API versions require this for unconfirmed transactions).
  const queryCandidates = ['', '?confirmed=false']

  const seenOutpoints = new Set()
  const mergedUtxos = []

  for (const candidate of addressCandidates) {
    for (const query of queryCandidates) {
      const url = `${apiBaseUrl}utxo/bch/${candidate}/${query}`
      try {
        const response = await fetch(url)
        if (!response.ok) {
          console.warn('[BitoHelp][bch-utxo] HTTP error', { status: response.status, url })
          continue
        }

        const payload = await response.json()
        console.info('[BitoHelp][bch-utxo] raw response', { url, payload })

        // Watchtower: { valid, address, utxos: [...] }
        // Fulcrum REST: top-level array
        const utxoList = Array.isArray(payload?.utxos)
          ? payload.utxos
          : Array.isArray(payload)
            ? payload
            : []

        for (const rawUtxo of utxoList) {
          const parsed = sanitizeUtxo(rawUtxo)
          if (!parsed) {
            continue
          }

          const outpointKey = `${parsed.txid}:${parsed.vout}`
          if (seenOutpoints.has(outpointKey)) {
            continue
          }

          seenOutpoints.add(outpointKey)
          mergedUtxos.push(parsed)
        }
      } catch (fetchErr) {
        console.warn('[BitoHelp][bch-utxo] fetch error', { url, error: String(fetchErr) })
        continue
      }
    }
  }

  return mergedUtxos
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

  if (hashBytes.length !== 20) {
    throw new Error('Only 20-byte P2PKH/P2SH addresses are supported.')
  }

  if (decoded.type === 'P2PKH') {
    return new Uint8Array([0x76, 0xa9, 0x14, ...hashBytes, 0x88, 0xac])
  }

  if (decoded.type === 'P2SH') {
    return new Uint8Array([0xa9, 0x14, ...hashBytes, 0x87])
  }

  throw new Error('Unsupported BCH address type for donation outputs.')
}

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
}) => {
  const senderLockingBytecode = toLockingBytecode(senderAddress)
  const charityLockingBytecode = toLockingBytecode(charityAddress)
  const changeLockingBytecode = toLockingBytecode(changeAddress)
  const emptyUnlockingBytecode = '<Uint8Array: 0x>'
  const walletConnectSequenceNumber = 0

  const sourceOutputs = plan.inputs.map((utxo) => ({
    outpointIndex: utxo.vout,
    outpointTransactionHash: toExtendedJsonUint8Array(hexToBytes(utxo.txid)),
    sequenceNumber: walletConnectSequenceNumber,
    unlockingBytecode: emptyUnlockingBytecode,
    lockingBytecode: toExtendedJsonUint8Array(senderLockingBytecode),
    valueSatoshis: toExtendedJsonBigInt(utxo.valueSatoshis),
  }))

  const inputs = plan.inputs.map((utxo, index) => ({
    outpointIndex: utxo.vout,
    outpointTransactionHash: toExtendedJsonUint8Array(hexToBytes(utxo.txid)),
    sequenceNumber: walletConnectSequenceNumber,
    unlockingBytecode: emptyUnlockingBytecode,
    // Some Paytaca builds reconstruct input.sourceOutput from the separate
    // sourceOutputs array, while others read it directly from each input.
    // Include both forms for compatibility.
    sourceOutput: sourceOutputs[index],
  }))

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

  return {
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

export const broadcastRawTransaction = async ({ apiBaseUrl, rawTxHex }) => {
  const response = await fetch(`${apiBaseUrl}broadcast/`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ transaction: rawTxHex }),
  })

  if (!response.ok) {
    throw new Error('Transaction broadcast failed at provider API.')
  }

  const payload = await response.json()
  if (!payload?.success && !payload?.txid) {
    throw new Error(payload?.error || 'Broadcast API did not accept the signed transaction.')
  }

  return {
    txid: payload?.txid || null,
    raw: payload,
  }
}

const tryGetJson = async (url) => {
  const response = await fetch(url)
  if (!response.ok) {
    return null
  }
  return response.json()
}

const parseConfirmationCount = (payload) => {
  const details = payload?.details || payload
  const confirmations = Number(details?.confirmations)
  if (isFinitePositiveInteger(confirmations)) {
    return confirmations
  }

  const hasBlock = Number(details?.blockheight || details?.block_height || 0) > 0
  if (hasBlock) {
    return 1
  }

  return 0
}

export const fetchTransactionConfirmations = async ({ apiBaseUrl, txid }) => {
  const urls = [
    `${apiBaseUrl}transactions/${txid}/`,
    `${apiBaseUrl}transaction/${txid}/`,
    `${apiBaseUrl}tx/${txid}/`,
  ]

  for (const url of urls) {
    const payload = await tryGetJson(url)
    if (!payload) {
      continue
    }

    const confirmations = parseConfirmationCount(payload)
    return {
      confirmations,
      payload,
    }
  }

  return {
    confirmations: 0,
    payload: null,
  }
}

const sleep = (ms) => new Promise((resolve) => window.setTimeout(resolve, ms))

export const waitForConfirmations = async ({
  apiBaseUrl,
  txid,
  minConfirmations = 1,
  timeoutMs = DEFAULT_CONFIRMATION_TIMEOUT_MS,
  pollMs = DEFAULT_CONFIRMATION_POLL_MS,
}) => {
  const start = Date.now()

  while (Date.now() - start <= timeoutMs) {
    const { confirmations } = await fetchTransactionConfirmations({ apiBaseUrl, txid })
    if (confirmations >= minConfirmations) {
      return { confirmed: true, confirmations }
    }
    await sleep(pollMs)
  }

  return {
    confirmed: false,
    confirmations: 0,
  }
}
export const fetchAddressBalance = async ({ apiBaseUrl, address }) => {
  try {
    const utxos = await fetchAddressUtxos({ apiBaseUrl, address })
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

// Fetch BCH balance from the mainnet Watchtower API by converting the chipnet
// address to its bitcoincash: equivalent (same key, different network prefix).
export const fetchMainnetBalanceForChipnetAddress = async ({ address }) => {
  const mainnetAddress = chipnetAddressToMainnet(address)
  if (!mainnetAddress) {
    return 0
  }
  const apiBaseUrl = 'https://watchtower.cash/api/'
  const plainAddress = mainnetAddress.split(':')[1]
  const candidates = [mainnetAddress, plainAddress].filter(Boolean)
  const queries = ['', '?confirmed=false']
  const seenOutpoints = new Set()
  let totalSatoshis = 0n
  for (const candidate of candidates) {
    for (const query of queries) {
      const url = `${apiBaseUrl}utxo/bch/${candidate}/${query}`
      try {
        const response = await fetch(url)
        if (!response.ok) {
          console.warn('[BitoHelp][bch-mainnet-utxo] HTTP error', { status: response.status, url })
          continue
        }
        const payload = await response.json()
        console.info('[BitoHelp][bch-mainnet-utxo] raw response', { url, payload })
        const utxoList = Array.isArray(payload?.utxos)
          ? payload.utxos
          : Array.isArray(payload)
            ? payload
            : []
        for (const rawUtxo of utxoList) {
          const parsed = sanitizeUtxo(rawUtxo)
          if (!parsed) continue
          const key = `${parsed.txid}:${parsed.vout}`
          if (seenOutpoints.has(key)) continue
          seenOutpoints.add(key)
          totalSatoshis += parsed.valueSatoshis
        }
      } catch (err) {
        console.warn('[BitoHelp][bch-mainnet-utxo] fetch error', { url, error: String(err) })
      }
    }
  }
  return Number(totalSatoshis) / 100000000
}

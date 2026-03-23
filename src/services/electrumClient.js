/**
 * Lightweight Electrum (Fulcrum) JSON-RPC client over WebSocket.
 * Used for BCH chipnet UTXO lookups, transaction broadcast, and confirmation checks.
 *
 * Protocol reference: https://electrum-cash-protocol.readthedocs.io/en/latest/
 */

const CHIPNET_FULCRUM_SERVERS = [
  'wss://chipnet.imaginary.cash:50004',
  'wss://chipnet.bch.ninja:50004',
]

const REQUEST_TIMEOUT_MS = 15000
const CONNECT_TIMEOUT_MS = 10000
const CLIENT_NAME = 'BitoHelp'
const PROTOCOL_VERSION = '1.4'

let activeSocket = null
let activeServerUrl = null
let requestIdCounter = 0
let pendingRequests = new Map()
let connectPromise = null
let negotiated = false

const cleanup = () => {
  if (activeSocket) {
    try {
      activeSocket.close()
    } catch {
      /* ignore */
    }
  }
  activeSocket = null
  activeServerUrl = null
  connectPromise = null
  negotiated = false

  for (const [, entry] of pendingRequests) {
    entry.reject(new Error('Electrum connection closed'))
  }
  pendingRequests = new Map()
}

const connectToServer = (url) =>
  new Promise((resolve, reject) => {
    const ws = new WebSocket(url)
    const timer = setTimeout(() => {
      ws.close()
      reject(new Error(`Electrum connect timeout: ${url}`))
    }, CONNECT_TIMEOUT_MS)

    ws.addEventListener('open', () => {
      clearTimeout(timer)
      resolve(ws)
    })

    ws.addEventListener('error', () => {
      clearTimeout(timer)
      reject(new Error(`Electrum connect failed: ${url}`))
    })
  })

const handleMessage = (event) => {
  let parsed
  try {
    parsed = JSON.parse(event.data)
  } catch {
    return
  }

  const entry = pendingRequests.get(parsed.id)
  if (!entry) return

  pendingRequests.delete(parsed.id)
  clearTimeout(entry.timer)

  if (parsed.error) {
    entry.reject(new Error(parsed.error.message || JSON.stringify(parsed.error)))
  } else {
    entry.resolve(parsed.result)
  }
}

const handleClose = () => {
  cleanup()
}

const ensureConnected = async () => {
  if (activeSocket && activeSocket.readyState === WebSocket.OPEN && negotiated) {
    return
  }

  // Prevent concurrent connection attempts
  if (connectPromise) {
    await connectPromise
    return
  }

  cleanup()

  connectPromise = (async () => {
    let lastError = null
    for (const url of CHIPNET_FULCRUM_SERVERS) {
      try {
        const ws = await connectToServer(url)
        ws.addEventListener('message', handleMessage)
        ws.addEventListener('close', handleClose)
        activeSocket = ws
        activeServerUrl = url

        // Protocol version negotiation (required by Electrum protocol)
        await sendRequest('server.version', [CLIENT_NAME, PROTOCOL_VERSION])
        negotiated = true
        return
      } catch (e) {
        lastError = e
      }
    }
    throw lastError || new Error('All Fulcrum servers unreachable')
  })()

  try {
    await connectPromise
  } finally {
    connectPromise = null
  }
}

const sendRequest = (method, params = []) =>
  new Promise((resolve, reject) => {
    if (!activeSocket || activeSocket.readyState !== WebSocket.OPEN) {
      reject(new Error('Electrum socket not connected'))
      return
    }

    const id = ++requestIdCounter
    const timer = setTimeout(() => {
      pendingRequests.delete(id)
      reject(new Error(`Electrum request timeout: ${method}`))
    }, REQUEST_TIMEOUT_MS)

    pendingRequests.set(id, { resolve, reject, timer })

    activeSocket.send(JSON.stringify({ jsonrpc: '2.0', method, params, id }))
  })

/**
 * Call an Electrum method, connecting if necessary.
 * Retries once on connection failure.
 */
export const electrumRequest = async (method, params = []) => {
  try {
    await ensureConnected()
    return await sendRequest(method, params)
  } catch (firstErr) {
    // Retry once with a fresh connection
    cleanup()
    try {
      await ensureConnected()
      return await sendRequest(method, params)
    } catch {
      throw firstErr
    }
  }
}

/**
 * Get unspent outputs for a BCH address.
 * Returns array of { tx_hash, tx_pos, height, value } where value is in satoshis.
 */
export const getAddressUtxos = async (address) => {
  return electrumRequest('blockchain.address.listunspent', [address])
}

/**
 * Broadcast a raw transaction hex to the network.
 * Returns the transaction id on success.
 */
export const broadcastTransaction = async (rawTxHex) => {
  return electrumRequest('blockchain.transaction.broadcast', [rawTxHex])
}

/**
 * Get transaction details including confirmation count.
 * @param {string} txid
 * @returns {{ confirmations: number, blockhash?: string }}
 */
export const getTransaction = async (txid) => {
  return electrumRequest('blockchain.transaction.get', [txid, true])
}

/**
 * Disconnect the active Electrum session.
 */
export const disconnect = () => {
  cleanup()
}

/**
 * Get the currently connected server URL (for diagnostics).
 */
export const getActiveServer = () => activeServerUrl

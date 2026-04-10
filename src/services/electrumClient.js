/**
 * Watchtower REST API client for BCH.
 * Used for UTXO lookups, transaction broadcast, and confirmation checks.
 *
 * Network selection is driven by the Pinia network store.
 */

import { useNetworkStore } from '../stores/network-store'

const CHIPNET_BASE = 'https://chipnet.watchtower.cash/api'
const MAINNET_BASE = 'https://watchtower.cash/api'
const REQUEST_TIMEOUT_MS = 15000

const getActiveBaseUrl = () => {
  try {
    const networkStore = useNetworkStore()
    return networkStore.isMainnet ? MAINNET_BASE : CHIPNET_BASE
  } catch {
    // Store may not be initialised yet (e.g. during SSR bootstrap)
    return CHIPNET_BASE
  }
}

const getBaseUrl = (address) => {
  if (typeof address === 'string' && address.startsWith('bitcoincash:')) {
    return MAINNET_BASE
  }
  if (typeof address === 'string' && address.startsWith('bchtest:')) {
    return CHIPNET_BASE
  }
  return getActiveBaseUrl()
}

const fetchWithTimeout = async (url, options = {}) => {
  const controller = new AbortController()
  const timer = setTimeout(() => controller.abort(), REQUEST_TIMEOUT_MS)
  try {
    const response = await fetch(url, { ...options, signal: controller.signal })
    return response
  } finally {
    clearTimeout(timer)
  }
}

/**
 * Get unspent outputs for a BCH address.
 * Returns array of { tx_hash, tx_pos, height, value } (Electrum-compatible shape).
 */
export const getAddressUtxos = async (address) => {
  const base = getBaseUrl(address)
  const url = `${base}/utxo/bch/${encodeURIComponent(address)}/`
  const response = await fetchWithTimeout(url)

  if (!response.ok) {
    throw new Error(`Watchtower UTXO request failed (${response.status})`)
  }

  const data = await response.json()

  if (!data?.valid) {
    throw new Error(`Watchtower reports invalid address: ${address}`)
  }

  // Map Watchtower format to Electrum-compatible format consumed by bchChipnet.js
  return (data.utxos || []).map((utxo) => ({
    tx_hash: utxo.txid,
    tx_pos: utxo.vout,
    height: utxo.block || 0,
    value: utxo.value,
  }))
}

/**
 * Broadcast a raw transaction hex to the network.
 * Returns the transaction id on success.
 */
export const broadcastTransaction = async (rawTxHex) => {
  const url = `${getActiveBaseUrl()}/broadcast/`
  const response = await fetchWithTimeout(url, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ transaction: rawTxHex }),
  })

  if (!response.ok) {
    const errorText = await response.text().catch(() => '')
    throw new Error(`Watchtower broadcast failed (${response.status}): ${errorText}`)
  }

  const data = await response.json()
  const txid = data?.txid || data?.tx_hash || data?.transaction_hash || null

  if (!txid) {
    throw new Error('Watchtower broadcast succeeded but no txid returned.')
  }

  return txid
}

/**
 * Get transaction details including confirmation count.
 * @param {string} txid
 * @returns {{ confirmations: number }}
 */
export const getTransaction = async (txid) => {
  const url = `${getActiveBaseUrl()}/tx/bch/${encodeURIComponent(txid)}/`
  const response = await fetchWithTimeout(url)

  if (!response.ok) {
    throw new Error(`Watchtower tx lookup failed (${response.status})`)
  }

  const data = await response.json()
  return {
    confirmations: data?.confirmations ?? 0,
    blockhash: data?.block_hash || data?.blockhash || null,
  }
}

/**
 * Disconnect — no-op for REST client (kept for API compatibility).
 */
export const disconnect = () => {}

/**
 * Get the currently active API base URL (for diagnostics).
 */
export const getActiveServer = () => getActiveBaseUrl()

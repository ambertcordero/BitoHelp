// BCH utility functions

export function isValidBCHAddress(address) {
  if (!address || typeof address !== 'string') return false

  const cashAddrRegex = /^(bitcoincash|bchtest):[qpzry9x8gf2tvdw0s3jn54khce6mua7l]{42}$/i
  const legacyRegex = /^[13mnMN][a-km-zA-HJ-NP-Z1-9]{25,34}$/

  return cashAddrRegex.test(address) || legacyRegex.test(address)
}

/**
 * Validate an address for a specific network prefix.
 * @param {string} address
 * @param {'bitcoincash'|'bchtest'} prefix
 */
export function isValidBCHAddressForPrefix(address, prefix) {
  if (!address || typeof address !== 'string') return false
  const cashAddrRegex = new RegExp(`^${prefix}:[qpzry9x8gf2tvdw0s3jn54khce6mua7l]{42}$`, 'i')
  return cashAddrRegex.test(address)
}

export function formatBCH(satoshis) {
  const bch = satoshis / 100000000
  return bch.toFixed(8) + ' BCH'
}

export function bchToSatoshis(bch) {
  return Math.floor(bch * 100000000)
}

export function satoshisToBCH(satoshis) {
  return satoshis / 100000000
}

export function shortenAddress(address, prefixLength = 10, suffixLength = 8) {
  if (!address || address.length <= prefixLength + suffixLength) return address
  return `${address.slice(0, prefixLength)}...${address.slice(-suffixLength)}`
}

export function getExplorerUrl(txid, isTestnet = false) {
  if (isTestnet) return `https://chipnet.watchtower.cash/tx/${txid}`
  return `https://watchtower.cash/tx/${txid}`
}

export function getAddressExplorerUrl(address, isTestnet = false) {
  if (isTestnet) return `https://chipnet.watchtower.cash/address/${address}`
  return `https://watchtower.cash/address/${address}`
}

export function calculateTxFee(inputCount = 1, outputCount = 2, feeRate = 1) {
  const estimatedSize = inputCount * 148 + outputCount * 34 + 10
  return estimatedSize * feeRate
}

export function formatDate(timestamp) {
  const date = new Date(timestamp * 1000)
  return date.toLocaleString()
}

export function validateDonationAmount(amount) {
  const minDonation = 0.0001
  const maxDonation = 100

  if (!amount || isNaN(amount)) {
    return { isValid: false, message: 'Please enter a valid amount' }
  }

  if (amount < minDonation) {
    return { isValid: false, message: `Minimum donation is ${minDonation} BCH` }
  }

  if (amount > maxDonation) {
    return { isValid: false, message: `Maximum donation is ${maxDonation} BCH per transaction` }
  }

  return { isValid: true, message: 'Valid amount' }
}

export default {
  isValidBCHAddress,
  isValidBCHAddressForPrefix,
  formatBCH,
  bchToSatoshis,
  satoshisToBCH,
  shortenAddress,
  getExplorerUrl,
  getAddressExplorerUrl,
  calculateTxFee,
  formatDate,
  validateDonationAmount,
}

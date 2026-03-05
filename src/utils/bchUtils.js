/**
 * BCH Utilities
 * Helper functions for Bitcoin Cash operations
 */

/**
 * Validates a Bitcoin Cash address
 * @param {string} address 
 * @returns {boolean} 
 */
export function isValidBCHAddress(address) {
  if (!address || typeof address !== 'string') {
    return false
  }
  
  
  const cashAddrRegex = /^(bitcoincash|bchtest):[qpzry9x8gf2tvdw0s3jn54khce6mua7l]{42}$/i
  const legacyRegex = /^[13mnMN][a-km-zA-HJ-NP-Z1-9]{25,34}$/
  
  return cashAddrRegex.test(address) || legacyRegex.test(address)
}

/**
 * Formats BCH amount from satoshis to BCH
 * @param {number} satoshis 
 * @returns {string} 
 */
export function formatBCH(satoshis) {
  const bch = satoshis / 100000000
  return bch.toFixed(8) + ' BCH'
}

/**
 * Converts BCH to satoshis
 * @param {number} bch 
 * @returns {number} 
 */
export function bchToSatoshis(bch) {
  return Math.floor(bch * 100000000)
}

/**
 * Converts satoshis to BCH
 * @param {number} satoshis 
 * @returns {number} 
 */
export function satoshisToBCH(satoshis) {
  return satoshis / 100000000
}

/**
 * Shortens a BCH address for display
 * @param {string} address 
 * @param {number} prefixLength 
 * @param {number} suffixLength 
 * @returns {string} 
 */
export function shortenAddress(address, prefixLength = 10, suffixLength = 8) {
  if (!address || address.length <= prefixLength + suffixLength) {
    return address
  }
  return `${address.slice(0, prefixLength)}...${address.slice(-suffixLength)}`
}

/**
 * Gets the explorer URL for a transaction
 * @param {string} txid 
 * @param {boolean} isTestnet 
 * @returns {string} 
 */
export function getExplorerUrl(txid, isTestnet = false) {
  if (isTestnet) {
    return `https://chipnet.chaingraph.cash/tx/${txid}`
  }
  return `https://explorer.bitcoin.com/bch/tx/${txid}`
}

/**
 * Gets the address explorer URL
 * @param {string} address 
 * @param {boolean} isTestnet 
 * @returns {string} 
 */
export function getAddressExplorerUrl(address, isTestnet = false) {
  if (isTestnet) {
    return `https://chipnet.chaingraph.cash/address/${address}`
  }
  return `https://explorer.bitcoin.com/bch/address/${address}`
}

/**
 * Calculates transaction fee
 * @param {number} inputCount 
 * @param {number} outputCount 
 * @param {number} feeRate 
 * @returns {number} 
 */
export function calculateTxFee(inputCount = 1, outputCount = 2, feeRate = 1) {
 
  const estimatedSize = (inputCount * 148) + (outputCount * 34) + 10
  return estimatedSize * feeRate
}

/**
 * Formats a timestamp to readable date
 * @param {number} timestamp 
 * @returns {string} 
 */
export function formatDate(timestamp) {
  const date = new Date(timestamp * 1000)
  return date.toLocaleString()
}

/**
 * Validates donation amount
 * @param {number} amount 
 * @returns {object} 
 */
export function validateDonationAmount(amount) {
  const minDonation = 0.0001 
  const maxDonation = 100 
  
  if (!amount || isNaN(amount)) {
    return {
      isValid: false,
      message: 'Please enter a valid amount'
    }
  }
  
  if (amount < minDonation) {
    return {
      isValid: false,
      message: `Minimum donation is ${minDonation} BCH`
    }
  }
  
  if (amount > maxDonation) {
    return {
      isValid: false,
      message: `Maximum donation is ${maxDonation} BCH per transaction`
    }
  }
  
  return {
    isValid: true,
    message: 'Valid amount'
  }
}

export default {
  isValidBCHAddress,
  formatBCH,
  bchToSatoshis,
  satoshisToBCH,
  shortenAddress,
  getExplorerUrl,
  getAddressExplorerUrl,
  calculateTxFee,
  formatDate,
  validateDonationAmount
}

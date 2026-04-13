import { api } from 'src/boot/axios'

/**
 * Fetch donations for a specific wallet address.
 */
export async function fetchDonorDonations({ walletAddress, limit = 50 }) {
  const addr = (walletAddress || '').toLowerCase().trim()
  if (!addr) return []
  const { data } = await api.get(`users/${encodeURIComponent(addr)}/donations/?limit=${limit}`)
  return Array.isArray(data) ? data : data.results || []
}

/**
 * Fetch donor profile + stats for a wallet address.
 * Returns { user, donations, stats: { total_donated, donation_count } }
 */
export async function fetchDonorProfile({ walletAddress }) {
  const addr = (walletAddress || '').toLowerCase().trim()
  if (!addr) return null
  const { data } = await api.get(`users/${encodeURIComponent(addr)}/profile/`)
  return data
}

/**
 * Fetch global donation stats.
 * Returns { total_donations, total_amount, by_cause, by_coin }
 */
export async function fetchGlobalStats() {
  const { data } = await api.get('stats/')
  return data
}

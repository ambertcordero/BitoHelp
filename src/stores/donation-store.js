import { defineStore, acceptHMRUpdate } from 'pinia'
import { api } from 'src/boot/axios'

export const useDonationStore = defineStore('donation', {
  state: () => ({
    latestDonation: null,
    donationHistory: [],
    totalDonated: 0,
    isLoading: false,
    error: null,
    walletUser: null,
    connectedWalletAddress: '',
  }),

  getters: {
    hasRecentDonation: (state) => state.latestDonation !== null,

    getDonationCount: (state) => state.donationHistory.length,

    getTotalAmount: (state) => {
      return state.donationHistory.reduce((total, donation) => {
        return total + (parseFloat(donation.amount) || 0)
      }, 0)
    },

    getDonationsByCause: (state) => {
      return (cause) => {
        return state.donationHistory.filter((d) => d.cause === cause)
      }
    },
  },

  actions: {
    async addDonation(donationData) {
      this.isLoading = true
      this.error = null

      try {
        console.log('Sending donation to API:', donationData)

        const payload = {
          txid: donationData.txid,
          recipient: donationData.recipient,
          amount: donationData.amount.toString(),
          coin: donationData.coin || 'Bitcoin Cash (BCH)',
          cause: donationData.cause,
          message: donationData.message || '',
          donor_name: donationData.donorName || '',
          donor_email: donationData.donorEmail || '',
          donor_contact: donationData.donorContact || '',
          explorer_url: donationData.explorerUrl,
          interval: donationData.interval || '',
          nonprofit: donationData.nonprofitId || null,
          wallet_address: (
            donationData.walletAddress ||
            this.connectedWalletAddress ||
            ''
          ).toLowerCase(),
        }

        console.log('API Payload:', payload)
        const response = await api.post('donations/', payload)
        console.log('API Response:', response)

        const donation = response.data
        this.latestDonation = donation
        this.donationHistory.unshift(donation)

        if (this.donationHistory.length > 50) {
          this.donationHistory = this.donationHistory.slice(0, 50)
        }

        this.totalDonated += parseFloat(donation.amount) || 0
        this.saveDonationsToStorage()

        return donation
      } catch (error) {
        console.error('API save failed - Full Error:', error)
        console.error('Error Response:', error.response)
        console.error('Error Request:', error.request)
        console.error('Error Message:', error.message)
        this.error = error.response?.data || error.message

        const localDonation = {
          id: Date.now(),
          ...donationData,
          timestamp: new Date().toISOString(),
        }
        this.latestDonation = localDonation
        this.donationHistory.unshift(localDonation)
        this.totalDonated += donationData.amount || 0
        this.saveDonationsToStorage()

        throw error
      } finally {
        this.isLoading = false
      }
    },

    async fetchDonations(limit = 20) {
      this.isLoading = true
      this.error = null

      try {
        const params = new URLSearchParams({ limit })
        if (this.connectedWalletAddress) {
          params.set('wallet', this.connectedWalletAddress.toLowerCase())
        }
        const response = await api.get(`donations/?${params}`)
        this.donationHistory = response.data.results || response.data
      } catch (error) {
        console.error('Failed to fetch donations:', error)
        this.error = error.response?.data || error.message
        this.loadDonationsFromStorage()
      } finally {
        this.isLoading = false
      }
    },

    async fetchStats() {
      try {
        const response = await api.get('stats/')
        return response.data
      } catch (error) {
        console.error('Failed to fetch stats:', error)
        return null
      }
    },

    clearLatestDonation() {
      this.latestDonation = null
    },

    saveDonationsToStorage() {
      try {
        localStorage.setItem('donationHistory', JSON.stringify(this.donationHistory))
        localStorage.setItem('totalDonated', this.totalDonated.toString())
      } catch (error) {
        console.error('Failed to save donations to storage:', error)
      }
    },

    loadDonationsFromStorage() {
      try {
        const history = localStorage.getItem('donationHistory')
        const total = localStorage.getItem('totalDonated')

        if (history) {
          this.donationHistory = JSON.parse(history)
        }

        if (total) {
          this.totalDonated = parseFloat(total)
        }
      } catch (error) {
        console.error('Failed to load donations from storage:', error)
      }
    },

    clearHistory() {
      this.donationHistory = []
      this.latestDonation = null
      this.totalDonated = 0
      localStorage.removeItem('donationHistory')
      localStorage.removeItem('totalDonated')
    },

    async connectWallet(walletAddress) {
      const addr = (walletAddress || '').toLowerCase().trim()
      if (!addr) return
      this.connectedWalletAddress = addr
      try {
        const response = await api.post('users/connect/', { wallet_address: addr })
        this.walletUser = response.data
      } catch (error) {
        console.error('Failed to register wallet user:', error)
      }
    },

    setWalletAddress(walletAddress) {
      this.connectedWalletAddress = (walletAddress || '').toLowerCase().trim()
    },

    disconnectWallet() {
      this.connectedWalletAddress = ''
      this.walletUser = null
      this.donationHistory = []
      this.totalDonated = 0
    },

    async fetchWalletDonations(walletAddress, limit = 50) {
      const addr = (walletAddress || this.connectedWalletAddress || '').toLowerCase().trim()
      if (!addr) return []
      this.isLoading = true
      this.error = null
      try {
        const response = await api.get(
          `users/${encodeURIComponent(addr)}/donations/?limit=${limit}`,
        )
        this.donationHistory = response.data || []
        this.totalDonated = this.donationHistory.reduce(
          (sum, d) => sum + (parseFloat(d.amount) || 0),
          0,
        )
        return this.donationHistory
      } catch (error) {
        console.error('Failed to fetch wallet donations:', error)
        this.error = error.response?.data || error.message
        return []
      } finally {
        this.isLoading = false
      }
    },
  },
})

if (import.meta.hot) {
  import.meta.hot.accept(acceptHMRUpdate(useDonationStore, import.meta.hot))
}

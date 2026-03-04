import { defineStore, acceptHMRUpdate } from 'pinia'
import { api } from 'src/boot/axios'

export const useDonationStore = defineStore('donation', {
  state: () => ({
    latestDonation: null,
    donationHistory: [],
    totalDonated: 0,
    isLoading: false,
    error: null,
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
        return state.donationHistory.filter(d => d.cause === cause)
      }
    }
  },

  actions: {
    async addDonation(donationData) {
      this.isLoading = true
      this.error = null
      
      try {
        // Save to Django API
        const response = await api.post('donations/', {
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
        })
        
        const donation = response.data
        this.latestDonation = donation
        this.donationHistory.unshift(donation)
        
        // Keep only last 50 donations in memory
        if (this.donationHistory.length > 50) {
          this.donationHistory = this.donationHistory.slice(0, 50)
        }
        
        this.totalDonated += parseFloat(donation.amount) || 0
        
        // Also save to localStorage as backup
        this.saveDonationsToStorage()
        
        console.log('✅ Donation saved to Django API:', donation)
        return donation
      } catch (error) {
        console.error('❌ Failed to save donation to API:', error)
        this.error = error.response?.data || error.message
        
        // Fallback: save to localStorage only
        const localDonation = {
          id: Date.now(),
          ...donationData,
          timestamp: new Date().toISOString()
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
        const response = await api.get(`donations/?limit=${limit}`)
        this.donationHistory = response.data.results || response.data
        console.log(`✅ Fetched ${this.donationHistory.length} donations from API`)
      } catch (error) {
        console.error('❌ Failed to fetch donations:', error)
        this.error = error.response?.data || error.message
        // Load from localStorage as fallback
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
        console.error('❌ Failed to fetch stats:', error)
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
    }
  },
})

if (import.meta.hot) {
  import.meta.hot.accept(acceptHMRUpdate(useDonationStore, import.meta.hot))
}

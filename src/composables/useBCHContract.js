import { ref, computed } from 'vue'
import { ElectrumNetworkProvider } from 'cashscript'
import { TestNetWallet } from 'mainnet-js'
import { 
  isValidBCHAddress, 
  bchToSatoshis,
  getExplorerUrl,
  validateDonationAmount 
} from '../utils/bchUtils'


const wallet = ref(null)
const walletAddress = ref('')
const walletBalance = ref(0)
const isConnected = ref(false)
const networkProvider = ref(null)
const mecenasContract = ref(null)
const isTestnet = ref(true)
const isTestMode = ref(true) 

export function useBCHContract() {
  
  const initializeNetwork = async () => {
    try {
     
      if (isTestnet.value) {
        networkProvider.value = new ElectrumNetworkProvider('chipnet')
      } else {
        networkProvider.value = new ElectrumNetworkProvider('mainnet')
      }
      console.log('BCH Network provider initialized')
    } catch (error) {
      console.error('Failed to initialize network:', error)
      throw error
    }
  }


  const connectWallet = async () => {
    try {
      if (isTestMode.value) {
        console.log('Using test wallet for development')
        walletAddress.value = 'bitcoincash:qp3wjpa3tjlj042z2wv7hahsldgwhwy0rq9sywjpyy'
        walletBalance.value = 100000000
        isConnected.value = true
        return
      }
      
      if (typeof window !== 'undefined' && window.bitcoincom) {
        const accounts = await window.bitcoincom.getAccounts()
        if (accounts && accounts.length > 0) {
          walletAddress.value = accounts[0]
          isConnected.value = true
          window.bitcoincom.getBalance().then(balance => {
            walletBalance.value = balance
          }).catch(err => console.warn('Balance fetch failed:', err))
        }
      } else {
        const testWallet = await TestNetWallet.newRandom()
        wallet.value = testWallet
        walletAddress.value = testWallet.cashaddr
        isConnected.value = true
        testWallet.getBalance('sat').then(balance => {
          walletBalance.value = balance
        }).catch(err => console.warn('Balance unavailable:', err))
      }
      
      initializeNetwork().catch(err => console.warn('Network init delayed:', err))
      console.log('Wallet connected:', walletAddress.value)
    } catch (error) {
      console.error('Wallet connection failed:', error)
      throw error
    }
  }

 
  const disconnectWallet = () => {
    wallet.value = null
    walletAddress.value = ''
    walletBalance.value = 0
    isConnected.value = false
    mecenasContract.value = null
  }


  const deployMecenasContract = async (recipientAddress, pledgeAmount) => {
    try {
      if (!networkProvider.value) await initializeNetwork()

      const contractInfo = {
        address: 'mecenas_contract_' + Date.now(),
        recipient: recipientAddress,
        funder: walletAddress.value,
        pledge: pledgeAmount,
        balance: 0
      }
      
      mecenasContract.value = contractInfo
      return contractInfo
    } catch (error) {
      console.error('Contract deployment failed:', error)
      throw error
    }
  }

  
  const sendDonation = async (donationData) => {
    try {
      const { recipient, amount, message, cause, coin, donorName, donorEmail } = donationData
      
      if (isTestMode.value) {
        await new Promise(resolve => setTimeout(resolve, 1500))
        const mockTxId = 'test_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9)
        return {
          success: true,
          txid: mockTxId,
          explorerUrl: `https://explorer.bitcoin.com/bch/tx/${mockTxId}`,
          donationData: {
            cause,
            amount,
            coin,
            recipient,
            message,
            donorName,
            donorEmail,
            timestamp: new Date().toISOString()
          }
        }
      }
      
     
      if (!isConnected.value) {
        throw new Error('Wallet not connected')
      }
    
      if (!isValidBCHAddress(recipient)) {
        throw new Error('Invalid BCH address')
      }
      
      const validation = validateDonationAmount(amount)
      if (!validation.isValid) {
        throw new Error(validation.message)
      }
      
      if (wallet.value) {
        const amountInSatoshis = bchToSatoshis(amount)
        const result = await wallet.value.send([
          {
            cashaddr: recipient,
            value: amountInSatoshis,
            unit: 'sat'
          }
        ])

        return {
          success: true,
          txid: result.txId,
          explorerUrl: getExplorerUrl(result.txId, isTestnet.value),
          donationData: {
            cause,
            amount,
            coin,
            recipient,
            message,
            donorName,
            donorEmail,
            timestamp: new Date().toISOString()
          }
        }
      } else if (window.bitcoincom) {
        const result = await window.bitcoincom.send({
          to: recipient,
          amount: amount,
          currency: 'BCH'
        })

        return {
          success: true,
          txid: result.txid,
          explorerUrl: getExplorerUrl(result.txid, isTestnet.value),
          donationData: {
            cause,
            amount,
            coin,
            recipient,
            message,
            donorName,
            donorEmail,
            timestamp: new Date().toISOString()
          }
        }
      }

      throw new Error('No valid wallet available')
    } catch (error) {
      console.error('Donation failed:', error)
      throw error
    }
  }

  const getTransactionHistory = async () => {
    try {
      if (!wallet.value) {
        return []
      }

      const history = await wallet.value.getHistory()
      return history
    } catch (error) {
      console.error('History fetch failed:', error)
      return []
    }
  }

  const triggerRecurringPayment = async () => {
    if (isTestMode.value) {
      await new Promise(resolve => setTimeout(resolve, 1000))
      const mockTxId = 'recurring_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9)
      return {
        success: true,
        txid: mockTxId,
        message: 'Recurring payment triggered successfully'
      }
    }

    if (!isConnected.value) throw new Error('Wallet not connected')
    throw new Error('Contract interaction not yet implemented')
  }

  const reclaimFunds = async () => {
    if (isTestMode.value) {
      await new Promise(resolve => setTimeout(resolve, 1000))
      const mockTxId = 'reclaim_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9)
      return {
        success: true,
        txid: mockTxId,
        message: 'Funds reclaimed successfully'
      }
    }

    if (!isConnected.value) throw new Error('Wallet not connected')
    throw new Error('Contract interaction not yet implemented')
  }

  const formattedBalance = computed(() => {
    return (walletBalance.value / 100000000).toFixed(8) + ' BCH'
  })

  const shortAddress = computed(() => {
    if (!walletAddress.value) return ''
    return walletAddress.value.slice(0, 10) + '...' + walletAddress.value.slice(-8)
  })

  return {
    wallet,
    walletAddress,
    walletBalance,
    isConnected,
    isTestnet,
    isTestMode,
    formattedBalance,
    shortAddress,
    connectWallet,
    disconnectWallet,
    deployMecenasContract,
    sendDonation,
    triggerRecurringPayment,
    reclaimFunds,
    getTransactionHistory,
    initializeNetwork,
    mecenasContract
  }
}

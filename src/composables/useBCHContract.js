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
const donationContract = ref(null)
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
        console.log(' TEST MODE: Simulating wallet connection')
        
    
        walletAddress.value = 'bitcoincash:qp3wjpa3tjlj042z2wv7hahsldgwhwy0rq9sywjpyy'
        walletBalance.value = 100000000 
        isConnected.value = true
        
        console.log(' Test wallet connected instantly:', walletAddress.value)
        return
      }
      
      
      if (typeof window !== 'undefined' && window.bitcoincom) {
        console.log('Connecting to Bitcoin.com wallet...')
        const accounts = await window.bitcoincom.getAccounts()
        if (accounts && accounts.length > 0) {
          walletAddress.value = accounts[0]
          isConnected.value = true
 
          
          window.bitcoincom.getBalance().then(balance => {
            walletBalance.value = balance
          }).catch(err => console.warn('Could not fetch balance:', err))
        }
      } else {
        
        console.log('No wallet extension found, creating test wallet...')
        const testWallet = await TestNetWallet.newRandom()
        wallet.value = testWallet
        walletAddress.value = testWallet.cashaddr
        isConnected.value = true
        
        
        testWallet.getBalance('sat').then(balance => {
          walletBalance.value = balance
        }).catch(err => console.warn('Could not fetch balance:', err))
      }
      
      
      initializeNetwork().catch(err => console.warn('Network init warning:', err))
      
      console.log(' Wallet connected:', walletAddress.value)
    } catch (error) {
      console.error('Failed to connect wallet:', error)
      throw error
    }
  }

 
  const disconnectWallet = () => {
    wallet.value = null
    walletAddress.value = ''
    walletBalance.value = 0
    isConnected.value = false
    donationContract.value = null
  }


  const deployDonationContract = async (nonprofitAddress) => {
    try {
      if (!networkProvider.value) {
        await initializeNetwork()
      }

      
      console.log('Deploying donation contract for nonprofit:', nonprofitAddress)
      
      
      return {
        address: 'contract_address_placeholder',
        nonprofitAddress: nonprofitAddress
      }
    } catch (error) {
      console.error('Failed to deploy contract:', error)
      throw error                         
    }
  }

  
  const sendDonation = async (donationData) => {
    try {
      const { recipient, amount, message, cause, coin, donorName, donorEmail, donorContact } = donationData
      
      
      if (isTestMode.value) {
        console.log('TEST MODE: Simulating donation transaction')
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
      
      console.log('Sending donation:', {
        cause: cause || 'Not specified',
        recipient,
        amount,
        coin: coin || 'BCH',
        message,
        donor: {
          name: donorName,
          email: donorEmail,
          contact: donorContact
        }
      })

      
      if (wallet.value) {
        const amountInSatoshis = bchToSatoshis(amount)
        
      
        const result = await wallet.value.send([
          {
            cashaddr: recipient,
            value: amountInSatoshis,
            unit: 'sat'
          }
        ])

        console.log('Donation sent successfully:', result)
        
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
      console.error('Failed to send donation:', error)
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
      console.error('Failed to get transaction history:', error)
      return []
    }
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
    deployDonationContract,
    sendDonation,
    getTransactionHistory,
    initializeNetwork
  }
}

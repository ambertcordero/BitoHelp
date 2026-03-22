<template>
  <q-page class="donation-page">

    <div class="donation-wrapper">

      <!-- LEFT SIDE ini !!!-->
      <div class="donation-form">

        <div class="row items-center q-col-gutter-md">
          <div class="col">
            <h1>Where your crypto creates a better tomorrow.</h1>
            <p class="subtitle">
              By donating crypto, you unlock smarter, more efficient giving.<br/>Support thousands of verified nonprofits through blockchain-powered donations.
            </p>
          </div>
        </div>

        <q-select 
          v-model="form.cause" 
          :options="nonprofitOptions"
          option-label="label"
          option-value="value"
          emit-value
          map-options
          outlined 
          label="Choose non-profit or a cause" 
          class="q-mb-md"
          :loading="loadingNonprofits"
          :disable="loadingNonprofits"
        >
          <template v-slot:option="scope">
            <q-item v-bind="scope.itemProps">
              <q-item-section>
                <q-item-label>{{ scope.opt.label }}</q-item-label>
                <q-item-label caption>{{ scope.opt.address }}</q-item-label>
              </q-item-section>
            </q-item>
          </template>
        </q-select>
        <q-input 
          v-model="form.recipientAddress" 
          outlined 
          label="Recipient BCH Address" 
          hint="Address auto-filled when nonprofit is selected"
          readonly
          class="q-mb-md" 
        />
        <div class="row q-col-gutter-md">
          <div class="col">
            <q-select v-model="form.coin" :options="cryptoOptions" label="Choose a coin" outlined dense class="q-mb-md"/>
          </div>
          <div class="col">
            <q-input 
              v-model.number="form.amount" 
              outlined 
              label="Amount" 
              type="number"
              step="0.00000001"
              min="0"
              :suffix="form.coin || 'BCH'"
            />
          </div>
        </div>  

        <q-input
          v-model="form.message"
          outlined
          type="textarea"
          label="Message here for non-profit (area of intent)"
          class="q-mt-md"
        />

        <!-- Donation Schedule -->
        <div class="q-mt-lg">
          <div class="section-title">Donation Schedule</div>

          <q-select
            v-model="form.interval"
            :options="intervalOptions"
            map-options
            emit-value
            outlined
            label="Donation Interval"
            :hint="!form.contract ? 'Please select a contract first' : 'Select how often you want to donate'"
            placeholder="Choose donation frequency"
            clearable
            class="q-mb-md"
            :disable="!form.contract"
          >
            <template v-slot:prepend>
              <q-icon name="schedule" />
            </template>
          </q-select>

          <q-select
            v-model="form.contract"
            :options="contractOptions"
            map-options
            emit-value
            outlined
            label="Contract Duration"
            hint="Select contract period for recurring donations"
            placeholder="Choose contract duration"
            clearable
            class="q-mb-md"
          >
            <template v-slot:prepend>
              <q-icon name="description" />
            </template>
          </q-select>

        </div>
       
        <div class="section-title">Donor Contact Info</div>

        <q-input v-model="form.email" outlined label="Email address" class="q-mb-md" />
        <q-input v-model="form.name" outlined label="Name of donor" class="q-mb-md" />
        <q-input v-model="form.contact" outlined label="Contact number" />
      </div>

      <!-- RIGHT SIDE ini !!!-->
      <div class="donation-summary">
        <div class="donation-summary-logo">
          <img src="~assets/image1.png" alt="BiToHelp" />
        </div>
        <div class="summary-card">
          <h3>Donation Summary</h3>

          <div class="summary-row">
            <span>Charity Name</span>
            <span>{{ form.cause || 'Not selected' }}</span>
          </div>

          <div class="summary-row">
            <span>Recipient Address</span>
            <span class="text-caption">{{ form.recipientAddress || 'Not entered' }}</span>
          </div>

          <div class="summary-row">
            <span>Coin</span>
            <span>{{ form.coin || 'BCH' }}</span>
          </div>

          <div class="summary-row">
            <span>Amount</span>
            <span>{{ form.amount || 0 }} {{ form.coin || 'BCH' }}</span>
          </div>

          <div class="summary-row" v-if="form.contract">
            <span>Contract</span>
            <span>{{ form.contract }}</span>
          </div>

          <div class="summary-row" v-if="!form.contract">
            <span>Interval</span>
            <span>{{ form.interval || 'Not selected' }}</span>
          </div>

          <div class="summary-row" v-if="form.contract">
            <span>Network Fee</span>
            <span>
              {{ form.coin === 'Paytaca Wallet (BCH)' ? '0.0001 BCH' : 'Varies by network' }}
            </span>
          </div>

          <div class="summary-divider"></div>

          <q-btn
            class="continue-btn"
            label="Send Donation"
            unelevated
            @click="handleDonation"
            :loading="processing"
            to="/donor"
            :disable="(!isTestMode && !isConnected) || !form.cause || !form.recipientAddress || !form.amount"
          />

          <p class="terms">
            By selecting continue you agree to our
            <span>terms and conditions</span>
          </p>

        </div>

      </div>

      <div class="donation-footer">
      <div class="footer-brand">
        <img src="~assets/image1.png" alt="BiToHelp" />
        <div class="footer-brand-text">BiToHelp</div>
      </div>
      <div class="footer-col">
        <div class="footer-title">About Us</div>
        <div>Donate crypto</div>
        <div>Explore causes</div>
      </div>
      <div class="footer-col">
        <div class="footer-title">For donors</div>
        <div>Donate crypto</div>
        <div>Explore causes</div>
      </div>
      <div class="footer-col">
        <div class="footer-title">For nonprofits</div>
        <div>Getting started</div>
      </div>
      <div class="footer-col">
        <div class="footer-title">Resources</div>
        <div>Blog</div>
        <div>Help Center</div>
        <div>Terms of use</div>
        <div>Privacy notice</div>
        <div>Copyright © 2026, All rights reserved.</div>
      </div>
      </div>
    </div>


  </q-page>
</template>

<script setup>
import { ref, watch, onMounted } from 'vue'
import { useBCHContract } from '../composables/useBCHContract'
import { useDonationStore } from '../stores/donation-store'
import { useQuasar } from 'quasar'
import { useRouter } from 'vue-router'
import { api } from 'boot/axios'

const $q = useQuasar()
const router = useRouter()
const donationStore = useDonationStore()


const nonprofits = ref([])
const nonprofitOptions = ref([])
const loadingNonprofits = ref(false)


const fetchNonprofits = async () => {
  loadingNonprofits.value = true
  try {
    const response = await api.get('nonprofits/verified/')
    nonprofits.value = response.data.map(np => ({
      id: np.id,
      label: np.name,
      value: np.name,
      address: np.bch_address,
      description: np.description,
      category: np.category,
      verified: np.verified
    }))
    nonprofitOptions.value = nonprofits.value
    console.log('Loaded nonprofits from API:', nonprofits.value.length)
  } catch (error) {
    console.error('Failed to load nonprofits:', error)
    $q.notify({
      type: 'negative',
      message: 'Failed to load nonprofit organizations',
      caption: 'Please refresh the page to try again'
    })

    nonprofits.value = []
    nonprofitOptions.value = []
  } finally {
    loadingNonprofits.value = false
  }
}


onMounted(() => {
  fetchNonprofits()
})

const contractOptions = ref([
  { label: '10 mins', value: '10 mins' },
  { label: '3 Months', value: '12 Weeks' },
  { label: '1 Year', value: '12 Months' }
])

const intervalOptions = ref([
  { label: '5 mins', value: '10 mins' },
  { label: '1 Month', value: '4 Weeks' },
  { label: '6 Months', value: '24 Weeks' },
  { label: '1 Year', value: '12 Months' },
  { label: '2 Year', value: '24 Months' }
])

const cryptoOptions = ref([
  'Paytaca Wallet (BCH)',
  'Ethereum (ETH)',
  'MetaMask (ETH)',
  'Bitcoin (BTC)',
  'Polygon (MATIC)',
  'Binance Smart Chain (BNB)',
  'Solana (SOL)',
  'Tether (USDT)',
  'Cardano (ADA)',
  'USD Coin (USDC)'
])

const form = ref({
  cause: null,
  nonprofitId: null,
  recipientAddress: '',
  coin: 'Paytaca Wallet (BCH)',
  amount: null,
  message: '',
  contract: null,
  interval: null,
  email: '',
  name: '',
  contact: ''
})

const {
  isConnected,
  isTestMode,
  sendDonation
} = useBCHContract()

const processing = ref(false)
const txResult = ref(null)


watch(() => form.value.cause, (newCause) => {
  if (newCause) {
    const selectedNonprofit = nonprofits.value.find(np => np.value === newCause)
    if (selectedNonprofit) {
      form.value.recipientAddress = selectedNonprofit.address
      form.value.nonprofitId = selectedNonprofit.id
    }
  } else {
    form.value.recipientAddress = ''
    form.value.nonprofitId = null
  }
})


watch(() => form.value.contract, (newContract) => {
  if (!newContract) {
    form.value.interval = null
  }
})

const handleDonation = async () => {
  if (!isTestMode.value && !isConnected.value) {
    $q.notify({
      type: 'warning',
      message: 'Please connect your wallet first',
      caption: 'Click the wallet button in the header'
    })
    return
  }

  if (!form.value.cause) {
    $q.notify({
      type: 'warning',
      message: 'Please select a non-profit or cause'
    })
    return
  }

  if (!form.value.recipientAddress) {
    $q.notify({
      type: 'warning',
      message: 'Please enter recipient address'
    })
    return
  }

  if (!form.value.amount || form.value.amount <= 0) {
    $q.notify({
      type: 'warning',
      message: 'Please enter a valid amount'
    })
    return
  }

  processing.value = true
  
  try {
    const donationData = {
      recipient: form.value.recipientAddress,
      amount: form.value.amount,
      message: form.value.message,
      cause: form.value.cause,
      coin: form.value.coin,
      contract: form.value.contract,
      interval: form.value.interval,
      donorName: form.value.name,
      donorEmail: form.value.email,
      donorContact: form.value.contact,
      nonprofitId: form.value.nonprofitId
    }

    const result = await sendDonation(donationData)
    txResult.value = result

    await donationStore.addDonation({
      ...donationData,
      txid: result.txid,
      explorerUrl: result.explorerUrl,
      timestamp: new Date().toISOString()
    })

    
    try {
      const response = await api.post('donations/', {
        txid: result.txid,
        recipient: form.value.recipientAddress,
        amount: form.value.amount,
        coin: form.value.coin,
        cause: form.value.cause,
        message: form.value.message,
        donor_name: form.value.name,
        donor_email: form.value.email,
        donor_contact: form.value.contact,
        explorer_url: result.explorerUrl,
        nonprofit: form.value.nonprofitId,
        contract: form.value.contract,
        interval: form.value.interval
      })
      console.log('Donation saved to database successfully:', response.data)
      console.log('Donation ID:', response.data.id)
      console.log('Charity can now see this donation in Dashboard')
    } catch (dbError) {
      console.error('Failed to save donation to database:', dbError)
      console.error('Error details:', dbError.response?.data)
      $q.notify({
        type: 'warning',
        message: 'Donation sent but not recorded',
        caption: 'Transaction completed but database save failed',
        position: 'top'
      })
    }

    $q.notify({
      type: 'positive',
      message: 'Donation sent successfully!',
      caption: `Transaction ID: ${result.txid}`,
      timeout: 5000,
      actions: [
        {
          label: 'View on Explorer',
          color: 'white',
          handler: () => {
            window.open(result.explorerUrl, '_blank')
          }
        }
      ]
    })

    console.log('Donation completed:', {
      cause: form.value.cause,
      amount: form.value.amount,
      txid: result.txid
    })

    setTimeout(() => {
      router.push('/continue')
    }, 2000)

  } catch (error) {
    console.error('Donation error:', error)
    $q.notify({
      type: 'negative',
      message: 'Failed to send donation',
      caption: error.message
    })
  } finally {
    processing.value = false
  }
}
</script>

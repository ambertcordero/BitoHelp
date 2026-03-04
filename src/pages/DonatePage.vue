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
          outlined 
          label="Choose non-profit or a cause" 
          class="q-mb-md"
        />
        <q-input 
          v-model="form.recipientAddress" 
          outlined 
          label="Recipient BCH Address" 
          hint="Enter the nonprofit's Bitcoin Cash address"
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

          <div class="summary-divider"></div>

          <q-btn
            class="continue-btn"
            label="Send Donation"
            unelevated
            @click="handleDonation"
            :loading="processing"
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
import { ref } from 'vue'
import { useBCHContract } from '../composables/useBCHContract'
import { useDonationStore } from '../stores/donation-store'
import { useQuasar } from 'quasar'
import { useRouter } from 'vue-router'

const $q = useQuasar()
const router = useRouter()
const donationStore = useDonationStore()

const nonprofitOptions = ref([
  'Typhoon Relief Fund',
  'Educational Fund',
  'Medical Fund',
  'Health Fund'
])

const cryptoOptions = ref([
  'Bitcoin Cash (BCH)',
  'Bitcoin (BTC)',
  'Ethereum (ETH)',
  'Tether (USDT)',
  'BNB',
  'USD Coin (USDC)'
])

const form = ref({
  cause: null,
  recipientAddress: '',
  coin: 'Bitcoin Cash (BCH)',
  amount: null,
  message: '',
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


const handleDonation = async () => {
  console.log(' handleDonation called')
  console.log('Test Mode:', isTestMode.value)
  console.log('Connected:', isConnected.value)
  console.log('Form data:', form.value)
  
  
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
    console.log('🔹 Starting donation process...')
    const donationData = {
      recipient: form.value.recipientAddress,
      amount: form.value.amount,
      message: form.value.message,
      cause: form.value.cause,
      coin: form.value.coin,
      donorName: form.value.name,
      donorEmail: form.value.email,
      donorContact: form.value.contact
    }

    console.log(' Sending donation with data:', donationData)
    const result = await sendDonation(donationData)
    console.log(' sendDonation result:', result)
    txResult.value = result

    // Save donation to store (Django API)
    await donationStore.addDonation({
      ...donationData,
      txid: result.txid,
      explorerUrl: result.explorerUrl,
      timestamp: new Date().toISOString()
    })

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

 
    console.log(' Donation completed:', {
      cause: form.value.cause,
      amount: form.value.amount,
      coin: form.value.coin,
      donor: form.value.name,
      txid: result.txid
    })

   
    console.log(' Redirecting to /continue in 2 seconds...')
    setTimeout(() => {
      console.log(' Executing router.push(/continue)')
      router.push('/continue')
        .then(() => console.log(' Navigation successful'))
        .catch(err => console.error(' Navigation failed:', err))
    }, 2000)

  } catch (error) {
    console.error(' Donation error:', error)
    console.error('Error details:', error.message, error.stack)
    $q.notify({
      type: 'negative',
      message: 'Failed to send donation',
      caption: error.message
    })
  } finally {
    console.log(' Setting processing to false')
    processing.value = false
  }
}
</script>

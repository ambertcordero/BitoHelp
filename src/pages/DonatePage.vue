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
import { ref, watch } from 'vue'
import { useBCHContract } from '../composables/useBCHContract'
import { useDonationStore } from '../stores/donation-store'
import { useQuasar } from 'quasar'
import { useRouter } from 'vue-router'

const $q = useQuasar()
const router = useRouter()
const donationStore = useDonationStore()

const nonprofits = ref([
  {
    label: 'Typhoon Relief Fund',
    value: 'Typhoon Relief Fund',
    address: 'bitcoincash:qp3wjpa3tjlj042z2wv7hahsldgwhwy0rq9sywjpyy'
  },
  {
    label: 'Educational Fund',
    value: 'Educational Fund',
    address: 'bitcoincash:qr4aadjrpu73d2wxwkxkcrt6gqxgu6a7usxfm96fst'
  },
  {
    label: 'Medical Fund',
    value: 'Medical Fund',
    address: 'bitcoincash:qpwngrc5j8d7vvz0a0mn0z5yak4axf8mvqnkzgd4n8'
  },
  {
    label: 'Health Fund',
    value: 'Health Fund',
    address: 'bitcoincash:qzj5zu6fgg8v2we82gh76xnrk9njcregluzgaztm45'
  }
])

const nonprofitOptions = ref(nonprofits.value)

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

// Watch for nonprofit selection and auto-fill address
watch(() => form.value.cause, (newCause) => {
  if (newCause) {
    const selectedNonprofit = nonprofits.value.find(np => np.value === newCause)
    if (selectedNonprofit) {
      form.value.recipientAddress = selectedNonprofit.address
    }
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
      donorName: form.value.name,
      donorEmail: form.value.email,
      donorContact: form.value.contact
    }

    const result = await sendDonation(donationData)
    txResult.value = result

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

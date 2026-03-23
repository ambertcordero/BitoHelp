<template>
  <q-page class="donation-page">
    <div class="donation-wrapper">
      <section class="donation-hero">
        <div class="donation-hero-copy">
          <h1>Where your crypto creates a better tomorrow.</h1>
          <p class="subtitle">
            By donating crypto, you unlock smarter, more efficient giving.<br />
            Support thousands of verified nonprofits through blockchain-powered donations.
          </p>
        </div>
        <div class="donation-hero-logo">
          <img src="~assets/BitoHelp.png" alt="BiToHelp" />
        </div>
      </section>

      <section class="donation-main">
        <div class="donation-form-panel">
          <q-select
            v-model="form.cause"
            :options="causeOptions"
            outlined
            emit-value
            map-options
            label="Choose a non-profit or a cause"
            class="donation-select q-mb-md"
          />

          <q-select
            v-model="form.organization"
            :options="organizationOptions"
            :disable="!form.cause"
            outlined
            emit-value
            map-options
            dropdown-icon=""
            label="Organization"
            class="donation-select organization-select q-mb-md"
          >
            <template #option="scope">
              <q-item v-bind="scope.itemProps">
                <q-item-section avatar>
                  <img :src="scope.opt.icon" :alt="scope.opt.label" class="org-option-icon" />
                </q-item-section>
                <q-item-section>
                  <q-item-label>{{ scope.opt.label }}</q-item-label>
                </q-item-section>
              </q-item>
            </template>

            <template #selected-item="scope">
              <span>{{ scope.opt.label }}</span>
            </template>

            <template #append>
              <img
                v-if="selectedOrganizationIcon"
                :src="selectedOrganizationIcon"
                :alt="selectedOrganizationName"
                class="org-append-icon"
              />
            </template>
          </q-select>

          <div class="floating-field" :class="{ 'is-filled': form.recipientAddress }">
            <input v-model.trim="form.recipientAddress" type="text" placeholder=" " />
            <label>Recipient's Address</label>
          </div>

          <div class="mini-grid q-mt-md">
            <div class="floating-field mini-field" :class="{ 'is-filled': form.deposit !== '' }">
              <input
                :value="form.deposit"
                type="text"
                inputmode="decimal"
                placeholder=" "
                @input="onDecimalInput('deposit', $event)"
              />
              <label>Deposit (total)</label>
              <span class="php-conversion">{{ depositPhp }}</span>
            </div>

            <div class="floating-field mini-field" :class="{ 'is-filled': form.withdrawal !== '' }">
              <input
                :value="form.withdrawal"
                type="text"
                inputmode="decimal"
                placeholder=" "
                @input="onDecimalInput('withdrawal', $event)"
              />
              <label>Withdrawal (per cycle)</label>
              <span class="php-conversion">{{ withdrawalPhp }}</span>
            </div>
          </div>

          <q-select
            v-model="form.interval"
            :options="intervalOptions"
            outlined
            emit-value
            map-options
            label="Interval"
            class="donation-select q-mt-md"
          />

          <q-select
            v-model="form.coin"
            :options="coinOptions"
            outlined
            emit-value
            map-options
            label="Coin"
            class="donation-select q-mt-md"
          />

          <div class="donor-title">DONOR CONTACT INFO</div>

          <div class="floating-field" :class="{ 'is-filled': form.name }">
            <input v-model.trim="form.name" type="text" placeholder=" " />
            <label>Donor's Name</label>
          </div>

          <div class="contact-grid q-mt-md">
            <div class="floating-field" :class="{ 'is-filled': form.email }">
              <input v-model.trim="form.email" type="email" placeholder=" " />
              <label>Email Address</label>
            </div>

            <div class="floating-field" :class="{ 'is-filled': form.contact }">
              <input v-model.trim="form.contact" type="text" placeholder=" " />
              <label>Contact Number</label>
            </div>
          </div>

          <div class="floating-field textarea-field q-mt-md" :class="{ 'is-filled': form.message }">
            <textarea v-model.trim="form.message" rows="6" placeholder=" "></textarea>
            <label>Message</label>
          </div>
        </div>

        <!-- RIGHT SIDE — keep existing summary -->
        <div class="donation-summary">
          <div class="donation-summary-logo">
            <img src="~assets/image1.png" alt="BiToHelp" />
          </div>
          <div class="summary-card">
            <h3>Donation Summary</h3>

            <div class="summary-row">
              <span>Charity Name</span>
              <span>{{ selectedOrganizationName || 'Not selected' }}</span>
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
              <span>Deposit</span>
              <span>{{ form.deposit || 0 }} {{ form.coin || 'BCH' }}</span>
            </div>

            <div class="summary-row">
              <span>Withdrawal</span>
              <span>{{ form.withdrawal || 0 }} {{ form.coin || 'BCH' }}</span>
            </div>

            <div class="summary-row">
              <span>Interval</span>
              <span>{{ summaryInterval }}</span>
            </div>

            <div class="summary-divider"></div>

            <q-btn
              class="continue-btn"
              label="Send Donation"
              unelevated
              @click="handleDonation"
              :loading="processing"
              :disable="!isConnected || !form.cause || !form.organization || !form.recipientAddress || !form.deposit"
            />

            <p class="terms">
              By selecting continue you agree to our
              <span>terms and conditions</span>
            </p>
          </div>
        </div>
      </section>
    </div>
  </q-page>
</template>

<script setup>
import { ref, computed, watch, onMounted, onUnmounted } from 'vue'
import { useDonationStore } from '../stores/donation-store'
import { useQuasar } from 'quasar'
import { useRouter } from 'vue-router'
import { api } from 'boot/axios'

import caraIcon from '../charity/Cara.ico'
import caritasManilaIcon from '../charity/Caritas Manila.ico'
import childHopePhIcon from '../charity/ChildHope PH.ico'
import gawadKalingaIcon from '../charity/Gawad Kalinga.ico'
import greenEarthIcon from '../charity/Green Earth.ico'
import haribonFoundationIcon from '../charity/Haribon Foundation.ico'
import saveTheChildrenIcon from '../charity/Save The Children.ico'
import worldVisionIcon from '../charity/World Vision.ico'

const $q = useQuasar()
const router = useRouter()
const donationStore = useDonationStore()

// --- Static options ---
const causeOptions = [
  { label: 'Animals', value: 'Animals' },
  { label: 'Children & Youth', value: 'Children & Youth' },
  { label: 'Poverty Alleviation', value: 'Poverty Alleviation' },
  { label: 'Housing & Community Humanitarian Aid', value: 'Housing & Community Humanitarian Aid' },
  { label: 'Environment & Conservation', value: 'Environment & Conservation' },
]

const organizationCatalog = [
  { label: 'CARA', value: 'CARA', icon: caraIcon, causes: ['Animals'] },
  { label: 'Caritas Manila', value: 'Caritas Manila', icon: caritasManilaIcon, causes: ['Poverty Alleviation'] },
  { label: 'ChildHope PH', value: 'ChildHope PH', icon: childHopePhIcon, causes: ['Children & Youth'] },
  { label: 'Gawad Kalinga', value: 'Gawad Kalinga', icon: gawadKalingaIcon, causes: ['Housing & Community Humanitarian Aid'] },
  { label: 'Green Earth', value: 'Green Earth', icon: greenEarthIcon, causes: ['Environment & Conservation'] },
  { label: 'Haribon Foundation', value: 'Haribon Foundation', icon: haribonFoundationIcon, causes: ['Environment & Conservation'] },
  { label: 'Save the Children', value: 'Save the Children', icon: saveTheChildrenIcon, causes: ['Children & Youth'] },
  { label: 'World Vision', value: 'World Vision', icon: worldVisionIcon, causes: ['Children & Youth', 'Housing & Community Humanitarian Aid'] },
]

const coinOptions = [
  { label: 'BCH', value: 'BCH' },
  { label: 'ETH', value: 'ETH' },
]

const intervalOptions = [
  { label: '10 mins', value: '10min' },
  { label: 'Weekly (coming soon)', value: 'weekly', disable: true },
  { label: 'Monthly (coming soon)', value: 'monthly', disable: true },
  { label: 'Quarterly (coming soon)', value: 'quarterly', disable: true },
  { label: 'Yearly (coming soon)', value: 'yearly', disable: true },
]

// --- API nonprofits (for address lookup) ---
const nonprofits = ref([])

const fetchNonprofits = async () => {
  try {
    const response = await api.get('nonprofits/verified/')
    nonprofits.value = response.data.map(np => ({
      id: np.id,
      name: np.name,
      address: np.bch_address,
      category: np.category,
    }))
    console.log('Loaded nonprofits from API:', nonprofits.value.length)
  } catch (error) {
    console.error('Failed to load nonprofits:', error)
  }
}

onMounted(() => {
  fetchNonprofits()
  fetchCryptoToPhpRates()
})

// --- Form ---
const form = ref({
  cause: null,
  organization: null,
  coin: 'BCH',
  recipientAddress: '',
  deposit: '',
  withdrawal: '',
  interval: '10min',
  name: '',
  email: '',
  contact: '',
  message: '',
})

// --- Computed ---
const organizationOptions = computed(() => {
  if (!form.value.cause) return []
  return organizationCatalog.filter(org => org.causes.includes(form.value.cause))
})

const selectedOrganizationName = computed(() => {
  const selected = organizationCatalog.find(o => o.value === form.value.organization)
  return selected?.label || ''
})

const selectedOrganizationIcon = computed(() => {
  const selected = organizationCatalog.find(o => o.value === form.value.organization)
  return selected?.icon || ''
})

const summaryInterval = computed(() => {
  const opt = intervalOptions.find(o => o.value === form.value.interval)
  return opt?.label || '—'
})

// --- PHP conversion ---
const conversionRates = ref({ BCH: 0, ETH: 0 })

const fetchCryptoToPhpRates = async () => {
  try {
    const response = await fetch(
      'https://api.coingecko.com/api/v3/simple/price?ids=bitcoin-cash,ethereum&vs_currencies=php'
    )
    if (!response.ok) return
    const data = await response.json()
    conversionRates.value = {
      BCH: Number(data?.['bitcoin-cash']?.php) || 0,
      ETH: Number(data?.ethereum?.php) || 0,
    }
  } catch {
    conversionRates.value = { BCH: 0, ETH: 0 }
  }
}

const formatPhp = (amount) =>
  Number(amount).toLocaleString('en-PH', {
    style: 'currency',
    currency: 'PHP',
    minimumFractionDigits: 2,
    maximumFractionDigits: 2,
  })

const depositPhp = computed(() => {
  const amount = Number(form.value.deposit)
  const rate = conversionRates.value[form.value.coin] || 0
  if (!amount || !rate) return 'PHP —'
  return formatPhp(amount * rate)
})

const withdrawalPhp = computed(() => {
  const amount = Number(form.value.withdrawal)
  const rate = conversionRates.value[form.value.coin] || 0
  if (!amount || !rate) return 'PHP —'
  return formatPhp(amount * rate)
})

const onDecimalInput = (field, event) => {
  const raw = String(event?.target?.value ?? '').replace(/[^\d.]/g, '')
  const [integerPart, ...fractionParts] = raw.split('.')
  const sanitized = fractionParts.length ? `${integerPart}.${fractionParts.join('')}` : integerPart
  form.value[field] = sanitized
  if (event?.target) event.target.value = sanitized
}

// --- Watchers ---
watch(() => form.value.cause, () => {
  form.value.organization = null
  form.value.recipientAddress = ''
})

watch(() => form.value.organization, (orgName) => {
  if (!orgName) {
    form.value.recipientAddress = ''
    return
  }
  const match = nonprofits.value.find(np => np.name === orgName)
  if (match) {
    form.value.recipientAddress = match.address
  }
})

// --- Wallet connection ---
const isConnected = ref(localStorage.getItem('bitohelp.wallet.connected') === '1')
function onWalletChange () {
  isConnected.value = localStorage.getItem('bitohelp.wallet.connected') === '1'
}
onMounted(() => window.addEventListener('bitohelp:wallet-connection-changed', onWalletChange))
onUnmounted(() => window.removeEventListener('bitohelp:wallet-connection-changed', onWalletChange))

const processing = ref(false)

// --- Donation handler ---
const handleDonation = async () => {
  if (!isConnected.value) {
    $q.notify({ type: 'warning', message: 'Please connect your wallet first', caption: 'Click the wallet button in the header' })
    return
  }
  if (!form.value.cause || !form.value.organization) {
    $q.notify({ type: 'warning', message: 'Please select a cause and organization' })
    return
  }
  if (!form.value.recipientAddress) {
    $q.notify({ type: 'warning', message: 'Please enter recipient address' })
    return
  }
  const depositAmount = Number(form.value.deposit)
  if (!depositAmount || depositAmount <= 0) {
    $q.notify({ type: 'warning', message: 'Please enter a valid deposit amount' })
    return
  }

  processing.value = true

  try {
    const donationData = {
      recipient: form.value.recipientAddress,
      amount: depositAmount,
      message: form.value.message,
      cause: form.value.cause,
      organization: form.value.organization,
      coin: form.value.coin,
      interval: form.value.interval,
      deposit: form.value.deposit,
      withdrawal: form.value.withdrawal,
      donorName: form.value.name,
      donorEmail: form.value.email,
      donorContact: form.value.contact,
    }

    // Find nonprofit ID from API data
    const matchedNp = nonprofits.value.find(np => np.name === form.value.organization)
    if (matchedNp) donationData.nonprofitId = matchedNp.id

    // Use WalletConnect global bridge to send the donation
    const walletClient = window.__bitohelpWalletClient__
    if (!walletClient) {
      throw new Error('Wallet session not available. Please reconnect your wallet.')
    }

    let result
    if (walletClient.namespace === 'bch') {
      const { selectInputsAndBuildPlan, buildWalletConnectBchSignPayload, extractWalletSignedTransaction, broadcastRawTransaction } = await import('../services/bchChipnet')
      const plan = await selectInputsAndBuildPlan({ address: walletClient.address, amountBch: depositAmount, recipientAddress: donationData.recipient })
      const signPayload = buildWalletConnectBchSignPayload(plan)
      const signResult = await walletClient.request({ chainId: walletClient.chain, request: { method: 'bch_signTransaction', params: signPayload } })
      const rawTx = extractWalletSignedTransaction(signResult)
      const txid = await broadcastRawTransaction(rawTx)
      result = { txid, explorerUrl: `https://chipnet.chaingraph.cash/tx/${txid}` }
      window.dispatchEvent(new CustomEvent('bitohelp:wallet-balance-adjust', { detail: { delta: -depositAmount, chain: walletClient.chain, address: walletClient.address } }))
    } else {
      const txHash = await walletClient.request({ chainId: walletClient.chain, request: { method: 'eth_sendTransaction', params: [{ from: walletClient.address, to: donationData.recipient, value: '0x' + Math.round(depositAmount * 1e18).toString(16) }] } })
      result = { txid: txHash, explorerUrl: `https://sepolia.etherscan.io/tx/${txHash}` }
    }

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
        amount: depositAmount,
        coin: form.value.coin,
        cause: form.value.cause,
        message: form.value.message,
        donor_name: form.value.name,
        donor_email: form.value.email,
        donor_contact: form.value.contact,
        explorer_url: result.explorerUrl,
        nonprofit: donationData.nonprofitId,
        interval: form.value.interval
      })
      console.log('Donation saved to database successfully:', response.data)
    } catch (dbError) {
      console.error('Failed to save donation to database:', dbError)
      $q.notify({ type: 'warning', message: 'Donation sent but not recorded', caption: 'Transaction completed but database save failed', position: 'top' })
    }

    $q.notify({
      type: 'positive',
      message: 'Donation sent successfully!',
      caption: `Transaction ID: ${result.txid}`,
      timeout: 5000,
      actions: [{ label: 'View on Explorer', color: 'white', handler: () => { window.open(result.explorerUrl, '_blank') } }]
    })

    setTimeout(() => { router.push('/continue') }, 2000)

  } catch (error) {
    console.error('Donation error:', error)
    $q.notify({ type: 'negative', message: 'Failed to send donation', caption: error.message })
  } finally {
    processing.value = false
  }
}
</script>

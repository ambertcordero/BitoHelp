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
            <label>Recipient’s Address</label>
          </div>

          <div class="mini-grid q-mt-md">
            <div class="floating-field mini-field" :class="{ 'is-filled': form.amount !== '' }">
              <input
                :value="form.amount"
                type="text"
                inputmode="decimal"
                placeholder=" "
                @input="onDecimalInput('amount', $event)"
              />
              <label>Amount to Donate</label>
              <span class="php-conversion">{{ amountPhp }}</span>
            </div>
          </div>

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

          <div class="floating-field" :class="{ 'is-filled': form.donorName }">
            <input v-model.trim="form.donorName" type="text" placeholder=" " />
            <label>Donor’s Name</label>
          </div>

          <div class="contact-grid q-mt-md">
            <div class="floating-field" :class="{ 'is-filled': form.email }">
              <input v-model.trim="form.email" type="email" placeholder=" " />
              <label>Email Address</label>
            </div>

            <div class="floating-field" :class="{ 'is-filled': form.contactNumber }">
              <input v-model.trim="form.contactNumber" type="text" placeholder=" " />
              <label>Contact Number</label>
            </div>
          </div>

          <div class="floating-field textarea-field q-mt-md" :class="{ 'is-filled': form.message }">
            <textarea v-model.trim="form.message" rows="6" placeholder=" "></textarea>
            <label>Message</label>
          </div>
        </div>

        <aside class="donation-summary-panel">
          <h3>DONATION SUMMARY</h3>

          <div class="summary-row">
            <span>Donor</span>
            <span>{{ form.donorName || '—' }}</span>
          </div>

          <div class="summary-row">
            <span>Recipient</span>
            <span>{{ selectedOrganizationName || '—' }}</span>
          </div>

          <div class="summary-row">
            <span>Contract</span>
            <span>{{ summaryContract }}</span>
          </div>

          <div class="summary-row">
            <span>Coin</span>
            <span>{{ form.coin || '—' }}</span>
          </div>

          <div class="summary-row">
            <span>Amount</span>
            <span>{{ summaryAmount }}</span>
          </div>

          <div class="summary-divider"></div>

          <q-btn
            class="donate-now-btn"
            label="DONATE NOW"
            unelevated
            :loading="isSubmittingDonation"
            :disable="isSubmittingDonation"
            @click="submitDonation"
          />
          <p v-if="submissionStatus.message" :class="submissionStatusClass" class="q-mt-sm">
            {{ submissionStatus.message }}
          </p>
        </aside>
      </section>
    </div>
  </q-page>
</template>

<script setup>
import { computed, onMounted, ref, watch } from 'vue'
import { useRouter } from 'vue-router'
import { Notify, useQuasar } from 'quasar'
import { parseEther, parseUnits } from 'ethers'

import caraIcon from '../../charity/Cara.ico'
import caritasManilaIcon from '../../charity/Caritas Manila.ico'
import childHopePhIcon from '../../charity/ChildHope PH.ico'
import gawadKalingaIcon from '../../charity/Gawad Kalinga.ico'
import greenEarthIcon from '../../charity/Green Earth.ico'
import haribonFoundationIcon from '../../charity/Haribon Foundation.ico'
import saveTheChildrenIcon from '../../charity/Save The Children.ico'
import worldVisionIcon from '../../charity/World Vision.ico'
import { CASHSCRIPT_CONTRACT_PATH } from '../contracts/recurringDonation'

const $q = useQuasar()
const router = useRouter()

const notify = (payload) => {
  if (typeof $q?.notify === 'function') {
    $q.notify(payload)
    return
  }

  if (typeof Notify?.create === 'function') {
    Notify.create(payload)
    return
  }

  if (import.meta.env.DEV) {
    console.warn('[BitoHelp][notify:fallback]', payload)
  }
}

const DONATIONS_STORAGE_KEY = 'bitohelp.donations'
const WALLET_SNAPSHOT_STORAGE_KEY = 'bitohelp.wallet.snapshot'
const WALLET_BALANCE_ADJUST_EVENT = 'bitohelp:wallet-balance-adjust'
const WALLET_BALANCE_REFRESH_EVENT = 'bitohelp:wallet-balance-refresh'
const DONATION_SENT_EVENT = 'bitohelp:donation-sent'
const WALLET_CLIENT_GLOBAL_KEY = '__bitohelpWalletClient__'
const WALLET_REQUEST_TIMEOUT_MS = 90000

const causeOptions = [
  { label: 'Animals', value: 'Animals' },
  { label: 'Children & Youth', value: 'Children & Youth' },
  { label: 'Poverty Alleviation', value: 'Poverty Alleviation' },
  { label: 'Housing & Community Humanitarian Aid', value: 'Housing & Community Humanitarian Aid' },
  { label: 'Environment & Conservation', value: 'Environment & Conservation' },
]

const organizationCatalog = [
  { label: 'CARA', value: 'CARA', icon: caraIcon, causes: ['Animals'] },
  {
    label: 'Caritas Manila',
    value: 'Caritas Manila',
    icon: caritasManilaIcon,
    causes: ['Poverty Alleviation'],
  },
  {
    label: 'ChildHope PH',
    value: 'ChildHope PH',
    icon: childHopePhIcon,
    causes: ['Children & Youth'],
  },
  {
    label: 'Gawad Kalinga',
    value: 'Gawad Kalinga',
    icon: gawadKalingaIcon,
    causes: ['Housing & Community Humanitarian Aid'],
  },
  {
    label: 'Green Earth',
    value: 'Green Earth',
    icon: greenEarthIcon,
    causes: ['Environment & Conservation'],
  },
  {
    label: 'Haribon Foundation',
    value: 'Haribon Foundation',
    icon: haribonFoundationIcon,
    causes: ['Environment & Conservation'],
  },
  {
    label: 'Save the Children',
    value: 'Save the Children',
    icon: saveTheChildrenIcon,
    causes: ['Children & Youth'],
  },
  {
    label: 'World Vision',
    value: 'World Vision',
    icon: worldVisionIcon,
    causes: ['Children & Youth', 'Housing & Community Humanitarian Aid'],
  },
]

const coinOptions = [
  { label: 'BCH', value: 'BCH' },
  { label: 'ETH', value: 'ETH' },
]

const form = ref({
  cause: null,
  organization: null,
  coin: 'BCH',
  recipientAddress: '',
  amount: '',
  donorName: '',
  email: '',
  contactNumber: '',
  message: '',
})

const conversionRates = ref({
  BCH: 0,
  ETH: 0,
})

const isSubmittingDonation = ref(false)
const submissionStatus = ref({ type: '', message: '' })

const submissionStatusClass = computed(() => ({
  'donation-status': true,
  'donation-status--error': submissionStatus.value.type === 'negative',
}))

const organizationOptions = computed(() => {
  if (!form.value.cause) {
    return []
  }

  return organizationCatalog.filter((organization) =>
    organization.causes.includes(form.value.cause),
  )
})

watch(
  () => form.value.cause,
  () => {
    form.value.organization = null
  },
)

const selectedOrganizationName = computed(() => {
  const selected = organizationCatalog.find((option) => option.value === form.value.organization)
  return selected?.label || ''
})

const selectedOrganizationIcon = computed(() => {
  const selected = organizationCatalog.find((option) => option.value === form.value.organization)
  return selected?.icon || ''
})

const summaryContract = computed(() => {
  if (form.value.coin === 'ETH') {
    return 'Direct transfer (ETH)'
  }

  return CASHSCRIPT_CONTRACT_PATH
})

const summaryAmount = computed(() => {
  const amount = Number(form.value.amount)
  if (!amount) {
    return '—'
  }

  return `${amount.toFixed(8)} ${form.value.coin || ''}`
})

const formatPhp = (amount) =>
  Number(amount).toLocaleString('en-PH', {
    style: 'currency',
    currency: 'PHP',
    minimumFractionDigits: 2,
    maximumFractionDigits: 2,
  })

const amountPhp = computed(() => {
  const amount = Number(form.value.amount)
  const rate = conversionRates.value[form.value.coin] || 0
  if (!amount || !rate) {
    return 'PHP —'
  }
  return formatPhp(amount * rate)
})

const fetchCryptoToPhpRates = async () => {
  try {
    const response = await fetch(
      'https://api.coingecko.com/api/v3/simple/price?ids=bitcoin-cash,ethereum&vs_currencies=php',
    )
    if (!response.ok) {
      return
    }
    const data = await response.json()
    conversionRates.value = {
      BCH: Number(data?.['bitcoin-cash']?.php) || 0,
      ETH: Number(data?.ethereum?.php) || 0,
    }
  } catch {
    conversionRates.value = {
      BCH: 0,
      ETH: 0,
    }
  }
}

onMounted(() => {
  fetchCryptoToPhpRates()
})

const sanitizeDecimalValue = (value) => {
  const cleaned = String(value ?? '').replace(/[^\d.]/g, '')
  const [integerPart, ...fractionParts] = cleaned.split('.')
  if (!fractionParts.length) {
    return integerPart
  }
  return `${integerPart}.${fractionParts.join('')}`
}

const onDecimalInput = (field, event) => {
  const sanitized = sanitizeDecimalValue(event?.target?.value)
  form.value[field] = sanitized
  if (event?.target) {
    event.target.value = sanitized
  }
}

const normalizeRecipientAddress = (value) => String(value ?? '').trim()

const isValidEthAddress = (value) => /^0x[0-9a-fA-F]{40}$/.test(normalizeRecipientAddress(value))

const isValidBchAddress = (value) => {
  const normalized = normalizeRecipientAddress(value).toLowerCase()
  return /^(bitcoincash:|bchtest:|bchreg:)?[qpzry9x8gf2tvdw0s3jn54khce6mua7l]{42}$/.test(normalized)
}

const isDecimalString = (value) => /^\d+(\.\d+)?$/.test(String(value ?? '').trim())

const decimalToBaseUnits = (value, decimals) => {
  const normalized = String(value ?? '').trim()
  if (!isDecimalString(normalized)) {
    return null
  }

  try {
    const units = parseUnits(normalized, decimals)
    return units > 0n ? units : null
  } catch {
    return null
  }
}

const parseEthAmountToWei = (value) => {
  const normalized = String(value ?? '').trim()
  if (!isDecimalString(normalized)) {
    return null
  }

  try {
    const wei = parseEther(normalized)
    return wei > 0n ? wei : null
  } catch {
    return null
  }
}

const toHexQuantity = (value) => `0x${value.toString(16)}`

const getWalletClient = () => window?.[WALLET_CLIENT_GLOBAL_KEY] || null

const executeWalletRequest = async (walletClient, chainId, method, candidateParams) => {
  let lastError = null

  for (const params of candidateParams) {
    try {
      if (import.meta.env.DEV) {
        console.info('[BitoHelp][donation-request:start]', { method, chainId, params })
      }

      const requestPromise = walletClient.request({
        chainId,
        request: {
          method,
          params,
        },
      })

      const response = await Promise.race([
        requestPromise,
        new Promise((_, reject) => {
          window.setTimeout(() => {
            reject(new Error('Wallet approval request timed out.'))
          }, WALLET_REQUEST_TIMEOUT_MS)
        }),
      ])

      if (import.meta.env.DEV) {
        console.info('[BitoHelp][donation-request:success]', { method, chainId, response })
      }

      return response
    } catch (error) {
      if (import.meta.env.DEV) {
        console.error('[BitoHelp][donation-request:error]', { method, chainId, error })
      }

      lastError = error

      const message = String(error?.message || '')
      if (/timed out/i.test(message)) {
        break
      }
    }
  }

  throw lastError || new Error(`Wallet rejected ${method} request.`)
}

const getErrorMessage = (error, fallback) => {
  const message =
    error?.message ||
    error?.cause?.message ||
    error?.data?.message ||
    error?.error?.message ||
    fallback

  if (typeof message !== 'string') {
    return fallback
  }

  if (/rejected|denied|cancel/i.test(message)) {
    return 'Transaction was rejected in wallet.'
  }

  return message
}

const extractTxReference = (result) => {
  if (typeof result === 'string') {
    return result
  }

  if (result && typeof result === 'object') {
    return result.txid || result.hash || result.transactionHash || result.result || null
  }

  return null
}

const sendBchDonation = async ({ walletClient, chainId, from, to, satoshis }) => {
  const satoshiNumber = Number(satoshis)
  const satoshiString = satoshis.toString()

  return executeWalletRequest(walletClient, chainId, 'bch_sendTransaction', [
    [{ from, to, value: satoshiNumber }],
    [{ from, to, value: satoshiString }],
    { from, to, value: satoshiString },
    [from, to, satoshiString],
  ])
}

const sendEthDonation = async ({ walletClient, chainId, from, to, wei }) =>
  executeWalletRequest(walletClient, chainId, 'eth_sendTransaction', [
    [
      {
        from,
        to,
        value: toHexQuantity(wei),
      },
    ],
  ])

const isWalletCompatibleWithCoin = (walletSnapshot, coin) => {
  const namespace = walletSnapshot?.namespace || ''
  const chain = walletSnapshot?.chain || ''
  if (coin === 'BCH') {
    return namespace === 'bch' && chain === 'bch:bchtest'
  }
  if (coin === 'ETH') {
    return namespace === 'eip155' && ['eip155:1', 'eip155:5', 'eip155:11155111'].includes(chain)
  }
  return false
}

const getWalletSnapshot = () => {
  try {
    const raw = localStorage.getItem(WALLET_SNAPSHOT_STORAGE_KEY)
    if (!raw) {
      return null
    }
    return JSON.parse(raw)
  } catch {
    return null
  }
}

const getStoredDonations = () => {
  try {
    const raw = localStorage.getItem(DONATIONS_STORAGE_KEY)
    if (!raw) {
      return []
    }
    const parsed = JSON.parse(raw)
    return Array.isArray(parsed) ? parsed : []
  } catch {
    return []
  }
}

const buildDonationId = () =>
  `donation-${Date.now()}-${Math.random().toString(36).slice(2, 8).toUpperCase()}`

const resetForm = () => {
  form.value = {
    cause: null,
    organization: null,
    coin: 'BCH',
    recipientAddress: '',
    amount: '',
    donorName: '',
    email: '',
    contactNumber: '',
    message: '',
  }
}

const submitDonation = async () => {
  if (isSubmittingDonation.value) {
    return
  }

  submissionStatus.value = { type: '', message: '' }

  const selectedCoin = form.value.coin
  const recipientAddress = normalizeRecipientAddress(form.value.recipientAddress)
  const amountUnits =
    selectedCoin === 'ETH'
      ? parseEthAmountToWei(form.value.amount)
      : decimalToBaseUnits(form.value.amount, 8)
  const amountCoin = Number.parseFloat(String(form.value.amount ?? '').trim())
  const walletSnapshot = getWalletSnapshot()
  const walletClient = getWalletClient()
  const activeAccount = walletClient?.address || walletSnapshot?.address || ''
  const activeChain = walletClient?.chain || walletSnapshot?.chain || ''

  if (!form.value.cause || !form.value.organization) {
    submissionStatus.value = {
      type: 'negative',
      message: 'Please select a cause and organization.',
    }
    notify({
      type: 'warning',
      message: 'Please select a cause and organization.',
    })
    return
  }

  if (!form.value.donorName || !form.value.email) {
    submissionStatus.value = {
      type: 'negative',
      message: 'Please provide donor name and email address.',
    }
    notify({
      type: 'warning',
      message: 'Please provide donor name and email address.',
    })
    return
  }

  if (!walletSnapshot?.connected || !activeAccount || !activeChain) {
    submissionStatus.value = {
      type: 'negative',
      message: 'Please connect your wallet before donating.',
    }
    notify({
      type: 'warning',
      message: 'Please connect your wallet before donating.',
    })
    return
  }

  if (!walletClient?.request) {
    submissionStatus.value = {
      type: 'negative',
      message: 'Wallet bridge unavailable. Reconnect wallet and try again.',
    }
    notify({
      type: 'warning',
      message: 'Wallet request bridge is unavailable. Reconnect your wallet and try again.',
    })
    return
  }

  if (!selectedCoin) {
    submissionStatus.value = {
      type: 'negative',
      message: 'Please select a coin for this donation.',
    }
    notify({
      type: 'warning',
      message: 'Please select a coin for this donation.',
    })
    return
  }

  if (
    !isWalletCompatibleWithCoin(
      { namespace: walletClient?.namespace || walletSnapshot?.namespace, chain: activeChain },
      selectedCoin,
    )
  ) {
    submissionStatus.value = {
      type: 'negative',
      message: `Connected wallet is not compatible with ${selectedCoin}.`,
    }
    notify({
      type: 'warning',
      message: `Connected wallet is not compatible with ${selectedCoin}.`,
    })
    return
  }

  if (!Number.isFinite(amountCoin) || amountCoin <= 0 || !amountUnits) {
    submissionStatus.value = { type: 'negative', message: 'Please enter a valid amount to donate.' }
    notify({
      type: 'warning',
      message: 'Please enter a valid amount to donate.',
    })
    return
  }

  if (selectedCoin === 'BCH' && !isValidBchAddress(recipientAddress)) {
    submissionStatus.value = {
      type: 'negative',
      message: 'Please enter a valid BCH recipient address.',
    }
    notify({
      type: 'warning',
      message: 'Please enter a valid BCH recipient address.',
    })
    return
  }

  if (selectedCoin === 'ETH' && !isValidEthAddress(recipientAddress)) {
    submissionStatus.value = {
      type: 'negative',
      message: 'Recipient must be a valid ETH address (0x + 40 hex chars).',
    }
    notify({
      type: 'warning',
      message: 'For ETH, recipient must be a valid address (0x + 40 hex chars).',
    })
    return
  }

  let txResult
  isSubmittingDonation.value = true

  try {
    submissionStatus.value = {
      type: '',
      message: 'Waiting for wallet approval... confirm in your wallet app.',
    }

    if (selectedCoin === 'BCH') {
      txResult = await sendBchDonation({
        walletClient,
        chainId: activeChain,
        from: activeAccount,
        to: recipientAddress,
        satoshis: amountUnits,
      })
    } else {
      txResult = await sendEthDonation({
        walletClient,
        chainId: activeChain,
        from: activeAccount,
        to: recipientAddress,
        wei: amountUnits,
      })
    }

    const txReference = extractTxReference(txResult)

    const donationRecord = {
      id: buildDonationId(),
      createdAt: new Date().toISOString(),
      status: 'sent',
      txReference,
      chain: activeChain,
      donor: {
        name: form.value.donorName,
        email: form.value.email,
        contactNumber: form.value.contactNumber || '',
        message: form.value.message || '',
        walletAddress: activeAccount,
        coin: selectedCoin,
      },
      recipient: {
        cause: form.value.cause,
        organization: form.value.organization,
        address: recipientAddress,
        addressType: selectedCoin === 'BCH' ? 'bch-address' : 'eth',
      },
      values: {
        coin: selectedCoin,
        amount: amountUnits.toString(),
        amountCoin,
      },
      contract: {
        version: '0.12.0',
        ...(selectedCoin === 'BCH'
          ? { type: 'recurring-donation', contractPath: CASHSCRIPT_CONTRACT_PATH }
          : { type: 'direct-eth-transfer' }),
      },
    }

    const existing = getStoredDonations()
    const nextDonations = [donationRecord, ...existing]
    localStorage.setItem(DONATIONS_STORAGE_KEY, JSON.stringify(nextDonations))

    window.dispatchEvent(
      new CustomEvent(WALLET_BALANCE_ADJUST_EVENT, {
        detail: {
          delta: -amountCoin,
          chain: activeChain,
          address: activeAccount,
        },
      }),
    )

    window.dispatchEvent(
      new CustomEvent(WALLET_BALANCE_REFRESH_EVENT, {
        detail: {
          chain: activeChain,
          address: activeAccount,
        },
      }),
    )

    window.dispatchEvent(
      new CustomEvent(DONATION_SENT_EVENT, {
        detail: {
          txHash: txReference,
          coin: selectedCoin,
          chain: activeChain,
          recipientAddress,
          amount: amountCoin,
        },
      }),
    )

    notify({
      type: 'positive',
      message: txReference
        ? `Donation sent successfully. Tx: ${txReference}`
        : 'Donation sent successfully.',
    })

    submissionStatus.value = {
      type: 'positive',
      message: txReference
        ? `Donation sent. Transaction hash: ${txReference}`
        : 'Donation sent successfully.',
    }

    resetForm()
    router.push('/continue')
  } catch (error) {
    const failureMessage = getErrorMessage(
      error,
      'Donation transaction failed or was rejected by wallet.',
    )
    submissionStatus.value = {
      type: 'negative',
      message: failureMessage,
    }
    notify({
      type: 'negative',
      message: failureMessage,
    })
  } finally {
    isSubmittingDonation.value = false
  }
}
</script>

<style scoped>
.donation-status {
  font-size: 0.86rem;
  color: #1f7a1f;
}

.donation-status--error {
  color: #b00020;
}
</style>

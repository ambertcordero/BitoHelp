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

          <!-- Row 1: Recipient Address | Coin -->
          <div class="compact-row q-mt-md">
            <div
              class="floating-field compact-field"
              :class="{ 'is-filled': form.recipientAddress }"
            >
              <input
                :value="truncatedRecipientAddress"
                type="text"
                placeholder=" "
                readonly
                :title="form.recipientAddress"
              />
              <label>Recipient's Address</label>
            </div>

            <q-select
              v-model="form.coin"
              :options="coinOptions"
              outlined
              emit-value
              map-options
              label="Coin"
              class="donation-select compact-select"
              dense
            />
          </div>

          <!-- Row 2: Deposit | Interval | Withdrawal -->
          <div class="compact-row-3 q-mt-md">
            <div
              class="floating-field compact-field mini-field"
              :class="{ 'is-filled': form.deposit !== '' }"
            >
              <input
                :value="form.deposit"
                type="text"
                inputmode="decimal"
                placeholder=" "
                @input="onDecimalInput('deposit', $event)"
              />
              <label>Deposit</label>
              <span class="php-conversion">{{ depositPhp }}</span>
            </div>

            <q-select
              v-model="form.interval"
              :options="intervalOptions"
              outlined
              emit-value
              map-options
              label="Interval"
              class="donation-select compact-select"
              dense
            />

            <div
              class="floating-field compact-field mini-field"
              :class="{ 'is-filled': form.withdrawal !== '' }"
            >
              <input
                :value="form.withdrawal"
                type="text"
                inputmode="decimal"
                placeholder=" "
                @input="onDecimalInput('withdrawal', $event)"
              />
              <label>Withdrawal</label>
              <span class="php-conversion">{{ withdrawalPhp }}</span>
            </div>
          </div>
          <p v-if="intervalWarning" class="interval-warning q-mt-xs q-mb-none">
            {{ intervalWarning }}
          </p>

          <!-- Payout Options -->
          <div class="payout-options q-mt-md">
            <label class="payout-checkbox">
              <input
                type="checkbox"
                :checked="form.smartPayout"
                @change="selectPayoutMode('smart')"
              />
              <span class="payout-checkbox__label">Smart Payout</span>
              <q-icon name="info" class="payout-info-icon" size="14px">
                <q-tooltip
                  anchor="top middle"
                  self="bottom middle"
                  :offset="[0, 6]"
                  max-width="260px"
                >
                  Automatically executes scheduled withdrawals once the interval is reached and
                  instantly notifies the donor via email with transaction details.
                </q-tooltip>
              </q-icon>
            </label>

            <label class="payout-checkbox">
              <input
                type="checkbox"
                :checked="form.payoutApproval"
                @change="selectPayoutMode('inbox_approval')"
              />
              <span class="payout-checkbox__label">Payout Approval</span>
              <q-icon name="info" class="payout-info-icon" size="14px">
                <q-tooltip
                  anchor="top middle"
                  self="bottom middle"
                  :offset="[0, 6]"
                  max-width="260px"
                >
                  Notifies the donor when a withdrawal is ready and requires their confirmation
                  before releasing funds to the recipient, ensuring full control over each
                  transaction.
                </q-tooltip>
              </q-icon>
            </label>
          </div>

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

        <!-- RIGHT SIDE — Donation Summary -->
        <aside class="donation-summary-panel">
          <h3>DONATION SUMMARY</h3>

          <div class="summary-row">
            <span>Donor</span>
            <span>{{ form.name || '—' }}</span>
          </div>

          <div class="summary-row">
            <span>Recipient</span>
            <span>{{ selectedOrganizationName || '—' }}</span>
          </div>

          <div class="summary-row">
            <span>Deposit</span>
            <span>{{ summaryDeposit }}</span>
          </div>

          <div class="summary-row">
            <span>Withdrawal</span>
            <span>{{ summaryWithdrawal }}</span>
          </div>

          <div class="summary-row">
            <span>Fee (per cycle)</span>
            <span>{{ summaryFeePerCycle }}</span>
          </div>

          <div class="summary-row">
            <span>Cycles</span>
            <span>{{ summaryCycles }}</span>
          </div>

          <div class="summary-divider"></div>

          <div class="summary-row summary-total">
            <span>Total Amount</span>
            <span>{{ summaryTotalAmount }}</span>
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
import { Notify, useQuasar } from 'quasar'
import {
  broadcastRawTransaction,
  buildWalletConnectBchSignPayload,
  decimalBchToSatoshis,
  extractWalletSignedTransaction,
  fetchAddressUtxos,
  getBchRuntimeConfig,
  isValidChipnetAddress,
  lockingBytecodeToAddressVariants,
  normalizeChipnetAddress,
  selectInputsAndBuildPlan,
} from '../services/bchChipnet'
import { createVaultContract, saveVaultRecord, startAutoWithdraw } from '../services/vaultDonation'
import { api } from 'boot/axios'
import { CASHSCRIPT_CONTRACT_PATH } from '../contracts/recurringDonation'

import caraIcon from '../charity/Cara.ico'
import caritasManilaIcon from '../charity/Caritas Manila.ico'
import childHopePhIcon from '../charity/ChildHope PH.ico'
import gawadKalingaIcon from '../charity/Gawad Kalinga.ico'
import greenEarthIcon from '../charity/Green Earth.ico'
import haribonFoundationIcon from '../charity/Haribon Foundation.ico'
import saveTheChildrenIcon from '../charity/Save The Children.ico'
import worldVisionIcon from '../charity/World Vision.ico'

const $q = useQuasar()

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
    console.warn('[CrypToCare][notify:fallback]', payload)
  }
}

const DONATIONS_STORAGE_KEY = 'cryptocare.donations'
const WALLET_SNAPSHOT_STORAGE_KEY = 'cryptocare.wallet.snapshot'
const WALLET_BALANCE_ADJUST_EVENT = 'cryptocare:wallet-balance-adjust'
const WALLET_BALANCE_REFRESH_EVENT = 'cryptocare:wallet-balance-refresh'
const DONATION_SENT_EVENT = 'cryptocare:donation-sent'
const WALLET_CLIENT_GLOBAL_KEY = '__cryptocareWalletClient__'
const WALLET_REQUEST_TIMEOUT_MS = 30000
const PAYTACA_BCH_CHIPNET_WC_LIMITATION_MESSAGE =
  'Paytaca approved the request but did not return a signed BCH chipnet transaction over WalletConnect. No funds were sent. This appears to be a wallet-side issue.'

const bchConfig = getBchRuntimeConfig()

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

const intervalOptions = [
  { label: '10 mins', value: '10min' },
  { label: 'Weekly (coming soon)', value: 'weekly', disable: true },
  { label: 'Monthly (coming soon)', value: 'monthly', disable: true },
  { label: 'Quarterly (coming soon)', value: 'quarterly', disable: true },
  { label: 'Yearly (coming soon)', value: 'yearly', disable: true },
]

const INTERVAL_BLOCKS = {
  '10min': 1,
  weekly: 1008,
  monthly: 4320,
  quarterly: 12960,
  yearly: 52560,
}

const isIntervalSupported = (key) => key === '10min'

// --- API nonprofits (for address lookup) ---
const nonprofits = ref([])

const fetchNonprofits = async () => {
  try {
    const response = await api.get('nonprofits/verified/')
    nonprofits.value = response.data.map((np) => ({
      id: np.id,
      name: np.name,
      address: np.bch_address,
      category: np.category,
    }))
  } catch (error) {
    if (import.meta.env.DEV) console.error('Failed to load nonprofits:', error)
  }
}

// --- Form ---
const form = ref({
  cause: null,
  organization: null,
  coin: 'BCH',
  recipientAddress: '',
  deposit: '',
  withdrawal: '',
  interval: '10min',
  smartPayout: true,
  payoutApproval: false,
  name: '',
  email: '',
  contact: '',
  message: '',
})

const selectPayoutMode = (mode) => {
  if (mode === 'smart') {
    form.value.smartPayout = !form.value.smartPayout
    if (form.value.smartPayout) form.value.payoutApproval = false
  } else {
    form.value.payoutApproval = !form.value.payoutApproval
    if (form.value.payoutApproval) form.value.smartPayout = false
  }
  // Ensure at least one is selected
  if (!form.value.smartPayout && !form.value.payoutApproval) {
    form.value.smartPayout = true
  }
}

const payoutMode = computed(() => (form.value.payoutApproval ? 'inbox_approval' : 'smart'))

const conversionRates = ref({ BCH: 0, ETH: 0 })
const isSubmittingDonation = ref(false)
const submissionStatus = ref({ type: '', message: '' })

const submissionStatusClass = computed(() => ({
  'donation-status': true,
  'donation-status--error': submissionStatus.value.type === 'negative',
}))

// --- Computed options ---
const organizationOptions = computed(() => {
  if (!form.value.cause) return []
  return organizationCatalog.filter((org) => org.causes.includes(form.value.cause))
})

const selectedOrganizationName = computed(() => {
  const selected = organizationCatalog.find((o) => o.value === form.value.organization)
  return selected?.label || ''
})

const selectedOrganizationIcon = computed(() => {
  const selected = organizationCatalog.find((o) => o.value === form.value.organization)
  return selected?.icon || ''
})

const truncatedRecipientAddress = computed(() => {
  const addr = form.value.recipientAddress || ''
  if (addr.length <= 16) return addr
  const clean = addr.includes(':') ? addr.split(':')[1] : addr
  return `${clean.slice(0, 6)}...${clean.slice(-4)}`
})

const summaryDeposit = computed(() => {
  const v = Number(form.value.deposit)
  if (!v) return '—'
  return `${v.toFixed(8)} ${form.value.coin || ''}`
})

const summaryWithdrawal = computed(() => {
  const v = Number(form.value.withdrawal)
  if (!v) return '—'
  return `${v.toFixed(8)} ${form.value.coin || ''}`
})

const VAULT_MINER_FEE_SATS = 1000

const summaryFeePerCycle = computed(() => {
  if (form.value.coin !== 'BCH') return '—'
  return `${(VAULT_MINER_FEE_SATS / 1e8).toFixed(8)} BCH`
})

const summaryCycles = computed(() => {
  const deposit = Number(form.value.deposit)
  const withdrawal = Number(form.value.withdrawal)
  if (!deposit || !withdrawal || form.value.coin !== 'BCH') return '—'
  const depositSats = Math.round(deposit * 1e8)
  const withdrawalSats = Math.round(withdrawal * 1e8)
  const costPerCycle = withdrawalSats + VAULT_MINER_FEE_SATS
  if (costPerCycle <= 0) return '—'
  const cycles = Math.floor(depositSats / costPerCycle)
  return cycles > 0 ? `${cycles}` : '0'
})

const summaryTotalAmount = computed(() => {
  const deposit = Number(form.value.deposit)
  const withdrawal = Number(form.value.withdrawal)
  if (!deposit || form.value.coin !== 'BCH') return '—'
  if (!withdrawal) return `${deposit.toFixed(8)} BCH`
  const depositSats = Math.round(deposit * 1e8)
  const withdrawalSats = Math.round(withdrawal * 1e8)
  const costPerCycle = withdrawalSats + VAULT_MINER_FEE_SATS
  const cycles = costPerCycle > 0 ? Math.floor(depositSats / costPerCycle) : 0
  const totalFees = cycles * VAULT_MINER_FEE_SATS
  const totalSats = depositSats + totalFees
  return `${(totalSats / 1e8).toFixed(8)} BCH`
})

const intervalWarning = computed(() => {
  if (!form.value.interval) return ''
  if (isIntervalSupported(form.value.interval)) return ''
  return 'This interval is not yet fully supported. Only "10 mins" is functional for now.'
})

// --- PHP conversion ---
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

const fetchCryptoToPhpRates = async () => {
  try {
    const response = await fetch(
      'https://api.coingecko.com/api/v3/simple/price?ids=bitcoin-cash,ethereum&vs_currencies=php',
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

// --- Input sanitization ---
const sanitizeDecimalValue = (value) => {
  const cleaned = String(value ?? '').replace(/[^\d.]/g, '')
  const [integerPart, ...fractionParts] = cleaned.split('.')
  if (!fractionParts.length) return integerPart
  return `${integerPart}.${fractionParts.join('')}`
}

const onDecimalInput = (field, event) => {
  const sanitized = sanitizeDecimalValue(event?.target?.value)
  form.value[field] = sanitized
  if (event?.target) event.target.value = sanitized
}

// --- Watchers ---
watch(
  () => form.value.cause,
  () => {
    form.value.organization = null
    form.value.recipientAddress = ''
  },
)

watch(
  () => form.value.organization,
  (orgName) => {
    if (!orgName) {
      form.value.recipientAddress = ''
      return
    }
    const match = nonprofits.value.find((np) => np.name === orgName)
    if (match) form.value.recipientAddress = match.address
  },
)

// --- Auto-withdraw callback ---
const onVaultWithdrawCycle = ({ txid: cycleTxid, amount, drained, cycleNumber }) => {
  const amtBch = Number(amount) / 1e8
  const msg = drained
    ? `Vault fully drained to recipient! Cycle #${cycleNumber}, txid: ${cycleTxid}`
    : `Vault withdrawal #${cycleNumber} sent to recipient (${amtBch.toFixed(8)} BCH). Txid: ${cycleTxid}`
  notify({ type: 'positive', message: msg })
}

onMounted(() => {
  fetchNonprofits()
  fetchCryptoToPhpRates()
})

// --- Wallet helpers ---
const normalizeRecipientAddress = (value) => String(value ?? '').trim()

const isValidEthAddress = (value) => /^0x[0-9a-fA-F]{40}$/.test(normalizeRecipientAddress(value))

const isDecimalString = (value) => /^\d+(\.\d+)?$/.test(String(value ?? '').trim())

const parseEthAmountToWei = (value) => {
  const normalized = String(value ?? '').trim()
  if (!isDecimalString(normalized)) return null
  try {
    // Convert decimal ETH string to wei (bigint) without ethers dependency
    const [whole = '0', frac = ''] = normalized.split('.')
    const padded = `${frac}000000000000000000`.slice(0, 18)
    const wei = BigInt(whole) * 10n ** 18n + BigInt(padded)
    return wei > 0n ? wei : null
  } catch {
    return null
  }
}

const toHexQuantity = (value) => `0x${value.toString(16)}`

const getWalletClient = () => window?.[WALLET_CLIENT_GLOBAL_KEY] || null

const serializeErrorDetails = (error) => {
  if (!error) return { value: error }
  if (typeof error === 'string') return { message: error }
  if (typeof error !== 'object') return { value: String(error) }

  const snapshot = {
    prototype: Object.getPrototypeOf(error)?.constructor?.name || null,
    toString: typeof error?.toString === 'function' ? String(error.toString()) : null,
    message: error?.message,
    reason: error?.reason,
    code: error?.code,
    name: error?.name,
  }

  for (const key of Object.getOwnPropertyNames(error)) {
    try {
      snapshot[key] = error[key]
    } catch {
      snapshot[key] = '[unreadable]'
    }
  }

  if (error?.cause && typeof error.cause === 'object') {
    snapshot.cause = serializeErrorDetails(error.cause)
  }

  return snapshot
}

const getWalletSessionSummary = (walletClient) => {
  const session = walletClient?.session
  const bchNamespace = session?.namespaces?.bch || null
  return {
    topic: walletClient?.topic || null,
    chain: walletClient?.chain || null,
    address: walletClient?.address || null,
    methods: Array.isArray(bchNamespace?.methods) ? [...bchNamespace.methods] : [],
    accounts: Array.isArray(bchNamespace?.accounts) ? [...bchNamespace.accounts] : [],
  }
}

const summarizeBchSigningPayload = (payload) => {
  const transaction = payload?.transaction || {}
  const inputs = Array.isArray(transaction?.inputs) ? transaction.inputs : []
  const outputs = Array.isArray(transaction?.outputs) ? transaction.outputs : []
  const sourceOutputs = Array.isArray(payload?.sourceOutputs) ? payload.sourceOutputs : []
  return {
    inputCount: inputs.length,
    outputCount: outputs.length,
    sourceOutputCount: sourceOutputs.length,
    hasAccount: Boolean(payload?.account),
    account: payload?.account || null,
    broadcast: payload?.broadcast,
  }
}

const summarizeBchSigningCompatibility = (payload, walletClient) => {
  const sourceOutputs = Array.isArray(payload?.sourceOutputs) ? payload.sourceOutputs : []
  const firstSourceOutput = sourceOutputs[0] || null
  const sourceAddressVariants = lockingBytecodeToAddressVariants(firstSourceOutput?.lockingBytecode)
  const walletAddress = normalizeChipnetAddress(walletClient?.address)
  const walletHashOnly = walletAddress ? walletAddress.split(':')[1] : null
  const getHashOnly = (address) => {
    const normalized = normalizeChipnetAddress(address)
    return normalized ? normalized.split(':')[1] : null
  }
  const sourceHashOnly = getHashOnly(sourceAddressVariants?.bchtest)
  return {
    walletAddress: walletAddress || null,
    sourceAddressChipnet: sourceAddressVariants?.bchtest || null,
    sameHash: Boolean(walletHashOnly && sourceHashOnly && walletHashOnly === sourceHashOnly),
  }
}

const validateBchWalletSession = (walletClient, chainId) => {
  const summary = getWalletSessionSummary(walletClient)
  const normalizedAddress = normalizeChipnetAddress(summary.address)
  const hasMatchingAccount = summary.accounts.some((account) => {
    const rawAccountAddress = account.includes(':')
      ? account.slice(account.indexOf(':') + 1)
      : account
    return normalizeChipnetAddress(rawAccountAddress) === normalizedAddress
  })

  if (!summary.topic) {
    throw new Error('WalletConnect session topic is missing. Reconnect wallet and try again.')
  }
  if (summary.chain && summary.chain !== chainId) {
    throw new Error(
      `WalletConnect session chain mismatch. Expected ${chainId}, got ${summary.chain}.`,
    )
  }
  if (!summary.methods.includes('bch_signTransaction')) {
    throw new Error('WalletConnect session does not allow BCH transaction signing.')
  }
  if (normalizedAddress && summary.accounts.length > 0 && !hasMatchingAccount) {
    throw new Error('WalletConnect session account does not match the connected BCH address.')
  }
  return summary
}

const buildBchSignRequestVariants = (signingPayload) => {
  const base = signingPayload && typeof signingPayload === 'object' ? signingPayload : {}
  const transaction =
    base.transaction && typeof base.transaction === 'object' ? base.transaction : { inputs: [] }
  const inputs = Array.isArray(transaction.inputs) ? transaction.inputs : []
  const sourceOutputs = Array.isArray(base.sourceOutputs) ? base.sourceOutputs : []

  const inlineInputSourceOutput = {
    ...base,
    transaction: {
      ...transaction,
      inputs: inputs.map((input, index) => {
        const sourceOutput = sourceOutputs[index]
        if (!sourceOutput) return input
        return { ...input, sourceOutput }
      }),
    },
  }

  return [
    base,
    // Some wallets only parse source outputs when nested per-input.
    inlineInputSourceOutput,
    // Some wallets reject top-level sourceOutputs entirely.
    Object.fromEntries(
      Object.entries(inlineInputSourceOutput).filter(([key]) => key !== 'sourceOutputs'),
    ),
  ]
}

const executeWalletRequest = async (walletClient, chainId, method, candidateParams) => {
  let lastError = null
  for (const params of candidateParams) {
    try {
      if (import.meta.env.DEV) {
        console.info('[CrypToCare][donation-request:start]', { method, chainId, params })
      }

      // Capture request ID in parallel (not blocking) — needed for history fallback.
      let capturedRequestId = null
      if (typeof walletClient?.waitForRequestSent === 'function') {
        walletClient.waitForRequestSent(method, 8000).then((rec) => {
          capturedRequestId = rec?.id ?? null
        })
      }

      // Fire the request immediately — relay timeout races from this point.
      const requestPromise = walletClient.request({ chainId, request: { method, params } })

      let response
      try {
        response = await Promise.race([
          requestPromise,
          new Promise((_, reject) =>
            window.setTimeout(() => reject(new Error('RELAY_TIMEOUT')), WALLET_REQUEST_TIMEOUT_MS),
          ),
        ])
      } catch (relayError) {
        if (relayError?.message !== 'RELAY_TIMEOUT') throw relayError

        // Relay timed out delivering the response. The WalletConnect SDK stores
        // responses in its local history even when relay delivery fails — poll it.
        if (capturedRequestId !== null && typeof walletClient?.getHistoryRecord === 'function') {
          if (import.meta.env.DEV) {
            console.warn(
              '[CrypToCare][donation-request:relay-drop] Polling history for id:',
              capturedRequestId,
            )
          }
          const deadline = Date.now() + 20000
          while (Date.now() < deadline) {
            await new Promise((r) => window.setTimeout(r, 1500))
            const record = await walletClient.getHistoryRecord(capturedRequestId)
            if (record?.response?.result !== undefined) {
              if (import.meta.env.DEV) {
                console.info(
                  '[CrypToCare][donation-request:history-recovered]',
                  record.response.result,
                )
              }
              response = record.response.result
              break
            }
            if (record?.response?.error) {
              throw new Error(
                record.response.error?.message ||
                  record.response.error?.reason ||
                  'Wallet rejected the request.',
              )
            }
          }
        }

        if (response === undefined) {
          throw new Error(
            'Wallet accepted but the relay did not deliver the response. Please try again.',
          )
        }
      }

      if (import.meta.env.DEV) {
        console.info('[CrypToCare][donation-request:success]', { method, response })
      }
      return response
    } catch (error) {
      lastError = error
    }
  }
  throw lastError || new Error(`Wallet did not accept ${method} request.`)
}

const getErrorMessage = (error, fallback) => {
  const message =
    error?.message || error?.reason || error?.cause?.message || error?.data?.message || fallback
  if (typeof message !== 'string') return fallback
  if (/failed to publish custom payload|tag:\s*undefined/i.test(message)) {
    return 'Wallet could not relay the BCH signing payload (tag undefined). Reconnect WalletConnect and retry; if it persists, update or switch wallet app.'
  }
  if (
    /user rejected|rejected by user|denied by user|cancelled by user|canceled by user/i.test(
      message,
    )
  ) {
    return 'Transaction was rejected in wallet.'
  }
  return message
}

const extractTxReference = (result) => {
  if (typeof result === 'string') return result
  if (result && typeof result === 'object') {
    return result.txid || result.hash || result.transactionHash || result.result || null
  }
  return null
}

const sendEthDonation = async ({ walletClient, chainId, from, to, wei }) =>
  executeWalletRequest(walletClient, chainId, 'eth_sendTransaction', [
    [{ from, to, value: toHexQuantity(wei) }],
  ])

const isWalletCompatibleWithCoin = (walletSnapshot, coin) => {
  const namespace = walletSnapshot?.namespace || ''
  const chain = walletSnapshot?.chain || ''
  if (coin === 'BCH') return namespace === 'bch' && chain === 'bch:bchtest'
  if (coin === 'ETH')
    return namespace === 'eip155' && ['eip155:1', 'eip155:5', 'eip155:11155111'].includes(chain)
  return false
}

const getWalletSnapshot = () => {
  try {
    const raw = localStorage.getItem(WALLET_SNAPSHOT_STORAGE_KEY)
    if (!raw) return null
    return JSON.parse(raw)
  } catch {
    return null
  }
}

// --- Donation record persistence ---
const getStoredDonations = () => {
  try {
    const raw = localStorage.getItem(DONATIONS_STORAGE_KEY)
    if (!raw) return []
    const parsed = JSON.parse(raw)
    return Array.isArray(parsed) ? parsed : []
  } catch {
    return []
  }
}

const buildDonationId = () =>
  `donation-${Date.now()}-${Math.random().toString(36).slice(2, 8).toUpperCase()}`

const saveDonations = (records) => {
  localStorage.setItem(DONATIONS_STORAGE_KEY, JSON.stringify(records))
}

const upsertDonationRecord = (record) => {
  const existing = getStoredDonations()
  const withoutCurrent = existing.filter((item) => item?.id !== record.id)
  saveDonations([record, ...withoutCurrent])
}

const updateDonationRecord = (donationId, partial) => {
  const existing = getStoredDonations()
  const next = existing.map((item) => {
    if (item?.id !== donationId) return item
    return { ...item, ...partial, updatedAt: new Date().toISOString() }
  })
  saveDonations(next)
}

// --- BCH signing via WalletConnect ---
const signBchTransactionWithWalletConnect = async ({ walletClient, chainId, signingPayload }) => {
  const resolvedChainId = walletClient?.chain || chainId

  if (import.meta.env.DEV) {
    console.info(
      '[CrypToCare][bch-session:preflight]',
      validateBchWalletSession(walletClient, resolvedChainId),
    )
  } else {
    validateBchWalletSession(walletClient, resolvedChainId)
  }

  try {
    const candidatePayloads = buildBchSignRequestVariants(signingPayload)
    if (import.meta.env.DEV) {
      console.info(
        '[CrypToCare][bch-sign-variants]',
        candidatePayloads.map((payload, idx) => ({
          variant: idx + 1,
          ...summarizeBchSigningPayload(payload),
        })),
      )
    }
    return await executeWalletRequest(
      walletClient,
      resolvedChainId,
      'bch_signTransaction',
      candidatePayloads,
    )
  } catch (error) {
    const details = serializeErrorDetails(error)
    const walletReason = details?.reason || error?.reason
    if (walletReason && typeof walletReason === 'string') {
      throw new Error(`Wallet signing error: ${walletReason}`)
    }

    const hasOpaqueWalletError =
      details?.prototype === 'Object' &&
      details?.message === undefined &&
      details?.reason === undefined

    if (resolvedChainId === 'bch:bchtest' && hasOpaqueWalletError) {
      throw new Error(PAYTACA_BCH_CHIPNET_WC_LIMITATION_MESSAGE)
    }

    throw error
  }
}

// --- BCH Vault Donation Flow ---
const runChipnetBchDonationFlow = async ({
  walletClient,
  chainId,
  senderAddress,
  charityAddress,
  amountSatoshis,
  amountCoin,
  donationId,
  withdrawalSatoshis,
  withdrawalCoin,
  intervalBlocks,
  intervalLabel,
  totalCycles,
  mode,
  donorEmail,
  donorName,
}) => {
  // 1. Instantiate the vault contract and derive the P2SH20 address
  submissionStatus.value = { type: '', message: 'Creating vault contract...' }

  const vault = createVaultContract({
    recipientAddress: charityAddress,
    funderAddress: senderAddress,
    withdrawalAmount: withdrawalSatoshis,
    intervalBlocks,
  })

  const vaultAddress = vault.address

  if (import.meta.env.DEV) {
    console.info('[CrypToCare][vault-contract]', {
      vaultAddress,
      params: vault.params,
      charityAddress,
      senderAddress,
    })
  }

  // 2. Build and sign a funding transaction to the vault address
  const feeRate = Number.isFinite(bchConfig.feeRateSatsPerByte) ? bchConfig.feeRateSatsPerByte : 1.2

  const utxos = await fetchAddressUtxos({ address: senderAddress })

  const plan = selectInputsAndBuildPlan({
    utxos,
    amountSatoshis,
    feeRateSatsPerByte: feeRate,
  })

  const signingPayload = buildWalletConnectBchSignPayload({
    plan,
    senderAddress,
    charityAddress: vaultAddress,
    changeAddress: senderAddress,
    amountSatoshis,
    userPrompt: `Fund vault contract for ${amountCoin} BCH → ${charityAddress}`,
    signingAccount: senderAddress,
    includeInlineSourceOutputs: false,
  })

  if (import.meta.env.DEV) {
    console.info('[CrypToCare][bch-sign-payload]', summarizeBchSigningPayload(signingPayload))
    console.info(
      '[CrypToCare][bch-sign-compat]',
      summarizeBchSigningCompatibility(signingPayload, walletClient),
    )
  }

  submissionStatus.value = {
    type: '',
    message:
      'Waiting for wallet signature... confirm in Paytaca. (May take a moment after accepting)',
  }

  const signedResult = await signBchTransactionWithWalletConnect({
    walletClient,
    chainId,
    signingPayload,
  })

  submissionStatus.value = { type: '', message: 'Signature received. Broadcasting to Chipnet...' }

  const { rawTxHex, signedTxid } = extractWalletSignedTransaction(signedResult)

  const broadcast = await broadcastRawTransaction({ rawTxHex })

  const txid = broadcast.txid || signedTxid
  if (!txid) {
    throw new Error('Unable to resolve BCH transaction id after broadcast.')
  }

  // 3. Save vault record and start auto-withdraw
  const vaultRecord = {
    donationId,
    createdAt: new Date().toISOString(),
    fundingTxid: txid,
    vaultAddress,
    depositSatoshis: amountSatoshis.toString(),
    depositCoin: amountCoin,
    withdrawalSatoshis: withdrawalSatoshis.toString(),
    withdrawalCoin,
    intervalBlocks,
    intervalLabel,
    totalCycles: totalCycles || 0,
    recipientAddress: charityAddress,
    funderAddress: senderAddress,
    contractParams: vault.params,
    payoutMode: mode || 'smart',
    donorEmail: donorEmail || '',
    donorName: donorName || '',
    status: 'funded',
  }
  saveVaultRecord(vaultRecord)

  // Begin auto-withdraw loop — will send to recipient once interval elapses
  startAutoWithdraw(vaultRecord, onVaultWithdrawCycle)

  updateDonationRecord(donationId, {
    status: 'sent',
    txReference: txid,
    txid,
    vaultAddress,
    feeSatoshis: plan.fee.toString(),
    confirmations: 0,
  })

  window.dispatchEvent(
    new CustomEvent(DONATION_SENT_EVENT, {
      detail: {
        txHash: txid,
        coin: 'BCH',
        chain: chainId,
        recipientAddress: charityAddress,
        vaultAddress,
        amount: amountCoin,
      },
    }),
  )

  return { txid, vaultAddress, confirmations: 0, feeSatoshis: plan.fee }
}

// --- Form reset ---
const resetForm = () => {
  form.value = {
    cause: null,
    organization: null,
    coin: 'BCH',
    recipientAddress: '',
    deposit: '',
    smartPayout: true,
    payoutApproval: false,
    withdrawal: '',
    interval: '10min',
    name: '',
    email: '',
    contact: '',
    message: '',
  }
}

// --- Submit Donation ---
const submitDonation = async () => {
  if (isSubmittingDonation.value) return

  submissionStatus.value = { type: '', message: '' }

  const selectedCoin = form.value.coin
  const typedRecipientAddress = normalizeRecipientAddress(form.value.recipientAddress)
  const recipientAddress =
    selectedCoin === 'BCH' ? normalizeChipnetAddress(typedRecipientAddress) : typedRecipientAddress
  const depositSatoshis = selectedCoin === 'BCH' ? decimalBchToSatoshis(form.value.deposit) : null
  const withdrawalSatoshis =
    selectedCoin === 'BCH' ? decimalBchToSatoshis(form.value.withdrawal) : null
  const amountUnitsEth = selectedCoin === 'ETH' ? parseEthAmountToWei(form.value.deposit) : null
  const depositCoin = Number.parseFloat(String(form.value.deposit ?? '').trim())
  const withdrawalCoin = Number.parseFloat(String(form.value.withdrawal ?? '').trim())
  const selectedInterval = form.value.interval
  const intervalBlocks = INTERVAL_BLOCKS[selectedInterval] || 1
  const walletSnapshot = getWalletSnapshot()
  const walletClient = getWalletClient()
  const activeAccount = walletClient?.address || walletSnapshot?.address || ''
  const activeChain = walletClient?.chain || walletSnapshot?.chain || ''

  // --- Validation ---
  if (!form.value.cause || !form.value.organization) {
    submissionStatus.value = {
      type: 'negative',
      message: 'Please select a cause and organization.',
    }
    notify({ type: 'warning', message: 'Please select a cause and organization.' })
    return
  }

  if (!walletSnapshot?.connected || !activeAccount || !activeChain) {
    submissionStatus.value = {
      type: 'negative',
      message: 'Please connect your wallet before donating.',
    }
    notify({ type: 'warning', message: 'Please connect your wallet before donating.' })
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
    notify({ type: 'warning', message: 'Please select a coin for this donation.' })
    return
  }

  if (selectedCoin === 'BCH' && !bchConfig.isChipnet) {
    submissionStatus.value = {
      type: 'negative',
      message: 'BCH donations require BCH_NETWORK=chipnet in app configuration.',
    }
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
    notify({ type: 'warning', message: `Connected wallet is not compatible with ${selectedCoin}.` })
    return
  }

  if (selectedCoin === 'BCH' && !isIntervalSupported(selectedInterval)) {
    submissionStatus.value = {
      type: 'negative',
      message: 'Only the "10 mins" interval is fully supported for now.',
    }
    return
  }

  const amountUnits = selectedCoin === 'BCH' ? depositSatoshis : amountUnitsEth
  if (!Number.isFinite(depositCoin) || depositCoin <= 0 || !amountUnits) {
    submissionStatus.value = { type: 'negative', message: 'Please enter a valid deposit amount.' }
    notify({ type: 'warning', message: 'Please enter a valid deposit amount.' })
    return
  }

  if (selectedCoin === 'BCH') {
    if (!Number.isFinite(withdrawalCoin) || withdrawalCoin <= 0 || !withdrawalSatoshis) {
      submissionStatus.value = {
        type: 'negative',
        message: 'Please enter a valid withdrawal amount per cycle.',
      }
      notify({ type: 'warning', message: 'Please enter a valid withdrawal amount per cycle.' })
      return
    }
    if (withdrawalSatoshis >= depositSatoshis) {
      submissionStatus.value = {
        type: 'negative',
        message: 'Withdrawal per cycle must be less than the total deposit.',
      }
      notify({
        type: 'warning',
        message: 'Withdrawal per cycle must be less than the total deposit.',
      })
      return
    }
  }

  // Require email when inbox_approval is selected
  if (payoutMode.value === 'inbox_approval' && !form.value.email) {
    submissionStatus.value = {
      type: 'negative',
      message: 'Donor email is required for Payout Approval mode.',
    }
    notify({ type: 'warning', message: 'Please enter your email for Payout Approval.' })
    return
  }

  if (selectedCoin === 'BCH' && !isValidChipnetAddress(typedRecipientAddress)) {
    submissionStatus.value = {
      type: 'negative',
      message: 'Recipient must be a valid BCH Chipnet address (bchtest:...).',
    }
    notify({
      type: 'warning',
      message: 'Recipient must be a valid BCH Chipnet address (bchtest:...).',
    })
    return
  }

  if (selectedCoin === 'ETH' && !isValidEthAddress(recipientAddress)) {
    submissionStatus.value = {
      type: 'negative',
      message: 'Recipient must be a valid ETH address (0x + 40 hex chars).',
    }
    return
  }

  // --- Build donation record ---
  const donationId = buildDonationId()
  const donationRecord = {
    id: donationId,
    createdAt: new Date().toISOString(),
    status: selectedCoin === 'BCH' ? 'preparing' : 'sent',
    txReference: null,
    chain: activeChain,
    donor: {
      name: form.value.name || 'Anonymous',
      email: form.value.email,
      contactNumber: form.value.contact || '',
      message: form.value.message || '',
      walletAddress: activeAccount,
      coin: selectedCoin,
    },
    recipient: {
      cause: form.value.cause,
      organization: form.value.organization,
      address: recipientAddress,
    },
    values: {
      coin: selectedCoin,
      deposit: amountUnits.toString(),
      depositCoin,
      ...(selectedCoin === 'BCH'
        ? {
            withdrawal: withdrawalSatoshis.toString(),
            withdrawalCoin,
            interval: selectedInterval,
            intervalBlocks,
          }
        : {}),
    },
    contract: {
      version: '0.12.0',
      ...(selectedCoin === 'BCH'
        ? { type: 'vault-bch-donation', contractPath: CASHSCRIPT_CONTRACT_PATH }
        : { type: 'direct-eth-transfer' }),
    },
  }

  upsertDonationRecord(donationRecord)
  isSubmittingDonation.value = true

  try {
    submissionStatus.value = {
      type: '',
      message: 'Waiting for wallet approval... confirm in your wallet app.',
    }

    let txReference = null
    let vaultAddr = ''

    if (selectedCoin === 'BCH') {
      // Total = deposit + (cycles × miner fee) so the vault can cover all withdrawal fees
      const feeSats = BigInt(VAULT_MINER_FEE_SATS)
      const costPerCycle = withdrawalSatoshis + feeSats
      const cycles = costPerCycle > 0n ? depositSatoshis / costPerCycle : 0n
      const totalFees = cycles * feeSats
      const totalSatoshis = depositSatoshis + totalFees
      const totalCoin = Number(totalSatoshis) / 1e8

      const bchResult = await runChipnetBchDonationFlow({
        walletClient,
        chainId: activeChain,
        senderAddress: activeAccount,
        charityAddress: recipientAddress,
        amountSatoshis: totalSatoshis,
        amountCoin: totalCoin,
        donationId,
        withdrawalSatoshis,
        withdrawalCoin,
        intervalBlocks,
        intervalLabel: selectedInterval,
        totalCycles: Number(cycles),
        mode: payoutMode.value,
        donorEmail: form.value.email,
        donorName: form.value.name,
      })
      txReference = bchResult.txid
      vaultAddr = bchResult.vaultAddress || ''
    } else {
      const txResult = await sendEthDonation({
        walletClient,
        chainId: activeChain,
        from: activeAccount,
        to: recipientAddress,
        wei: amountUnits,
      })
      txReference = extractTxReference(txResult)
      updateDonationRecord(donationId, { status: 'sent', txReference })
    }

    // Also save to backend database (best-effort)
    try {
      const matchedNp = nonprofits.value.find((np) => np.name === form.value.organization)
      const explorerUrl = txReference ? `https://chipnet.bchexplorer.info/tx/${txReference}` : ''
      const donationRes = await api.post('donations/', {
        txid: txReference,
        recipient: form.value.recipientAddress,
        amount: depositCoin,
        coin: form.value.coin,
        cause: form.value.cause,
        message: form.value.message,
        donor_name: form.value.name || 'Anonymous',
        donor_email: form.value.email,
        donor_contact: form.value.contact,
        explorer_url: explorerUrl,
        nonprofit: matchedNp?.id,
        contract: vaultAddr,
        interval: form.value.interval,
        interval_blocks: intervalBlocks,
        payout_mode: payoutMode.value,
        wallet_address: (activeAccount || '').toLowerCase(),
      })

      // Schedule all payout cycles in the backend so the dashboard
      // can display them in Pending Withdrawals and show the Withdraw button.
      if (selectedCoin === 'BCH' && withdrawalSatoshis && intervalBlocks) {
        const savedDonationId = donationRes?.data?.id
        const feeSats = BigInt(VAULT_MINER_FEE_SATS)
        const costPerCycle = withdrawalSatoshis + feeSats
        const totalCycles = costPerCycle > 0n ? Number(depositSatoshis / costPerCycle) : 0
        const intervalMs = Number(intervalBlocks) * 10 * 60 * 1000

        for (let cycle = 1; cycle <= totalCycles; cycle++) {
          const dueAt = new Date(Date.now() + cycle * intervalMs).toISOString()
          // best-effort — don't block on failures
          api
            .post('payouts/request/', {
              donation_id: savedDonationId ?? donationId,
              donor_email: form.value.email || '',
              donor_name: form.value.name || 'Anonymous',
              recipient_address: form.value.recipientAddress,
              vault_address: vaultAddr,
              payout_amount_satoshis: Number(withdrawalSatoshis),
              coin: form.value.coin,
              interval_label: form.value.interval,
              interval_blocks: intervalBlocks,
              cycle_number: cycle,
              total_cycles: totalCycles,
              due_at: dueAt,
              payout_mode: payoutMode.value,
            })
            .catch(() => {
              /* best-effort */
            })
        }
      }
    } catch {
      /* backend save is best-effort */
    }

    window.dispatchEvent(
      new CustomEvent(WALLET_BALANCE_ADJUST_EVENT, {
        detail: { delta: -depositCoin, chain: activeChain, address: activeAccount },
      }),
    )

    setTimeout(() => {
      window.dispatchEvent(
        new CustomEvent(WALLET_BALANCE_REFRESH_EVENT, {
          detail: { chain: activeChain, address: activeAccount },
        }),
      )
    }, 2000)

    notify({
      type: 'positive',
      message: txReference
        ? `Donation sent successfully! Txid: ${txReference}`
        : 'Donation sent successfully!',
    })

    submissionStatus.value = {
      type: 'positive',
      message: txReference
        ? `Donation sent successfully! Txid: ${txReference}`
        : 'Donation sent successfully!',
    }

    resetForm()
  } catch (error) {
    const failureMessage = getErrorMessage(
      error,
      'Donation transaction failed or was rejected by wallet.',
    )
    const isKnownPaytacaChipnetLimitation =
      failureMessage === PAYTACA_BCH_CHIPNET_WC_LIMITATION_MESSAGE

    updateDonationRecord(donationId, { status: 'failed', lastError: failureMessage })

    submissionStatus.value = {
      type: isKnownPaytacaChipnetLimitation ? 'warning' : 'negative',
      message: failureMessage,
    }
    if (!isKnownPaytacaChipnetLimitation) {
      notify({ type: 'negative', message: failureMessage })
    }
  } finally {
    isSubmittingDonation.value = false
  }
}
</script>

<style scoped>
/* ── Glassmorphism panels ────────────────────────────────────── */
.donation-form-panel {
  background: rgba(255, 255, 255, 0.6);
  backdrop-filter: blur(20px) saturate(180%);
  -webkit-backdrop-filter: blur(20px) saturate(180%);
  border: 2px solid #1565c0;
  border-radius: 20px;
  box-shadow:
    0 2px 0 rgba(21, 101, 192, 0.12),
    0 8px 32px rgba(30, 40, 80, 0.14),
    0 16px 48px rgba(30, 40, 80, 0.08);
  padding: 28px;
  transition:
    box-shadow 0.25s ease,
    transform 0.25s ease;
}
.donation-form-panel:hover {
  box-shadow:
    0 2px 0 rgba(21, 101, 192, 0.18),
    0 12px 40px rgba(30, 40, 80, 0.18),
    0 24px 60px rgba(30, 40, 80, 0.1);
  transform: translateY(-3px);
}

.donation-summary-panel {
  background: rgba(255, 255, 255, 0.6);
  backdrop-filter: blur(20px) saturate(180%);
  -webkit-backdrop-filter: blur(20px) saturate(180%);
  border: 2px solid #1565c0;
  border-radius: 20px;
  box-shadow:
    0 2px 0 rgba(21, 101, 192, 0.12),
    0 8px 32px rgba(30, 40, 80, 0.14),
    0 16px 48px rgba(30, 40, 80, 0.08);
  padding: 28px;
  transition:
    box-shadow 0.25s ease,
    transform 0.25s ease;
}
.donation-summary-panel:hover {
  box-shadow:
    0 2px 0 rgba(21, 101, 192, 0.18),
    0 12px 40px rgba(30, 40, 80, 0.18),
    0 24px 60px rgba(30, 40, 80, 0.1);
  transform: translateY(-3px);
}

/* Dark mode */
.body--dark .donation-form-panel,
.body--dark .donation-summary-panel {
  background: rgba(20, 24, 40, 0.65);
  backdrop-filter: blur(20px) saturate(160%);
  -webkit-backdrop-filter: blur(20px) saturate(160%);
  border: 2px solid #42a5f5;
  box-shadow:
    0 2px 0 rgba(66, 165, 245, 0.12),
    0 8px 32px rgba(0, 0, 0, 0.4),
    0 16px 48px rgba(0, 0, 0, 0.22);
}
.body--dark .donation-form-panel:hover,
.body--dark .donation-summary-panel:hover {
  box-shadow:
    0 2px 0 rgba(66, 165, 245, 0.2),
    0 12px 40px rgba(0, 0, 0, 0.5),
    0 24px 60px rgba(0, 0, 0, 0.28);
  transform: translateY(-3px);
}

.donation-status {
  font-size: 0.86rem;
  color: #1f7a1f;
}

.donation-status--error {
  color: #b00020;
}

.interval-warning {
  font-size: 0.82rem;
  color: #b06000;
  font-weight: 600;
}
</style>

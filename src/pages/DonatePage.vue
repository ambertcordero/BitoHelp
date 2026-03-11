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
            <div class="floating-field mini-field" :class="{ 'is-filled': form.deposit !== '' }">
              <input
                :value="form.deposit"
                type="text"
                inputmode="decimal"
                placeholder=" "
                @input="onDecimalInput('deposit', $event)"
              />
              <label>Deposit (BCH)</label>
              <span class="php-conversion">{{ depositPhp }}</span>
            </div>

            <div class="floating-field mini-field is-filled">
              <input value="5 minutes" type="text" readonly placeholder=" " />
              <label>Interval</label>
            </div>

            <div class="floating-field mini-field" :class="{ 'is-filled': form.withdrawal !== '' }">
              <input
                :value="form.withdrawal"
                type="text"
                inputmode="decimal"
                placeholder=" "
                @input="onDecimalInput('withdrawal', $event)"
              />
              <label>Withdrawal (BCH)</label>
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
            <span>Deposit</span>
            <span>{{ summaryAmount }}</span>
          </div>

          <div class="summary-row">
            <span>Interval</span>
            <span>5 minutes</span>
          </div>

          <div class="summary-row">
            <span>Withdrawal</span>
            <span>{{ summaryWithdrawal }}</span>
          </div>

          <div class="summary-divider"></div>

          <q-btn
            class="donate-now-btn"
            label="DEPOSIT NOW"
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
import { parseEther } from 'ethers'
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
  waitForConfirmations,
} from '../services/bchChipnet'

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
const BCH_CONFIRMATION_MIN = 1

const bchConfig = getBchRuntimeConfig()

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
  deposit: '',
  withdrawal: '',
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
  const amount = Number(form.value.deposit)
  if (!amount) {
    return '—'
  }

  return `${amount.toFixed(8)} BCH`
})

const summaryWithdrawal = computed(() => {
  const withdrawal = Number(form.value.withdrawal)
  if (!withdrawal) {
    return '—'
  }

  return `${withdrawal.toFixed(8)} BCH`
})

const formatPhp = (amount) =>
  Number(amount).toLocaleString('en-PH', {
    style: 'currency',
    currency: 'PHP',
    minimumFractionDigits: 2,
    maximumFractionDigits: 2,
  })

const depositPhp = computed(() => {
  const amount = Number(form.value.deposit)
  const rate = conversionRates.value.BCH || 0
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

const isDecimalString = (value) => /^\d+(\.\d+)?$/.test(String(value ?? '').trim())

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

const serializeErrorDetails = (error) => {
  if (!error) {
    return { value: error }
  }

  if (typeof error === 'string') {
    return { message: error }
  }

  if (typeof error !== 'object') {
    return { value: String(error) }
  }

  const prototypeName = Object.getPrototypeOf(error)?.constructor?.name || null
  const symbolKeys = Object.getOwnPropertySymbols(error)

  const propertyNames = Object.getOwnPropertyNames(error)
  const snapshot = {
    prototype: prototypeName,
    toString: typeof error?.toString === 'function' ? String(error.toString()) : null,
    message: error?.message,
    code: error?.code,
    name: error?.name,
  }

  for (const key of propertyNames) {
    try {
      snapshot[key] = error[key]
    } catch {
      snapshot[key] = '[unreadable]'
    }
  }

  if (symbolKeys.length > 0) {
    snapshot.symbolProps = {}
    for (const symbolKey of symbolKeys) {
      const symbolName = String(symbolKey)
      try {
        snapshot.symbolProps[symbolName] = error[symbolKey]
      } catch {
        snapshot.symbolProps[symbolName] = '[unreadable]'
      }
    }
  }

  if (error?.cause && typeof error.cause === 'object') {
    snapshot.cause = serializeErrorDetails(error.cause)
  }

  if (error?.data && typeof error.data === 'object') {
    snapshot.data = { ...error.data }
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
    transportType: session?.transportType || null,
    sessionConfig: session?.sessionConfig || null,
    peerRedirect: session?.peer?.metadata?.redirect || null,
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
    everyInputHasInlineSourceOutput: inputs.every((input) => Boolean(input?.sourceOutput)),
    hasAccount: Boolean(payload?.account),
    account: payload?.account || null,
    broadcast: payload?.broadcast,
    locktime: transaction?.locktime,
    version: transaction?.version,
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
    walletHashOnly,
    sourceAddressMainnet: sourceAddressVariants?.bitcoincash || null,
    sourceAddressChipnet: sourceAddressVariants?.bchtest || null,
    sourceHashOnly,
    sameHash: Boolean(walletHashOnly && sourceHashOnly && walletHashOnly === sourceHashOnly),
    exactChipnetMatch: Boolean(
      walletAddress &&
      sourceAddressVariants?.bchtest &&
      walletAddress === sourceAddressVariants.bchtest,
    ),
  }
}

const ensureWalletSessionReachable = async (walletClient, timeoutMs = 10000) => {
  if (typeof walletClient?.ping !== 'function') {
    return true
  }

  await Promise.race([
    walletClient.ping(),
    new Promise((_, reject) => {
      window.setTimeout(() => {
        reject(
          new Error('WalletConnect session is not responding. Reconnect wallet and try again.'),
        )
      }, timeoutMs)
    }),
  ])

  return true
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
      `WalletConnect session chain mismatch. Expected ${chainId}, got ${summary.chain}. Reconnect wallet and try again.`,
    )
  }

  if (!summary.methods.includes('bch_signTransaction')) {
    throw new Error(
      'WalletConnect session does not allow BCH transaction signing. Reconnect wallet and try again.',
    )
  }

  if (normalizedAddress && summary.accounts.length > 0 && !hasMatchingAccount) {
    throw new Error(
      'WalletConnect session account does not match the connected BCH address. Reconnect wallet and try again.',
    )
  }

  return summary
}

const executeWalletRequest = async (walletClient, chainId, method, candidateParams) => {
  let lastError = null
  let sawOpaqueWalletReject = false

  for (const params of candidateParams) {
    const requestSentPromise =
      typeof walletClient?.waitForRequestSent === 'function'
        ? walletClient.waitForRequestSent(method)
        : Promise.resolve(null)

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

      const requestMeta = await requestSentPromise
      const historyRecord = requestMeta?.id
        ? await walletClient?.getHistoryRecord?.(requestMeta.id)
        : null

      if (import.meta.env.DEV) {
        console.info('[BitoHelp][donation-request:success]', {
          method,
          chainId,
          response,
          requestMeta,
          historyRecord,
        })
      }

      return response
    } catch (error) {
      const requestMeta = await requestSentPromise.catch(() => null)
      const historyRecord = requestMeta?.id
        ? await walletClient?.getHistoryRecord?.(requestMeta.id)
        : null
      const pendingHistory = walletClient?.getPendingHistory?.() || []

      if (import.meta.env.DEV) {
        console.error('[BitoHelp][donation-request:error]', {
          method,
          chainId,
          error,
          errorDetails: serializeErrorDetails(error),
          requestMeta,
          historyRecord,
          pendingHistory,
          walletSession:
            method === 'bch_signTransaction' ? getWalletSessionSummary(walletClient) : undefined,
        })
      }

      if (
        method === 'bch_signTransaction' &&
        error &&
        typeof error === 'object' &&
        Object.keys(error).length === 0
      ) {
        sawOpaqueWalletReject = true
      }

      lastError = error

      const message = String(error?.message || '')
      if (/timed out/i.test(message)) {
        break
      }
    }
  }

  if (method === 'bch_signTransaction' && sawOpaqueWalletReject) {
    throw new Error(
      'Paytaca rejected BCH signing without error details. This appears to be a wallet-side chipnet signing issue.',
    )
  }

  throw lastError || new Error(`Wallet did not accept ${method} request.`)
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
  if (typeof result === 'string') {
    return result
  }

  if (result && typeof result === 'object') {
    return result.txid || result.hash || result.transactionHash || result.result || null
  }

  return null
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
    if (item?.id !== donationId) {
      return item
    }
    return {
      ...item,
      ...partial,
      updatedAt: new Date().toISOString(),
    }
  })
  saveDonations(next)
}

const signBchTransactionWithWalletConnect = async ({ walletClient, chainId, signingPayload }) => {
  const resolvedChainId = walletClient?.chain || chainId

  if (import.meta.env.DEV) {
    console.info(
      '[BitoHelp][bch-session:preflight]',
      validateBchWalletSession(walletClient, resolvedChainId),
    )
  } else {
    validateBchWalletSession(walletClient, resolvedChainId)
  }

  await ensureWalletSessionReachable(walletClient)

  return executeWalletRequest(walletClient, resolvedChainId, 'bch_signTransaction', [
    signingPayload,
  ])
}

const runChipnetBchDonationFlow = async ({
  walletClient,
  chainId,
  senderAddress,
  charityAddress,
  amountSatoshis,
  depositCoin,
  donationId,
}) => {
  const feeRate = Number.isFinite(bchConfig.feeRateSatsPerByte) ? bchConfig.feeRateSatsPerByte : 1.2

  const utxos = await fetchAddressUtxos({
    apiBaseUrl: bchConfig.apiBaseUrl,
    address: senderAddress,
  })

  const plan = selectInputsAndBuildPlan({
    utxos,
    amountSatoshis,
    feeRateSatsPerByte: feeRate,
  })

  const signingPayload = buildWalletConnectBchSignPayload({
    plan,
    senderAddress,
    charityAddress,
    changeAddress: senderAddress,
    amountSatoshis,
    userPrompt: `Deposit ${depositCoin} BCH vault for ${charityAddress} (interval 5 minutes, withdrawal ${form.value.withdrawal || '0'} BCH)`,
    signingAccount: senderAddress,
    includeInlineSourceOutputs: false,
  })

  if (import.meta.env.DEV) {
    console.info('[BitoHelp][bch-sign-payload]', summarizeBchSigningPayload(signingPayload))
    console.info(
      '[BitoHelp][bch-sign-compat]',
      summarizeBchSigningCompatibility(signingPayload, walletClient),
    )
  }

  submissionStatus.value = {
    type: '',
    message: 'Waiting for wallet signature... confirm in Paytaca.',
  }

  const signedResult = await signBchTransactionWithWalletConnect({
    walletClient,
    chainId,
    signingPayload,
  })

  const { rawTxHex, signedTxid } = extractWalletSignedTransaction(signedResult)

  submissionStatus.value = {
    type: '',
    message: 'Broadcasting signed transaction to Chipnet...',
  }

  const broadcast = await broadcastRawTransaction({
    apiBaseUrl: bchConfig.apiBaseUrl,
    rawTxHex,
  })

  const txid = broadcast.txid || signedTxid
  if (!txid) {
    throw new Error('Unable to resolve BCH transaction id after broadcast.')
  }

  updateDonationRecord(donationId, {
    status: 'pending',
    txReference: txid,
    txid,
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
        amount: depositCoin,
      },
    }),
  )

  submissionStatus.value = {
    type: '',
    message: `Broadcasted. Waiting for ${BCH_CONFIRMATION_MIN} confirmation on Chipnet...`,
  }

  const confirmation = await waitForConfirmations({
    apiBaseUrl: bchConfig.apiBaseUrl,
    txid,
    minConfirmations: BCH_CONFIRMATION_MIN,
  })

  if (!confirmation.confirmed) {
    updateDonationRecord(donationId, {
      status: 'pending',
      confirmations: 0,
      lastError: 'Confirmation timeout',
    })
    throw new Error('Transaction broadcasted but confirmation timed out. It may confirm shortly.')
  }

  updateDonationRecord(donationId, {
    status: 'confirmed',
    confirmations: confirmation.confirmations,
    confirmedAt: new Date().toISOString(),
  })

  return {
    txid,
    confirmations: confirmation.confirmations,
    feeSatoshis: plan.fee,
  }
}

const resetForm = () => {
  form.value = {
    cause: null,
    organization: null,
    coin: 'BCH',
    recipientAddress: '',
    deposit: '',
    withdrawal: '',
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
  const typedRecipientAddress = normalizeRecipientAddress(form.value.recipientAddress)
  const recipientAddress =
    selectedCoin === 'BCH' ? normalizeChipnetAddress(typedRecipientAddress) : typedRecipientAddress
  const depositUnitsEth = selectedCoin === 'ETH' ? parseEthAmountToWei(form.value.deposit) : null
  const depositUnitsBch = selectedCoin === 'BCH' ? decimalBchToSatoshis(form.value.deposit) : null
  const depositCoin = Number.parseFloat(String(form.value.deposit ?? '').trim())
  const withdrawalUnitsBch = decimalBchToSatoshis(form.value.withdrawal)
  const withdrawalCoin = Number.parseFloat(String(form.value.withdrawal ?? '').trim())
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

  if (selectedCoin === 'BCH' && !bchConfig.isChipnet) {
    submissionStatus.value = {
      type: 'negative',
      message: 'BCH donations require BCH_NETWORK=chipnet in app configuration.',
    }
    notify({
      type: 'warning',
      message: 'Set BCH_NETWORK=chipnet before sending BCH donations.',
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

  const amountUnits = selectedCoin === 'BCH' ? depositUnitsBch : depositUnitsEth

  if (!Number.isFinite(depositCoin) || depositCoin <= 0 || !amountUnits) {
    submissionStatus.value = {
      type: 'negative',
      message: 'Please enter a valid BCH deposit amount.',
    }
    notify({
      type: 'warning',
      message: 'Please enter a valid BCH deposit amount.',
    })
    return
  }

  if (
    selectedCoin === 'BCH' &&
    (!Number.isFinite(withdrawalCoin) || withdrawalCoin <= 0 || !withdrawalUnitsBch)
  ) {
    submissionStatus.value = {
      type: 'negative',
      message: 'Please enter a valid BCH withdrawal amount.',
    }
    notify({
      type: 'warning',
      message: 'Please enter a valid BCH withdrawal amount.',
    })
    return
  }

  if (selectedCoin === 'BCH' && withdrawalUnitsBch > amountUnits) {
    submissionStatus.value = {
      type: 'negative',
      message: 'Withdrawal amount cannot be greater than deposit amount.',
    }
    notify({
      type: 'warning',
      message: 'Withdrawal amount cannot be greater than deposit amount.',
    })
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
    notify({
      type: 'warning',
      message: 'For ETH, recipient must be a valid address (0x + 40 hex chars).',
    })
    return
  }

  const donationId = buildDonationId()
  const donationRecord = {
    id: donationId,
    createdAt: new Date().toISOString(),
    status: selectedCoin === 'BCH' ? 'preparing' : 'sent',
    txReference: null,
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
      addressType: selectedCoin === 'BCH' ? 'bch-chipnet-address' : 'eth',
    },
    values: {
      coin: selectedCoin,
      amount: amountUnits.toString(),
      amountCoin: depositCoin,
      deposit: amountUnits.toString(),
      depositCoin,
      withdrawal: withdrawalUnitsBch ? withdrawalUnitsBch.toString() : null,
      withdrawalCoin: Number.isFinite(withdrawalCoin) ? withdrawalCoin : null,
      intervalMinutes: 5,
    },
    contract: {
      version: '0.12.0',
      ...(selectedCoin === 'BCH'
        ? { type: 'recurring-bch-vault', contractPath: CASHSCRIPT_CONTRACT_PATH }
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

    if (selectedCoin === 'BCH') {
      const bchResult = await runChipnetBchDonationFlow({
        walletClient,
        chainId: activeChain,
        senderAddress: activeAccount,
        charityAddress: recipientAddress,
        amountSatoshis: amountUnits,
        depositCoin,
        donationId,
      })

      txReference = bchResult.txid
    } else {
      const txResult = await sendEthDonation({
        walletClient,
        chainId: activeChain,
        from: activeAccount,
        to: recipientAddress,
        wei: amountUnits,
      })
      txReference = extractTxReference(txResult)
      updateDonationRecord(donationId, {
        status: 'sent',
        txReference,
      })
    }

    window.dispatchEvent(
      new CustomEvent(WALLET_BALANCE_ADJUST_EVENT, {
        detail: {
          delta: -depositCoin,
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
          amount: depositCoin,
        },
      }),
    )

    notify({
      type: 'positive',
      message:
        selectedCoin === 'BCH'
          ? `Donation confirmed on Chipnet. Txid: ${txReference}`
          : txReference
            ? `Donation sent successfully. Tx: ${txReference}`
            : 'Donation sent successfully.',
    })

    submissionStatus.value = {
      type: 'positive',
      message:
        selectedCoin === 'BCH'
          ? `Donation confirmed (${BCH_CONFIRMATION_MIN}+ conf). Txid: ${txReference}`
          : txReference
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

    const isConfirmationTimeout = /confirmation timed out/i.test(failureMessage)
    if (selectedCoin === 'BCH' && !isConfirmationTimeout) {
      updateDonationRecord(donationId, {
        status: 'failed',
        lastError: failureMessage,
      })
    }

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

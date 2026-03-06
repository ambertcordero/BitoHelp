<template>
  <q-layout view="lHh Lpr lFf">
    <!-- HEADER ini !!!-->
    <q-header class="app-header">
      <q-toolbar class="q-px-lg">
        <!-- Logo ini !!!-->
        <div class="row items-center">
          <q-avatar size="40px">
            <img src="~assets/BitoHelp.png" />
          </q-avatar>

          <div class="app-title q-ml-sm">BitoHelp</div>
        </div>

        <q-space />

        <div class="topbar__wallet">
          <div class="topbar__actions">
            <button
              class="wallet-toggle"
              :class="{
                'wallet-toggle--connected': isConnected,
                'wallet-toggle--pending': isConnecting,
              }"
              @click="handleConnect"
            >
              <span
                class="wallet-toggle__icon"
                :class="walletIconClass"
                @mouseenter="handleIdleIconHover"
              >
                <span
                  v-if="isConnecting"
                  ref="bitcoinLoaderContainer"
                  class="wallet-toggle__lottie wallet-toggle__lottie--loader"
                  aria-hidden="true"
                ></span>

                <img
                  v-else-if="walletIconUrl"
                  :src="walletIconUrl"
                  :alt="walletName"
                  @load="iconLoading = false"
                  @error="iconLoading = false"
                />

                <QSkeleton v-if="iconLoading" type="QAvatar" size="46px" class="wallet-skeleton" />

                <span
                  v-else-if="!walletIconUrl"
                  ref="walletLottieContainer"
                  class="wallet-toggle__lottie"
                  aria-hidden="true"
                ></span>
              </span>

              <span v-if="!isConnected && !isConnecting" class="wallet-toggle__label">
                Connect Wallet
              </span>

              <span v-else-if="isConnected" class="wallet-toggle__info">
                <strong>{{ formattedBalance }}</strong>
                <small>{{ shortAddress }}</small>
              </span>
            </button>
          </div>

          <p v-if="walletError" class="wallet-error">{{ walletError }}</p>
        </div>
      </q-toolbar>
    </q-header>

    <!-- PAGE CONTENT -->
    <q-page-container>
      <router-view />
    </q-page-container>
  </q-layout>
</template>

<script setup>
import { computed, nextTick, onBeforeUnmount, onMounted, ref, watch } from 'vue'
import { Core as WalletConnectCore } from '@walletconnect/core'
import SignClient from '@walletconnect/sign-client'
import { WalletConnectModal } from '@walletconnect/modal'
import { QSkeleton } from 'quasar'
import lottie from 'lottie-web'

import logoUrl from '../assets/BitoHelp.png'
import bitcoinIcon from '../../wallets/Bitcoin.ico'
import cashonizeIcon from '../../wallets/Cashonize.ico'
import metamaskIcon from '../../wallets/MetaMask.ico'
import paytacaIcon from '../../wallets/Paytaca.ico'
import walletconnectIcon from '../../wallets/Walletconnect.ico'
import walletLottieJson from '../../lottie/WALLET.json'
import bitcoinLoaderJson from '../../lottie/Bitcoin Loader.json'
import {
  fetchAddressBalance,
  fetchMainnetBalanceForChipnetAddress,
  getBchRuntimeConfig,
  normalizeChipnetAddress,
} from '../services/bchChipnet'

const projectId = '1e52dff3b9c75d86cfc7b1190c02d3a0'
const makeWalletConnectStoragePrefix = () =>
  `bitohelp-${Date.now().toString(36)}-${Math.random().toString(36).slice(2, 8)}`
let walletConnectStoragePrefix = makeWalletConnectStoragePrefix()
const walletConnectRelayUrl = 'wss://relay.walletconnect.com'
const bchChains = ['bch:bchtest']
const evmChains = ['eip155:1', 'eip155:5', 'eip155:11155111']
const evmNativeSymbols = {
  1: 'ETH',
  10: 'ETH',
  56: 'BNB',
  137: 'MATIC',
  250: 'FTM',
  324: 'ETH',
  42161: 'ETH',
  43114: 'AVAX',
  59144: 'ETH',
  8453: 'ETH',
  5: 'ETH',
  11155111: 'ETH',
}
const evmRpcByChain = {
  'eip155:1': 'https://ethereum-rpc.publicnode.com',
  'eip155:5': 'https://ethereum-goerli-rpc.publicnode.com',
  'eip155:11155111': 'https://rpc.sepolia.org',
}

const walletAddress = ref('')
const walletBalance = ref(0)
const bchSessionAddresses = ref([]) // all BCH addresses in current session
const walletError = ref('')
const isConnected = ref(false)
const walletIconUrl = ref('')
const walletName = ref('Wallet')
const walletNamespace = ref('')
const walletChain = ref('')
const iconLoading = ref(false)
const isConnecting = ref(false)
const isBalanceLoading = ref(false)

const walletLottieContainer = ref(null)
const bitcoinLoaderContainer = ref(null)

let signClient
let wcModal
let sessionTopic
let walletLottieAnimation
let walletLottieTimeout
let bitcoinLoaderAnimation
let unsubscribeModalState
let qrDismissed = false
let balanceRequestNonce = 0
let walletConnectInitPromise

const WALLETCONNECT_SESSION_PING_TIMEOUT_MS = 10000

const WALLET_CONNECTED_STORAGE_KEY = 'bitohelp.wallet.connected'
const WALLET_NAMESPACE_STORAGE_KEY = 'bitohelp.wallet.namespace'
const WALLET_CONNECTED_EVENT = 'bitohelp:wallet-connection-changed'
const WALLET_SNAPSHOT_STORAGE_KEY = 'bitohelp.wallet.snapshot'
const WALLET_BALANCE_ADJUST_EVENT = 'bitohelp:wallet-balance-adjust'
const WALLET_BALANCE_REFRESH_EVENT = 'bitohelp:wallet-balance-refresh'
const WALLET_CLIENT_GLOBAL_KEY = '__bitohelpWalletClient__'

const syncWalletConnectionState = (connected, namespace = '') => {
  localStorage.setItem(WALLET_CONNECTED_STORAGE_KEY, connected ? '1' : '0')
  if (connected && namespace) {
    localStorage.setItem(WALLET_NAMESPACE_STORAGE_KEY, namespace)
  } else {
    localStorage.removeItem(WALLET_NAMESPACE_STORAGE_KEY)
  }
  window.dispatchEvent(
    new CustomEvent(WALLET_CONNECTED_EVENT, {
      detail: { connected, namespace },
    }),
  )
}

const syncWalletSnapshot = () => {
  const snapshot = {
    connected: isConnected.value,
    namespace: walletNamespace.value,
    chain: walletChain.value,
    address: walletAddress.value,
    balance: Number(walletBalance.value || 0),
    symbol: walletSymbol.value,
    updatedAt: Date.now(),
  }

  localStorage.setItem(WALLET_SNAPSHOT_STORAGE_KEY, JSON.stringify(snapshot))
  window.dispatchEvent(
    new CustomEvent(WALLET_CONNECTED_EVENT, {
      detail: snapshot,
    }),
  )
}

const syncWalletClientBridge = () => {
  if (
    !isConnected.value ||
    !signClient ||
    !sessionTopic ||
    !walletChain.value ||
    !walletNamespace.value ||
    !walletAddress.value
  ) {
    delete window[WALLET_CLIENT_GLOBAL_KEY]
    return
  }

  const session = getWalletConnectSession(sessionTopic)

  const activeTopic = sessionTopic
  const activeSession = session

  const waitForRequestSent = (method, timeoutMs = 5000) =>
    new Promise((resolve) => {
      if (!signClient) {
        resolve(null)
        return
      }

      let settled = false
      let timeoutId

      const cleanup = () => {
        if (timeoutId) {
          window.clearTimeout(timeoutId)
        }
        signClient.off('session_request_sent', handleSent)
      }

      const resolveOnce = (value) => {
        if (settled) {
          return
        }
        settled = true
        cleanup()
        resolve(value)
      }

      const handleSent = (event) => {
        if (event?.topic !== activeTopic || event?.request?.method !== method) {
          return
        }
        resolveOnce({
          id: event.id,
          topic: event.topic,
          chainId: event.chainId,
          request: event.request,
        })
      }

      timeoutId = window.setTimeout(() => resolveOnce(null), timeoutMs)
      signClient.on('session_request_sent', handleSent)
    })

  const getHistoryRecord = async (id) => {
    if (!signClient || id === undefined || id === null) {
      return null
    }

    try {
      return await signClient.core.history.get(activeTopic, id)
    } catch {
      return null
    }
  }

  const getPendingHistory = () => {
    try {
      const pending = signClient?.core?.history?.pending || []
      return pending.filter((entry) => entry?.topic === activeTopic)
    } catch {
      return []
    }
  }

  window[WALLET_CLIENT_GLOBAL_KEY] = {
    namespace: walletNamespace.value,
    chain: walletChain.value,
    address: walletAddress.value,
    topic: activeTopic,
    session: activeSession,
    ping: () => signClient.ping({ topic: activeTopic }),
    waitForRequestSent,
    getHistoryRecord,
    getPendingHistory,
    request: (payload) => {
      if (walletNamespace.value === 'bch') {
        getWalletConnectSession(activeTopic)
      }
      return signClient.request({ topic: activeTopic, ...payload })
    },
  }
}

const handleWalletBalanceAdjust = (event) => {
  if (!isConnected.value) {
    return
  }

  const delta = Number(event?.detail?.delta)
  if (!Number.isFinite(delta) || delta === 0) {
    return
  }

  const targetChain = event?.detail?.chain
  const targetAddress = event?.detail?.address

  if (targetChain && targetChain !== walletChain.value) {
    return
  }

  if (
    targetAddress &&
    normalizeAddressForComparison(targetAddress, targetChain || walletChain.value) !==
      normalizeAddressForComparison(walletAddress.value, walletChain.value)
  ) {
    return
  }

  walletBalance.value = Math.max(0, walletBalance.value + delta)
}

const handleWalletBalanceRefresh = (event) => {
  if (!isConnected.value || !walletAddress.value || !walletChain.value) {
    return
  }

  const targetChain = event?.detail?.chain
  const targetAddress = event?.detail?.address

  if (targetChain && targetChain !== walletChain.value) {
    return
  }

  if (
    targetAddress &&
    normalizeAddressForComparison(targetAddress, targetChain || walletChain.value) !==
      normalizeAddressForComparison(walletAddress.value, walletChain.value)
  ) {
    return
  }

  fetchBalance(walletAddress.value, walletChain.value)
}

const destroyWalletLottie = () => {
  if (walletLottieTimeout) {
    window.clearTimeout(walletLottieTimeout)
    walletLottieTimeout = undefined
  }
  if (walletLottieAnimation) {
    walletLottieAnimation.destroy()
    walletLottieAnimation = undefined
  }
}

const destroyBitcoinLoader = () => {
  if (bitcoinLoaderAnimation) {
    bitcoinLoaderAnimation.destroy()
    bitcoinLoaderAnimation = undefined
  }
}

const initWalletLottie = () => {
  if (!walletLottieContainer.value || walletLottieAnimation) {
    return
  }

  walletLottieAnimation = lottie.loadAnimation({
    container: walletLottieContainer.value,
    renderer: 'svg',
    loop: false,
    autoplay: false,
    animationData: walletLottieJson,
    rendererSettings: {
      preserveAspectRatio: 'xMidYMid slice',
    },
  })

  walletLottieAnimation.goToAndStop(0, true)
}

const initBitcoinLoader = () => {
  if (!bitcoinLoaderContainer.value || bitcoinLoaderAnimation) {
    return
  }

  bitcoinLoaderAnimation = lottie.loadAnimation({
    container: bitcoinLoaderContainer.value,
    renderer: 'svg',
    loop: true,
    autoplay: true,
    animationData: bitcoinLoaderJson,
    rendererSettings: {
      preserveAspectRatio: 'xMidYMid meet',
    },
  })
}

const handleIdleIconHover = () => {
  if (isConnected.value || walletIconUrl.value || iconLoading.value) {
    return
  }

  initWalletLottie()
  if (!walletLottieAnimation) {
    return
  }

  if (walletLottieTimeout) {
    window.clearTimeout(walletLottieTimeout)
  }

  walletLottieAnimation.goToAndStop(0, true)
  walletLottieAnimation.play()

  walletLottieTimeout = window.setTimeout(() => {
    walletLottieAnimation?.goToAndStop(0, true)
    walletLottieTimeout = undefined
  }, 1000)
}

const resetWalletState = () => {
  isConnected.value = false
  isConnecting.value = false
  walletAddress.value = ''
  walletBalance.value = 0
  bchSessionAddresses.value = []
  walletIconUrl.value = ''
  walletName.value = 'Wallet'
  walletNamespace.value = ''
  walletChain.value = ''
  isBalanceLoading.value = false
  iconLoading.value = false
  sessionTopic = undefined
  delete window[WALLET_CLIENT_GLOBAL_KEY]
  destroyBitcoinLoader()
}

const handleQrClosed = () => {
  if (!isConnecting.value || isConnected.value) {
    return
  }
  qrDismissed = true
  wcModal?.closeModal()
  resetWalletState()
}

const shortAddress = computed(() => {
  if (!walletAddress.value) {
    return ''
  }
  // For BCH addresses strip the network prefix ('bchtest:' / 'bitcoincash:')
  // so the UI shows the readable hash portion, e.g. 'qz52lg...wnsa'
  const display =
    walletNamespace.value === 'bch' && walletAddress.value.includes(':')
      ? walletAddress.value.slice(walletAddress.value.indexOf(':') + 1)
      : walletAddress.value
  const start = display.slice(0, 6)
  const end = display.slice(-4)
  return `${start}...${end}`
})

const walletSymbol = computed(() => {
  if (walletNamespace.value === 'bch') {
    if (walletChain.value === 'bch:bchtest') {
      return 'tBCH'
    }
    return 'BCH'
  }

  if (walletNamespace.value === 'eip155') {
    const chainNumber = walletChain.value.split(':')[1] || ''
    return evmNativeSymbols[chainNumber] || 'NATIVE'
  }

  return 'COIN'
})

// Truncate (never round up) a BCH value to 3 decimal places, then strip
// trailing zeros while keeping at least one decimal digit.
// Examples: 0.09999318 → "0.099",  0.10000000 → "0.1",  1.50000000 → "1.5"
const formatBchDisplay = (value) => {
  const floored = Math.floor(value * 1000) / 1000
  return floored
    .toFixed(3)
    .replace(/(\.\d*[1-9])0+$/, '$1')
    .replace(/\.0+$/, '.0')
}

const formattedBalance = computed(() => {
  if (!isConnected.value) {
    return '0.000'
  }

  if (isBalanceLoading.value) {
    return `Loading ${walletSymbol.value}...`
  }

  if (walletNamespace.value === 'bch') {
    return `${formatBchDisplay(walletBalance.value)} ${walletSymbol.value}`
  }

  return `${walletBalance.value.toFixed(4)} ${walletSymbol.value}`
})

const walletIconClass = computed(() =>
  isConnected.value ? 'wallet-toggle__icon--connected' : 'wallet-toggle__icon--idle',
)

const parseBchAccount = (account) => {
  if (!account || !account.startsWith('bch:')) {
    return ''
  }

  const parts = account.split(':')

  // bch:chipnet:bchtest:qq... → bchtest:qq...
  if (parts.length >= 4 && parts[2] === 'bchtest') {
    return `${parts[2]}:${parts.slice(3).join(':')}`.toLowerCase()
  }

  // bch:bchtest:qq... → bchtest:qq...
  if (parts.length >= 3 && parts[1] === 'bchtest') {
    return `${parts[1]}:${parts.slice(2).join(':')}`.toLowerCase()
  }

  // bch:chipnet:qq... or bch:chipnet:bchtest:qq...
  if (parts.length >= 3 && parts[1] === 'chipnet') {
    const addressPart = parts.slice(2).join(':')
    // If already has a recognised CashAddr prefix, pass it through so
    // normalizeChipnetAddress can validate the correct checksum variant.
    if (addressPart.startsWith('bchtest:')) {
      return addressPart.toLowerCase()
    }
    return `bchtest:${addressPart}`.toLowerCase()
  }

  // Fallback: last part only
  const addressPart = parts[parts.length - 1]
  if (addressPart && !addressPart.includes(':')) {
    return `bchtest:${addressPart}`.toLowerCase()
  }

  return addressPart.toLowerCase()
}

const parseBchChainFromAccount = (account) => {
  if (!account || !account.startsWith('bch:')) {
    return ''
  }

  const parts = account.split(':')
  if (parts.length < 2) {
    return ''
  }

  const network = parts[1]
  if (network === 'chipnet' || network === 'bchtest') {
    return 'bch:bchtest'
  }
  // Fallback for unrecognised BCH chains
  return 'bch:bchtest'
}

const hasSupportedNamespace = (session) => {
  const namespaces = session?.namespaces || {}
  return Boolean(namespaces?.bch?.accounts?.length || namespaces?.eip155?.accounts?.length)
}

const hasBchNamespace = (session) => Boolean(session?.namespaces?.bch?.accounts?.length)

const sanitizeWalletConnectSession = (session) => {
  if (!session || !hasBchNamespace(session)) {
    return session
  }

  const peerMetadata = session.peer?.metadata || {}
  const redirect = peerMetadata.redirect || {}
  const sessionConfig = session.sessionConfig || {}
  let mutated = false

  if (session.transportType !== 'relay') {
    session.transportType = 'relay'
    mutated = true
  }

  if (sessionConfig.disableDeepLink !== true) {
    session.sessionConfig = {
      ...sessionConfig,
      disableDeepLink: true,
    }
    mutated = true
  }

  if (redirect.linkMode || redirect.universal || redirect.native) {
    session.peer = {
      ...session.peer,
      metadata: {
        ...peerMetadata,
        redirect: {
          ...redirect,
          linkMode: false,
          universal: '',
          native: '',
        },
      },
    }
    mutated = true
  }

  if (mutated && import.meta.env.DEV) {
    console.info('[BitoHelp][walletconnect] sanitized BCH session transport', {
      topic: session.topic,
      transportType: session.transportType,
      sessionConfig: session.sessionConfig,
      peerRedirect: session.peer?.metadata?.redirect,
    })
  }

  return session
}

const getWalletConnectSession = (topic = sessionTopic) => {
  if (!signClient || !topic) {
    return null
  }

  try {
    return sanitizeWalletConnectSession(signClient.session.get(topic))
  } catch {
    return null
  }
}

const pickStoredSession = (sessions) => {
  if (!Array.isArray(sessions) || sessions.length === 0) {
    return null
  }

  const nowSeconds = Math.floor(Date.now() / 1000)
  const activeSessions = sessions.filter((session) => Number(session?.expiry || 0) > nowSeconds)
  const supportedSessions = activeSessions.filter(hasSupportedNamespace)
  const rankedSessions = (supportedSessions.length ? supportedSessions : activeSessions).slice()

  if (rankedSessions.length === 0) {
    return null
  }

  rankedSessions.sort((left, right) => {
    const leftExpiry = Number(left?.expiry || 0)
    const rightExpiry = Number(right?.expiry || 0)
    return rightExpiry - leftExpiry
  })

  return sanitizeWalletConnectSession(rankedSessions[0] || null)
}

const pingWalletConnectSession = async (
  topic,
  timeoutMs = WALLETCONNECT_SESSION_PING_TIMEOUT_MS,
) => {
  if (!signClient || !topic) {
    return false
  }

  try {
    await Promise.race([
      signClient.ping({ topic }),
      new Promise((_, reject) => {
        window.setTimeout(() => {
          reject(new Error('WalletConnect session ping timed out.'))
        }, timeoutMs)
      }),
    ])
    return true
  } catch (error) {
    if (import.meta.env.DEV) {
      console.warn('[BitoHelp][walletconnect] session ping failed', {
        topic,
        error: String(error?.message || error || ''),
      })
    }
    return false
  }
}
const getStoredPairings = () => {
  try {
    return signClient?.pairing?.getAll?.() || []
  } catch {
    return []
  }
}

const cleanupInactivePairings = async ({ deletePairings = false } = {}) => {
  if (!signClient) {
    return
  }

  const inactivePairings = getStoredPairings().filter((pairing) => !pairing?.active)
  if (inactivePairings.length === 0) {
    return
  }

  if (import.meta.env.DEV) {
    console.info('[BitoHelp][walletconnect] cleaning inactive pairings', {
      count: inactivePairings.length,
      deletePairings,
      topics: inactivePairings.map((pairing) => pairing.topic),
    })
  }

  for (const pairing of inactivePairings) {
    const topic = pairing?.topic
    if (!topic) {
      continue
    }

    try {
      if (deletePairings) {
        await signClient.core.pairing.disconnect({ topic })
      } else {
        await signClient.core.relayer.subscriber.unsubscribe(topic)
      }
    } catch (error) {
      if (import.meta.env.DEV) {
        console.warn('[BitoHelp][walletconnect] pairing cleanup failed', {
          topic,
          deletePairings,
          error: String(error),
        })
      }
    }
  }
}

const restartWalletConnectTransport = async () => {
  try {
    await signClient?.core?.relayer?.restartTransport?.()
  } catch (error) {
    if (import.meta.env.DEV) {
      console.warn('[BitoHelp][walletconnect] transport restart failed', String(error))
    }
  }
}

const clearWalletConnectStorageByPrefix = (prefix) => {
  const candidatePrefix = String(prefix || '').trim()
  if (!candidatePrefix || typeof window === 'undefined') {
    return
  }

  try {
    const keysToDelete = []
    for (let index = 0; index < localStorage.length; index += 1) {
      const key = localStorage.key(index)
      if (key && key.includes(candidatePrefix)) {
        keysToDelete.push(key)
      }
    }
    keysToDelete.forEach((key) => localStorage.removeItem(key))

    if (import.meta.env.DEV && keysToDelete.length > 0) {
      console.info('[BitoHelp][walletconnect] cleared prefixed storage keys', {
        prefix: candidatePrefix,
        count: keysToDelete.length,
      })
    }
  } catch (error) {
    if (import.meta.env.DEV) {
      console.warn('[BitoHelp][walletconnect] failed to clear prefixed storage keys', {
        prefix: candidatePrefix,
        error: String(error),
      })
    }
  }
}

const disposeWalletConnectClient = async () => {
  if (!signClient) {
    return
  }

  const previousPrefix = walletConnectStoragePrefix

  try {
    await disconnectAllWalletConnectSessions()
  } catch {
    // Disconnect best-effort; always continue with teardown.
  }

  try {
    await signClient?.core?.relayer?.transportClose?.()
  } catch {
    // transportClose is optional across WC versions
  }

  signClient = undefined
  walletConnectInitPromise = undefined

  clearWalletConnectStorageByPrefix(previousPrefix)
  walletConnectStoragePrefix = makeWalletConnectStoragePrefix()

  if (import.meta.env.DEV) {
    console.info('[BitoHelp][walletconnect] disposed client and rotated storage prefix', {
      previousPrefix,
      nextPrefix: walletConnectStoragePrefix,
    })
  }
}

const disconnectAllWalletConnectSessions = async () => {
  if (!signClient) {
    return
  }

  const sessions = signClient.session.getAll()
  for (const session of sessions) {
    const topic = session?.topic
    if (!topic) {
      continue
    }

    try {
      await signClient.disconnect({
        topic,
        reason: {
          code: 6000,
          message: 'User disconnected',
        },
      })
    } catch (error) {
      if (import.meta.env.DEV) {
        console.warn('[BitoHelp][walletconnect] session disconnect failed', {
          topic,
          error: String(error),
        })
      }
    }
  }
}

const prepareFreshWalletConnectConnection = async () => {
  if (!signClient) {
    return
  }

  await disconnectAllWalletConnectSessions()
  await cleanupInactivePairings({ deletePairings: true })
  await restartWalletConnectTransport()
}

const parseAccount = (account) => {
  if (!account) {
    return ''
  }

  if (account.startsWith('bch:')) {
    return parseBchAccount(account)
  }

  const parts = account.split(':')
  return parts[parts.length - 1] || ''
}

const normalizeAddressForComparison = (address, chainId) => {
  const raw = String(address || '').trim()
  if (!raw) {
    return ''
  }

  if ((chainId || '').startsWith('bch:')) {
    return normalizeChipnetAddress(raw) || raw.toLowerCase()
  }

  return raw.toLowerCase()
}

const nativeDecimalToWei = (value) => {
  const normalized = String(value ?? '').trim()
  if (!normalized) {
    return 0n
  }

  const [integerRaw, fractionRaw = ''] = normalized.split('.')
  const integerPart = integerRaw || '0'
  const paddedFraction = (fractionRaw + '0'.repeat(18)).slice(0, 18)

  return BigInt(integerPart) * 10n ** 18n + BigInt(paddedFraction)
}

const parseBalanceWei = (rawBalance, options = {}) => {
  const { assumeNativeForPlainDecimal = false } = options

  if (typeof rawBalance === 'bigint') {
    return rawBalance
  }

  if (typeof rawBalance === 'number') {
    if (!Number.isFinite(rawBalance) || rawBalance < 0) {
      return 0n
    }

    if (assumeNativeForPlainDecimal) {
      return nativeDecimalToWei(rawBalance.toString())
    }

    return BigInt(Math.trunc(rawBalance))
  }

  if (rawBalance && typeof rawBalance === 'object') {
    const nested = rawBalance.result ?? rawBalance.balance ?? rawBalance.value
    if (nested !== undefined) {
      return parseBalanceWei(nested, options)
    }
    return 0n
  }

  if (typeof rawBalance !== 'string') {
    return 0n
  }

  const value = rawBalance.trim()
  if (!value) {
    return 0n
  }

  if (value.startsWith('0x') || value.startsWith('0X')) {
    return BigInt(value)
  }

  if (assumeNativeForPlainDecimal) {
    if (/^\d+(\.\d+)?$/.test(value)) {
      return nativeDecimalToWei(value)
    }
  }

  return BigInt(value)
}

const weiToNative = (wei) => Number(wei) / 1e18

const logWalletBalanceDebug = (stage, details) => {
  if (!import.meta.env.DEV) {
    return
  }

  console.info('[BitoHelp][wallet-balance]', stage, details)
}

const fetchEvmBalanceFromRpc = async (chainId, address) => {
  const rpcUrl = evmRpcByChain[chainId]
  if (!rpcUrl) {
    throw new Error('Unsupported EVM chain RPC')
  }

  const response = await fetch(rpcUrl, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      id: Date.now(),
      jsonrpc: '2.0',
      method: 'eth_getBalance',
      params: [address, 'latest'],
    }),
  })

  if (!response.ok) {
    throw new Error('RPC balance request failed')
  }

  const data = await response.json()
  if (data?.error) {
    throw new Error(data.error?.message || 'RPC returned an error')
  }

  return {
    rpcUrl,
    rawWei: data?.result,
    wei: parseBalanceWei(data?.result),
  }
}

const parseChainFromAccount = (account) => {
  if (!account) {
    return ''
  }

  if (account.startsWith('bch:')) {
    return parseBchChainFromAccount(account)
  }

  const parts = account.split(':')
  if (parts.length < 2) {
    return ''
  }
  return `${parts[0]}:${parts[1]}`
}

const normalizeEvmChainId = (value) => {
  if (typeof value === 'number' && Number.isFinite(value)) {
    return `eip155:${Math.trunc(value)}`
  }

  if (typeof value !== 'string') {
    return ''
  }

  const normalized = value.trim().toLowerCase()
  if (!normalized) {
    return ''
  }

  if (normalized.startsWith('eip155:')) {
    return normalized
  }

  if (normalized.startsWith('0x')) {
    const chainNumber = Number.parseInt(normalized, 16)
    if (Number.isFinite(chainNumber)) {
      return `eip155:${chainNumber}`
    }
    return ''
  }

  if (/^\d+$/.test(normalized)) {
    return `eip155:${normalized}`
  }

  return ''
}

const selectPreferredAccount = (accounts, preferredChains) => {
  if (!Array.isArray(accounts) || !accounts.length) {
    return ''
  }

  const matched = accounts.find((account) =>
    preferredChains.includes(parseChainFromAccount(account)),
  )
  return matched || accounts[0]
}

const resolveWalletIcon = (name) => {
  const key = (name || '').toLowerCase()
  if (key.includes('react wallet v2')) return walletconnectIcon
  if (key.includes('walletconnect')) return walletconnectIcon
  if (key.includes('paytaca')) return paytacaIcon
  if (key.includes('cashonize')) return cashonizeIcon
  if (key.includes('metamask')) return metamaskIcon
  if (key.includes('bitcoin')) return bitcoinIcon
  return ''
}

const updateFromSession = (session) => {
  const sanitizedSession = sanitizeWalletConnectSession(session)
  const bchNamespace = sanitizedSession.namespaces.bch
  const evmNamespace = sanitizedSession.namespaces.eip155

  let namespaceKey = ''
  let account = ''
  let chain = ''

  if (bchNamespace?.accounts?.length) {
    const preferredBchAccount = selectPreferredAccount(bchNamespace.accounts, bchChains)
    namespaceKey = 'bch'
    account = preferredBchAccount
    chain = parseChainFromAccount(account)

    // Collect all valid BCH addresses from the session so we can sum balances
    const allNormalized = bchNamespace.accounts
      .map((a) => normalizeChipnetAddress(parseBchAccount(a)))
      .filter(Boolean)
    bchSessionAddresses.value = [...new Set(allNormalized)]

    console.info('[BitoHelp][bch-session]', {
      topic: sanitizedSession.topic,
      transportType: sanitizedSession.transportType || null,
      sessionConfig: sanitizedSession.sessionConfig || null,
      peerRedirect: sanitizedSession.peer?.metadata?.redirect || null,
      rawAccount: account,
      parsedChain: chain,
      allBchAccounts: bchNamespace.accounts,
      resolvedAddresses: bchSessionAddresses.value,
    })
  } else if (evmNamespace?.accounts?.length) {
    const preferredEvmAccount = selectPreferredAccount(evmNamespace.accounts, evmChains)
    namespaceKey = 'eip155'
    account = preferredEvmAccount
    chain = parseChainFromAccount(account)
  }

  if (!account) {
    walletError.value = 'No supported accounts found in the session.'
    return
  }

  walletNamespace.value = namespaceKey
  walletChain.value = chain
  const parsedAddress = parseAccount(account)

  if (namespaceKey === 'bch') {
    const normalized = normalizeChipnetAddress(parsedAddress)
    if (!normalized) {
      walletError.value = `Invalid BCH address format: ${parsedAddress}`
      if (import.meta.env.DEV) {
        console.error('[BitoHelp][bch-session] Invalid address', {
          rawAccount: account,
          parsedAddress,
        })
      }
      return
    }
    walletAddress.value = normalized

    if (import.meta.env.DEV) {
      console.info('[BitoHelp][bch-session] Address normalized', {
        raw: parsedAddress,
        normalized,
      })
    }
  } else {
    walletAddress.value = parsedAddress
  }

  const metadata = sanitizedSession.peer?.metadata
  walletName.value = metadata?.name || 'Wallet'
  walletIconUrl.value = resolveWalletIcon(walletName.value) || metadata?.icons?.[0] || ''

  iconLoading.value = Boolean(walletIconUrl.value)
  fetchBalance(walletAddress.value, walletChain.value)
}

const fetchBalance = async (address, chainId = walletChain.value) => {
  const requestNonce = ++balanceRequestNonce

  const finishLoading = () => {
    if (requestNonce === balanceRequestNonce) {
      isBalanceLoading.value = false
    }
  }

  const setBalanceSafely = (nextBalance) => {
    if (requestNonce !== balanceRequestNonce) {
      return
    }

    walletBalance.value = nextBalance
  }

  if (!address) {
    setBalanceSafely(0)
    finishLoading()
    return
  }

  isBalanceLoading.value = true

  try {
    if (walletNamespace.value === 'eip155') {
      const isReactWalletV2 = (walletName.value || '').toLowerCase().includes('react wallet v2')

      logWalletBalanceDebug('request:start', {
        account: address,
        chainId,
        rpc: evmRpcByChain[chainId] || null,
        walletName: walletName.value,
      })

      try {
        if (!signClient || !sessionTopic) {
          throw new Error('No active session')
        }

        const balanceResult = await signClient.request({
          topic: sessionTopic,
          chainId,
          request: {
            method: 'eth_getBalance',
            params: [address, 'latest'],
          },
        })

        logWalletBalanceDebug('walletconnect:response', {
          account: address,
          chainId,
          rawWei: balanceResult,
        })

        const walletBalanceWei = parseBalanceWei(balanceResult, {
          assumeNativeForPlainDecimal: isReactWalletV2,
        })

        try {
          const rpcBalance = await fetchEvmBalanceFromRpc(chainId, address)

          logWalletBalanceDebug('rpc:response', {
            account: address,
            chainId,
            rpc: rpcBalance.rpcUrl,
            rawWei: rpcBalance.rawWei,
          })

          const effectiveBalanceWei =
            rpcBalance.wei > walletBalanceWei ? rpcBalance.wei : walletBalanceWei
          setBalanceSafely(weiToNative(effectiveBalanceWei))
        } catch {
          setBalanceSafely(weiToNative(walletBalanceWei))
        }
      } catch {
        const rpcBalance = await fetchEvmBalanceFromRpc(chainId, address)

        logWalletBalanceDebug('rpc:response:fallback', {
          account: address,
          chainId,
          rpc: rpcBalance.rpcUrl,
          rawWei: rpcBalance.rawWei,
        })

        setBalanceSafely(weiToNative(rpcBalance.wei))
      }
    } else {
      // BCH Chipnet: sum balance across ALL addresses in the session
      const { apiBaseUrl } = getBchRuntimeConfig()

      // Use all session addresses if available, otherwise fall back to the
      // single address that was passed in.
      const primaryNorm = normalizeChipnetAddress(address)
      const addressList =
        bchSessionAddresses.value.length > 0
          ? bchSessionAddresses.value
          : primaryNorm
            ? [primaryNorm]
            : []

      if (addressList.length === 0) {
        const msg = `Cannot fetch BCH balance — unrecognised address: "${address}"`
        console.error('[BitoHelp][bch-balance]', msg)
        walletError.value = msg
        setBalanceSafely(0)
        finishLoading()
        return
      }

      console.info('[BitoHelp][bch-balance] fetching all addresses', {
        addressList,
        apiBaseUrl,
      })

      let totalBalance = 0
      for (const addr of addressList) {
        // 1. Chipnet UTXOs
        try {
          const chipnetBal = await fetchAddressBalance({
            apiBaseUrl,
            address: addr,
          })
          console.info('[BitoHelp][bch-balance] chipnet result', {
            address: addr,
            balance: chipnetBal,
          })
          totalBalance += chipnetBal
        } catch (addrErr) {
          console.warn('[BitoHelp][bch-balance] chipnet fetch failed', addr, String(addrErr))
        }
        // 2. Mainnet UTXOs (same key-pair, bitcoincash: prefix, watchtower.cash API)
        try {
          const mainnetBal = await fetchMainnetBalanceForChipnetAddress({ address: addr })
          console.info('[BitoHelp][bch-balance] mainnet result', {
            address: addr,
            balance: mainnetBal,
          })
          totalBalance += mainnetBal
        } catch (addrErr) {
          console.warn('[BitoHelp][bch-balance] mainnet fetch failed', addr, String(addrErr))
        }
      }

      console.info('[BitoHelp][bch-balance] total', { totalBalance, addresses: addressList })
      setBalanceSafely(totalBalance)
    }
  } catch (err) {
    console.error('[BitoHelp][bch-balance] error', String(err), { account: address, chainId })
    if (walletNamespace.value !== 'eip155') {
      walletError.value = `Balance fetch failed: ${err?.message || err}`
    }
  } finally {
    finishLoading()
  }
}

const initWalletConnect = async () => {
  if (signClient) {
    return
  }

  if (walletConnectInitPromise) {
    await walletConnectInitPromise
    return
  }

  walletConnectInitPromise = (async () => {
    const core = new WalletConnectCore({
      projectId,
      customStoragePrefix: walletConnectStoragePrefix,
      relayUrl: walletConnectRelayUrl,
      telemetryEnabled: false,
      logger: import.meta.env.DEV ? 'error' : undefined,
    })

    signClient = await SignClient.init({
      core,
      projectId,
      relayUrl: walletConnectRelayUrl,
      logger: import.meta.env.DEV ? 'error' : undefined,
      telemetryEnabled: false,
      metadata: {
        name: 'BiToHelp',
        description: 'Periodic donations on Bitcoin Cash.',
        url: window.location.origin,
        icons: [logoUrl],
      },
    })

    if (import.meta.env.DEV) {
      console.info('[BitoHelp][walletconnect] initialized', {
        storagePrefix: walletConnectStoragePrefix,
        relayUrl: walletConnectRelayUrl,
      })
    }

    signClient.on('session_request_sent', async (event) => {
      if (!import.meta.env.DEV || event?.request?.method !== 'bch_signTransaction') {
        return
      }

      let historyRecord = null
      try {
        historyRecord = await signClient.core.history.get(event.topic, event.id)
      } catch {
        historyRecord = null
      }

      console.info('[BitoHelp][walletconnect] session_request_sent', {
        id: event.id,
        topic: event.topic,
        chainId: event.chainId,
        method: event.request?.method,
        historyRecord,
      })
    })

    signClient.on('session_request_expire', (event) => {
      if (!import.meta.env.DEV) {
        return
      }

      console.warn('[BitoHelp][walletconnect] session_request_expire', event)
    })

    await cleanupInactivePairings()

    wcModal = new WalletConnectModal({
      projectId,
      themeMode: 'light',
    })

    if (typeof wcModal.subscribeModal === 'function') {
      unsubscribeModalState = wcModal.subscribeModal((modalState) => {
        if (!modalState?.open) {
          handleQrClosed()
        }
      })
    }

    signClient.on('session_delete', ({ topic }) => {
      if (!sessionTopic || topic === sessionTopic) {
        resetWalletState()
      }
    })

    signClient.on('session_event', ({ topic, params }) => {
      if (!sessionTopic || topic !== sessionTopic) {
        return
      }

      if (params?.event?.name === 'accountsChanged') {
        const accounts = params?.event?.data
        if (Array.isArray(accounts) && accounts.length > 0) {
          const account = accounts[0]
          const accountChain = parseChainFromAccount(account)

          if (accountChain) {
            walletChain.value = accountChain
          }

          const parsedAddress = parseAccount(account)

          if (walletNamespace.value === 'bch') {
            const normalized = normalizeChipnetAddress(parsedAddress)
            if (!normalized) {
              walletError.value = `Invalid BCH address: ${parsedAddress}`
              if (import.meta.env.DEV) {
                console.error('[BitoHelp][bch-accountsChanged] Invalid address', {
                  account,
                  parsedAddress,
                })
              }
              resetWalletState()
              return
            }
            walletAddress.value = normalized

            if (import.meta.env.DEV) {
              console.info('[BitoHelp][bch-accountsChanged]', {
                rawAccount: account,
                parsedChain: accountChain,
                normalized,
              })
            }
          } else {
            walletAddress.value = parsedAddress
          }

          fetchBalance(walletAddress.value, walletChain.value)
        } else {
          resetWalletState()
        }
        return
      }

      if (params?.event?.name === 'chainChanged') {
        const chainEventData = params?.event?.data
        const nextChain = normalizeEvmChainId(
          Array.isArray(chainEventData)
            ? chainEventData[0]
            : (chainEventData?.chainId ?? chainEventData),
        )

        if (nextChain) {
          walletChain.value = nextChain
        }

        if (walletAddress.value) {
          fetchBalance(walletAddress.value, walletChain.value)
        }
      }
    })

    signClient.on('session_update', ({ topic, params }) => {
      if (!sessionTopic || topic !== sessionTopic) {
        return
      }

      const activeSession = getWalletConnectSession(topic)

      updateFromSession({
        topic,
        namespaces: params.namespaces,
        transportType: activeSession?.transportType,
        sessionConfig: activeSession?.sessionConfig,
        peer: {
          metadata: {
            name: walletName.value,
            icons: walletIconUrl.value ? [walletIconUrl.value] : [],
            redirect: activeSession?.peer?.metadata?.redirect,
          },
        },
      })
    })

    const existingSessions = signClient.session.getAll()
    const session = pickStoredSession(existingSessions)
    if (session) {
      const isReachable = await pingWalletConnectSession(session.topic)
      if (isReachable) {
        sessionTopic = session.topic
        isConnected.value = true
        updateFromSession(session)
      } else {
        resetWalletState()
        await cleanupInactivePairings({ deletePairings: true })
        await restartWalletConnectTransport()
      }
    }
  })()

  try {
    await walletConnectInitPromise
  } finally {
    walletConnectInitPromise = undefined
  }
}

const handleConnect = async () => {
  walletError.value = ''
  qrDismissed = false

  if (isConnected.value && sessionTopic) {
    await initWalletConnect()

    if (!signClient) {
      walletError.value = 'WalletConnect client failed to initialize.'
      return
    }

    await signClient.disconnect({
      topic: sessionTopic,
      reason: {
        code: 6000,
        message: 'User disconnected',
      },
    })
    resetWalletState()
    return
  }

  try {
    isConnecting.value = true

    await disposeWalletConnectClient()
    await initWalletConnect()

    if (!signClient) {
      throw new Error('WalletConnect client failed to initialize.')
    }

    await prepareFreshWalletConnectConnection()
    let connection

    try {
      connection = await signClient.connect({
        requiredNamespaces: {
          bch: {
            methods: ['bch_signMessage', 'bch_signTransaction', 'bch_sendTransaction'],
            chains: bchChains,
            events: [],
          },
        },
      })
    } catch {
      try {
        connection = await signClient.connect({
          requiredNamespaces: {
            bch: {
              methods: ['bch_signMessage', 'bch_signTransaction', 'bch_sendTransaction'],
              chains: bchChains,
              events: [],
            },
            eip155: {
              methods: ['eth_getBalance', 'eth_sign', 'personal_sign', 'eth_sendTransaction'],
              chains: evmChains,
              events: ['accountsChanged', 'chainChanged'],
            },
          },
        })
      } catch {
        connection = await signClient.connect({
          requiredNamespaces: {
            eip155: {
              methods: ['eth_getBalance', 'eth_sign', 'personal_sign', 'eth_sendTransaction'],
              chains: evmChains,
              events: ['accountsChanged', 'chainChanged'],
            },
          },
        })
      }
    }

    const { uri, approval } = connection

    if (uri) {
      wcModal.openModal({ uri })
    }

    const session = sanitizeWalletConnectSession(await approval())
    qrDismissed = false
    wcModal.closeModal()
    sessionTopic = session.topic
    isConnecting.value = false
    isConnected.value = true
    updateFromSession(session)
  } catch (error) {
    const wasDismissed = qrDismissed
    qrDismissed = false
    isConnecting.value = false
    destroyBitcoinLoader()

    if (import.meta.env.DEV) {
      console.error('[BitoHelp][walletconnect] connect failed', {
        error: String(error?.message || error || ''),
      })
    }

    if (!wasDismissed) {
      walletError.value = 'Wallet connection failed. Please try again.'
    }

    wcModal?.closeModal()
  }
}

onMounted(() => {
  initWalletLottie()
  initWalletConnect()
  window.addEventListener(WALLET_BALANCE_ADJUST_EVENT, handleWalletBalanceAdjust)
  window.addEventListener(WALLET_BALANCE_REFRESH_EVENT, handleWalletBalanceRefresh)
})

watch(
  () => [isConnected.value, walletNamespace.value],
  async ([connected, namespace]) => {
    syncWalletConnectionState(connected, namespace)

    if (connected) {
      destroyWalletLottie()
      return
    }

    await nextTick()
    initWalletLottie()
  },
)

watch(
  () => [
    isConnected.value,
    walletNamespace.value,
    walletChain.value,
    walletAddress.value,
    walletBalance.value,
    walletSymbol.value,
  ],
  () => {
    syncWalletSnapshot()
    syncWalletClientBridge()
  },
)

watch(
  () => isConnecting.value,
  async (connecting) => {
    if (connecting) {
      destroyWalletLottie()
      await nextTick()
      initBitcoinLoader()
      return
    }

    destroyBitcoinLoader()
    if (!isConnected.value && !walletIconUrl.value) {
      await nextTick()
      initWalletLottie()
    }
  },
)

onBeforeUnmount(() => {
  window.removeEventListener(WALLET_BALANCE_ADJUST_EVENT, handleWalletBalanceAdjust)
  window.removeEventListener(WALLET_BALANCE_REFRESH_EVENT, handleWalletBalanceRefresh)
  if (typeof unsubscribeModalState === 'function') {
    unsubscribeModalState()
  }
  void disposeWalletConnectClient()
  destroyWalletLottie()
  destroyBitcoinLoader()
})
</script>

<template>
  <q-layout view="lHh Lpr lFf">
    <!-- HEADER ini !!!-->
    <q-header reveal class="app-header">
      <q-toolbar class="q-px-lg">
        <!-- Logo ini !!!-->
        <div class="row items-center">
          <q-avatar size="40px">
            <img src="~assets/BitoHelp.png" />
          </q-avatar>

          <div class="app-title q-ml-sm">BitoHelp</div>
        </div>

        <q-space />

        <div class="nav-menu gt-md">
          <q-btn flat no-caps label="Home" class="nav-item" to="/" />
          <q-btn flat no-caps label="Mission" class="nav-item" to="/donate" />
          <q-btn flat no-caps label="Charities" class="nav-item" to="/charities" />

          <q-btn flat no-caps class="nav-item">
            <div class="row items-center no-wrap">
              <span>Get Involved</span>
              <q-icon name="expand_more" size="20px" class="q-ml-xs" />
            </div>
            <q-menu anchor="bottom left" self="top left">
              <q-list style="min-width: 200px">
                <q-item clickable v-ripple to="/donate">
                  <q-item-section>Donate Now</q-item-section>
                </q-item>
                <q-item clickable v-ripple to="/donate">
                  <q-item-section>Start Fundraiser</q-item-section>
                </q-item>
                <q-item clickable v-ripple to="/donate">
                  <q-item-section>Volunteer</q-item-section>
                </q-item>
              </q-list>
            </q-menu>
          </q-btn>

          <q-btn flat no-caps class="nav-item">
            <div class="row items-center no-wrap">
              <span>About</span>
              <q-icon name="expand_more" size="20px" class="q-ml-xs" />
            </div>
            <q-menu anchor="bottom left" self="top left">
              <q-list style="min-width: 200px">
                <q-item clickable v-ripple to="/donate">
                  <q-item-section>Our Story</q-item-section>
                </q-item>
                <q-item clickable v-ripple to="/donate">
                  <q-item-section>Team</q-item-section>
                </q-item>
                <q-item clickable v-ripple to="/donate">
                  <q-item-section>Impact Report</q-item-section>
                </q-item>
              </q-list>
            </q-menu>
          </q-btn>

          <q-btn flat no-caps label="Contact" class="nav-item" to="/donate" />
        </div>

        <q-space />

        <!-- Notification Bell ini !!!-->
        <q-btn
          round
          icon="notifications"
          flat
          color="blue"
          class="q-mr-sm"
          @click="toggleNotifications"
        >
          <q-badge v-if="unreadCount > 0" floating color="red" rounded>{{ unreadCount }}</q-badge>
          <q-tooltip>Notifications</q-tooltip>

          <q-menu>
            <q-list style="min-width: 350px">
              <q-item-label header class="text-weight-bold">
                Notifications
                <q-btn
                  v-if="notifications.length > 0"
                  flat
                  dense
                  size="sm"
                  label="Clear all"
                  class="float-right"
                  @click="clearAllNotifications"
                />
              </q-item-label>

              <q-separator />

              <div v-if="notifications.length === 0" class="q-pa-md text-center text-grey-6">
                No notifications yet
              </div>

              <q-item
                v-for="notification in notifications"
                :key="notification.id"
                clickable
                v-ripple
                @click="markAsRead(notification.id)"
                :class="{ 'bg-blue-1': !notification.read }"
              >
                <q-item-section avatar>
                  <q-avatar
                    :icon="notification.isCharity ? 'volunteer_activism' : 'check_circle'"
                    :color="notification.isCharity ? 'green' : 'positive'"
                    text-color="white"
                  />
                </q-item-section>

                <q-item-section>
                  <q-item-label class="text-weight-medium">{{ notification.title }}</q-item-label>
                  <q-item-label caption lines="2">{{ notification.message }}</q-item-label>
                  <q-item-label caption class="text-grey-6">{{ notification.time }}</q-item-label>
                </q-item-section>

                <q-item-section side>
                  <q-btn
                    flat
                    dense
                    round
                    icon="close"
                    size="sm"
                    @click.stop="removeNotification(notification.id)"
                  />
                </q-item-section>
              </q-item>
            </q-list>
          </q-menu>
        </q-btn>

        <!-- Wallet Toggle Switch ini !!!-->
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

                <QSkeleton v-if="iconLoading" type="QAvatar" size="36px" class="wallet-skeleton" />

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

    <q-page-container>
      <router-view />
    </q-page-container>
  </q-layout>
</template>

<script setup>
import { computed, nextTick, onBeforeUnmount, onMounted, ref, watch } from 'vue'
import { useRouter } from 'vue-router'
import { Core as WalletConnectCore } from '@walletconnect/core'
import SignClient from '@walletconnect/sign-client'
import { WalletConnectModal } from '@walletconnect/modal'
import { QSkeleton } from 'quasar'
import lottie from 'lottie-web'
import { useDonationStore } from '../stores/donation-store'
import { useQuasar } from 'quasar'
import { fetchAddressBalance, normalizeChipnetAddress } from '../services/bchChipnet'
import { resumeAllAutoWithdraws } from '../services/vaultDonation'

import logoUrl from '../assets/BitoHelp.png'
import bitcoinIcon from '../../wallets/Bitcoin.ico'
import cashonizeIcon from '../../wallets/Cashonize.ico'
import metamaskIcon from '../../wallets/MetaMask.ico'
import paytacaIcon from '../../wallets/Paytaca.ico'
import walletconnectIcon from '../../wallets/Walletconnect.ico'
import walletLottieJson from '../../lottie/WALLET.json'
import bitcoinLoaderJson from '../../lottie/Bitcoin Loader.json'

const $q = useQuasar()
const router = useRouter()
const donationStore = useDonationStore()

// ── WalletConnect constants ──
const projectId = '1e52dff3b9c75d86cfc7b1190c02d3a0'
const makeWalletConnectStoragePrefix = () => {
  const uid = typeof crypto !== 'undefined' && crypto.randomUUID
    ? crypto.randomUUID()
    : `${Date.now().toString(36)}-${Math.random().toString(36).slice(2, 10)}`
  return `bitohelp-${uid}`
}
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

// ── Wallet reactive state ──
const walletAddress = ref('')
const walletBalance = ref(0)
const bchSessionAddresses = ref([])
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
let balanceRetryTimer
let balanceRetryDelay = 0
let walletConnectInitPromise

const WALLETCONNECT_SESSION_PING_TIMEOUT_MS = 10000

const WALLET_CONNECTED_STORAGE_KEY = 'bitohelp.wallet.connected'
const WALLET_NAMESPACE_STORAGE_KEY = 'bitohelp.wallet.namespace'
const WALLET_CONNECTED_EVENT = 'bitohelp:wallet-connection-changed'
const WALLET_SNAPSHOT_STORAGE_KEY = 'bitohelp.wallet.snapshot'
const WALLET_BALANCE_ADJUST_EVENT = 'bitohelp:wallet-balance-adjust'
const WALLET_BALANCE_REFRESH_EVENT = 'bitohelp:wallet-balance-refresh'
const WALLET_CLIENT_GLOBAL_KEY = '__bitohelpWalletClient__'

// ── Sync helpers ──
const syncWalletConnectionState = (connected, namespace = '') => {
  localStorage.setItem(WALLET_CONNECTED_STORAGE_KEY, connected ? '1' : '0')
  if (connected && namespace) {
    localStorage.setItem(WALLET_NAMESPACE_STORAGE_KEY, namespace)
  } else {
    localStorage.removeItem(WALLET_NAMESPACE_STORAGE_KEY)
  }
  window.dispatchEvent(
    new CustomEvent(WALLET_CONNECTED_EVENT, { detail: { connected, namespace } }),
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
  window.dispatchEvent(new CustomEvent(WALLET_CONNECTED_EVENT, { detail: snapshot }))
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

  const waitForRequestSent = (method, timeoutMs = 5000) =>
    new Promise((resolve) => {
      if (!signClient) {
        resolve(null)
        return
      }
      let settled = false
      let timeoutId
      const cleanup = () => {
        if (timeoutId) window.clearTimeout(timeoutId)
        signClient.off('session_request_sent', handleSent)
      }
      const resolveOnce = (value) => {
        if (settled) return
        settled = true
        cleanup()
        resolve(value)
      }
      const handleSent = (event) => {
        if (event?.topic !== activeTopic || event?.request?.method !== method) return
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
    if (!signClient || id === undefined || id === null) return null
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
    session,
    ping: () => signClient.ping({ topic: activeTopic }),
    waitForRequestSent,
    getHistoryRecord,
    getPendingHistory,
    request: (payload) => {
      if (walletNamespace.value === 'bch') getWalletConnectSession(activeTopic)
      return signClient.request({ topic: activeTopic, ...payload })
    },
  }
}

// ── Balance event handlers ──
const handleWalletBalanceAdjust = (event) => {
  if (!isConnected.value) return
  const delta = Number(event?.detail?.delta)
  if (!Number.isFinite(delta) || delta === 0) return
  const targetChain = event?.detail?.chain
  const targetAddress = event?.detail?.address
  if (targetChain && targetChain !== walletChain.value) return
  if (
    targetAddress &&
    normalizeAddressForComparison(targetAddress, targetChain || walletChain.value) !==
      normalizeAddressForComparison(walletAddress.value, walletChain.value)
  )
    return
  walletBalance.value = Math.max(0, walletBalance.value + delta)
}

const handleWalletBalanceRefresh = (event) => {
  if (!isConnected.value || !walletAddress.value || !walletChain.value) return
  const targetChain = event?.detail?.chain
  const targetAddress = event?.detail?.address
  if (targetChain && targetChain !== walletChain.value) return
  if (
    targetAddress &&
    normalizeAddressForComparison(targetAddress, targetChain || walletChain.value) !==
      normalizeAddressForComparison(walletAddress.value, walletChain.value)
  )
    return
  fetchBalance(walletAddress.value, walletChain.value)
}

// ── Lottie animations ──
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
  if (!walletLottieContainer.value || walletLottieAnimation) return
  walletLottieAnimation = lottie.loadAnimation({
    container: walletLottieContainer.value,
    renderer: 'svg',
    loop: false,
    autoplay: false,
    animationData: walletLottieJson,
    rendererSettings: { preserveAspectRatio: 'xMidYMid slice' },
  })
  walletLottieAnimation.goToAndStop(0, true)
}
const initBitcoinLoader = () => {
  if (!bitcoinLoaderContainer.value || bitcoinLoaderAnimation) return
  bitcoinLoaderAnimation = lottie.loadAnimation({
    container: bitcoinLoaderContainer.value,
    renderer: 'svg',
    loop: true,
    autoplay: true,
    animationData: bitcoinLoaderJson,
    rendererSettings: { preserveAspectRatio: 'xMidYMid meet' },
  })
}
const handleIdleIconHover = () => {
  if (isConnected.value || walletIconUrl.value || iconLoading.value) return
  initWalletLottie()
  if (!walletLottieAnimation) return
  if (walletLottieTimeout) window.clearTimeout(walletLottieTimeout)
  walletLottieAnimation.goToAndStop(0, true)
  walletLottieAnimation.play()
  walletLottieTimeout = window.setTimeout(() => {
    walletLottieAnimation?.goToAndStop(0, true)
    walletLottieTimeout = undefined
  }, 1000)
}

// ── Balance retry ──
const clearBalanceRetry = () => {
  if (balanceRetryTimer) {
    window.clearTimeout(balanceRetryTimer)
    balanceRetryTimer = undefined
  }
  balanceRetryDelay = 0
}
const scheduleBalanceRetry = () => {
  clearBalanceRetry()
  if (!isConnected.value || !walletAddress.value) return
  balanceRetryDelay = Math.min((balanceRetryDelay || 15000) * 2, 60000)
  if (balanceRetryDelay === 0) balanceRetryDelay = 15000
  balanceRetryTimer = window.setTimeout(() => {
    balanceRetryTimer = undefined
    if (isConnected.value && walletAddress.value)
      fetchBalance(walletAddress.value, walletChain.value)
  }, balanceRetryDelay)
}

// ── Reset state ──
const resetWalletState = () => {
  clearBalanceRetry()
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
  if (!isConnecting.value || isConnected.value) return
  qrDismissed = true
  wcModal?.closeModal()
  resetWalletState()
}

// ── Computed properties ──
const shortAddress = computed(() => {
  if (!walletAddress.value) return ''
  const display =
    walletNamespace.value === 'bch' && walletAddress.value.includes(':')
      ? walletAddress.value.slice(walletAddress.value.indexOf(':') + 1)
      : walletAddress.value
  return `${display.slice(0, 6)}...${display.slice(-4)}`
})

const walletSymbol = computed(() => {
  if (walletNamespace.value === 'bch') return walletChain.value === 'bch:bchtest' ? 'tBCH' : 'BCH'
  if (walletNamespace.value === 'eip155') {
    const chainNumber = walletChain.value.split(':')[1] || ''
    return evmNativeSymbols[chainNumber] || 'NATIVE'
  }
  return 'COIN'
})

const formatBchDisplay = (value) => {
  const floored = Math.floor(value * 1000) / 1000
  return floored
    .toFixed(3)
    .replace(/(\.\d*[1-9])0+$/, '$1')
    .replace(/\.0+$/, '.0')
}

const formattedBalance = computed(() => {
  if (!isConnected.value) return '0.000'
  if (isBalanceLoading.value) return `Loading ${walletSymbol.value}...`
  if (walletNamespace.value === 'bch')
    return `${formatBchDisplay(walletBalance.value)} ${walletSymbol.value}`
  return `${walletBalance.value.toFixed(4)} ${walletSymbol.value}`
})

const walletIconClass = computed(() =>
  isConnected.value ? 'wallet-toggle__icon--connected' : 'wallet-toggle__icon--idle',
)

// ── BCH address parsing ──
const parseBchAccount = (account) => {
  if (!account || !account.startsWith('bch:')) return ''
  const parts = account.split(':')
  if (parts.length >= 4 && parts[2] === 'bchtest')
    return `${parts[2]}:${parts.slice(3).join(':')}`.toLowerCase()
  if (parts.length >= 3 && parts[1] === 'bchtest')
    return `${parts[1]}:${parts.slice(2).join(':')}`.toLowerCase()
  if (parts.length >= 3 && parts[1] === 'chipnet') {
    const addressPart = parts.slice(2).join(':')
    if (addressPart.startsWith('bchtest:')) return addressPart.toLowerCase()
    return `bchtest:${addressPart}`.toLowerCase()
  }
  const addressPart = parts[parts.length - 1]
  if (addressPart && !addressPart.includes(':')) return `bchtest:${addressPart}`.toLowerCase()
  return addressPart.toLowerCase()
}

const parseBchChainFromAccount = (account) => {
  if (!account || !account.startsWith('bch:')) return ''
  const parts = account.split(':')
  if (parts.length < 2) return ''
  return 'bch:bchtest'
}

const hasSupportedNamespace = (session) => {
  const namespaces = session?.namespaces || {}
  return Boolean(namespaces?.bch?.accounts?.length || namespaces?.eip155?.accounts?.length)
}
const hasBchNamespace = (session) => Boolean(session?.namespaces?.bch?.accounts?.length)

const sanitizeWalletConnectSession = (session) => {
  if (!session || !hasBchNamespace(session)) return session
  const peerMetadata = session.peer?.metadata || {}
  const redirect = peerMetadata.redirect || {}
  const sessionConfig = session.sessionConfig || {}
  if (session.transportType !== 'relay') {
    session.transportType = 'relay'
  }
  if (sessionConfig.disableDeepLink !== true) {
    session.sessionConfig = { ...sessionConfig, disableDeepLink: true }
  }
  if (redirect.linkMode || redirect.universal || redirect.native) {
    session.peer = {
      ...session.peer,
      metadata: {
        ...peerMetadata,
        redirect: { ...redirect, linkMode: false, universal: '', native: '' },
      },
    }
  }
  return session
}

const getWalletConnectSession = (topic = sessionTopic) => {
  if (!signClient || !topic) return null
  try {
    return sanitizeWalletConnectSession(signClient.session.get(topic))
  } catch {
    return null
  }
}

const pickStoredSession = (sessions) => {
  if (!Array.isArray(sessions) || sessions.length === 0) return null
  const nowSeconds = Math.floor(Date.now() / 1000)
  const activeSessions = sessions.filter((s) => Number(s?.expiry || 0) > nowSeconds)
  const supportedSessions = activeSessions.filter(hasSupportedNamespace)
  const rankedSessions = (supportedSessions.length ? supportedSessions : activeSessions).slice()
  if (rankedSessions.length === 0) return null
  rankedSessions.sort((l, r) => Number(r?.expiry || 0) - Number(l?.expiry || 0))
  return sanitizeWalletConnectSession(rankedSessions[0] || null)
}

const pingWalletConnectSession = async (
  topic,
  timeoutMs = WALLETCONNECT_SESSION_PING_TIMEOUT_MS,
) => {
  if (!signClient || !topic) return false
  try {
    await Promise.race([
      signClient.ping({ topic }),
      new Promise((_, reject) =>
        window.setTimeout(() => reject(new Error('ping timed out')), timeoutMs),
      ),
    ])
    return true
  } catch {
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
  if (!signClient) return
  const inactivePairings = getStoredPairings().filter((p) => !p?.active)
  if (inactivePairings.length === 0) return
  for (const pairing of inactivePairings) {
    const topic = pairing?.topic
    if (!topic) continue
    try {
      if (deletePairings) await signClient.core.pairing.disconnect({ topic })
      else await signClient.core.relayer.subscriber.unsubscribe(topic)
    } catch {
      /* best effort */
    }
  }
}

const restartWalletConnectTransport = async () => {
  try {
    await signClient?.core?.relayer?.restartTransport?.()
  } catch {
    /* best effort */
  }
}

const purgeAllWalletConnectStorage = () => {
  if (typeof window === 'undefined') return
  try {
    const keysToDelete = []
    for (let i = 0; i < localStorage.length; i++) {
      const key = localStorage.key(i)
      if (key && (key.includes('wc@2') || key.startsWith('bitohelp-'))) {
        keysToDelete.push(key)
      }
    }
    keysToDelete.forEach((key) => localStorage.removeItem(key))
  } catch {
    /* best effort */
  }
}

const disposeWalletConnectClient = async () => {
  const previousPrefix = walletConnectStoragePrefix
  if (signClient) {
    try {
      await disconnectAllWalletConnectSessions()
    } catch {
      /* best effort */
    }
    try {
      await signClient?.core?.relayer?.transportClose?.()
    } catch {
      /* optional */
    }
  }
  signClient = undefined
  walletConnectInitPromise = undefined
  purgeAllWalletConnectStorage()
  walletConnectStoragePrefix = makeWalletConnectStoragePrefix()
}

const disconnectAllWalletConnectSessions = async () => {
  if (!signClient) return
  const sessions = signClient.session.getAll()
  for (const session of sessions) {
    const topic = session?.topic
    if (!topic) continue
    try {
      await signClient.disconnect({ topic, reason: { code: 6000, message: 'User disconnected' } })
    } catch {
      /* best effort */
    }
  }
}

const waitForRelayConnected = async (timeoutMs = 5000) => {
  if (!signClient?.core?.relayer) return
  const relayer = signClient.core.relayer
  if (relayer.connected) return
  await new Promise((resolve) => {
    const timer = setTimeout(resolve, timeoutMs)
    const check = () => {
      if (relayer.connected) { clearTimeout(timer); resolve() }
    }
    relayer.on?.('relayer_connect', () => { clearTimeout(timer); resolve() })
    // Poll as fallback in case the event doesn't fire
    const poll = setInterval(() => {
      if (relayer.connected) { clearInterval(poll); clearTimeout(timer); resolve() }
    }, 200)
    setTimeout(() => clearInterval(poll), timeoutMs)
    check()
  })
}

const prepareFreshWalletConnectConnection = async () => {
  if (!signClient) return
  await disconnectAllWalletConnectSessions()
  await cleanupInactivePairings({ deletePairings: true })
  await restartWalletConnectTransport()
  await waitForRelayConnected()
}

const parseAccount = (account) => {
  if (!account) return ''
  if (account.startsWith('bch:')) return parseBchAccount(account)
  const parts = account.split(':')
  return parts[parts.length - 1] || ''
}

function normalizeAddressForComparison(address, chainId) {
  const raw = String(address || '').trim()
  if (!raw) return ''
  if ((chainId || '').startsWith('bch:')) return normalizeChipnetAddress(raw) || raw.toLowerCase()
  return raw.toLowerCase()
}

const nativeDecimalToWei = (value) => {
  const normalized = String(value ?? '').trim()
  if (!normalized) return 0n
  const [integerRaw, fractionRaw = ''] = normalized.split('.')
  const integerPart = integerRaw || '0'
  const paddedFraction = (fractionRaw + '0'.repeat(18)).slice(0, 18)
  return BigInt(integerPart) * 10n ** 18n + BigInt(paddedFraction)
}

const parseBalanceWei = (rawBalance, options = {}) => {
  const { assumeNativeForPlainDecimal = false } = options
  if (typeof rawBalance === 'bigint') return rawBalance
  if (typeof rawBalance === 'number') {
    if (!Number.isFinite(rawBalance) || rawBalance < 0) return 0n
    if (assumeNativeForPlainDecimal) return nativeDecimalToWei(rawBalance.toString())
    return BigInt(Math.trunc(rawBalance))
  }
  if (rawBalance && typeof rawBalance === 'object') {
    const nested = rawBalance.result ?? rawBalance.balance ?? rawBalance.value
    if (nested !== undefined) return parseBalanceWei(nested, options)
    return 0n
  }
  if (typeof rawBalance !== 'string') return 0n
  const value = rawBalance.trim()
  if (!value) return 0n
  if (value.startsWith('0x') || value.startsWith('0X')) return BigInt(value)
  if (assumeNativeForPlainDecimal && /^\d+(\.\d+)?$/.test(value)) return nativeDecimalToWei(value)
  return BigInt(value)
}

const weiToNative = (wei) => Number(wei) / 1e18

const fetchEvmBalanceFromRpc = async (chainId, address) => {
  const rpcUrl = evmRpcByChain[chainId]
  if (!rpcUrl) throw new Error('Unsupported EVM chain RPC')
  const response = await fetch(rpcUrl, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      id: Date.now(),
      jsonrpc: '2.0',
      method: 'eth_getBalance',
      params: [address, 'latest'],
    }),
  })
  if (!response.ok) throw new Error('RPC balance request failed')
  const data = await response.json()
  if (data?.error) throw new Error(data.error?.message || 'RPC returned an error')
  return { rpcUrl, rawWei: data?.result, wei: parseBalanceWei(data?.result) }
}

const parseChainFromAccount = (account) => {
  if (!account) return ''
  if (account.startsWith('bch:')) return parseBchChainFromAccount(account)
  const parts = account.split(':')
  if (parts.length < 2) return ''
  return `${parts[0]}:${parts[1]}`
}

const normalizeEvmChainId = (value) => {
  if (typeof value === 'number' && Number.isFinite(value)) return `eip155:${Math.trunc(value)}`
  if (typeof value !== 'string') return ''
  const normalized = value.trim().toLowerCase()
  if (!normalized) return ''
  if (normalized.startsWith('eip155:')) return normalized
  if (normalized.startsWith('0x')) {
    const chainNumber = Number.parseInt(normalized, 16)
    if (Number.isFinite(chainNumber)) return `eip155:${chainNumber}`
    return ''
  }
  if (/^\d+$/.test(normalized)) return `eip155:${normalized}`
  return ''
}

const selectPreferredAccount = (accounts, preferredChains) => {
  if (!Array.isArray(accounts) || !accounts.length) return ''
  const matched = accounts.find((a) => preferredChains.includes(parseChainFromAccount(a)))
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

// ── Session → state ──
const updateFromSession = (session) => {
  const sanitized = sanitizeWalletConnectSession(session)
  const bchNs = sanitized.namespaces.bch
  const evmNs = sanitized.namespaces.eip155
  let namespaceKey = ''
  let account = ''
  let chain = ''

  if (bchNs?.accounts?.length) {
    namespaceKey = 'bch'
    account = selectPreferredAccount(bchNs.accounts, bchChains)
    chain = parseChainFromAccount(account)
    const allNormalized = bchNs.accounts
      .map((a) => normalizeChipnetAddress(parseBchAccount(a)))
      .filter(Boolean)
    bchSessionAddresses.value = [...new Set(allNormalized)]
    if (import.meta.env.DEV) {
      console.info('[BitoHelp][bch-session]', {
        topic: sanitized.topic,
        transportType: sanitized.transportType || null,
        sessionConfig: sanitized.sessionConfig || null,
        peerRedirect: sanitized.peer?.metadata?.redirect || null,
        rawAccount: account,
        parsedChain: chain,
        allBchAccounts: bchNs.accounts,
        resolvedAddresses: bchSessionAddresses.value,
      })
    }
  } else if (evmNs?.accounts?.length) {
    namespaceKey = 'eip155'
    account = selectPreferredAccount(evmNs.accounts, evmChains)
    chain = parseChainFromAccount(account)
    if (import.meta.env.DEV) {
      console.info('[BitoHelp][evm-session]', {
        rawAccount: account,
        parsedChain: chain,
        allEvmAccounts: evmNs.accounts,
      })
    }
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
      if (import.meta.env.DEV)
        console.error('[BitoHelp][bch-session] Invalid address', {
          rawAccount: account,
          parsedAddress,
        })
      walletError.value = `Invalid BCH address format: ${parsedAddress}`
      return
    }
    if (import.meta.env.DEV)
      console.info('[BitoHelp][bch-session] Address normalized', { raw: parsedAddress, normalized })
    walletAddress.value = normalized
  } else {
    walletAddress.value = parsedAddress
  }

  const metadata = sanitized.peer?.metadata
  walletName.value = metadata?.name || 'Wallet'
  walletIconUrl.value = resolveWalletIcon(walletName.value) || metadata?.icons?.[0] || ''
  iconLoading.value = Boolean(walletIconUrl.value)
  fetchBalance(walletAddress.value, walletChain.value)
}

// ── Fetch balance ──
const logWalletBalanceDebug = (stage, details) => {
  if (!import.meta.env.DEV) return
  console.info('[BitoHelp][wallet-balance]', stage, details)
}

const fetchBalance = async (address, chainId = walletChain.value) => {
  const requestNonce = ++balanceRequestNonce
  const finishLoading = () => {
    if (requestNonce === balanceRequestNonce) isBalanceLoading.value = false
  }
  const setBalanceSafely = (next) => {
    if (requestNonce === balanceRequestNonce) walletBalance.value = next
  }
  if (!address) {
    setBalanceSafely(0)
    finishLoading()
    return
  }
  isBalanceLoading.value = true
  logWalletBalanceDebug('request:start', {
    account: address,
    chainId,
    rpc: evmRpcByChain[chainId] || null,
    walletName: walletName.value,
  })
  try {
    if (walletNamespace.value === 'eip155') {
      const isReactWalletV2 = (walletName.value || '').toLowerCase().includes('react wallet v2')
      try {
        if (!signClient || !sessionTopic) throw new Error('No active session')
        const balanceResult = await signClient.request({
          topic: sessionTopic,
          chainId,
          request: { method: 'eth_getBalance', params: [address, 'latest'] },
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
          setBalanceSafely(
            weiToNative(rpcBalance.wei > walletBalanceWei ? rpcBalance.wei : walletBalanceWei),
          )
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
      const primaryNorm = normalizeChipnetAddress(address)
      const addressList =
        bchSessionAddresses.value.length > 0
          ? bchSessionAddresses.value
          : primaryNorm
            ? [primaryNorm]
            : []
      if (addressList.length === 0) {
        walletError.value = `Cannot fetch BCH balance — unrecognised address: "${address}"`
        setBalanceSafely(0)
        finishLoading()
        return
      }
      console.info('[BitoHelp][bch-balance] fetching all addresses', { addressList })
      let totalBalance = 0
      let firstBalanceError = ''
      for (const addr of addressList) {
        try {
          const chipnetBal = await fetchAddressBalance({ address: addr })
          console.info('[BitoHelp][bch-balance] chipnet result', {
            address: addr,
            balance: chipnetBal,
          })
          totalBalance += chipnetBal
        } catch (e) {
          if (!firstBalanceError) firstBalanceError = String(e?.message || e || '')
        }
      }
      console.info('[BitoHelp][bch-balance] total', { totalBalance, addresses: addressList })
      if (totalBalance === 0 && firstBalanceError) {
        walletError.value = /provider unavailable/i.test(firstBalanceError)
          ? 'BCH balance service temporarily unavailable — retrying...'
          : firstBalanceError
        scheduleBalanceRetry()
      } else {
        walletError.value = ''
        clearBalanceRetry()
      }
      setBalanceSafely(totalBalance)
    }
  } catch (err) {
    logWalletBalanceDebug('error', {
      account: address,
      chainId,
      error: String(err?.message || err),
    })
    if (walletNamespace.value !== 'eip155') {
      walletError.value = /provider unavailable/i.test(String(err?.message || ''))
        ? 'BCH balance service temporarily unavailable — retrying...'
        : `Balance fetch failed: ${err?.message || err}`
      scheduleBalanceRetry()
    }
  } finally {
    finishLoading()
  }
}

// ── Init WalletConnect ──
const initWalletConnect = async () => {
  if (signClient) return
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
    })

    signClient = await SignClient.init({
      core,
      projectId,
      relayUrl: walletConnectRelayUrl,
      telemetryEnabled: false,
      metadata: {
        name: 'BiToHelp',
        description: 'Periodic donations on Bitcoin Cash.',
        url: window.location.origin,
        icons: [logoUrl],
      },
    })

    await cleanupInactivePairings()

    wcModal = new WalletConnectModal({ projectId, themeMode: 'light' })

    if (typeof wcModal.subscribeModal === 'function') {
      unsubscribeModalState = wcModal.subscribeModal((modalState) => {
        if (!modalState?.open) handleQrClosed()
      })
    }

    signClient.on('session_delete', ({ topic }) => {
      if (!sessionTopic || topic === sessionTopic) resetWalletState()
    })

    signClient.on('session_event', ({ topic, params }) => {
      if (!sessionTopic || topic !== sessionTopic) return
      if (params?.event?.name === 'accountsChanged') {
        const accounts = params?.event?.data
        if (Array.isArray(accounts) && accounts.length > 0) {
          const account = accounts[0]
          const accountChain = parseChainFromAccount(account)
          if (accountChain) walletChain.value = accountChain
          const parsedAddress = parseAccount(account)
          if (walletNamespace.value === 'bch') {
            const normalized = normalizeChipnetAddress(parsedAddress)
            if (!normalized) {
              walletError.value = `Invalid BCH address: ${parsedAddress}`
              resetWalletState()
              return
            }
            walletAddress.value = normalized
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
        const data = params?.event?.data
        const nextChain = normalizeEvmChainId(
          Array.isArray(data) ? data[0] : (data?.chainId ?? data),
        )
        if (nextChain) walletChain.value = nextChain
        if (walletAddress.value) fetchBalance(walletAddress.value, walletChain.value)
      }
    })

    signClient.on('session_update', ({ topic, params }) => {
      if (!sessionTopic || topic !== sessionTopic) return
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

// ── Connect / disconnect toggle ──
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
      reason: { code: 6000, message: 'User disconnected' },
    })
    resetWalletState()
    return
  }

  try {
    isConnecting.value = true
    await disposeWalletConnectClient()
    await initWalletConnect()
    if (!signClient) throw new Error('WalletConnect client failed to initialize.')
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
    if (uri) wcModal.openModal({ uri })
    const session = sanitizeWalletConnectSession(await approval())
    qrDismissed = false
    wcModal.closeModal()
    sessionTopic = session.topic
    isConnecting.value = false
    isConnected.value = true
    updateFromSession(session)
  } catch {
    const wasDismissed = qrDismissed
    qrDismissed = false
    isConnecting.value = false
    destroyBitcoinLoader()
    if (!wasDismissed) walletError.value = 'Wallet connection failed. Please try again.'
    wcModal?.closeModal()
  }
}

// ── Notification system ──
const CHARITY_WALLET = 'bitcoincash:qp3wjpa3tjlj042z2wv7hahsldgwhwy0rq9sywjpyy'
const notifications = ref([])
const unreadCount = computed(() => notifications.value.filter((n) => !n.read).length)
const lastCheckedId = ref(null)

watch(
  () => donationStore.latestDonation,
  (newDonation, oldDonation) => {
    if (newDonation && newDonation !== oldDonation) {
      if (newDonation.recipient === CHARITY_WALLET) {
        addCharityNotification({
          title: 'New Donation Received!',
          message: `Received ${newDonation.amount} BCH for ${newDonation.cause}`,
          txid: newDonation.txid,
          amount: newDonation.amount,
          cause: newDonation.cause,
          isCharity: true,
        })
      } else {
        addNotification({
          title: 'Donation Successful!',
          message: `Your donation of ${newDonation.amount} BCH to ${newDonation.cause} was sent successfully.`,
          txid: newDonation.txid,
          isCharity: false,
        })
      }
    }
  },
)

let pollInterval = null

async function checkForNewDonations() {
  try {
    await donationStore.fetchDonations(10)
    const donations = donationStore.donationHistory
    const charityDonations = donations.filter((d) => d.recipient === CHARITY_WALLET)
    if (charityDonations.length > 0) {
      const latestDonation = charityDonations[0]
      if (lastCheckedId.value !== latestDonation.id) {
        lastCheckedId.value = latestDonation.id
        addCharityNotification({
          title: 'New Donation Received!',
          message: `Received ${latestDonation.amount} BCH for ${latestDonation.cause}`,
          txid: latestDonation.txid,
          amount: latestDonation.amount,
          cause: latestDonation.cause,
          donorName: latestDonation.donor_name || 'Anonymous',
          isCharity: true,
        })
      }
    }
  } catch (error) {
    console.error('Error checking for new donations:', error)
  }
}

function addNotification(data) {
  notifications.value.unshift({
    id: Date.now(),
    title: data.title,
    message: data.message,
    time: new Date().toLocaleTimeString(),
    read: false,
    txid: data.txid,
    isCharity: data.isCharity || false,
  })
  if (notifications.value.length > 20) notifications.value = notifications.value.slice(0, 20)
}

function addCharityNotification(data) {
  notifications.value.unshift({
    id: Date.now(),
    title: data.title,
    message: data.message,
    time: new Date().toLocaleTimeString(),
    read: false,
    txid: data.txid,
    amount: data.amount,
    cause: data.cause,
    donorName: data.donorName,
    isCharity: true,
  })
  if (notifications.value.length > 20) notifications.value = notifications.value.slice(0, 20)
  $q.notify({
    type: 'positive',
    message: 'New Donation Received!',
    caption: `${data.amount} BCH for ${data.cause}`,
    position: 'top-right',
    timeout: 5000,
    actions: [
      {
        label: 'View',
        color: 'white',
        handler: () => {
          router.push('/dashboard')
        },
      },
    ],
  })
}

function toggleNotifications() {
  notifications.value.forEach((n) => (n.read = true))
}
function markAsRead(id) {
  const n = notifications.value.find((n) => n.id === id)
  if (n) {
    n.read = true
    if (n.isCharity) router.push('/dashboard')
  }
}
function removeNotification(id) {
  const i = notifications.value.findIndex((n) => n.id === id)
  if (i > -1) notifications.value.splice(i, 1)
}
function clearAllNotifications() {
  notifications.value = []
}

// ── Lifecycle ──
onMounted(() => {
  initWalletLottie()
  initWalletConnect()
  window.addEventListener(WALLET_BALANCE_ADJUST_EVENT, handleWalletBalanceAdjust)
  window.addEventListener(WALLET_BALANCE_REFRESH_EVENT, handleWalletBalanceRefresh)
  pollInterval = setInterval(checkForNewDonations, 30000)
  checkForNewDonations()
  // Resume auto-withdraw timers for all active vaults from previous sessions
  resumeAllAutoWithdraws((cycle) => {
    if (import.meta.env.DEV) {
      console.info('[BitoHelp][vault-autowithdraw:cycle]', cycle)
    }
  })
})

watch(
  () => [isConnected.value, walletNamespace.value],
  async ([connected]) => {
    syncWalletConnectionState(connected, walletNamespace.value)
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
  if (typeof unsubscribeModalState === 'function') unsubscribeModalState()
  clearBalanceRetry()
  void disposeWalletConnectClient()
  destroyWalletLottie()
  destroyBitcoinLoader()
  if (pollInterval) clearInterval(pollInterval)
})
</script>

<style scoped>
.nav-menu {
  display: flex;
  align-items: center;
  gap: 8px;
}

.nav-item {
  font-size: 15px;
  font-weight: 500;
  color: #333;
  padding: 8px 16px;
  transition: color 0.2s ease;
}

.nav-item:hover {
  color: #1976d2;
}

.app-title {
  font-size: 20px;
  font-weight: 700;
  color: #333;
}

.app-header {
  background: rgba(255, 255, 255, 0.265);
  backdrop-filter: blur(10px);
  color: #333;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

/* Wallet Toggle Switch */
.topbar__wallet {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  gap: 0.25rem;
}

.topbar__actions {
  display: flex;
  align-items: center;
  gap: 0.8rem;
}

.wallet-toggle {
  position: relative;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 0.3rem 0.7rem 0.3rem 3.2rem;
  border-radius: 999px;
  border: none;
  background: #2e58d8;
  color: #ffffff;
  font-weight: 700;
  font-size: 0.95rem;
  cursor: pointer;
  width: 200px;
  min-height: 48px;
  text-align: center;
  transition: background-color 0.24s ease;
}

.wallet-toggle__icon {
  position: absolute;
  left: 4px;
  top: 50%;
  transform: translateY(-50%);
  width: 40px;
  height: 40px;
  border-radius: 50%;
  display: grid;
  place-items: center;
  background: #1eb5ce;
  font-size: 1rem;
  font-weight: 700;
  color: #ffffff;
  flex: 0 0 auto;
  z-index: 2;
  overflow: hidden;
  transition:
    left 0.24s cubic-bezier(0.4, 0, 0.2, 1),
    background-color 0.24s ease;
}

.wallet-toggle__icon--connected {
  background: #1c9b7e;
}

.wallet-toggle__icon img {
  width: 70%;
  height: 70%;
  object-fit: contain;
}

.wallet-toggle__lottie {
  width: 100%;
  height: 50%;
  display: block;
  transform: translateY(3px) translateX(1px) scale(4);
  transform-origin: center;
}

.wallet-toggle__lottie svg {
  width: 100% !important;
  height: 100% !important;
  display: block;
}

.wallet-toggle__lottie--loader {
  width: 94%;
  height: 94%;
  transform: none;
}

.wallet-skeleton {
  position: absolute;
  inset: 4px;
  border-radius: 50%;
}

.wallet-toggle__label {
  letter-spacing: 0.02em;
  display: inline-block;
  width: 100%;
  text-align: center;
  padding-right: 0.4rem;
}

.wallet-toggle__info {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  line-height: 1.1;
  width: 100%;
  text-align: center;
  padding-right: 0.3rem;
}

.wallet-toggle__info strong {
  font-size: 1.05rem;
}

.wallet-toggle__info small {
  font-size: 0.75rem;
  opacity: 0.9;
}

.wallet-toggle--connected {
  background: #8cc84a;
  color: #ffffff;
  padding: 0.3rem 3.2rem 0.3rem 0.7rem;
}

.wallet-toggle--connected .wallet-toggle__icon {
  left: calc(100% - 44px);
  background: #1aa6c3;
}

.wallet-toggle--pending {
  padding: 0.3rem 0.7rem;
}

.wallet-toggle--pending .wallet-toggle__icon {
  left: calc(50% - 20px);
}

.wallet-error {
  color: #d32f2f;
  font-weight: 600;
  font-size: 0.75rem;
  margin: 0;
}

@media (max-width: 1024px) {
  .nav-menu {
    display: none;
  }

  .wallet-toggle {
    width: 160px;
    min-height: 40px;
    font-size: 0.8rem;
    padding: 0.25rem 0.5rem 0.25rem 2.6rem;
  }

  .wallet-toggle__icon {
    width: 32px;
    height: 32px;
  }

  .wallet-toggle--connected {
    padding: 0.25rem 2.6rem 0.25rem 0.5rem;
  }

  .wallet-toggle--connected .wallet-toggle__icon {
    left: calc(100% - 36px);
  }

  .wallet-toggle--pending .wallet-toggle__icon {
    left: calc(50% - 16px);
  }
}
</style>

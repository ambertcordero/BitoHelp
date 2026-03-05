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

const projectId = '1e52dff3b9c75d86cfc7b1190c02d3a0'
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

  window[WALLET_CLIENT_GLOBAL_KEY] = {
    namespace: walletNamespace.value,
    chain: walletChain.value,
    address: walletAddress.value,
    request: (payload) => signClient.request({ topic: sessionTopic, ...payload }),
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

  if (targetAddress && targetAddress !== walletAddress.value) {
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

  if (targetAddress && targetAddress !== walletAddress.value) {
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
  const start = walletAddress.value.slice(0, 6)
  const end = walletAddress.value.slice(-4)
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

const formattedBalance = computed(() => {
  if (!isConnected.value) {
    return '0.000'
  }

  if (isBalanceLoading.value) {
    return `Loading ${walletSymbol.value}...`
  }

  return `${walletBalance.value.toFixed(3)} ${walletSymbol.value}`
})

const walletIconClass = computed(() =>
  isConnected.value ? 'wallet-toggle__icon--connected' : 'wallet-toggle__icon--idle',
)

const parseAccount = (account) => {
  if (!account) {
    return ''
  }
  const parts = account.split(':')
  return parts[parts.length - 1] || ''
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
  const bchNamespace = session.namespaces.bch
  const evmNamespace = session.namespaces.eip155

  let namespaceKey = ''
  let account = ''
  let chain = ''

  if (bchNamespace?.accounts?.length) {
    const preferredBchAccount = selectPreferredAccount(bchNamespace.accounts, bchChains)
    namespaceKey = 'bch'
    account = preferredBchAccount
    chain = parseChainFromAccount(account)
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
  walletAddress.value = parseAccount(account)

  const metadata = session.peer?.metadata
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
      const isBchTestnet = chainId === 'bch:bchtest' || address.toLowerCase().startsWith('bchtest:')
      const apiBase = isBchTestnet
        ? 'https://trest.bitcoin.com/v2/address/details/'
        : 'https://rest.bitcoin.com/v2/address/details/'
      const response = await fetch(`${apiBase}${address}`)
      if (!response.ok) {
        throw new Error('Balance request failed')
      }
      const data = await response.json()
      const balanceSat = data.balanceSat ?? 0
      setBalanceSafely(balanceSat / 1e8)
    }
  } catch {
    logWalletBalanceDebug('request:error', {
      account: address,
      chainId,
    })
  } finally {
    finishLoading()
  }
}

const initWalletConnect = async () => {
  if (signClient) {
    return
  }

  signClient = await SignClient.init({
    projectId,
    metadata: {
      name: 'BiToHelp',
      description: 'Periodic donations on Bitcoin Cash.',
      url: window.location.origin,
      icons: [logoUrl],
    },
  })

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

        walletAddress.value = parseAccount(account)
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

    updateFromSession({
      namespaces: params.namespaces,
      peer: {
        metadata: {
          name: walletName.value,
          icons: walletIconUrl.value ? [walletIconUrl.value] : [],
        },
      },
    })
  })

  const existingSessions = signClient.session.getAll()
  if (existingSessions.length) {
    const session = existingSessions[0]
    sessionTopic = session.topic
    isConnected.value = true
    updateFromSession(session)
  }
}

const handleConnect = async () => {
  walletError.value = ''
  qrDismissed = false
  await initWalletConnect()

  if (!signClient) {
    walletError.value = 'WalletConnect client failed to initialize.'
    return
  }

  if (isConnected.value && sessionTopic) {
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
    let connection

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

    const session = await approval()
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
  destroyWalletLottie()
  destroyBitcoinLoader()
})
</script>

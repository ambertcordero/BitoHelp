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

        <!-- Wallet Button ini !!!-->
        <q-btn
          v-if="!isConnected"
          unelevated
          icon="mdi-wallet"
          label="Connect Wallet"
          class="wallet-btn"
          @click="handleConnectWallet"
          :loading="connecting"
          :loading-label="'Connecting...'"
        >
          <q-tooltip v-if="!connecting">Click to connect your BCH wallet</q-tooltip>
        </q-btn>
        
        <!-- Connected Wallet Info -->
        <div v-else class="row items-center q-gutter-sm">
          <q-chip
            icon="mdi-wallet"
            color="primary"
            text-color="white"
            class="q-py-sm"
          >
            <div class="column">
              <div class="text-caption">{{ shortAddress }}</div>
              <div class="text-weight-bold">{{ formattedBalance }}</div>
            </div>
          </q-chip>
          <q-btn
            flat
            dense
            round
            icon="mdi-close"
            @click="disconnectWallet"
          >
            <q-tooltip>Disconnect Wallet</q-tooltip>
          </q-btn>
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
import { ref } from 'vue'
import { useBCHContract } from '../composables/useBCHContract'
import { useQuasar } from 'quasar'

const $q = useQuasar()

const {
  isConnected,
  isTestMode,
  formattedBalance,
  shortAddress,
  connectWallet,
  disconnectWallet
} = useBCHContract()

const connecting = ref(false)


const handleConnectWallet = async () => {
  connecting.value = true
  
  
  let loadingNotif = null
  if (!isTestMode.value) {
    loadingNotif = $q.notify({
      type: 'ongoing',
      message: 'Connecting to wallet...',
      spinner: true,
      position: 'top',
      timeout: 0 
    })
  }
  
 
  const timeoutPromise = new Promise((_, reject) => {
    setTimeout(() => reject(new Error('Connection timeout - taking too long')), 10000) // 10 second timeout
  })
  
  try {
    
    await Promise.race([
      connectWallet(),
      timeoutPromise
    ])
    
    
    if (loadingNotif) {
      loadingNotif()
    }
    
    $q.notify({
      type: 'positive',
      message: isTestMode.value ? 'Test wallet connected!' : 'Wallet connected successfully!',
      caption: shortAddress.value,
      position: 'top',
      timeout: 2000
    })
  } catch (error) {
    console.error('Connection error:', error)
    
    
    if (loadingNotif) {
      loadingNotif()
    }
    
    $q.notify({
      type: 'negative',
      message: 'Failed to connect wallet',
      caption: error.message || 'Please try again or use test mode',
      position: 'top',
      timeout: 4000,
      actions: [
        {
          label: 'Retry',
          color: 'white',
          handler: () => {
            handleConnectWallet()
          }
        }
      ]
    })
  } finally {
    connecting.value = false
  }
}
</script>

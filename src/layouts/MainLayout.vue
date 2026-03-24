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
        <q-btn round icon="notifications" flat color="blue" class="q-mr-sm" @click="toggleNotifications">
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

        <!-- Wallet Button ini !!!-->
        <q-btn
          v-if="!isConnected"
          unelevated
          icon="mdi-wallet"
          label="Connect Wallet"
          class="wallet-btn q-px-md q-py-sm"
          no-caps
          align="center"
          @click="handleConnectWallet"
          :loading="connecting"
          :loading-label="'Connecting...'"
        >
          <q-tooltip v-if="!connecting">Click to connect your BCH wallet</q-tooltip>
        </q-btn>
        
    
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

    <q-page-container>
      <router-view />
    </q-page-container>

  </q-layout>
</template>

<script setup>
import { ref, computed, watch, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import { useBCHContract } from '../composables/useBCHContract'
import { useDonationStore } from '../stores/donation-store'
import { useQuasar } from 'quasar'

const $q = useQuasar()
const router = useRouter()
const donationStore = useDonationStore()

const {
  isConnected,
  isTestMode,
  formattedBalance,
  shortAddress,
  connectWallet,
  disconnectWallet
} = useBCHContract()

const connecting = ref(false)
const CHARITY_WALLET = 'bitcoincash:qp3wjpa3tjlj042z2wv7hahsldgwhwy0rq9sywjpyy'
const notifications = ref([])
const unreadCount = computed(() => notifications.value.filter(n => !n.read).length)
const lastCheckedId = ref(null)


watch(() => donationStore.latestDonation, (newDonation, oldDonation) => {
  if (newDonation && newDonation !== oldDonation) {
    if (newDonation.recipient === CHARITY_WALLET) {
      addCharityNotification({
        title: 'New Donation Received!',
        message: `Received ${newDonation.amount} BCH for ${newDonation.cause}`,
        txid: newDonation.txid,
        amount: newDonation.amount,
        cause: newDonation.cause,
        isCharity: true
      })
    } else {
      addNotification({
        title: 'Donation Successful!',
        message: `Your donation of ${newDonation.amount} BCH to ${newDonation.cause} was sent successfully.`,
        txid: newDonation.txid,
        isCharity: false
      })
    }
  }
})


let pollInterval = null

onMounted(() => {
  pollInterval = setInterval(checkForNewDonations, 30000)
  checkForNewDonations()
})

onUnmounted(() => {
  if (pollInterval) {
    clearInterval(pollInterval)
  }
})

async function checkForNewDonations() {
  try {
    await donationStore.fetchDonations(10)
    const donations = donationStore.donationHistory
    
    
    const charityDonations = donations.filter(d => d.recipient === CHARITY_WALLET)
    
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
          isCharity: true
        })
      }
    }
  } catch (error) {
    console.error('Error checking for new donations:', error)
  }
}


function addNotification(data) {
  const notification = {
    id: Date.now(),
    title: data.title,
    message: data.message,
    time: new Date().toLocaleTimeString(),
    read: false,
    txid: data.txid,
    isCharity: data.isCharity || false
  }
  notifications.value.unshift(notification)
  
  if (notifications.value.length > 20) {
    notifications.value = notifications.value.slice(0, 20)
  }
}

function addCharityNotification(data) {
  const notification = {
    id: Date.now(),
    title: data.title,
    message: data.message,
    time: new Date().toLocaleTimeString(),
    read: false,
    txid: data.txid,
    amount: data.amount,
    cause: data.cause,
    donorName: data.donorName,
    isCharity: true
  }
  notifications.value.unshift(notification)
  
  
  if (notifications.value.length > 20) {
    notifications.value = notifications.value.slice(0, 20)
  }
  
 
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
        }
      }
    ]
  })
}

function toggleNotifications() {
  notifications.value.forEach(n => n.read = true)
}

function markAsRead(id) {
  const notification = notifications.value.find(n => n.id === id)
  if (notification) {
    notification.read = true
    if (notification.isCharity) {
      router.push('/dashboard')
    }
  }
}

function removeNotification(id) {
  const index = notifications.value.findIndex(n => n.id === id)
  if (index > -1) {
    notifications.value.splice(index, 1)
  }
}

function clearAllNotifications() {
  notifications.value = []
}



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
    setTimeout(() => reject(new Error('Connection timeout - taking too long')), 10000) 
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
  margin-right: 15px;
}

.wallet-btn {
  background: #1976d2;
  color: white;
  border-radius: 8px;
  font-weight: 600;
}

@media (max-width: 1024px) {
  .nav-menu {
    display: none;
  }
  
  .wallet-btn {
    font-size: 12px;
    padding: 4px 8px;
  }
  
  .wallet-btn .q-btn__content {
    font-size: 11px;
  }
}
</style>

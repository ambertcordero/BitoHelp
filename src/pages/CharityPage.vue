<template>
  <q-page class="charity-dashboard">
    <div class="dashboard-container">
      <div class="stats-row">
        <q-card class="stat-card stat-card-blue">
          <q-card-section>
            <div class="stat-header">TOTAL DONATION</div>
            <div class="stat-header">RECIEVED</div>
            <div class="stat-content">
              <div class="stat-icon">
                <img src="~assets/bch.png" alt="Bitcoin" class="stat-icon-img" />
              </div>
              <div class="stat-value">{{ totalReceived }} BCH</div>
              <div class="stat-badge">
                <img src="~assets/donation.png" alt="Donate" class="stat-badge-img" />
                <div class="badge-text">{{ totalDonationCount }} DONATIONS</div>
              </div>
            </div>
          </q-card-section>
        </q-card>

        <q-card class="stat-card stat-card-purple">
          <q-card-section>
            <div class="stat-header">TOTAL</div>
            <div class="stat-header">PROJECTS</div>
            <div class="stat-content">
              <div class="stat-value-large">{{ totalProjects }}+</div>
              <div class="stat-icon-right">
                <img src="~assets/project.png" alt="Verified" class="stat-icon-right-img" />
              </div>
            </div>
          </q-card-section>
        </q-card>

        <q-card class="stat-card stat-card-yellow">
          <q-card-section>
            <div class="stat-header">VERIFIED</div>
            <div class="stat-header">TRANSACTION</div>
            <div class="stat-content">
              <div class="stat-value-large">{{ totalTransactions }}+</div>
              <div class="stat-icon-badge">
                <img src="~assets/transaction.png" alt="Badge" class="stat-icon-badge-img" />
              </div>
            </div>
          </q-card-section>
        </q-card>
      </div>

     
      <div class="main-content-row">
        <q-card class="management-panel">
          <q-card-section>
            <div class="panel-title">DONATION MANAGANENT</div>
            <div class="fund-list">
              <div v-for="fund in displayedFunds" :key="fund.name" class="fund-item">
                <div class="fund-icon">
                  <img src="~assets/paytaca.png" alt="Fund" class="fund-icon-img" />
                </div>
                <div class="fund-info">
                  <div class="fund-name">{{ fund.name }}</div>
                  <div class="fund-details">{{ fund.hours }} • {{ fund.amount }}</div>
                </div>
                <q-btn 
                  label="Withdraw" 
                  color="primary" 
                  size="sm" 
                  unelevated 
                  class="withdraw-btn"
                />
              </div>
            </div>
            <div class="see-more" v-if="funds.length > 5" @click="toggleFunds">
              {{ showAllFunds ? 'Show Less' : 'See More' }}
            </div>
          </q-card-section>
        </q-card>

        <q-card class="wallet-panel">
          <q-card-section class="wallet-panel-section">
            <div class="panel-title-with-info">
              <span>WALLET TRANSACTION</span>
              <q-icon name="info" size="20px" class="info-icon" />
            </div>

            <div class="wallet-box">
              <div class="wallet-content">
                <div class="wallet-icon-section">
                  <div class="wallet-icon-wrapper">
                    <img src="~assets/paytaca.png" alt="Wallet" class="wallet-icon-img" />
                  </div>
                  <div class="wallet-title">WALLET</div>
                </div>
                <div class="wallet-info-section">
                  <div class="info-row">
                    <span class="info-label">CHARITY NAME:</span>
                    <span class="info-value">{{ latestDonation?.cause || 'No donations yet' }}</span>
                  </div>
                  <div class="info-row">
                    <span class="info-label">RECIPIENT ADDRESS:</span>
                    <span class="info-value">{{ latestDonation ? CHARITY_WALLET.substring(0, 20) + '...' : 'No donations yet' }}</span>
                  </div>
                  <div class="info-row">
                    <span class="info-label">COIN:</span>
                    <span class="info-value">{{ latestDonation?.coin || 'Bitcoin Cash (BCH)' }}</span>
                  </div>
                  <div class="info-row">
                    <span class="info-label">AMOUNT:</span>
                    <span class="info-value highlight">{{ latestDonation?.amount || '0' }} {{ latestDonation?.coin || 'Bitcoin Cash (BCH)' }}</span>
                  </div>
                </div>
              </div>
              <div class="wallet-addresses">
                <div class="address-row">
                  <span class="address-label">CHARITY WALLET ADDRESS:</span>
                  <span class="address-text">{{ CHARITY_WALLET }}</span>
                  <q-btn 
                    flat 
                    dense 
                    round 
                    icon="content_copy" 
                    size="xs"
                    @click="copyToClipboard(CHARITY_WALLET)"
                  >
                    <q-tooltip>Copy address</q-tooltip>
                  </q-btn>
                </div>
                <div class="address-row">
                  <span class="address-label">TOTAL RECEIVED:</span>
                  <span class="address-text">{{ totalReceived }} BCH</span>
                </div>
              </div>
            </div>

            <div class="recent-section">
              <div class="section-header">
                <div class="section-title">RECENT DONATION</div>
                <div style="display: flex; gap: 8px; align-items: center;">
                  <div class="section-type">BCH Transaction</div>
                  <q-btn 
                    flat
                    dense
                    round
                    icon="refresh" 
                    size="sm"
                    color="primary"
                    @click="refreshDonations"
                    :loading="donationStore.isLoading"
                  >
                    <q-tooltip>Refresh donations</q-tooltip>
                  </q-btn>
                </div>
              </div>

              <div v-if="recentDonations.length === 0" class="no-donations">
                <q-icon name="inbox" size="48px" color="grey-5" />
                <div class="no-donations-text">No donations received yet</div>
              </div>

              <q-expansion-item
                v-for="(donation, index) in displayedDonations" 
                :key="index"
                class="donation-expansion-item"
              >
                <template v-slot:header>
                  <div class="donation-item">
                    <div class="donation-icon">
                      <img src="~assets/paytaca.png" alt="BCH" class="donation-icon-img" />
                    </div>
                    <div class="donation-info">
                      <div class="donation-name">{{ donation.cause }}</div>
                      <div class="donation-date">{{ formatDate(donation.timestamp) }}</div>
                    </div>
                    <div class="donation-amount">{{ donation.amount }} BCH</div>
                    <q-badge color="positive" rounded>Received</q-badge>
                  </div>
                </template>

                <q-card flat bordered class="donor-details-card">
                  <q-card-section>
                    <div class="donor-title">Donor Information</div>
                    
                    <div class="donor-info-grid">
                      <div class="donor-field">
                        <q-icon name="person" color="primary" size="20px" />
                        <div class="donor-field-content">
                          <div class="donor-field-label">Name</div>
                          <div class="donor-field-value">{{ donation.donor_name || 'Anonymous' }}</div>
                        </div>
                      </div>

                      <div class="donor-field">
                        <q-icon name="email" color="primary" size="20px" />
                        <div class="donor-field-content">
                          <div class="donor-field-label">Email</div>
                          <div class="donor-field-value">{{ donation.donor_email || 'Not provided' }}</div>
                        </div>
                      </div>

                      <div class="donor-field">
                        <q-icon name="phone" color="primary" size="20px" />
                        <div class="donor-field-content">
                          <div class="donor-field-label">Contact</div>
                          <div class="donor-field-value">{{ donation.donor_contact || 'Not provided' }}</div>
                        </div>
                      </div>

                      <div class="donor-field">
                        <q-icon name="description" color="primary" size="20px" />
                        <div class="donor-field-content">
                          <div class="donor-field-label">Message</div>
                          <div class="donor-field-value">{{ donation.message || 'No message' }}</div>
                        </div>
                      </div>

                      <div class="donor-field full-width">
                        <q-icon name="link" color="primary" size="20px" />
                        <div class="donor-field-content">
                          <div class="donor-field-label">Transaction ID</div>
                          <div class="donor-field-value txid">
                            {{ donation.txid }}
                            <q-btn 
                              flat 
                              dense 
                              round 
                              icon="content_copy" 
                              size="xs"
                              @click.stop="copyToClipboard(donation.txid)"
                            />
                            <q-btn 
                              flat 
                              dense 
                              round 
                              icon="open_in_new" 
                              size="xs"
                              @click.stop="openExplorer(donation.explorer_url)"
                            />
                          </div>
                        </div>
                      </div>
                    </div>
                  </q-card-section>
                </q-card>
              </q-expansion-item>

              <div class="see-more" v-if="recentDonations.length > 5" @click="toggleDonations">
                {{ showAllDonations ? 'Show Less' : 'See More' }}
              </div>
            </div>
          </q-card-section>
        </q-card>
      </div>

   
      <div class="bottom-row">
        <div class="projects-section">
          <div class="section-title-main">PROJECTS</div>
          <div class="projects-grid">
            <q-card class="project-card" v-for="project in projects" :key="project.name">
              <img :src="project.image" class="project-image" />
              <div class="project-overlay">
                <div class="project-title">{{ project.name }}</div>
              </div>
            </q-card>
          </div>
        </div>

      
        <q-card class="chart-card">
          <q-card-section>
            <div class="chart-title">DONATION TRANSACTION CHART</div>
            
            <div class="chart-legend">
              <div class="legend-item">
                <div class="legend-dot" style="background: #5b7cff"></div>
                <span>Medical Fund</span>
              </div>
              <div class="legend-item">
                <div class="legend-dot" style="background: #b99aff"></div>
                <span>Educ Fund</span>
              </div>
              <div class="legend-item">
                <div class="legend-dot" style="background: #ffb84d"></div>
                <span>Health Fund</span>
              </div>
            </div>

            <div class="chart-container">
              <div class="chart-bars">
                <div v-for="data in chartData" :key="data.coin" class="bar-group">
                  <div class="bars">
                    <div 
                      v-for="(bar, index) in data.values" 
                      :key="index"
                      class="bar"
                      :style="{ height: bar.value * 10 + 'px', background: bar.color }"
                    ></div>
                  </div>
                  <div class="bar-label">{{ data.coin }}</div>
                </div>
              </div>
              <div class="y-axis">
                <div v-for="n in 6" :key="n" class="y-label">{{ (6-n) * 5 }}</div>
              </div>
            </div>
          </q-card-section>
        </q-card>
      </div>

    </div>
  </q-page>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useDonationStore } from '../stores/donation-store'
import { useQuasar } from 'quasar'

const $q = useQuasar()
const donationStore = useDonationStore()


const CHARITY_WALLET = 'bitcoincash:qp3wjpa3tjlj042z2wv7hahsldgwhwy0rq9sywjpyy'
const totalProjects = ref('100')
const totalTransactions = ref('100')


const showAllFunds = ref(false)
const showAllDonations = ref(false)

const funds = ref([
  { name: 'Medical Fund', icon: 'volunteer_activism', color: 'red', hours: '5 Years cont...', amount: '0.5BCH' },
  { name: 'Educational Fund', icon: 'school', color: 'green', hours: '2 Years cont...', amount: '0.15BCH' },
  { name: 'Typhoon Relief Fund', icon: 'cyclone', color: 'blue', hours: '3 Years cont...', amount: '0.25BCH' },
  { name: 'Health Fund', icon: 'favorite', color: 'red', hours: '1 Years cont...', amount: '0.5BCH' },
  { name: 'Medical Fund', icon: 'local_hospital', color: 'orange', hours: '5  cont...', amount: '0.25BCH' },
  { name: 'Medical Fund', icon: 'medical_services', color: 'orange', hours: '5 Years cont...', amount: '0.23BCH' },
  { name: 'Medical Fund', icon: 'volunteer_activism', color: 'blue', hours: '5 Years cont...', amount: '0.50BCH' },
  { name: 'Medical Fund', icon: 'health_and_safety', color: 'purple', hours: '5 Years cont...', amount: '0.57BCH' },
])


const recentDonations = computed(() => {
  const filtered = donationStore.donationHistory
    .filter(d => d.recipient === CHARITY_WALLET)
  
  console.log('=== CHARITY PAGE DEBUG ===')
  console.log('Total donations in history:', donationStore.donationHistory.length)
  console.log('All donations:', donationStore.donationHistory)
  console.log('CHARITY_WALLET:', CHARITY_WALLET)
  console.log('Filtered donations for this charity:', filtered.length)
  console.log('Filtered donations:', filtered)
  
  return filtered
})



const latestDonation = computed(() => {
  return recentDonations.value.length > 0 ? recentDonations.value[0] : null
})

const displayedFunds = computed(() => {
  return showAllFunds.value ? funds.value : funds.value.slice(0, 5)
})

const displayedDonations = computed(() => {
  return showAllDonations.value ? recentDonations.value : recentDonations.value.slice(0, 5)
})

function toggleFunds() {
  showAllFunds.value = !showAllFunds.value
}

function toggleDonations() {
  showAllDonations.value = !showAllDonations.value
}



const totalReceived = computed(() => {
  const total = recentDonations.value.reduce((sum, d) => {
    return sum + parseFloat(d.amount || 0)
  }, 0)
  return total .toFixed(2)
})

const totalDonationCount = computed(() => recentDonations.value.length)

const projects = ref([
  { name: 'Medical Fund', image: new URL('../assets/medical.jpg', import.meta.url).href },
  { name: 'Typhoon Fund', image: new URL('../assets/typhoon.jpeg', import.meta.url).href },
])

const chartData = ref([
  { 
    coin: 'Paytaca', 
    values: [
      { value: 15, color: '#5b7cff' },
      { value: 5, color: '#b99aff' },
      { value: 5, color: '#ffb84d' }
    ]
  },
  { 
    coin: 'BNB', 
    values: [
      { value: 5, color: '#5b7cff' },
      { value: 12, color: '#b99aff' },
      { value: 10, color: '#ffb84d' }
    ]
  },
  { 
    coin: 'ETHERIUM', 
    values: [
      { value: 15, color: '#5b7cff' },
      { value: 17, color: '#b99aff' },
      { value: 22, color: '#ffb84d' }
    ]
  },
])


function formatDate(timestamp) {
  if (!timestamp) return 'Unknown date'
  const date = new Date(timestamp)
  return date.toLocaleString('en-US', { 
    month: 'short', 
    day: 'numeric', 
    year: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}

function copyToClipboard(text) {
  navigator.clipboard.writeText(text)
  $q.notify({
    type: 'positive',
    message: 'Copied to clipboard!',
    position: 'top',
    timeout: 2000
  })
}

function openExplorer(url) {
  if (url) {
    window.open(url, '_blank')
  }
}

async function refreshDonations() {
  console.log('Manually refreshing donations...')
  await donationStore.fetchDonations(50)
  $q.notify({
    type: 'positive',
    message: 'Donations refreshed',
    position: 'top',
    timeout: 1000
  })
}

onMounted(async () => {
  await donationStore.fetchDonations(50)
  console.log('CharityPage mounted - donations fetched')
})

watch(() => donationStore.latestDonation, (newDonation) => {
  if (newDonation) {
    console.log('New donation detected:', newDonation)
    donationStore.fetchDonations(50)
  }
})
</script>

<style scoped>
.charity-dashboard {
  background: #d1cece82;
  min-height: 100vh;
  padding: 20px;
}

.dashboard-container {
  max-width: 1400px;
  margin: 0 auto;
}


.stats-row {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 20px;
  margin-bottom: 20px;
}

.stat-card {
  border-radius: 20px;
  padding: 10px;
  color: white;
}

.stat-card-blue {
  background: linear-gradient(135deg, #6c85f5dc 0%, #8799f3 100%);
  border: 4px solid #fffdf9;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.5);
}

.stat-card-purple {
  background: linear-gradient(135deg, #a9a4ffd3 0%, #7e7affd0 100%);
  border: 4px solid #fffdf9;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.5);
}

.stat-card-yellow {
  background: linear-gradient(135deg, #e3d273d9 0%, #ebcf89e2 100%);
  border: 4px solid #fffdf9;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.5);
}

.stat-header {
  font-size: 36px;
  font-weight: bold;
  line-height: 1.2;
}

.stat-content {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-top: 15px;
}

.stat-icon {
  background: rgba(255, 255, 255, 0.2);
  border-radius: 50%;
  padding: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.stat-icon-img {
  width: 80px;
  height: 80px;
  object-fit: contain;
}

.stat-value {
  font-size: 32px;
  font-weight: bold;
  font-style: italic;
}

.stat-value-large {
  font-size: 48px;
  font-weight: bold;
}

.stat-badge {
  background: #ffb84d;
  border-radius: 15px;
  padding: 10px 20px;
  text-align: center;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.stat-badge-img {
  width: 48px;
  height: 48px;
  object-fit: contain;
}

.badge-text {
  font-size: 14px;
  font-weight: bold;
  margin-top: 5px;
}

.stat-icon-right {
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
}

.stat-icon-right-img {
  width: 130px;
  height: 130px;
  object-fit: contain;
}

.stat-icon-badge {
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
}

.stat-icon-badge-img {
  width: 130px;
  height: 130px;
  object-fit: contain;
}

/* Main Content */
.main-content-row {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 20px;
  margin-bottom: 20px;
}

.management-panel,
.wallet-panel {
  border-radius: 20px;
}

.management-panel {
  grid-column: 1 / 3;
  max-width: none;
}

.wallet-panel {
  max-width: 420px;
}

.wallet-panel-section {
  padding: 16px !important;
}

.panel-title {
  font-size: 16px;
  font-weight: bold;
  margin-bottom: 15px;
  letter-spacing: 1px;
}

.panel-title-with-info {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 16px;
  font-weight: bold;
  margin-bottom: 15px;
  letter-spacing: 1px;
}

.info-icon {
  cursor: pointer;
  opacity: 0.7;
  
}
/* Fund List */
.fund-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.fund-item {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px;
  background: #f8f9fa;
  border-radius: 12px;
}

.fund-icon {
  background: white;
  border-radius: 50%;
  padding: 6px;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 35px;
  height: 35px;
  flex-shrink: 0;
}

.fund-icon-img {
  width: 50px;
  height: 50px;
  object-fit: contain;
}

.fund-info {
  flex: 1;
  min-width: 0;
}

.fund-name {
  font-weight: 600;
  font-size: 14px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.fund-details {
  font-size: 12px;
  color: #666;
  margin-top: 2px;
  font-style: italic;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.withdraw-btn {
  border-radius: 8px;
  padding: 8px 16px;
  flex-shrink: 0;
}


.wallet-box {
  background: linear-gradient(135deg, #85acea 0%, #2563eb 100%);
  border-radius: 15px;
  padding: 15px;
  color: white;
  margin-bottom: 15px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.5);
  border: 3px solid #fffdf9;
  width: 100%;
}

.wallet-content {
  display: flex;
  gap: 15px;
  margin-bottom: 12px;
  align-items: flex-start;
}

.wallet-icon-section {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 6px;
  min-width: 80px;
}

.wallet-icon-wrapper {
  width: 70px;
  height: 70px;
  background: linear-gradient(135deg, #7cb5fa85 0%, #89afec8b 100%);
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.5);
  overflow: hidden;
}

.wallet-icon {
  width: 40px;
  height: 40px;
  color: white;
}

.wallet-icon-img {
  width: 100px;
  height: 100px;
  object-fit: contain;
}

.wallet-title {
  font-size: 14px;
  font-weight: bold;
  letter-spacing: 1px;
}

.wallet-info-section {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.info-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1px 0;
}

.info-label {
  font-size: 10px;
  opacity: 0.9;
  font-weight: 500;
  letter-spacing: 0.3px;
}

.info-value {
  font-size: 11px;
  font-weight: bold;
  text-align: right;
}

.info-value.highlight {
  color: #fbbf24;
  font-size: 12px;
}

.wallet-addresses {
  display: flex;
  flex-direction: column;
  gap: 6px;
  border-top: 1px solid rgba(255, 255, 255, 0.2);
  padding-top: 10px;
  margin-top: 6px;
}

.address-row {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 9px;
}

.address-label {
  font-weight: 600;
  min-width: 150px;
  opacity: 0.9;
  font-size: 9px;
}

.address-text {
  flex: 1;
  word-break: break-all;
  font-size: 8px;
  opacity: 0.9;
}

.copy-icon {
  cursor: pointer;
  opacity: 0.7;
  transition: opacity 0.2s;
}

.copy-icon:hover {
  opacity: 1;
}


.recent-section {
  margin-top: 0;
  width: 100%;
  max-height: 400px;
  overflow-y: auto;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
}

.section-title {
  font-size: 13px;
  font-weight: bold;
}

.section-type {
  font-size: 11px;
  color: #666;
}

.donation-item {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 10px;
  background: #f8f9fa;
  border-radius: 10px;
  margin-bottom: 8px;
  width: 100%;
}

.donation-icon {
  width: 28px;
  height: 28px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #3b82f6;
}

.heart-icon {
  width: 24px;
  height: 24px;
}

.donation-icon-img {
  width: 60px;
  height: 60px;
  object-fit: contain;
}

.donation-info {
  flex: 1;
}

.donation-name {
  font-weight: 600;
  font-size: 13px;
}

.donation-date {
  font-size: 11px;
  color: #666;
  margin-top: 2px;
  font-style: italic;
}

.donation-amount {
  font-weight: bold;
  margin-right: 8px;
  font-size: 13px;
}

.donation-btn {
  min-width: 70px;
  border-radius: 20px;
  font-size: 11px;
  padding: 4px 12px;
}

.see-more {
  text-align: center;
  color: #666;
  font-size: 14px;
  cursor: pointer;
  margin-top: 10px;
  padding: 8px;
  width: 100%;
}

.see-more:hover {
  text-decoration: underline;
}


.donation-expansion-item {
  margin-bottom: 8px;
  width: 100%;
}

.no-donations {
  text-align: center;
  padding: 40px 20px;
  color: #999;
}

.no-donations-text {
  margin-top: 12px;
  font-size: 14px;
}

.donor-details-card {
  margin-top: 8px;
  background: #fafbfc;
}

.donor-title {
  font-size: 16px;
  font-weight: bold;
  margin-bottom: 16px;
  color: #2c3e50;
}

.donor-info-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
}

.donor-field {
  display: flex;
  gap: 12px;
  align-items: start;
}

.donor-field.full-width {
  grid-column: 1 / -1;
}

.donor-field-content {
  flex: 1;
}

.donor-field-label {
  font-size: 12px;
  color: #666;
  margin-bottom: 4px;
  font-weight: 500;
}

.donor-field-value {
  font-size: 14px;
  color: #2c3e50;
  font-weight: 600;
  word-break: break-word;
}

.donor-field-value.txid {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 12px;
  font-family: monospace;
}

/* Bottom Row - Projects and Chart */
.bottom-row {
  display: grid;
  grid-template-columns: 400px 1fr;
  gap: 20px;
  margin-bottom: 20px;
}


.projects-section {
  display: flex;
  flex-direction: column;
}

.section-title-main {
  font-size: 18px;
  font-weight: bold;
  margin-bottom: 15px;
  letter-spacing: 1px;
}

.projects-grid {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.project-card {
  border-radius: 20px;
  overflow: hidden;
  position: relative;
  height: 200px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.5);

}

.project-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.project-overlay {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  background: linear-gradient(to top, rgba(0,0,0,0.7), transparent);
  padding: 20px;
}

.project-title {
  color: white;
  font-weight: bold;
  font-size: 18px;
}


.chart-card {
  border-radius: 20px;
}

.chart-title {
  font-size: 16px;
  font-weight: bold;
  margin-bottom: 15px;
  letter-spacing: 1px;
}

.chart-legend {
  display: flex;
  gap: 25px;
  margin-bottom: 20px;
}

.legend-item {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 13px;
}

.legend-dot {
  width: 12px;
  height: 12px;
  border-radius: 50%;
}

.chart-container {
  display: flex;
  gap: 20px;
  position: relative;
}

.chart-bars {
  flex: 1;
  display: flex;
  justify-content: space-around;
  align-items: flex-end;
  height: 300px;
  border-bottom: 2px solid #e5e7eb;
  padding-bottom: 30px;
}

.bar-group {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.bars {
  display: flex;
  gap: 4px;
  align-items: flex-end;
  height: 250px;
}

.bar {
  width: 35px;
  border-radius: 8px 8px 0 0;
  transition: all 0.3s ease;
}

.bar:hover {
  opacity: 0.8;
}

.bar-label {
  margin-top: 10px;
  font-size: 13px;
  font-weight: 600;
}

.y-axis {
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  height: 280px;
  padding-bottom: 30px;
}

.y-label {
  font-size: 12px;
  color: #666;
}

@media (max-width: 1400px) {
  .main-content-row {
    grid-template-columns: 1fr 1fr;
    gap: 15px;
  }

  .management-panel {
    grid-column: 1 / 2;
  }

  .wallet-panel {
    grid-column: 2 / 3;
    max-width: 100%;
  }
}

@media (max-width: 1024px) {
  .stats-row {
    grid-template-columns: 1fr;
  }

  .main-content-row {
    grid-template-columns: 1fr;
  }

  .management-panel {
    grid-column: 1;
  }

  .wallet-panel {
    max-width: 100%;
  }

  .wallet-box {
    max-width: 100%;
  }

  .bottom-row {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 768px) {
  .charity-dashboard {
    padding: 15px;
  }

  .stats-row {
    gap: 15px;
  }

  .main-content-row {
    gap: 15px;
  }

  .stat-card {
    padding: 15px;
  }

  .wallet-content {
    flex-direction: column;
    align-items: center;
    gap: 12px;
  }

  .wallet-icon-section {
    width: 100%;
    flex-direction: row;
    justify-content: center;
  }

  .wallet-info-section {
    width: 100%;
  }

  .address-row {
    flex-direction: column;
    gap: 4px;
    align-items: flex-start;
  }

  .address-label {
    min-width: auto;
  }

  .info-row {
    flex-direction: column;
    gap: 2px;
    align-items: flex-start;
  }

  .info-label {
    font-size: 9px;
  }

  .info-value {
    font-size: 10px;
    text-align: left;
  }

  .donation-item {
    flex-wrap: wrap;
    gap: 8px;
    padding: 8px;
  }

  .donation-icon-img {
    width: 50px;
    height: 50px;
  }

  .fund-item {
    flex-wrap: wrap;
    padding: 8px;
  }

  .fund-name {
    font-size: 13px;
  }

  .recent-section {
    max-width: 100%;
  }
}

@media (max-width: 480px) {
  .charity-dashboard {
    padding: 10px;
  }

  .dashboard-container {
    padding: 0;
  }

  .wallet-box {
    padding: 12px;
  }

  .wallet-icon-wrapper {
    width: 60px;
    height: 60px;
  }

  .wallet-icon-img {
    width: 80px;
    height: 80px;
  }

  .wallet-title {
    font-size: 12px;
  }

  .panel-title,
  .panel-title-with-info {
    font-size: 14px;
  }

  .donation-name,
  .fund-name {
    font-size: 12px;
  }

  .donation-date,
  .fund-details {
    font-size: 10px;
  }

  .address-text {
    font-size: 7px;
  }
}

</style>


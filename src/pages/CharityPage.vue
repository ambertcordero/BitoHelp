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
              <div class="stat-value">{{ totalDonations }} BCH</div>
              <div class="stat-badge">
                <img src="~assets/donation.png" alt="Donate" class="stat-badge-img" />
                <div class="badge-text">DONATE</div>
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
              <div v-for="fund in funds" :key="fund.name" class="fund-item">
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
          </q-card-section>
        </q-card>

        <q-card class="wallet-panel">
          <q-card-section>
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
                    <span class="info-label">CONTRACT:</span>
                    <span class="info-value">5 YEARS</span>
                  </div>
                  <div class="info-row">
                    <span class="info-label">PERIOD OF WITHDRAWAL:</span>
                    <span class="info-value">AFTER 30 DAYS</span>
                  </div>
                  <div class="info-row">
                    <span class="info-label">AMOUNT:</span>
                    <span class="info-value">1 MILLION</span>
                  </div>
                  <div class="info-row">
                    <span class="info-label">BALANCE:</span>
                    <span class="info-value highlight">4.5 MILLION</span>
                  </div>
                </div>
              </div>
              <div class="wallet-addresses">
                <div class="address-row">
                  <span class="address-label">CONTRACT ADDRESS:</span>
                  <span class="address-text">bitcoincash:qp3wjpa3tjlj042z2wv7hahsldgwhwy0rq9sywjpyy</span>
                  <q-icon name="content_copy" size="14px" class="copy-icon" />
                </div>
                <div class="address-row">
                  <span class="address-label">DONOR ADDRESS:</span>
                  <span class="address-text">bitcoincash:qp3wjpa3tjlj042z2wv7hahsldgwhwy0rq9sywjpyy</span>
                  <q-icon name="content_copy" size="14px" class="copy-icon" />
                </div>
              </div>
            </div>

            <div class="recent-section">
              <div class="section-header">
                <div class="section-title">RECENT DONATION</div>
                <div class="section-type">BCH Transaction</div>
              </div>

              <div v-for="(donation, index) in recentDonations" :key="index" class="donation-item">
                <div class="donation-icon">
                  <img :src="donation.image" alt="Paytaca" class="donation-icon-img" />
                </div>
                <div class="donation-info">
                  <div class="donation-name">{{ donation.cause }}</div>
                  <div class="donation-date">{{ donation.date }}</div>
                </div>
                <div class="donation-amount">{{ donation.amount }}BCH</div>
                <q-btn 
                  :label="donation.status" 
                  :color="donation.status === 'Recieve' ? 'negative' : 'primary'" 
                  size="sm" 
                  unelevated 
                  rounded
                  class="donation-btn"
                />
              </div>

              <div class="see-more">See More</div>
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
import { ref, onMounted } from 'vue'
import { useDonationStore } from '../stores/donation-store'

const donationStore = useDonationStore()

const totalDonations = ref('5000')
const totalProjects = ref('100')
const totalTransactions = ref('100')

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

const recentDonations = ref([
  { cause: 'Medical Fund', date: 'Month of January', amount: '0.10', status: 'Recieve', image: new URL('../assets/paytaca.png', import.meta.url).href },
  { cause: 'Medical Fund', date: 'Month of February', amount: '0.10', status: 'Recieve', image: new URL('../assets/paytaca.png', import.meta.url).href },
  { cause: 'Medical Fund', date: 'Month of March', amount: '0.10', status: 'Claim', image: new URL('../assets/paytaca.png', import.meta.url).href },
  { cause: 'Medical Fund', date: 'Month of April', amount: '0.10', status: 'Unclaimed', image: new URL('../assets/paytaca.png', import.meta.url).href },
  { cause: 'Medical Fund', date: 'Month of May', amount: '0.10', status: 'Unclaimed', image: new URL('../assets/paytaca.png', import.meta.url).href },
  { cause: 'Medical Fund', date: 'Month of June', amount: '0.10', status: 'Unclaimed', image: new URL('../assets/paytaca.png', import.meta.url).href },
])

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

onMounted(async () => {
  await donationStore.fetchDonations()
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
  grid-template-columns: 380px 1fr;
  gap: 20px;
  margin-bottom: 20px;
}

.management-panel,
.wallet-panel {
  border-radius: 20px;
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
  gap: 12px;
  padding: 12px;
  background: #f8f9fa;
  border-radius: 12px;
}

.fund-icon {
  background: white;
  border-radius: 50%;
  padding: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 40px;
  height: 40px;
}

.fund-icon-img {
  width: 84px;
  height: 84px;
  object-fit: contain;
}

.fund-info {
  flex: 1;
}

.fund-name {
  font-weight: 600;
  font-size: 24px;
}

.fund-details {
  font-size: 16px;
  color: #666;
  margin-top: 2px;
    font-style: italic;
}

.withdraw-btn {
  border-radius: 8px;
  padding: 12px 34px;
  
}

/* Wallet Box */
.wallet-box {
  background: linear-gradient(135deg, #85acea 0%, #2563eb 100%);
  border-radius: 20px;
  padding: 25px;
  color: white;
  margin-bottom: 20px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.5);
  border: 4px solid #fffdf9;
}

.wallet-content {
  display: flex;
  gap: 30px;
  margin-bottom: 20px;
  align-items: center;
}

.wallet-icon-section {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 10px;
  min-width: 120px;
}

.wallet-icon-wrapper {
  width: 100px;
  height: 100px;
  background: linear-gradient(135deg, #7cb5fa85 0%, #89afec8b 100%);
  border-radius: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.5);
  overflow: hidden;
}

.wallet-icon {
  width: 50px;
  height: 50px;
  color: white;
}

.wallet-icon-img {
  width: 160px;
  height: 160px;
  object-fit: contain;
}

.wallet-title {
  font-size: 18px;
  font-weight: bold;
  letter-spacing: 2px;
}

.wallet-info-section {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.info-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 4px 0;
}

.info-label {
  font-size: 14px;
  opacity: 0.95;
  font-weight: 500;
}

.info-value {
  font-size: 13px;
  font-weight: bold;
  text-align: right;
}

.info-value.highlight {
  color: #fbbf24;
  font-size: 14px;
}

.wallet-addresses {
  display: flex;
  flex-direction: column;
  gap: 12px;
  border-top: 1px solid rgba(255, 255, 255, 0.2);
  padding-top: 15px;
}

.address-row {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 10px;
}

.address-label {
  font-weight: 600;
  min-width: 130px;
  opacity: 0.95;
}

.address-text {
  flex: 1;
  font-family: monospace;
  word-break: break-all;
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

/* Recent Section */
.recent-section {
  margin-top: 20px;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
}

.section-title {
  font-size: 14px;
  font-weight: bold;
}

.section-type {
  font-size: 12px;
  color: #666;
}

.donation-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px;
  background: #f8f9fa;
  border-radius: 12px;
  margin-bottom: 10px;
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
  width: 84px;
  height: 84px;
  object-fit: contain;
}

.donation-info {
  flex: 1;
}

.donation-name {
  font-weight: 600;
  font-size: 14px;
}

.donation-date {
  font-size: 12px;
  color: #666;
  margin-top: 2px;
  font-style: italic;
}

.donation-amount {
  font-weight: bold;
  margin-right: 10px;
  font-size: 14px;
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
}

.see-more:hover {
  text-decoration: underline;
}

/* Bottom Row - Projects and Chart */
.bottom-row {
  display: grid;
  grid-template-columns: 400px 1fr;
  gap: 20px;
  margin-bottom: 20px;
}

/* Projects Section */
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

/* Chart */
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

@media (max-width: 1024px) {
  .stats-row {
    grid-template-columns: 1fr;
  }

  .main-content-row {
    grid-template-columns: 1fr;
  }

  .bottom-row {
    grid-template-columns: 1fr;
  }
}
</style>


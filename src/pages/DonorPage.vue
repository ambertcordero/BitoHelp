<template>
  <q-page class="donor-page">
    <div class="row" style="min-height: 100vh;">
      <div class="col-12 col-md-4 col-lg-3 q-pa-md sidebar-container">
        <div class="accounts-sidebar">
          <h5 class="q-mt-none q-mb-md">Donor<br><strong>Dashboard</strong></h5>
          
        
          <div class="q-mb-md">
            <q-btn-toggle
              v-model="activeTab"
              spread
              no-caps
              toggle-color="primary"
              color="white"
              text-color="black"
              :options="[
                {label: 'Donations', value: 'donations'},
                {label: 'Activity', value: 'activity'}
              ]"
            />
          </div>

          <q-input
            v-model="searchQuery"
            outlined
            dense
            placeholder="Search"
            class="q-mb-md"
            bg-color="white"
          >
            <template v-slot:prepend>
              <q-icon name="search" />
            </template>
            <template v-slot:append>
              <q-btn flat dense icon="tune" size="sm" />
            </template>
          </q-input>

          
          <q-list>
            <q-item
              v-for="wallet in wallets"
              :key="wallet.id"
              clickable
              v-ripple
              :active="selectedWallet?.id === wallet.id"
              @click="selectWallet(wallet)"
              class="account-item q-mb-sm rounded-borders"
              active-class="bg-white"
            >
              <q-item-section avatar>
                <img src="~assets/paytaca.png" alt="wallet" class="icon-img" style="width: 32px; height: 32px;" />
              </q-item-section>
              <q-item-section>
                <q-item-label class="text-weight-medium">{{ wallet.name }}</q-item-label>
                <q-item-label caption class="text-caption">{{ wallet.address.substring(0, 12) }}...</q-item-label>
                <div class="row q-mt-sm">
                  <div class="col">
                    <q-item-label caption>Total Donated</q-item-label>
                    <q-item-label class="text-weight-bold">{{ formatCurrency(wallet.totalDonated) }} BCH</q-item-label>
                  </div>
                  <div class="col">
                    <q-item-label caption>Donations</q-item-label>
                    <q-item-label class="text-weight-bold">{{ wallet.donationCount }}</q-item-label>
                  </div>
                </div>
              </q-item-section>
              <q-item-section side>
                <q-btn flat round dense icon="more_vert" size="sm" />
              </q-item-section>
            </q-item>
          </q-list>

          <div class="text-center q-mt-md">
            <a href="#" class="view-all-link text-blue-7 text-weight-medium" style="text-decoration: none;">View all</a>
          </div>

         
          <div v-if="activeTab === 'donations'" class="q-mt-md">
            <q-btn
              unelevated
              color="primary"
              label="Make Donation"
              icon="volunteer_activism"
              class="full-width"
              @click="$router.push('/donate')"
            />
          </div>
        </div>
      </div>

      <div class="col-12 col-md-8 col-lg-9 q-pa-md q-pa-lg-lg bg-white main-content">
        <div v-if="activeTab === 'donations' && selectedWallet" class="wallet-details">
          <div class="row items-center justify-between q-mb-lg flex-wrap">
            <h4 class="q-my-none col-12 col-sm-auto">{{ selectedWallet.name }}</h4>
            <div class="col-12 col-sm-auto q-mt-sm q-mt-sm-none">
              <q-btn flat icon="search" round />
              <q-btn flat icon="tune" round label="Filter" />
            </div>
          </div>

       
          <q-tabs
            v-model="detailTab"
            dense
            class="text-grey-7"
            active-color="blue-7"
            indicator-color="blue-7"
            align="left"
          >
            <q-tab name="donations" label="Donations Made" />
            <q-tab name="details" label="Details" />
            <q-tab name="projects" label="Supported Projects" />
            <q-tab name="recipients" label="Received by Recipient" />
          </q-tabs>

          <q-separator class="q-mb-lg" />

          <q-tab-panels v-model="detailTab" animated>
         
            <q-tab-panel name="donations">
              <div class="text-h6 q-mb-md">Donation History</div>
              
              <q-table
                :rows="donationHistory"
                :columns="donationColumns"
                row-key="id"
                flat
                :pagination="{ rowsPerPage: 10 }"
                class="transactions-table"
              >
                <template v-slot:body-cell-interval="props">
                  <q-td :props="props">
                    <q-badge
                      v-if="props.row.interval"
                      color="blue-7"
                      :label="props.row.interval"
                    />
                    <span v-else class="text-grey-6">One-time</span>
                  </q-td>
                </template>
                <template v-slot:body-cell-amount="props">
                  <q-td :props="props">
                    <span class="text-weight-medium text-positive">
                      {{ formatCurrency(props.row.amount) }}
                    </span>
                  </q-td>
                </template>
                <template v-slot:body-cell-coin="props">
                  <q-td :props="props">
                    <q-badge color="primary" :label="props.row.coin || 'BCH'" />
                  </q-td>
                </template>
                <template v-slot:body-cell-actions="props">
                  <q-td :props="props">
                    <q-btn flat round dense icon="more_vert" size="sm">
                      <q-menu>
                        <q-list style="min-width: 100px">
                          <q-item clickable v-close-popup @click="viewDonationDetails(props.row)">
                            <q-item-section>View Details</q-item-section>
                          </q-item>
                          <q-item clickable v-close-popup @click="viewReceipt(props.row)">
                            <q-item-section>View Receipt</q-item-section>
                          </q-item>
                          <q-item clickable v-close-popup @click="downloadReceipt(props.row)">
                            <q-item-section>Download Receipt</q-item-section>
                          </q-item>
                        </q-list>
                      </q-menu>
                    </q-btn>
                  </q-td>
                </template>
              </q-table>
            </q-tab-panel>

          
            <q-tab-panel name="details" class="details-panel">
              <div class="row q-col-gutter-md q-col-gutter-xl-lg">
                <div class="col-12 col-sm-6 col-lg-4">
                  <div class="detail-section">
                    <div class="detail-item q-mb-md">
                      <div class="text-caption text-grey-6 q-mb-xs">Contract Address</div>
                      <div class="text-weight-medium">{{ selectedWallet.fullNumber }}</div>
                    </div>
                    <div class="detail-item q-mb-md">
                      <div class="text-caption text-grey-6 q-mb-xs">Donor Address</div>
                      <div class="text-weight-medium">{{ selectedWallet.iban }}</div>
                    </div>
                    <div class="detail-item q-mb-md">
                      <div class="text-caption text-grey-6 q-mb-xs">Network Fee </div>
                      <div class="text-weight-medium">{{ selectedWallet.creditRate }}</div>
                    </div>
                  </div>
                </div>

               
                <div class="col-12 col-sm-6 col-lg-4">
                  <div class="detail-section">
                    <div class="detail-item q-mb-md">
                      <div class="text-caption text-grey-6 q-mb-xs">Account name</div>
                      <div class="text-weight-medium">{{ selectedWallet.accountName }}</div>
                    </div>
                    <div class="detail-item q-mb-md">
                      <div class="text-caption text-grey-6 q-mb-xs">Contract Code</div>
                      <div class="text-weight-medium">{{ selectedWallet.swift }}</div>
                    </div>
                    <div class="detail-item q-mb-md">
                      <div class="text-caption text-grey-6 q-mb-xs">Amount Balance</div>
                      <div class="text-weight-medium">{{ selectedWallet.debitRate }}</div>
                    </div>
                  </div>
                </div>

         
                <div class="col-12 col-sm-6 col-lg-4">
                  <div class="detail-section">
                    <div class="detail-item q-mb-md">
                      <div class="text-caption text-grey-6 q-mb-xs">Wallet Type</div>
                      <div class="text-weight-medium">{{ selectedWallet.product }}</div>
                    </div>
                    <div class="detail-item q-mb-md">
                      <div class="text-caption text-grey-6 q-mb-xs">Donor Name</div>
                      <div class="text-weight-medium">{{ selectedWallet.branch }}</div>
                    </div>
                    <div class="detail-item q-mb-md">
                      <div class="text-caption text-grey-6 q-mb-xs">Total Contract</div>
                      <div class="text-weight-medium">BCH-{{ selectedWallet.overdraftLimit }}</div>
                    </div>
                  </div>
                </div>
              </div>

              
              <div class="q-mt-xl">
                <div class="row items-center justify-between q-mb-md">
                  <h6 class="q-my-none">Wallet Cards</h6>
                  <q-btn flat dense icon="expand_less" />
                </div>

                <div class="row q-col-gutter-md">
                  <div v-for="card in selectedWallet.impactCards" :key="card.id" class="col-12 col-sm-6 col-md-4">
                    <q-card flat :class="['wallet-stat-card', card.colorClass]">
                      <q-card-section>
                        <div class="wallet-stat-header">{{ card.title1 }}</div>
                        <div class="wallet-stat-header">{{ card.title2 }}</div>
                        <div class="wallet-stat-content">
                          <div v-if="card.largeValue" class="wallet-stat-value-large">
                            {{ card.largeValue }}
                          </div>
                          <div v-if="card.rightIcon" class="wallet-stat-icon-right">
                            <img :src="card.rightIcon" alt="right-icon" class="wallet-stat-icon-right-img" />
                          </div>
                        </div>
                      </q-card-section>
                    </q-card>
                  </div>
                </div>
              </div>
            </q-tab-panel>

            
            <q-tab-panel name="projects">
              <div class="text-h6 q-mb-md">Projects You've Supported</div>
              
              <div class="row q-col-gutter-md">
                <div v-for="project in supportedProjects" :key="project.id" class="col-12 col-md-6 col-lg-4">
                  <q-card flat bordered class="project-card-detail">
                    <q-img :src="project.image" height="150px" />
                    <q-card-section>
                      <div class="text-h6">{{ project.name }}</div>
                      <div class="text-caption text-grey-6">{{ project.category }}</div>
                      <div class="q-mt-sm">
                        <div class="text-caption">Your contribution:</div>
                        <div class="text-h6 text-primary">{{ formatCurrency(project.donated) }} BCH</div>
                      </div>
                      <div class="q-mt-xs">
                        <div class="text-caption">Number of donations:</div>
                        <div class="text-weight-bold">{{ project.count }}</div>
                      </div>
                    </q-card-section>
                    <q-card-actions>
                      <q-btn flat color="primary" label="View Project" />
                      <q-space />
                      <q-btn flat color="primary" label="Donate Again" icon="volunteer_activism" />
                    </q-card-actions>
                  </q-card>
                </div>
              </div>
            </q-tab-panel>

            
            <q-tab-panel name="recipients">
              <div class="text-h6 q-mb-md">Donations Received by Recipients</div>
              
              <div class="row q-col-gutter-md">
                <div v-for="recipient in recipientSummary" :key="recipient.name" class="col-12 col-md-6 col-lg-4">
                  <q-card flat bordered class="recipient-card">
                    <q-card-section>
                      <div class="flex items-center q-mb-md">
                        <q-avatar size="48px" color="primary" text-color="white">
                          <q-icon name="account_balance" size="28px" />
                        </q-avatar>
                        <div class="q-ml-md flex-1" style="min-width: 0;">
                          <div class="text-subtitle1 text-weight-bold ellipsis">{{ recipient.cause }}</div>
                          <div class="text-caption text-grey-6">{{ recipient.name }}</div>
                        </div>
                      </div>
                      
                      <q-separator class="q-mb-md" />
                      
                      <div class="row q-col-gutter-sm">
                        <div class="col-6">
                          <div class="text-caption text-grey-6">Total Received</div>
                          <div class="text-h6 text-positive">{{ formatCurrency(recipient.totalAmount) }} BCH</div>
                        </div>
                        <div class="col-6">
                          <div class="text-caption text-grey-6">Donations</div>
                          <div class="text-h6">{{ recipient.count }}</div>
                        </div>
                      </div>
                      
                      <div class="q-mt-md">
                        <div class="text-caption text-grey-6 q-mb-xs">Last Donation</div>
                        <div class="text-body2">{{ recipient.lastDate }}</div>
                      </div>
                      
                      <div class="q-mt-sm">
                        <div class="text-caption text-grey-6 q-mb-xs">Status</div>
                        <q-badge 
                          :color="recipient.hasCompleted ? 'positive' : 'warning'"
                          :label="recipient.hasCompleted ? 'All Received' : 'Pending'"
                        />
                      </div>
                    </q-card-section>
                    
                    <q-card-actions>
                      <q-btn flat color="primary" label="View Details" @click="viewRecipientDetails(recipient)" />
                      <q-space />
                      <q-btn flat color="primary" icon="volunteer_activism" label="Donate Again" />
                    </q-card-actions>
                  </q-card>
                </div>
              </div>
             
              <div class="q-mt-xl">
                <div class="text-h6 q-mb-md">Recipient Statistics</div>
                <q-card flat bordered>
                  <q-card-section>
                    <div class="row q-col-gutter-md">
                      <div class="col-12 col-sm-4">
                        <div class="stat-box">
                          <q-icon name="people" size="32px" color="primary" />
                          <div class="text-caption text-grey-6 q-mt-sm">Total Recipients</div>
                          <div class="text-h5 text-weight-bold">{{ recipientSummary.length }}</div>
                        </div>
                      </div>
                      <div class="col-12 col-sm-4">
                        <div class="stat-box">
                          <q-icon name="payments" size="32px" color="positive" />
                          <div class="text-caption text-grey-6 q-mt-sm">Total Distributed</div>
                          <div class="text-h5 text-weight-bold text-positive">{{ totalDistributed }} BCH</div>
                        </div>
                      </div>
                      <div class="col-12 col-sm-4">
                        <div class="stat-box">
                          <q-icon name="trending_up" size="32px" color="blue" />
                          <div class="text-caption text-grey-6 q-mt-sm">Average per Recipient</div>
                          <div class="text-h5 text-weight-bold text-blue">{{ averagePerRecipient }} BCH</div>
                        </div>
                      </div>
                    </div>
                  </q-card-section>
                </q-card>
              </div>
            </q-tab-panel>
          </q-tab-panels>
        </div>

       
        <div v-if="activeTab === 'activity'" class="activity-view">
          <div class="row items-center justify-between q-mb-lg">
            <h4 class="q-my-none">Donation Activity</h4>
            <div>
              <q-btn flat icon="download" label="Export" />
              <q-btn flat icon="refresh" @click="refreshActivity" />
            </div>
          </div>

       
          <div class="row q-mb-md q-col-gutter-md">
            <div class="col-12 col-sm-6 col-md-3">
              <q-card flat class="stats-card">
                <q-card-section>
                  <div class="text-caption text-grey-6">Total Donations</div>
                  <div class="text-h5 text-weight-bold">{{ allDonations.length }}</div>
                </q-card-section>
              </q-card>
            </div>
            <div class="col-12 col-sm-6 col-md-3">
              <q-card flat class="stats-card bg-positive text-white">
                <q-card-section>
                  <div class="text-caption">Completed</div>
                  <div class="text-h5 text-weight-bold">{{ completedCount }}</div>
                </q-card-section>
              </q-card>
            </div>
            <div class="col-12 col-sm-6 col-md-3">
              <q-card flat class="stats-card bg-warning text-white">
                <q-card-section>
                  <div class="text-caption">Pending</div>
                  <div class="text-h5 text-weight-bold">{{ pendingCount }}</div>
                </q-card-section>
              </q-card>
            </div>
            <div class="col-12 col-sm-6 col-md-3">
              <q-card flat class="stats-card bg-info text-white">
                <q-card-section>
                  <div class="text-caption">Total Amount</div>
                  <div class="text-h5 text-weight-bold">{{ totalDonatedAmount }} BCH</div>
                </q-card-section>
              </q-card>
            </div>
          </div>

         
          <q-card flat class="q-mt-md">
            <q-card-section>
              <div class="row q-col-gutter-md q-mb-md">
                <div class="col-12 col-md-6">
                  <q-input
                    v-model="activitySearch"
                    outlined
                    dense
                    placeholder="Search donations..."
                  >
                    <template v-slot:prepend>
                      <q-icon name="search" />
                    </template>
                  </q-input>
                </div>
                <div class="col-12 col-md-3">
                  <q-select
                    v-model="statusFilter"
                    :options="['All', 'Completed', 'Pending', 'Failed']"
                    outlined
                    dense
                    label="Status"
                  />
                </div>
                <div class="col-12 col-md-3">
                  <q-select
                    v-model="categoryFilter"
                    :options="['All', 'Medical', 'Education', 'Relief', 'Environment']"
                    outlined
                    dense
                    label="Category"
                  />
                </div>
              </div>

              <q-table
                :rows="filteredActivity"
                :columns="donationColumns"
                row-key="id"
                flat
                :pagination="{ rowsPerPage: 15 }"
                class="transactions-table"
              >
                <template v-slot:body-cell-interval="props">
                  <q-td :props="props">
                    <q-badge
                      v-if="props.row.interval"
                      color="blue-7"
                      :label="props.row.interval"
                    />
                    <span v-else class="text-grey-6">One-time</span>
                  </q-td>
                </template>
                <template v-slot:body-cell-amount="props">
                  <q-td :props="props">
                    <span class="text-weight-medium text-positive">
                      {{ formatCurrency(props.row.amount) }}
                    </span>
                  </q-td>
                </template>
                <template v-slot:body-cell-coin="props">
                  <q-td :props="props">
                    <q-badge color="primary" :label="props.row.coin || 'BCH'" />
                  </q-td>
                </template>
                <template v-slot:body-cell-actions="props">
                  <q-td :props="props">
                    <q-btn flat round dense icon="visibility" size="sm" @click="viewDonationDetails(props.row)">
                      <q-tooltip>View Details</q-tooltip>
                    </q-btn>
                  </q-td>
                </template>
              </q-table>
            </q-card-section>
          </q-card>
        </div>
      </div>
    </div>
  </q-page>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useDonationStore } from '../stores/donation-store'
import { useQuasar } from 'quasar'
import bchImg from 'src/assets/bch.png'
import projectImg from 'src/assets/project.png'
import transactionImg from 'src/assets/transaction.png'

const $q = useQuasar()
const donationStore = useDonationStore()


const activeTab = ref('donations')
const detailTab = ref('donations')
const searchQuery = ref('')
const activitySearch = ref('')
const statusFilter = ref('All')
const categoryFilter = ref('All')


const wallets = ref([
  {
    id: 1,
    name: 'Personal Wallet',
    address: 'qp3wjpa3tjlj042z2wv7hahsldgwhwy0rq9sywjpyy',
    fullNumber: 'qr5agtachyxvm8pqg2z7z8z9z5z6z7z8z9zdef789',
    type: 'Paytaca',
    totalDonated: 5.75,
    donationCount: 12,
    totalFees: 0.00012,
    donorName: 'Juan Dela Cruz',
    email: 'juan@example.com',
    firstDonation: 'Jan 15, 2026',
    lastDonation: 'Mar 13, 2026',
    accountName: 'Personal Wallet',
    product: 'Paytaca',
    iban: 'qp3wjpa3tjlj042z2wv7hahsldgwhwy0rq9sywjpyy',
    swift: 'BCYPCY2N',
    branch: 'Juan Dela Cruz',
    creditRate: '1000',
    debitRate: '5.75',
    overdraftLimit: '5.75',
    impactCards: [
      {
        id: 1,
        title1: 'TOTAL',
        title2: 'DONATED',
        colorClass: 'wallet-stat-card-blue',
        largeValue: '5.75 BCH',
        rightIcon: bchImg
      },
      {
        id: 2,
        title1: 'PROJECTS',
        title2: 'SUPPORTED',
        colorClass: 'wallet-stat-card-purple',
        largeValue: '8+',
        rightIcon: projectImg
      },
      {
        id: 3,
        title1: 'TOTAL',
        title2: 'TRANSACTIONS',
        colorClass: 'wallet-stat-card-yellow',
        largeValue: '12+',
        rightIcon: transactionImg
      }
    ]
  },
  {
    id: 2,
    name: 'Business Wallet',
    address: 'qq8z6kx7qzj3zjz5qz9z5z6z7z8z9zabc123456',
    fullNumber: 'qq8z6kx7qzj3zjz5qz9z5z6z7z8z9zabc123456',
    type: 'Paytaca',
    totalDonated: 12.50,
    donationCount: 25,
    totalFees: 0.00025,
    donorName: 'ABC Corporation',
    email: 'corporate@example.com',
    firstDonation: 'Dec 1, 2025',
    lastDonation: 'Mar 12, 2026',
    accountName: 'Business Wallet',
    product: 'Paytaca',
    iban: 'qq8z6kx7qzj3zjz5qz9z5z6z7z8z9zabc123456',
    swift: 'BCYPCY2N',
    branch: 'ABC Corporation',
    creditRate: '1000',
    debitRate: '12.50',
    overdraftLimit: '12.50',
    impactCards: []
  },
  {
    id: 3,
    name: 'Family Fund',
    address: 'qr5agtachyxvm8pqg2z7z8z9z5z6z7z8z9zdef789',
    fullNumber: 'qr5agtachyxvm8pqg2z7z8z9z5z6z7z8z9zdef789',
    type: 'Paytaca',
    totalDonated: 3.25,
    donationCount: 8,
    totalFees: 0.00008,
    donorName: 'Dela Cruz Family',
    email: 'family@example.com',
    firstDonation: 'Feb 10, 2026',
    lastDonation: 'Mar 11, 2026',
    accountName: 'Family Fund',
    product: 'Paytaca',
    iban: 'qr5agtachyxvm8pqg2z7z8z9z5z6z7z8z9zdef789',
    swift: 'BCYPCY2N',
    branch: 'Dela Cruz Family',
    creditRate: '1000',
    debitRate: '3.25',
    overdraftLimit: '3.25',
    impactCards: []
  }
])

const selectedWallet = ref(wallets.value[0])

const donationColumns = [
  { name: 'date', label: 'Date', field: row => formatDate(row.timestamp), align: 'left', sortable: true },
  { name: 'recipient', label: 'Recipient', field: 'recipient', align: 'left' },
  { name: 'donor', label: 'Donor Name', field: 'donor_name', align: 'left' },
  { name: 'amount', label: 'Amount', field: 'amount', align: 'right', sortable: true },
  { name: 'interval', label: 'Interval', field: 'interval', align: 'center' },
  { name: 'coin', label: 'Coin', field: 'coin', align: 'center' },
  { name: 'actions', label: 'Actions', field: 'actions', align: 'center' }
]


const sampleDonations = [
  {
    id: 1,
    txid: 'sample_tx_001',
    recipient: 'Typhoon Relief Fund',
    donor_name: 'John Doe',
    amount: '0.50',
    coin: 'BCH',
    cause: 'Disaster Relief',
    interval: 'One-time',
    timestamp: '2026-03-15T10:30:00Z',
    message: 'Hope this helps!'
  },
  {
    id: 2,
    txid: 'sample_tx_002',
    recipient: 'Medical Emergency Fund',
    donor_name: 'Maria Santos',
    amount: '1.25',
    coin: 'BCH',
    cause: 'Healthcare',
    interval: 'Monthly',
    timestamp: '2026-03-14T14:20:00Z',
    message: 'Supporting healthcare'
  },
  {
    id: 3,
    txid: 'sample_tx_003',
    recipient: 'Education Scholarship',
    donor_name: 'Anonymous',
    amount: '0.75',
    coin: 'BCH',
    cause: 'Education',
    interval: 'Quarterly',
    timestamp: '2026-03-10T09:15:00Z',
    message: ''
  }
]


const donationHistory = computed(() => {
  const realDonations = donationStore.donationHistory || []
  return realDonations.length > 0 ? realDonations : sampleDonations
})


const allDonations = computed(() => {
  const realDonations = donationStore.donationHistory || []
  return realDonations.length > 0 ? realDonations : sampleDonations
})


const updateWalletStats = () => {
  if (donationHistory.value && donationHistory.value.length > 0) {
    const total = donationHistory.value.reduce((sum, d) => sum + parseFloat(d.amount || 0), 0)
    const count = donationHistory.value.length
    
  
    selectedWallet.value.totalDonated = total
    selectedWallet.value.donationCount = count
    selectedWallet.value.debitRate = total.toFixed(4)
    selectedWallet.value.overdraftLimit = total.toFixed(4)
    

    if (selectedWallet.value.impactCards && selectedWallet.value.impactCards.length > 0) {
      selectedWallet.value.impactCards[0].largeValue = `${total.toFixed(4)} BCH`
      selectedWallet.value.impactCards[2].largeValue = `${count}+`
    }
  }
}


watch(() => donationStore.donationHistory, () => {
  updateWalletStats()
}, { immediate: true, deep: true })


const supportedProjects = ref([
  {
    id: 1,
    name: 'Medical Fund',
    category: 'Healthcare',
    image: new URL('../assets/medical.jpg', import.meta.url).href,
    donated: 3.10,
    count: 5
  },
  {
    id: 2,
    name: 'Education Fund',
    category: 'Education',
    image: new URL('../assets/typhoon.jpeg', import.meta.url).href,
    donated: 2.75,
    count: 3
  },
  {
    id: 3,
    name: 'Typhoon Relief',
    category: 'Disaster Relief',
    image: new URL('../assets/typhoon.jpeg', import.meta.url).href,
    donated: 0.95,
    count: 2
  }
])


const completedCount = computed(() => allDonations.value.length)
const pendingCount = computed(() => 0)
const totalDonatedAmount = computed(() => {
  const total = allDonations.value.reduce((sum, d) => sum + parseFloat(d.amount || 0), 0)
  return total.toFixed(4)
})


const recipientSummary = computed(() => {
  const recipientMap = {}
  donationHistory.value.forEach(donation => {
    const recipientName = donation.recipient || 'Unknown'
    if (!recipientMap[recipientName]) {
      recipientMap[recipientName] = {
        name: recipientName,
        cause: donation.cause || 'General',
        totalAmount: 0,
        count: 0,
        lastDate: donation.timestamp || donation.date,
        hasCompleted: true,
        donations: []
      }
    }
    
    recipientMap[recipientName].totalAmount += parseFloat(donation.amount || 0)
    recipientMap[recipientName].count++
    recipientMap[recipientName].donations.push(donation)
    
    
    if (donation.status === 'pending') {
      recipientMap[recipientName].hasCompleted = false
    }
    
    const donationDate = donation.timestamp || donation.date
    if (donationDate > recipientMap[recipientName].lastDate) {
      recipientMap[recipientName].lastDate = donationDate
    }
  })
  
  return Object.values(recipientMap).sort((a, b) => b.totalAmount - a.totalAmount)
})

const totalDistributed = computed(() => {
  const total = recipientSummary.value.reduce((sum, r) => sum + r.totalAmount, 0)
  return total.toFixed(2)
})

const averagePerRecipient = computed(() => {
  if (recipientSummary.value.length === 0) return '0.00'
  const avg = parseFloat(totalDistributed.value) / recipientSummary.value.length
  return avg.toFixed(2)
})

const filteredActivity = computed(() => {
  let filtered = [...allDonations.value]
  
  
  if (categoryFilter.value !== 'All') {
    filtered = filtered.filter(d => 
      d.cause && d.cause.toLowerCase().includes(categoryFilter.value.toLowerCase())
    )
  }
  
 
  if (activitySearch.value) {
    const search = activitySearch.value.toLowerCase()
    filtered = filtered.filter(d => 
      (d.cause && d.cause.toLowerCase().includes(search)) ||
      (d.donor_name && d.donor_name.toLowerCase().includes(search)) ||
      (d.donor_email && d.donor_email.toLowerCase().includes(search)) ||
      (d.txid && d.txid.toLowerCase().includes(search)) ||
      (d.interval && d.interval.toLowerCase().includes(search))
    )
  }
  
  return filtered
})


const selectWallet = (wallet) => {
  selectedWallet.value = wallet
  detailTab.value = 'donations'
}

const formatCurrency = (amount) => {
  const num = parseFloat(amount) || 0
  return num.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 8 })
}

const formatDate = (timestamp) => {
  if (!timestamp) return 'N/A'
  const date = new Date(timestamp)
  return date.toLocaleDateString('en-US', { 
    year: 'numeric', 
    month: 'short', 
    day: 'numeric'
  })
}

const viewDonationDetails = (donation) => {
  const donationDate = formatDate(donation.timestamp || donation.date)
  const formattedAmount = formatCurrency(donation.amount)
  
  $q.dialog({
    title: '',
    message: `
      <div style="max-width: 550px; margin: 0 auto; font-family: 'Roboto', sans-serif;">
        <!-- Header -->
        <div style="padding: 20px 24px; background: white; border-bottom: 1px solid #e0e0e0; margin: -16px -16px 0 -16px;">
          <div style="font-size: 20px; font-weight: 600; color: #212121; margin-bottom: 4px;">Donation Details</div>
          <div style="font-size: 13px; color: #757575;">BiToHelp Blockchain Donation Platform</div>
        </div>
        
        <!-- Content -->
        <div style="padding: 24px; background: white;">
          <!-- Details Table -->
          <div style="border: 1px solid #e0e0e0; border-radius: 8px; overflow: hidden;">
            <table style="width: 100%; border-collapse: collapse;">
              <tr style="background: #fafafa; border-bottom: 1px solid #e0e0e0;">
                <td style="padding: 14px 16px; font-size: 13px; color: #757575; font-weight: 500; width: 40%;">Date</td>
                <td style="padding: 14px 16px; font-size: 14px; color: #212121; font-weight: 500; text-align: right;">${donationDate}</td>
              </tr>
              <tr style="border-bottom: 1px solid #e0e0e0;">
                <td style="padding: 14px 16px; font-size: 13px; color: #757575; font-weight: 500;">Cause / Nonprofit</td>
                <td style="padding: 14px 16px; font-size: 14px; color: #212121; font-weight: 500; text-align: right;">${donation.cause || 'N/A'}</td>
              </tr>
              <tr style="border-bottom: 1px solid #e0e0e0;">
                <td style="padding: 14px 16px; font-size: 13px; color: #757575; font-weight: 500;">Donor Name</td>
                <td style="padding: 14px 16px; font-size: 14px; color: #212121; font-weight: 500; text-align: right;">${donation.donor_name || 'Anonymous'}</td>
              </tr>
              <tr style="border-bottom: 1px solid #e0e0e0;">
                <td style="padding: 14px 16px; font-size: 13px; color: #757575; font-weight: 500;">Donor Email</td>
                <td style="padding: 14px 16px; font-size: 14px; color: #212121; font-weight: 500; text-align: right;">${donation.donor_email || 'N/A'}</td>
              </tr>
              <tr style="border-bottom: 1px solid #e0e0e0;">
                <td style="padding: 14px 16px; font-size: 13px; color: #757575; font-weight: 500;">Interval</td>
                <td style="padding: 14px 16px; font-size: 14px; color: #212121; font-weight: 500; text-align: right;">${donation.interval || 'One-time'}</td>
              </tr>
              <tr style="border-bottom: 1px solid #e0e0e0;">
                <td style="padding: 14px 16px; font-size: 13px; color: #757575; font-weight: 500;">Message</td>
                <td style="padding: 14px 16px; font-size: 14px; color: #212121; font-weight: 500; text-align: right;">${donation.message || 'No message'}</td>
              </tr>
              <tr style="border-bottom: 1px solid #e0e0e0;">
                <td style="padding: 14px 16px; font-size: 13px; color: #757575; font-weight: 500;">Transaction ID</td>
                <td style="padding: 14px 16px; font-size: 12px; color: #212121; font-weight: 400; text-align: right; word-break: break-all;">${donation.txid || 'N/A'}</td>
              </tr>
              <tr style="background: #f5f5f5;">
                <td style="padding: 18px 16px; font-size: 14px; color: #424242; font-weight: 600;">Donation Amount</td>
                <td style="padding: 18px 16px; font-size: 18px; color: #1976d2; font-weight: 700; text-align: right;">${formattedAmount} ${donation.coin || 'BCH'}</td>
              </tr>
            </table>
          </div>
          
          <!-- Footer Note -->
          <div style="margin-top: 20px; padding: 12px 16px; background: #f5f5f5; border-left: 3px solid #1976d2; border-radius: 4px;">
            <div style="color: #424242; font-size: 12px; line-height: 1.6;">
              <strong>Note:</strong> This transaction is recorded on the Bitcoin Cash blockchain. For receipt or tax purposes, use the 'View Receipt' option.
            </div>
          </div>
        </div>
      </div>
    `,
    html: true,
    ok: {
      label: 'Close',
      color: 'primary',
      flat: false,
      unelevated: true,
      noCaps: true
    },
    cancel: {
      label: 'View Receipt',
      color: 'primary',
      flat: true,
      noCaps: true
    }
  }).onCancel(() => {
    viewReceipt(donation)
  })
}

const viewReceipt = (donation) => {
  try {
    const receiptDate = new Date(donation.date).toLocaleDateString('en-US', { 
      year: 'numeric', 
      month: 'long', 
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    })
    
    const currentDate = new Date().toLocaleDateString('en-US', { 
      year: 'numeric', 
      month: 'long', 
      day: 'numeric' 
    })
    
    const mockTxId = `BTHLP-${Date.now().toString().slice(-10)}`
    const walletInfo = selectedWallet.value
    const formattedAmount = formatCurrency(donation.amount)
    const statusBadgeColor = donation.status === 'completed' ? '#4caf50' : '#ff9800'
    
    const receiptHTML = `
      <div style="max-width: 700px; margin: 0 auto; font-family: 'Roboto', sans-serif; background: white;">
        <!-- Letterhead -->
        <div style="background: white; padding: 32px 32px 24px; text-align: center; border-bottom: 2px solid #e0e0e0; margin: -16px -16px 0 -16px;">
          <div style="font-size: 32px; font-weight: 700; color: #212121; letter-spacing: 0.5px; margin-bottom: 6px;">BiToHelp</div>
          <div style="font-size: 13px; color: #757575; font-weight: 400; margin-bottom: 4px;">Blockchain-Powered Charitable Giving</div>
          <div style="font-size: 12px; color: #9e9e9e;">Building a Better Tomorrow, One Transaction at a Time</div>
        </div>
        
        <!-- Receipt Title -->
        <div style="background: #fafafa; padding: 20px 32px; border-bottom: 1px solid #e0e0e0;">
          <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 12px;">
            <div>
              <h2 style="margin: 0; color: #212121; font-size: 22px; font-weight: 600;">Official Donation Receipt</h2>
              <p style="margin: 6px 0 0 0; color: #757575; font-size: 13px;">Tax-Deductible Donation Record</p>
            </div>
            <div style="text-align: right;">
              <div style="background: ${statusBadgeColor}; color: white; padding: 6px 14px; border-radius: 4px; font-size: 12px; font-weight: 600; text-transform: uppercase; display: inline-block;">
                ${donation.status}
              </div>
            </div>
          </div>
        </div>
        
        <!-- Receipt Details -->
        <div style="padding: 32px;">
          <!-- Receipt Info Bar -->
          <div style="background: #f5f5f5; padding: 18px 20px; border-radius: 8px; margin-bottom: 28px; border: 1px solid #e0e0e0;">
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px;">
              <div>
                <div style="color: #757575; font-size: 11px; font-weight: 600; text-transform: uppercase; letter-spacing: 0.3px; margin-bottom: 6px;">Receipt Number</div>
                <div style="color: #212121; font-size: 15px; font-weight: 600; font-family: monospace;">${mockTxId}</div>
              </div>
              <div style="text-align: right;">
                <div style="color: #757575; font-size: 11px; font-weight: 600; text-transform: uppercase; letter-spacing: 0.3px; margin-bottom: 6px;">Issue Date</div>
                <div style="color: #212121; font-size: 14px; font-weight: 600;">${currentDate}</div>
              </div>
            </div>
          </div>
          
          <!-- Donor Information -->
          <div style="margin-bottom: 28px;">
            <h3 style="color: #424242; font-size: 15px; font-weight: 600; margin: 0 0 14px 0; text-transform: uppercase; letter-spacing: 0.3px; border-bottom: 2px solid #e0e0e0; padding-bottom: 10px;">Donor Information</h3>
            <table style="width: 100%; border-collapse: collapse;">
              <tr>
                <td style="padding: 12px 0; color: #757575; font-size: 13px; font-weight: 500; width: 35%;">Full Name:</td>
                <td style="padding: 12px 0; color: #212121; font-size: 14px; font-weight: 500;">${walletInfo.donorName}</td>
              </tr>
              <tr style="border-top: 1px solid #eeeeee;">
                <td style="padding: 12px 0; color: #757575; font-size: 13px; font-weight: 500;">Email Address:</td>
                <td style="padding: 12px 0; color: #212121; font-size: 14px; font-weight: 500;">${walletInfo.email}</td>
              </tr>
              <tr style="border-top: 1px solid #eeeeee;">
                <td style="padding: 12px 0; color: #757575; font-size: 13px; font-weight: 500;">BCH Wallet:</td>
                <td style="padding: 12px 0; color: #212121; font-size: 11px; font-weight: 500; font-family: monospace; word-break: break-all;">${walletInfo.address}</td>
              </tr>
            </table>
          </div>
          
          <!-- Donation Information -->
          <div style="margin-bottom: 28px;">
            <h3 style="color: #424242; font-size: 15px; font-weight: 600; margin: 0 0 14px 0; text-transform: uppercase; letter-spacing: 0.3px; border-bottom: 2px solid #e0e0e0; padding-bottom: 10px;">Donation Details</h3>
            <table style="width: 100%; border-collapse: collapse;">
              <tr>
                <td style="padding: 12px 0; color: #757575; font-size: 13px; font-weight: 500; width: 35%;">Transaction Date:</td>
                <td style="padding: 12px 0; color: #212121; font-size: 14px; font-weight: 500;">${receiptDate}</td>
              </tr>
              <tr style="border-top: 1px solid #eeeeee;">
                <td style="padding: 12px 0; color: #757575; font-size: 13px; font-weight: 500;">Recipient Organization:</td>
                <td style="padding: 12px 0; color: #212121; font-size: 14px; font-weight: 500;">${donation.recipient}</td>
              </tr>
              <tr style="border-top: 1px solid #eeeeee;">
                <td style="padding: 12px 0; color: #757575; font-size: 13px; font-weight: 500;">Cause Category:</td>
                <td style="padding: 12px 0; color: #212121; font-size: 14px; font-weight: 500;">${donation.cause}</td>
              </tr>
              <tr style="border-top: 1px solid #eeeeee;">
                <td style="padding: 12px 0; color: #757575; font-size: 13px; font-weight: 500;">Payment Method:</td>
                <td style="padding: 12px 0; color: #212121; font-size: 14px; font-weight: 500;">Bitcoin Cash (BCH)</td>
              </tr>
            </table>
          </div>
          
          <!-- Amount Section -->
          <div style="background: #fafafa; padding: 24px; border-radius: 8px; margin: 28px 0; border: 2px solid #e0e0e0;">
            <div style="text-align: center;">
              <div style="color: #757575; font-size: 13px; font-weight: 600; text-transform: uppercase; letter-spacing: 0.3px; margin-bottom: 10px;">Total Donation Amount</div>
              <div style="color: #1976d2; font-size: 36px; font-weight: 700; line-height: 1;">${formattedAmount} BCH</div>
            </div>
          </div>
          
          <!-- Tax Information -->
          <div style="background: #f5f5f5; border: 1px solid #e0e0e0; border-radius: 8px; padding: 18px 20px; margin-bottom: 24px; border-left: 3px solid #1976d2;">
            <div>
              <h4 style="margin: 0 0 8px 0; color: #424242; font-size: 14px; font-weight: 600;">Tax Deduction Notice</h4>
              <p style="margin: 0; color: #616161; font-size: 13px; line-height: 1.6;">
                This receipt serves as official documentation for tax purposes. Please consult with your tax advisor regarding the deductibility of this donation in your jurisdiction. BiToHelp is a registered charitable platform facilitating cryptocurrency donations.
              </p>
            </div>
          </div>
          
          <!-- Footer -->
          <div style="text-align: center; padding-top: 24px; border-top: 2px solid #e0e0e0;">
            <div style="color: #424242; font-size: 18px; font-weight: 600; margin-bottom: 10px;">Thank You for Your Generosity!</div>
            <p style="color: #757575; font-size: 13px; line-height: 1.7; margin: 10px 0;">
              Your contribution makes a real difference in people's lives. Together, we're building<br/>
              a more transparent and efficient charitable giving ecosystem powered by blockchain technology.
            </p>
            <div style="margin-top: 20px; padding-top: 20px; border-top: 1px solid #e0e0e0;">
              <p style="color: #9e9e9e; font-size: 11px; margin: 5px 0; line-height: 1.6;">
                BiToHelp - Cryptocurrency Donation Platform<br/>
                This is a computer-generated receipt and is valid without signature.<br/>
                For inquiries, please contact support@bitohelp.org
              </p>
            </div>
          </div>
        </div>
      </div>
    `
    
    $q.dialog({
      title: '',
      message: receiptHTML,
      html: true,
      ok: {
        label: 'Close',
        color: 'grey-7',
        flat: true,
        noCaps: true
      },
      cancel: {
        label: 'Download Receipt',
        color: 'primary',
        unelevated: true,
        noCaps: true
      }
    }).onCancel(() => {
      downloadReceipt(donation)
    })
  } catch (error) {
    console.error('Error in viewReceipt:', error)
    $q.notify({
      type: 'negative',
      message: 'Error viewing receipt',
      caption: error.message,
      position: 'top'
    })
  }
}

const downloadReceipt = (donation) => {
  try {
    const receiptDate = new Date(donation.date).toLocaleDateString('en-US', { 
      year: 'numeric', 
      month: 'long', 
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    })
    
    const currentDate = new Date().toLocaleDateString('en-US', { 
      year: 'numeric', 
      month: 'long', 
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    })
    
    const mockTxId = `BTHLP-${Date.now().toString().slice(-10)}`
    const walletInfo = selectedWallet.value
    const formattedAmount = formatCurrency(donation.amount)
    
    
    const receiptContent = `
╔════════════════════════════════════════════════════════════════════════════╗
║                                                                            ║
║                              B i T o H e l p                               ║
║                   Blockchain-Powered Charitable Giving                     ║
║            Building a Better Tomorrow, One Transaction at a Time           ║
║                                                                            ║
╚════════════════════════════════════════════════════════════════════════════╝


                          OFFICIAL DONATION RECEIPT
                        Tax-Deductible Donation Record
                                                                              

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

 RECEIPT INFORMATION

 Receipt Number:      ${mockTxId}
 Issue Date:          ${currentDate}
 Transaction Status:  ${donation.status.toUpperCase()}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

 DONOR INFORMATION

 Full Name:           ${walletInfo.donorName}
 Email Address:       ${walletInfo.email}
 BCH Wallet Address:  ${walletInfo.address}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

 DONATION DETAILS

 Transaction Date:         ${receiptDate}
 Recipient Organization:   ${donation.recipient}
 Cause Category:           ${donation.cause}
 Payment Method:           Bitcoin Cash (BCH)
 
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

                            DONATION AMOUNT

                        ${formattedAmount} BCH

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

 TAX INFORMATION

 This receipt serves as official documentation for tax purposes. Please
 consult with your tax advisor regarding the deductibility of this donation
 in your jurisdiction. BiToHelp is a registered charitable platform 
 facilitating cryptocurrency donations to verified non-profit organizations.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

                       THANK YOU FOR YOUR GENEROSITY!

 Your contribution makes a real difference in people's lives. Together, we're
 building a more transparent and efficient charitable giving ecosystem powered
 by blockchain technology.

 This transaction has been recorded on the Bitcoin Cash blockchain, ensuring
 permanent transparency and accountability.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

                              BiToHelp Platform
                    Cryptocurrency Donation Platform
          This is a computer-generated receipt and is valid without signature
                 For inquiries: support@bitohelp.org

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    `
    
   
    const blob = new Blob([receiptContent], { type: 'text/plain;charset=utf-8' })
    const url = window.URL.createObjectURL(blob)
    const link = document.createElement('a')
    link.href = url
    link.download = `BiToHelp_Receipt_${mockTxId}.txt`
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
    window.URL.revokeObjectURL(url)
    
    $q.notify({
      type: 'positive',
      message: 'Receipt downloaded successfully!',
      caption: `Saved as BiToHelp_Receipt_${mockTxId}.txt`,
      position: 'top',
      timeout: 3000,
      icon: 'download',
      actions: [
        {
          label: 'OK',
          color: 'white'
        }
      ]
    })
  } catch (error) {
    console.error('Error in downloadReceipt:', error)
    $q.notify({
      type: 'negative',
      message: 'Error downloading receipt',
      caption: error.message,
      position: 'top',
      icon: 'error'
    })
  }
}

const refreshActivity = () => {
  $q.notify({
    type: 'info',
    message: 'Refreshing activity...',
    position: 'top',
    timeout: 1000
  })
  setTimeout(() => {
    $q.notify({
      type: 'positive',
      message: 'Activity updated',
      position: 'top',
      timeout: 1500
    })
  }, 1000)
}

const viewRecipientDetails = (recipient) => {
  const donationsList = recipient.donations
    .map(d => `<li>${d.date}: ${d.amount} BCH (${d.status})</li>`)
    .join('')
  
  $q.dialog({
    title: `${recipient.name} - Donation Details`,
    message: `
      <div style="text-align: left;">
        <p><strong>Cause:</strong> ${recipient.cause}</p>
        <p><strong>Total Received:</strong> ${formatCurrency(recipient.totalAmount)} BCH</p>
        <p><strong>Number of Donations:</strong> ${recipient.count}</p>
        <p><strong>Last Donation:</strong> ${recipient.lastDate}</p>
        <br>
        <p><strong>Donation History:</strong></p>
        <ul style="margin-top: 8px;">${donationsList}</ul>
      </div>
    `,
    html: true,
    ok: {
      label: 'Close',
      color: 'primary'
    }
  })
}

onMounted(async () => {
  await donationStore.fetchDonations(50)
  console.log('DonorPage mounted')
})
</script>

<style scoped lang="scss">
.donor-page {
  overflow-x: hidden;
}

.sidebar-container {
  background-color: #8e8b8b2d;

}

.accounts-sidebar {
  border-radius: 8px;
  padding: 1rem;

  h5 {
    font-size: 1.5rem;
    line-height: 1.3;
    
    strong {
      font-weight: 700;
    }
  }
}

.account-item {
  background-color: rgba(85, 139, 220, 0.4);
  transition: all 0.3s ease;
  
  &:hover {
    background-color: rgba(255, 255, 255, 0.9);
  }
}

.details-panel {
  background-color: #aba7a73a;
  border-radius: 8px;
  border: inset 1px rgba(255, 255, 255, 0.5);
  padding: 1rem;
}

.detail-section {
  .detail-item {
    padding: 0.5rem 0;
  }
}


.wallet-stat-card {
  border-radius: 20px;
  padding: 10px;
  color: white;
  transition: all 0.2s ease;
  
  &:hover {
    transform: translateY(-5px);
    box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
  }
}

.wallet-stat-card-blue {
  background: linear-gradient(135deg, #6c85f5dc 0%, #8799f3 100%);
  border: 4px solid #fffdf9;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.5);
}

.wallet-stat-card-purple {
  background: linear-gradient(135deg, #a9a4ffd3 0%, #7e7affd0 100%);
  border: 4px solid #fffdf9;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.5);
}

.wallet-stat-card-yellow {
  background: linear-gradient(135deg, #e3d273d9 0%, #ebcf89e2 100%);
  border: 4px solid #fffdf9;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.5);
}

.wallet-stat-header {
  font-size: 24px;
  font-weight: bold;
  line-height: 1.2;
}

.wallet-stat-content {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-top: 15px;
  flex-wrap: wrap;
}

.wallet-stat-icon {
  background: rgba(255, 255, 255, 0.2);
  border-radius: 50%;
  padding: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.wallet-stat-icon-img {
  width: 60px;
  height: 60px;
  object-fit: contain;
}

.wallet-stat-value {
  font-size: 24px;
  font-weight: bold;
  font-style: italic;
}

.wallet-stat-value-large {
  font-size: 36px;
  font-weight: bold;
}

.wallet-stat-badge {
  background: #ffb84d;
  border-radius: 15px;
  padding: 10px 15px;
  text-align: center;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.wallet-stat-badge-img {
  width: 36px;
  height: 36px;
  object-fit: contain;
}

.wallet-badge-text {
  font-size: 12px;
  font-weight: bold;
  margin-top: 5px;
}

.wallet-stat-icon-right {
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
}

.wallet-stat-icon-right-img {
  width: 100px;
  height: 100px;
  object-fit: contain;
}


.stats-card {
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}


.project-card-detail {
  border-radius: 12px;
  overflow: hidden;
  transition: all 0.3s ease;
  
  &:hover {
    transform: translateX(-5px);
    box-shadow: 0 8px 16px rgba(14, 63, 221, 0.15);
    border-color: #8799f3;
  }
}



@property --angle {
  syntax: "<angle>";
  initial-value: 0deg;
  inherits: false;
}

.recipient-card {
  --angle: 0deg;
  background: #d1d2d485;
  border-radius: 4px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.9);
  backdrop-filter: blur(9px);
  transition: all 0.3s ease;
}

.recipient-card:hover {
  transform: scale(1.05); 
  box-shadow: 0 8px 16px rgba(211, 37, 37, 0.1);
  border: 8px solid transparent;
  border-image: conic-gradient(
    from var(--angle),
    #150ae5, #ffea01,
    #02f791, #f20404
  ) 1;

  animation: border-rotate 4s linear infinite;
}

@keyframes border-rotate {
  to {
    --angle: 360deg;
  }
}
.stat-box {
  text-align: center;
  padding: 16px;
  border-radius: 8px;
  background: #f8f9fa;
  transition: all 0.3s ease;
  
  &:hover {
    background: #e9ecef;
  }
}


:deep(.q-btn-toggle) {
  border-radius: 4px;
  overflow: hidden;
}

:deep(.q-tab) {
  font-weight: 500;
}


.transactions-table {
  :deep(.q-table__card) {
    box-shadow: none;
  }
  
  :deep(tbody tr:hover) {
    background-color: rgba(0, 0, 0, 0.02);
  }
}


@media (max-width: 1024px) {
  .sidebar-container {
    padding-bottom: 2rem;
  }
}

@media (max-width: 768px) {
  .accounts-sidebar h5 {
    font-size: 1.2rem;
  }
  
  .account-item {
    margin-bottom: 0.5rem;
  }
}
</style>

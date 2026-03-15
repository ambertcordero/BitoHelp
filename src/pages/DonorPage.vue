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
                <q-item-label caption>{{ wallet.address.substring(0, 20) }}...</q-item-label>
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
                <template v-slot:body-cell-status="props">
                  <q-td :props="props">
                    <q-badge
                      :color="props.row.status === 'completed' ? 'positive' : props.row.status === 'pending' ? 'warning' : 'negative'"
                      :label="props.row.status"
                    />
                  </q-td>
                </template>
                <template v-slot:body-cell-amount="props">
                  <q-td :props="props">
                    <span class="text-weight-medium text-negative">
                      -{{ formatCurrency(props.row.amount) }} BCH
                    </span>
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
                          <q-item clickable v-close-popup>
                            <q-item-section>View Receipt</q-item-section>
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
                      <div class="text-caption text-grey-6 q-mb-xs">Wallet Address</div>
                      <div class="text-weight-medium">{{ selectedWallet.address }}</div>
                    </div>
                    <div class="detail-item q-mb-md">
                      <div class="text-caption text-grey-6 q-mb-xs">Wallet Type</div>
                      <div class="text-weight-medium">{{ selectedWallet.type }}</div>
                    </div>
                    <div class="detail-item q-mb-md">
                      <div class="text-caption text-grey-6 q-mb-xs">Network Fee Paid</div>
                      <div class="text-weight-medium">{{ selectedWallet.totalFees }} BCH</div>
                    </div>
                  </div>
                </div>

                <div class="col-12 col-sm-6 col-lg-4">
                  <div class="detail-section">
                    <div class="detail-item q-mb-md">
                      <div class="text-caption text-grey-6 q-mb-xs">Donor Name</div>
                      <div class="text-weight-medium">{{ selectedWallet.donorName }}</div>
                    </div>
                    <div class="detail-item q-mb-md">
                      <div class="text-caption text-grey-6 q-mb-xs">Email</div>
                      <div class="text-weight-medium">{{ selectedWallet.email }}</div>
                    </div>
                    <div class="detail-item q-mb-md">
                      <div class="text-caption text-grey-6 q-mb-xs">Total Donated</div>
                      <div class="text-weight-medium">{{ formatCurrency(selectedWallet.totalDonated) }} BCH</div>
                    </div>
                  </div>
                </div>

                <div class="col-12 col-sm-6 col-lg-4">
                  <div class="detail-section">
                    <div class="detail-item q-mb-md">
                      <div class="text-caption text-grey-6 q-mb-xs">First Donation</div>
                      <div class="text-weight-medium">{{ selectedWallet.firstDonation }}</div>
                    </div>
                    <div class="detail-item q-mb-md">
                      <div class="text-caption text-grey-6 q-mb-xs">Last Donation</div>
                      <div class="text-weight-medium">{{ selectedWallet.lastDonation }}</div>
                    </div>
                    <div class="detail-item q-mb-md">
                      <div class="text-caption text-grey-6 q-mb-xs">Total Transactions</div>
                      <div class="text-weight-medium">{{ selectedWallet.donationCount }}</div>
                    </div>
                  </div>
                </div>
              </div>

              
              <div class="q-mt-xl">
                <div class="row items-center justify-between q-mb-md">
                  <h6 class="q-my-none">Your Impact</h6>
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
                        <div class="q-ml-md">
                          <div class="text-h6">{{ recipient.name }}</div>
                          <div class="text-caption text-grey-6">{{ recipient.cause }}</div>
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
                <template v-slot:body-cell-status="props">
                  <q-td :props="props">
                    <q-badge
                      :color="props.row.status === 'completed' ? 'positive' : props.row.status === 'pending' ? 'warning' : 'negative'"
                      :label="props.row.status"
                    />
                  </q-td>
                </template>
                <template v-slot:body-cell-amount="props">
                  <q-td :props="props">
                    <span class="text-weight-medium text-negative">
                      -{{ formatCurrency(props.row.amount) }} BCH
                    </span>
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
import { ref, computed, onMounted } from 'vue'
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
    type: 'Paytaca',
    totalDonated: 5.75,
    donationCount: 12,
    totalFees: 0.00012,
    donorName: 'Juan Dela Cruz',
    email: 'juan@example.com',
    firstDonation: 'Jan 15, 2026',
    lastDonation: 'Mar 13, 2026',
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
    type: 'Paytaca',
    totalDonated: 12.50,
    donationCount: 25,
    totalFees: 0.00025,
    donorName: 'ABC Corporation',
    email: 'corporate@example.com',
    firstDonation: 'Dec 1, 2025',
    lastDonation: 'Mar 12, 2026',
    impactCards: []
  },
  {
    id: 3,
    name: 'Family Fund',
    address: 'qr5agtachyxvm8pqg2z7z8z9z5z6z7z8z9zdef789',
    type: 'Paytaca',
    totalDonated: 3.25,
    donationCount: 8,
    totalFees: 0.00008,
    donorName: 'Dela Cruz Family',
    email: 'family@example.com',
    firstDonation: 'Feb 10, 2026',
    lastDonation: 'Mar 11, 2026',
    impactCards: []
  }
])

const selectedWallet = ref(wallets.value[0])


const donationColumns = [
  { name: 'date', label: 'Date', field: 'date', align: 'left', sortable: true },
  { name: 'recipient', label: 'Recipient', field: 'recipient', align: 'left' },
  { name: 'cause', label: 'Cause', field: 'cause', align: 'left' },
  { name: 'amount', label: 'Amount', field: 'amount', align: 'right', sortable: true },
  { name: 'status', label: 'Status', field: 'status', align: 'center' },
  { name: 'actions', label: 'Actions', field: 'actions', align: 'center' }
]


const donationHistory = ref([
  { id: 1, date: '2026-03-13', recipient: 'Medical Fund', cause: 'Healthcare', amount: 0.75, status: 'completed' },
  { id: 2, date: '2026-03-12', recipient: 'Education Fund', cause: 'Education', amount: 1.2, status: 'completed' },
  { id: 3, date: '2026-03-11', recipient: 'Typhoon Relief', cause: 'Relief', amount: 0.5, status: 'completed' },
  { id: 4, date: '2026-03-10', recipient: 'Medical Fund', cause: 'Healthcare', amount: 0.85, status: 'completed' },
  { id: 5, date: '2026-03-09', recipient: 'Environment Fund', cause: 'Environment', amount: 0.35, status: 'completed' },
  { id: 6, date: '2026-03-08', recipient: 'Education Fund', cause: 'Education', amount: 1.0, status: 'completed' },
  { id: 7, date: '2026-03-07', recipient: 'Medical Fund', cause: 'Healthcare', amount: 0.6, status: 'completed' },
  { id: 8, date: '2026-03-06', recipient: 'Relief Fund', cause: 'Relief', amount: 0.45, status: 'pending' },
])

const allDonations = ref([
  { id: 1, date: '2026-03-13', recipient: 'Medical Fund', cause: 'Healthcare', amount: 0.75, status: 'completed' },
  { id: 2, date: '2026-03-12', recipient: 'Education Fund', cause: 'Education', amount: 1.2, status: 'completed' },
  { id: 3, date: '2026-03-11', recipient: 'Typhoon Relief', cause: 'Relief', amount: 0.5, status: 'completed' },
  { id: 4, date: '2026-03-10', recipient: 'Medical Fund', cause: 'Healthcare', amount: 0.85, status: 'completed' },
  { id: 5, date: '2026-03-09', recipient: 'Environment Fund', cause: 'Environment', amount: 0.35, status: 'completed' },
  { id: 6, date: '2026-03-08', recipient: 'Education Fund', cause: 'Education', amount: 1.0, status: 'completed' },
  { id: 7, date: '2026-03-07', recipient: 'Medical Fund', cause: 'Healthcare', amount: 0.6, status: 'completed' },
  { id: 8, date: '2026-03-06', recipient: 'Relief Fund', cause: 'Relief', amount: 0.45, status: 'pending' },
  { id: 9, date: '2026-03-05', recipient: 'Medical Fund', cause: 'Healthcare', amount: 0.9, status: 'completed' },
  { id: 10, date: '2026-03-04', recipient: 'Education Fund', cause: 'Education', amount: 0.55, status: 'completed' },
])


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


const completedCount = computed(() => 
  allDonations.value.filter(d => d.status === 'completed').length
)

const pendingCount = computed(() => 
  allDonations.value.filter(d => d.status === 'pending').length
)

const totalDonatedAmount = computed(() => {
  const total = allDonations.value
    .filter(d => d.status === 'completed')
    .reduce((sum, d) => sum + d.amount, 0)
  return total.toFixed(2)
})


const recipientSummary = computed(() => {
  const recipientMap = {}
  donationHistory.value.forEach(donation => {
    const recipientName = donation.recipient
    if (!recipientMap[recipientName]) {
      recipientMap[recipientName] = {
        name: recipientName,
        cause: donation.cause,
        totalAmount: 0,
        count: 0,
        lastDate: donation.date,
        hasCompleted: true,
        donations: []
      }
    }
    
    recipientMap[recipientName].totalAmount += donation.amount
    recipientMap[recipientName].count++
    recipientMap[recipientName].donations.push(donation)
    
    
    if (donation.status === 'pending') {
      recipientMap[recipientName].hasCompleted = false
    }
    

    if (donation.date > recipientMap[recipientName].lastDate) {
      recipientMap[recipientName].lastDate = donation.date
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
  
  if (statusFilter.value !== 'All') {
    filtered = filtered.filter(d => d.status === statusFilter.value.toLowerCase())
  }
  
  if (categoryFilter.value !== 'All') {
    filtered = filtered.filter(d => d.cause === categoryFilter.value)
  }
  
  if (activitySearch.value) {
    const search = activitySearch.value.toLowerCase()
    filtered = filtered.filter(d => 
      d.recipient.toLowerCase().includes(search) ||
      d.cause.toLowerCase().includes(search) ||
      d.date.includes(search)
    )
  }
  
  return filtered
})


const selectWallet = (wallet) => {
  selectedWallet.value = wallet
  detailTab.value = 'donations'
}

const formatCurrency = (amount) => {
  return amount.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 8 })
}

const viewDonationDetails = (donation) => {
  $q.dialog({
    title: 'Donation Details',
    message: `
      <div style="text-align: left;">
        <p><strong>Date:</strong> ${donation.date}</p>
        <p><strong>Recipient:</strong> ${donation.recipient}</p>
        <p><strong>Cause:</strong> ${donation.cause}</p>
        <p><strong>Amount:</strong> ${donation.amount} BCH</p>
        <p><strong>Status:</strong> ${donation.status.toUpperCase()}</p>
      </div>
    `,
    html: true,
    ok: {
      label: 'Close',
      color: 'primary'
    }
  })
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
  background-color: #eeeeee;
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
    transform: translateY(-4px);
    box-shadow: 0 8px 16px rgba(0, 0, 0, 0.15);
  }
}


.recipient-card {

  border: 2px solid #e0e0e0;
  border-radius: 12px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.9);
  transition: all 0.3s ease;
  
  
  &:hover {
    transform: translateY(-4px);
    box-shadow: 0 8px 16px rgba(211, 37, 37, 0.15);
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

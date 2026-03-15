<template>
  <q-page class="dashboard-page">
    <div class="row" style="min-height: 100vh;">
      <div class="col-12 col-md-4 col-lg-3 q-pa-md sidebar-container">
        <div class="accounts-sidebar">
          <h5 class="q-mt-none q-mb-md">Charity<br><strong>Dashboard</strong></h5>
          
         
          <div class="q-mb-md">
            <q-btn-toggle
              v-model="activeTab"
              spread
              no-caps
              toggle-color="primary"
              color="white"
              text-color="black"
              :options="[
                {label: 'Withdraw', value: 'balances'},
                {label: 'Transaction Status', value: 'status'}
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
              v-for="account in accounts"
              :key="account.id"
              clickable
              v-ripple
              :active="selectedAccount?.id === account.id"
              @click="selectAccount(account)"
              class="account-item q-mb-sm rounded-borders"
              active-class="bg-white"
            >
              <q-item-section avatar>
                <img src="~assets/paytaca.png" alt="wallet" class="icon-img" style="width: 32px; height: 32px;" />
              </q-item-section>
              <q-item-section>
                <q-item-label class="text-weight-medium">{{ account.name }}</q-item-label>
                <q-item-label caption>{{ account.number }}</q-item-label>
                <div class="row q-mt-sm">
                  <div class="col">
                    <q-item-label caption>Current BCH</q-item-label>
                    <q-item-label class="text-weight-bold">{{ formatCurrency(account.current) }}</q-item-label>
                  </div>
                  <div class="col">
                    <q-item-label caption>Available BCH</q-item-label>
                    <q-item-label class="text-weight-bold">{{ formatCurrency(account.available) }}</q-item-label>
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

          
          <div v-if="activeTab === 'balances'" class="q-mt-md">
            <q-btn
              unelevated
              color="primary"
              label="Withdraw Funds"
              icon="account_balance_wallet"
              class="full-width"
              @click="openWithdrawDialog"
              :disable="!selectedAccount"
            />
          </div>
        </div>
      </div>

    
      <div class="col-12 col-md-8 col-lg-9 q-pa-md q-pa-lg-lg bg-white main-content">
        <div v-if="activeTab === 'balances' && selectedAccount" class="account-details">
          <div class="row items-center justify-between q-mb-lg flex-wrap">
            <h4 class="q-my-none col-12 col-sm-auto">{{ selectedAccount.name }}</h4>
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
            <q-tab name="transactions" label="Transactions" />
            <q-tab name="details" label="Details" />
            <q-tab name="pending" label="Pending" />
          </q-tabs>

          <q-separator class="q-mb-lg" />

          <q-tab-panels v-model="detailTab" animated>
            <q-tab-panel name="transactions">
              <div class="text-h6 q-mb-md">Recent Transactions</div>
              
              <q-table
                :rows="transactions"
                :columns="transactionColumns"
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
                    <span class="text-weight-medium">
                      {{ formatCurrency(props.row.amount) }} BCH
                    </span>
                  </q-td>
                </template>
                <template v-slot:body-cell-actions="props">
                  <q-td :props="props">
                    <q-btn flat round dense icon="more_vert" size="sm">
                      <q-menu>
                        <q-list style="min-width: 100px">
                          <q-item clickable v-close-popup>
                            <q-item-section>View Details</q-item-section>
                          </q-item>
                          <q-item clickable v-close-popup>
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
                      <div class="text-weight-medium">{{ selectedAccount.fullNumber }}</div>
                    </div>
                    <div class="detail-item q-mb-md">
                      <div class="text-caption text-grey-6 q-mb-xs">Donor Address</div>
                      <div class="text-weight-medium">{{ selectedAccount.iban }}</div>
                    </div>
                    <div class="detail-item q-mb-md">
                      <div class="text-caption text-grey-6 q-mb-xs">Network Fee </div>
                      <div class="text-weight-medium">{{ selectedAccount.creditRate }}</div>
                    </div>
                  </div>
                </div>

               
                <div class="col-12 col-sm-6 col-lg-4">
                  <div class="detail-section">
                    <div class="detail-item q-mb-md">
                      <div class="text-caption text-grey-6 q-mb-xs">Account name</div>
                      <div class="text-weight-medium">{{ selectedAccount.accountName }}</div>
                    </div>
                    <div class="detail-item q-mb-md">
                      <div class="text-caption text-grey-6 q-mb-xs">Contract Code</div>
                      <div class="text-weight-medium">{{ selectedAccount.swift }}</div>
                    </div>
                    <div class="detail-item q-mb-md">
                      <div class="text-caption text-grey-6 q-mb-xs">Amount Balance</div>
                      <div class="text-weight-medium">{{ selectedAccount.debitRate }}</div>
                    </div>
                  </div>
                </div>

         
                <div class="col-12 col-sm-6 col-lg-4">
                  <div class="detail-section">
                    <div class="detail-item q-mb-md">
                      <div class="text-caption text-grey-6 q-mb-xs">Wallet Type</div>
                      <div class="text-weight-medium">{{ selectedAccount.product }}</div>
                    </div>
                    <div class="detail-item q-mb-md">
                      <div class="text-caption text-grey-6 q-mb-xs">Donor Name</div>
                      <div class="text-weight-medium">{{ selectedAccount.branch }}</div>
                    </div>
                    <div class="detail-item q-mb-md">
                      <div class="text-caption text-grey-6 q-mb-xs">Total Contract</div>
                      <div class="text-weight-medium">BCH-{{ selectedAccount.overdraftLimit }}</div>
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
                  <div v-for="card in selectedAccount.cards" :key="card.id" class="col-12 col-sm-6 col-md-4">
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

       
            <q-tab-panel name="pending">
              <div class="text-h6 q-mb-md">Pending Transactions</div>
              
              <q-table
                :rows="pendingTransactions"
                :columns="transactionColumns"
                row-key="id"
                flat
                :pagination="{ rowsPerPage: 10 }"
                class="transactions-table"
              >
                <template v-slot:body-cell-status="props">
                  <q-td :props="props">
                    <q-badge color="warning" label="pending" />
                  </q-td>
                </template>
                <template v-slot:body-cell-amount="props">
                  <q-td :props="props">
                    <span class="text-weight-medium">
                      {{ formatCurrency(props.row.amount) }} BCH
                    </span>
                  </q-td>
                </template>
                <template v-slot:body-cell-actions="props">
                  <q-td :props="props">
                    <q-btn flat round dense icon="more_vert" size="sm">
                      <q-menu>
                        <q-list style="min-width: 100px">
                          <q-item clickable v-close-popup>
                            <q-item-section>View Details</q-item-section>
                          </q-item>
                          <q-item clickable v-close-popup>
                            <q-item-section>Cancel</q-item-section>
                          </q-item>
                        </q-list>
                      </q-menu>
                    </q-btn>
                  </q-td>
                </template>
              </q-table>
            </q-tab-panel>
          </q-tab-panels>
        </div>

       
        <div v-if="activeTab === 'status'" class="transaction-status">
          <div class="row items-center justify-between q-mb-lg">
            <h4 class="q-my-none">Transaction Status</h4>
            <div>
              <q-btn flat icon="download" label="Export" />
              <q-btn flat icon="refresh" @click="refreshTransactions" />
            </div>
          </div>

          <div class="row q-mb-md q-col-gutter-md">
            <div class="col-12 col-sm-6 col-md-3">
              <q-card flat class="stats-card">
                <q-card-section>
                  <div class="text-caption text-grey-6">Total Transactions</div>
                  <div class="text-h5 text-weight-bold">{{ allTransactions.length }}</div>
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
              <q-card flat class="stats-card bg-negative text-white">
                <q-card-section>
                  <div class="text-caption">Failed</div>
                  <div class="text-h5 text-weight-bold">{{ failedCount }}</div>
                </q-card-section>
              </q-card>
            </div>
          </div>

          <q-card flat class="q-mt-md">
            <q-card-section>
              <div class="row q-col-gutter-md q-mb-md">
                <div class="col-12 col-md-6">
                  <q-input
                    v-model="transactionSearch"
                    outlined
                    dense
                    placeholder="Search transactions..."
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
                    v-model="typeFilter"
                    :options="['All', 'Paytaca', 'Ethereum', 'MetaMask', 'Bitcoin', 'Polygon']"
                    outlined
                    dense
                    label="Wallet Type"
                  />
                </div>
              </div>

              <q-table
                :rows="filteredTransactions"
                :columns="transactionColumns"
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
                    <span class="text-weight-medium">
                      {{ formatCurrency(props.row.amount) }} BCH
                    </span>
                  </q-td>
                </template>
                <template v-slot:body-cell-actions="props">
                  <q-td :props="props">
                    <q-btn flat round dense icon="visibility" size="sm" @click="viewTransactionDetails(props.row)">
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

   
    <q-dialog v-model="withdrawDialog" persistent>
      <q-card style="min-width: 400px; max-width: 500px;">
        <q-card-section class="row items-center q-pb-none">
          <div class="text-h6">Withdraw Funds</div>
          <q-space />
          <q-btn icon="close" flat round dense v-close-popup />
        </q-card-section>

        <q-card-section>
          <div v-if="selectedAccount" class="q-mb-md">
            <div class="text-caption text-grey-6">Available Balance</div>
            <div class="text-h5 text-weight-bold text-primary">
              {{ formatCurrency(selectedAccount.available) }} BCH
            </div>
          </div>

          <q-form @submit="handleWithdraw" class="q-gutter-md">
            <q-input
              v-model="withdrawForm.amount"
              type="number"
              label="Amount (BCH)"
              outlined
              :rules="[
                val => !!val || 'Amount is required',
                val => val > 0 || 'Amount must be greater than 0',
                val => val <= selectedAccount?.available || 'Insufficient balance'
              ]"
              step="0.00000001"
              min="0"
            >
              <template v-slot:prepend>
                <q-icon name="payments" />
              </template>
              <template v-slot:hint>
                Min: 0.00001 BCH
              </template>
            </q-input>

            <q-input
              v-model="withdrawForm.donorAddress"
              label="Donor Address"
              outlined
              :rules="[
                val => !!val || 'Address is required',
                val => validateAddress(val) || 'Invalid BCH address'
              ]"
            >
              <template v-slot:prepend>
                <q-icon name="account_balance_wallet" />
              </template>
            </q-input>

            <q-input
              v-model="withdrawForm.note"
              label="Note (Optional)"
              outlined
              type="textarea"
              rows="3"
              maxlength="200"
              counter
            >
              <template v-slot:prepend>
                <q-icon name="note" />
              </template>
            </q-input>

            <div class="q-mt-md">
              <div class="row q-col-gutter-sm">
                <div class="col-6">
                  <div class="text-caption text-grey-6">Transaction Fee</div>
                  <div class="text-weight-medium">~0.00001 BCH</div>
                </div>
                <div class="col-6">
                  <div class="text-caption text-grey-6">Total Amount</div>
                  <div class="text-weight-bold text-primary">
                    {{ calculateTotal() }} BCH
                  </div>
                </div>
              </div>
            </div>
          </q-form>
        </q-card-section>

        <q-card-actions align="right" class="q-px-md q-pb-md">
          <q-btn flat label="Cancel" color="grey-7" v-close-popup />
          <q-btn
            unelevated
            label="Withdraw"
            color="primary"
            @click="handleWithdraw"
            :loading="withdrawing"
            :disable="!isFormValid()"
          />
        </q-card-actions>
      </q-card>
    </q-dialog>
  </q-page>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useQuasar } from 'quasar'
import { useBCHContract } from '../composables/useBCHContract'
import bchImg from 'src/assets/bch.png'
import projectImg from 'src/assets/project.png'
import transactionImg from 'src/assets/transaction.png'

const $q = useQuasar()
const { isConnected } = useBCHContract()

const activeTab = ref('balances')
const detailTab = ref('details')
const searchQuery = ref('')
const withdrawDialog = ref(false)
const withdrawing = ref(false)
const withdrawForm = ref({
  amount: '',
  donorAddress: '',
  note: ''
})

const accounts = ref([
  {
    id: 1,
    name: 'Kapamilya Donor',
    number: '',
    fullNumber: 'qr5agtachyxvm8pqg2z7z8z9z5z6z7z8z9zdef789',
    current: 122267.85,
    available: 122267.85,
    accountName: 'Kapamilya Donor',
    product: 'Paytaca',
    iban: 'qp3wjpa3tjlj042z2wv7hahsldgwhwy0rq9sywjpyy',
    swift: 'BCYPCY2N',
    branch: 'Tanggol Dalisay',
    donorAddress: 'qp3wjpa3tjlj042z2wv7hahsldgwhwy0rq9sywjpyy',
    creditRate: '1000',
    debitRate: '856,00',
    overdraftLimit: '122,267.85',
    cards: [
      {
        id: 1,
        title1: 'TOTAL DONATION',
        title2: 'RECEIVED',
        colorClass: 'wallet-stat-card-blue',
        icon: bchImg,
        largeValue: '122.85',
        rightIcon: bchImg
      },
      {
        id: 2,
        title1: 'TOTAL',
        title2: 'PROJECTS',
        colorClass: 'wallet-stat-card-purple',
        icon: projectImg,
        largeValue: '50+',
        rightIcon: projectImg
      },
      {
        id: 3,
        title1: 'VERIFIED',
        title2: 'TRANSACTION',
        colorClass: 'wallet-stat-card-yellow',
        icon: transactionImg,
        largeValue: '200+',
        rightIcon: transactionImg
      }
    ]
  },
  {
    id: 2,
    name: 'GMA Kapuso Donor',
    number: '',
    fullNumber: 'qr5agtachyxvm8pqg2z7z8z9z5z6z7z8z9zdef789',
    current: 95420.50,
    available: 95420.50,
    accountName: 'GMA Kapuso Donor',
    product: 'Paytaca',
    iban: 'qp3wjpa3tjlj042z2wv7hahsldgwhwy0rq9sywjpyy',
    swift: 'BCYPCY2N',
    branch: 'Pacquiao',
    donorAddress: 'bitcoincash:qq8z6kx7qzj3zjz5qz9z5z6z7z8z9zabc123456',
    creditRate: '1000',
    debitRate: '856,00',
    overdraftLimit: '3,000,000.00',
    cards: []
  },
  {
    id: 3,
    name: 'Tulong Dunong ',
    number: '',
    fullNumber: 'qr5agtachyxvm8pqg2z7z8z9z5z6z7z8z9zdef789',
    current: 78350.25,
    available: 78350.25,
    accountName: 'Tulong Dunong Donor',
    product: 'Paytaca',
    iban: 'qp3wjpa3tjlj042z2wv7hahsldgwhwy0rq9sywjpyy',
    swift: 'BCYPCY2N',
    branch: 'Casimero',
    donorAddress: 'bitcoincash:qr5agtachyxvm8pqg2z7z8z9z5z6z7z8z9zdef789',
    creditRate: '1000',
    debitRate: '856,00',
    overdraftLimit: '1,234,900.00',
    cards: []
  }
])

const selectedAccount = ref(accounts.value[0])


const transactionSearch = ref('')
const statusFilter = ref('All')
const typeFilter = ref('All')

const transactionColumns = [
  { name: 'date', label: 'Date', field: 'date', align: 'left', sortable: true },
  { name: 'description', label: 'Description', field: 'description', align: 'left' },
  { name: 'type', label: 'Type', field: 'type', align: 'center' },
  { name: 'amount', label: 'Amount', field: 'amount', align: 'right', sortable: true },
  { name: 'status', label: 'Status', field: 'status', align: 'center' },
  { name: 'actions', label: 'Actions', field: 'actions', align: 'center' }
]

const transactions = ref([
  { id: 1, date: '2026-03-13', description: 'Donation from Anonymous', type: 'Paytaca', amount: 0.5, status: 'completed' },
  { id: 2, date: '2026-03-12', description: 'Donation from Anonymous', type: 'Paytaca', amount: 1.2, status: 'completed' },
  { id: 3, date: '2026-03-11', description: 'Donation from Anonymous', type: 'Paytaca', amount: 0.8, status: 'completed' },
  { id: 4, date: '2026-03-10', description: 'Donation from Anonymous', type: 'Paytaca', amount: 2.5, status: 'completed' },
  { id: 5, date: '2026-03-09', description: 'Donation from Anonymous', type: 'Paytaca', amount: 0.3, status: 'completed' },
])

const pendingTransactions = ref([
  { id: 6, date: '2026-03-13', description: 'Pending donation verification', type: 'Paytaca', amount: 0.75, status: 'pending' },
  { id: 7, date: '2026-03-13', description: 'Awaiting network confirmation', type: 'Paytaca', amount: 1.0, status: 'pending' },
])

const allTransactions = ref([
  { id: 1, date: '2026-03-13', description: 'Donation from John Doe', type: 'Paytaca', amount: 0.5, status: 'completed' },
  { id: 2, date: '2026-03-12', description: 'Donation from Jane Smith', type: 'Ethereum', amount: 1.2, status: 'completed' },
  { id: 3, date: '2026-03-11', description: 'Donation from Anonymous', type: 'MetaMask', amount: 0.8, status: 'completed' },
  { id: 4, date: '2026-03-10', description: 'Donation from Maria ', type: 'Paytaca', amount: 2.5, status: 'completed' },
  { id: 5, date: '2026-03-09', description: 'Donation from Robert Brown', type: 'Bitcoin', amount: 0.3, status: 'completed' },
  { id: 6, date: '2026-03-13', description: 'Pending donation verification', type: 'Polygon', amount: 0.75, status: 'pending' },
  { id: 7, date: '2026-03-13', description: 'Awaiting network confirmation', type: 'Ethereum', amount: 1.0, status: 'pending' },
  { id: 8, date: '2026-03-08', description: 'Project funding - Education', type: 'Paytaca', amount: 5.0, status: 'completed' },
  { id: 9, date: '2026-03-07', description: 'Project funding - Healthcare', type: 'MetaMask', amount: 3.2, status: 'completed' },
  { id: 10, date: '2026-03-06', description: 'Failed transaction', type: 'Bitcoin', amount: 1.5, status: 'failed' },
  { id: 11, date: '2026-03-05', description: 'Donation from Alex The Great', type: 'Polygon', amount: 0.95, status: 'completed' },
  { id: 12, date: '2026-03-04', description: 'Project funding - Environment', type: 'Ethereum', amount: 2.8, status: 'completed' },
])


const completedCount = computed(() => 
  allTransactions.value.filter(t => t.status === 'completed').length
)

const pendingCount = computed(() => 
  allTransactions.value.filter(t => t.status === 'pending').length
)

const failedCount = computed(() => 
  allTransactions.value.filter(t => t.status === 'failed').length
)

const filteredTransactions = computed(() => {
  let filtered = [...allTransactions.value]
  

  if (statusFilter.value !== 'All') {
    filtered = filtered.filter(t => t.status === statusFilter.value.toLowerCase())
  }
  
  
  if (typeFilter.value !== 'All') {
    filtered = filtered.filter(t => t.type === typeFilter.value.toLowerCase())
  }
  

  if (transactionSearch.value) {
    const search = transactionSearch.value.toLowerCase()
    filtered = filtered.filter(t => 
      t.description.toLowerCase().includes(search) ||
      t.date.includes(search) ||
      t.status.toLowerCase().includes(search)
    )
  }
  
  return filtered
})

const selectAccount = (account) => {
  selectedAccount.value = account
  detailTab.value = 'details'
}

const formatCurrency = (amount) => {
  return amount.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })
}

const openWithdrawDialog = () => {
  if (!isConnected.value) {
    $q.notify({
      type: 'warning',
      message: 'Please connect your wallet first',
      position: 'top'
    })
    return
  }
  

  withdrawForm.value = {
    amount: selectedAccount.value?.available?.toString() || '',
    donorAddress: selectedAccount.value?.donorAddress || '',
    note: ''
  }
  
  withdrawDialog.value = true
}

const validateAddress = (address) => {
  if (!address) return false
  const bchRegex = /^(bitcoincash:)?[qp][a-z0-9]{41}$/i
  return bchRegex.test(address)
}

const calculateTotal = () => {
  const amount = parseFloat(withdrawForm.value.amount) || 0
  const fee = 0.00001
  return (amount + fee).toFixed(8)
}

const isFormValid = () => {
  const amount = parseFloat(withdrawForm.value.amount)
  return (
    amount > 0 &&
    amount <= selectedAccount.value?.available &&
    validateAddress(withdrawForm.value.donorAddress)
  )
}

const handleWithdraw = async () => {
  if (!isFormValid()) return

  withdrawing.value = true

  try {
    const amount = parseFloat(withdrawForm.value.amount)
    const donor = withdrawForm.value.donorAddress

    
    $q.dialog({
      title: 'Confirm Withdrawal',
      message: `Withdraw ${amount} BCH to ${donor.substring(0, 20)}...?`,
      cancel: true,
      persistent: true
    }).onOk(async () => {
      try {
        await new Promise(resolve => setTimeout(resolve, 2000))
        selectedAccount.value.available -= amount
        selectedAccount.value.current -= amount
        $q.notify({
          type: 'positive',
          message: 'Withdrawal successful!',
          caption: `${amount} BCH sent to ${donor.substring(0, 30)}...`,
          position: 'top',
          timeout: 3000
        })
        withdrawForm.value = {
          amount: '',
          donorAddress: '',
          note: ''
        }
        withdrawDialog.value = false
      } catch (error) {
        console.error('Withdrawal error:', error)
        $q.notify({
          type: 'negative',
          message: 'Withdrawal failed',
          caption: error.message || 'Please try again',
          position: 'top'
        })
      }
    })
  } catch (error) {
    console.error('Withdrawal error:', error)
    $q.notify({
      type: 'negative',
      message: 'Withdrawal failed',
      caption: error.message || 'Please try again',
      position: 'top'
    })
  } finally {
    withdrawing.value = false
  }
}

const refreshTransactions = () => {
  $q.notify({
    type: 'info',
    message: 'Refreshing transactions...',
    position: 'top',
    timeout: 1000
  })
  setTimeout(() => {
    $q.notify({
      type: 'positive',
      message: 'Transactions updated',
      position: 'top',
      timeout: 1500
    })
  }, 1000)
}

const viewTransactionDetails = (transaction) => {
  $q.dialog({
    title: 'Transaction Details',
    message: `
      <div style="text-align: left;">
        <p><strong>Date:</strong> ${transaction.date}</p>
        <p><strong>Description:</strong> ${transaction.description}</p>
        <p><strong>Type:</strong> ${transaction.type.toUpperCase()}</p>
        <p><strong>Amount:</strong> ${transaction.amount} BCH</p>
        <p><strong>Status:</strong> ${transaction.status.toUpperCase()}</p>
      </div>
    `,
    html: true,
    ok: {
      label: 'Close',
      color: 'primary'
    }
  })
}
</script>

<style scoped lang="scss">
.dashboard-page {
  overflow-x: hidden;
}

.sidebar-container {
  background-color: #eeeeee; 
}

.accounts-sidebar {
  border-radius: 8px;
  padding: 1rem;
}

.accounts-sidebar {
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
  box-shadow: inset;
  padding: 1rem;
}

.detail-section {
  .detail-item {
    padding: 0.5rem 0;
  }
}

.credit-card {
  border-radius: 12px;
  background: linear-gradient(135deg, #6c85f5dc 0%, #8799f3 100%);
  border: 4px solid #fffdf9;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.5);
  padding: 1rem;
  min-height: 200px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  
  .card-number {
    font-size: 1.1rem;
    letter-spacing: 2px;
  }
}

.wallet-stat-card {
  border-radius: 20px;
  padding: 10px;
  color: white;
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
  font-size: 20px;
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

:deep(.q-btn-toggle) {
  border-radius: 4px;
  overflow: hidden;
}

:deep(.q-tab) {
  font-weight: 500;
}

.wallet-stat-card {
  border-radius: 20px;
  padding: 10px;
  color: white;
}

.wallet-stat-card:hover {
  transform: translateY(-5px);
  box-shadow: inset, 0 8px 16px rgba(0, 0, 0, 0.2);
}

.wallet-stat-card-blue {
  background: linear-gradient(135deg, #6c85f5dc 0%, #8799f3 100%);
  border: px solid #f9f9ff;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.9);
  transition: all 0.2s ease;
}

.wallet-stat-card-purple {
  background: linear-gradient(135deg, #a9a4ffd3 0%, #7e7affd0 100%);
  border: 4px solid #f9f9ff;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.5);
  transition: all 0.2s ease;
}

.wallet-stat-card-yellow {
  background: linear-gradient(135deg, #e3d273d9 0%, #ebcf89e2 100%);
  border: 4px solid #fffdf9;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.5);
  transition: all 0.2s ease;
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


@media (max-width: 1023px) {
  .wallet-stat-header {
    font-size: 20px;
  }
  
  .wallet-stat-icon-img {
    width: 50px;
    height: 50px;
  }
  
  .wallet-stat-icon-right-img {
    width: 80px;
    height: 80px;
  }
}

@media (max-width: 599px) {
  .accounts-sidebar h5 {
    font-size: 1.2rem;
  }
  
  .wallet-stat-header {
    font-size: 18px;
  }
  
  .wallet-stat-value {
    font-size: 20px;
  }
  
  .wallet-stat-value-large {
    font-size: 28px;
  }
  
  .wallet-stat-icon-img {
    width: 40px;
    height: 40px;
  }
  
  .wallet-stat-icon-right-img {
    width: 60px;
    height: 60px;
  }
  
  .wallet-stat-badge-img {
    width: 28px;
    height: 28px;
  }
  
  .wallet-badge-text {
    font-size: 10px;
  }
}

.stats-card {
  border-radius: 8px;
  transition: all 0.3s ease;
  
  &:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  }
}

.transactions-table {
  :deep(.q-table__top) {
    padding: 12px 0;
  }
  
  :deep(thead tr th) {
    font-weight: 600;
    font-size: 13px;
  }
  
  :deep(tbody tr) {
    cursor: pointer;
    
    &:hover {
      background-color: rgba(0, 0, 0, 0.02);
    }
  }
}

.transaction-status {
  .stats-card {
    min-height: 100px;
  }
}

.view-all-link {
  transition: color 0.3s ease;
  
  &:hover {
    color: #2196F3 !important;
  }
}

:deep(.q-tab) {
  transition: color 0.3s ease;
  
  &:hover {
    color: #2196F3 !important;
  }
}

:deep(.q-tab--active) {
  &:hover {
    color: #2196F3 !important;
  }
}
</style>
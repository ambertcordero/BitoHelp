<template>
  <q-page class="dashboard-page">
    <div class="row" style="min-height: 100vh">
      <div class="col-12 col-md-4 col-lg-3 q-pa-md sidebar-container">
        <div class="accounts-sidebar">
          <h5 class="q-mt-none q-mb-md">Charity<br /><strong>Dashboard</strong></h5>

          <div class="q-mb-md">
            <q-btn-toggle
              v-model="activeTab"
              spread
              no-caps
              toggle-color="primary"
              color="white"
              text-color="black"
              :options="[
                { label: 'Withdraw', value: 'balances' },
                { label: 'Transaction Status', value: 'status' },
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
                <img
                  src="~assets/paytaca.png"
                  alt="wallet"
                  class="icon-img"
                  style="width: 32px; height: 32px"
                />
              </q-item-section>
              <q-item-section>
                <q-item-label class="text-weight-medium">{{ account.name }}</q-item-label>
                <q-item-label caption>{{ account.number }}</q-item-label>
                <div class="row q-mt-sm">
                  <div class="col">
                    <q-item-label caption>Current BCH</q-item-label>
                    <q-item-label class="text-weight-bold">{{
                      formatCurrency(account.current)
                    }}</q-item-label>
                  </div>
                  <div class="col">
                    <q-item-label caption>Available BCH</q-item-label>
                    <q-item-label class="text-weight-bold">{{
                      formatCurrency(account.available)
                    }}</q-item-label>
                  </div>
                </div>
              </q-item-section>
              <q-item-section side>
                <q-btn flat round dense icon="more_vert" size="sm" />
              </q-item-section>
            </q-item>
          </q-list>

          <div class="text-center q-mt-md">
            <a
              href="#"
              class="view-all-link text-blue-7 text-weight-medium"
              style="text-decoration: none"
              >View all</a
            >
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
            <q-tab name="transactions" label="All Donations" />
            <q-tab name="details" label="Details" />
            <q-tab name="pending" label="Pending Withdrawals" />
          </q-tabs>

          <q-separator class="q-mb-lg" />

          <q-tab-panels v-model="detailTab" animated>
            <q-tab-panel name="transactions">
              <div class="text-h6 q-mb-md">All Donations Received</div>

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
                      :color="props.row.withdrawn ? 'positive' : 'warning'"
                      :label="props.row.withdrawn ? 'Withdrawn' : 'Pending Withdrawal'"
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
                          <q-item clickable v-close-popup @click="openDonationDetails(props.row)">
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
                <!-- Donation Details Dialog -->
                <q-dialog v-model="donationDetailsDialog">
                  <q-card style="min-width: 400px; max-width: 500px">
                    <q-card-section class="row items-center q-pb-none">
                      <div class="text-h6">Donation Details</div>
                      <q-space />
                      <q-btn icon="close" flat round dense v-close-popup @click="donationDetailsDialog = false" />
                    </q-card-section>
                    <q-card-section>
                      <div v-if="selectedDonation">
                        <div class="q-mb-sm"><strong>Date:</strong> {{ selectedDonation.date }}</div>
                        <div class="q-mb-sm"><strong>Amount:</strong> {{ formatCurrency(selectedDonation.amount) }} BCH</div>
                        <div class="q-mb-sm"><strong>Donor Name:</strong> {{ selectedDonation.donorName }}</div>
                        <div class="q-mb-sm"><strong>Donor Email:</strong> {{ selectedDonation.donorEmail }}</div>
                        <div class="q-mb-sm"><strong>Donor Contact:</strong> {{ selectedDonation.donorContact }}</div>
                        <div class="q-mb-sm"><strong>Message:</strong> {{ selectedDonation.description }}</div>
                        <div class="q-mb-sm"><strong>Cause:</strong> {{ selectedDonation.cause }}</div>
                        <div class="q-mb-sm"><strong>Transaction ID:</strong> {{ selectedDonation.txid }}</div>
                        <div class="q-mb-sm"><strong>Explorer URL:</strong> <a :href="selectedDonation.explorerUrl" target="_blank">{{ selectedDonation.explorerUrl }}</a></div>
                        <div class="q-mb-sm"><strong>Contract:</strong> {{ selectedDonation.contract }}</div>
                        <div class="q-mb-sm"><strong>Interval:</strong> {{ selectedDonation.interval }}</div>
                      </div>
                    </q-card-section>
                    <q-card-actions align="right" class="q-px-md q-pb-md">
                      <q-btn flat label="Close" color="grey-7" v-close-popup @click="donationDetailsDialog = false" />
                    </q-card-actions>
                  </q-card>
                </q-dialog>

              // Donation Details Dialog State
              const donationDetailsDialog = ref(false)
              const selectedDonation = ref(null)

              function openDonationDetails(donation) {
                selectedDonation.value = donation
                donationDetailsDialog.value = true
              }
              </q-table>
            </q-tab-panel>

            <q-tab-panel name="details" class="details-panel">
              <div class="row q-col-gutter-md q-col-gutter-xl-lg">
                <div class="col-12 col-sm-6 col-lg-4">
                  <div class="detail-section">
                    <div class="detail-item q-mb-md">
                      <div class="text-caption text-grey-6 q-mb-xs">Wallet Address</div>
                      <div class="text-weight-medium">{{ selectedAccount.address }}</div>
                    </div>
                    <div class="detail-item q-mb-md">
                      <div class="text-caption text-grey-6 q-mb-xs">Wallet Type</div>
                      <div class="text-weight-medium">{{ selectedAccount.type }}</div>
                    </div>
                    <div class="detail-item q-mb-md">
                      <div class="text-caption text-grey-6 q-mb-xs">Network Fee Paid</div>
                      <div class="text-weight-medium">{{ selectedAccount.totalFees }} BCH</div>
                    </div>
                  </div>
                </div>

                <div class="col-12 col-sm-6 col-lg-4">
                  <div class="detail-section">
                    <div class="detail-item q-mb-md">
                      <div class="text-caption text-grey-6 q-mb-xs">Charity Name</div>
                      <div class="text-weight-medium">{{ selectedAccount.charityName }}</div>
                    </div>
                    <div class="detail-item q-mb-md">
                      <div class="text-caption text-grey-6 q-mb-xs">Email</div>
                      <div class="text-weight-medium">{{ selectedAccount.email }}</div>
                    </div>
                    <div class="detail-item q-mb-md">
                      <div class="text-caption text-grey-6 q-mb-xs">Total Received</div>
                      <div class="text-weight-medium">
                        {{ formatCurrency(selectedAccount.totalReceived) }} BCH
                      </div>
                    </div>
                  </div>
                </div>

                <div class="col-12 col-sm-6 col-lg-4">
                  <div class="detail-section">
                    <div class="detail-item q-mb-md">
                      <div class="text-caption text-grey-6 q-mb-xs">First Donation Received</div>
                      <div class="text-weight-medium">{{ selectedAccount.firstDonation }}</div>
                    </div>
                    <div class="detail-item q-mb-md">
                      <div class="text-caption text-grey-6 q-mb-xs">Last Donation Received</div>
                      <div class="text-weight-medium">{{ selectedAccount.lastDonation }}</div>
                    </div>
                    <div class="detail-item q-mb-md">
                      <div class="text-caption text-grey-6 q-mb-xs">Total Transactions</div>
                      <div class="text-weight-medium">{{ selectedAccount.transactionCount }}</div>
                    </div>
                  </div>
                </div>
              </div>

              <div class="q-mt-xl">
                <div class="row items-center justify-between q-mb-md">
                  <h6 class="q-my-none">Charity Impact</h6>
                  <q-btn flat dense icon="expand_less" />
                </div>

                <div class="row q-col-gutter-md">
                  <div
                    v-for="card in selectedAccount.cards"
                    :key="card.id"
                    class="col-12 col-sm-6 col-md-4"
                  >
                    <q-card flat :class="['wallet-stat-card', card.colorClass]">
                      <q-card-section>
                        <div class="wallet-stat-header">{{ card.title1 }}</div>
                        <div class="wallet-stat-header">{{ card.title2 }}</div>
                        <div class="wallet-stat-content">
                          <div v-if="card.largeValue" class="wallet-stat-value-large">
                            {{ card.largeValue }}
                          </div>
                          <div v-if="card.rightIcon" class="wallet-stat-icon-right">
                            <img
                              :src="card.rightIcon"
                              alt="right-icon"
                              class="wallet-stat-icon-right-img"
                            />
                          </div>
                        </div>
                      </q-card-section>
                    </q-card>
                  </div>
                </div>
              </div>
            </q-tab-panel>

            <q-tab-panel name="pending">
              <div class="text-h6 q-mb-md">Pending Withdrawals</div>

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
                    <q-badge color="warning" label="Pending Withdrawal" />
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
                      :color="
                        props.row.status === 'completed'
                          ? 'positive'
                          : props.row.status === 'pending'
                            ? 'warning'
                            : 'negative'
                      "
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
                    <q-btn
                      flat
                      round
                      dense
                      icon="visibility"
                      size="sm"
                      @click="viewTransactionDetails(props.row)"
                    >
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
      <q-card style="min-width: 400px; max-width: 500px">
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
                (val) => !!val || 'Amount is required',
                (val) => val > 0 || 'Amount must be greater than 0',
                (val) => val <= selectedAccount?.available || 'Insufficient balance',
              ]"
              step="0.00000001"
              min="0"
            >
              <template v-slot:prepend>
                <q-icon name="payments" />
              </template>
              <template v-slot:hint> Min: 0.00001 BCH </template>
            </q-input>

            <q-input
              v-model="withdrawForm.donorAddress"
              label="Donor Address"
              outlined
              :rules="[
                (val) => !!val || 'Address is required',
                (val) => validateAddress(val) || 'Invalid BCH address',
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
                  <div class="text-weight-bold text-primary">{{ calculateTotal() }} BCH</div>
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
import { ref, computed, onMounted, onUnmounted, watch } from 'vue'
import { useQuasar } from 'quasar'
import { api } from 'boot/axios'
import bchImg from 'src/assets/bch.png'
import projectImg from 'src/assets/project.png'
import transactionImg from 'src/assets/transaction.png'

const $q = useQuasar()

const isConnected = ref(localStorage.getItem('bitohelp.wallet.connected') === '1')
function onWalletChange() {
  isConnected.value = localStorage.getItem('bitohelp.wallet.connected') === '1'
}
onMounted(() => window.addEventListener('bitohelp:wallet-connection-changed', onWalletChange))
onUnmounted(() => window.removeEventListener('bitohelp:wallet-connection-changed', onWalletChange))

const loadingDonations = ref(false)
const apiDonations = ref([])
const withdrawnDonations = ref(new Set())

const activeTab = ref('balances')
const detailTab = ref('details')
const searchQuery = ref('')
const withdrawDialog = ref(false)
const withdrawing = ref(false)
const withdrawForm = ref({
  amount: '',
  donorAddress: '',
  note: '',
})

const accounts = ref([
  {
    id: 1,
    name: 'Kapamilya Donor',
    number: '',
    address: 'qr5agtachyxvm8pqg2z7z8z9z5z6z7z8z9zdef789',
    current: 122267.85,
    available: 122267.85,
    type: 'Paytaca',
    totalFees: 1000,
    charityName: 'Kapamilya Foundation',
    email: 'contact@kapamilya.org',
    totalReceived: 122267.85,
    firstDonation: 'Jan 10, 2026',
    lastDonation: 'Mar 13, 2026',
    transactionCount: 200,
    cards: [
      {
        id: 1,
        title1: 'TOTAL DONATION',
        title2: 'RECEIVED',
        colorClass: 'wallet-stat-card-blue',
        icon: bchImg,
        largeValue: '122.85',
        rightIcon: bchImg,
      },
      {
        id: 2,
        title1: 'TOTAL',
        title2: 'PROJECTS',
        colorClass: 'wallet-stat-card-purple',
        icon: projectImg,
        largeValue: '50+',
        rightIcon: projectImg,
      },
      {
        id: 3,
        title1: 'VERIFIED',
        title2: 'TRANSACTION',
        colorClass: 'wallet-stat-card-yellow',
        icon: transactionImg,
        largeValue: '200+',
        rightIcon: transactionImg,
      },
    ],
  },
  {
    id: 2,
    name: 'GMA Kapuso Donor',
    number: '',
    address: 'qq8z6kx7qzj3zjz5qz9z5z6z7z8z9zabc123456',
    current: 95420.5,
    available: 95420.5,
    type: 'Paytaca',
    totalFees: 850,
    charityName: 'GMA Kapuso Foundation',
    email: 'info@kapuso.org',
    totalReceived: 95420.5,
    firstDonation: 'Dec 5, 2025',
    lastDonation: 'Mar 12, 2026',
    transactionCount: 175,
    cards: [],
  },
  {
    id: 3,
    name: 'Tulong Dunong ',
    number: '',
    address: 'qr5agtachyxvm8pqg2z7z8z9z5z6z7z8z9zdef789',
    current: 78350.25,
    available: 78350.25,
    type: 'Paytaca',
    totalFees: 650,
    charityName: 'Tulong Dunong Foundation',
    email: 'support@tulongdunong.org',
    totalReceived: 78350.25,
    firstDonation: 'Jan 20, 2026',
    lastDonation: 'Mar 11, 2026',
    transactionCount: 150,
    cards: [],
  },
])

const selectedAccount = ref(accounts.value[0])

const fetchDonations = async () => {
  loadingDonations.value = true
  try {
    // Use selectedAccount to get the charity/nonprofit id
    const nonprofitId = selectedAccount.value?.id
    if (!nonprofitId) {
      apiDonations.value = []
      loadingDonations.value = false
      return
    }
    // Fetch donations for the selected nonprofit/charity
    const response = await api.get(`nonprofits/${nonprofitId}/donations/`)

    if (Array.isArray(response.data)) {
      apiDonations.value = response.data
      console.log('Loaded donations for nonprofit', nonprofitId, ':', apiDonations.value.length)
    } else if (response.data && Array.isArray(response.data.results)) {
      apiDonations.value = response.data.results
      console.log('Loaded donations for nonprofit (paginated):', apiDonations.value.length)
    } else {
      console.warn(' Unexpected API response format:', response.data)
      apiDonations.value = []
    }

    updateTransactionsFromAPI()
    updateAccountStats()

    if (apiDonations.value.length > 0) {
      $q.notify({
        type: 'positive',
        message: `Loaded ${apiDonations.value.length} donations`,
        position: 'top',
        timeout: 2000,
      })
    }
  } catch (error) {
    console.error(' Failed to fetch donations:', error)
    apiDonations.value = []
    $q.notify({
      type: 'negative',
      message: 'Failed to load donation data',
      caption: 'Using default view. Check if server is running.',
      position: 'top',
    })
  } finally {
    loadingDonations.value = false
  }
}

const updateTransactionsFromAPI = () => {
  if (!Array.isArray(apiDonations.value) || apiDonations.value.length === 0) {
    console.log('No donations data to display')
    return
  }

  const mappedTransactions = apiDonations.value.map((donation, index) => ({
    id: donation.id || index + 1,
    date: new Date(donation.timestamp).toISOString().split('T')[0],
    description: `Donation from ${donation.donor_name || 'Anonymous'}${donation.message ? ' - ' + donation.message : ''}`,
    donorName: donation.donor_name || 'Anonymous',
    donorEmail: donation.donor_email || 'N/A',
    donorContact: donation.donor_contact || 'N/A',
    type: donation.coin || 'BCH',
    amount: parseFloat(donation.amount),
    status: withdrawnDonations.value.has(donation.id) ? 'completed' : 'pending',
    cause: donation.cause,
    txid: donation.txid,
    explorerUrl: donation.explorer_url,
    contract: donation.contract || 'N/A',
    interval: donation.interval || 'N/A',
    nonprofit: donation.nonprofit,
    withdrawn: withdrawnDonations.value.has(donation.id),
  }))

  transactions.value = mappedTransactions.slice(0, 5)
  allTransactions.value = mappedTransactions

  pendingTransactions.value = mappedTransactions.filter((t) => !t.withdrawn)

  createWithdrawalAccounts()
}

const updateAccountStats = () => {
  if (!Array.isArray(apiDonations.value) || apiDonations.value.length === 0) {
    console.log('No donations to update stats')
    return
  }

  const totalAmount = apiDonations.value.reduce((sum, d) => sum + parseFloat(d.amount), 0)
  const uniqueNonprofits = new Set(apiDonations.value.map((d) => d.nonprofit || d.cause))

  if (selectedAccount.value) {
    selectedAccount.value.totalReceived = totalAmount
    selectedAccount.value.current = totalAmount
    selectedAccount.value.available = totalAmount
    selectedAccount.value.transactionCount = apiDonations.value.length

    selectedAccount.value.cards = [
      {
        id: 1,
        title1: 'TOTAL DONATION',
        title2: 'RECEIVED',
        colorClass: 'wallet-stat-card-blue',
        icon: bchImg,
        largeValue: totalAmount.toFixed(2),
        rightIcon: bchImg,
      },
      {
        id: 2,
        title1: 'TOTAL',
        title2: 'CAUSES',
        colorClass: 'wallet-stat-card-purple',
        icon: projectImg,
        largeValue: `${uniqueNonprofits.size}+`,
        rightIcon: projectImg,
      },
      {
        id: 3,
        title1: 'VERIFIED',
        title2: 'TRANSACTION',
        colorClass: 'wallet-stat-card-yellow',
        icon: transactionImg,
        largeValue: `${apiDonations.value.length}+`,
        rightIcon: transactionImg,
      },
    ]
  }
}

const createWithdrawalAccounts = () => {
  if (!Array.isArray(apiDonations.value) || apiDonations.value.length === 0) return

  const groupedDonations = {}

  apiDonations.value.forEach((donation) => {
    const key = donation.cause || 'Unknown Charity'
    if (!groupedDonations[key]) {
      groupedDonations[key] = {
        donations: [],
        total: 0,
        pending: 0,
      }
    }

    const amount = parseFloat(donation.amount)
    groupedDonations[key].donations.push(donation)
    groupedDonations[key].total += amount

    if (!withdrawnDonations.value.has(donation.id)) {
      groupedDonations[key].pending += amount
    }
  })

  const newAccounts = Object.entries(groupedDonations).map(([charity, data], index) => ({
    id: index + 1,
    name: charity,
    number: `${data.donations.length} donations`,
    address: data.donations[0]?.recipient || '',
    current: data.total,
    available: data.pending,
    type: 'Paytaca',
    totalFees: 0,
    charityName: charity,
    email: '',
    totalReceived: data.total,
    firstDonation: data.donations[data.donations.length - 1]?.timestamp
      ? new Date(data.donations[data.donations.length - 1].timestamp).toLocaleDateString()
      : 'N/A',
    lastDonation: data.donations[0]?.timestamp
      ? new Date(data.donations[0].timestamp).toLocaleDateString()
      : 'N/A',
    transactionCount: data.donations.length,
    donations: data.donations,
    cards: [],
  }))

  accounts.value = newAccounts
  if (newAccounts.length > 0 && !selectedAccount.value) {
    selectedAccount.value = newAccounts[0]
  }
}


onMounted(() => {
  fetchDonations()
  const saved = localStorage.getItem('withdrawnDonations')
  if (saved) {
    withdrawnDonations.value = new Set(JSON.parse(saved))
  }
})

// Refetch donations when selectedAccount changes
watch(selectedAccount, () => {
  fetchDonations()
})

const transactionSearch = ref('')
const statusFilter = ref('All')
const typeFilter = ref('All')

const transactionColumns = [
  { name: 'date', label: 'Date', field: 'date', align: 'left', sortable: true },
  { name: 'donorName', label: 'Donor Name', field: 'donorName', align: 'left' },
  { name: 'description', label: 'Message', field: 'description', align: 'left' },
  { name: 'type', label: 'Type', field: 'type', align: 'center' },
  { name: 'amount', label: 'Amount', field: 'amount', align: 'right', sortable: true },
  { name: 'status', label: 'Status', field: 'status', align: 'center' },
  { name: 'actions', label: 'Actions', field: 'actions', align: 'center' },
]

const transactions = ref([
  {
    id: 1,
    date: '2026-03-13',
    description: 'Donation from Anonymous',
    type: 'Paytaca',
    amount: 0.5,
    status: 'completed',
  },
  {
    id: 2,
    date: '2026-03-12',
    description: 'Donation from Anonymous',
    type: 'Paytaca',
    amount: 1.2,
    status: 'completed',
  },
  {
    id: 3,
    date: '2026-03-11',
    description: 'Donation from Anonymous',
    type: 'Paytaca',
    amount: 0.8,
    status: 'completed',
  },
  {
    id: 4,
    date: '2026-03-10',
    description: 'Donation from Anonymous',
    type: 'Paytaca',
    amount: 2.5,
    status: 'completed',
  },
  {
    id: 5,
    date: '2026-03-09',
    description: 'Donation from Anonymous',
    type: 'Paytaca',
    amount: 0.3,
    status: 'completed',
  },
])

const pendingTransactions = ref([
  {
    id: 6,
    date: '2026-03-13',
    description: 'Pending donation verification',
    type: 'Paytaca',
    amount: 0.75,
    status: 'pending',
  },
  {
    id: 7,
    date: '2026-03-13',
    description: 'Awaiting network confirmation',
    type: 'Paytaca',
    amount: 1.0,
    status: 'pending',
  },
])

const allTransactions = ref([
  {
    id: 1,
    date: '2026-03-13',
    description: 'Donation from John Doe',
    type: 'Paytaca',
    amount: 0.5,
    status: 'completed',
  },
  {
    id: 2,
    date: '2026-03-12',
    description: 'Donation from Jane Smith',
    type: 'Ethereum',
    amount: 1.2,
    status: 'completed',
  },
  {
    id: 3,
    date: '2026-03-11',
    description: 'Donation from Anonymous',
    type: 'MetaMask',
    amount: 0.8,
    status: 'completed',
  },
  {
    id: 4,
    date: '2026-03-10',
    description: 'Donation from Maria ',
    type: 'Paytaca',
    amount: 2.5,
    status: 'completed',
  },
  {
    id: 5,
    date: '2026-03-09',
    description: 'Donation from Robert Brown',
    type: 'Bitcoin',
    amount: 0.3,
    status: 'completed',
  },
  {
    id: 6,
    date: '2026-03-13',
    description: 'Pending donation verification',
    type: 'Polygon',
    amount: 0.75,
    status: 'pending',
  },
  {
    id: 7,
    date: '2026-03-13',
    description: 'Awaiting network confirmation',
    type: 'Ethereum',
    amount: 1.0,
    status: 'pending',
  },
  {
    id: 8,
    date: '2026-03-08',
    description: 'Project funding - Education',
    type: 'Paytaca',
    amount: 5.0,
    status: 'completed',
  },
  {
    id: 9,
    date: '2026-03-07',
    description: 'Project funding - Healthcare',
    type: 'MetaMask',
    amount: 3.2,
    status: 'completed',
  },
  {
    id: 10,
    date: '2026-03-06',
    description: 'Failed transaction',
    type: 'Bitcoin',
    amount: 1.5,
    status: 'failed',
  },
  {
    id: 11,
    date: '2026-03-05',
    description: 'Donation from Alex The Great',
    type: 'Polygon',
    amount: 0.95,
    status: 'completed',
  },
  {
    id: 12,
    date: '2026-03-04',
    description: 'Project funding - Environment',
    type: 'Ethereum',
    amount: 2.8,
    status: 'completed',
  },
])

const completedCount = computed(
  () => allTransactions.value.filter((t) => t.status === 'completed').length,
)

const pendingCount = computed(
  () => allTransactions.value.filter((t) => t.status === 'pending').length,
)

const failedCount = computed(
  () => allTransactions.value.filter((t) => t.status === 'failed').length,
)

const filteredTransactions = computed(() => {
  let filtered = [...allTransactions.value]

  if (statusFilter.value !== 'All') {
    filtered = filtered.filter((t) => t.status === statusFilter.value.toLowerCase())
  }

  if (typeFilter.value !== 'All') {
    filtered = filtered.filter((t) => t.type === typeFilter.value.toLowerCase())
  }

  if (transactionSearch.value) {
    const search = transactionSearch.value.toLowerCase()
    filtered = filtered.filter(
      (t) =>
        t.description.toLowerCase().includes(search) ||
        t.date.includes(search) ||
        t.status.toLowerCase().includes(search),
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
      position: 'top',
    })
    return
  }

  withdrawForm.value = {
    amount: selectedAccount.value?.available?.toString() || '',
    donorAddress: selectedAccount.value?.donorAddress || '',
    note: '',
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
    const donorAddress = withdrawForm.value.donorAddress

    $q.dialog({
      title: '',
      message: `
        <div style="font-family: 'Roboto', sans-serif;">
          <div style="padding: 16px 0; border-bottom: 1px solid #e0e0e0; margin-bottom: 20px;">
            <div style="font-size: 18px; font-weight: 600; color: #212121;">Confirm Withdrawal</div>
            <div style="font-size: 13px; color: #757575; margin-top: 4px;">Please review the details before proceeding</div>
          </div>

          <div style="background: #f5f5f5; padding: 16px; border-radius: 8px; border: 1px solid #e0e0e0; margin-bottom: 16px;">
            <div style="margin-bottom: 12px;">
              <div style="font-size: 12px; color: #757575; font-weight: 500; margin-bottom: 4px;">WITHDRAWAL AMOUNT</div>
              <div style="font-size: 20px; font-weight: 700; color: #1976d2;">${amount} BCH</div>
            </div>
            <div style="padding-top: 12px; border-top: 1px solid #e0e0e0;">
              <div style="font-size: 12px; color: #757575; font-weight: 500; margin-bottom: 4px;">RECIPIENT ADDRESS</div>
              <div style="font-size: 12px; font-weight: 600; color: #424242; font-family: monospace; word-break: break-all;">${donorAddress}</div>
            </div>
          </div>

          <div style="padding: 12px 16px; background: #fff3cd; border-left: 3px solid #ff9800; border-radius: 4px;">
            <div style="color: #856404; font-size: 12px; line-height: 1.6;">
              <strong>Warning:</strong> This transaction cannot be reversed. Please verify the recipient address carefully.
            </div>
          </div>
        </div>
      `,
      html: true,
      cancel: {
        label: 'Cancel',
        color: 'grey-7',
        flat: true,
        noCaps: true,
      },
      ok: {
        label: 'Confirm Withdrawal',
        color: 'primary',
        unelevated: true,
        noCaps: true,
      },
      persistent: true,
    }).onOk(async () => {
      try {
        // Simulate withdrawal process
        await new Promise((resolve) => setTimeout(resolve, 2000))

        // Mark donations as withdrawn
        const withdrawnAmount = amount
        let remainingAmount = withdrawnAmount

        if (selectedAccount.value?.donations) {
          for (const donation of selectedAccount.value.donations) {
            if (remainingAmount <= 0) break
            if (!withdrawnDonations.value.has(donation.id)) {
              withdrawnDonations.value.add(donation.id)
              remainingAmount -= parseFloat(donation.amount)
            }
          }

          // Save to localStorage
          localStorage.setItem('withdrawnDonations', JSON.stringify([...withdrawnDonations.value]))
        }

        // Update account balance
        selectedAccount.value.available -= amount
        if (selectedAccount.value.available < 0) selectedAccount.value.available = 0

        // Refresh data
        await fetchDonations()

        $q.notify({
          type: 'positive',
          message: 'Withdrawal successful!',
          caption: `${amount} BCH sent to ${donorAddress.substring(0, 30)}...`,
          position: 'top',
          timeout: 3000,
        })

        withdrawForm.value = {
          amount: '',
          donorAddress: '',
          note: '',
        }
        withdrawDialog.value = false
      } catch (error) {
        console.error('Withdrawal error:', error)
        $q.notify({
          type: 'negative',
          message: 'Withdrawal failed',
          caption: error.message || 'Please try again',
          position: 'top',
        })
      }
    })
  } catch (error) {
    console.error('Withdrawal error:', error)
    $q.notify({
      type: 'negative',
      message: 'Withdrawal failed',
      caption: error.message || 'Please try again',
      position: 'top',
    })
  } finally {
    withdrawing.value = false
  }
}

const refreshTransactions = async () => {
  $q.notify({
    type: 'info',
    message: 'Refreshing transactions...',
    position: 'top',
    timeout: 1000,
  })

  await fetchDonations()

  $q.notify({
    type: 'positive',
    message: 'Transactions updated',
    position: 'top',
    timeout: 1500,
  })
}

const viewTransactionDetails = (transaction) => {
  const transactionDate = new Date(transaction.date).toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  })

  const formattedAmount = formatCurrency(parseFloat(transaction.amount))
  const statusColor =
    transaction.status === 'completed'
      ? 'positive'
      : transaction.status === 'pending'
        ? 'warning'
        : 'negative'
  const typeColor = '#4caf50'

  $q.dialog({
    title: '',
    message: `
      <div style="max-width: 550px; margin: 0 auto; font-family: 'Roboto', sans-serif;">
        <!-- Header -->
        <div style="padding: 20px 24px; background: white; border-bottom: 1px solid #e0e0e0; margin: -16px -16px 0 -16px;">
          <div style="font-size: 20px; font-weight: 600; color: #212121; margin-bottom: 4px;">Donation Details</div>
          <div style="font-size: 13px; color: #757575;">BiToHelp Charity Dashboard</div>
        </div>

        <!-- Content -->
        <div style="padding: 24px; background: white;">
          <!-- Status Badge -->
          <div style="margin-bottom: 24px;">
            <div style="display: inline-block; background: ${statusColor === 'positive' ? '#4caf50' : statusColor === 'warning' ? '#ff9800' : '#f44336'}; color: white; padding: 6px 16px; border-radius: 4px; font-size: 13px; font-weight: 600; text-transform: uppercase;">
              ${transaction.status}
            </div>
          </div>

          <!-- Details Table -->
          <div style="border: 1px solid #e0e0e0; border-radius: 8px; overflow: hidden;">
            <table style="width: 100%; border-collapse: collapse;">
              <tr style="background: #fafafa; border-bottom: 1px solid #e0e0e0;">
                <td style="padding: 14px 16px; font-size: 13px; color: #757575; font-weight: 500; width: 40%;">Donation Date</td>
                <td style="padding: 14px 16px; font-size: 14px; color: #212121; font-weight: 500; text-align: right;">${transactionDate}</td>
              </tr>
              <tr style="border-bottom: 1px solid #e0e0e0;">
                <td style="padding: 14px 16px; font-size: 13px; color: #757575; font-weight: 500;">Donor Name</td>
                <td style="padding: 14px 16px; font-size: 14px; color: #212121; font-weight: 600; text-align: right;">${transaction.donorName || 'Anonymous'}</td>
              </tr>
              <tr style="border-bottom: 1px solid #e0e0e0;">
                <td style="padding: 14px 16px; font-size: 13px; color: #757575; font-weight: 500;">Donor Email</td>
                <td style="padding: 14px 16px; font-size: 14px; color: #212121; font-weight: 500; text-align: right;">${transaction.donorEmail || 'N/A'}</td>
              </tr>
              <tr style="border-bottom: 1px solid #e0e0e0;">
                <td style="padding: 14px 16px; font-size: 13px; color: #757575; font-weight: 500;">Donor Contact</td>
                <td style="padding: 14px 16px; font-size: 14px; color: #212121; font-weight: 500; text-align: right;">${transaction.donorContact || 'N/A'}</td>
              </tr>
              ${
                transaction.contract && transaction.contract !== 'N/A'
                  ? `
              <tr style="border-bottom: 1px solid #e0e0e0;">
                <td style="padding: 14px 16px; font-size: 13px; color: #757575; font-weight: 500;">Contract</td>
                <td style="padding: 14px 16px; font-size: 14px; color: #1976d2; font-weight: 600; text-align: right;">${transaction.contract}</td>
              </tr>
              `
                  : ''
              }
              ${
                transaction.interval && transaction.interval !== 'N/A'
                  ? `
              <tr style="border-bottom: 1px solid #e0e0e0;">
                <td style="padding: 14px 16px; font-size: 13px; color: #757575; font-weight: 500;">Interval</td>
                <td style="padding: 14px 16px; font-size: 14px; color: #1976d2; font-weight: 600; text-align: right;">${transaction.interval}</td>
              </tr>
              `
                  : ''
              }
              <tr style="border-bottom: 1px solid #e0e0e0;">
                <td style="padding: 14px 16px; font-size: 13px; color: #757575; font-weight: 500;">Message</td>
                <td style="padding: 14px 16px; font-size: 14px; color: #212121; font-weight: 500; text-align: right;">${transaction.description || 'No message'}</td>
              </tr>
              <tr style="border-bottom: 1px solid #e0e0e0;">
                <td style="padding: 14px 16px; font-size: 13px; color: #757575; font-weight: 500;">Wallet Type</td>
                <td style="padding: 14px 16px; font-size: 14px; color: ${typeColor}; font-weight: 600; text-align: right; text-transform: uppercase;">${transaction.type}</td>
              </tr>
              <tr style="background: #f5f5f5;">
                <td style="padding: 18px 16px; font-size: 14px; color: #424242; font-weight: 600;">Amount</td>
                <td style="padding: 18px 16px; font-size: 18px; color: ${typeColor}; font-weight: 700; text-align: right;">
                  ${formattedAmount} ${transaction.type}
                </td>
              </tr>
              ${
                transaction.txid
                  ? `
              <tr style="border-top: 1px solid #e0e0e0;">
                <td style="padding: 14px 16px; font-size: 13px; color: #757575; font-weight: 500;">Transaction ID</td>
                <td style="padding: 14px 16px; font-size: 11px; color: #424242; font-family: monospace; text-align: right; word-break: break-all;">${transaction.txid}</td>
              </tr>
              `
                  : ''
              }
            </table>
          </div>

          ${
            transaction.explorerUrl
              ? `
          <div style="margin-top: 16px; text-align: center;">
            <a href="${transaction.explorerUrl}" target="_blank" style="display: inline-block; padding: 10px 24px; background: #1976d2; color: white; text-decoration: none; border-radius: 4px; font-weight: 600; font-size: 13px;">
              View on Blockchain Explorer
            </a>
          </div>
          `
              : ''
          }

          <!-- Footer Note -->
          <div style="margin-top: 20px; padding: 12px 16px; background: #f5f5f5; border-left: 3px solid #1976d2; border-radius: 4px;">
            <div style="color: #424242; font-size: 12px; line-height: 1.6;">
              <strong>Note:</strong> This donation is recorded on the Bitcoin Cash blockchain and can be verified through the transaction hash.
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
      noCaps: true,
    },
  })
}
</script>

<style scoped lang="scss">
.dashboard-page {
  overflow-x: hidden;
}

.sidebar-container {
  background-color: #8e8b8b2d;
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
  background-color: #8e8b8b2d;
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
  box-shadow:
    inset,
    0 8px 16px rgba(0, 0, 0, 0.2);
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
    color: #2196f3 !important;
  }
}

:deep(.q-tab) {
  transition: color 0.3s ease;

  &:hover {
    color: #2196f3 !important;
  }
}

:deep(.q-tab--active) {
  &:hover {
    color: #2196f3 !important;
  }
}
</style>

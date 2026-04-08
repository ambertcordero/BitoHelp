<template>
  <q-page class="wallet-user-detail q-pa-md">
    <!-- Loading state -->
    <div v-if="loading" class="column items-center justify-center" style="min-height: 60vh">
      <q-spinner-dots size="48px" color="primary" />
      <div class="q-mt-md text-grey-7">Loading user activity...</div>
    </div>

    <!-- Error state -->
    <div v-else-if="error" class="column items-center justify-center" style="min-height: 60vh">
      <q-icon name="error_outline" size="64px" color="negative" class="q-mb-md" />
      <div class="text-h6 q-mb-sm">User Not Found</div>
      <p class="text-grey-7">{{ error }}</p>
      <q-btn
        flat
        color="primary"
        label="Back to Users"
        icon="arrow_back"
        @click="$router.push('/wallet-users')"
      />
    </div>

    <!-- Content -->
    <div v-else>
      <!-- Header -->
      <div class="row items-center q-mb-lg">
        <q-btn
          flat
          round
          icon="arrow_back"
          @click="$router.push('/wallet-users')"
          class="q-mr-sm"
        />
        <div>
          <h5 class="q-mt-none q-mb-xs">
            Wallet User <strong>#{{ userData.user?.id }}</strong>
          </h5>
          <div class="text-mono text-grey-7" style="font-size: 13px">
            {{ userData.user?.wallet_address }}
          </div>
        </div>
      </div>

      <!-- Stats cards -->
      <div class="row q-col-gutter-md q-mb-lg">
        <div class="col-12 col-sm-4">
          <q-card flat bordered class="stat-card">
            <q-card-section class="text-center">
              <div class="text-caption text-grey-7">Total Donated</div>
              <div class="text-h6 text-primary text-weight-bold">
                {{ stats.total_donated?.toFixed(4) || '0.0000' }} BCH
              </div>
            </q-card-section>
          </q-card>
        </div>
        <div class="col-12 col-sm-4">
          <q-card flat bordered class="stat-card">
            <q-card-section class="text-center">
              <div class="text-caption text-grey-7">Donations</div>
              <div class="text-h6 text-weight-bold">{{ stats.donation_count || 0 }}</div>
            </q-card-section>
          </q-card>
        </div>
        <div class="col-12 col-sm-4">
          <q-card flat bordered class="stat-card">
            <q-card-section class="text-center">
              <div class="text-caption text-grey-7">Payout Approvals</div>
              <div class="text-h6 text-weight-bold">{{ stats.payout_count || 0 }}</div>
            </q-card-section>
          </q-card>
        </div>
      </div>

      <!-- Tabs: Timeline / Donations / Payouts -->
      <q-card flat bordered>
        <q-tabs v-model="activeTab" dense class="text-primary" align="left" narrow-indicator>
          <q-tab name="timeline" label="Timeline" icon="timeline" />
          <q-tab name="donations" label="Donations" icon="volunteer_activism" />
          <q-tab name="payouts" label="Payout Approvals" icon="paid" />
        </q-tabs>

        <q-separator />

        <q-tab-panels v-model="activeTab" animated>
          <!-- Timeline -->
          <q-tab-panel name="timeline" class="q-pa-none">
            <q-list separator v-if="userData.activities?.length">
              <q-item v-for="(act, i) in userData.activities" :key="i">
                <q-item-section avatar>
                  <q-avatar
                    :icon="act.type === 'donation' ? 'volunteer_activism' : 'paid'"
                    :color="act.type === 'donation' ? 'primary' : 'orange'"
                    text-color="white"
                    size="36px"
                  />
                </q-item-section>
                <q-item-section>
                  <q-item-label>
                    <q-badge
                      :color="act.type === 'donation' ? 'primary' : 'orange'"
                      :label="act.type === 'donation' ? 'Donation' : 'Payout Approval'"
                      class="q-mr-sm"
                    />
                    <template v-if="act.type === 'donation'">
                      {{ act.data.amount }} {{ act.data.coin }} → {{ act.data.recipient }}
                    </template>
                    <template v-else>
                      Cycle {{ act.data.cycle_number }}/{{ act.data.total_cycles }} —
                      {{ formatSats(act.data.payout_amount_satoshis) }} {{ act.data.coin }}
                      <q-badge
                        :color="statusColor(act.data.status)"
                        :label="act.data.status"
                        class="q-ml-sm"
                      />
                    </template>
                  </q-item-label>
                  <q-item-label caption>
                    {{ formatDate(act.timestamp) }}
                    <template v-if="act.data.cause"> · {{ act.data.cause }}</template>
                    <template v-if="act.data.txid"> · TX: {{ truncate(act.data.txid) }}</template>
                  </q-item-label>
                </q-item-section>
              </q-item>
            </q-list>
            <div v-else class="q-pa-lg text-center text-grey-6">No activity found.</div>
          </q-tab-panel>

          <!-- Donations tab -->
          <q-tab-panel name="donations" class="q-pa-none">
            <q-table
              :rows="userData.donations || []"
              :columns="donationCols"
              row-key="id"
              flat
              dense
              :pagination="{ rowsPerPage: 15 }"
            />
            <div v-if="!userData.donations?.length" class="q-pa-lg text-center text-grey-6">
              No donations.
            </div>
          </q-tab-panel>

          <!-- Payouts tab -->
          <q-tab-panel name="payouts" class="q-pa-none">
            <q-table
              :rows="userData.payout_approvals || []"
              :columns="payoutCols"
              row-key="id"
              flat
              dense
              :pagination="{ rowsPerPage: 15 }"
            />
            <div v-if="!userData.payout_approvals?.length" class="q-pa-lg text-center text-grey-6">
              No payout approvals.
            </div>
          </q-tab-panel>
        </q-tab-panels>
      </q-card>
    </div>
  </q-page>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { api } from 'boot/axios'

const route = useRoute()
const loading = ref(true)
const error = ref(null)
const userData = ref({})
const activeTab = ref('timeline')

const stats = computed(() => userData.value.stats || {})

const donationCols = [
  { name: 'id', label: 'ID', field: 'id', align: 'left', sortable: true },
  {
    name: 'date',
    label: 'Date',
    field: (row) => formatDate(row.timestamp),
    align: 'left',
    sortable: true,
  },
  { name: 'recipient', label: 'Recipient', field: 'recipient', align: 'left' },
  { name: 'amount', label: 'Amount', field: 'amount', align: 'right', sortable: true },
  { name: 'coin', label: 'Coin', field: 'coin', align: 'center' },
  { name: 'cause', label: 'Cause', field: 'cause', align: 'left' },
  { name: 'interval', label: 'Interval', field: 'interval', align: 'center' },
]

const payoutCols = [
  { name: 'id', label: 'ID', field: 'id', align: 'left', sortable: true },
  {
    name: 'date',
    label: 'Date',
    field: (row) => formatDate(row.created_at),
    align: 'left',
    sortable: true,
  },
  {
    name: 'cycle',
    label: 'Cycle',
    field: (row) => `${row.cycle_number}/${row.total_cycles}`,
    align: 'center',
  },
  {
    name: 'amount',
    label: 'Amount (sats)',
    field: 'payout_amount_satoshis',
    align: 'right',
    sortable: true,
  },
  { name: 'coin', label: 'Coin', field: 'coin', align: 'center' },
  { name: 'status', label: 'Status', field: 'status', align: 'center' },
  { name: 'txid', label: 'TxID', field: (row) => truncate(row.txid || ''), align: 'left' },
]

function formatDate(ts) {
  if (!ts) return '—'
  const d = new Date(ts)
  return isNaN(d)
    ? '—'
    : d.toLocaleString('en-US', {
        month: 'short',
        day: 'numeric',
        year: 'numeric',
        hour: '2-digit',
        minute: '2-digit',
      })
}

function formatSats(sats) {
  if (!sats) return '0'
  return (Number(sats) / 1e8).toFixed(4)
}

function truncate(str) {
  if (!str || str.length <= 16) return str || ''
  return str.slice(0, 8) + '...' + str.slice(-8)
}

function statusColor(s) {
  const map = {
    pending: 'warning',
    approved: 'info',
    executed: 'positive',
    expired: 'grey',
    failed: 'negative',
  }
  return map[s] || 'grey'
}

onMounted(async () => {
  const userId = route.params.id
  try {
    const res = await api.get(`users/${userId}/activities/`)
    userData.value = res.data
  } catch (err) {
    console.error('Failed to load user activities:', err)
    error.value = err.response?.data?.error || 'Could not load user activity.'
  } finally {
    loading.value = false
  }
})
</script>

<style scoped lang="scss">
.wallet-user-detail {
  max-width: 1100px;
  margin: 0 auto;
}
.text-mono {
  font-family: 'Courier New', monospace;
}
.stat-card {
  border-radius: 12px;
}
</style>

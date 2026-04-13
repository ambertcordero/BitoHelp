<template>
  <q-page class="donation-page">
    <div
      class="main-content"
      style="
        background: linear-gradient(180deg, #b8c5f2 0%, #d5ddff 100%);
        min-height: 100vh;
        width: 100%;
        padding: 24px 40px;
      "
    >
      <div class="text-h5 text-weight-bold q-mb-md q-ml-sm" style="color: #1a1a1a"></div>

      <!-- First Section: Dropdown and Fund Card  ini !!!-->
      <div class="row q-col-gutter-md q-mb-md">
        <!-- Left: Cause Selector and Wallet/Progress ini !!! -->
        <div class="col-12 col-md-3">
          <q-select
            v-model="selectedCause"
            :options="causes"
            label="Choose for non-profit or a cause"
            filled
            bg-color="white"
            dropdown-icon="expand_more"
            class="cause-dropdown q-mb-md"
            style="border-radius: 8px; box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1)"
          >
            <template v-slot:option="scope">
              <q-item
                v-bind="scope.itemProps"
                :class="scope.opt === selectedCause ? 'bg-yellow-3' : ''"
              >
                <q-item-section>
                  <q-item-label>{{ scope.opt }}</q-item-label>
                </q-item-section>
              </q-item>
            </template>
          </q-select>

          <!-- Wallet and Progress ini !!!-->
          <div class="q-pa-md">
            <!-- Bitcoin Wallet ini !!!-->
            <div
              class="wallet-box q-pa-sm q-mb-sm"
              style="
                background: rgba(120, 145, 255, 0.35);
                border-radius: 6px;
                border: 1px solid rgba(255, 255, 255, 0.9);
              "
            >
              <div class="row items-center justify-between no-wrap">
                <div class="text-body2 text-weight-medium" style="color: #ffffff">
                  Bitcoin Wallet: {{ walletAddress }}
                </div>
                <q-btn
                  round
                  flat
                  dense
                  icon="content_copy"
                  text-color="white"
                  size="sm"
                  @click="copyWallet"
                />
              </div>
            </div>

            <!-- Progress Bar ini !!!-->
            <div class="progress-wrap" style="width: calc(100% + 96px); margin-right: -48px">
              <div class="row items-center no-wrap q-gutter-sm" style="width: 100%">
                <q-linear-progress
                  :value="progress"
                  color="amber-5"
                  track-color="white"
                  size="12px"
                  rounded
                  class="col"
                  style="box-shadow: none; border: 1px solid rgba(255, 255, 255, 0.9); width: 100%"
                />
                <span
                  class="text-caption text-weight-bold"
                  style="color: #ffffff; min-width: 72px; text-align: right"
                  >{{ Math.round(progress * 100) }}% Funded</span
                >
              </div>
              <div class="text-center q-mt-xs">
                <span class="text-caption text-weight-bold" style="color: #ffffff"
                  >{{ raised }} BTC/ {{ goal }}BTC Goal</span
                >
              </div>
            </div>
          </div>
        </div>

        <!-- Right: Title, Subtitle and QR Code ini !!!-->
        <div class="col-12 col-md-9">
          <div class="q-pa-md">
            <!-- Title and QR Code Row  ini !!!-->
            <div class="row items-start q-col-gutter-md userpage-qr-row">
              <div class="col">
                <div
                  class="text-h4 text-weight-bold q-mb-lg"
                  style="color: #1a1a1a; text-align: center"
                >
                  {{ selectedCause }}
                </div>
                <div class="text-body1" style="color: #2a2a2a; text-align: center">
                  Raising Funds for Typhoon Victims
                </div>
              </div>
              <div
                class="col-auto userpage-qr"
                style="display: flex; justify-content: center; align-items: center"
              >
                <div
                  class="qr-code-box q-pa-xs"
                  style="
                    background: white;
                    border-radius: 6px;
                    border: 2px solid #ffffff;
                    box-shadow: none;
                  "
                >
                  <img
                    :src="`https://api.qrserver.com/v1/create-qr-code/?size=160x160&data=${walletAddress}`"
                    alt="QR Code"
                    class="qr-code-img"
                    style="width: 170px; height: 170px; display: block"
                  />
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Second Section: Forms and Other Content -->
      <div class="row q-col-gutter-md">
        <!-- Left Column: Donation Form ini !!!-->
        <div class="col-12 col-md-4">
          <!-- Donation Form  ini !!! -->
          <q-card
            class="q-pa-md q-mb-md"
            style="
              background: #e3edfc;
              border-radius: 10px;
              box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
              border: none;
              border-style: solid;
              border-color: #3b82f6;
            "
          >
            <div class="text-body1 text-weight-bold q-mb-md" style="color: #1a1a1a">
              Enter BTC Amount
            </div>
            <q-input
              v-model="btcAmount"
              outlined
              dense
              class="q-mb-xs"
              style="font-size: 15px; font-weight: 500"
            />
            <div class="text-caption text-grey-8 q-mb-lg">Network Fee ~0.00002 BTC</div>
            <q-btn
              label="DONATE WITH BITCOIN"
              color="primary"
              unelevated
              class="full-width"
              padding="md"
              style="font-weight: 700; font-size: 13px; letter-spacing: 0.3px"
              @click="$router.push('/donate')"
            />
          </q-card>

          <!-- Donation History ini !!! -->
          <q-card
            class="q-pa-md"
            style="
              background: #e3edfc;
              border-radius: 10px;
              box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
              border: none;
              border-style: solid;
              border-color: #3b82f6;
            "
          >
            <div class="row justify-between items-center q-mb-md">
              <span class="text-body1 text-weight-bold" style="color: #1a1a1a"
                >Your Donation History</span
              >
              <q-btn
                flat
                color="primary"
                label="View All"
                size="sm"
                dense
                class="text-weight-medium"
              />
            </div>
            <q-markup-table flat dense class="history-table" bordered separator="horizontal">
              <thead>
                <tr>
                  <th class="text-left" style="font-weight: 700">Date</th>
                  <th class="text-left" style="font-weight: 700">Fund</th>
                  <th class="text-right" style="font-weight: 700">Amount</th>
                </tr>
              </thead>
              <tbody>
                <tr v-if="donationHistory.length === 0">
                  <td colspan="3" class="text-center text-grey-7 q-pa-md">No donations yet</td>
                </tr>
                <tr v-for="item in donationHistory" :key="item.Date">
                  <td class="text-weight-medium">{{ item.Date }}</td>
                  <td>{{ item.Fund }}</td>
                  <td class="text-right text-weight-medium">{{ item.Amount }}</td>
                </tr>
              </tbody>
            </q-markup-table>
          </q-card>
        </div>

        <!-- Right Column: Transparency and Transactions  ini !!!-->
        <div class="col-12 col-md-8">
          <!-- Transparency ini !!!-->
          <q-card
            class="q-pa-md q-mb-md"
            style="
              background: #e3edfc;
              border-radius: 10px;
              box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
              border: none;
              border-style: solid;
              border-color: #3b82f6;
            "
          >
            <div class="text-h6 text-weight-bold q-mb-md" style="color: #1a1a1a">Transparency</div>

            <!-- Total Raised ini !!!-->
            <div class="row items-center justify-between q-mb-sm">
              <div class="row items-center q-gutter-sm">
                <q-avatar size="36px" color="primary" text-color="white">
                  <q-icon name="currency_bitcoin" size="20px" />
                </q-avatar>
                <div class="text-body2 text-grey-8">Total Raised</div>
              </div>
              <div class="text-h6 text-weight-bold" style="color: #1a1a1a">
                {{ totalRaised }} BTC
              </div>
            </div>

            <!-- Total Donors ini !!!-->
            <div class="row items-center justify-between">
              <div class="row items-center q-gutter-sm">
                <q-avatar size="36px" color="orange-7" text-color="white">
                  <q-icon name="people" size="20px" />
                </q-avatar>
                <div class="text-body2 text-grey-8">Total Donors</div>
              </div>
              <div class="text-h6 text-weight-bold" style="color: #1a1a1a">{{ totalDonors }}</div>
            </div>
          </q-card>

          <!-- Latest Blockchain Transactions ini !!!-->
          <q-card
            class="q-pa-md"
            style="
              background: #e3edfc;
              border-radius: 10px;
              box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
              border: none;
              border-style: solid;
              border-color: #3b82f6;
            "
          >
            <div class="text-h6 text-weight-bold q-mb-md" style="color: #1a1a1a">
              Latest Blockchain Transactions
            </div>
            <div class="transactions-list">
              <div v-if="transactions.length === 0" class="text-center q-pa-lg">
                <q-icon name="info" size="48px" color="grey-5" class="q-mb-md" />
                <div class="text-body2 text-grey-7">
                  No transactions yet. Make your first donation!
                </div>
                <q-btn
                  label="Donate Now"
                  color="primary"
                  class="q-mt-md"
                  @click="$router.push('/donate')"
                />
              </div>
              <div
                v-for="(tx, index) in transactions"
                :key="index"
                class="transaction-item row items-center justify-between q-pa-md q-mb-sm"
                style="background: #f5f5f5; border-radius: 8px; cursor: pointer"
                @click="openExplorer(tx)"
              >
                <q-tooltip>Click to view on blockchain explorer</q-tooltip>
                <div class="row items-center q-gutter-md">
                  <q-avatar size="44px" color="primary" text-color="white">
                    <q-icon name="currency_bitcoin" size="24px" />
                  </q-avatar>
                  <div>
                    <div class="text-body2 text-weight-bold" style="color: #1a1a1a">
                      {{ tx.Date }}
                    </div>
                    <div class="text-body1 text-weight-bold" style="color: #1a1a1a">
                      {{ tx.Amount }}
                    </div>
                    <div class="text-caption text-grey-8">{{ tx.Wallet }}</div>
                  </div>
                </div>
                <q-chip
                  outline
                  color="grey-7"
                  text-color="grey-9"
                  class="text-weight-medium"
                  style="padding: 8px 12px"
                >
                  <div style="text-align: center; line-height: 1.3">
                    <div style="font-size: 12px">{{ tx.Status }}</div>
                    <div style="font-size: 10px; opacity: 0.8">{{ tx.Time }}</div>
                  </div>
                </q-chip>
              </div>
            </div>
            <div class="text-right q-mt-md">
              <q-btn
                flat
                color="primary"
                label="View All BlockChain"
                class="text-weight-medium"
                dense
              />
            </div>
          </q-card>
        </div>
      </div>

      <div class="donation-footer">
        <div class="footer-brand">
          <img src="~assets/image1.png" alt="CrypToCare" />
          <div class="footer-brand-text">CrypToCare</div>
        </div>
        <div class="footer-col">
          <div class="footer-title">About Us</div>
          <div>Donate crypto</div>
          <div>Explore causes</div>
        </div>
        <div class="footer-col">
          <div class="footer-title">For donors</div>
          <div>Donate crypto</div>
          <div>Explore causes</div>
        </div>
        <div class="footer-col">
          <div class="footer-title">For nonprofits</div>
          <div>Getting started</div>
        </div>
        <div class="footer-col">
          <div class="footer-title">Resources</div>
          <div>Blog</div>
          <div>Help Center</div>
          <div>Terms of use</div>
          <div>Privacy notice</div>
          <div>Copyright © 2026, All rights reserved.</div>
        </div>
      </div>
    </div>
  </q-page>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useDonationStore } from '../stores/donation-store'
import { useNetworkStore } from '../stores/network-store'
import { useQuasar } from 'quasar'

const $q = useQuasar()
const donationStore = useDonationStore()

onMounted(() => {
  donationStore.loadDonationsFromStorage()

  if (donationStore.latestDonation) {
    $q.notify({
      type: 'positive',
      message: `Thank you for your donation to ${donationStore.latestDonation.cause}!`,
      caption: `Amount: ${donationStore.latestDonation.amount} ${donationStore.latestDonation.coin}`,
      position: 'top',
      timeout: 3000,
    })
  }
})

const selectedCause = ref(donationStore.latestDonation?.cause || 'Typhoon Relief Fund')
const causes = ['Typhoon Relief Fund', 'Educational Fund', 'Medical Fund', 'Health Fund']

const btcAmount = ref('0.01 BTC')
const walletAddress = computed(() => {
  return donationStore.latestDonation?.recipient || '1A1bcxy..9GhYz'
})

const progress = computed(() => {
  const total = donationStore.getTotalAmount
  const goalValue = 5
  return Math.min(total / goalValue, 1)
})

const raised = computed(() => {
  return donationStore.getTotalAmount.toFixed(4)
})

const goal = ref(5)

const totalRaised = computed(() => {
  return donationStore.getTotalAmount.toFixed(2)
})

const totalDonors = computed(() => {
  return donationStore.getDonationCount
})

const donationHistory = computed(() => {
  return donationStore.donationHistory.slice(0, 4).map((donation) => ({
    Date: new Date(donation.timestamp).toLocaleDateString('en-US', {
      month: 'short',
      day: 'numeric',
    }),
    Fund: donation.cause,
    Amount: `${donation.amount} ${donation.coin}`,
  }))
})

const transactions = computed(() => {
  return donationStore.donationHistory.slice(0, 4).map((donation) => {
    const date = new Date(donation.timestamp)
    const timeAgo = getTimeAgo(date)
    const shortAddress = donation.recipient
      ? `${donation.recipient.slice(0, 7)}..${donation.recipient.slice(-5)}`
      : 'N/A'

    return {
      Date: date.toLocaleDateString('en-US', { month: 'short', day: 'numeric' }),
      Amount: `${donation.amount} ${donation.coin}`,
      Wallet: shortAddress,
      Status: 'Confirmed',
      Time: timeAgo,
      txid: donation.txid,
      explorerUrl: donation.explorerUrl,
    }
  })
})

const getTimeAgo = (date) => {
  const now = new Date()
  const diffMs = now - date
  const diffMins = Math.floor(diffMs / 60000)
  const diffHours = Math.floor(diffMs / 3600000)
  const diffDays = Math.floor(diffMs / 86400000)

  if (diffMins < 1) return 'Just now'
  if (diffMins < 60) return `${diffMins} min${diffMins > 1 ? 's' : ''} ago`
  if (diffHours < 24) return `${diffHours} hour${diffHours > 1 ? 's' : ''} ago`
  return `${diffDays} day${diffDays > 1 ? 's' : ''} ago`
}

const networkStore = useNetworkStore()

const openExplorer = (tx) => {
  if (tx.explorerUrl) {
    window.open(tx.explorerUrl, '_blank')
  } else if (tx.txid) {
    window.open(`${networkStore.explorerBaseUrl}/tx/${tx.txid}`, '_blank')
  }
}

const copyWallet = () => {
  navigator.clipboard.writeText(walletAddress.value)
  alert('Wallet copied to clipboard!')
}
</script>

<style scoped>
.donation-page {
  min-height: 100vh;
  width: 100%;
  margin: 0;
  padding: 0;
  font-family:
    -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
}

.main-content {
  max-width: 100%;
  margin: 0 auto;
}

.cause-dropdown {
  font-weight: 500;
  font-size: 14px;
}

.cause-dropdown :deep(.q-field__control) {
  min-height: 56px;
  border-radius: 8px;
}

.cause-dropdown :deep(.q-field__label) {
  font-size: 13px;
  color: #5a5a5a;
}

.cause-dropdown :deep(.q-field__native) {
  font-weight: 500;
  color: #1a1a1a;
}

.fund-info-card {
  border: none;
}

.wallet-box {
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.15);
  transition: all 0.2s ease;
}

.wallet-box:hover {
  box-shadow: 0 3px 8px rgba(0, 0, 0, 0.2);
}

.qr-code-box {
  transition: transform 0.2s ease;
}

.qr-code-box:hover {
  transform: scale(1.02);
}

.wallet-progress-card {
  border: none;
}

.history-table {
  background: transparent;
}

.history-table thead th {
  font-weight: 700;
  font-size: 13px;
  color: #2a2a2a;
  padding: 12px 8px;
  background: transparent;
  border-bottom: 2px solid #e0e0e0;
}

.history-table tbody td {
  font-size: 14px;
  padding: 12px 8px;
  color: #2a2a2a;
  border-bottom: 1px solid #f0f0f0;
}

.transaction-item {
  transition: all 0.25s ease;
  border: 1px solid rgba(0, 0, 0, 0.05);
}

.transaction-item:hover {
  background: #f0f1f3 !important;
  transform: translateX(2px);
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.08);
}

.qr-box {
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.12);
}
</style>

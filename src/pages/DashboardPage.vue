<template>
  <q-page class="dashboard-page">
    <div class="row" style="min-height: 100vh">
      <div class="col-12 col-md-4 col-lg-3 sidebar-container">
        <div class="accounts-sidebar">

          <!-- ── Sidebar Header ─────────────────────────────────── -->
          <div class="sidebar-header">
            <div class="row items-center justify-between no-wrap">
              <div>
                <div class="sidebar-title">Charity Dashboard</div>
                <div class="sidebar-subtitle">{{ accounts.length }} active account{{ accounts.length !== 1 ? 's' : '' }}</div>
              </div>
              <div style="width: 38px; height: 38px; border-radius: 10px; background: #1a237e; display: flex; align-items: center; justify-content: center;">
                <q-icon name="dashboard" color="white" size="20px" />
              </div>
            </div>
            <div class="q-mt-md">
              <div class="sidebar-toggle">
                <div
                  class="sidebar-toggle__btn"
                  :class="{ 'sidebar-toggle__btn--active': activeTab === 'balances' }"
                  @click="activeTab = 'balances'"
                >
                  <q-icon name="account_balance_wallet" size="14px" class="q-mr-xs" />
                  Withdraw
                </div>
                <div
                  class="sidebar-toggle__btn"
                  :class="{ 'sidebar-toggle__btn--active': activeTab === 'status' }"
                  @click="activeTab = 'status'"
                >
                  <q-icon name="swap_horiz" size="14px" class="q-mr-xs" />
                  Status
                </div>
              </div>
            </div>
          </div>

          <!-- ── Search ─────────────────────────────────────────── -->
          <div class="q-px-md q-pt-md q-pb-xs">
            <q-input
              v-model="searchQuery"
              outlined
              dense
              placeholder="Search accounts…"
              class="sidebar-search"
              style="border-radius: 8px;"
            >
              <template v-slot:prepend>
                <q-icon name="search" color="grey-5" size="18px" />
              </template>
            </q-input>
          </div>

          <!-- ── Account Cards ──────────────────────────────────── -->
          <div class="q-px-sm q-pb-md q-pt-sm">
            <div
              v-for="account in accounts"
              :key="account.id"
              class="sidebar-account-card"
              :class="{ 'sidebar-account-card--active': selectedAccount?.id === account.id }"
              @click="selectAccount(account)"
            >
              <!-- Top row: colored avatar + name + due badge -->
              <div class="row items-start no-wrap q-mb-sm">
                <div class="sidebar-avatar">
                  <img src="~assets/paytaca.png" alt="wallet" style="width: 24px; height: 24px; object-fit: contain;" />
                </div>
                <div style="flex: 1; min-width: 0; margin-left: 10px;">
                  <div class="sidebar-account-name ellipsis">{{ account.name }}</div>
                  <div class="sidebar-account-sub">{{ account.number }}</div>
                </div>
                <q-badge
                  v-if="getAccountPayoutInfo(account)?.dueApproval?.length > 0 || getAccountPayoutInfo(account)?.dueSmart?.length > 0"
                  color="orange"
                  rounded
                  style="font-size: 10px; font-weight: 700; padding: 3px 7px; flex-shrink: 0; margin-top: 2px;"
                  label="Due"
                />
              </div>

              <!-- BCH stat blocks -->
              <div class="row q-mb-sm" style="gap: 8px;">
                <div style="flex: 1; background: #f5f7fa; border-radius: 8px; padding: 8px 10px;">
                  <div class="sidebar-stat-label">Total BCH</div>
                  <div class="sidebar-stat-value">{{ formatCurrency(account.current) }}</div>
                </div>
                <div style="flex: 1; background: #f0faf2; border-radius: 8px; padding: 8px 10px;">
                  <div class="sidebar-stat-label">Available</div>
                  <div class="sidebar-stat-value" style="color: #2e7d32;">{{ formatCurrency(account.available) }}</div>
                </div>
              </div>

              <!-- Payout action row -->
              <q-separator style="opacity: 0.08; margin-bottom: 10px;" />
              <div v-if="getAccountPayoutInfo(account)">
                <q-btn
                  v-if="getAccountPayoutInfo(account).dueApproval.length > 0"
                  unelevated color="positive" icon="mark_email_read"
                  label="Request Withdrawal" size="sm" class="full-width" no-caps
                  style="font-weight: 700; border-radius: 8px;"
                  @click.stop="handleContractWithdraw(account)"
                />
                <q-btn
                  v-else-if="getAccountPayoutInfo(account).dueSmart.length > 0"
                  unelevated color="positive" icon="account_balance_wallet"
                  label="Withdraw Now" size="sm" class="full-width" no-caps
                  style="font-weight: 700; border-radius: 8px;"
                  @click.stop="handleSmartWithdrawAll(account)"
                />
                <div
                  v-else-if="getAccountPayoutInfo(account).upcoming"
                  class="row items-center no-wrap" style="gap: 6px;"
                >
                  <q-icon name="schedule" color="blue-6" size="14px" style="flex-shrink: 0;" />
                  <span style="font-size: 11.5px; color: #546e7a; font-weight: 600;">
                    Next:
                    {{ new Date(getAccountPayoutInfo(account).upcoming.due_at).toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' }) }}
                  </span>
                </div>
                <div v-else class="row items-center no-wrap" style="gap: 6px;">
                  <q-icon name="check_circle_outline" color="grey-4" size="14px" />
                  <span style="font-size: 11px; color: #bdbdbd;">No pending withdrawals</span>
                </div>
              </div>
            </div>

            <div class="text-center q-mt-sm">
              <a href="#" class="view-all-link text-blue-7 text-weight-medium" style="text-decoration: none; font-size: 13px;">View all</a>
            </div>
          </div>

        </div>
      </div>

      <div class="col-12 col-md-8 col-lg-9 q-pa-md q-pa-lg-lg main-content">
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
            class="text-grey-6 dashboard-tabs"
            active-color="blue-5"
            indicator-color="blue-5"
            align="left"
          >
            <q-tab name="transactions" label="All Donations" />
            <q-tab name="details" label="Details" />
            <q-tab name="pending" label="Pending Withdrawals" />
          </q-tabs>

          <q-separator class="q-mb-lg" />

          <q-tab-panels v-model="detailTab" animated>
            <q-tab-panel name="transactions">
              <!-- Header -->
              <div class="row items-center justify-between q-mb-md">
                <div>
                  <div class="text-h6 text-weight-bold">Withdrawal History</div>
                  <div class="text-caption text-grey-6">All completed cycle payouts for this account</div>
                </div>
                <q-chip
                  color="green-2"
                  text-color="green-9"
                  icon="check_circle"
                  :label="`${getAccountSchedule(selectedAccount).executed.length} completed`"
                  style="font-weight: 700;"
                />
              </div>

              <!-- Empty state -->
              <div
                v-if="getAccountSchedule(selectedAccount).executed.length === 0"
                class="text-center q-py-xl"
                style="border: 2px dashed #e0e0e0; border-radius: 12px;"
              >
                <q-icon name="history" size="48px" color="grey-4" />
                <div class="text-grey-6 q-mt-sm text-weight-medium">No withdrawals yet</div>
                <div class="text-caption text-grey-4 q-mt-xs">Completed cycle payouts will appear here</div>
              </div>

              <!-- History table -->
              <q-table
                v-else
                :rows="getAccountSchedule(selectedAccount).executed"
                :columns="executedColumns"
                row-key="id"
                flat
                bordered
                :pagination="{ rowsPerPage: 15, sortBy: 'executed_at', descending: true }"
                class="transactions-table"
              >
                <template v-slot:body-cell-executed_at="props">
                  <q-td :props="props">
                    <div class="text-weight-medium" style="font-size: 13px;">
                      {{ new Date(props.row.executed_at).toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' }) }}
                    </div>
                    <div class="text-caption text-grey-6">
                      {{ new Date(props.row.executed_at).toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit' }) }}
                    </div>
                  </q-td>
                </template>
                <template v-slot:body-cell-amount="props">
                  <q-td :props="props">
                    <span class="text-weight-bold text-green-8" style="font-size: 14px;">
                      {{ (props.row.payout_amount_satoshis / 1e8).toFixed(8) }}
                    </span>
                    <span class="text-caption text-grey-6 q-ml-xs">BCH</span>
                  </q-td>
                </template>
                <template v-slot:body-cell-cycle="props">
                  <q-td :props="props" class="text-center">
                    <q-chip
                      dense
                      color="green-2"
                      text-color="green-9"
                      :label="`${props.row.cycle_number} / ${props.row.total_cycles}`"
                      style="font-size: 11px; font-weight: 700; border-radius: 6px; height: 22px;"
                    />
                  </q-td>
                </template>
                <template v-slot:body-cell-interval="props">
                  <q-td :props="props" class="text-center">
                    <q-badge color="blue-2" text-color="blue-9" :label="props.row.interval_label || '—'" />
                  </q-td>
                </template>
                <template v-slot:body-cell-txid="props">
                  <q-td :props="props">
                    <span
                      v-if="props.row.txid"
                      class="text-primary"
                      style="font-family: monospace; font-size: 12px; cursor: pointer;"
                      @click="$q.copyToClipboard(props.row.txid).then(() => $q.notify({ type: 'positive', message: 'TxID copied', position: 'top', timeout: 1500 }))"
                    >
                      {{ props.row.txid.substring(0, 18) }}&hellip;
                      <q-icon name="content_copy" size="12px" class="q-ml-xs" />
                    </span>
                    <span v-else class="text-grey-5 text-caption">—</span>
                  </q-td>
                </template>
                <template v-slot:body-cell-payout_status="props">
                  <q-td :props="props" class="text-center">
                    <q-badge color="positive" label="Completed" style="font-weight: 600;" />
                  </q-td>
                </template>
              </q-table>
            </q-tab-panel>

            <q-tab-panel name="details" class="details-panel q-pa-none">

              <!-- ── Profile Header Card ──────────────────────────────── -->
              <q-card flat class="detail-info-card" style="border-radius: 14px; margin-bottom: 16px; overflow: hidden;">
                <q-card-section class="q-pa-none">
                  <div class="row no-wrap items-stretch">

                    <!-- Left: Avatar + name + role -->
                    <div class="row items-center q-pa-lg" style="flex: 0 0 auto; min-width: 260px; border-right: 1px solid #f0f0f0; gap: 18px;">
                      <!-- Org avatar / logo -->
                      <div style="flex-shrink: 0;">
                        <div
                          v-if="nonprofitDetail?.logo_url"
                          style="width: 72px; height: 72px; border-radius: 50%; overflow: hidden; border: 3px solid #e8f0fe;"
                        >
                          <img :src="nonprofitDetail.logo_url" style="width: 100%; height: 100%; object-fit: cover;" />
                        </div>
                        <div
                          v-else
                          style="width: 72px; height: 72px; border-radius: 50%; background: linear-gradient(135deg, #1565c0, #0d47a1); display: flex; align-items: center; justify-content: center; border: 3px solid #e8f0fe; flex-shrink: 0;"
                        >
                          <span style="font-size: 28px; font-weight: 800; color: white;">
                            {{ selectedAccount.name?.charAt(0)?.toUpperCase() || 'N' }}
                          </span>
                        </div>
                      </div>
                      <!-- Name + category -->
                      <div style="min-width: 0;">
                        <div style="font-size: 18px; font-weight: 700; color: #1a237e; line-height: 1.2;" class="ellipsis">
                          {{ selectedAccount.name }}
                        </div>
                        <div class="q-mt-xs" style="display: flex; align-items: center; gap: 6px; flex-wrap: wrap;">
                          <span style="font-size: 13px; color: #1976d2; font-weight: 600;">
                            {{ nonprofitDetail?.category || 'Nonprofit' }}
                          </span>
                          <span style="color: #bdbdbd;">|</span>
                          <span style="font-size: 12px; color: #9e9e9e;">
                            {{ nonprofitDetail?.active === false ? 'Inactive' : 'Active Organization' }}
                          </span>
                        </div>
                        <q-chip
                          v-if="nonprofitDetail?.verified"
                          dense
                          color="green-2"
                          text-color="green-8"
                          icon="verified"
                          label="Verified"
                          style="font-size: 11px; font-weight: 700; margin-top: 8px;"
                        />
                        <q-chip
                          v-else
                          dense
                          color="grey-2"
                          text-color="grey-7"
                          icon="schedule"
                          label="Unverified"
                          style="font-size: 11px; margin-top: 8px;"
                        />
                      </div>
                    </div>

                    <!-- Right: Quick stats grid -->
                    <div class="row items-center q-px-lg q-py-md" style="flex: 1; gap: 0; flex-wrap: wrap;">
                      <div
                        v-for="stat in [
                          { label: 'BCH Address', value: selectedAccount.address || '—', mono: true, icon: 'account_balance_wallet' },
                          { label: 'Website', value: nonprofitDetail?.website || '—', link: nonprofitDetail?.website, icon: 'language' },
                          { label: 'Email', value: nonprofitDetail?.email || selectedAccount.email || '—', icon: 'mail_outline' },
                          { label: 'Phone', value: nonprofitDetail?.phone || '—', icon: 'phone' },
                        ]"
                        :key="stat.label"
                        style="min-width: 50%; padding: 10px 16px 10px 0;"
                      >
                        <div class="text-caption text-grey-5" style="font-size: 11px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 3px;">
                          <q-icon :name="stat.icon" size="12px" class="q-mr-xs" />{{ stat.label }}
                        </div>
                        <a
                          v-if="stat.link"
                          :href="stat.link"
                          target="_blank"
                          style="font-size: 13px; font-weight: 600; color: #1976d2; word-break: break-all; text-decoration: none;"
                        >{{ stat.value }}</a>
                        <div
                          v-else
                          :style="{ fontSize: '13px', fontWeight: 600, color: '#212121', wordBreak: 'break-all', fontFamily: stat.mono ? 'monospace' : 'inherit' }"
                        >{{ stat.value }}</div>
                      </div>
                    </div>

                  </div>
                </q-card-section>
              </q-card>

              <!-- ── Two column cards ─────────────────────────────────── -->
              <div class="row q-col-gutter-md">

                <!-- Wallet & Financial Information -->
                <div class="col-12 col-md-6">
                  <q-card flat class="detail-info-card" style="border-radius: 14px; height: 100%;">
                    <q-card-section class="q-pb-xs">
                      <div class="row items-center justify-between">
                        <div style="font-size: 14px; font-weight: 700; color: #37474f;">Wallet Information</div>
                        <q-icon name="account_balance_wallet" color="blue-4" size="20px" />
                      </div>
                    </q-card-section>
                    <q-separator />
                    <q-card-section class="q-pt-md">
                      <div class="row q-col-gutter-md">

                        <div class="col-6">
                          <div class="text-caption text-grey-5" style="font-size: 11px; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 4px;">Wallet Type</div>
                          <div style="font-size: 14px; font-weight: 700; color: #212121;">{{ selectedAccount.type || '—' }}</div>
                        </div>

                        <div class="col-6">
                          <div class="text-caption text-grey-5" style="font-size: 11px; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 4px;">Network Fee Paid</div>
                          <div style="font-size: 14px; font-weight: 700; color: #212121;">{{ selectedAccount.totalFees || '0' }} BCH</div>
                        </div>

                        <div class="col-12">
                          <div class="text-caption text-grey-5" style="font-size: 11px; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 4px;">BCH Address</div>
                          <div
                            style="font-size: 12px; font-weight: 600; font-family: monospace; color: #1565c0; background: #e8f0fe; border-radius: 6px; padding: 8px 12px; word-break: break-all; cursor: pointer;"
                            @click="$q.copyToClipboard(selectedAccount.address).then(() => $q.notify({ type: 'positive', message: 'Address copied', position: 'top', timeout: 1500 }))"
                          >
                            {{ selectedAccount.address || '—' }}
                            <q-icon name="content_copy" size="13px" class="q-ml-xs text-blue-8" />
                          </div>
                        </div>

                        <div class="col-6">
                          <div class="text-caption text-grey-5" style="font-size: 11px; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 4px;">Total Received</div>
                          <div style="font-size: 18px; font-weight: 800; color: #1565c0;">
                            {{ formatCurrency(selectedAccount.totalReceived) }}
                            <span style="font-size: 12px; font-weight: 600; color: #90a4ae;">BCH</span>
                          </div>
                        </div>

                        <div class="col-6">
                          <div class="text-caption text-grey-5" style="font-size: 11px; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 4px;">Available Balance</div>
                          <div style="font-size: 18px; font-weight: 800; color: #2e7d32;">
                            {{ formatCurrency(selectedAccount.available) }}
                            <span style="font-size: 12px; font-weight: 600; color: #90a4ae;">BCH</span>
                          </div>
                        </div>

                      </div>
                    </q-card-section>
                  </q-card>
                </div>

                <!-- Donation Statistics -->
                <div class="col-12 col-md-6">
                  <q-card flat class="detail-info-card" style="border-radius: 14px; height: 100%;">
                    <q-card-section class="q-pb-xs">
                      <div class="row items-center justify-between">
                        <div style="font-size: 14px; font-weight: 700; color: #37474f;">Donation Statistics</div>
                        <q-icon name="bar_chart" color="purple-4" size="20px" />
                      </div>
                    </q-card-section>
                    <q-separator />
                    <q-card-section class="q-pt-md">
                      <div class="row q-col-gutter-md">

                        <div class="col-6">
                          <div class="text-caption text-grey-5" style="font-size: 11px; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 4px;">Total Donations</div>
                          <div style="font-size: 14px; font-weight: 700; color: #212121;">{{ selectedAccount.transactionCount || 0 }}</div>
                        </div>

                        <div class="col-6">
                          <div class="text-caption text-grey-5" style="font-size: 11px; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 4px;">Active Since</div>
                          <div style="font-size: 14px; font-weight: 700; color: #212121;">
                            {{ nonprofitDetail?.created_at ? new Date(nonprofitDetail.created_at).toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' }) : '—' }}
                          </div>
                        </div>

                        <div class="col-6">
                          <div class="text-caption text-grey-5" style="font-size: 11px; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 4px;">First Donation</div>
                          <div style="font-size: 14px; font-weight: 700; color: #212121;">{{ selectedAccount.firstDonation || '—' }}</div>
                        </div>

                        <div class="col-6">
                          <div class="text-caption text-grey-5" style="font-size: 11px; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 4px;">Last Donation</div>
                          <div style="font-size: 14px; font-weight: 700; color: #212121;">{{ selectedAccount.lastDonation || '—' }}</div>
                        </div>

                        <div class="col-12">
                          <div class="text-caption text-grey-5" style="font-size: 11px; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 6px;">Charity Description</div>
                          <div style="font-size: 13px; color: #546e7a; line-height: 1.6; background: #fafafa; border-radius: 8px; padding: 10px 12px; border: 1px solid #f0f0f0;">
                            {{ nonprofitDetail?.description || 'No description available.' }}
                          </div>
                        </div>

                      </div>
                    </q-card-section>
                  </q-card>
                </div>

              </div>

              <!-- ── Donation Analytics Charts ─────────────────────────── -->
              <div class="q-mt-lg">
                <div class="row items-center q-mb-md">
                  <div class="dash-chart-section-title">Donation Analytics</div>
                </div>

                <div class="row q-col-gutter-md">

                  <!-- Line: BCH Received Over Time -->
                  <div class="col-12 col-md-6">
                    <q-card flat class="detail-info-card dash-chart-card">
                      <q-card-section class="q-pb-xs">
                        <div class="row items-center justify-between">
                          <div>
                            <div class="dash-chart-card-title">Donation Trend</div>
                            <div class="dash-chart-card-sub">BCH received over time</div>
                          </div>
                          <q-icon name="show_chart" color="blue-4" size="20px" />
                        </div>
                      </q-card-section>
                      <q-separator />
                      <q-card-section class="q-pa-md">
                        <div class="dash-chart-canvas">
                          <LineChart :data="dashLineChartData" :options="dashLineChartOptions" />
                        </div>
                      </q-card-section>
                    </q-card>
                  </div>

                  <!-- Bar: BCH by Wallet Type -->
                  <div class="col-12 col-md-6">
                    <q-card flat class="detail-info-card dash-chart-card">
                      <q-card-section class="q-pb-xs">
                        <div class="row items-center justify-between">
                          <div>
                            <div class="dash-chart-card-title">Donations by Wallet Type</div>
                            <div class="dash-chart-card-sub">Total BCH per wallet</div>
                          </div>
                          <q-icon name="bar_chart" color="purple-4" size="20px" />
                        </div>
                      </q-card-section>
                      <q-separator />
                      <q-card-section class="q-pa-md">
                        <div class="dash-chart-canvas">
                          <BarChart :data="dashBarChartData" :options="dashBarChartOptions" />
                        </div>
                      </q-card-section>
                    </q-card>
                  </div>

                </div>
              </div>

            </q-tab-panel>

            <q-tab-panel name="pending">
              <!-- Header -->
              <div class="row items-center justify-between q-mb-md">
                <div>
                  <div class="text-h6 text-weight-bold">Scheduled Withdrawals</div>
                  <div class="text-caption text-grey-6">Full cycle schedule for each active contract</div>
                </div>
                <q-chip
                  color="orange-2"
                  text-color="orange-9"
                  icon="pending_actions"
                  :label="`${pendingScheduleGroups.length} contract${pendingScheduleGroups.length !== 1 ? 's' : ''}`"
                  style="font-weight: 700;"
                />
              </div>

              <!-- Empty state -->
              <div
                v-if="pendingScheduleGroups.length === 0"
                class="text-center q-py-xl"
                style="border: 2px dashed #e0e0e0; border-radius: 12px;"
              >
                <q-icon name="pending_actions" size="48px" color="grey-4" />
                <div class="text-grey-6 q-mt-sm text-weight-medium">No scheduled withdrawals</div>
                <div class="text-caption text-grey-4 q-mt-xs">Active contract cycles will appear here once set up</div>
              </div>

              <!-- Contract schedule groups -->
              <div v-else>
                <div
                  v-for="group in pendingScheduleGroups"
                  :key="group.donationId"
                  class="q-mb-xl"
                >
                  <!-- Contract header card -->
                  <div
                    :style="{
                      background: group.hasDue
                        ? 'linear-gradient(135deg, #fff8e1 0%, #fff3cd 100%)'
                        : 'linear-gradient(135deg, #e8f0fe 0%, #ede7f6 100%)',
                      borderRadius: '12px',
                      padding: '16px 20px',
                      marginBottom: '10px',
                      border: group.hasDue ? '1px solid #ffcc02' : '1px solid #c5d8ff',
                    }"
                  >
                    <div class="row items-center justify-between no-wrap">
                      <div style="min-width: 0; flex: 1;">
                        <div style="font-size: 16px; font-weight: 700; color: #1a237e;" class="ellipsis">
                          {{ group.donorName }}
                        </div>
                        <div class="text-caption q-mt-xs" style="color: #546e7a;">
                          <q-icon name="schedule" size="13px" />
                          <span class="q-ml-xs">{{ group.intervalLabel }} interval</span>
                          &nbsp;&middot;&nbsp;
                          <q-icon name="currency_bitcoin" size="13px" />
                          <span class="q-ml-xs">{{ group.amountBch }} BCH per cycle</span>
                          &nbsp;&middot;&nbsp;
                          <q-icon name="repeat" size="13px" />
                          <span class="q-ml-xs">{{ group.cyclesRemaining }} of {{ group.totalCycles }} cycles remaining</span>
                        </div>
                      </div>
                      <div class="q-ml-md row items-center q-gutter-sm">
                        <q-chip
                          dense
                          :color="group.hasDue ? 'orange-2' : 'blue-3'"
                          :text-color="group.hasDue ? 'orange-9' : 'blue-9'"
                          :label="group.hasDue ? 'Due Now' : 'On Schedule'"
                          :icon="group.hasDue ? 'warning' : 'event'"
                          style="font-weight: 700;"
                        />
                        <q-badge
                          v-if="group.payoutMode === 'smart'"
                          color="blue-grey-3"
                          text-color="blue-grey-9"
                          label="Smart"
                        />
                        <q-badge
                          v-else
                          color="deep-orange-2"
                          text-color="deep-orange-9"
                          label="Approval"
                        />
                      </div>
                    </div>
                  </div>

                  <!-- Cycle timeline table -->
                  <div style="border: 1px solid #e3e8ef; border-radius: 10px; overflow: hidden;">
                    <!-- Table header -->
                    <div
                      class="row items-center"
                      style="background: #f7f9fc; padding: 8px 18px; border-bottom: 1px solid #e3e8ef;"
                    >
                      <div class="col-2" style="font-size: 10.5px; font-weight: 700; color: #90a4ae; text-transform: uppercase; letter-spacing: 0.5px;">Cycle</div>
                      <div class="col-4" style="font-size: 10.5px; font-weight: 700; color: #90a4ae; text-transform: uppercase; letter-spacing: 0.5px;">Scheduled Date</div>
                      <div class="col-3 text-right" style="font-size: 10.5px; font-weight: 700; color: #90a4ae; text-transform: uppercase; letter-spacing: 0.5px;">Amount</div>
                      <div class="col-3 text-center" style="font-size: 10.5px; font-weight: 700; color: #90a4ae; text-transform: uppercase; letter-spacing: 0.5px;">Status</div>
                    </div>

                    <!-- Cycle rows -->
                    <div
                      v-for="(cycle, idx) in group.cycles"
                      :key="cycle.cycleNumber"
                      class="row items-center"
                      :style="{
                        padding: '11px 18px',
                        borderBottom: idx < group.cycles.length - 1 ? '1px solid #f0f4f8' : 'none',
                        background: cycle.status === 'due' ? '#fffde7' : idx % 2 === 0 ? '#ffffff' : '#fafbfc',
                        transition: 'background 0.2s',
                      }"
                    >
                      <!-- Cycle # badge -->
                      <div class="col-2">
                        <q-chip
                          dense
                          :color="cycle.status === 'due' ? 'orange-3' : cycle.status === 'next' ? 'blue-3' : 'blue-grey-2'"
                          :text-color="cycle.status === 'due' ? 'orange-10' : cycle.status === 'next' ? 'blue-10' : 'blue-grey-8'"
                          :label="`#${cycle.cycleNumber}`"
                          style="font-size: 11px; font-weight: 800; border-radius: 6px; height: 22px;"
                        />
                      </div>

                      <!-- Date & time -->
                      <div class="col-4">
                        <div style="font-size: 13px; font-weight: 600; color: #263238;">
                          {{ cycle.dueAt.toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' }) }}
                        </div>
                        <div style="font-size: 11px; color: #9e9e9e;">
                          {{ cycle.dueAt.toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit' }) }}
                        </div>
                      </div>

                      <!-- Amount -->
                      <div class="col-3 text-right">
                        <div style="font-size: 13px; font-weight: 700; color: #1565c0;">{{ cycle.amountBch }}</div>
                        <div style="font-size: 10px; color: #90a4ae;">BCH</div>
                      </div>

                      <!-- Status + optional Withdraw button -->
                      <div class="col-3 text-center">
                        <div class="row justify-center items-center q-gutter-xs">
                          <q-btn
                            v-if="cycle.status === 'due' && cycle.payoutId"
                            unelevated
                            color="positive"
                            label="Withdraw"
                            size="xs"
                            no-caps
                            style="font-weight: 700; min-width: 80px;"
                            @click="handleSmartWithdraw({ duePayoutId: cycle.payoutId, amount: parseFloat(cycle.amountBch), donorName: group.donorName, nonprofit: selectedAccount.nonprofitId })"
                          />
                          <q-badge
                            v-else-if="cycle.status === 'due'"
                            color="orange"
                            label="Due Now"
                            style="font-weight: 700;"
                          />
                          <q-badge
                            v-else-if="cycle.status === 'next'"
                            color="blue"
                            text-color="white"
                            label="Next"
                            style="font-weight: 600;"
                          />
                          <q-badge
                            v-else-if="cycle.status === 'upcoming'"
                            color="blue-grey-3"
                            text-color="blue-grey-8"
                            label="Upcoming"
                          />
                          <q-badge
                            v-else
                            color="grey-3"
                            text-color="grey-8"
                            label="Scheduled"
                          />
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
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

          <q-card flat class="q-mt-md status-table-card">
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

    <!-- ═══════════════════════════════════════════════════════════
         Transaction Detail Dialog
         ═══════════════════════════════════════════════════════════ -->
    <q-dialog v-model="txDetailDialog.open">
      <q-card class="tx-detail-dialog">

        <!-- Header -->
        <div class="tx-detail-header">
          <div class="row items-center justify-between no-wrap">
            <div>
              <div class="tx-detail-title">Donation Details</div>
              <div class="tx-detail-sub">BitoHelp Charity Dashboard</div>
            </div>
            <q-btn flat round dense icon="close" @click="txDetailDialog.open = false" class="tx-close-btn" />
          </div>
        </div>

        <q-card-section class="q-pt-md q-pb-sm">
          <!-- Status badge -->
          <q-badge
            :color="txDetailDialog.statusColor"
            :label="txDetailDialog.data?.status?.toUpperCase()"
            style="font-size: 12px; font-weight: 700; padding: 5px 14px; border-radius: 6px; letter-spacing: 0.5px;"
          />
        </q-card-section>

        <!-- Details rows -->
        <q-card-section class="q-pt-xs q-pb-md">
          <div class="tx-detail-table">
            <div class="tx-detail-row" v-for="row in txDetailDialog.rows" :key="row.label">
              <div class="tx-detail-label">{{ row.label }}</div>
              <div class="tx-detail-value" :style="row.style">{{ row.value }}</div>
            </div>
            <div class="tx-detail-row tx-detail-row--amount">
              <div class="tx-detail-label" style="font-weight: 700;">Amount</div>
              <div class="tx-detail-value" style="font-size: 18px; font-weight: 800; color: #4caf50;">
                {{ txDetailDialog.formattedAmount }} {{ txDetailDialog.data?.type }}
              </div>
            </div>
            <div class="tx-detail-row" v-if="txDetailDialog.data?.txid">
              <div class="tx-detail-label">Transaction ID</div>
              <div class="tx-detail-value" style="font-family: monospace; font-size: 11px; word-break: break-all;">
                {{ txDetailDialog.data.txid }}
              </div>
            </div>
          </div>

          <!-- Explorer link -->
          <div v-if="txDetailDialog.data?.explorerUrl" class="text-center q-mt-md">
            <q-btn
              unelevated color="primary" icon="open_in_new"
              label="View on Blockchain Explorer" no-caps
              :href="txDetailDialog.data.explorerUrl" target="_blank"
              style="border-radius: 8px;"
            />
          </div>

          <!-- Note -->
          <div class="tx-detail-note q-mt-md">
            <q-icon name="info_outline" size="14px" class="q-mr-xs" />
            <span>This donation is recorded on the Bitcoin Cash blockchain and can be verified through the transaction hash.</span>
          </div>
        </q-card-section>

        <q-card-actions align="right" class="q-px-md q-pb-md">
          <q-btn unelevated color="primary" label="Close" no-caps style="border-radius: 8px; min-width: 90px;" @click="txDetailDialog.open = false" />
        </q-card-actions>
      </q-card>
    </q-dialog>

    <!-- ═══════════════════════════════════════════════════════════
         Professional Withdraw Confirm Dialog
         ═══════════════════════════════════════════════════════════ -->
    <q-dialog v-model="withdrawConfirmDialog.open" persistent>
      <q-card style="min-width: 480px; max-width: 560px; border-radius: 16px; overflow: hidden; box-shadow: 0 20px 60px rgba(0,0,0,0.18);">

        <!-- ── Gradient Header ──────────────────────────────────── -->
        <div
          :style="{
            background: withdrawConfirmDialog.mode === 'inbox_approval'
              ? 'linear-gradient(135deg, #f57c00 0%, #e64a19 100%)'
              : 'linear-gradient(135deg, #1565c0 0%, #0d47a1 100%)',
            padding: '20px 24px',
          }"
        >
          <div class="row items-center no-wrap">
            <div
              style="width: 44px; height: 44px; border-radius: 50%; background: rgba(255,255,255,0.18); display: flex; align-items: center; justify-content: center; margin-right: 14px; flex-shrink: 0;"
            >
              <q-icon
                :name="withdrawConfirmDialog.mode === 'inbox_approval' ? 'mark_email_read' : 'account_balance_wallet'"
                color="white"
                size="22px"
              />
            </div>
            <div style="flex: 1; min-width: 0;">
              <div class="text-white text-weight-bold" style="font-size: 17px; line-height: 1.2;">
                {{ withdrawConfirmDialog.mode === 'inbox_approval' ? 'Request Withdrawal Approval' : 'Confirm Withdrawal' }}
              </div>
              <div class="text-white ellipsis" style="opacity: 0.78; font-size: 12.5px; margin-top: 2px;">
                {{ withdrawConfirmDialog.accountName }}
              </div>
            </div>
            <q-btn
              icon="close"
              flat
              round
              dense
              color="white"
              size="sm"
              :disable="withdrawConfirmDialog.loading"
              @click="withdrawConfirmDialog.open = false"
            />
          </div>
        </div>

        <!-- ── Summary Stats Row ────────────────────────────────── -->
        <div class="q-px-lg q-pt-lg q-pb-sm">
          <div class="row q-col-gutter-sm">

            <!-- Total BCH -->
            <div class="col-4">
              <div style="background: #e8f0fe; border-radius: 10px; padding: 14px 12px; border: 1px solid #c5d8ff; text-align: center;">
                <q-icon name="currency_bitcoin" color="blue-8" size="20px" />
                <div style="font-size: 11px; font-weight: 700; color: #1a56db; text-transform: uppercase; letter-spacing: 0.6px; margin-top: 4px;">Total Amount</div>
                <div style="font-size: 17px; font-weight: 800; color: #1a56db; margin-top: 2px; line-height: 1;">
                  {{ withdrawConfirmDialog.totalBch }}
                </div>
                <div style="font-size: 11px; color: #6b8cc7; margin-top: 1px;">BCH</div>
              </div>
            </div>

            <!-- Payout Count -->
            <div class="col-4">
              <div style="background: #e6f4ea; border-radius: 10px; padding: 14px 12px; border: 1px solid #b7dcc3; text-align: center;">
                <q-icon name="receipt_long" color="green-8" size="20px" />
                <div style="font-size: 11px; font-weight: 700; color: #1e6b3a; text-transform: uppercase; letter-spacing: 0.6px; margin-top: 4px;">Payouts Due</div>
                <div style="font-size: 17px; font-weight: 800; color: #1e6b3a; margin-top: 2px; line-height: 1;">
                  {{ withdrawConfirmDialog.payouts.length }}
                </div>
                <div style="font-size: 11px; color: #5a9970; margin-top: 1px;">scheduled</div>
              </div>
            </div>

            <!-- Date & Time -->
            <div class="col-4">
              <div style="background: #fef3e8; border-radius: 10px; padding: 14px 12px; border: 1px solid #f5d4ae; text-align: center;">
                <q-icon name="schedule" color="orange-9" size="20px" />
                <div style="font-size: 11px; font-weight: 700; color: #c45e0a; text-transform: uppercase; letter-spacing: 0.6px; margin-top: 4px;">Executed On</div>
                <div style="font-size: 12px; font-weight: 800; color: #c45e0a; margin-top: 2px; line-height: 1.2;">
                  {{ fmtDialogDate(new Date()) }}
                </div>
                <div style="font-size: 11px; color: #c07940; margin-top: 1px;">{{ fmtDialogTime(new Date()) }}</div>
              </div>
            </div>

          </div>
        </div>

        <!-- ── Payout Details Table ──────────────────────────────── -->
        <div class="q-px-lg q-pb-sm">
          <div style="font-size: 11px; font-weight: 700; color: #78909c; text-transform: uppercase; letter-spacing: 0.7px; margin-bottom: 8px;">
            Payout Details
          </div>
          <div style="border: 1px solid #e3e8ef; border-radius: 10px; overflow: hidden;">

            <!-- Table Header -->
            <div class="row" style="background: #f5f7fa; padding: 8px 14px; border-bottom: 1px solid #e3e8ef;">
              <div class="col-5" style="font-size: 10.5px; font-weight: 700; color: #90a4ae; text-transform: uppercase; letter-spacing: 0.5px;">Donor</div>
              <div class="col-3 text-right" style="font-size: 10.5px; font-weight: 700; color: #90a4ae; text-transform: uppercase; letter-spacing: 0.5px;">Amount</div>
              <div class="col-2 text-center" style="font-size: 10.5px; font-weight: 700; color: #90a4ae; text-transform: uppercase; letter-spacing: 0.5px;">Cycle</div>
              <div class="col text-right" style="font-size: 10.5px; font-weight: 700; color: #90a4ae; text-transform: uppercase; letter-spacing: 0.5px;">Scheduled</div>
            </div>

            <!-- Table Rows -->
            <div
              v-for="(payout, idx) in withdrawConfirmDialog.payouts"
              :key="payout.id"
              class="row items-center"
              :style="{
                padding: '10px 14px',
                borderBottom: idx < withdrawConfirmDialog.payouts.length - 1 ? '1px solid #f0f4f8' : 'none',
                background: idx % 2 === 0 ? '#ffffff' : '#fafbfc',
              }"
            >
              <div class="col-5" style="min-width: 0;">
                <div class="ellipsis" style="font-size: 13px; font-weight: 600; color: #1a237e;">{{ payout.donorName }}</div>
                <div class="ellipsis" style="font-size: 11px; color: #9e9e9e;">{{ payout.donorEmail || '—' }}</div>
              </div>
              <div class="col-3 text-right">
                <div style="font-size: 13px; font-weight: 700; color: #1565c0;">{{ payout.amountBch }}</div>
                <div style="font-size: 10px; color: #90a4ae;">BCH</div>
              </div>
              <div class="col-2 text-center">
                <q-chip
                  dense
                  :label="`${payout.cycleNumber} / ${payout.totalCycles}`"
                  color="blue-2"
                  text-color="blue-9"
                  style="font-size: 10px; font-weight: 700; border-radius: 6px; height: 20px;"
                />
              </div>
              <div class="col text-right">
                <div style="font-size: 11px; font-weight: 600; color: #e65100;">{{ fmtDialogDateShort(new Date(payout.dueAt)) }}</div>
                <div style="font-size: 10px; color: #9e9e9e;">{{ fmtDialogTime(new Date(payout.dueAt)) }}</div>
              </div>
            </div>

          </div>
        </div>

        <!-- ── Mode Notice ───────────────────────────────────────── -->
        <div class="q-px-lg q-pb-md">
          <!-- inbox_approval notice -->
          <div
            v-if="withdrawConfirmDialog.mode === 'inbox_approval'"
            style="background: #fff8e1; border-left: 4px solid #ffc107; border-radius: 6px; padding: 10px 14px; display: flex; align-items: flex-start; gap: 8px;"
          >
            <q-icon name="mail_outline" color="orange-8" size="16px" style="margin-top: 1px; flex-shrink: 0;" />
            <div style="font-size: 12px; color: #6d4c00; line-height: 1.5;">
              <strong>Approval Required</strong> — An email will be sent to each donor asking them to approve this scheduled withdrawal. Funds will only move once they confirm.
            </div>
          </div>
          <!-- smart notice -->
          <div
            v-else
            style="background: #e8f5e9; border-left: 4px solid #43a047; border-radius: 6px; padding: 10px 14px; display: flex; align-items: flex-start; gap: 8px;"
          >
            <q-icon name="bolt" color="green-8" size="16px" style="margin-top: 1px; flex-shrink: 0;" />
            <div style="font-size: 12px; color: #1b5e20; line-height: 1.5;">
              <strong>Smart Withdrawal</strong> — This payout will execute automatically on the Bitcoin Cash blockchain. This action cannot be undone.
            </div>
          </div>
        </div>

        <q-separator />

        <!-- ── Action Buttons ────────────────────────────────────── -->
        <q-card-actions align="right" class="q-pa-md" style="gap: 8px;">
          <q-btn
            flat
            label="Cancel"
            color="grey-7"
            no-caps
            :disable="withdrawConfirmDialog.loading"
            @click="withdrawConfirmDialog.open = false"
          />
          <q-btn
            unelevated
            :label="withdrawConfirmDialog.mode === 'inbox_approval' ? 'Send Approval Emails' : 'Confirm Withdrawal'"
            :color="withdrawConfirmDialog.mode === 'inbox_approval' ? 'deep-orange' : 'positive'"
            no-caps
            style="min-width: 168px; font-weight: 600; letter-spacing: 0.3px;"
            :loading="withdrawConfirmDialog.loading"
            :icon="withdrawConfirmDialog.mode === 'inbox_approval' ? 'send' : 'check_circle'"
            @click="executeWithdrawConfirm"
          />
        </q-card-actions>

      </q-card>
    </q-dialog>

  </q-page>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted, watch } from 'vue'
import { useQuasar } from 'quasar'
import { Line as LineChart, Bar as BarChart } from 'vue-chartjs'
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  Title,
  Tooltip,
  Legend,
  Filler
} from 'chart.js'

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  Title,
  Tooltip,
  Legend,
  Filler
)
import { api } from 'boot/axios'
import bchImg from 'src/assets/bch.png'
import projectImg from 'src/assets/project.png'
import transactionImg from 'src/assets/transaction.png'

const $q = useQuasar()

// Map of nonprofitId → sidebar button state
const nonprofitPayoutsMap = ref({})
// Map of nonprofitId → { pending: [], executed: [] } for schedule/history tabs
const allPayoutsMap = ref({})
// Full nonprofit detail fetched from API
const nonprofitDetail = ref(null)

const fetchNonprofitDetail = async (nonprofitId) => {
  if (!nonprofitId) return
  try {
    const res = await api.get(`nonprofits/${nonprofitId}/`)
    nonprofitDetail.value = res.data
  } catch {
    nonprofitDetail.value = null
  }
}

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

// ── Transaction Detail Dialog ─────────────────────────────────────────────────
const txDetailDialog = ref({
  open: false,
  data: null,
  statusColor: 'positive',
  formattedAmount: '',
  rows: [],
})

// ── Withdraw Confirm Dialog ───────────────────────────────────────────────────
const withdrawConfirmDialog = ref({
  open: false,
  mode: 'smart', // 'smart' | 'inbox_approval'
  accountName: '',
  payouts: [],   // [{ id, donorName, donorEmail, amountBch, cycleNumber, totalCycles, dueAt }]
  totalBch: '0',
  loading: false,
  onConfirm: null,
})

const fmtDialogDate = (d) =>
  d.toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' })
const fmtDialogDateShort = (d) =>
  d.toLocaleDateString('en-US', { month: 'short', day: 'numeric' })
const fmtDialogTime = (d) =>
  d.toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit' })

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
    payoutMode: donation.payout_mode || 'smart',
    withdrawn: withdrawnDonations.value.has(donation.id),
    duePayoutId: null, // filled after payout fetch
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
    nonprofitId: data.donations[0]?.nonprofit ?? null,
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

  // Fetch scheduled payout info for each nonprofit
  newAccounts.forEach((acct) => {
    if (acct.nonprofitId) fetchPayoutsForNonprofit(acct.nonprofitId)
  })
}

const fetchPayoutsForNonprofit = async (nonprofitId) => {
  try {
    const [pendingRes, executedRes] = await Promise.all([
      api.get('payouts/', { params: { nonprofit_id: nonprofitId, status: 'pending' } }),
      api.get('payouts/', { params: { nonprofit_id: nonprofitId, status: 'executed' } }),
    ])
    const pending = Array.isArray(pendingRes.data) ? pendingRes.data : []
    const executed = Array.isArray(executedRes.data) ? executedRes.data : []

    // Store full data for schedule/history tabs
    allPayoutsMap.value = {
      ...allPayoutsMap.value,
      [nonprofitId]: { pending, executed },
    }

    // Sidebar button state
    const now = new Date()
    const due = pending.filter((p) => new Date(p.due_at) <= now)
    nonprofitPayoutsMap.value = {
      ...nonprofitPayoutsMap.value,
      [nonprofitId]: {
        dueApproval: due.filter((p) => p.payout_mode === 'inbox_approval'),
        dueSmart: due.filter((p) => p.payout_mode !== 'inbox_approval'),
        upcoming: pending.find((p) => new Date(p.due_at) > now) ?? null,
      },
    }

    // Stamp duePayoutId on matching smart transaction rows
    due
      .filter((p) => p.payout_mode !== 'inbox_approval')
      .forEach((payout) => {
        const stamp = (list) => {
          const row = list.value.find((t) => payout.donation_id && t.id === payout.donation_id)
          if (row) row.duePayoutId = payout.id
        }
        stamp(transactions)
        stamp(allTransactions)
      })
  } catch {
    // silently ignore
  }
}

const getAccountPayoutInfo = (account) => {
  if (!account.nonprofitId) return null
  return nonprofitPayoutsMap.value[account.nonprofitId] ?? null
}

const getAccountSchedule = (account) => {
  if (!account?.nonprofitId) return { pending: [], executed: [] }
  return allPayoutsMap.value[account.nonprofitId] ?? { pending: [], executed: [] }
}


onMounted(() => {
  fetchDonations()
  const saved = localStorage.getItem('withdrawnDonations')
  if (saved) {
    withdrawnDonations.value = new Set(JSON.parse(saved))
  }
})

// Refetch donations + payouts when selectedAccount changes
watch(selectedAccount, (acct) => {
  fetchDonations()
  if (acct?.nonprofitId) {
    fetchPayoutsForNonprofit(acct.nonprofitId)
    fetchNonprofitDetail(acct.nonprofitId)
  }
})

const transactionSearch = ref('')
const statusFilter = ref('All')
const typeFilter = ref('All')

// ── Dashboard Analytics Charts ────────────────────────────────────────────────
const dashChartTextColor = computed(() => $q.dark.isActive ? 'rgba(255,255,255,0.65)' : '#546e7a')
const dashChartGridColor  = computed(() => $q.dark.isActive ? 'rgba(255,255,255,0.07)' : 'rgba(0,0,0,0.07)')

// Line chart: BCH received over time (last 15 transactions)
const dashLineChartData = computed(() => {
  const sorted = [...allTransactions.value]
    .filter(t => t.status === 'completed')
    .sort((a, b) => new Date(a.date) - new Date(b.date))
    .slice(-15)
  return {
    labels: sorted.map(t => {
      const d = new Date(t.date)
      return isNaN(d) ? t.date : d.toLocaleDateString('en-US', { month: 'short', day: 'numeric' })
    }),
    datasets: [{
      label: 'BCH Received',
      data: sorted.map(t => parseFloat(t.amount || 0)),
      borderColor: '#1976d2',
      backgroundColor: $q.dark.isActive ? 'rgba(25,118,210,0.18)' : 'rgba(25,118,210,0.1)',
      borderWidth: 2,
      pointBackgroundColor: '#1976d2',
      pointRadius: 4,
      fill: true,
      tension: 0.4
    }]
  }
})
const dashLineChartOptions = computed(() => ({
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: { display: false },
    tooltip: { callbacks: { label: ctx => ` ${ctx.parsed.y.toFixed(4)} BCH` } }
  },
  scales: {
    x: {
      grid: { color: dashChartGridColor.value },
      ticks: { color: dashChartTextColor.value, font: { size: 10 } }
    },
    y: {
      grid: { color: dashChartGridColor.value },
      ticks: { color: dashChartTextColor.value, font: { size: 10 }, callback: v => v + ' BCH' },
      beginAtZero: true
    }
  }
}))

// Bar chart: total BCH by wallet type
const DASH_COLORS = ['#1976d2','#7b1fa2','#2e7d32','#e65100','#c62828','#00838f','#37474f']
const dashTypeMap = computed(() => {
  const map = {}
  allTransactions.value.forEach(t => {
    const tp = t.type || 'Other'
    map[tp] = (map[tp] || 0) + parseFloat(t.amount || 0)
  })
  return map
})
const dashBarChartData = computed(() => {
  const types = Object.keys(dashTypeMap.value)
  return {
    labels: types,
    datasets: [{
      label: 'Total BCH',
      data: types.map(tp => parseFloat(dashTypeMap.value[tp].toFixed(4))),
      backgroundColor: types.map((_, i) => DASH_COLORS[i % DASH_COLORS.length] + 'cc'),
      borderColor:      types.map((_, i) => DASH_COLORS[i % DASH_COLORS.length]),
      borderWidth: 1.5,
      borderRadius: 6
    }]
  }
})
const dashBarChartOptions = computed(() => ({
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: { display: false },
    tooltip: { callbacks: { label: ctx => ` ${ctx.parsed.y.toFixed(4)} BCH` } }
  },
  scales: {
    x: { grid: { display: false }, ticks: { color: dashChartTextColor.value, font: { size: 10 } } },
    y: {
      grid: { color: dashChartGridColor.value },
      ticks: { color: dashChartTextColor.value, font: { size: 10 }, callback: v => v + ' BCH' },
      beginAtZero: true
    }
  }
}))
// ─────────────────────────────────────────────────────────────────────────────

// Columns for executed withdrawals history table
const executedColumns = [
  { name: 'executed_at', label: 'Date Executed', field: 'executed_at', align: 'left', sortable: true },
  { name: 'donor_name', label: 'Donor', field: 'donor_name', align: 'left' },
  { name: 'amount', label: 'Amount', field: 'payout_amount_satoshis', align: 'right', sortable: true },
  { name: 'cycle', label: 'Cycle', field: 'cycle_number', align: 'center' },
  { name: 'interval', label: 'Interval', field: 'interval_label', align: 'center' },
  { name: 'txid', label: 'Transaction ID', field: 'txid', align: 'left' },
  { name: 'payout_status', label: 'Status', field: 'status', align: 'center' },
]

// Pending schedule grouped by contract (donation_id), with projected future cycles
const pendingScheduleGroups = computed(() => {
  if (!selectedAccount.value) return []
  const { pending } = getAccountSchedule(selectedAccount.value)
  const groups = {}
  pending.forEach((p) => {
    const key = p.donation_id
    if (!groups[key]) {
      groups[key] = {
        donationId: key,
        donorName: p.donor_name || 'Anonymous',
        donorEmail: p.donor_email || '',
        intervalLabel: p.interval_label || '—',
        amountBch: (p.payout_amount_satoshis / 1e8).toFixed(8),
        totalCycles: p.total_cycles,
        cyclesRemaining: p.total_cycles - p.cycle_number + 1,
        hasDue: new Date(p.due_at) <= new Date(),
        payoutId: p.id,
        payoutMode: p.payout_mode,
        cycles: [],
      }
    }
    const pg = groups[key]
    const intervalMs = p.interval_blocks * 10 * 60 * 1000
    const baseDue = new Date(p.due_at)
    const now = new Date()
    for (let c = p.cycle_number; c <= p.total_cycles; c++) {
      const dueAt = new Date(baseDue.getTime() + (c - p.cycle_number) * intervalMs)
      let status = 'scheduled'
      if (c === p.cycle_number) status = dueAt <= now ? 'due' : 'next'
      else if (c === p.cycle_number + 1) status = 'upcoming'
      pg.cycles.push({
        cycleNumber: c,
        dueAt,
        amountBch: (p.payout_amount_satoshis / 1e8).toFixed(8),
        status,
        payoutId: c === p.cycle_number ? p.id : null,
      })
    }
  })
  return Object.values(groups)
})

const transactionColumns = [
  { name: 'date', label: 'Date', field: 'date', align: 'left', sortable: true },
  { name: 'donorName', label: 'Donor Name', field: 'donorName', align: 'left' },
  { name: 'description', label: 'Message', field: 'description', align: 'left' },
  { name: 'type', label: 'Type', field: 'type', align: 'center' },
  { name: 'amount', label: 'Amount', field: 'amount', align: 'right', sortable: true },
  { name: 'status', label: 'Status', field: 'status', align: 'center' },
  { name: 'actions', label: 'Actions', field: 'actions', align: 'center', style: 'min-width: 120px' },
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

const executeWithdrawConfirm = async () => {
  if (!withdrawConfirmDialog.value.onConfirm) return
  withdrawConfirmDialog.value.loading = true
  try {
    await withdrawConfirmDialog.value.onConfirm()
    withdrawConfirmDialog.value.open = false
  } catch (err) {
    $q.notify({
      type: 'negative',
      message: 'Operation failed',
      caption: err?.response?.data?.error || 'Please try again.',
      position: 'top',
    })
  } finally {
    withdrawConfirmDialog.value.loading = false
  }
}

const handleSmartWithdraw = (row) => {
  if (!row.duePayoutId || row.withdrawn) return

  const amountBch = formatCurrency(row.amount)
  withdrawConfirmDialog.value = {
    open: true,
    mode: 'smart',
    accountName: row.donorName,
    totalBch: amountBch,
    payouts: [
      {
        id: row.duePayoutId,
        donorName: row.donorName,
        donorEmail: row.donorEmail || '',
        amountBch,
        cycleNumber: row.cycleNumber || 1,
        totalCycles: row.totalCycles || '—',
        dueAt: new Date().toISOString(),
      },
    ],
    loading: false,
    onConfirm: async () => {
      await api.post(`payouts/${row.duePayoutId}/execute/`, { txid: row.txid || `manual-${row.id}` })
      withdrawnDonations.value.add(row.id)
      localStorage.setItem('withdrawnDonations', JSON.stringify([...withdrawnDonations.value]))
      row.withdrawn = true
      row.status = 'completed'
      row.duePayoutId = null
      if (row.nonprofit) fetchPayoutsForNonprofit(row.nonprofit)
      $q.notify({
        type: 'positive',
        message: 'Withdrawal confirmed!',
        caption: `${amountBch} BCH executed.`,
        position: 'top',
        timeout: 3000,
      })
    },
  }
}

const handleSmartWithdrawAll = (account) => {
  const info = getAccountPayoutInfo(account)
  if (!info || info.dueSmart.length === 0) return

  const duePayouts = info.dueSmart
  const totalBch = duePayouts.reduce((sum, p) => sum + p.payout_amount_satoshis / 1e8, 0).toFixed(8)

  withdrawConfirmDialog.value = {
    open: true,
    mode: 'smart',
    accountName: account.name,
    totalBch,
    payouts: duePayouts.map((p) => ({
      id: p.id,
      donorName: p.donor_name || 'Anonymous',
      donorEmail: p.donor_email || '',
      amountBch: (p.payout_amount_satoshis / 1e8).toFixed(8),
      cycleNumber: p.cycle_number,
      totalCycles: p.total_cycles,
      dueAt: p.due_at,
    })),
    loading: false,
    onConfirm: async () => {
      let successCount = 0
      let failCount = 0
      for (const payout of duePayouts) {
        try {
          await api.post(`payouts/${payout.id}/execute/`, {
            txid: `smart-${payout.id}-c${payout.cycle_number}`,
          })
          const row = allTransactions.value.find((t) => t.id === payout.donation_id)
          if (row) {
            row.withdrawn = true
            row.status = 'completed'
            row.duePayoutId = null
            withdrawnDonations.value.add(row.id)
          }
          successCount++
        } catch {
          failCount++
        }
      }
      localStorage.setItem('withdrawnDonations', JSON.stringify([...withdrawnDonations.value]))
      if (account.nonprofitId) fetchPayoutsForNonprofit(account.nonprofitId)
      if (successCount > 0) {
        $q.notify({
          type: 'positive',
          message: `${successCount} withdrawal(s) confirmed`,
          caption: `${totalBch} BCH executed for ${account.name}`,
          position: 'top',
          timeout: 3000,
        })
      }
      if (failCount > 0) {
        $q.notify({ type: 'warning', message: `${failCount} payout(s) failed`, position: 'top' })
      }
    },
  }
}

const handleContractWithdraw = async (account) => {
  const info = getAccountPayoutInfo(account)
  if (!info || info.dueApproval.length === 0) return

  const duePayouts = info.dueApproval
  const totalBch = duePayouts.reduce((sum, p) => sum + p.payout_amount_satoshis / 1e8, 0).toFixed(8)

  withdrawConfirmDialog.value = {
    open: true,
    mode: 'inbox_approval',
    accountName: account.name,
    totalBch,
    payouts: duePayouts.map((p) => ({
      id: p.id,
      donorName: p.donor_name || 'Anonymous',
      donorEmail: p.donor_email || '',
      amountBch: (p.payout_amount_satoshis / 1e8).toFixed(8),
      cycleNumber: p.cycle_number,
      totalCycles: p.total_cycles,
      dueAt: p.due_at,
    })),
    loading: false,
    onConfirm: async () => {
      let successCount = 0
      let failCount = 0
      for (const payout of duePayouts) {
        try {
          await api.post(`payouts/${payout.id}/trigger/`)
          successCount++
        } catch {
          failCount++
        }
      }
      if (account.nonprofitId) fetchPayoutsForNonprofit(account.nonprofitId)
      if (successCount > 0) {
        $q.notify({
          type: 'positive',
          message: `Approval email${successCount > 1 ? 's' : ''} sent to ${successCount} donor${successCount > 1 ? 's' : ''}`,
          caption: 'Withdrawals will execute once donors approve via email.',
          position: 'top',
          timeout: 4000,
        })
      }
      if (failCount > 0) {
        $q.notify({
          type: 'warning',
          message: `${failCount} email${failCount > 1 ? 's' : ''} failed to send`,
          caption: 'Check email configuration.',
          position: 'top',
          timeout: 4000,
        })
      }
    },
  }
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
    year: 'numeric', month: 'long', day: 'numeric', hour: '2-digit', minute: '2-digit',
  })
  const statusColor =
    transaction.status === 'completed' ? 'positive' :
    transaction.status === 'pending' ? 'warning' : 'negative'

  const rows = [
    { label: 'Donation Date', value: transactionDate },
    { label: 'Donor Name', value: transaction.donorName || 'Anonymous' },
    { label: 'Donor Email', value: transaction.donorEmail || 'N/A' },
    { label: 'Donor Contact', value: transaction.donorContact || 'N/A' },
    ...(transaction.contract && transaction.contract !== 'N/A'
      ? [{ label: 'Contract', value: transaction.contract, style: 'color: #1976d2; font-weight: 600;' }] : []),
    ...(transaction.interval && transaction.interval !== 'N/A'
      ? [{ label: 'Interval', value: transaction.interval, style: 'color: #1976d2; font-weight: 600;' }] : []),
    { label: 'Message', value: transaction.description || 'No message' },
    { label: 'Wallet Type', value: transaction.type?.toUpperCase(), style: 'color: #4caf50; font-weight: 600;' },
  ]

  txDetailDialog.value = {
    open: true,
    data: transaction,
    statusColor,
    formattedAmount: formatCurrency(parseFloat(transaction.amount)),
    rows,
  }
}
</script>

<style scoped lang="scss">
.dashboard-page {
  overflow-x: hidden;
  min-height: 100vh;
  background:
    radial-gradient(ellipse at 15% 30%, rgba(100, 160, 255, 0.25) 0%, transparent 55%),
    radial-gradient(ellipse at 85% 70%, rgba(160, 110, 255, 0.2) 0%, transparent 55%),
    #eef2f7;
  background-attachment: fixed;
}

.body--dark .dashboard-page {
  background:
    radial-gradient(ellipse at 15% 30%, rgba(60, 90, 180, 0.35) 0%, transparent 55%),
    radial-gradient(ellipse at 85% 70%, rgba(100, 60, 180, 0.3) 0%, transparent 55%),
    #0f1117;
}

.sidebar-container {
  background: rgba(255, 255, 255, 0.55);
  backdrop-filter: blur(16px);
  -webkit-backdrop-filter: blur(16px);
  border-right: 1px solid rgba(255, 255, 255, 0.4);
  min-height: 100vh;
  padding: 0;
}

.body--dark .sidebar-container {
  background: rgba(20, 24, 40, 0.6);
  border-right: 1px solid rgba(255, 255, 255, 0.08);
}

.main-content {
  background: rgba(255, 255, 255, 0.6);
  backdrop-filter: blur(18px);
  -webkit-backdrop-filter: blur(18px);
  border-left: 1px solid rgba(255, 255, 255, 0.5);
}

.body--dark .main-content {
  background: rgba(18, 22, 38, 0.65);
  border-left: 1px solid rgba(255, 255, 255, 0.06);
}

.accounts-sidebar {
  border-radius: 0;
  padding: 0;
}

.sidebar-header {
  padding: 24px 20px 20px;
}

.sidebar-toggle {
  display: flex;
  background: rgba(0, 0, 0, 0.06);
  border-radius: 10px;
  padding: 3px;
  gap: 3px;
}

.sidebar-toggle__btn {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 7px 10px;
  border-radius: 8px;
  font-size: 13px;
  font-weight: 600;
  color: #546e7a;
  cursor: pointer;
  transition: all 0.2s ease;
  user-select: none;

  &:hover {
    color: #1565c0;
    background: rgba(21, 101, 192, 0.08);
  }

  &.sidebar-toggle__btn--active {
    background: #ffffff;
    color: #1565c0;
    box-shadow: 0 1px 6px rgba(0, 0, 0, 0.1);
  }
}

.body--dark .sidebar-toggle {
  background: rgba(255, 255, 255, 0.07);
}

.body--dark .sidebar-toggle__btn {
  color: rgba(255, 255, 255, 0.45);

  &:hover {
    color: #90caf9;
    background: rgba(144, 202, 249, 0.1);
  }

  &.sidebar-toggle__btn--active {
    background: rgba(144, 202, 249, 0.15);
    color: #90caf9;
    box-shadow: 0 1px 6px rgba(0, 0, 0, 0.3);
  }
}

.sidebar-search {
  :deep(.q-field__control) {
    background: rgba(255, 255, 255, 0.85);
    border-radius: 8px;
  }
}

.body--dark .sidebar-search {
  :deep(.q-field__control) {
    background: rgba(255, 255, 255, 0.07);
  }

  :deep(.q-field__native),
  :deep(.q-field__input) {
    color: #e0e0e0 !important;
  }

  :deep(.q-placeholder) {
    color: rgba(255, 255, 255, 0.35) !important;
  }
}

.sidebar-title {
  font-size: 18px;
  font-weight: 800;
  color: #1a237e;
  line-height: 1.2;
  letter-spacing: -0.3px;
}

.body--dark .sidebar-title {
  color: #e8eaf6;
}

.sidebar-subtitle {
  font-size: 12px;
  color: #78909c;
  margin-top: 2px;
  font-weight: 500;
}

.body--dark .sidebar-subtitle {
  color: #90a4ae;
}

.sidebar-account-card {
  background: rgba(255, 255, 255, 0.75);
  backdrop-filter: blur(8px);
  -webkit-backdrop-filter: blur(8px);
  border-radius: 14px;
  padding: 14px;
  margin-bottom: 10px;
  cursor: pointer;
  border: 1.5px solid rgba(255, 255, 255, 0.6);
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.06);
  transition: all 0.2s ease;

  &:hover {
    border-color: #90caf9;
    box-shadow: 0 4px 20px rgba(21, 101, 192, 0.14);
    transform: translateY(-1px);
  }

  &.sidebar-account-card--active {
    border-color: #1565c0;
    box-shadow: 0 4px 20px rgba(21, 101, 192, 0.2);
  }
}

.body--dark .sidebar-account-card {
  background: rgba(30, 36, 60, 0.7);
  border-color: rgba(255, 255, 255, 0.08);

  &:hover {
    border-color: #5c8ee0;
    box-shadow: 0 4px 20px rgba(92, 142, 224, 0.2);
  }

  &.sidebar-account-card--active {
    border-color: #5c8ee0;
    box-shadow: 0 4px 20px rgba(92, 142, 224, 0.25);
  }
}

.sidebar-avatar {
  width: 38px;
  height: 38px;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #e8f0fe;
  flex-shrink: 0;
}

.sidebar-account-name {
  font-size: 13.5px;
  font-weight: 700;
  color: #1a237e;
  line-height: 1.2;
}

.body--dark .sidebar-account-name {
  color: #c5cae9;
}

.sidebar-account-sub {
  font-size: 11px;
  color: #90a4ae;
  margin-top: 1px;
  font-weight: 500;
}

.sidebar-stat-label {
  font-size: 10px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  color: #90a4ae;
  margin-bottom: 2px;
}

.sidebar-stat-value {
  font-size: 14px;
  font-weight: 800;
  color: #263238;
  line-height: 1;
}

.body--dark .sidebar-stat-value {
  color: #eceff1;
}

.details-panel {
  background-color: transparent;
  border-radius: 8px;
  padding: 1rem;
}

/* ── Dashboard Analytics Chart Cards ─────────────────────────────── */
.dash-chart-section-title {
  font-size: 14px;
  font-weight: 700;
  color: #37474f;
}
.body--dark .dash-chart-section-title {
  color: rgba(255, 255, 255, 0.75);
}
.dash-chart-card-title {
  font-size: 13px;
  font-weight: 700;
  color: #37474f;
}
.body--dark .dash-chart-card-title {
  color: rgba(255, 255, 255, 0.85);
}
.dash-chart-card-sub {
  font-size: 11px;
  color: #90a4ae;
  margin-top: 2px;
}
.body--dark .dash-chart-card-sub {
  color: rgba(255, 255, 255, 0.35);
}
.dash-chart-canvas {
  position: relative;
  height: 200px;
}
.dash-chart-canvas--pie {
  height: 240px;
}
.dash-chart-canvas--scatter3d {
  height: 420px;
  width: 100%;
}
/* ──────────────────────────────────────────────────────────────────── */

.detail-info-card {
  border: 1.5px solid #90caf9 !important;
  background: rgba(255, 255, 255, 0.72);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  transition: border-color 0.2s ease, box-shadow 0.2s ease;

  &:hover {
    border-color: #1565c0 !important;
    box-shadow: 0 4px 20px rgba(21, 101, 192, 0.12);
  }
}

.body--dark .detail-info-card {
  border-color: rgba(100, 160, 255, 0.3) !important;
  background: rgba(25, 32, 56, 0.65) !important;

  &:hover {
    border-color: #5c8ee0 !important;
    box-shadow: 0 4px 20px rgba(92, 142, 224, 0.18);
  }
}

:deep(.q-tab-panels) {
  background: transparent !important;
}

:deep(.q-tab-panel) {
  background: transparent !important;
}

.body--dark :deep(.q-tab-panels),
.body--dark :deep(.q-tab-panel) {
  background: transparent !important;
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
  border-radius: 12px;
  border: 1.5px solid rgba(144, 202, 249, 0.5);
  background: rgba(255, 255, 255, 0.72);
  backdrop-filter: blur(8px);
  -webkit-backdrop-filter: blur(8px);
  transition: all 0.2s ease;

  &:hover {
    transform: translateY(-2px);
    border-color: #1565c0;
    box-shadow: 0 4px 16px rgba(21, 101, 192, 0.14);
  }
}

.body--dark .stats-card {
  background: rgba(25, 32, 56, 0.65) !important;
  border-color: rgba(100, 160, 255, 0.25) !important;
  color: #e0e0e0;

  .text-caption {
    color: rgba(255, 255, 255, 0.5) !important;
  }

  &:hover {
    border-color: #5c8ee0 !important;
    box-shadow: 0 4px 16px rgba(92, 142, 224, 0.2);
  }
}

.status-table-card {
  border-radius: 14px;
  border: 1.5px solid rgba(144, 202, 249, 0.5);
  background: rgba(255, 255, 255, 0.72);
  backdrop-filter: blur(8px);
  -webkit-backdrop-filter: blur(8px);
}

.body--dark .status-table-card {
  background: rgba(25, 32, 56, 0.65) !important;
  border-color: rgba(100, 160, 255, 0.25) !important;
}

.transactions-table {
  background: transparent !important;

  :deep(.q-table__container),
  :deep(.q-table__middle),
  :deep(.q-table) {
    background: transparent !important;
  }

  :deep(.q-table__top) {
    padding: 12px 0;
    background: transparent !important;
  }

  :deep(thead tr th) {
    font-weight: 600;
    font-size: 13px;
    background: rgba(144, 202, 249, 0.08);
  }

  :deep(tbody tr) {
    cursor: pointer;

    &:hover td {
      background: rgba(21, 101, 192, 0.05) !important;
    }
  }

  :deep(.q-table__bottom) {
    background: transparent !important;
  }
}

.body--dark .transactions-table {
  :deep(.q-table) {
    color: #e0e0e0;
  }

  :deep(thead tr th) {
    color: rgba(255, 255, 255, 0.5);
    background: rgba(144, 202, 249, 0.05) !important;
    border-color: rgba(255, 255, 255, 0.08) !important;
  }

  :deep(tbody tr td) {
    border-color: rgba(255, 255, 255, 0.05) !important;
    color: #e0e0e0;
  }

  :deep(tbody tr:hover td) {
    background: rgba(144, 202, 249, 0.07) !important;
  }

  :deep(.q-table__bottom) {
    color: rgba(255, 255, 255, 0.4);
    border-color: rgba(255, 255, 255, 0.07) !important;
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

.body--dark .dashboard-tabs {
  :deep(.q-tab) {
    color: rgba(255, 255, 255, 0.55) !important;
  }

  :deep(.q-tab--active) {
    color: #90caf9 !important;
  }

  :deep(.q-tabs__indicator) {
    background: #90caf9 !important;
  }
}

// ── Transaction Detail Dialog ────────────────────────────────────────────────
.tx-detail-dialog {
  min-width: 480px;
  max-width: 560px;
  border-radius: 16px !important;
  overflow: hidden;
  border: 1.5px solid rgba(144, 202, 249, 0.5);
  background: rgba(255, 255, 255, 0.92);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
}

.body--dark .tx-detail-dialog {
  background: rgba(18, 24, 46, 0.92) !important;
  border-color: rgba(100, 160, 255, 0.25) !important;
}

.tx-detail-header {
  padding: 20px 20px 16px;
  border-bottom: 1px solid rgba(144, 202, 249, 0.3);
  background: rgba(21, 101, 192, 0.06);
}

.body--dark .tx-detail-header {
  background: rgba(144, 202, 249, 0.05);
  border-color: rgba(255, 255, 255, 0.07);
}

.tx-detail-title {
  font-size: 18px;
  font-weight: 800;
  color: #1a237e;
  line-height: 1.2;
}

.body--dark .tx-detail-title {
  color: #e8eaf6;
}

.tx-detail-sub {
  font-size: 12px;
  color: #78909c;
  margin-top: 2px;
}

.body--dark .tx-detail-sub {
  color: rgba(255, 255, 255, 0.4);
}

.tx-close-btn {
  color: #90a4ae !important;
}

.body--dark .tx-close-btn {
  color: rgba(255, 255, 255, 0.4) !important;
}

.tx-detail-table {
  border: 1.5px solid rgba(144, 202, 249, 0.4);
  border-radius: 10px;
  overflow: hidden;
}

.body--dark .tx-detail-table {
  border-color: rgba(100, 160, 255, 0.15);
}

.tx-detail-row {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  padding: 12px 14px;
  border-bottom: 1px solid rgba(0, 0, 0, 0.05);
  gap: 16px;

  &:last-child {
    border-bottom: none;
  }

  &:nth-child(odd) {
    background: rgba(0, 0, 0, 0.012);
  }

  &.tx-detail-row--amount {
    background: rgba(76, 175, 80, 0.06);
    border-top: 1px solid rgba(76, 175, 80, 0.15);
  }
}

.body--dark .tx-detail-row {
  border-bottom-color: rgba(255, 255, 255, 0.05);

  &:nth-child(odd) {
    background: rgba(255, 255, 255, 0.025);
  }

  &.tx-detail-row--amount {
    background: rgba(76, 175, 80, 0.08);
    border-top-color: rgba(76, 175, 80, 0.2);
  }
}

.tx-detail-label {
  font-size: 12.5px;
  color: #78909c;
  font-weight: 600;
  flex-shrink: 0;
  min-width: 120px;
}

.body--dark .tx-detail-label {
  color: rgba(255, 255, 255, 0.45);
}

.tx-detail-value {
  font-size: 13.5px;
  color: #212121;
  font-weight: 500;
  text-align: right;
}

.body--dark .tx-detail-value {
  color: #e0e0e0;
}

.tx-detail-note {
  display: flex;
  align-items: flex-start;
  gap: 6px;
  padding: 10px 14px;
  background: rgba(21, 101, 192, 0.06);
  border-left: 3px solid #1976d2;
  border-radius: 6px;
  font-size: 12px;
  color: #546e7a;
  line-height: 1.6;
}

.body--dark .tx-detail-note {
  background: rgba(144, 202, 249, 0.07);
  color: rgba(255, 255, 255, 0.5);
}
</style>

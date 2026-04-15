<template>
  <q-page class="dashboard-page">
    <div class="row" style="min-height: 100vh">
      <div class="col-12 col-md-4 col-lg-3 sidebar-container">
        <div class="accounts-sidebar">
          <!-- ── Sidebar Header ─────────────────────────────────── -->
          <div class="sidebar-header">
            <div class="row items-center justify-between no-wrap">
              <div style="min-width: 0; flex: 1">
                <div class="sidebar-title">
                  <template v-if="nonprofitProfile">
                    {{ nonprofitProfile.name }}
                    <q-icon
                      v-if="nonprofitProfile.verified"
                      name="verified"
                      color="green-4"
                      size="16px"
                      class="q-ml-xs"
                      style="vertical-align: middle"
                    />
                  </template>
                  <template v-else>Charity Dashboard</template>
                </div>
                <div class="sidebar-subtitle">
                  {{ accounts.length }} active account{{ accounts.length !== 1 ? 's' : '' }}
                </div>
              </div>
              <div class="sidebar-header-icon">
                <div
                  v-if="nonprofitProfile?.logo_url"
                  style="
                    width: 36px;
                    height: 36px;
                    border-radius: 50%;
                    overflow: hidden;
                    border: 2px solid rgba(255, 255, 255, 0.3);
                  "
                >
                  <img
                    :src="nonprofitProfile.logo_url"
                    style="width: 100%; height: 100%; object-fit: cover"
                  />
                </div>
                <q-icon v-else name="dashboard" color="white" size="20px" />
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
              style="border-radius: 8px"
            >
              <template v-slot:prepend>
                <q-icon name="search" color="grey-5" size="18px" />
              </template>
            </q-input>
          </div>

          <!-- ── Account Cards ──────────────────────────────────── -->
          <div class="q-px-sm q-pb-md q-pt-sm">
            <!-- Skeleton cards while loading -->
            <template v-if="loadingDonations">
              <div v-for="n in 4" :key="'sk-' + n" class="sidebar-skeleton-card">
                <div class="row items-center no-wrap q-mb-sm" style="gap: 10px">
                  <q-skeleton
                    type="QAvatar"
                    size="38px"
                    style="border-radius: 10px; flex-shrink: 0"
                  />
                  <div style="flex: 1; min-width: 0">
                    <q-skeleton type="text" width="70%" style="margin-bottom: 5px" />
                    <q-skeleton type="text" width="50%" />
                  </div>
                </div>
                <q-skeleton
                  type="QInput"
                  style="border-radius: 20px; height: 22px; margin-bottom: 10px"
                />
                <div class="row" style="gap: 8px">
                  <q-skeleton style="flex: 1; height: 44px; border-radius: 8px" />
                  <q-skeleton style="flex: 1; height: 44px; border-radius: 8px" />
                </div>
              </div>
            </template>

            <div
              v-for="account in filteredAccounts"
              :key="account.id"
              class="sidebar-account-card"
              :class="{ 'sidebar-account-card--active': selectedAccount?.id === account.id }"
              @click="selectAccount(account)"
            >
              <!-- Active accent bar -->
              <div class="sidebar-card-accent" />

              <!-- Top row: avatar + name + due badge -->
              <div class="row items-start no-wrap q-mb-xs">
                <div class="sidebar-avatar">
                  <img
                    src="~assets/paytaca.png"
                    alt="wallet"
                    style="width: 24px; height: 24px; object-fit: contain"
                  />
                </div>
                <div style="flex: 1; min-width: 0; margin-left: 10px">
                  <div class="sidebar-account-name ellipsis">{{ account.name }}</div>
                  <div class="sidebar-account-sub ellipsis">
                    {{ account.email || account.contact || 'Anonymous Donor' }}
                  </div>
                </div>
                <q-badge
                  v-if="
                    getAccountPayoutInfo(account)?.dueApproval?.length > 0 ||
                    getAccountPayoutInfo(account)?.dueSmart?.length > 0
                  "
                  color="orange"
                  rounded
                  style="
                    font-size: 10px;
                    font-weight: 700;
                    padding: 3px 7px;
                    flex-shrink: 0;
                    margin-top: 2px;
                  "
                  label="Due"
                />
              </div>

              <!-- Address copy pill -->
              <div class="q-mt-xs" v-if="account.address">
                <div
                  class="sidebar-address-pill ellipsis"
                  @click.stop="
                    $q.copyToClipboard(account.address).then(() =>
                      $q.notify({
                        type: 'positive',
                        message: 'Address copied',
                        position: 'top',
                        timeout: 1500,
                      }),
                    )
                  "
                >
                  <q-icon
                    name="account_balance_wallet"
                    size="10px"
                    class="q-mr-xs"
                    style="flex-shrink: 0"
                  />
                  <span class="sidebar-address-pill-label">BCH:</span>
                  <span class="q-ml-xs">{{ account.address }}</span>
                  <q-icon
                    name="content_copy"
                    size="10px"
                    class="q-ml-xs sidebar-address-copy-icon"
                    style="flex-shrink: 0"
                  />
                </div>
              </div>

              <!-- Divider -->
              <div class="sidebar-card-divider" />

              <!-- BCH stat blocks -->
              <div class="row q-mt-xs q-mb-sm" style="gap: 8px">
                <div class="sidebar-stat-block sidebar-stat-block--neutral">
                  <div class="row items-center no-wrap" style="gap: 4px; margin-bottom: 2px">
                    <q-icon name="currency_bitcoin" size="11px" color="blue-grey-5" />
                    <div class="sidebar-stat-label">Total Received</div>
                  </div>
                  <div class="sidebar-stat-value">
                    {{ formatCurrency(account.totalReceived ?? account.current) }}
                  </div>
                </div>
                <div class="sidebar-stat-block sidebar-stat-block--positive">
                  <div class="row items-center no-wrap" style="gap: 4px; margin-bottom: 2px">
                    <q-icon name="receipt_long" size="11px" color="green-7" />
                    <div class="sidebar-stat-label">Transactions</div>
                  </div>
                  <div class="sidebar-stat-value sidebar-stat-value--positive">
                    {{ account.transactionCount ?? 0 }}
                  </div>
                </div>
              </div>

              <!-- Payout action row -->
              <q-separator class="sidebar-card-sep" style="margin-bottom: 10px" />
              <div v-if="getAccountPayoutInfo(account)">
                <q-btn
                  v-if="getAccountPayoutInfo(account).dueApproval.length > 0"
                  unelevated
                  color="positive"
                  icon="mark_email_read"
                  label="Request Withdrawal"
                  size="sm"
                  class="full-width"
                  no-caps
                  style="font-weight: 700; border-radius: 8px"
                  @click.stop="handleContractWithdraw(account)"
                />
                <q-btn
                  v-else-if="getAccountPayoutInfo(account).dueSmart.length > 0"
                  unelevated
                  color="positive"
                  icon="account_balance_wallet"
                  label="Withdraw Now"
                  size="sm"
                  class="full-width"
                  no-caps
                  style="font-weight: 700; border-radius: 8px"
                  @click.stop="handleSmartWithdrawAll(account)"
                />
                <div
                  v-else-if="getAccountPayoutInfo(account).upcoming"
                  class="row items-center no-wrap"
                  style="gap: 6px"
                >
                  <q-icon name="schedule" color="blue-6" size="14px" style="flex-shrink: 0" />
                  <span class="sidebar-next-text">
                    Next:
                    {{
                      new Date(getAccountPayoutInfo(account).upcoming.due_at).toLocaleDateString(
                        'en-US',
                        { month: 'short', day: 'numeric', year: 'numeric' },
                      )
                    }}
                  </span>
                </div>
                <div v-else class="row items-center no-wrap" style="gap: 6px">
                  <q-icon name="check_circle_outline" color="grey-4" size="14px" />
                  <span class="sidebar-no-pending-text">No pending withdrawals</span>
                </div>
              </div>
            </div>

            <div class="text-center q-mt-sm">
              <a
                href="#"
                class="view-all-link text-weight-medium"
                style="text-decoration: none; font-size: 13px"
                >View all</a
              >
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
            mobile-arrows
          >
            <q-tab name="transactions" label="Withdrawal History" />
            <q-tab name="details" label="Details" />
            <q-tab name="pending" label="Pending Withdrawals" />
            <q-tab
              v-if="nonprofitProfile"
              name="profile"
              label="Organization Profile"
              icon="business"
            />
          </q-tabs>

          <q-separator class="q-mb-lg" />

          <q-tab-panels v-model="detailTab" animated>
            <q-tab-panel name="transactions">
              <!-- Header -->
              <div class="row items-center justify-between q-mb-md">
                <div>
                  <div class="text-h6 text-weight-bold">Withdrawal History</div>
                  <div class="text-caption text-grey-6">
                    All completed cycle payouts for this account
                  </div>
                </div>
                <q-chip
                  color="green-2"
                  text-color="green-9"
                  icon="check_circle"
                  :label="`${getAccountSchedule(selectedAccount).executed.length} completed`"
                  style="font-weight: 700"
                />
              </div>

              <!-- Empty state -->
              <div
                v-if="getAccountSchedule(selectedAccount).executed.length === 0"
                class="text-center q-py-xl"
                style="border: 2px dashed #e0e0e0; border-radius: 12px"
              >
                <q-icon name="history" size="48px" color="grey-4" />
                <div class="text-grey-6 q-mt-sm text-weight-medium">No withdrawals yet</div>
                <div class="text-caption text-grey-4 q-mt-xs">
                  Completed cycle payouts will appear here
                </div>
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
                :grid="$q.screen.lt.md"
              >
                <template v-slot:body-cell-executed_at="props">
                  <q-td :props="props">
                    <div class="text-weight-medium" style="font-size: 13px">
                      {{
                        new Date(props.row.executed_at).toLocaleDateString('en-US', {
                          month: 'short',
                          day: 'numeric',
                          year: 'numeric',
                        })
                      }}
                    </div>
                    <div class="text-caption text-grey-6">
                      {{
                        new Date(props.row.executed_at).toLocaleTimeString('en-US', {
                          hour: '2-digit',
                          minute: '2-digit',
                        })
                      }}
                    </div>
                  </q-td>
                </template>
                <template v-slot:body-cell-amount="props">
                  <q-td :props="props">
                    <span class="text-weight-bold text-green-8" style="font-size: 14px">
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
                      style="font-size: 11px; font-weight: 700; border-radius: 6px; height: 22px"
                    />
                  </q-td>
                </template>
                <template v-slot:body-cell-interval="props">
                  <q-td :props="props" class="text-center">
                    <q-badge
                      color="blue-2"
                      text-color="blue-9"
                      :label="props.row.interval_label || '—'"
                    />
                  </q-td>
                </template>
                <template v-slot:body-cell-txid="props">
                  <q-td :props="props">
                    <span
                      v-if="resolvePayoutTxid(props.row)"
                      class="text-primary"
                      style="font-family: monospace; font-size: 12px; cursor: pointer"
                      @click="copyTxid(resolvePayoutTxid(props.row))"
                    >
                      {{ formatTxidPreview(resolvePayoutTxid(props.row), 18) }}
                      <q-icon name="content_copy" size="12px" class="q-ml-xs" />
                    </span>
                    <span
                      v-else-if="props.row.txid"
                      class="text-warning text-caption text-weight-medium"
                      >Invalid TXID</span
                    >
                    <span v-else class="text-grey-5 text-caption">—</span>
                  </q-td>
                </template>
                <template v-slot:body-cell-payout_status="props">
                  <q-td :props="props" class="text-center">
                    <q-badge color="positive" label="Completed" style="font-weight: 600" />
                  </q-td>
                </template>

                <!-- Mobile card layout -->
                <template v-slot:item="props">
                  <div class="dash-mobile-card">
                    <div class="dash-mobile-card__header">
                      <div class="dash-mobile-card__title">
                        {{ props.row.donor_name || 'Anonymous' }}
                      </div>
                      <q-badge color="positive" label="Completed" style="font-weight: 600" />
                    </div>
                    <div class="dash-mobile-card__body">
                      <div class="dash-mobile-card__row">
                        <span class="dash-mobile-card__label">Date</span>
                        <span class="dash-mobile-card__value">
                          {{
                            new Date(props.row.executed_at).toLocaleDateString('en-US', {
                              month: 'short',
                              day: 'numeric',
                              year: 'numeric',
                            })
                          }}
                          <span class="text-grey-6 q-ml-xs" style="font-size: 11px">
                            {{
                              new Date(props.row.executed_at).toLocaleTimeString('en-US', {
                                hour: '2-digit',
                                minute: '2-digit',
                              })
                            }}
                          </span>
                        </span>
                      </div>
                      <div class="dash-mobile-card__row">
                        <span class="dash-mobile-card__label">Amount</span>
                        <span class="dash-mobile-card__value text-green-8 text-weight-bold">
                          {{ (props.row.payout_amount_satoshis / 1e8).toFixed(8) }} BCH
                        </span>
                      </div>
                      <div class="dash-mobile-card__row">
                        <span class="dash-mobile-card__label">Cycle</span>
                        <q-chip
                          dense
                          color="green-2"
                          text-color="green-9"
                          :label="`${props.row.cycle_number} / ${props.row.total_cycles}`"
                          style="
                            font-size: 11px;
                            font-weight: 700;
                            border-radius: 6px;
                            height: 22px;
                          "
                        />
                      </div>
                      <div class="dash-mobile-card__row">
                        <span class="dash-mobile-card__label">Interval</span>
                        <q-badge
                          color="blue-2"
                          text-color="blue-9"
                          :label="props.row.interval_label || '—'"
                        />
                      </div>
                      <div v-if="resolvePayoutTxid(props.row)" class="dash-mobile-card__row">
                        <span class="dash-mobile-card__label">TxID</span>
                        <span
                          class="text-primary dash-mobile-card__txid"
                          @click="copyTxid(resolvePayoutTxid(props.row))"
                        >
                          {{ formatTxidPreview(resolvePayoutTxid(props.row), 16) }}
                          <q-icon name="content_copy" size="11px" class="q-ml-xs" />
                        </span>
                      </div>
                    </div>
                  </div>
                </template>
              </q-table>
            </q-tab-panel>

            <q-tab-panel name="details" class="details-panel q-pa-none">
              <!-- ── Skeleton detail panel while loading ───────────────── -->
              <template v-if="loadingDonations">
                <!-- Profile header skeleton -->
                <div class="detail-skeleton-card q-mb-md">
                  <div class="row items-center no-wrap" style="gap: 18px; padding: 20px">
                    <q-skeleton
                      type="QAvatar"
                      size="72px"
                      style="border-radius: 50%; flex-shrink: 0"
                    />
                    <div style="flex: 1">
                      <q-skeleton type="text" width="40%" style="margin-bottom: 8px" />
                      <q-skeleton type="text" width="25%" style="margin-bottom: 6px" />
                      <q-skeleton type="QBadge" width="70px" />
                    </div>
                  </div>
                </div>
                <!-- Two info card skeletons -->
                <div class="row q-col-gutter-md q-mb-md">
                  <div class="col-12 col-md-6">
                    <div class="detail-skeleton-card" style="padding: 18px">
                      <q-skeleton type="text" width="40%" style="margin-bottom: 14px" />
                      <q-skeleton type="QInput" style="margin-bottom: 10px; height: 36px" />
                      <q-skeleton type="QInput" style="margin-bottom: 10px; height: 36px" />
                      <q-skeleton type="QInput" style="height: 36px" />
                    </div>
                  </div>
                  <div class="col-12 col-md-6">
                    <div class="detail-skeleton-card" style="padding: 18px">
                      <q-skeleton type="text" width="40%" style="margin-bottom: 14px" />
                      <q-skeleton type="QInput" style="margin-bottom: 10px; height: 36px" />
                      <q-skeleton type="QInput" style="margin-bottom: 10px; height: 36px" />
                      <q-skeleton type="QInput" style="height: 36px" />
                    </div>
                  </div>
                </div>
                <!-- Chart skeletons -->
                <div class="row q-col-gutter-md">
                  <div class="col-12 col-md-6">
                    <div class="detail-skeleton-card" style="padding: 18px">
                      <q-skeleton type="text" width="35%" style="margin-bottom: 12px" />
                      <q-skeleton style="height: 200px; border-radius: 10px" />
                    </div>
                  </div>
                  <div class="col-12 col-md-6">
                    <div class="detail-skeleton-card" style="padding: 18px">
                      <q-skeleton type="text" width="35%" style="margin-bottom: 12px" />
                      <q-skeleton style="height: 200px; border-radius: 10px" />
                    </div>
                  </div>
                </div>
              </template>

              <!-- ── Profile Header Card ──────────────────────────────── -->
              <template v-else>
                <q-card
                  flat
                  class="detail-info-card"
                  style="border-radius: 14px; margin-bottom: 16px; overflow: hidden"
                >
                  <q-card-section class="q-pa-none">
                    <div class="row no-wrap items-stretch profile-header-row">
                      <!-- Left: Avatar + name + role -->
                      <div
                        class="row items-center q-pa-lg profile-left-col"
                        style="
                          flex: 0 0 auto;
                          min-width: 260px;
                          border-right: 1px solid #f0f0f0;
                          gap: 18px;
                        "
                      >
                        <!-- Org avatar / logo -->
                        <div style="flex-shrink: 0">
                          <div
                            v-if="nonprofitDetail?.logo_url"
                            style="
                              width: 72px;
                              height: 72px;
                              border-radius: 50%;
                              overflow: hidden;
                              border: 3px solid #e8f0fe;
                            "
                          >
                            <img
                              :src="nonprofitDetail.logo_url"
                              style="width: 100%; height: 100%; object-fit: cover"
                            />
                          </div>
                          <div
                            v-else
                            style="
                              width: 72px;
                              height: 72px;
                              border-radius: 50%;
                              background: linear-gradient(135deg, #1565c0, #0d47a1);
                              display: flex;
                              align-items: center;
                              justify-content: center;
                              border: 3px solid #e8f0fe;
                              flex-shrink: 0;
                            "
                          >
                            <span style="font-size: 28px; font-weight: 800; color: white">
                              {{ selectedAccount.name?.charAt(0)?.toUpperCase() || 'N' }}
                            </span>
                          </div>
                        </div>
                        <!-- Name + category -->
                        <div style="min-width: 0">
                          <div
                            style="
                              font-size: 18px;
                              font-weight: 700;
                              color: #1a237e;
                              line-height: 1.2;
                            "
                            class="ellipsis org-name-text"
                          >
                            {{ selectedAccount.name }}
                          </div>
                          <div
                            class="q-mt-xs"
                            style="display: flex; align-items: center; gap: 6px; flex-wrap: wrap"
                          >
                            <span
                              class="org-category-text"
                              style="font-size: 13px; color: #1976d2; font-weight: 600"
                            >
                              {{ nonprofitDetail?.category || 'Nonprofit' }}
                            </span>
                            <span style="color: #bdbdbd">|</span>
                            <span class="org-status-text" style="font-size: 12px; color: #9e9e9e">
                              {{
                                nonprofitDetail?.active === false
                                  ? 'Inactive'
                                  : 'Active Organization'
                              }}
                            </span>
                          </div>
                          <q-chip
                            v-if="nonprofitDetail?.verified"
                            dense
                            color="green-2"
                            text-color="green-8"
                            icon="verified"
                            label="Verified"
                            style="font-size: 11px; font-weight: 700; margin-top: 8px"
                          />
                          <q-chip
                            v-else
                            dense
                            color="grey-2"
                            text-color="grey-7"
                            icon="schedule"
                            label="Unverified"
                            style="font-size: 11px; margin-top: 8px"
                          />
                        </div>
                      </div>

                      <!-- Right: Quick stats grid -->
                      <div
                        class="row items-center q-px-lg q-py-md profile-stats-col"
                        style="flex: 1; gap: 0; flex-wrap: wrap"
                      >
                        <div
                          v-for="stat in [
                            {
                              label: 'BCH Address',
                              value: selectedAccount.address || '—',
                              mono: true,
                              icon: 'account_balance_wallet',
                            },
                            {
                              label: 'Website',
                              value: nonprofitDetail?.website || '—',
                              link: nonprofitDetail?.website,
                              icon: 'language',
                            },
                            {
                              label: 'Email',
                              value: nonprofitDetail?.email || selectedAccount.email || '—',
                              icon: 'mail_outline',
                            },
                            { label: 'Phone', value: nonprofitDetail?.phone || '—', icon: 'phone' },
                          ]"
                          :key="stat.label"
                          style="min-width: 50%; padding: 10px 16px 10px 0"
                        >
                          <div
                            class="text-caption text-grey-5"
                            style="
                              font-size: 11px;
                              font-weight: 700;
                              text-transform: uppercase;
                              letter-spacing: 0.5px;
                              margin-bottom: 3px;
                            "
                          >
                            <q-icon :name="stat.icon" size="12px" class="q-mr-xs" />{{ stat.label }}
                          </div>
                          <a
                            v-if="stat.link"
                            :href="stat.link"
                            target="_blank"
                            style="
                              font-size: 13px;
                              font-weight: 600;
                              color: #1976d2;
                              word-break: break-all;
                              text-decoration: none;
                            "
                            >{{ stat.value }}</a
                          >
                          <div
                            v-else
                            class="stat-value-text"
                            :style="{
                              fontSize: '13px',
                              fontWeight: 600,
                              wordBreak: 'break-all',
                              fontFamily: stat.mono ? 'monospace' : 'inherit',
                            }"
                          >
                            {{ stat.value }}
                          </div>
                        </div>
                      </div>
                    </div>
                  </q-card-section>
                </q-card>

                <!-- ── Two column cards ─────────────────────────────────── -->
                <div class="row q-col-gutter-md">
                  <!-- Wallet & Financial Information -->
                  <div class="col-12 col-md-6">
                    <q-card flat class="detail-info-card" style="border-radius: 14px; height: 100%">
                      <q-card-section class="q-pb-xs">
                        <div class="row items-center justify-between">
                          <div
                            class="info-card-title"
                            style="font-size: 14px; font-weight: 700; color: #37474f"
                          >
                            Wallet Information
                          </div>
                          <q-icon name="account_balance_wallet" color="blue-4" size="20px" />
                        </div>
                      </q-card-section>
                      <q-separator />
                      <q-card-section class="q-pt-md">
                        <div class="row q-col-gutter-md">
                          <div class="col-6">
                            <div
                              class="text-caption text-grey-5"
                              style="
                                font-size: 11px;
                                text-transform: uppercase;
                                letter-spacing: 0.5px;
                                margin-bottom: 4px;
                              "
                            >
                              Wallet Type
                            </div>
                            <div
                              class="field-value-text"
                              style="font-size: 14px; font-weight: 700; color: #212121"
                            >
                              {{ selectedAccount.type || '—' }}
                            </div>
                          </div>

                          <div class="col-6">
                            <div
                              class="text-caption text-grey-5"
                              style="
                                font-size: 11px;
                                text-transform: uppercase;
                                letter-spacing: 0.5px;
                                margin-bottom: 4px;
                              "
                            >
                              Network Fee Paid
                            </div>
                            <div
                              class="field-value-text"
                              style="font-size: 14px; font-weight: 700; color: #212121"
                            >
                              {{ selectedAccount.totalFees || '0' }} BCH
                            </div>
                          </div>

                          <div class="col-12">
                            <div
                              class="text-caption text-grey-5"
                              style="
                                font-size: 11px;
                                text-transform: uppercase;
                                letter-spacing: 0.5px;
                                margin-bottom: 4px;
                              "
                            >
                              BCH Address
                            </div>
                            <div
                              class="bch-address-box"
                              style="
                                font-size: 12px;
                                font-weight: 600;
                                font-family: monospace;
                                color: #1565c0;
                                background: #e8f0fe;
                                border-radius: 6px;
                                padding: 8px 12px;
                                word-break: break-all;
                                cursor: pointer;
                              "
                              @click="
                                $q.copyToClipboard(selectedAccount.address).then(() =>
                                  $q.notify({
                                    type: 'positive',
                                    message: 'Address copied',
                                    position: 'top',
                                    timeout: 1500,
                                  }),
                                )
                              "
                            >
                              {{ selectedAccount.address || '—' }}
                              <q-icon name="content_copy" size="13px" class="q-ml-xs text-blue-8" />
                            </div>
                          </div>

                          <div class="col-6">
                            <div
                              class="text-caption text-grey-5"
                              style="
                                font-size: 11px;
                                text-transform: uppercase;
                                letter-spacing: 0.5px;
                                margin-bottom: 4px;
                              "
                            >
                              Total Received
                            </div>
                            <div
                              class="total-received-value"
                              style="font-size: 18px; font-weight: 800; color: #1565c0"
                            >
                              {{ formatCurrency(selectedAccount.totalReceived) }}
                              <span
                                class="bch-unit-label"
                                style="font-size: 12px; font-weight: 600; color: #90a4ae"
                                >BCH</span
                              >
                            </div>
                          </div>

                          <div class="col-6">
                            <div
                              class="text-caption text-grey-5"
                              style="
                                font-size: 11px;
                                text-transform: uppercase;
                                letter-spacing: 0.5px;
                                margin-bottom: 4px;
                              "
                            >
                              Available Balance
                            </div>
                            <div
                              class="available-balance-value"
                              style="font-size: 18px; font-weight: 800; color: #2e7d32"
                            >
                              {{ formatCurrency(selectedAccount.available) }}
                              <span
                                class="bch-unit-label"
                                style="font-size: 12px; font-weight: 600; color: #90a4ae"
                                >BCH</span
                              >
                            </div>
                          </div>
                        </div>
                      </q-card-section>
                    </q-card>
                  </div>

                  <!-- Donation Statistics -->
                  <div class="col-12 col-md-6">
                    <q-card flat class="detail-info-card" style="border-radius: 14px; height: 100%">
                      <q-card-section class="q-pb-xs">
                        <div class="row items-center justify-between">
                          <div
                            class="info-card-title"
                            style="font-size: 14px; font-weight: 700; color: #37474f"
                          >
                            Donation Statistics
                          </div>
                          <q-icon name="bar_chart" color="purple-4" size="20px" />
                        </div>
                      </q-card-section>
                      <q-separator />
                      <q-card-section class="q-pt-md">
                        <div class="row q-col-gutter-md">
                          <div class="col-6">
                            <div
                              class="text-caption text-grey-5"
                              style="
                                font-size: 11px;
                                text-transform: uppercase;
                                letter-spacing: 0.5px;
                                margin-bottom: 4px;
                              "
                            >
                              Total Donations
                            </div>
                            <div
                              class="field-value-text"
                              style="font-size: 14px; font-weight: 700; color: #212121"
                            >
                              {{ selectedAccount.transactionCount || 0 }}
                            </div>
                          </div>

                          <div class="col-6">
                            <div
                              class="text-caption text-grey-5"
                              style="
                                font-size: 11px;
                                text-transform: uppercase;
                                letter-spacing: 0.5px;
                                margin-bottom: 4px;
                              "
                            >
                              Active Since
                            </div>
                            <div
                              class="field-value-text"
                              style="font-size: 14px; font-weight: 700; color: #212121"
                            >
                              {{
                                nonprofitDetail?.created_at
                                  ? new Date(nonprofitDetail.created_at).toLocaleDateString(
                                      'en-US',
                                      { month: 'short', day: 'numeric', year: 'numeric' },
                                    )
                                  : '—'
                              }}
                            </div>
                          </div>

                          <div class="col-6">
                            <div
                              class="text-caption text-grey-5"
                              style="
                                font-size: 11px;
                                text-transform: uppercase;
                                letter-spacing: 0.5px;
                                margin-bottom: 4px;
                              "
                            >
                              First Donation
                            </div>
                            <div
                              class="field-value-text"
                              style="font-size: 14px; font-weight: 700; color: #212121"
                            >
                              {{ selectedAccount.firstDonation || '—' }}
                            </div>
                          </div>

                          <div class="col-6">
                            <div
                              class="text-caption text-grey-5"
                              style="
                                font-size: 11px;
                                text-transform: uppercase;
                                letter-spacing: 0.5px;
                                margin-bottom: 4px;
                              "
                            >
                              Last Donation
                            </div>
                            <div
                              class="field-value-text"
                              style="font-size: 14px; font-weight: 700; color: #212121"
                            >
                              {{ selectedAccount.lastDonation || '—' }}
                            </div>
                          </div>

                          <div class="col-12">
                            <div
                              class="text-caption text-grey-5"
                              style="
                                font-size: 11px;
                                text-transform: uppercase;
                                letter-spacing: 0.5px;
                                margin-bottom: 6px;
                              "
                            >
                              Charity Description
                            </div>
                            <div
                              class="description-box"
                              style="
                                font-size: 13px;
                                color: #546e7a;
                                line-height: 1.6;
                                background: #fafafa;
                                border-radius: 8px;
                                padding: 10px 12px;
                                border: 1px solid #f0f0f0;
                              "
                            >
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

                    <!-- Donut: BCH per donation send -->
                    <div class="col-12 col-md-6">
                      <q-card flat class="detail-info-card dash-chart-card">
                        <q-card-section class="q-pb-xs">
                          <div class="row items-center justify-between">
                            <div>
                              <div class="dash-chart-card-title">Donations per Send</div>
                              <div class="dash-chart-card-sub">
                                {{
                                  selectedAccount
                                    ? selectedAccount.name + "'s sends"
                                    : 'Select a donor'
                                }}
                              </div>
                            </div>
                            <q-icon name="donut_large" color="purple-4" size="20px" />
                          </div>
                        </q-card-section>
                        <q-separator />
                        <q-card-section class="q-pa-md" style="position: relative">
                          <div class="dash-chart-canvas">
                            <DoughnutChart
                              :data="dashDonutChartData"
                              :options="dashDonutChartOptions"
                            />
                          </div>
                          <!-- Center total label -->
                          <div class="dash-donut-center">
                            <div class="dash-donut-total">{{ dashDonutTotal }}</div>
                            <div class="dash-donut-label">BCH</div>
                          </div>
                        </q-card-section>
                      </q-card>
                    </div>
                  </div>
                </div> </template
              ><!-- end v-else (not loading) -->
            </q-tab-panel>

            <q-tab-panel name="pending">
              <!-- Header -->
              <div class="row items-center justify-between q-mb-md">
                <div>
                  <div class="text-h6 text-weight-bold">Scheduled Withdrawals</div>
                  <div class="text-caption text-grey-6">
                    Full cycle schedule for each active contract
                  </div>
                </div>
                <q-chip
                  color="orange-2"
                  text-color="orange-9"
                  icon="pending_actions"
                  :label="`${pendingScheduleGroups.length} contract${pendingScheduleGroups.length !== 1 ? 's' : ''}`"
                  style="font-weight: 700"
                />
              </div>

              <!-- Empty state -->
              <div
                v-if="pendingScheduleGroups.length === 0"
                class="text-center q-py-xl pending-empty-state"
              >
                <q-icon name="pending_actions" size="48px" color="grey-4" />
                <div class="text-grey-6 q-mt-sm text-weight-medium">No scheduled withdrawals</div>
                <div class="text-caption text-grey-4 q-mt-xs">
                  Active contract cycles will appear here once set up
                </div>
              </div>

              <!-- Contract schedule groups -->
              <div v-else>
                <div v-for="group in pendingScheduleGroups" :key="group.donationId" class="q-mb-xl">
                  <!-- Contract header card -->
                  <div
                    class="contract-header-card"
                    :style="{
                      background: group.hasDue
                        ? $q.dark.isActive
                          ? 'linear-gradient(135deg, #2a1e00 0%, #2d2100 100%)'
                          : 'linear-gradient(135deg, #fff8e1 0%, #fff3cd 100%)'
                        : $q.dark.isActive
                          ? 'linear-gradient(135deg, #0d1a3d 0%, #151435 100%)'
                          : 'linear-gradient(135deg, #e8f0fe 0%, #ede7f6 100%)',
                      borderRadius: '12px',
                      padding: '16px 20px',
                      marginBottom: '10px',
                      border: group.hasDue
                        ? $q.dark.isActive
                          ? '1px solid #7a5400'
                          : '1px solid #ffcc02'
                        : $q.dark.isActive
                          ? '1px solid #2e3f6e'
                          : '1px solid #c5d8ff',
                    }"
                  >
                    <div class="row items-center justify-between no-wrap">
                      <div style="min-width: 0; flex: 1">
                        <div
                          class="ellipsis contract-donor-name"
                          style="font-size: 16px; font-weight: 700; color: #1a237e"
                        >
                          {{ group.donorName }}
                        </div>
                        <div
                          class="text-caption q-mt-xs contract-meta-caption"
                          style="color: #546e7a"
                        >
                          <q-icon name="schedule" size="13px" />
                          <span class="q-ml-xs">{{ group.intervalLabel }} interval</span>
                          &nbsp;&middot;&nbsp;
                          <q-icon name="currency_bitcoin" size="13px" />
                          <span class="q-ml-xs">{{ group.amountBch }} BCH per cycle</span>
                          &nbsp;&middot;&nbsp;
                          <q-icon name="repeat" size="13px" />
                          <span class="q-ml-xs"
                            >{{ group.cyclesRemaining }} of {{ group.totalCycles }} cycles
                            remaining</span
                          >
                        </div>
                      </div>
                      <div class="q-ml-md row items-center q-gutter-sm">
                        <q-chip
                          dense
                          :color="group.hasDue ? 'orange-2' : 'blue-3'"
                          :text-color="group.hasDue ? 'orange-9' : 'blue-9'"
                          :label="group.hasDue ? 'Due Now' : 'On Schedule'"
                          :icon="group.hasDue ? 'warning' : 'event'"
                          style="font-weight: 700"
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
                  <div class="cycle-table-wrapper">
                    <!-- Table header — hidden on mobile, replaced by card labels -->
                    <div class="row items-center cycle-table-header gt-sm">
                      <div class="col-2 cycle-col-label">Cycle</div>
                      <div class="col-4 cycle-col-label">Scheduled Date</div>
                      <div class="col-3 text-right cycle-col-label">Amount</div>
                      <div class="col-3 text-center cycle-col-label">Status</div>
                    </div>

                    <!-- Desktop cycle rows -->
                    <div
                      v-for="(cycle, idx) in group.cycles"
                      :key="cycle.cycleNumber"
                      class="gt-sm row items-center cycle-row"
                      :style="{
                        padding: '11px 18px',
                        borderBottom:
                          idx < group.cycles.length - 1
                            ? $q.dark.isActive
                              ? '1px solid #1e2d50'
                              : '1px solid #f0f4f8'
                            : 'none',
                        background:
                          cycle.status === 'due'
                            ? $q.dark.isActive
                              ? '#1f1a00'
                              : '#fffde7'
                            : idx % 2 === 0
                              ? $q.dark.isActive
                                ? '#0f1629'
                                : '#ffffff'
                              : $q.dark.isActive
                                ? '#111d3a'
                                : '#fafbfc',
                        transition: 'background 0.2s',
                      }"
                    >
                      <div class="col-2">
                        <q-chip
                          dense
                          :color="
                            cycle.status === 'due'
                              ? 'orange-3'
                              : cycle.status === 'next'
                                ? 'blue-3'
                                : 'blue-grey-2'
                          "
                          :text-color="
                            cycle.status === 'due'
                              ? 'orange-10'
                              : cycle.status === 'next'
                                ? 'blue-10'
                                : 'blue-grey-8'
                          "
                          :label="`#${cycle.cycleNumber}`"
                          style="
                            font-size: 11px;
                            font-weight: 800;
                            border-radius: 6px;
                            height: 22px;
                          "
                        />
                      </div>
                      <div class="col-4">
                        <div
                          class="cycle-date-text"
                          style="font-size: 13px; font-weight: 600; color: #263238"
                        >
                          {{
                            cycle.dueAt.toLocaleDateString('en-US', {
                              month: 'short',
                              day: 'numeric',
                              year: 'numeric',
                            })
                          }}
                        </div>
                        <div class="cycle-time-text" style="font-size: 11px; color: #9e9e9e">
                          {{
                            cycle.dueAt.toLocaleTimeString('en-US', {
                              hour: '2-digit',
                              minute: '2-digit',
                            })
                          }}
                        </div>
                      </div>
                      <div class="col-3 text-right">
                        <div
                          class="cycle-amount-text"
                          style="font-size: 13px; font-weight: 700; color: #1565c0"
                        >
                          {{ cycle.amountBch }}
                        </div>
                        <div class="cycle-bch-label" style="font-size: 10px; color: #90a4ae">
                          BCH
                        </div>
                      </div>
                      <div class="col-3 text-center">
                        <div class="row justify-center items-center q-gutter-xs">
                          <q-btn
                            v-if="cycle.status === 'due' && cycle.payoutId"
                            unelevated
                            color="positive"
                            label="Withdraw"
                            size="xs"
                            no-caps
                            style="font-weight: 700; min-width: 80px"
                            @click="
                              handleSmartWithdraw({
                                duePayoutId: cycle.payoutId,
                                amount: parseFloat(cycle.amountBch),
                                donorName: group.donorName,
                                nonprofit: selectedAccount.nonprofitId,
                              })
                            "
                          />
                          <q-badge
                            v-else-if="cycle.status === 'due'"
                            color="orange"
                            label="Due Now"
                            style="font-weight: 700"
                          />
                          <q-badge
                            v-else-if="cycle.status === 'next'"
                            color="blue"
                            text-color="white"
                            label="Next"
                            style="font-weight: 600"
                          />
                          <q-badge
                            v-else-if="cycle.status === 'upcoming'"
                            color="blue-grey-3"
                            text-color="blue-grey-8"
                            label="Upcoming"
                          />
                          <q-badge v-else color="grey-3" text-color="grey-8" label="Scheduled" />
                        </div>
                      </div>
                    </div>

                    <!-- Mobile cycle cards -->
                    <div
                      v-for="cycle in group.cycles"
                      :key="`m-${cycle.cycleNumber}`"
                      class="lt-md cycle-mobile-card"
                      :class="{ 'cycle-mobile-card--due': cycle.status === 'due' }"
                    >
                      <div class="cycle-mobile-card__top">
                        <q-chip
                          dense
                          :color="
                            cycle.status === 'due'
                              ? 'orange-3'
                              : cycle.status === 'next'
                                ? 'blue-3'
                                : 'blue-grey-2'
                          "
                          :text-color="
                            cycle.status === 'due'
                              ? 'orange-10'
                              : cycle.status === 'next'
                                ? 'blue-10'
                                : 'blue-grey-8'
                          "
                          :label="`Cycle #${cycle.cycleNumber}`"
                          style="
                            font-size: 11px;
                            font-weight: 800;
                            border-radius: 6px;
                            height: 22px;
                          "
                        />
                        <div class="row items-center q-gutter-xs">
                          <q-btn
                            v-if="cycle.status === 'due' && cycle.payoutId"
                            unelevated
                            color="positive"
                            label="Withdraw"
                            size="xs"
                            no-caps
                            style="font-weight: 700"
                            @click="
                              handleSmartWithdraw({
                                duePayoutId: cycle.payoutId,
                                amount: parseFloat(cycle.amountBch),
                                donorName: group.donorName,
                                nonprofit: selectedAccount.nonprofitId,
                              })
                            "
                          />
                          <q-badge
                            v-else-if="cycle.status === 'due'"
                            color="orange"
                            label="Due Now"
                            style="font-weight: 700"
                          />
                          <q-badge
                            v-else-if="cycle.status === 'next'"
                            color="blue"
                            text-color="white"
                            label="Next"
                            style="font-weight: 600"
                          />
                          <q-badge
                            v-else-if="cycle.status === 'upcoming'"
                            color="blue-grey-3"
                            text-color="blue-grey-8"
                            label="Upcoming"
                          />
                          <q-badge v-else color="grey-3" text-color="grey-8" label="Scheduled" />
                        </div>
                      </div>
                      <div class="cycle-mobile-card__info">
                        <div class="cycle-mobile-card__row">
                          <span class="cycle-mobile-card__label">Date</span>
                          <span class="cycle-mobile-card__value cycle-date-text">
                            {{
                              cycle.dueAt.toLocaleDateString('en-US', {
                                month: 'short',
                                day: 'numeric',
                                year: 'numeric',
                              })
                            }}
                            <span class="cycle-time-text q-ml-xs">{{
                              cycle.dueAt.toLocaleTimeString('en-US', {
                                hour: '2-digit',
                                minute: '2-digit',
                              })
                            }}</span>
                          </span>
                        </div>
                        <div class="cycle-mobile-card__row">
                          <span class="cycle-mobile-card__label">Amount</span>
                          <span class="cycle-mobile-card__value cycle-amount-text text-weight-bold"
                            >{{ cycle.amountBch }}
                            <span style="font-size: 10px; color: #90a4ae">BCH</span></span
                          >
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </q-tab-panel>

            <!-- ═══════════════════════════════════════════════════════
                 Organization Profile Tab
                 ═══════════════════════════════════════════════════════ -->
            <q-tab-panel v-if="nonprofitProfile" name="profile" class="details-panel q-pa-none">
              <!-- Skeleton while loading -->
              <template v-if="loadingProfile">
                <div class="detail-skeleton-card q-mb-md">
                  <div class="row items-center no-wrap" style="gap: 18px; padding: 20px">
                    <q-skeleton
                      type="QAvatar"
                      size="72px"
                      style="border-radius: 50%; flex-shrink: 0"
                    />
                    <div style="flex: 1">
                      <q-skeleton type="text" width="40%" style="margin-bottom: 8px" />
                      <q-skeleton type="text" width="25%" style="margin-bottom: 6px" />
                      <q-skeleton type="QBadge" width="70px" />
                    </div>
                  </div>
                </div>
                <div class="row q-col-gutter-md q-mb-md">
                  <div class="col-12 col-md-6">
                    <div class="detail-skeleton-card" style="padding: 18px">
                      <q-skeleton type="text" width="40%" style="margin-bottom: 14px" />
                      <q-skeleton type="QInput" style="margin-bottom: 10px; height: 36px" />
                      <q-skeleton type="QInput" style="margin-bottom: 10px; height: 36px" />
                      <q-skeleton type="QInput" style="height: 36px" />
                    </div>
                  </div>
                  <div class="col-12 col-md-6">
                    <div class="detail-skeleton-card" style="padding: 18px">
                      <q-skeleton type="text" width="40%" style="margin-bottom: 14px" />
                      <q-skeleton type="QInput" style="margin-bottom: 10px; height: 36px" />
                      <q-skeleton type="QInput" style="margin-bottom: 10px; height: 36px" />
                      <q-skeleton type="QInput" style="height: 36px" />
                    </div>
                  </div>
                </div>
              </template>

              <template v-else>
                <!-- Profile Header Card -->
                <q-card
                  flat
                  class="detail-info-card"
                  style="border-radius: 14px; margin-bottom: 16px; overflow: hidden"
                >
                  <q-card-section class="q-pa-none">
                    <div class="row no-wrap items-stretch profile-header-row">
                      <!-- Left: Logo + name + category -->
                      <div
                        class="row items-center q-pa-lg profile-left-col"
                        style="
                          flex: 0 0 auto;
                          min-width: 260px;
                          border-right: 1px solid #f0f0f0;
                          gap: 18px;
                        "
                      >
                        <div style="flex-shrink: 0">
                          <div
                            v-if="nonprofitProfile.logo_url"
                            style="
                              width: 72px;
                              height: 72px;
                              border-radius: 50%;
                              overflow: hidden;
                              border: 3px solid #e8f0fe;
                            "
                          >
                            <img
                              :src="nonprofitProfile.logo_url"
                              style="width: 100%; height: 100%; object-fit: cover"
                            />
                          </div>
                          <div
                            v-else
                            style="
                              width: 72px;
                              height: 72px;
                              border-radius: 50%;
                              background: linear-gradient(135deg, #1565c0, #0d47a1);
                              display: flex;
                              align-items: center;
                              justify-content: center;
                              border: 3px solid #e8f0fe;
                              flex-shrink: 0;
                            "
                          >
                            <span style="font-size: 28px; font-weight: 800; color: white">
                              {{ nonprofitProfile.name?.charAt(0)?.toUpperCase() || 'N' }}
                            </span>
                          </div>
                        </div>
                        <div style="min-width: 0">
                          <div
                            style="
                              font-size: 18px;
                              font-weight: 700;
                              color: #1a237e;
                              line-height: 1.2;
                            "
                            class="ellipsis org-name-text"
                          >
                            {{ nonprofitProfile.name }}
                          </div>
                          <div
                            class="q-mt-xs"
                            style="display: flex; align-items: center; gap: 6px; flex-wrap: wrap"
                          >
                            <span
                              class="org-category-text"
                              style="font-size: 13px; color: #1976d2; font-weight: 600"
                            >
                              {{
                                CATEGORY_LABELS[nonprofitProfile.category] ||
                                nonprofitProfile.category
                              }}
                            </span>
                            <span style="color: #bdbdbd">|</span>
                            <span class="org-status-text" style="font-size: 12px; color: #9e9e9e">
                              {{
                                nonprofitProfile.active === false
                                  ? 'Inactive'
                                  : 'Active Organization'
                              }}
                            </span>
                          </div>
                          <q-chip
                            v-if="nonprofitProfile.verified"
                            dense
                            color="green-2"
                            text-color="green-8"
                            icon="verified"
                            label="Verified"
                            style="font-size: 11px; font-weight: 700; margin-top: 8px"
                          />
                          <q-chip
                            v-else
                            dense
                            color="grey-2"
                            text-color="grey-7"
                            icon="schedule"
                            label="Unverified"
                            style="font-size: 11px; margin-top: 8px"
                          />
                        </div>
                      </div>
                      <!-- Right: Quick stats -->
                      <div
                        class="row items-center q-px-lg q-py-md profile-stats-col"
                        style="flex: 1; gap: 0; flex-wrap: wrap"
                      >
                        <div
                          v-for="stat in [
                            {
                              label: 'BCH Address',
                              value: nonprofitProfile.bch_address || '—',
                              mono: true,
                              icon: 'account_balance_wallet',
                            },
                            {
                              label: 'Website',
                              value: nonprofitProfile.website || '—',
                              link: nonprofitProfile.website,
                              icon: 'language',
                            },
                            {
                              label: 'Email',
                              value: nonprofitProfile.email || '—',
                              icon: 'mail_outline',
                            },
                            { label: 'Phone', value: nonprofitProfile.phone || '—', icon: 'phone' },
                          ]"
                          :key="stat.label"
                          style="min-width: 50%; padding: 10px 16px 10px 0"
                        >
                          <div
                            class="text-caption text-grey-5"
                            style="
                              font-size: 11px;
                              font-weight: 700;
                              text-transform: uppercase;
                              letter-spacing: 0.5px;
                              margin-bottom: 3px;
                            "
                          >
                            <q-icon :name="stat.icon" size="12px" class="q-mr-xs" />{{ stat.label }}
                          </div>
                          <a
                            v-if="stat.link"
                            :href="stat.link"
                            target="_blank"
                            style="
                              font-size: 13px;
                              font-weight: 600;
                              color: #1976d2;
                              word-break: break-all;
                              text-decoration: none;
                            "
                            >{{ stat.value }}</a
                          >
                          <div
                            v-else
                            class="stat-value-text"
                            :style="{
                              fontSize: '13px',
                              fontWeight: 600,
                              wordBreak: 'break-all',
                              fontFamily: stat.mono ? 'monospace' : 'inherit',
                            }"
                          >
                            {{ stat.value }}
                          </div>
                        </div>
                      </div>
                    </div>
                  </q-card-section>
                </q-card>

                <!-- Two column info cards -->
                <div class="row q-col-gutter-md q-mb-md">
                  <!-- Organization Information -->
                  <div class="col-12 col-md-6">
                    <q-card flat class="detail-info-card" style="border-radius: 14px; height: 100%">
                      <q-card-section class="q-pb-xs">
                        <div class="row items-center justify-between">
                          <div
                            class="info-card-title"
                            style="font-size: 14px; font-weight: 700; color: #37474f"
                          >
                            Organization Information
                          </div>
                          <q-icon name="business" color="blue-4" size="20px" />
                        </div>
                      </q-card-section>
                      <q-separator />
                      <q-card-section class="q-pt-md">
                        <div class="row q-col-gutter-md">
                          <div class="col-6">
                            <div
                              class="text-caption text-grey-5"
                              style="
                                font-size: 11px;
                                text-transform: uppercase;
                                letter-spacing: 0.5px;
                                margin-bottom: 4px;
                              "
                            >
                              Organization Name
                            </div>
                            <div
                              class="field-value-text"
                              style="font-size: 14px; font-weight: 700; color: #212121"
                            >
                              {{ nonprofitProfile.name }}
                            </div>
                          </div>
                          <div class="col-6">
                            <div
                              class="text-caption text-grey-5"
                              style="
                                font-size: 11px;
                                text-transform: uppercase;
                                letter-spacing: 0.5px;
                                margin-bottom: 4px;
                              "
                            >
                              Category
                            </div>
                            <div
                              class="field-value-text"
                              style="font-size: 14px; font-weight: 700; color: #212121"
                            >
                              {{
                                CATEGORY_LABELS[nonprofitProfile.category] ||
                                nonprofitProfile.category
                              }}
                            </div>
                          </div>
                          <div class="col-12">
                            <div
                              class="text-caption text-grey-5"
                              style="
                                font-size: 11px;
                                text-transform: uppercase;
                                letter-spacing: 0.5px;
                                margin-bottom: 4px;
                              "
                            >
                              BCH Wallet Address
                            </div>
                            <div
                              class="bch-address-box"
                              style="
                                font-size: 12px;
                                font-weight: 600;
                                font-family: monospace;
                                color: #1565c0;
                                background: #e8f0fe;
                                border-radius: 6px;
                                padding: 8px 12px;
                                word-break: break-all;
                                cursor: pointer;
                              "
                              @click="
                                $q.copyToClipboard(nonprofitProfile.bch_address).then(() =>
                                  $q.notify({
                                    type: 'positive',
                                    message: 'Address copied',
                                    position: 'top',
                                    timeout: 1500,
                                  }),
                                )
                              "
                            >
                              {{ nonprofitProfile.bch_address }}
                              <q-icon name="content_copy" size="13px" class="q-ml-xs text-blue-8" />
                            </div>
                          </div>
                          <div class="col-6">
                            <div
                              class="text-caption text-grey-5"
                              style="
                                font-size: 11px;
                                text-transform: uppercase;
                                letter-spacing: 0.5px;
                                margin-bottom: 4px;
                              "
                            >
                              Website
                            </div>
                            <a
                              v-if="nonprofitProfile.website"
                              :href="nonprofitProfile.website"
                              target="_blank"
                              style="
                                font-size: 14px;
                                font-weight: 600;
                                color: #1976d2;
                                text-decoration: none;
                              "
                              >{{ nonprofitProfile.website }}</a
                            >
                            <div
                              v-else
                              class="field-value-text"
                              style="font-size: 14px; font-weight: 700; color: #212121"
                            >
                              —
                            </div>
                          </div>
                          <div class="col-6">
                            <div
                              class="text-caption text-grey-5"
                              style="
                                font-size: 11px;
                                text-transform: uppercase;
                                letter-spacing: 0.5px;
                                margin-bottom: 4px;
                              "
                            >
                              Email
                            </div>
                            <div
                              class="field-value-text"
                              style="font-size: 14px; font-weight: 700; color: #212121"
                            >
                              {{ nonprofitProfile.email || '—' }}
                            </div>
                          </div>
                          <div class="col-6">
                            <div
                              class="text-caption text-grey-5"
                              style="
                                font-size: 11px;
                                text-transform: uppercase;
                                letter-spacing: 0.5px;
                                margin-bottom: 4px;
                              "
                            >
                              Phone
                            </div>
                            <div
                              class="field-value-text"
                              style="font-size: 14px; font-weight: 700; color: #212121"
                            >
                              {{ nonprofitProfile.phone || '—' }}
                            </div>
                          </div>
                          <div class="col-6">
                            <div
                              class="text-caption text-grey-5"
                              style="
                                font-size: 11px;
                                text-transform: uppercase;
                                letter-spacing: 0.5px;
                                margin-bottom: 4px;
                              "
                            >
                              Member Since
                            </div>
                            <div
                              class="field-value-text"
                              style="font-size: 14px; font-weight: 700; color: #212121"
                            >
                              {{
                                nonprofitProfile.created_at
                                  ? new Date(nonprofitProfile.created_at).toLocaleDateString(
                                      'en-US',
                                      { month: 'short', day: 'numeric', year: 'numeric' },
                                    )
                                  : '—'
                              }}
                            </div>
                          </div>
                        </div>
                      </q-card-section>
                    </q-card>
                  </div>

                  <!-- Donation Overview -->
                  <div class="col-12 col-md-6">
                    <q-card flat class="detail-info-card" style="border-radius: 14px; height: 100%">
                      <q-card-section class="q-pb-xs">
                        <div class="row items-center justify-between">
                          <div
                            class="info-card-title"
                            style="font-size: 14px; font-weight: 700; color: #37474f"
                          >
                            Donation Overview
                          </div>
                          <q-icon name="bar_chart" color="purple-4" size="20px" />
                        </div>
                      </q-card-section>
                      <q-separator />
                      <q-card-section class="q-pt-md">
                        <div class="row q-col-gutter-md">
                          <div class="col-6">
                            <div
                              class="text-caption text-grey-5"
                              style="
                                font-size: 11px;
                                text-transform: uppercase;
                                letter-spacing: 0.5px;
                                margin-bottom: 4px;
                              "
                            >
                              Total Received
                            </div>
                            <div
                              class="total-received-value"
                              style="font-size: 18px; font-weight: 800; color: #1565c0"
                            >
                              {{ parseFloat(nonprofitProfile.total_received_bch || 0).toFixed(8) }}
                              <span
                                class="bch-unit-label"
                                style="font-size: 12px; font-weight: 600; color: #90a4ae"
                                >BCH</span
                              >
                            </div>
                          </div>
                          <div class="col-6">
                            <div
                              class="text-caption text-grey-5"
                              style="
                                font-size: 11px;
                                text-transform: uppercase;
                                letter-spacing: 0.5px;
                                margin-bottom: 4px;
                              "
                            >
                              Total Donations
                            </div>
                            <div
                              class="field-value-text"
                              style="font-size: 18px; font-weight: 800; color: #2e7d32"
                            >
                              {{ nonprofitProfile.donation_count || 0 }}
                            </div>
                          </div>
                          <div class="col-6">
                            <div
                              class="text-caption text-grey-5"
                              style="
                                font-size: 11px;
                                text-transform: uppercase;
                                letter-spacing: 0.5px;
                                margin-bottom: 4px;
                              "
                            >
                              Unique Donors
                            </div>
                            <div
                              class="field-value-text"
                              style="font-size: 14px; font-weight: 700; color: #212121"
                            >
                              {{ nonprofitProfile.unique_donor_count || 0 }}
                            </div>
                          </div>
                          <div class="col-6">
                            <div
                              class="text-caption text-grey-5"
                              style="
                                font-size: 11px;
                                text-transform: uppercase;
                                letter-spacing: 0.5px;
                                margin-bottom: 4px;
                              "
                            >
                              Verification
                            </div>
                            <q-chip
                              v-if="nonprofitProfile.verified"
                              dense
                              color="green-2"
                              text-color="green-8"
                              icon="verified"
                              label="Verified"
                              style="font-size: 11px; font-weight: 700"
                            />
                            <q-chip
                              v-else
                              dense
                              color="grey-2"
                              text-color="grey-7"
                              icon="schedule"
                              label="Unverified"
                              style="font-size: 11px"
                            />
                          </div>
                          <div class="col-12">
                            <div
                              class="text-caption text-grey-5"
                              style="
                                font-size: 11px;
                                text-transform: uppercase;
                                letter-spacing: 0.5px;
                                margin-bottom: 6px;
                              "
                            >
                              Description
                            </div>
                            <div
                              class="description-box"
                              style="
                                font-size: 13px;
                                color: #546e7a;
                                line-height: 1.6;
                                background: #fafafa;
                                border-radius: 8px;
                                padding: 10px 12px;
                                border: 1px solid #f0f0f0;
                              "
                            >
                              {{ nonprofitProfile.description || 'No description available.' }}
                            </div>
                          </div>
                        </div>
                      </q-card-section>
                    </q-card>
                  </div>
                </div>

                <!-- Received Donations Table -->
                <div class="q-mt-md">
                  <div class="row items-center justify-between q-mb-md">
                    <div>
                      <div class="text-h6 text-weight-bold">Received Donations</div>
                      <div class="text-caption text-grey-6">All donations received from donors</div>
                    </div>
                    <q-chip
                      color="blue-2"
                      text-color="blue-9"
                      icon="volunteer_activism"
                      :label="`${nonprofitProfile.donations?.length || 0} donation${(nonprofitProfile.donations?.length || 0) !== 1 ? 's' : ''}`"
                      style="font-weight: 700"
                    />
                  </div>

                  <div
                    v-if="!nonprofitProfile.donations?.length"
                    class="text-center q-py-xl"
                    style="border: 2px dashed #e0e0e0; border-radius: 12px"
                  >
                    <q-icon name="volunteer_activism" size="48px" color="grey-4" />
                    <div class="text-grey-6 q-mt-sm text-weight-medium">
                      No donations received yet
                    </div>
                    <div class="text-caption text-grey-4 q-mt-xs">
                      Donations will appear here once donors contribute
                    </div>
                  </div>

                  <q-table
                    v-else
                    :rows="nonprofitProfile.donations"
                    :columns="profileDonationColumns"
                    row-key="id"
                    flat
                    bordered
                    :pagination="{ rowsPerPage: 15, sortBy: 'timestamp', descending: true }"
                    class="transactions-table"
                    :grid="$q.screen.lt.md"
                  >
                    <template v-slot:body-cell-timestamp="props">
                      <q-td :props="props">
                        <div class="text-weight-medium" style="font-size: 13px">
                          {{
                            new Date(props.row.timestamp).toLocaleDateString('en-US', {
                              month: 'short',
                              day: 'numeric',
                              year: 'numeric',
                            })
                          }}
                        </div>
                        <div class="text-caption text-grey-6">
                          {{
                            new Date(props.row.timestamp).toLocaleTimeString('en-US', {
                              hour: '2-digit',
                              minute: '2-digit',
                            })
                          }}
                        </div>
                      </q-td>
                    </template>
                    <template v-slot:body-cell-donor_name="props">
                      <q-td :props="props">
                        {{ props.row.donor_name || 'Anonymous' }}
                      </q-td>
                    </template>
                    <template v-slot:body-cell-amount="props">
                      <q-td :props="props">
                        <span class="text-weight-bold text-green-8" style="font-size: 14px">
                          {{ parseFloat(props.row.amount).toFixed(8) }}
                        </span>
                        <span class="text-caption text-grey-6 q-ml-xs">BCH</span>
                      </q-td>
                    </template>
                    <template v-slot:body-cell-coin="props">
                      <q-td :props="props" class="text-center">
                        <q-badge color="primary" :label="props.row.coin || 'BCH'" />
                      </q-td>
                    </template>
                    <template v-slot:body-cell-interval="props">
                      <q-td :props="props" class="text-center">
                        <q-badge
                          v-if="props.row.interval"
                          color="blue-2"
                          text-color="blue-9"
                          :label="props.row.interval"
                        />
                        <span v-else class="text-grey-6">One-time</span>
                      </q-td>
                    </template>
                    <template v-slot:body-cell-txid="props">
                      <q-td :props="props">
                        <span
                          v-if="isValidTxid(props.row.txid)"
                          class="text-primary"
                          style="font-family: monospace; font-size: 12px; cursor: pointer"
                          @click="copyTxid(props.row.txid)"
                        >
                          {{ formatTxidPreview(props.row.txid, 18) }}
                          <q-icon name="content_copy" size="12px" class="q-ml-xs" />
                        </span>
                        <span v-else class="text-grey-5 text-caption">—</span>
                      </q-td>
                    </template>

                    <!-- Mobile card layout -->
                    <template v-slot:item="props">
                      <div class="dash-mobile-card">
                        <div class="dash-mobile-card__header">
                          <div class="dash-mobile-card__title">
                            {{ props.row.donor_name || 'Anonymous' }}
                          </div>
                          <q-badge color="primary" :label="props.row.coin || 'BCH'" />
                        </div>
                        <div class="dash-mobile-card__body">
                          <div class="dash-mobile-card__row">
                            <span class="dash-mobile-card__label">Date</span>
                            <span class="dash-mobile-card__value">
                              {{
                                new Date(props.row.timestamp).toLocaleDateString('en-US', {
                                  month: 'short',
                                  day: 'numeric',
                                  year: 'numeric',
                                })
                              }}
                            </span>
                          </div>
                          <div class="dash-mobile-card__row">
                            <span class="dash-mobile-card__label">Amount</span>
                            <span class="dash-mobile-card__value text-green-8 text-weight-bold">
                              {{ parseFloat(props.row.amount).toFixed(8) }} BCH
                            </span>
                          </div>
                          <div class="dash-mobile-card__row">
                            <span class="dash-mobile-card__label">Cause</span>
                            <span class="dash-mobile-card__value">{{
                              props.row.cause || '—'
                            }}</span>
                          </div>
                          <div class="dash-mobile-card__row">
                            <span class="dash-mobile-card__label">Interval</span>
                            <span class="dash-mobile-card__value">
                              <q-badge
                                v-if="props.row.interval"
                                color="blue-7"
                                :label="props.row.interval"
                              />
                              <span v-else class="text-grey-6">One-time</span>
                            </span>
                          </div>
                          <div v-if="isValidTxid(props.row.txid)" class="dash-mobile-card__row">
                            <span class="dash-mobile-card__label">TxID</span>
                            <span
                              class="text-primary dash-mobile-card__txid"
                              @click="copyTxid(props.row.txid)"
                            >
                              {{ formatTxidPreview(props.row.txid, 16) }}
                              <q-icon name="content_copy" size="11px" class="q-ml-xs" />
                            </span>
                          </div>
                        </div>
                      </div>
                    </template>
                  </q-table>
                </div>
              </template>
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
                :grid="$q.screen.lt.md"
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

                <!-- Mobile card layout -->
                <template v-slot:item="props">
                  <div class="dash-mobile-card">
                    <div class="dash-mobile-card__header">
                      <div class="dash-mobile-card__title">
                        {{ props.row.donorName || props.row.description || 'Transaction' }}
                      </div>
                      <q-badge
                        :color="
                          props.row.status === 'completed'
                            ? 'positive'
                            : props.row.status === 'pending'
                              ? 'warning'
                              : 'negative'
                        "
                        :label="props.row.status"
                        style="font-weight: 600; text-transform: capitalize"
                      />
                    </div>
                    <div class="dash-mobile-card__body">
                      <div class="dash-mobile-card__row">
                        <span class="dash-mobile-card__label">Date</span>
                        <span class="dash-mobile-card__value">{{ props.row.date }}</span>
                      </div>
                      <div class="dash-mobile-card__row">
                        <span class="dash-mobile-card__label">Amount</span>
                        <span class="dash-mobile-card__value text-weight-bold"
                          >{{ formatCurrency(props.row.amount) }} BCH</span
                        >
                      </div>
                      <div v-if="props.row.type" class="dash-mobile-card__row">
                        <span class="dash-mobile-card__label">Type</span>
                        <span class="dash-mobile-card__value">{{ props.row.type }}</span>
                      </div>
                      <div v-if="props.row.description" class="dash-mobile-card__row">
                        <span class="dash-mobile-card__label">Message</span>
                        <span class="dash-mobile-card__value dash-mobile-card__desc">{{
                          props.row.description
                        }}</span>
                      </div>
                    </div>
                    <div class="dash-mobile-card__footer">
                      <q-btn
                        flat
                        dense
                        no-caps
                        icon="receipt_long"
                        label="Details"
                        size="sm"
                        color="primary"
                        @click="viewTransactionDetails(props.row)"
                      />
                    </div>
                  </div>
                </template>
              </q-table>
            </q-card-section>
          </q-card>
        </div>
      </div>
    </div>

    <q-dialog
      v-model="withdrawDialog"
      persistent
      :position="$q.screen.lt.sm ? 'bottom' : 'standard'"
    >
      <q-card
        class="withdraw-dialog-card"
        :style="
          $q.screen.lt.sm
            ? 'width: 100vw; max-width: 100vw; border-radius: 16px 16px 0 0;'
            : 'min-width: 400px; max-width: 500px;'
        "
      >
        <q-card-section class="row items-center q-pb-none">
          <div class="text-h6">Withdraw Funds</div>
          <q-space />
          <q-btn icon="close" flat round dense v-close-popup />
        </q-card-section>

        <q-card-section class="withdraw-dialog-content">
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

        <q-card-actions
          :align="$q.screen.lt.sm ? 'stretch' : 'right'"
          :class="
            $q.screen.lt.sm ? 'column q-px-md q-pb-md withdraw-dialog-actions' : 'q-px-md q-pb-md'
          "
          style="gap: 8px"
        >
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
    <q-dialog v-model="txDetailDialog.open" :position="$q.screen.lt.sm ? 'bottom' : 'standard'">
      <q-card class="tx-detail-dialog">
        <!-- Header -->
        <div class="tx-detail-header">
          <div class="row items-center justify-between no-wrap">
            <div>
              <div class="tx-detail-title">Donation Details</div>
              <div class="tx-detail-sub">CrypToCare Charity Dashboard</div>
            </div>
            <q-btn
              flat
              round
              dense
              icon="close"
              @click="txDetailDialog.open = false"
              class="tx-close-btn"
            />
          </div>
        </div>

        <q-card-section class="q-pt-md q-pb-sm">
          <!-- Status badge -->
          <q-badge
            :color="txDetailDialog.statusColor"
            :label="txDetailDialog.data?.status?.toUpperCase()"
            style="
              font-size: 12px;
              font-weight: 700;
              padding: 5px 14px;
              border-radius: 6px;
              letter-spacing: 0.5px;
            "
          />
        </q-card-section>

        <!-- Details rows -->
        <q-card-section class="q-pt-xs q-pb-md tx-detail-content">
          <div class="tx-detail-table">
            <div class="tx-detail-row" v-for="row in txDetailDialog.rows" :key="row.label">
              <div class="tx-detail-label">{{ row.label }}</div>
              <div class="tx-detail-value" :style="row.style">{{ row.value }}</div>
            </div>
            <div class="tx-detail-row tx-detail-row--amount">
              <div class="tx-detail-label" style="font-weight: 700">Amount</div>
              <div
                class="tx-detail-value"
                style="font-size: 18px; font-weight: 800; color: #4caf50"
              >
                {{ txDetailDialog.formattedAmount }} {{ txDetailDialog.data?.type }}
              </div>
            </div>
            <div class="tx-detail-row" v-if="isValidTxid(txDetailDialog.data?.txid)">
              <div class="tx-detail-label">Transaction ID</div>
              <div
                class="tx-detail-value"
                style="font-family: monospace; font-size: 11px; word-break: break-all"
              >
                {{ normalizeTxid(txDetailDialog.data.txid) }}
              </div>
            </div>
            <div class="tx-detail-row" v-else-if="txDetailDialog.data?.txid">
              <div class="tx-detail-label">Transaction ID</div>
              <div class="tx-detail-value text-warning text-weight-medium">Invalid TXID format</div>
            </div>
          </div>

          <!-- Explorer link -->
          <div v-if="isValidTxid(txDetailDialog.data?.txid)" class="text-center q-mt-md">
            <q-btn
              class="tx-detail-explorer-btn"
              unelevated
              color="primary"
              icon="open_in_new"
              :label="
                txDetailDialog.data?.explorerUrl
                  ? 'View on Blockchain Explorer'
                  : 'Explorer Link Unavailable'
              "
              :disable="!txDetailDialog.data?.explorerUrl"
              no-caps
              :href="txDetailDialog.data?.explorerUrl || undefined"
              target="_blank"
              style="border-radius: 8px"
            />
            <div v-if="!txDetailDialog.data?.explorerUrl" class="text-caption text-grey-6 q-mt-xs">
              This TXID is format-valid but has no verified on-chain explorer URL yet.
            </div>
          </div>

          <!-- Note -->
          <div class="tx-detail-note q-mt-md">
            <q-icon name="info_outline" size="14px" class="q-mr-xs" />
            <span
              >This donation is recorded on the Bitcoin Cash blockchain and can be verified through
              the transaction hash.</span
            >
          </div>
        </q-card-section>

        <q-card-actions align="right" class="q-px-md q-pb-md tx-detail-actions">
          <q-btn
            unelevated
            color="primary"
            label="Close"
            no-caps
            style="border-radius: 8px; min-width: 90px"
            @click="txDetailDialog.open = false"
          />
        </q-card-actions>
      </q-card>
    </q-dialog>

    <!-- ═══════════════════════════════════════════════════════════
         Professional Withdraw Confirm Dialog
         ═══════════════════════════════════════════════════════════ -->
    <q-dialog
      v-model="withdrawConfirmDialog.open"
      persistent
      :position="$q.screen.lt.sm ? 'bottom' : 'standard'"
    >
      <q-card
        class="withdraw-confirm-card"
        :style="
          $q.screen.lt.sm
            ? 'width:100vw;max-width:100vw;min-width:unset;border-radius:16px 16px 0 0;'
            : ''
        "
      >
        <!-- ── Gradient Header ──────────────────────────────────── -->
        <div
          :style="{
            background:
              withdrawConfirmDialog.mode === 'inbox_approval'
                ? 'linear-gradient(135deg, #f57c00 0%, #e64a19 100%)'
                : 'linear-gradient(135deg, #1565c0 0%, #0d47a1 100%)',
            padding: '20px 24px',
          }"
        >
          <div class="row items-center no-wrap">
            <div class="wcd-header-icon-circle">
              <q-icon
                :name="
                  withdrawConfirmDialog.mode === 'inbox_approval'
                    ? 'mark_email_read'
                    : 'account_balance_wallet'
                "
                color="white"
                size="22px"
              />
            </div>
            <div style="flex: 1; min-width: 0">
              <div class="text-white text-weight-bold" style="font-size: 17px; line-height: 1.2">
                {{
                  withdrawConfirmDialog.mode === 'inbox_approval'
                    ? 'Request Withdrawal Approval'
                    : 'Confirm Withdrawal'
                }}
              </div>
              <div
                class="text-white ellipsis"
                style="opacity: 0.78; font-size: 12.5px; margin-top: 2px"
              >
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
        <div :class="$q.screen.lt.sm ? 'q-px-sm q-pt-md q-pb-sm' : 'q-px-lg q-pt-lg q-pb-sm'">
          <div class="row q-col-gutter-sm">
            <!-- Total BCH -->
            <div class="col-4">
              <div class="wcd-stat-box wcd-stat-box--blue">
                <q-icon name="currency_bitcoin" color="blue-8" size="20px" />
                <div class="wcd-stat-label wcd-stat-label--blue">Total Amount</div>
                <div class="wcd-stat-value wcd-stat-value--blue">
                  {{ withdrawConfirmDialog.totalBch }}
                </div>
                <div class="wcd-stat-unit wcd-stat-unit--blue">BCH</div>
              </div>
            </div>

            <!-- Payout Count -->
            <div class="col-4">
              <div class="wcd-stat-box wcd-stat-box--green">
                <q-icon name="receipt_long" color="green-8" size="20px" />
                <div class="wcd-stat-label wcd-stat-label--green">Payouts Due</div>
                <div class="wcd-stat-value wcd-stat-value--green">
                  {{ withdrawConfirmDialog.payouts.length }}
                </div>
                <div class="wcd-stat-unit wcd-stat-unit--green">scheduled</div>
              </div>
            </div>

            <!-- Date & Time -->
            <div class="col-4">
              <div class="wcd-stat-box wcd-stat-box--orange">
                <q-icon name="schedule" color="orange-9" size="20px" />
                <div class="wcd-stat-label wcd-stat-label--orange">Executed On</div>
                <div class="wcd-stat-value wcd-stat-value--orange">
                  {{ fmtDialogDate(new Date()) }}
                </div>
                <div class="wcd-stat-unit wcd-stat-unit--orange">
                  {{ fmtDialogTime(new Date()) }}
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- ── Payout Details Table ──────────────────────────────── -->
        <div :class="$q.screen.lt.sm ? 'q-px-sm q-pb-sm' : 'q-px-lg q-pb-sm'">
          <div class="wcd-table-heading">Payout Details</div>
          <div class="wcd-table-wrapper">
            <!-- Desktop: table header -->
            <div v-if="!$q.screen.lt.sm" class="row wcd-table-header">
              <div class="col-5 wcd-col-label">Donor</div>
              <div class="col-3 text-right wcd-col-label">Amount</div>
              <div class="col-2 text-center wcd-col-label">Cycle</div>
              <div class="col text-right wcd-col-label">Scheduled</div>
            </div>

            <!-- Desktop: table rows -->
            <template v-if="!$q.screen.lt.sm">
              <div
                v-for="(payout, idx) in withdrawConfirmDialog.payouts"
                :key="payout.id"
                class="row items-center wcd-table-row"
                :style="{
                  borderBottom:
                    idx < withdrawConfirmDialog.payouts.length - 1
                      ? $q.dark.isActive
                        ? '1px solid #1e2d50'
                        : '1px solid #f0f4f8'
                      : 'none',
                  background:
                    idx % 2 === 0
                      ? $q.dark.isActive
                        ? '#0f1629'
                        : '#ffffff'
                      : $q.dark.isActive
                        ? '#111d3a'
                        : '#fafbfc',
                }"
              >
                <div class="col-5" style="min-width: 0">
                  <div class="ellipsis wcd-donor-name">{{ payout.donorName }}</div>
                  <div class="ellipsis wcd-donor-email">{{ payout.donorEmail || '—' }}</div>
                </div>
                <div class="col-3 text-right">
                  <div class="wcd-payout-amount">{{ payout.amountBch }}</div>
                  <div class="wcd-payout-bch">BCH</div>
                </div>
                <div class="col-2 text-center">
                  <q-chip
                    dense
                    :label="`${payout.cycleNumber} / ${payout.totalCycles}`"
                    color="blue-2"
                    text-color="blue-9"
                    style="font-size: 10px; font-weight: 700; border-radius: 6px; height: 20px"
                  />
                </div>
                <div class="col text-right">
                  <div class="wcd-due-date">{{ fmtDialogDateShort(new Date(payout.dueAt)) }}</div>
                  <div class="wcd-due-time">{{ fmtDialogTime(new Date(payout.dueAt)) }}</div>
                </div>
              </div>
            </template>

            <!-- Mobile: card rows -->
            <template v-else>
              <div
                v-for="(payout, idx) in withdrawConfirmDialog.payouts"
                :key="payout.id"
                class="wcd-mobile-row"
                :style="{
                  borderBottom:
                    idx < withdrawConfirmDialog.payouts.length - 1
                      ? $q.dark.isActive
                        ? '1px solid #1e2d50'
                        : '1px solid #f0f4f8'
                      : 'none',
                  background:
                    idx % 2 === 0
                      ? $q.dark.isActive
                        ? '#0f1629'
                        : '#ffffff'
                      : $q.dark.isActive
                        ? '#111d3a'
                        : '#fafbfc',
                }"
              >
                <div class="row items-start justify-between no-wrap">
                  <div style="min-width: 0; flex: 1">
                    <div class="ellipsis wcd-donor-name">{{ payout.donorName }}</div>
                    <div class="ellipsis wcd-donor-email">{{ payout.donorEmail || '—' }}</div>
                  </div>
                  <div class="text-right" style="flex-shrink: 0; margin-left: 10px">
                    <div class="wcd-payout-amount">{{ payout.amountBch }}</div>
                    <div class="wcd-payout-bch">BCH</div>
                  </div>
                </div>
                <div class="row items-center justify-between q-mt-xs">
                  <q-chip
                    dense
                    :label="`Cycle ${payout.cycleNumber} / ${payout.totalCycles}`"
                    color="blue-2"
                    text-color="blue-9"
                    style="
                      font-size: 10px;
                      font-weight: 700;
                      border-radius: 6px;
                      height: 20px;
                      margin: 0;
                    "
                  />
                  <div class="text-right">
                    <div class="wcd-due-date">{{ fmtDialogDateShort(new Date(payout.dueAt)) }}</div>
                    <div class="wcd-due-time">{{ fmtDialogTime(new Date(payout.dueAt)) }}</div>
                  </div>
                </div>
              </div>
            </template>
          </div>
        </div>

        <!-- ── Mode Notice ───────────────────────────────────────── -->
        <div :class="$q.screen.lt.sm ? 'q-px-sm q-pb-md' : 'q-px-lg q-pb-md'">
          <!-- inbox_approval notice -->
          <div
            v-if="withdrawConfirmDialog.mode === 'inbox_approval'"
            class="wcd-notice wcd-notice--approval"
          >
            <q-icon
              name="mail_outline"
              color="orange-8"
              size="16px"
              style="margin-top: 1px; flex-shrink: 0"
            />
            <div class="wcd-notice-text wcd-notice-text--approval">
              <strong>Approval Required</strong> — An email will be sent to each donor asking them
              to approve this scheduled withdrawal. Funds will only move once they confirm.
            </div>
          </div>
          <!-- smart notice -->
          <div v-else class="wcd-notice wcd-notice--smart">
            <q-icon
              name="bolt"
              color="green-8"
              size="16px"
              style="margin-top: 1px; flex-shrink: 0"
            />
            <div class="wcd-notice-text wcd-notice-text--smart">
              <strong>Smart Withdrawal</strong> — This payout will execute automatically on the
              Bitcoin Cash blockchain. This action cannot be undone.
            </div>
          </div>
        </div>

        <q-separator />

        <!-- ── Action Buttons ────────────────────────────────────── -->
        <q-card-actions
          :align="$q.screen.lt.sm ? 'stretch' : 'right'"
          :class="$q.screen.lt.sm ? 'column-reverse q-pa-md' : 'q-pa-md'"
          style="gap: 8px"
        >
          <q-btn
            flat
            label="Cancel"
            color="grey-7"
            no-caps
            :class="$q.screen.lt.sm ? 'full-width' : ''"
            :disable="withdrawConfirmDialog.loading"
            @click="withdrawConfirmDialog.open = false"
          />
          <q-btn
            unelevated
            :label="
              withdrawConfirmDialog.mode === 'inbox_approval'
                ? 'Send Approval Emails'
                : 'Confirm Withdrawal'
            "
            :color="withdrawConfirmDialog.mode === 'inbox_approval' ? 'deep-orange' : 'positive'"
            no-caps
            :class="$q.screen.lt.sm ? 'full-width' : ''"
            :style="
              $q.screen.lt.sm
                ? 'font-weight: 600; letter-spacing: 0.3px;'
                : 'min-width: 168px; font-weight: 600; letter-spacing: 0.3px;'
            "
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
import { Line as LineChart, Doughnut as DoughnutChart } from 'vue-chartjs'
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  ArcElement,
  Title,
  Tooltip,
  Legend,
  Filler,
} from 'chart.js'

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  ArcElement,
  Title,
  Tooltip,
  Legend,
  Filler,
)
import { api } from 'boot/axios'
import { useRouter } from 'vue-router'
import { useNetworkStore } from 'src/stores/network-store'
import { executeWithdraw, buildVaultRecordFromBackend } from 'src/services/vaultDonation'
import bchImg from 'src/assets/bch.png'
import projectImg from 'src/assets/project.png'
import transactionImg from 'src/assets/transaction.png'

const $q = useQuasar()
const router = useRouter()
const networkStore = useNetworkStore()
const TXID_PATTERN = /^[A-Fa-f0-9]{64}$/

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

// ── Wallet-connected nonprofit profile (by-wallet lookup) ─────────────────────
const WALLET_SNAPSHOT_KEY = 'cryptocare.wallet.snapshot'
const nonprofitProfile = ref(null)
const loadingProfile = ref(false)

const getConnectedWalletAddress = () => {
  try {
    const raw = localStorage.getItem(WALLET_SNAPSHOT_KEY)
    if (!raw) return ''
    const parsed = JSON.parse(raw)
    return parsed?.connected ? parsed.address || '' : ''
  } catch {
    return ''
  }
}

const fetchNonprofitByWallet = async () => {
  const address = getConnectedWalletAddress()
  if (!address) {
    nonprofitProfile.value = null
    return
  }
  loadingProfile.value = true
  try {
    const res = await api.get('nonprofits/by-wallet/', { params: { address } })
    nonprofitProfile.value = res.data
  } catch {
    nonprofitProfile.value = null
  } finally {
    loadingProfile.value = false
  }
}

const CATEGORY_LABELS = {
  animals: 'Animals',
  poverty: 'Poverty Alleviation',
  children_youth: 'Children & Youth',
  housing_humanitarian: 'Housing & Community Humanitarian Aid',
  environment: 'Environment & Conservation',
}

const isConnected = ref(localStorage.getItem('cryptocare.wallet.connected') === '1')
function onWalletChange() {
  isConnected.value = localStorage.getItem('cryptocare.wallet.connected') === '1'
  if (!isConnected.value) {
    router.replace('/')
    return
  }
  fetchNonprofitByWallet()
}
onMounted(() => window.addEventListener('cryptocare:wallet-connection-changed', onWalletChange))
onUnmounted(() =>
  window.removeEventListener('cryptocare:wallet-connection-changed', onWalletChange),
)

const loadingDonations = ref(false)
const apiDonations = ref([])
const withdrawnDonations = ref(new Set())

const activeTab = ref('balances')
const detailTab = ref('details')
const searchQuery = ref('')
const filteredAccounts = computed(() => {
  const q = searchQuery.value.trim().toLowerCase()
  if (!q) return accounts.value
  return accounts.value.filter(
    (a) =>
      a.name?.toLowerCase().includes(q) ||
      a.email?.toLowerCase().includes(q) ||
      a.contact?.toLowerCase().includes(q) ||
      a.address?.toLowerCase().includes(q),
  )
})
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
  payouts: [], // [{ id, donorName, donorEmail, amountBch, cycleNumber, totalCycles, dueAt }]
  totalBch: '0',
  loading: false,
  onConfirm: null,
})

const fmtDialogDate = (d) =>
  d.toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' })
const fmtDialogDateShort = (d) => d.toLocaleDateString('en-US', { month: 'short', day: 'numeric' })
const fmtDialogTime = (d) => d.toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit' })

const accounts = ref([])

const selectedAccount = ref(null)

const fetchDonations = async () => {
  loadingDonations.value = true
  try {
    // Fetch all donations and group by charity into sidebar accounts
    // Min 600ms skeleton so it's always visible
    const [response] = await Promise.all([
      api.get('donations/'),
      new Promise((resolve) => setTimeout(resolve, 600)),
    ])

    if (Array.isArray(response.data)) {
      apiDonations.value = response.data
      console.log('Loaded donations:', apiDonations.value.length)
    } else if (response.data && Array.isArray(response.data.results)) {
      apiDonations.value = response.data.results
      console.log('Loaded donations (paginated):', apiDonations.value.length)
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
    explorerUrl: getExplorerUrlForDonation(donation),
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

  // Group sidebar accounts by donor identity (sender-side), not organization
  const groupedAccounts = {}

  const looksLikeBchAddress = (value) => /^(bitcoincash:)?[qp][a-z0-9]{41}$/i.test(value || '')

  apiDonations.value.forEach((donation) => {
    const nonprofitId = donation.nonprofit ?? null
    const donorEmail = donation.donor_email?.trim() || ''
    const donorName = donation.donor_name?.trim() || ''
    const donorContact = donation.donor_contact?.trim() || ''
    const donorAddress = looksLikeBchAddress(donorContact) ? donorContact : ''
    const groupKey = donorEmail
      ? `email:${donorEmail.toLowerCase()}`
      : donorName
        ? `name:${donorName.toLowerCase()}`
        : donorContact
          ? `contact:${donorContact.toLowerCase()}`
          : `anonymous:${donation.id}`

    if (!groupedAccounts[groupKey]) {
      groupedAccounts[groupKey] = {
        donations: [],
        total: 0,
        pending: 0,
        nonprofitId,
        name: donorName || 'Anonymous Donor',
        email: donorEmail,
        contact: donorContact,
        address: donorAddress,
      }
    }

    const amount = parseFloat(donation.amount)
    groupedAccounts[groupKey].donations.push(donation)
    groupedAccounts[groupKey].total += amount

    if (!withdrawnDonations.value.has(donation.id)) {
      groupedAccounts[groupKey].pending += amount
    }
  })

  const newAccounts = Object.entries(groupedAccounts).map(([groupKey, data]) => {
    const timestamps = data.donations
      .map((d) => d.timestamp)
      .filter(Boolean)
      .map((ts) => new Date(ts).getTime())
      .filter((ts) => Number.isFinite(ts))
      .sort((a, b) => a - b)

    const firstTs = timestamps[0]
    const lastTs = timestamps[timestamps.length - 1]

    return {
      id: groupKey,
      nonprofitId: data.nonprofitId,
      name: data.name,
      number: data.email || data.contact || '',
      address: data.address,
      current: data.total,
      available: data.pending,
      type: 'Paytaca',
      totalFees: 0,
      charityName: data.donations[0]?.cause || '',
      email: data.email,
      contact: data.contact,
      totalReceived: data.total,
      firstDonation: firstTs ? new Date(firstTs).toLocaleDateString() : 'N/A',
      lastDonation: lastTs ? new Date(lastTs).toLocaleDateString() : 'N/A',
      transactionCount: data.donations.length,
      donations: data.donations,
      cards: [],
    }
  })

  accounts.value = newAccounts
  if (newAccounts.length > 0) {
    const selectedId = selectedAccount.value?.id
    selectedAccount.value = newAccounts.find((a) => a.id === selectedId) || newAccounts[0]
  } else {
    selectedAccount.value = null
  }

  // Fetch payout info for each unique nonprofit
  const seenNonprofits = new Set()
  newAccounts.forEach((acct) => {
    if (acct.nonprofitId && !seenNonprofits.has(acct.nonprofitId)) {
      seenNonprofits.add(acct.nonprofitId)
      fetchPayoutsForNonprofit(acct.nonprofitId)
    }
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

    // Stamp duePayoutId + payout metadata on matching smart transaction rows
    due
      .filter((p) => p.payout_mode !== 'inbox_approval')
      .forEach((payout) => {
        const stamp = (list) => {
          const row = list.value.find((t) => payout.donation_id && t.id === payout.donation_id)
          if (row) {
            row.duePayoutId = payout.id
            row.vault_address = payout.vault_address
            row.recipientAddress = payout.recipient_address
            row.cycleNumber = payout.cycle_number
            row.totalCycles = payout.total_cycles
          }
        }
        stamp(transactions)
        stamp(allTransactions)
      })

    // Keep dashboard TXIDs aligned with payout backend records.
    const latestExecutedByDonation = {}
    executed.forEach((payout) => {
      if (!payout?.donation_id || !payout?.txid) return
      const current = latestExecutedByDonation[payout.donation_id]
      const currentTs = current?.executed_at ? new Date(current.executed_at).getTime() : 0
      const nextTs = payout.executed_at ? new Date(payout.executed_at).getTime() : 0
      if (!current || nextTs >= currentTs) {
        latestExecutedByDonation[payout.donation_id] = payout
      }
    })

    Object.entries(latestExecutedByDonation).forEach(([donationId, payout]) => {
      const txid = String(payout.txid || '')
        .trim()
        .toLowerCase()
      const explorerUrl = txid ? `${networkStore.explorerBaseUrl}/tx/${txid}` : ''
      const stamp = (list) => {
        const row = list.value.find((t) => String(t.id) === String(donationId))
        if (!row) return
        row.txid = txid
        row.explorerUrl = explorerUrl
        row.status = 'completed'
        row.withdrawn = true
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
  fetchNonprofitByWallet()
  const saved = localStorage.getItem('withdrawnDonations')
  if (saved) {
    withdrawnDonations.value = new Set(JSON.parse(saved))
  }
})

// Fetch payouts + details when selected account changes (donations already loaded globally)
watch(selectedAccount, (acct) => {
  if (acct?.nonprofitId) {
    fetchPayoutsForNonprofit(acct.nonprofitId)
    fetchNonprofitDetail(acct.nonprofitId)
  }
})

const transactionSearch = ref('')
const statusFilter = ref('All')
const typeFilter = ref('All')

// ── Dashboard Analytics Charts ────────────────────────────────────────────────
const dashChartTextColor = computed(() => ($q.dark.isActive ? 'rgba(255,255,255,0.65)' : '#546e7a'))
const dashChartGridColor = computed(() =>
  $q.dark.isActive ? 'rgba(255,255,255,0.07)' : 'rgba(0,0,0,0.07)',
)

// Line chart: BCH received over time for the selected donor
const dashLineChartData = computed(() => {
  const donorDonationIds = new Set((selectedAccount.value?.donations ?? []).map((d) => d.id))
  const sorted = [...allTransactions.value]
    .filter(
      (t) =>
        t.status === 'completed' && (donorDonationIds.size === 0 || donorDonationIds.has(t.id)),
    )
    .sort((a, b) => new Date(a.date) - new Date(b.date))
    .slice(-15)
  return {
    labels: sorted.map((t) => {
      const d = new Date(t.date)
      return isNaN(d) ? t.date : d.toLocaleDateString('en-US', { month: 'short', day: 'numeric' })
    }),
    datasets: [
      {
        label: 'BCH Received',
        data: sorted.map((t) => parseFloat(t.amount || 0)),
        borderColor: '#1976d2',
        backgroundColor: $q.dark.isActive ? 'rgba(25,118,210,0.18)' : 'rgba(25,118,210,0.1)',
        borderWidth: 2,
        pointBackgroundColor: '#1976d2',
        pointRadius: 4,
        fill: true,
        tension: 0.4,
      },
    ],
  }
})
const dashLineChartOptions = computed(() => ({
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: { display: false },
    tooltip: { callbacks: { label: (ctx) => ` ${ctx.parsed.y.toFixed(4)} BCH` } },
  },
  scales: {
    x: {
      grid: { color: dashChartGridColor.value },
      ticks: { color: dashChartTextColor.value, font: { size: 10 } },
    },
    y: {
      grid: { color: dashChartGridColor.value },
      ticks: { color: dashChartTextColor.value, font: { size: 10 }, callback: (v) => v + ' BCH' },
      beginAtZero: true,
    },
  },
}))

// Donut chart: BCH per individual donation send for the selected donor
const DASH_COLORS = [
  '#1976d2',
  '#7b1fa2',
  '#2e7d32',
  '#e65100',
  '#c62828',
  '#00838f',
  '#37474f',
  '#f57f17',
  '#00695c',
  '#4527a0',
]
const dashDonutChartData = computed(() => {
  const donorDonationIds = new Set((selectedAccount.value?.donations ?? []).map((d) => d.id))
  const sends = [...allTransactions.value]
    .filter((t) => donorDonationIds.size === 0 || donorDonationIds.has(t.id))
    .sort((a, b) => new Date(a.date) - new Date(b.date))
  return {
    labels: sends.map((t) => {
      const d = new Date(t.date)
      return isNaN(d)
        ? t.date
        : d.toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: '2-digit' })
    }),
    datasets: [
      {
        label: 'BCH Sent',
        data: sends.map((t) => parseFloat(parseFloat(t.amount || 0).toFixed(4))),
        backgroundColor: sends.map((_, i) => DASH_COLORS[i % DASH_COLORS.length] + 'cc'),
        borderColor: sends.map((_, i) => DASH_COLORS[i % DASH_COLORS.length]),
        borderWidth: 2,
        hoverOffset: 8,
      },
    ],
  }
})
const dashDonutTotal = computed(() => {
  const donorDonationIds = new Set((selectedAccount.value?.donations ?? []).map((d) => d.id))
  return allTransactions.value
    .filter((t) => donorDonationIds.size === 0 || donorDonationIds.has(t.id))
    .reduce((sum, t) => sum + parseFloat(t.amount || 0), 0)
    .toFixed(4)
})
const dashDonutChartOptions = computed(() => ({
  responsive: true,
  maintainAspectRatio: false,
  cutout: '65%',
  plugins: {
    legend: {
      display: true,
      position: 'bottom',
      labels: {
        color: dashChartTextColor.value,
        font: { size: 10 },
        boxWidth: 10,
        padding: 8,
      },
    },
    tooltip: {
      callbacks: {
        label: (ctx) =>
          ` ${ctx.parsed.toFixed(4)} BCH (${((ctx.parsed / parseFloat(dashDonutTotal.value)) * 100).toFixed(1)}%)`,
      },
    },
  },
}))
// ─────────────────────────────────────────────────────────────────────────────

// Columns for executed withdrawals history table
const executedColumns = [
  {
    name: 'executed_at',
    label: 'Date Executed',
    field: 'executed_at',
    align: 'left',
    sortable: true,
  },
  { name: 'donor_name', label: 'Donor', field: 'donor_name', align: 'left' },
  {
    name: 'amount',
    label: 'Amount',
    field: 'payout_amount_satoshis',
    align: 'right',
    sortable: true,
  },
  { name: 'cycle', label: 'Cycle', field: 'cycle_number', align: 'center' },
  { name: 'interval', label: 'Interval', field: 'interval_label', align: 'center' },
  { name: 'txid', label: 'Transaction ID', field: 'txid', align: 'left' },
  { name: 'payout_status', label: 'Status', field: 'status', align: 'center' },
]

// Pending schedule grouped by contract (donation_id)
// All cycles are now stored in the backend with their own due_at,
// so we just display each record directly — no projection needed.
const pendingScheduleGroups = computed(() => {
  if (!selectedAccount.value) return []
  const { pending } = getAccountSchedule(selectedAccount.value)
  const groups = {}
  const now = new Date()

  // Sort ascending by due_at so cycles are in order
  const sorted = [...pending].sort((a, b) => new Date(a.due_at) - new Date(b.due_at))

  sorted.forEach((p) => {
    const key = p.donation_id
    if (!groups[key]) {
      groups[key] = {
        donationId: key,
        donorName: p.donor_name || 'Anonymous',
        donorEmail: p.donor_email || '',
        intervalLabel: p.interval_label || '—',
        amountBch: (p.payout_amount_satoshis / 1e8).toFixed(8),
        totalCycles: p.total_cycles,
        cyclesRemaining: 0,
        hasDue: false,
        payoutId: p.id,
        payoutMode: p.payout_mode,
        cycles: [],
      }
    }
    const pg = groups[key]
    const dueAt = new Date(p.due_at)
    const isDue = dueAt <= now

    if (isDue) {
      pg.hasDue = true
      pg.payoutId = p.id // keep last due payout id for sidebar button
    }

    // status: due (past) → next (first future) → upcoming (second future) → scheduled (rest)
    const futureCycles = pg.cycles.filter((c) => c.status !== 'due').length
    let status = 'scheduled'
    if (isDue) status = 'due'
    else if (futureCycles === 0) status = 'next'
    else if (futureCycles === 1) status = 'upcoming'

    pg.cyclesRemaining = pg.cycles.filter((c) => c.status !== 'due').length + (isDue ? 0 : 1)

    pg.cycles.push({
      cycleNumber: p.cycle_number,
      dueAt,
      amountBch: (p.payout_amount_satoshis / 1e8).toFixed(8),
      status,
      payoutId: p.id,
    })
  })

  // Recalculate cyclesRemaining after all records are processed
  Object.values(groups).forEach((g) => {
    g.cyclesRemaining = g.cycles.filter((c) => c.status !== 'due').length
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
  {
    name: 'actions',
    label: 'Actions',
    field: 'actions',
    align: 'center',
    style: 'min-width: 120px',
  },
]

// Columns for the Organization Profile received donations table
const profileDonationColumns = [
  { name: 'timestamp', label: 'Date', field: 'timestamp', align: 'left', sortable: true },
  { name: 'donor_name', label: 'Donor', field: 'donor_name', align: 'left' },
  { name: 'amount', label: 'Amount', field: 'amount', align: 'right', sortable: true },
  { name: 'coin', label: 'Coin', field: 'coin', align: 'center' },
  { name: 'cause', label: 'Cause', field: 'cause', align: 'left' },
  { name: 'interval', label: 'Interval', field: 'interval', align: 'center' },
  { name: 'txid', label: 'TxID', field: 'txid', align: 'left' },
]

const transactions = ref([])

const pendingTransactions = ref([])

const allTransactions = ref([])

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

const normalizeTxid = (txid) => {
  const value = (txid || '').trim()
  return TXID_PATTERN.test(value) ? value.toLowerCase() : ''
}

const isValidTxid = (txid) => normalizeTxid(txid).length > 0

/**
 * Resolve the txid for an executed payout row.
 * Primary source: backend PayoutApproval.txid.
 * Fallback: localStorage vault withdrawalHistory matched by cycle_number.
 */
const resolvePayoutTxid = (row) => {
  const backendTxid = normalizeTxid(row.txid)
  if (backendTxid) return backendTxid
  try {
    const raw = localStorage.getItem('cryptocare.vaults')
    if (!raw) return ''
    const vaults = JSON.parse(raw)
    if (!Array.isArray(vaults)) return ''
    // Match by donation_ref or vault_address
    const vault = vaults.find(
      (v) =>
        (row.donation_ref && String(v.donationId) === String(row.donation_ref)) ||
        (row.vault_address && v.vaultAddress === row.vault_address),
    )
    if (!vault?.withdrawalHistory?.length) return ''
    const match = vault.withdrawalHistory.find((h) => h.cycleNumber === row.cycle_number)
    return normalizeTxid(match?.txid) || ''
  } catch {
    return ''
  }
}

const formatTxidPreview = (txid, visible = 18) => {
  const normalized = normalizeTxid(txid)
  return normalized ? `${normalized.substring(0, visible)}…` : 'Invalid TXID'
}

const copyTxid = (txid) => {
  const normalized = normalizeTxid(txid)
  if (!normalized) {
    $q.notify({ type: 'warning', message: 'Invalid TXID format', position: 'top', timeout: 1500 })
    return
  }
  $q.copyToClipboard(normalized).then(() => {
    $q.notify({ type: 'positive', message: 'TxID copied', position: 'top', timeout: 1500 })
  })
}

const getExplorerUrlForDonation = (donation) => {
  const normalized = normalizeTxid(donation?.txid)
  const provided = (donation?.explorer_url || '').trim()
  if (!normalized || !provided) return ''
  const expected = `${networkStore.explorerBaseUrl}/tx/${normalized}`
  return provided.toLowerCase() === expected.toLowerCase() ? expected : ''
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
      // Look up the full payout object from allPayoutsMap
      const nonprofitId = row.nonprofit
      const payoutsData = allPayoutsMap.value[nonprofitId]
      const payout = payoutsData?.pending?.find((p) => p.id === row.duePayoutId)

      let resultTxid = ''
      const vaultRecord =
        payout?.funder_address && payout?.recipient_address
          ? buildVaultRecordFromBackend({
              recipientAddress: payout.recipient_address,
              funderAddress: payout.funder_address,
              withdrawalSatoshis: payout.payout_amount_satoshis,
              intervalBlocks: payout.interval_blocks,
              vaultAddress: payout.vault_address,
            })
          : null

      if (vaultRecord) {
        const result = await executeWithdraw(vaultRecord)
        if (result.success) {
          resultTxid = result.txid
          await api.post('payouts/record/', {
            donation_id: payout.donation_id,
            cycle_number: payout.cycle_number,
            txid: resultTxid,
            recipient_address: payout.recipient_address,
            vault_address: payout.vault_address,
            payout_amount_satoshis: payout.payout_amount_satoshis,
            interval_blocks: payout.interval_blocks,
          })
        } else {
          throw new Error(`Withdrawal failed: ${result.reason || 'unknown error'}`)
        }
      } else {
        // Funder address unavailable — mark executed; auto-scheduler will fill txid
        await api.post(`payouts/${row.duePayoutId}/execute/`, {})
      }

      withdrawnDonations.value.add(row.id)
      localStorage.setItem('withdrawnDonations', JSON.stringify([...withdrawnDonations.value]))
      row.withdrawn = true
      row.status = 'completed'
      if (resultTxid) row.txid = resultTxid
      row.duePayoutId = null
      if (row.nonprofit) fetchPayoutsForNonprofit(row.nonprofit)
      $q.notify({
        type: 'positive',
        message: 'Withdrawal confirmed!',
        caption: resultTxid
          ? `BCH sent. TxID: ${resultTxid.substring(0, 14)}…`
          : 'Marked executed. TxID will appear once the auto-scheduler runs.',
        position: 'top',
        timeout: 5000,
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
          const row = allTransactions.value.find((t) => t.id === payout.donation_id)
          const vaultRecord =
            payout.funder_address && payout.recipient_address
              ? buildVaultRecordFromBackend({
                  recipientAddress: payout.recipient_address,
                  funderAddress: payout.funder_address,
                  withdrawalSatoshis: payout.payout_amount_satoshis,
                  intervalBlocks: payout.interval_blocks,
                  vaultAddress: payout.vault_address,
                })
              : null

          let resultTxid = ''
          if (vaultRecord) {
            const result = await executeWithdraw(vaultRecord)
            if (result.success) {
              resultTxid = result.txid
              await api.post('payouts/record/', {
                donation_id: payout.donation_id,
                cycle_number: payout.cycle_number,
                txid: resultTxid,
                recipient_address: payout.recipient_address,
                vault_address: payout.vault_address,
                payout_amount_satoshis: payout.payout_amount_satoshis,
                interval_blocks: payout.interval_blocks,
              })
            } else {
              failCount++
              continue
            }
          } else {
            await api.post(`payouts/${payout.id}/execute/`, {})
          }

          if (row) {
            row.withdrawn = true
            row.status = 'completed'
            if (resultTxid) row.txid = resultTxid
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
          caption: `Each cycle has its own unique transaction ID.`,
          position: 'top',
          timeout: 4000,
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
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  })
  const statusColor =
    transaction.status === 'completed'
      ? 'positive'
      : transaction.status === 'pending'
        ? 'warning'
        : 'negative'

  const rows = [
    { label: 'Donation Date', value: transactionDate },
    { label: 'Donor Name', value: transaction.donorName || 'Anonymous' },
    { label: 'Donor Email', value: transaction.donorEmail || 'N/A' },
    { label: 'Donor Contact', value: transaction.donorContact || 'N/A' },
    ...(transaction.contract && transaction.contract !== 'N/A'
      ? [
          {
            label: 'Contract',
            value: transaction.contract,
            style: 'color: #1976d2; font-weight: 600;',
          },
        ]
      : []),
    ...(transaction.interval && transaction.interval !== 'N/A'
      ? [
          {
            label: 'Interval',
            value: transaction.interval,
            style: 'color: #1976d2; font-weight: 600;',
          },
        ]
      : []),
    { label: 'Message', value: transaction.description || 'No message' },
    {
      label: 'Wallet Type',
      value: transaction.type?.toUpperCase(),
      style: 'color: #4caf50; font-weight: 600;',
    },
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
  background: linear-gradient(135deg, #f0f4ff 0%, #f7f4ff 50%, #f0f9ff 100%);
  background-attachment: fixed;
}

.body--dark .dashboard-page {
  background:
    radial-gradient(ellipse at 15% 30%, rgba(60, 90, 180, 0.35) 0%, transparent 55%),
    radial-gradient(ellipse at 85% 70%, rgba(100, 60, 180, 0.3) 0%, transparent 55%), #0f1117;
}

.sidebar-container {
  background: rgba(255, 255, 255, 0.55);
  backdrop-filter: blur(16px);
  -webkit-backdrop-filter: blur(16px);
  border-right: 1.5px solid rgba(21, 101, 192, 0.14);
  min-height: 100vh;
  padding: 0;
}

.body--dark .sidebar-container {
  background: rgba(20, 24, 40, 0.6);
  border-right: 1.5px solid rgba(93, 156, 245, 0.14);
}

.main-content {
  background: rgba(255, 255, 255, 0.6);
  backdrop-filter: blur(18px);
  -webkit-backdrop-filter: blur(18px);
  border-left: 1.5px solid rgba(21, 101, 192, 0.1);
}

.body--dark .main-content {
  background: rgba(18, 22, 38, 0.65);
  border-left: 1.5px solid rgba(93, 156, 245, 0.12);
}

.accounts-sidebar {
  border-radius: 0;
  padding: 0;
}

.sidebar-header {
  padding: 24px 20px 20px;
}

.sidebar-header-icon {
  width: 38px;
  height: 38px;
  border-radius: 10px;
  background: #1a237e;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}
.body--dark .sidebar-header-icon {
  background: rgba(93, 156, 245, 0.25);
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
  font-family: 'Space Grotesk', 'Inter', sans-serif;
  font-size: 20px;
  font-weight: 700;
  letter-spacing: -0.4px;
  line-height: 1.2;
  background: linear-gradient(125deg, #0d47a1 0%, #1976d2 55%, #1565c0 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.body--dark .sidebar-title {
  background: linear-gradient(125deg, #90caf9 0%, #e8eaf6 55%, #bbdefb 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
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

.sidebar-skeleton-card {
  background: rgba(255, 255, 255, 0.6);
  border-radius: 14px;
  padding: 14px;
  margin-bottom: 10px;
  border: 1.5px solid rgba(255, 255, 255, 0.5);
}
.body--dark .sidebar-skeleton-card {
  background: rgba(30, 36, 60, 0.5);
  border-color: rgba(255, 255, 255, 0.06);
}

.detail-skeleton-card {
  background: rgba(255, 255, 255, 0.75);
  border-radius: 14px;
  border: 1.5px solid rgba(21, 101, 192, 0.12);
  box-shadow: 0 2px 10px rgba(21, 101, 192, 0.07);
}
.body--dark .detail-skeleton-card {
  background: rgba(30, 36, 60, 0.7);
  border-color: rgba(255, 255, 255, 0.08);
}

.sidebar-account-card {
  background: rgba(255, 255, 255, 0.82);
  backdrop-filter: blur(8px);
  -webkit-backdrop-filter: blur(8px);
  border-radius: 14px;
  padding: 14px;
  margin-bottom: 10px;
  cursor: pointer;
  border: 1.5px solid #e2e8f0;
  box-shadow:
    0 1px 3px rgba(0, 0, 0, 0.07),
    0 3px 10px rgba(0, 0, 0, 0.06);
  transition: all 0.22s cubic-bezier(0.34, 1.56, 0.64, 1);
  position: relative;
  overflow: hidden;

  &:hover {
    border-color: #90caf9;
    box-shadow:
      0 2px 6px rgba(0, 0, 0, 0.08),
      0 8px 24px rgba(21, 101, 192, 0.18);
    transform: translateY(-2px);
  }

  &.sidebar-account-card--active {
    border-color: #1565c0;
    box-shadow:
      0 0 0 2px rgba(21, 101, 192, 0.18),
      0 4px 8px rgba(0, 0, 0, 0.08),
      0 10px 28px rgba(21, 101, 192, 0.22);

    .sidebar-card-accent {
      opacity: 1;
    }
  }
}

.sidebar-card-accent {
  position: absolute;
  left: 0;
  top: 0;
  bottom: 0;
  width: 3px;
  background: linear-gradient(180deg, #1565c0, #42a5f5);
  border-radius: 3px 0 0 3px;
  opacity: 0;
  transition: opacity 0.2s ease;
}
.body--dark .sidebar-account-card.sidebar-account-card--active .sidebar-card-accent {
  background: linear-gradient(180deg, #5d9cf5, #7ecbff);
}

.sidebar-card-divider {
  height: 1px;
  background: rgba(0, 0, 0, 0.07);
  margin: 8px 0 6px;
  border-radius: 1px;
}
.body--dark .sidebar-card-divider {
  background: rgba(255, 255, 255, 0.07);
}

.sidebar-address-pill {
  display: inline-flex;
  align-items: center;
  background: rgba(21, 101, 192, 0.07);
  border: 1px solid rgba(21, 101, 192, 0.15);
  border-radius: 20px;
  padding: 2px 8px;
  font-size: 10px;
  color: #546e7a;
  cursor: pointer;
  max-width: 100%;
  transition: background 0.15s;

  &:hover {
    background: rgba(21, 101, 192, 0.13);
    .sidebar-address-copy-icon {
      opacity: 1;
    }
  }
}
.body--dark .sidebar-address-pill {
  background: rgba(93, 156, 245, 0.1);
  border-color: rgba(93, 156, 245, 0.2);
  color: #7a96b8;

  &:hover {
    background: rgba(93, 156, 245, 0.18);
  }
}

.sidebar-address-pill-label {
  font-weight: 700;
  color: #1565c0;
  margin-right: 3px;
  flex-shrink: 0;
}
.body--dark .sidebar-address-pill-label {
  color: #5d9cf5;
}

.sidebar-address-copy-icon {
  opacity: 0.4;
  transition: opacity 0.15s;
  flex-shrink: 0;
}

.body--dark .sidebar-account-card {
  background: rgba(30, 36, 60, 0.75);
  border-color: rgba(255, 255, 255, 0.1);
  box-shadow:
    0 1px 3px rgba(0, 0, 0, 0.25),
    0 4px 14px rgba(0, 0, 0, 0.22);

  &:hover {
    border-color: #5c8ee0;
    box-shadow:
      0 2px 6px rgba(0, 0, 0, 0.3),
      0 8px 24px rgba(92, 142, 224, 0.22);
  }

  &.sidebar-account-card--active {
    border-color: #5c8ee0;
    box-shadow:
      0 0 0 2px rgba(92, 142, 224, 0.22),
      0 4px 8px rgba(0, 0, 0, 0.3),
      0 10px 28px rgba(92, 142, 224, 0.28);

    .sidebar-card-accent {
      opacity: 1;
    }
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
.body--dark .sidebar-avatar {
  background: rgba(93, 156, 245, 0.15);
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
.body--dark .sidebar-account-sub {
  color: #5a7a9e;
}

.sidebar-card-sep {
  opacity: 0.15;
}
.body--dark .sidebar-card-sep {
  opacity: 0.08;
}

.sidebar-stat-block {
  flex: 1;
  min-width: 0;
  border-radius: 8px;
  padding: 8px 10px;
  overflow: hidden;
}
.sidebar-stat-block--neutral {
  background: #f5f7fa;
}
.sidebar-stat-block--positive {
  background: #f0faf2;
}
.body--dark .sidebar-stat-block--neutral {
  background: rgba(255, 255, 255, 0.05);
}
.body--dark .sidebar-stat-block--positive {
  background: rgba(46, 125, 50, 0.12);
}

.sidebar-stat-label {
  font-size: 10px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  color: #90a4ae;
  margin-bottom: 2px;
}
.body--dark .sidebar-stat-label {
  color: #5a7a9e;
}

.sidebar-stat-value {
  font-size: 14px;
  font-weight: 800;
  color: #263238;
  line-height: 1;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
.sidebar-stat-value--positive {
  color: #2e7d32;
}
.body--dark .sidebar-stat-value {
  color: #eceff1;
}
.body--dark .sidebar-stat-value--positive {
  color: #4caf50 !important;
}

.sidebar-next-text {
  font-size: 11.5px;
  color: #546e7a;
  font-weight: 600;
}
.body--dark .sidebar-next-text {
  color: #7a96b8;
}

.sidebar-no-pending-text {
  font-size: 11px;
  color: #90a4ae;
}
.body--dark .sidebar-no-pending-text {
  color: #3d5470;
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

.dash-donut-center {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -62%);
  text-align: center;
  pointer-events: none;
}
.dash-donut-total {
  font-size: 16px;
  font-weight: 800;
  color: #1a237e;
  line-height: 1.1;
}
.dash-donut-label {
  font-size: 10px;
  font-weight: 700;
  color: #90a4ae;
  letter-spacing: 0.5px;
  text-transform: uppercase;
}
.body--dark .dash-donut-total {
  color: #c5cae9;
}
.body--dark .dash-donut-label {
  color: #5a7a9e;
}
/* ──────────────────────────────────────────────────────────────────── */

.detail-info-card {
  border: 1.5px solid #90caf9 !important;
  background: rgba(255, 255, 255, 0.72);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  transition:
    border-color 0.2s ease,
    box-shadow 0.2s ease;

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

/* Dashboard Details Tab Dark Mode */
.body--dark .profile-left-col {
  border-right-color: #2e3f6e !important;
}
.body--dark .org-name-text {
  color: #d8e8ff !important;
}
.body--dark .org-category-text {
  color: #5d9cf5 !important;
}
.body--dark .org-status-text {
  color: #7a96b8 !important;
}
.stat-value-text {
  color: #212121;
}
.body--dark .stat-value-text {
  color: #c8d8f0 !important;
}
.body--dark .info-card-title {
  color: #c8d8f0 !important;
}
.body--dark .field-value-text {
  color: #c8d8f0 !important;
}
.body--dark .bch-address-box {
  color: #7ecbff !important;
  background: rgba(30, 58, 110, 0.7) !important;
}
.body--dark .total-received-value {
  color: #5d9cf5 !important;
}
.body--dark .available-balance-value {
  color: #4caf50 !important;
}
.body--dark .bch-unit-label {
  color: #7a96b8 !important;
}
.body--dark .description-box {
  color: #8fa8cb !important;
  background: rgba(26, 34, 64, 0.6) !important;
  border-color: #2e3f6e !important;
}
.body--dark .detail-info-card .text-grey-5 {
  color: #5a7a9e !important;
}

/* Pending Tab Dark Mode */
.pending-empty-state {
  border: 2px dashed #e0e0e0;
  border-radius: 12px;
}
.body--dark .pending-empty-state {
  border-color: #2e3f6e;
}
.body--dark .pending-empty-state .text-grey-6,
.body--dark .pending-empty-state .text-grey-4 {
  color: #5a7a9e !important;
}

.body--dark .contract-donor-name {
  color: #d8e8ff !important;
}
.body--dark .contract-meta-caption {
  color: #7a96b8 !important;
}

.cycle-table-wrapper {
  border: 1px solid #e3e8ef;
  border-radius: 10px;
  overflow: hidden;
}
.body--dark .cycle-table-wrapper {
  border-color: #2e3f6e;
}

.cycle-table-header {
  background: #f7f9fc;
  padding: 8px 18px;
  border-bottom: 1px solid #e3e8ef;
}
.body--dark .cycle-table-header {
  background: #111d3a;
  border-bottom-color: #2e3f6e;
}

.cycle-col-label {
  font-size: 10.5px;
  font-weight: 700;
  color: #90a4ae;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}
.body--dark .cycle-col-label {
  color: #5a7a9e;
}

.cycle-date-text {
  color: #263238;
}
.body--dark .cycle-date-text {
  color: #c8d8f0 !important;
}
.cycle-time-text {
  color: #9e9e9e;
}
.body--dark .cycle-time-text {
  color: #5a7a9e !important;
}
.cycle-amount-text {
  color: #1565c0;
}
.body--dark .cycle-amount-text {
  color: #5d9cf5 !important;
}
.cycle-bch-label {
  color: #90a4ae;
}
.body--dark .cycle-bch-label {
  color: #5a7a9e !important;
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
  color: #1565c0;
  transition: color 0.3s ease;

  &:hover {
    color: #2196f3 !important;
  }
}
.body--dark .view-all-link {
  color: #5d9cf5;
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
  width: 540px;
  max-width: 95vw;
  border-radius: 16px !important;
  overflow: hidden;
  border: 1.5px solid rgba(144, 202, 249, 0.5);
  background: rgba(255, 255, 255, 0.92);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
}

@media (max-width: 599px) {
  .tx-detail-dialog {
    width: 100%;
    max-width: 100%;
    border-radius: 16px 16px 0 0 !important;
  }

  .tx-detail-content {
    max-height: calc(85vh - 180px);
    overflow-y: auto;
  }

  .tx-detail-header {
    padding: 16px 16px 13px;
  }

  .tx-detail-title {
    font-size: 16px;
  }

  .tx-detail-row {
    flex-direction: column;
    gap: 3px;
    padding: 10px 12px;
  }

  .tx-detail-label {
    min-width: 0;
    font-size: 11px;
  }

  .tx-detail-value {
    font-size: 12.5px;
    text-align: left;
  }

  .tx-detail-explorer-btn {
    width: 100%;
  }

  .tx-detail-actions {
    padding-top: 10px;
  }

  .tx-detail-actions .q-btn {
    width: 100%;
    min-height: 40px;
  }
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

/* ─── Withdraw Confirm Dialog ───────────────────────────────────────── */
.withdraw-confirm-card {
  min-width: 480px;
  max-width: 560px;
  width: 100%;
  border-radius: 16px;
  overflow: hidden;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.18);
}

@media (max-width: 599px) {
  .withdraw-confirm-card {
    min-width: unset !important;
    max-width: 100vw !important;
    width: 100vw !important;
    border-radius: 16px 16px 0 0 !important;
  }
}

.body--dark .withdraw-confirm-card {
  background: #0f1629;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.55);
}

/* ─── Primary Withdraw Dialog ──────────────────────────────────────── */
.withdraw-dialog-card {
  width: 100%;
}

@media (max-width: 599px) {
  .withdraw-dialog-card {
    min-width: unset !important;
    max-width: 100vw !important;
    width: 100vw !important;
    border-radius: 16px 16px 0 0 !important;
  }

  .withdraw-dialog-content {
    max-height: calc(86vh - 150px);
    overflow-y: auto;
    padding-bottom: 10px;
  }

  .withdraw-dialog-actions .q-btn {
    width: 100%;
    min-height: 42px;
  }
}

/* Header icon circle */
.wcd-header-icon-circle {
  width: 44px;
  height: 44px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.18);
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 14px;
  flex-shrink: 0;
}

/* Stat boxes */
.wcd-stat-box {
  border-radius: 10px;
  padding: 14px 12px;
  border: 1px solid;
  text-align: center;
}

.wcd-stat-box--blue {
  background: #e8f0fe;
  border-color: #c5d8ff;
}
.wcd-stat-box--green {
  background: #e6f4ea;
  border-color: #b7dcc3;
}
.wcd-stat-box--orange {
  background: #fef3e8;
  border-color: #f5d4ae;
}

.body--dark .wcd-stat-box--blue {
  background: rgba(26, 86, 219, 0.15);
  border-color: #1e3a6e;
}
.body--dark .wcd-stat-box--green {
  background: rgba(30, 107, 58, 0.18);
  border-color: #1a3d28;
}
.body--dark .wcd-stat-box--orange {
  background: rgba(196, 94, 10, 0.15);
  border-color: #3d2510;
}

/* Stat labels */
.wcd-stat-label {
  font-size: 11px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.6px;
  margin-top: 4px;
}
.wcd-stat-label--blue {
  color: #1a56db;
}
.wcd-stat-label--green {
  color: #1e6b3a;
}
.wcd-stat-label--orange {
  color: #c45e0a;
}

.body--dark .wcd-stat-label--blue {
  color: #7ecbff;
}
.body--dark .wcd-stat-label--green {
  color: #81c995;
}
.body--dark .wcd-stat-label--orange {
  color: #ffb74d;
}

/* Stat values */
.wcd-stat-value {
  font-size: 17px;
  font-weight: 800;
  margin-top: 2px;
  line-height: 1;
}
.wcd-stat-value--blue {
  color: #1a56db;
}
.wcd-stat-value--green {
  color: #1e6b3a;
}
.wcd-stat-value--orange {
  font-size: 12px;
  font-weight: 800;
  color: #c45e0a;
  line-height: 1.2;
}

.body--dark .wcd-stat-value--blue {
  color: #7ecbff;
}
.body--dark .wcd-stat-value--green {
  color: #81c995;
}
.body--dark .wcd-stat-value--orange {
  color: #ffb74d;
}

/* Stat units */
.wcd-stat-unit {
  font-size: 11px;
  margin-top: 1px;
}
.wcd-stat-unit--blue {
  color: #6b8cc7;
}
.wcd-stat-unit--green {
  color: #5a9970;
}
.wcd-stat-unit--orange {
  color: #c07940;
}

.body--dark .wcd-stat-unit--blue {
  color: #5a7a9e;
}
.body--dark .wcd-stat-unit--green {
  color: #4a7a5e;
}
.body--dark .wcd-stat-unit--orange {
  color: #8a6240;
}

/* Table heading label */
.wcd-table-heading {
  font-size: 11px;
  font-weight: 700;
  color: #78909c;
  text-transform: uppercase;
  letter-spacing: 0.7px;
  margin-bottom: 8px;
}
.body--dark .wcd-table-heading {
  color: #5a7a9e;
}

/* Table wrapper */
.wcd-table-wrapper {
  border: 1px solid #e3e8ef;
  border-radius: 10px;
  overflow: hidden;
}
.body--dark .wcd-table-wrapper {
  border-color: #2e3f6e;
}

/* Table header row */
.wcd-table-header {
  background: #f5f7fa;
  padding: 8px 14px;
  border-bottom: 1px solid #e3e8ef;
}
.body--dark .wcd-table-header {
  background: #111d3a;
  border-bottom-color: #2e3f6e;
}

/* Column labels */
.wcd-col-label {
  font-size: 10.5px;
  font-weight: 700;
  color: #90a4ae;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}
.body--dark .wcd-col-label {
  color: #5a7a9e;
}

/* Table rows */
.wcd-table-row {
  padding: 10px 14px;
}

/* Mobile payout card row */
.wcd-mobile-row {
  padding: 12px 14px;
}

/* Donor name / email */
.wcd-donor-name {
  font-size: 13px;
  font-weight: 600;
  color: #1a237e;
}
.wcd-donor-email {
  font-size: 11px;
  color: #9e9e9e;
}
.body--dark .wcd-donor-name {
  color: #c8d8f0;
}
.body--dark .wcd-donor-email {
  color: #5a7a9e;
}

/* Payout amount */
.wcd-payout-amount {
  font-size: 13px;
  font-weight: 700;
  color: #1565c0;
}
.wcd-payout-bch {
  font-size: 10px;
  color: #90a4ae;
}
.body--dark .wcd-payout-amount {
  color: #7ecbff;
}
.body--dark .wcd-payout-bch {
  color: #5a7a9e;
}

/* Due date / time */
.wcd-due-date {
  font-size: 11px;
  font-weight: 600;
  color: #e65100;
}
.wcd-due-time {
  font-size: 10px;
  color: #9e9e9e;
}
.body--dark .wcd-due-date {
  color: #ffb74d;
}
.body--dark .wcd-due-time {
  color: #5a7a9e;
}

/* Notice boxes */
.wcd-notice {
  border-left: 4px solid;
  border-radius: 6px;
  padding: 10px 14px;
  display: flex;
  align-items: flex-start;
  gap: 8px;
}
.wcd-notice--approval {
  background: #fff8e1;
  border-color: #ffc107;
}
.wcd-notice--smart {
  background: #e8f5e9;
  border-color: #43a047;
}

.body--dark .wcd-notice--approval {
  background: rgba(255, 193, 7, 0.1);
  border-color: #b8860b;
}
.body--dark .wcd-notice--smart {
  background: rgba(67, 160, 71, 0.1);
  border-color: #2e7d32;
}

.wcd-notice-text {
  font-size: 12px;
  line-height: 1.5;
}
.wcd-notice-text--approval {
  color: #6d4c00;
}
.wcd-notice-text--smart {
  color: #1b5e20;
}

.body--dark .wcd-notice-text--approval {
  color: #ffe082;
}
.body--dark .wcd-notice-text--smart {
  color: #a5d6a7;
}

/* ── Dashboard mobile cards (All Donations + Transaction Status) ── */
.transactions-table {
  :deep(.q-table__grid-content) {
    gap: 10px;
    padding: 4px 0;
  }
}

.dash-mobile-card {
  width: 100%;
  border-radius: 14px;
  border: 1.5px solid rgba(21, 101, 192, 0.16);
  background: rgba(255, 255, 255, 0.88);
  overflow: hidden;
  margin-bottom: 2px;
  box-shadow: 0 1px 4px rgba(21, 101, 192, 0.08);
}

.dash-mobile-card__header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 11px 14px 8px;
  border-bottom: 1.5px solid rgba(21, 101, 192, 0.1);
  gap: 8px;
}

.dash-mobile-card__title {
  font-size: 14px;
  font-weight: 700;
  color: #1565c0;
  flex: 1;
  min-width: 0;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.dash-mobile-card__body {
  padding: 8px 14px 6px;
  display: flex;
  flex-direction: column;
  gap: 5px;
}

.dash-mobile-card__row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 8px;
  font-size: 13px;
}

.dash-mobile-card__label {
  color: #78909c;
  font-weight: 500;
  flex-shrink: 0;
  min-width: 64px;
}

.dash-mobile-card__value {
  color: rgba(0, 0, 0, 0.82);
  font-weight: 500;
  text-align: right;
}

.dash-mobile-card__desc {
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  max-width: 160px;
}

.dash-mobile-card__txid {
  font-family: monospace;
  font-size: 12px;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 3px;
}

.dash-mobile-card__footer {
  display: flex;
  align-items: center;
  justify-content: flex-end;
  gap: 2px;
  padding: 4px 8px 6px;
  border-top: 1.5px solid rgba(21, 101, 192, 0.08);
}

/* Dark mode */
.body--dark .dash-mobile-card {
  background: rgba(18, 26, 52, 0.82);
  border-color: rgba(93, 156, 245, 0.22);
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.25);
}
.body--dark .dash-mobile-card__header {
  border-bottom-color: rgba(93, 156, 245, 0.14);
}
.body--dark .dash-mobile-card__title {
  color: #90caf9;
}
.body--dark .dash-mobile-card__label {
  color: rgba(255, 255, 255, 0.45);
}
.body--dark .dash-mobile-card__value {
  color: rgba(255, 255, 255, 0.85);
}
.body--dark .dash-mobile-card__footer {
  border-top-color: rgba(93, 156, 245, 0.1);
}

/* ── Pending cycles — mobile card ─────────────────────────────── */
.cycle-mobile-card {
  padding: 10px 14px;
  border-bottom: 1px solid #f0f4f8;
  background: #ffffff;
  transition: background 0.2s;
}
.cycle-mobile-card:last-child {
  border-bottom: none;
}
.cycle-mobile-card--due {
  background: #fffde7;
}

.cycle-mobile-card__top {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 8px;
  margin-bottom: 8px;
}

.cycle-mobile-card__info {
  display: flex;
  flex-direction: column;
  gap: 5px;
}

.cycle-mobile-card__row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  font-size: 13px;
  gap: 8px;
}

.cycle-mobile-card__label {
  font-size: 10.5px;
  font-weight: 700;
  color: #90a4ae;
  text-transform: uppercase;
  letter-spacing: 0.4px;
  flex-shrink: 0;
}

.cycle-mobile-card__value {
  font-weight: 500;
  text-align: right;
}

/* Dark mode cycle mobile cards */
.body--dark .cycle-mobile-card {
  background: #0f1629;
  border-bottom-color: #1e2d50;
}
.body--dark .cycle-mobile-card--due {
  background: #1f1a00;
}
.body--dark .cycle-mobile-card__label {
  color: #5a7a9e;
}

/* ── Profile Header Card: Mobile Responsive ──────────────────────── */
@media (max-width: 599px) {
  .profile-header-row {
    flex-direction: column !important;
  }
  .profile-left-col {
    flex: none !important;
    min-width: 0 !important;
    width: 100% !important;
    border-right: none !important;
    border-bottom: 1px solid #f0f0f0;
    padding: 16px !important;
  }
  .body--dark .profile-left-col {
    border-bottom: 1px solid #2e3f6e !important;
    border-right: none !important;
  }
  .profile-stats-col {
    width: 100% !important;
    padding: 12px 16px 16px !important;
  }
  .profile-stats-col > div {
    min-width: 100% !important;
    padding-right: 0 !important;
  }
}
</style>

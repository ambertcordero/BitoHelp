<template>
  <q-page class="donor-page">
    <div class="row" style="min-height: 100vh;">
      <div class="col-12 col-md-4 col-lg-3 q-pa-md sidebar-container">
        <div class="accounts-sidebar">
          <h5 class="q-mt-none q-mb-md">Donor<br><strong>Dashboard</strong></h5>
          
        
          <div class="q-mb-md">
            <div class="sidebar-toggle">
              <div
                class="sidebar-toggle__btn"
                :class="{ active: activeTab === 'donations' }"
                @click="activeTab = 'donations'"
              >
                <q-icon name="volunteer_activism" size="14px" class="q-mr-xs" />
                Donations
              </div>
              <div
                class="sidebar-toggle__btn"
                :class="{ active: activeTab === 'activity' }"
                @click="activeTab = 'activity'"
              >
                <q-icon name="bar_chart" size="14px" class="q-mr-xs" />
                Activity
              </div>
            </div>
          </div>

          <q-input
            v-model="searchQuery"
            outlined
            dense
            placeholder="Search"
            class="sidebar-search q-mb-md"
          >
            <template v-slot:prepend>
              <q-icon name="search" />
            </template>
            <template v-slot:append>
              <q-btn flat dense icon="tune" size="sm" />
            </template>
          </q-input>

          
          <!-- Sidebar skeleton while loading -->
          <div v-if="loadingDonations" class="q-px-sm q-pb-sm">
            <div v-for="n in 3" :key="n" class="sidebar-account-card" style="pointer-events: none;">
              <div class="row items-center no-wrap q-mb-sm" style="gap: 10px;">
                <q-skeleton type="QAvatar" size="32px" />
                <div style="flex: 1;">
                  <q-skeleton type="text" width="60%" style="margin-bottom: 4px;" />
                  <q-skeleton type="text" width="40%" />
                </div>
              </div>
              <q-skeleton type="text" width="85%" style="margin-bottom: 10px; border-radius: 20px;" />
              <div class="sidebar-card-divider" />
              <div class="row q-mt-xs" style="gap: 8px;">
                <q-skeleton style="flex: 1; height: 38px; border-radius: 8px;" />
                <q-skeleton style="flex: 1; height: 38px; border-radius: 8px;" />
              </div>
            </div>
          </div>

          <div v-else class="q-px-sm q-pb-sm">
            <div
              v-for="wallet in filteredWallets"
              :key="wallet.id"
              class="sidebar-account-card"
              :class="{ 'sidebar-account-card--active': selectedWallet?.id === wallet.id }"
              @click="selectWallet(wallet)"
            >
              <!-- Active accent bar -->
              <div class="sidebar-card-accent" />

              <!-- Top row: avatar + name + address -->
              <div class="row items-start no-wrap q-mb-xs">
                <div class="sidebar-avatar">
                  <img src="~assets/paytaca.png" alt="wallet" style="width: 24px; height: 24px; object-fit: contain;" />
                </div>
                <div style="flex: 1; min-width: 0; margin-left: 10px;">
                  <div class="sidebar-account-name ellipsis">{{ wallet.name }}</div>
                  <div class="sidebar-account-sub">{{ wallet.type || 'Paytaca' }}</div>
                </div>
                <q-btn flat round dense icon="more_vert" size="xs" class="sidebar-menu-btn" @click.stop />
              </div>

              <!-- Address copy pill -->
              <div class="q-mt-xs">
                <div
                  class="sidebar-address-pill ellipsis"
                  @click.stop="$q.copyToClipboard(wallet.address).then(() => $q.notify({ type: 'positive', message: 'Donor address copied', position: 'top', timeout: 1500 }))"
                >
                  <q-icon name="person" size="10px" class="q-mr-xs" style="flex-shrink:0;" />
                  <span class="sidebar-address-pill-label">Donor:</span>
                  <span class="q-ml-xs">{{ wallet.address }}</span>
                  <q-icon name="content_copy" size="10px" class="q-ml-xs sidebar-address-copy-icon" style="flex-shrink:0;" />
                </div>
              </div>

              <!-- Divider -->
              <div class="sidebar-card-divider" />

              <!-- BCH stat blocks -->
              <div class="row q-mt-xs" style="gap: 8px;">
                <div class="sidebar-stat-block sidebar-stat-block--blue">
                  <div class="row items-center no-wrap" style="gap: 4px; margin-bottom: 2px;">
                    <q-icon name="currency_bitcoin" size="11px" color="blue-7" />
                    <div class="sidebar-stat-label">Total Donated</div>
                  </div>
                  <div class="sidebar-stat-value">{{ formatCurrency(wallet.totalDonated) }} BCH</div>
                </div>
                <div class="sidebar-stat-block sidebar-stat-block--green">
                  <div class="row items-center no-wrap" style="gap: 4px; margin-bottom: 2px;">
                    <q-icon name="volunteer_activism" size="11px" color="green-7" />
                    <div class="sidebar-stat-label">Donations</div>
                  </div>
                  <div class="sidebar-stat-value sidebar-stat-value--green">{{ wallet.donationCount }}</div>
                </div>
              </div>
            </div>
          </div>

          <div class="text-center q-mt-md">
            <a href="#" class="view-all-link text-blue-7 text-weight-medium" style="text-decoration: none;">View all</a>
          </div>

         
          <div v-if="activeTab === 'donations'" class="q-mt-md">
            <q-btn
              unelevated
              label="Make Donation"
              icon="volunteer_activism"
              no-caps
              class="full-width make-donation-btn"
              @click="$router.push('/donate')"
            />
          </div>
        </div>
      </div>

      <div class="col-12 col-md-8 col-lg-9 q-pa-md q-pa-lg-lg main-content">

        <!-- Main content skeleton while loading -->
        <div v-if="loadingDonations">
          <!-- Header skeleton -->
          <div class="row items-center justify-between q-mb-lg">
            <q-skeleton type="text" width="180px" style="height: 28px;" />
            <div class="row q-gutter-sm">
              <q-skeleton type="QBtn" width="36px" height="36px" style="border-radius: 50%;" />
              <q-skeleton type="QBtn" width="80px" height="36px" style="border-radius: 8px;" />
            </div>
          </div>
          <!-- Tabs skeleton -->
          <div class="row q-gutter-md q-mb-md">
            <q-skeleton v-for="t in 4" :key="t" type="text" width="100px" style="height: 20px;" />
          </div>
          <q-separator class="q-mb-lg" />
          <!-- Stat cards -->
          <div class="row q-col-gutter-md q-mb-lg">
            <div v-for="s in 4" :key="s" class="col-6 col-md-3">
              <q-skeleton style="height: 80px; border-radius: 12px;" />
            </div>
          </div>
          <!-- Table skeleton -->
          <q-skeleton style="height: 320px; border-radius: 12px;" />
        </div>

        <div v-if="activeTab === 'donations' && selectedWallet && !loadingDonations" class="wallet-details">
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
            class="text-grey-6 donor-detail-tabs"
            active-color="blue-5"
            indicator-color="blue-5"
            align="left"
            mobile-arrows
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
                :grid="$q.screen.lt.md"
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

                <!-- Mobile card layout (grid mode) -->
                <template v-slot:item="props">
                  <div class="donation-mobile-card">
                    <div class="donation-mobile-card__header">
                      <div class="donation-mobile-card__recipient">{{ props.row.recipient }}</div>
                      <q-badge color="primary" :label="props.row.coin || 'BCH'" class="q-ml-xs" />
                    </div>

                    <div class="donation-mobile-card__body">
                      <div class="donation-mobile-card__row">
                        <span class="donation-mobile-card__label">Date</span>
                        <span class="donation-mobile-card__value">{{ formatDate(props.row.timestamp) }}</span>
                      </div>
                      <div class="donation-mobile-card__row">
                        <span class="donation-mobile-card__label">Donor</span>
                        <span class="donation-mobile-card__value">{{ props.row.donor_name }}</span>
                      </div>
                      <div class="donation-mobile-card__row">
                        <span class="donation-mobile-card__label">Amount</span>
                        <span class="donation-mobile-card__value text-weight-bold text-positive">{{ formatCurrency(props.row.amount) }}</span>
                      </div>
                      <div class="donation-mobile-card__row">
                        <span class="donation-mobile-card__label">Interval</span>
                        <span class="donation-mobile-card__value">
                          <q-badge v-if="props.row.interval" color="blue-7" :label="props.row.interval" />
                          <span v-else class="text-grey-6">One-time</span>
                        </span>
                      </div>
                    </div>

                    <div class="donation-mobile-card__footer">
                      <q-btn
                        flat dense no-caps
                        icon="receipt_long" label="Details"
                        size="sm" color="primary"
                        @click="viewDonationDetails(props.row)"
                      />
                      <q-btn
                        flat dense no-caps
                        icon="picture_as_pdf" label="Receipt"
                        size="sm" color="blue-grey"
                        @click="viewReceipt(props.row)"
                      />
                      <q-btn
                        flat dense no-caps
                        icon="download" label="Download"
                        size="sm" color="blue-grey"
                        @click="downloadReceipt(props.row)"
                      />
                    </div>
                  </div>
                </template>
              </q-table>
            </q-tab-panel>

          
            <q-tab-panel name="details" class="details-panel q-pa-none">

              <!-- ── Two column cards ──────────────────────────────────── -->
              <div class="row q-col-gutter-md">

                <!-- Wallet Information -->
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
                          <div class="detail-field-label">Account Name</div>
                          <div class="detail-field-value">{{ selectedWallet.accountName }}</div>
                        </div>

                        <div class="col-6">
                          <div class="detail-field-label">Wallet Type</div>
                          <div class="detail-field-value">{{ selectedWallet.product }}</div>
                        </div>

                        <div class="col-12">
                          <div class="detail-field-label">Contract Address</div>
                          <div
                            class="detail-address-field"
                            @click="$q.copyToClipboard(selectedWallet.fullNumber).then(() => $q.notify({ type: 'positive', message: 'Address copied', position: 'top', timeout: 1500 }))"
                          >
                            {{ selectedWallet.fullNumber }}
                            <q-icon name="content_copy" size="13px" class="q-ml-xs text-blue-8" />
                          </div>
                        </div>

                        <div class="col-12">
                          <div class="detail-field-label">Donor Address</div>
                          <div
                            class="detail-address-field"
                            @click="$q.copyToClipboard(selectedWallet.iban).then(() => $q.notify({ type: 'positive', message: 'Address copied', position: 'top', timeout: 1500 }))"
                          >
                            {{ selectedWallet.iban }}
                            <q-icon name="content_copy" size="13px" class="q-ml-xs text-blue-8" />
                          </div>
                        </div>

                      </div>
                    </q-card-section>
                  </q-card>
                </div>

                <!-- Donation Overview -->
                <div class="col-12 col-md-6">
                  <q-card flat class="detail-info-card" style="border-radius: 14px; height: 100%;">
                    <q-card-section class="q-pb-xs">
                      <div class="row items-center justify-between">
                        <div style="font-size: 14px; font-weight: 700; color: #37474f;">Donation Overview</div>
                        <q-icon name="bar_chart" color="purple-4" size="20px" />
                      </div>
                    </q-card-section>
                    <q-separator />
                    <q-card-section class="q-pt-md">
                      <div class="row q-col-gutter-md">

                        <div class="col-6">
                          <div class="detail-field-label">Donor Name</div>
                          <div class="detail-field-value">{{ selectedWallet.branch }}</div>
                        </div>

                        <div class="col-6">
                          <div class="detail-field-label">Contract Code</div>
                          <div class="detail-field-value">{{ selectedWallet.swift }}</div>
                        </div>

                        <div class="col-6">
                          <div class="detail-field-label">Amount Balance</div>
                          <div style="font-size: 18px; font-weight: 800; color: #1565c0;">
                            {{ selectedWallet.debitRate }}
                            <span style="font-size: 12px; font-weight: 600; color: #90a4ae;">BCH</span>
                          </div>
                        </div>

                        <div class="col-6">
                          <div class="detail-field-label">Total Contract</div>
                          <div style="font-size: 18px; font-weight: 800; color: #2e7d32;">
                            {{ selectedWallet.overdraftLimit }}
                            <span style="font-size: 12px; font-weight: 600; color: #90a4ae;">BCH</span>
                          </div>
                        </div>

                        <div class="col-6">
                          <div class="detail-field-label">Network Fee</div>
                          <div class="detail-field-value">{{ selectedWallet.creditRate }}</div>
                        </div>

                        <div class="col-6">
                          <div class="detail-field-label">Total Donations</div>
                          <div class="detail-field-value">{{ selectedWallet.donationCount }}</div>
                        </div>

                        <div class="col-6">
                          <div class="detail-field-label">First Donation</div>
                          <div class="detail-field-value">{{ selectedWallet.firstDonation || '—' }}</div>
                        </div>

                        <div class="col-6">
                          <div class="detail-field-label">Last Donation</div>
                          <div class="detail-field-value">{{ selectedWallet.lastDonation || '—' }}</div>
                        </div>

                      </div>
                    </q-card-section>
                  </q-card>
                </div>

              </div>

              <!-- ── Analytics Charts ───────────────────────────────────── -->
              <div class="q-mt-md">
                <div class="row items-center q-mb-md">
                  <div style="font-size: 14px; font-weight: 700; color: #37474f;" class="chart-section-title">Donation Analytics</div>
                </div>

                <div class="row q-col-gutter-md">

                  <!-- Line Chart: Donation Trend -->
                  <div class="col-12 col-md-6">
                    <q-card flat class="detail-info-card chart-card">
                      <q-card-section class="q-pb-xs">
                        <div class="row items-center justify-between">
                          <div>
                            <div class="chart-card-title">Donation Trend</div>
                            <div class="chart-card-sub">BCH donated over time</div>
                          </div>
                          <q-icon name="show_chart" color="blue-4" size="20px" />
                        </div>
                      </q-card-section>
                      <q-separator />
                      <q-card-section class="q-pa-md">
                        <div class="chart-canvas-wrapper">
                          <LineChart :data="lineChartData" :options="lineChartOptions" />
                        </div>
                      </q-card-section>
                    </q-card>
                  </div>

                  <!-- Bar Chart: By Cause -->
                  <div class="col-12 col-md-6">
                    <q-card flat class="detail-info-card chart-card">
                      <q-card-section class="q-pb-xs">
                        <div class="row items-center justify-between">
                          <div>
                            <div class="chart-card-title">Donations by Cause</div>
                            <div class="chart-card-sub">Total BCH per category</div>
                          </div>
                          <q-icon name="bar_chart" color="purple-4" size="20px" />
                        </div>
                      </q-card-section>
                      <q-separator />
                      <q-card-section class="q-pa-md">
                        <div class="chart-canvas-wrapper">
                          <BarChart :data="barChartData" :options="barChartOptions" />
                        </div>
                      </q-card-section>
                    </q-card>
                  </div>

                  <!-- Doughnut Chart: Distribution -->
                  <div class="col-12 col-md-6">
                    <q-card flat class="detail-info-card chart-card">
                      <q-card-section class="q-pb-xs">
                        <div class="row items-center justify-between">
                          <div>
                            <div class="chart-card-title">Donation Distribution</div>
                            <div class="chart-card-sub">Breakdown by cause</div>
                          </div>
                          <q-icon name="pie_chart" color="green-5" size="20px" />
                        </div>
                      </q-card-section>
                      <q-separator />
                      <q-card-section class="q-pa-md">
                        <div class="chart-canvas-wrapper chart-canvas-wrapper--pie">
                          <DoughnutChart :data="doughnutChartData" :options="doughnutChartOptions" />
                        </div>
                      </q-card-section>
                    </q-card>
                  </div>

                  <!-- Radar Chart: BCH + Count per Cause -->
                  <div class="col-12 col-md-6">
                    <q-card flat class="detail-info-card chart-card">
                      <q-card-section class="q-pb-xs">
                        <div class="row items-center justify-between">
                          <div>
                            <div class="chart-card-title">Cause Radar</div>
                            <div class="chart-card-sub">BCH vs. count per category</div>
                          </div>
                          <q-icon name="radar" color="orange-5" size="20px" />
                        </div>
                      </q-card-section>
                      <q-separator />
                      <q-card-section class="q-pa-md">
                        <div class="chart-canvas-wrapper chart-canvas-wrapper--pie">
                          <RadarChart :data="radarChartData" :options="radarChartOptions" />
                        </div>
                      </q-card-section>
                    </q-card>
                  </div>

                  <!-- 3D Scatter Chart: Amount × Date × Recipient -->
                  <div class="col-12">
                    <q-card flat class="detail-info-card chart-card">
                      <q-card-section class="q-pb-xs">
                        <div class="row items-center justify-between">
                          <div>
                            <div class="chart-card-title">3D Donation Scatter</div>
                            <div class="chart-card-sub">Date · BCH Amount · Recipient — drag to rotate</div>
                          </div>
                          <q-icon name="scatter_plot" color="deep-orange-4" size="20px" />
                        </div>
                      </q-card-section>
                      <q-separator />
                      <q-card-section class="q-pa-md">
                        <div ref="scatter3dContainer" class="chart-canvas-wrapper chart-canvas-wrapper--scatter3d" />
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

       
        <div v-if="activeTab === 'activity' && !loadingDonations" class="activity-view">
          <div class="row items-center justify-between q-mb-lg activity-view__header">
            <h4 class="q-my-none activity-heading">Donation Activity</h4>
            <div class="activity-view__actions">
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

         
          <q-card flat class="q-mt-md activity-section-card">
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
                :grid="$q.screen.lt.md"
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

                <!-- Mobile card layout (grid mode) -->
                <template v-slot:item="props">
                  <div class="donation-mobile-card">
                    <div class="donation-mobile-card__header">
                      <div class="donation-mobile-card__recipient">{{ props.row.recipient }}</div>
                      <q-badge color="primary" :label="props.row.coin || 'BCH'" class="q-ml-xs" />
                    </div>

                    <div class="donation-mobile-card__body">
                      <div class="donation-mobile-card__row">
                        <span class="donation-mobile-card__label">Date</span>
                        <span class="donation-mobile-card__value">{{ formatDate(props.row.timestamp) }}</span>
                      </div>
                      <div class="donation-mobile-card__row">
                        <span class="donation-mobile-card__label">Donor</span>
                        <span class="donation-mobile-card__value">{{ props.row.donor_name }}</span>
                      </div>
                      <div class="donation-mobile-card__row">
                        <span class="donation-mobile-card__label">Amount</span>
                        <span class="donation-mobile-card__value text-weight-bold text-positive">{{ formatCurrency(props.row.amount) }}</span>
                      </div>
                      <div class="donation-mobile-card__row">
                        <span class="donation-mobile-card__label">Interval</span>
                        <span class="donation-mobile-card__value">
                          <q-badge v-if="props.row.interval" color="blue-7" :label="props.row.interval" />
                          <span v-else class="text-grey-6">One-time</span>
                        </span>
                      </div>
                    </div>

                    <div class="donation-mobile-card__footer">
                      <q-btn
                        flat dense no-caps
                        icon="receipt_long" label="Details"
                        size="sm" color="primary"
                        @click="viewDonationDetails(props.row)"
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

    <!-- Recipient Detail Dialog -->
    <q-dialog v-model="recipientDetailDialog.open">
      <q-card class="tx-detail-dialog">

        <!-- Header -->
        <div class="tx-detail-header">
          <div class="row items-center justify-between no-wrap">
            <div style="min-width: 0; flex: 1; overflow: hidden;">
              <div class="tx-detail-title" style="white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">{{ recipientDetailDialog.name }}</div>
              <div class="tx-detail-sub">Received by Recipient</div>
            </div>
            <q-btn flat round dense icon="close" @click="recipientDetailDialog.open = false" class="tx-close-btn q-ml-sm" style="flex-shrink: 0;" />
          </div>
        </div>

        <!-- Status badge -->
        <q-card-section class="q-pt-md q-pb-sm">
          <q-badge
            :color="recipientDetailDialog.hasCompleted ? 'positive' : 'warning'"
            :label="recipientDetailDialog.hasCompleted ? 'ALL RECEIVED' : 'PENDING'"
            style="font-size: 12px; font-weight: 700; padding: 5px 14px; border-radius: 6px; letter-spacing: 0.5px;"
          />
        </q-card-section>

        <!-- Details rows -->
        <q-card-section class="q-pt-xs q-pb-md" style="max-height: 65vh; overflow-y: auto;">
          <div class="tx-detail-table">
            <div class="tx-detail-row" v-for="row in recipientDetailDialog.rows" :key="row.label">
              <div class="tx-detail-label">{{ row.label }}</div>
              <div class="tx-detail-value" :style="row.style">{{ row.value }}</div>
            </div>
            <div class="tx-detail-row tx-detail-row--amount">
              <div class="tx-detail-label" style="font-weight: 700;">Total Received</div>
              <div class="tx-detail-value" style="font-size: 18px; font-weight: 800; color: #4caf50;">
                {{ recipientDetailDialog.totalAmount }} BCH
              </div>
            </div>
          </div>

          <!-- Donation history -->
          <div v-if="recipientDetailDialog.donations.length > 0" class="q-mt-md">
            <div style="font-size: 12px; font-weight: 700; color: #78909c; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 8px;">Donation History</div>
            <div class="tx-detail-table recipient-history-table">
              <div
                v-for="(d, i) in recipientDetailDialog.donations"
                :key="i"
                class="tx-detail-row recipient-history-row"
              >
                <div class="tx-detail-label recipient-history-label">
                  <div style="font-weight: 700;">{{ d.cycleLabel || 'Cycle' }}</div>
                  <div style="font-size: 11px; color: #78909c; margin-top: 2px;">{{ d.date || d.timestamp || '—' }}</div>
                  <div
                    v-if="d.txid"
                    class="recipient-history-txid"
                    @click="$q.copyToClipboard(d.txid).then(() => $q.notify({ type: 'positive', message: 'TxID copied', position: 'top', timeout: 1200 }))"
                  >
                    TXID: {{ d.txid }}
                  </div>
                </div>
                <div class="tx-detail-value recipient-history-value">
                  <span style="font-weight: 700;">{{ d.amount }} BCH</span>
                  <q-badge
                    :color="d.status === 'withdrawn' || d.status === 'completed' ? 'positive' : 'warning'"
                    :label="d.status || 'pending'"
                    class="q-ml-sm recipient-history-badge"
                    style="font-size: 10px;"
                  />
                </div>
              </div>
            </div>
          </div>

          <!-- Note -->
          <div class="tx-detail-note q-mt-md">
            <q-icon name="info_outline" size="14px" class="q-mr-xs" />
            <span>Donations to this recipient are recorded on the Bitcoin Cash blockchain.</span>
          </div>
        </q-card-section>

        <q-card-actions align="right" class="q-px-md q-pb-md">
          <q-btn unelevated color="primary" label="Close" no-caps style="border-radius: 8px; min-width: 90px;" @click="recipientDetailDialog.open = false" />
        </q-card-actions>
      </q-card>
    </q-dialog>

    <!-- Donation Detail Dialog -->
    <q-dialog v-model="donationDetailDialog.open">
      <q-card class="tx-detail-dialog">
        <div class="tx-detail-header">
          <div class="row items-center justify-between no-wrap">
            <div style="min-width: 0; flex: 1; overflow: hidden;">
              <div class="tx-detail-title">Donation Details</div>
              <div class="tx-detail-sub">BiToHelp Blockchain Donation Platform</div>
            </div>
            <q-btn flat round dense icon="close" @click="donationDetailDialog.open = false" class="tx-close-btn q-ml-sm" style="flex-shrink: 0;" />
          </div>
        </div>

        <q-card-section class="q-pt-md q-pb-xs">
          <q-badge
            :color="donationDetailDialog.statusColor"
            :label="donationDetailDialog.statusLabel"
            style="font-size: 12px; font-weight: 700; padding: 5px 14px; border-radius: 6px; letter-spacing: 0.5px;"
          />
        </q-card-section>

        <q-card-section class="q-pt-xs q-pb-md" style="max-height: 65vh; overflow-y: auto;">
          <div class="tx-detail-table">
            <div class="tx-detail-row" v-for="row in donationDetailDialog.rows" :key="row.label">
              <div class="tx-detail-label">{{ row.label }}</div>
              <div class="tx-detail-value" :style="row.style">{{ row.value }}</div>
            </div>
            <div class="tx-detail-row tx-detail-row--amount">
              <div class="tx-detail-label" style="font-weight: 700;">Donation Amount</div>
              <div class="tx-detail-value" style="font-size: 18px; font-weight: 800; color: #1976d2;">
                {{ donationDetailDialog.formattedAmount }} {{ donationDetailDialog.coin }}
              </div>
            </div>
            <div class="tx-detail-row" v-if="donationDetailDialog.txid">
              <div class="tx-detail-label">Transaction ID</div>
              <div class="tx-detail-value" style="font-family: monospace; font-size: 11px; word-break: break-all;">
                {{ donationDetailDialog.txid }}
              </div>
            </div>
          </div>

          <div class="tx-detail-note q-mt-md">
            <q-icon name="info_outline" size="14px" class="q-mr-xs" />
            <span>This transaction is recorded on the Bitcoin Cash blockchain. For receipt or tax purposes, use View Receipt.</span>
          </div>
        </q-card-section>

        <q-card-actions align="right" class="q-px-md q-pb-md" style="gap: 8px;">
          <q-btn flat color="primary" label="View Receipt" no-caps @click="openReceiptFromDetail()" />
          <q-btn unelevated color="primary" label="Close" no-caps style="border-radius: 8px; min-width: 90px;" @click="donationDetailDialog.open = false" />
        </q-card-actions>
      </q-card>
    </q-dialog>

    <!-- Receipt Dialog -->
    <q-dialog v-model="receiptDialog.open">
      <q-card class="receipt-dialog">
        <!-- Letterhead header -->
        <div class="receipt-header">
          <div class="row items-center justify-between no-wrap">
            <div style="min-width: 0; flex: 1; overflow: hidden;">
              <div class="receipt-brand">BiToHelp</div>
              <div class="receipt-brand-sub">Blockchain-Powered Charitable Giving</div>
            </div>
            <q-btn flat round dense icon="close" @click="receiptDialog.open = false" class="tx-close-btn q-ml-sm" style="flex-shrink: 0;" />
          </div>
        </div>

        <q-card-section class="q-pa-none" style="max-height: 70vh; overflow-y: auto;">
          <!-- Receipt title bar -->
          <div class="receipt-title-bar">
            <div class="row items-center justify-between no-wrap">
              <div>
                <div style="font-size: 16px; font-weight: 700;">Official Donation Receipt</div>
                <div style="font-size: 12px; margin-top: 2px; opacity: 0.65;">Tax-Deductible Donation Record</div>
              </div>
              <q-badge
                :color="receiptDialog.statusColor"
                :label="receiptDialog.statusLabel"
                style="font-size: 11px; font-weight: 700; padding: 4px 12px; border-radius: 6px;"
              />
            </div>
          </div>

          <div class="q-pa-md">
            <!-- Receipt number + date -->
            <div class="receipt-info-bar q-mb-md">
              <div class="row">
                <div class="col-6">
                  <div class="receipt-field-label">Receipt Number</div>
                  <div class="receipt-field-mono">{{ receiptDialog.receiptNumber }}</div>
                </div>
                <div class="col-6 text-right">
                  <div class="receipt-field-label">Issue Date</div>
                  <div class="receipt-field-value">{{ receiptDialog.currentDate }}</div>
                </div>
              </div>
            </div>

            <!-- Donor Information -->
            <div class="receipt-section-title">Donor Information</div>
            <div class="tx-detail-table q-mb-md">
              <div class="tx-detail-row">
                <div class="tx-detail-label">Full Name</div>
                <div class="tx-detail-value">{{ receiptDialog.donorName }}</div>
              </div>
              <div class="tx-detail-row">
                <div class="tx-detail-label">Email Address</div>
                <div class="tx-detail-value">{{ receiptDialog.donorEmail }}</div>
              </div>
              <div class="tx-detail-row">
                <div class="tx-detail-label">BCH Wallet</div>
                <div class="tx-detail-value" style="font-family: monospace; font-size: 11px; word-break: break-all;">{{ receiptDialog.walletAddress }}</div>
              </div>
            </div>

            <!-- Donation Details -->
            <div class="receipt-section-title">Donation Details</div>
            <div class="tx-detail-table q-mb-md">
              <div class="tx-detail-row">
                <div class="tx-detail-label">Transaction Date</div>
                <div class="tx-detail-value">{{ receiptDialog.receiptDate }}</div>
              </div>
              <div class="tx-detail-row">
                <div class="tx-detail-label">Recipient</div>
                <div class="tx-detail-value">{{ receiptDialog.recipient }}</div>
              </div>
              <div class="tx-detail-row">
                <div class="tx-detail-label">Cause Category</div>
                <div class="tx-detail-value">{{ receiptDialog.cause }}</div>
              </div>
              <div class="tx-detail-row">
                <div class="tx-detail-label">Payment Method</div>
                <div class="tx-detail-value">Bitcoin Cash (BCH)</div>
              </div>
              <div class="tx-detail-row tx-detail-row--amount">
                <div class="tx-detail-label" style="font-weight: 700;">Total Amount</div>
                <div class="tx-detail-value" style="font-size: 20px; font-weight: 800; color: #1976d2;">
                  {{ receiptDialog.formattedAmount }} BCH
                </div>
              </div>
            </div>

            <!-- Tax notice -->
            <div class="tx-detail-note q-mb-md">
              <q-icon name="gavel" size="14px" class="q-mr-xs" />
              <span><strong>Tax Deduction Notice:</strong> This receipt serves as official documentation for tax purposes. Please consult your tax advisor regarding deductibility in your jurisdiction.</span>
            </div>

            <!-- Footer -->
            <div class="receipt-footer">
              <div style="font-size: 14px; font-weight: 700; margin-bottom: 6px;">Thank You for Your Generosity!</div>
              <div style="font-size: 12px; opacity: 0.65; line-height: 1.6;">BiToHelp • Cryptocurrency Donation Platform<br>This is a computer-generated receipt valid without signature.<br>For inquiries: support@bitohelp.org</div>
            </div>
          </div>
        </q-card-section>

        <q-card-actions align="right" class="q-px-md q-pb-md" style="gap: 8px;">
          <q-btn flat color="grey-7" label="Close" no-caps @click="receiptDialog.open = false" />
          <q-btn unelevated color="primary" label="Download Receipt" icon="download" no-caps style="border-radius: 8px;" @click="downloadReceipt(receiptDialog.donation)" />
        </q-card-actions>
      </q-card>
    </q-dialog>

  </q-page>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted, watch, nextTick } from 'vue'
import { Line as LineChart, Bar as BarChart, Doughnut as DoughnutChart, Radar as RadarChart } from 'vue-chartjs'
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  RadialLinearScale,
  PointElement,
  LineElement,
  BarElement,
  ArcElement,
  Title,
  Tooltip,
  Legend,
  Filler
} from 'chart.js'

ChartJS.register(
  CategoryScale,
  LinearScale,
  RadialLinearScale,
  PointElement,
  LineElement,
  BarElement,
  ArcElement,
  Title,
  Tooltip,
  Legend,
  Filler
)
import { useDonationStore } from '../stores/donation-store'
import { useQuasar } from 'quasar'
import { api } from 'boot/axios'
import bchImg from 'src/assets/bch.png'
import projectImg from 'src/assets/project.png'
import transactionImg from 'src/assets/transaction.png'

const $q = useQuasar()
const donationStore = useDonationStore()
const WALLET_SNAPSHOT_STORAGE_KEY = 'bitohelp.wallet.snapshot'
const WALLET_CONNECTED_EVENT = 'bitohelp:wallet-connection-changed'

const connectedWalletSnapshot = ref({
  connected: false,
  address: '',
  namespace: '',
})
const handleWalletConnectionChanged = () => refreshConnectedWalletSnapshot()

const refreshConnectedWalletSnapshot = () => {
  try {
    const raw = localStorage.getItem(WALLET_SNAPSHOT_STORAGE_KEY)
    if (!raw) {
      connectedWalletSnapshot.value = { connected: false, address: '', namespace: '' }
      return
    }
    const parsed = JSON.parse(raw)
    connectedWalletSnapshot.value = {
      connected: Boolean(parsed?.connected),
      address: parsed?.address || '',
      namespace: parsed?.namespace || '',
    }
  } catch {
    connectedWalletSnapshot.value = { connected: false, address: '', namespace: '' }
  }
}

refreshConnectedWalletSnapshot()

const loadingDonations = ref(true)
const payoutCyclesByDonationId = ref({})

const recipientDetailDialog = ref({
  open: false,
  name: '',
  hasCompleted: true,
  totalAmount: '0.00',
  rows: [],
  donations: []
})

const donationDetailDialog = ref({
  open: false,
  statusColor: 'positive',
  statusLabel: 'COMPLETED',
  formattedAmount: '0.00',
  coin: 'BCH',
  txid: '',
  rows: []
})

const receiptDialog = ref({
  open: false,
  donation: null,
  statusColor: 'positive',
  statusLabel: 'COMPLETED',
  receiptNumber: '',
  currentDate: '',
  receiptDate: '',
  donorName: '',
  donorEmail: '',
  walletAddress: '',
  recipient: '',
  cause: '',
  formattedAmount: '0.00'
})


const activeTab = ref('donations')
const detailTab = ref('donations')
const searchQuery = ref('')
const filteredWallets = computed(() => {
  const q = searchQuery.value.trim().toLowerCase()
  if (!q) return wallets.value
  return wallets.value.filter(
    (w) =>
      w.name?.toLowerCase().includes(q) ||
      w.address?.toLowerCase().includes(q) ||
      w.type?.toLowerCase().includes(q),
  )
})
const activitySearch = ref('')
const statusFilter = ref('All')
const categoryFilter = ref('All')


const wallets = ref([])

const selectedWallet = ref(null)

const buildWalletsFromDonations = () => {
  if (!connectedWalletSnapshot.value.connected) {
    wallets.value = []
    selectedWallet.value = null
    return
  }

  const donations = donationHistory.value || []
  const totalDonated = donations.reduce((sum, donation) => sum + parseFloat(donation.amount || 0), 0)
  const donationCount = donations.length
  const timestamps = donations
    .map((d) => new Date(d.timestamp || d.date || Date.now()).getTime())
    .filter((ts) => Number.isFinite(ts))
    .sort((a, b) => a - b)

  const firstDonationTs = timestamps[0] || Date.now()
  const lastDonationTs = timestamps[timestamps.length - 1] || Date.now()

  const profileConfigs = [
    { name: 'Guest Wallet', email: 'guest@bitohelp.local', product: 'Paytaca Guest' },
    { name: 'Business Account', email: 'business@bitohelp.local', product: 'Paytaca Business' },
    { name: 'Family Account', email: 'family@bitohelp.local', product: 'Paytaca Family' },
  ]
  const connectedAddress = connectedWalletSnapshot.value.address || ''

  const nextWallets = profileConfigs.map((profile, idx) => ({
    id: `connected-wallet-${idx + 1}`,
    name: profile.name,
    address: connectedAddress,
    fullNumber: connectedAddress,
    type: 'Paytaca',
    totalDonated,
    donationCount,
    totalFees: 0,
    donorName: profile.name,
    email: profile.email,
    firstDonationTs,
    lastDonationTs,
    accountName: profile.name,
    product: profile.product,
    iban: connectedAddress,
    swift: 'BCYPCY2N',
    branch: profile.name,
    creditRate: '1000',
    debitRate: totalDonated.toFixed(4),
    overdraftLimit: totalDonated.toFixed(4),
    impactCards: [
      {
        id: 1,
        title1: 'TOTAL',
        title2: 'DONATED',
        colorClass: 'wallet-stat-card-blue',
        largeValue: `${totalDonated.toFixed(4)} BCH`,
        rightIcon: bchImg,
      },
      {
        id: 2,
        title1: 'PROJECTS',
        title2: 'SUPPORTED',
        colorClass: 'wallet-stat-card-purple',
        largeValue: '—',
        rightIcon: projectImg,
      },
      {
        id: 3,
        title1: 'TOTAL',
        title2: 'TRANSACTIONS',
        colorClass: 'wallet-stat-card-yellow',
        largeValue: `${donationCount}+`,
        rightIcon: transactionImg,
      },
    ],
    firstDonation: formatDate(firstDonationTs),
    lastDonation: formatDate(lastDonationTs),
  }))

  wallets.value = nextWallets
  const currentId = selectedWallet.value?.id
  selectedWallet.value = wallets.value.find((wallet) => wallet.id === currentId) || wallets.value[0]
}

const donationColumns = [
  { name: 'date', label: 'Date', field: row => formatDate(row.timestamp), align: 'left', sortable: true },
  { name: 'recipient', label: 'Recipient', field: 'recipient', align: 'left' },
  { name: 'donor', label: 'Donor Name', field: 'donor_name', align: 'left' },
  { name: 'amount', label: 'Amount', field: 'amount', align: 'right', sortable: true },
  { name: 'interval', label: 'Interval', field: 'interval', align: 'center' },
  { name: 'coin', label: 'Coin', field: 'coin', align: 'center' },
  { name: 'actions', label: 'Actions', field: 'actions', align: 'center' }
]


const donationHistory = computed(() => {
  const realDonations = donationStore.donationHistory || []
  return realDonations
})


const allDonations = computed(() => {
  const realDonations = donationStore.donationHistory || []
  return realDonations
})

// ── Chart helpers ─────────────────────────────────────────────────────────────
const chartTextColor = computed(() => $q.dark.isActive ? 'rgba(255,255,255,0.65)' : '#546e7a')
const chartGridColor  = computed(() => $q.dark.isActive ? 'rgba(255,255,255,0.10)' : 'rgba(0,0,0,0.18)')

// Line chart: BCH donated over time (last 15 donations sorted by date)
const lineChartData = computed(() => {
  const sorted = [...donationHistory.value]
    .sort((a, b) => new Date(a.timestamp || a.date || 0) - new Date(b.timestamp || b.date || 0))
    .slice(-15)
  return {
    labels: sorted.map(d => {
      const dt = new Date(d.timestamp || d.date)
      return isNaN(dt) ? '—' : dt.toLocaleDateString('en-US', { month: 'short', day: 'numeric' })
    }),
    datasets: [{
      label: 'BCH Donated',
      data: sorted.map(d => parseFloat(d.amount || 0)),
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
const lineChartOptions = computed(() => ({
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: { display: false },
    tooltip: { callbacks: { label: ctx => ` ${ctx.parsed.y.toFixed(4)} BCH` } }
  },
  scales: {
    x: {
      grid: { color: chartGridColor.value },
      ticks: { color: chartTextColor.value, font: { size: 10 } }
    },
    y: {
      grid: { color: chartGridColor.value },
      ticks: { color: chartTextColor.value, font: { size: 10 }, callback: v => v + ' BCH' },
      beginAtZero: true
    }
  }
}))

// Bar chart: total BCH per cause category
const CHART_COLORS = ['#1976d2','#7b1fa2','#2e7d32','#e65100','#c62828','#00838f','#37474f']
const causeChartMap = computed(() => {
  const map = {}
  donationHistory.value.forEach(d => {
    const c = d.cause || 'General'
    map[c] = (map[c] || 0) + parseFloat(d.amount || 0)
  })
  return map
})
const barChartData = computed(() => {
  const causes = Object.keys(causeChartMap.value)
  return {
    labels: causes,
    datasets: [{
      label: 'Total BCH',
      data: causes.map(c => parseFloat(causeChartMap.value[c].toFixed(4))),
      backgroundColor: causes.map((_, i) => CHART_COLORS[i % CHART_COLORS.length] + 'cc'),
      borderColor:      causes.map((_, i) => CHART_COLORS[i % CHART_COLORS.length]),
      borderWidth: 1.5,
      borderRadius: 6
    }]
  }
})
const barChartOptions = computed(() => ({
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: { display: false },
    tooltip: { callbacks: { label: ctx => ` ${ctx.parsed.y.toFixed(4)} BCH` } }
  },
  scales: {
    x: {
      grid: { display: false },
      ticks: { color: chartTextColor.value, font: { size: 10 } }
    },
    y: {
      grid: { color: chartGridColor.value },
      ticks: { color: chartTextColor.value, font: { size: 10 }, callback: v => v + ' BCH' },
      beginAtZero: true
    }
  }
}))

// Doughnut chart: BCH distribution by cause
const doughnutChartData = computed(() => {
  const causes = Object.keys(causeChartMap.value)
  const PIE_BG = [
    'rgba(25,118,210,0.85)','rgba(123,31,162,0.85)','rgba(46,125,50,0.85)',
    'rgba(230,81,0,0.85)','rgba(198,40,40,0.85)','rgba(0,131,143,0.85)','rgba(55,71,79,0.85)'
  ]
  return {
    labels: causes,
    datasets: [{
      data: causes.map(c => parseFloat(causeChartMap.value[c].toFixed(4))),
      backgroundColor: PIE_BG.slice(0, causes.length),
      borderColor: $q.dark.isActive ? 'rgba(18,24,46,0.8)' : 'rgba(255,255,255,0.8)',
      borderWidth: 2
    }]
  }
})
const doughnutChartOptions = computed(() => ({
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: {
      position: 'bottom',
      labels: { color: chartTextColor.value, font: { size: 11 }, padding: 12, boxWidth: 12 }
    },
    tooltip: { callbacks: { label: ctx => ` ${ctx.label}: ${ctx.parsed.toFixed(4)} BCH` } }
  }
}))

// Radar chart: donation count + total BCH per cause
const radarChartData = computed(() => {
  const causes = Object.keys(causeChartMap.value)
  const countMap = {}
  donationHistory.value.forEach(d => {
    const c = d.cause || 'General'
    countMap[c] = (countMap[c] || 0) + 1
  })
  const isDark = $q.dark.isActive
  return {
    labels: causes,
    datasets: [
      {
        label: 'Total BCH',
        data: causes.map(c => parseFloat(causeChartMap.value[c].toFixed(4))),
        borderColor: '#1976d2',
        backgroundColor: isDark ? 'rgba(25,118,210,0.25)' : 'rgba(25,118,210,0.15)',
        borderWidth: 2,
        pointBackgroundColor: '#1976d2',
        pointRadius: 4
      },
      {
        label: 'No. of Donations',
        data: causes.map(c => countMap[c] || 0),
        borderColor: '#7b1fa2',
        backgroundColor: isDark ? 'rgba(123,31,162,0.25)' : 'rgba(123,31,162,0.12)',
        borderWidth: 2,
        pointBackgroundColor: '#7b1fa2',
        pointRadius: 4
      }
    ]
  }
})

const radarChartOptions = computed(() => ({
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: {
      position: 'bottom',
      labels: { color: chartTextColor.value, font: { size: 11 }, padding: 12, boxWidth: 12 }
    },
    tooltip: {
      callbacks: {
        label: ctx => ` ${ctx.dataset.label}: ${ctx.parsed.r}`
      }
    }
  },
  scales: {
    r: {
      grid:      { color: chartGridColor.value },
      angleLines: { color: chartGridColor.value },
      pointLabels: { color: chartTextColor.value, font: { size: 10 } },
      ticks: { color: chartTextColor.value, font: { size: 9 }, backdropColor: 'transparent' },
      beginAtZero: true
    }
  }
}))
// ─────────────────────────────────────────────────────────────────────────────

const updateWalletStats = () => {
  buildWalletsFromDonations()
}


watch(() => donationStore.donationHistory, () => {
  updateWalletStats()
}, { immediate: true, deep: true })

watch(connectedWalletSnapshot, () => {
  updateWalletStats()
}, { deep: true })


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

function formatDate(timestamp) {
  if (!timestamp) return 'N/A'
  const date = new Date(timestamp)
  return date.toLocaleDateString('en-US', { 
    year: 'numeric', 
    month: 'short', 
    day: 'numeric'
  })
}

function formatDateTime(timestamp) {
  if (!timestamp) return 'N/A'
  const date = new Date(timestamp)
  return date.toLocaleString('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}

const normalizeCycleStatus = (status) => {
  const value = (status || '').toLowerCase()
  if (value === 'executed') return 'withdrawn'
  return value || 'pending'
}

const fetchPayoutCycles = async () => {
  try {
    const response = await api.get('payouts/')
    const payouts = Array.isArray(response.data) ? response.data : []
    const grouped = {}

    payouts.forEach((payout) => {
      if (!payout?.donation_id) return
      if (!grouped[payout.donation_id]) grouped[payout.donation_id] = []
      grouped[payout.donation_id].push(payout)
    })

    Object.keys(grouped).forEach((donationId) => {
      grouped[donationId].sort((a, b) => (a.cycle_number || 0) - (b.cycle_number || 0))
    })

    payoutCyclesByDonationId.value = grouped
  } catch (error) {
    payoutCyclesByDonationId.value = {}
    console.warn('Unable to load payout cycles for donor view:', error)
  }
}

const buildRecipientHistoryRows = (recipient) => {
  const rows = []
  const donations = recipient?.donations || []

  donations.forEach((donation) => {
    const cycles = payoutCyclesByDonationId.value[donation.id] || []

    if (cycles.length > 0) {
      cycles.forEach((cycle) => {
        const amountBch = Number(cycle.payout_amount_satoshis || 0) / 1e8
        const rawDate = cycle.executed_at || cycle.due_at || donation.timestamp || donation.date
        rows.push({
          cycleLabel: `Cycle ${cycle.cycle_number || 1}/${cycle.total_cycles || 1}`,
          date: formatDateTime(rawDate),
          amount: formatCurrency(amountBch),
          status: normalizeCycleStatus(cycle.status),
          txid: cycle.txid || donation.txid || '',
          sortKey: new Date(rawDate).getTime() || 0,
        })
      })
      return
    }

    const rawDate = donation.timestamp || donation.date
    rows.push({
      cycleLabel: donation.interval ? 'Cycle 1/1' : 'One-time',
      date: formatDateTime(rawDate),
      amount: formatCurrency(donation.amount),
      status: normalizeCycleStatus(donation.status),
      txid: donation.txid || '',
      sortKey: new Date(rawDate).getTime() || 0,
    })
  })

  return rows.sort((a, b) => (b.sortKey || 0) - (a.sortKey || 0))
}

const openReceiptFromDetail = () => {
  donationDetailDialog.value.open = false
  const donation = donationDetailDialog.value._raw
  if (donation) viewReceipt(donation)
}

const viewDonationDetails = (donation) => {
  const donationDate = formatDate(donation.timestamp || donation.date)
  const formattedAmount = formatCurrency(donation.amount)
  donationDetailDialog.value = {
    open: true,
    _raw: donation,
    statusColor: donation.status === 'completed' ? 'positive' : donation.status === 'failed' ? 'negative' : 'warning',
    statusLabel: (donation.status || 'pending').toUpperCase(),
    formattedAmount,
    coin: donation.coin || 'BCH',
    txid: donation.txid || '',
    rows: [
      { label: 'Date', value: donationDate },
      { label: 'Cause / Nonprofit', value: donation.cause || 'N/A' },
      { label: 'Recipient', value: donation.recipient || 'N/A' },
      { label: 'Donor Name', value: donation.donor_name || 'Anonymous' },
      { label: 'Donor Email', value: donation.donor_email || 'N/A' },
      { label: 'Interval', value: donation.interval || 'One-time' },
      { label: 'Message', value: donation.message || 'No message' },
    ]
  }
}

const viewReceipt = (donation) => {
  try {
    const receiptDate = new Date(donation.date || donation.timestamp).toLocaleDateString('en-US', {
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

    receiptDialog.value = {
      open: true,
      donation,
      statusColor: donation.status === 'completed' ? 'positive' : donation.status === 'failed' ? 'negative' : 'warning',
      statusLabel: (donation.status || 'pending').toUpperCase(),
      receiptNumber: mockTxId,
      currentDate,
      receiptDate,
      donorName: walletInfo.donorName,
      donorEmail: walletInfo.email,
      walletAddress: walletInfo.address,
      recipient: donation.recipient || 'N/A',
      cause: donation.cause || 'N/A',
      formattedAmount
    }
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
  const historyRows = buildRecipientHistoryRows(recipient)
  recipientDetailDialog.value = {
    open: true,
    name: recipient.name,
    hasCompleted: recipient.hasCompleted,
    totalAmount: formatCurrency(recipient.totalAmount),
    donations: historyRows,
    rows: [
      { label: 'Cause', value: recipient.cause || 'General' },
      { label: 'Number of Donations', value: recipient.count },
      { label: 'Cycles Tracked', value: historyRows.length },
      { label: 'Last Donation', value: recipient.lastDate || '—' },
    ]
  }
}

// ── 3D Scatter Chart (Plotly) ─────────────────────────────────────────────
const scatter3dContainer = ref(null)
let scatter3dInstance = null

const build3dScatter = async () => {
  if (!scatter3dContainer.value) return
  const donations = donationHistory.value
  if (!donations.length) return
  let Plotly
  try { Plotly = (await import('plotly.js-gl3d-dist-min')).default } catch { return }

  const recipientNames = [...new Set(donations.map(d => d.recipient || 'Unknown'))]
  const CAUSE_COLORS = [
    '#1976d2','#7b1fa2','#2e7d32','#e65100','#c62828','#00838f','#37474f','#ad1457'
  ]
  const causeList = [...new Set(donations.map(d => d.cause || 'General'))]

  const sorted = [...donations].sort((a, b) =>
    new Date(a.timestamp || a.date || 0) - new Date(b.timestamp || b.date || 0)
  )
  const baseTime = new Date(sorted[0].timestamp || sorted[0].date || Date.now()).getTime()

  const isDark = $q.dark.isActive
  // paper_bgcolor / plot_bgcolor are 2-D-only properties; scene.bgcolor controls the GL3D viewport.
  // WebGL ignores alpha, so we use solid colours to avoid a black scene background.
  const paperBg    = isDark ? 'rgba(0,0,0,0)'    : 'rgba(0,0,0,0)'
  const sceneBg    = isDark ? '#12182e'           : '#f8faff'
  const textColor  = isDark ? 'rgba(255,255,255,0.75)' : '#37474f'
  const gridColor  = isDark ? 'rgba(255,255,255,0.15)' : 'rgba(0,0,0,0.22)'

  // Group by cause for separate traces (legend)
  const traces = causeList.map((cause, ci) => {
    const causeRows = sorted.filter(d => (d.cause || 'General') === cause)
    return {
      type: 'scatter3d',
      mode: 'markers',
      name: cause,
      x: causeRows.map(d => +(((new Date(d.timestamp || d.date || Date.now()).getTime() - baseTime) / 86400000).toFixed(1))),
      y: causeRows.map(d => parseFloat(d.amount || 0)),
      z: causeRows.map(d => recipientNames.indexOf(d.recipient || 'Unknown')),
      text: causeRows.map(d => `${d.recipient || 'Unknown'}<br>${parseFloat(d.amount || 0).toFixed(4)} BCH<br>${d.cause || 'General'}`),
      hovertemplate: '%{text}<extra></extra>',
      marker: {
        size: 7,
        color: CAUSE_COLORS[ci % CAUSE_COLORS.length],
        opacity: 0.85,
        line: { color: 'rgba(255,255,255,0.3)', width: 0.5 }
      }
    }
  })

  const layout = {
    paper_bgcolor: paperBg,
    plot_bgcolor:  paperBg,
    margin: { l: 0, r: 0, t: 10, b: 0 },
    legend: {
      font: { color: textColor, size: 11 },
      bgcolor: 'rgba(0,0,0,0)',
      orientation: 'h',
      x: 0, y: -0.05
    },
    scene: {
      bgcolor: sceneBg,
      xaxis: {
        title: { text: 'Days Since First', font: { color: textColor, size: 10 } },
        gridcolor: gridColor, zerolinecolor: gridColor,
        tickfont: { color: textColor, size: 9 },
        showbackground: false
      },
      yaxis: {
        title: { text: 'BCH Amount', font: { color: textColor, size: 10 } },
        gridcolor: gridColor, zerolinecolor: gridColor,
        tickfont: { color: textColor, size: 9 },
        showbackground: false
      },
      zaxis: {
        title: { text: 'Recipient', font: { color: textColor, size: 10 } },
        gridcolor: gridColor, zerolinecolor: gridColor,
        tickfont: { color: textColor, size: 9 },
        tickvals: recipientNames.map((_, i) => i),
        ticktext: recipientNames.map(n => n.length > 12 ? n.slice(0, 12) + '…' : n),
        showbackground: false
      }
    }
  }

  const config = { responsive: true, displayModeBar: false }

  if (scatter3dInstance) {
    Plotly.react(scatter3dContainer.value, traces, layout, config)
  } else {
    Plotly.newPlot(scatter3dContainer.value, traces, layout, config)
    scatter3dInstance = true
  }
}

watch(
  () => [donationHistory.value, $q.dark.isActive],
  () => nextTick(build3dScatter),
  { deep: true }
)
// ─────────────────────────────────────────────────────────────────────────────

onMounted(async () => {
  window.addEventListener(WALLET_CONNECTED_EVENT, handleWalletConnectionChanged)

  loadingDonations.value = true
  await Promise.all([
    donationStore.fetchDonations(50),
    fetchPayoutCycles(),
    new Promise((resolve) => setTimeout(resolve, 600)),
  ])
  loadingDonations.value = false
  console.log('DonorPage mounted')
  await nextTick()
  build3dScatter()
})

onUnmounted(() => {
  window.removeEventListener(WALLET_CONNECTED_EVENT, handleWalletConnectionChanged)
})
</script>

<style scoped lang="scss">
.donor-page {
  overflow-x: hidden;
  background:
    linear-gradient(135deg, #f0f4ff 0%, #f7f4ff 50%, #f0f9ff 100%);
  background-attachment: fixed;
  min-height: 100vh;
}

.body--dark .donor-page {
  background:
    radial-gradient(ellipse at 0% 0%, rgba(25, 50, 90, 0.6) 0%, transparent 55%),
    radial-gradient(ellipse at 100% 0%, rgba(50, 30, 80, 0.5) 0%, transparent 55%),
    radial-gradient(ellipse at 50% 100%, rgba(10, 30, 60, 0.4) 0%, transparent 60%),
    #0d1117;
}

.sidebar-container {
  background: rgba(255, 255, 255, 0.55);
  backdrop-filter: blur(16px);
  -webkit-backdrop-filter: blur(16px);
  border-right: 1.5px solid rgba(21, 101, 192, 0.14);
}

.body--dark .sidebar-container {
  background: rgba(20, 24, 40, 0.6);
  border-right: 1.5px solid rgba(93, 156, 245, 0.14);
}

.main-content {
  background: rgba(255, 255, 255, 0.72);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  border-left: 1.5px solid rgba(21, 101, 192, 0.10);
}

.body--dark .main-content {
  background: rgba(18, 24, 46, 0.92);
  border-left: 1.5px solid rgba(93, 156, 245, 0.12);
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
.body--dark .accounts-sidebar h5 {
  color: #c5cae9;
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

  /* hide more_vert until hover */
  .sidebar-menu-btn {
    opacity: 0;
    transition: opacity 0.15s ease;
  }

  &:hover {
    border-color: #90caf9;
    box-shadow:
      0 2px 6px rgba(0, 0, 0, 0.08),
      0 8px 24px rgba(21, 101, 192, 0.18);
    transform: translateY(-2px);

    .sidebar-menu-btn {
      opacity: 1;
    }
  }

  &.sidebar-account-card--active {
    border-color: #1565c0;
    box-shadow:
      0 0 0 2px rgba(21, 101, 192, 0.18),
      0 4px 8px rgba(0, 0, 0, 0.08),
      0 10px 28px rgba(21, 101, 192, 0.22);

    .sidebar-menu-btn {
      opacity: 1;
    }

    .sidebar-card-accent {
      opacity: 1;
    }
  }
}

.sidebar-card-accent {
  position: absolute;
  top: 0;
  left: 0;
  width: 4px;
  height: 100%;
  background: linear-gradient(180deg, #1565c0, #42a5f5);
  border-radius: 14px 0 0 14px;
  opacity: 0;
  transition: opacity 0.2s ease;
}

.sidebar-card-divider {
  height: 1px;
  background: rgba(144, 202, 249, 0.3);
  margin: 8px 0 0;
}

.sidebar-address-pill {
  display: flex;
  align-items: center;
  font-size: 10.5px;
  font-family: monospace;
  font-weight: 600;
  color: #5c7ea6;
  background: rgba(144, 202, 249, 0.12);
  border: 1px solid rgba(144, 202, 249, 0.3);
  border-radius: 20px;
  padding: 3px 10px;
  cursor: pointer;
  transition: background 0.15s ease, color 0.15s ease;

  &:hover {
    background: rgba(21, 101, 192, 0.1);
    color: #1565c0;
  }
}


.sidebar-address-pill-label {
  font-family: sans-serif;
  font-size: 9.5px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.4px;
  opacity: 0.7;
  flex-shrink: 0;
}

.sidebar-address-copy-icon {
  flex-shrink: 0;
  opacity: 0.5;
}

.body--dark .sidebar-account-card {
  background: rgba(30, 36, 60, 0.75);
  border-color: rgba(255, 255, 255, 0.10);
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
      background: linear-gradient(180deg, #5d9cf5, #7ecbff);
    }
  }
}

.body--dark .sidebar-card-divider {
  background: rgba(100, 160, 255, 0.15);
}

.body--dark .sidebar-address-pill {
  color: #5a7a9e;
  background: rgba(93, 156, 245, 0.08);
  border-color: rgba(93, 156, 245, 0.2);

  &:hover {
    background: rgba(93, 156, 245, 0.15);
    color: #90caf9;
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

.body--dark .sidebar-stat-value {
  color: #eceff1;
}

.sidebar-stat-value--green {
  color: #2e7d32;
}

.body--dark .sidebar-stat-value--green {
  color: #66bb6a;
}

.sidebar-stat-block {
  flex: 1;
  min-width: 0;
  border-radius: 8px;
  padding: 8px 10px;
  overflow: hidden;
}

.sidebar-stat-block--blue {
  background: #f5f7fa;
}

.sidebar-stat-block--green {
  background: #f0faf2;
}

.body--dark .sidebar-stat-block--blue {
  background: rgba(30, 45, 80, 0.6);
}

.body--dark .sidebar-stat-block--green {
  background: rgba(20, 46, 30, 0.6);
}

.view-all-link {
  color: #1976d2;
  font-size: 13px;
}
.body--dark .view-all-link {
  color: #5d9cf5 !important;
}

.body--dark .sidebar-account-card .sidebar-stat-value[style*="2e7d32"] {
  color: #66bb6a !important;
}

.details-panel {
  background-color: rgba(255, 255, 255, 0.45);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  border-radius: 8px;
  border: 1px solid rgba(144, 202, 249, 0.3);
  padding: 1rem;
}

.body--dark .details-panel {
  background-color: rgba(20, 28, 52, 0.7);
  border-color: rgba(100, 160, 255, 0.2);
}

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

.detail-field-label {
  font-size: 11px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  color: #90a4ae;
  margin-bottom: 4px;
}

.detail-field-value {
  font-size: 14px;
  font-weight: 700;
  color: #212121;
}

.body--dark .detail-field-value {
  color: #eceff1;
}

.detail-address-field {
  font-size: 12px;
  font-weight: 600;
  font-family: monospace;
  color: #1565c0;
  background: #e8f0fe;
  border-radius: 6px;
  padding: 8px 12px;
  word-break: break-all;
  cursor: pointer;
}

.body--dark .detail-address-field {
  color: #90caf9;
  background: rgba(30, 50, 100, 0.5);
}

.detail-section {
  .detail-item {
    padding: 0.5rem 0;
  }
}

/* ── Chart Cards ──────────────────────────────────────────────────── */
.chart-section-title {
  color: #37474f;
}
.body--dark .chart-section-title {
  color: rgba(255, 255, 255, 0.75);
}

.chart-card {
  /* inherits detail-info-card glass styling */
}

.chart-card-title {
  font-size: 13px;
  font-weight: 700;
  color: #37474f;
}
.body--dark .chart-card-title {
  color: rgba(255, 255, 255, 0.85);
}

.chart-card-sub {
  font-size: 11px;
  color: #90a4ae;
  margin-top: 2px;
}
.body--dark .chart-card-sub {
  color: rgba(255, 255, 255, 0.35);
}

.chart-canvas-wrapper {
  position: relative;
  height: 200px;
}
.chart-canvas-wrapper--pie {
  height: 240px;
}
.chart-canvas-wrapper--scatter3d {
  height: 420px;
  width: 100%;
}
/* ──────────────────────────────────────────────────────────────────── */

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
  border: 2px solid rgba(255, 255, 255, 0.5);
  box-shadow: 0 4px 16px rgba(108, 133, 245, 0.45), 0 1px 4px rgba(0,0,0,0.18);
}

.wallet-stat-card-purple {
  background: linear-gradient(135deg, #a9a4ffd3 0%, #7e7affd0 100%);
  border: 2px solid rgba(255, 255, 255, 0.5);
  box-shadow: 0 4px 16px rgba(126, 122, 255, 0.45), 0 1px 4px rgba(0,0,0,0.18);
}

.wallet-stat-card-yellow {
  background: linear-gradient(135deg, #e3d273d9 0%, #ebcf89e2 100%);
  border: 2px solid rgba(255, 255, 255, 0.5);
  box-shadow: 0 4px 16px rgba(227, 210, 115, 0.45), 0 1px 4px rgba(0,0,0,0.18);
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
  background: rgba(255, 255, 255, 0.65) !important;
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  border: 1.5px solid rgba(144, 202, 249, 0.5) !important;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
}

.body--dark .stats-card {
  background: rgba(20, 28, 52, 0.75) !important;
  border-color: rgba(100, 160, 255, 0.25) !important;
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

.body--dark .project-card-detail {
  background: #1a2240 !important;
  border-color: #2e3f6e !important;
  color: #c8d8f0;
}

.body--dark .project-card-detail .text-h6 {
  color: #d8e8ff !important;
}

.body--dark .project-card-detail .text-caption {
  color: #7a96b8 !important;
}

.body--dark .project-card-detail .text-weight-bold {
  color: #c8d8f0 !important;
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

.body--dark .recipient-card {
  background: rgba(30, 36, 60, 0.75);
  border-color: #2e3f6e !important;
}

.body--dark .recipient-card .text-subtitle1 {
  color: #d8e8ff !important;
}

.body--dark .recipient-card .text-caption,
.body--dark .recipient-card .text-grey-6 {
  color: #7a96b8 !important;
}

.body--dark .recipient-card .text-body2 {
  color: #c8d8f0 !important;
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
  background: rgba(248, 249, 250, 0.8);
  transition: all 0.3s ease;

  &:hover {
    background: rgba(233, 236, 239, 0.9);
  }
}

.body--dark .stat-box {
  background: rgba(30, 38, 65, 0.7);

  &:hover {
    background: rgba(40, 50, 80, 0.8);
  }
}

/* Supported Projects & Recipients tab headings + stat card wrapper */
.body--dark .q-tab-panel .text-h6 {
  color: #d8e8ff !important;
}

.body--dark .q-tab-panel > .q-mt-xl .q-card {
  background: #1a2240 !important;
  border-color: #2e3f6e !important;
}

.body--dark .stat-box .text-caption,
.body--dark .stat-box .text-grey-6 {
  color: #7a96b8 !important;
}

.body--dark .stat-box .text-h5 {
  color: #d8e8ff !important;
}


.sidebar-toggle {
  display: flex;
  background: rgba(0, 0, 0, 0.06);
  border-radius: 10px;
  padding: 4px;
  gap: 4px;

  .sidebar-toggle__btn {
    flex: 1;
    text-align: center;
    padding: 7px 10px;
    border-radius: 7px;
    font-size: 13px;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.2s ease;
    color: #555;
    display: flex;
    align-items: center;
    justify-content: center;

    &.active {
      background: white;
      color: #1565c0;
      box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
    }

    &:not(.active):hover {
      background: rgba(255, 255, 255, 0.5);
    }
  }
}

.make-donation-btn {
  background: linear-gradient(135deg, #1565c0, #1976d2) !important;
  color: #fff !important;
  font-weight: 700;
  font-size: 14px;
  letter-spacing: 0.4px;
  border-radius: 12px;
  box-shadow: 0 4px 16px rgba(21, 101, 192, 0.35);
  transition: transform 0.2s ease, box-shadow 0.2s ease;
  position: relative;
  overflow: hidden;
}
.make-donation-btn::after {
  content: '';
  position: absolute;
  top: 0; left: -100%;
  width: 60%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255,255,255,0.38), transparent);
  transform: skewX(-20deg);
  animation: donation-shimmer 2.8s ease infinite;
}
@keyframes donation-shimmer {
  0%   { left: -100%; }
  60%  { left: 160%; }
  100% { left: 160%; }
}
.make-donation-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 28px rgba(21, 101, 192, 0.45) !important;
}

.body--dark .make-donation-btn {
  background: linear-gradient(135deg, #0d47a1, #1565c0) !important;
  color: #e3f2fd !important;
  box-shadow: 0 4px 16px rgba(21, 101, 192, 0.45);
}

.body--dark .make-donation-btn:hover {
  background: linear-gradient(135deg, #1565c0, #1e88e5) !important;
  box-shadow: 0 8px 28px rgba(30, 136, 229, 0.5) !important;
}

.body--dark .sidebar-toggle {
  background: rgba(255, 255, 255, 0.08);

  .sidebar-toggle__btn {
    color: #aaa;

    &.active {
      background: rgba(255, 255, 255, 0.15);
      color: #90caf9;
      box-shadow: 0 2px 8px rgba(0, 0, 0, 0.3);
    }

    &:not(.active):hover {
      background: rgba(255, 255, 255, 0.1);
    }
  }
}

.sidebar-search {
  :deep(.q-field__control) {
    background: rgba(255, 255, 255, 0.85) !important;
  }
}

.body--dark .sidebar-search {
  :deep(.q-field__control) {
    background: rgba(255, 255, 255, 0.08) !important;
  }

  :deep(.q-field__native),
  :deep(.q-field__suffix) {
    color: #e0e0e0 !important;
  }
}

:deep(.q-tab) {
  font-weight: 500;
}

.body--dark .donor-detail-tabs {
  color: rgba(255, 255, 255, 0.6);

  :deep(.q-tab--active) {
    color: #90caf9 !important;
  }

  :deep(.q-tabs__content) {
    color: rgba(255, 255, 255, 0.6);
  }
}

:deep(.q-tab-panels) {
  background: transparent !important;
}

:deep(.q-tab-panel) {
  background: transparent !important;
}


/* ─── Donation Activity section ─────────────────────────────────── */
.activity-heading {
  font-size: 1.4rem;
  font-weight: 700;
  color: #1a237e;
}
.body--dark .activity-heading {
  color: #d8e8ff;
}

.activity-view__header {
  flex-wrap: wrap;
  gap: 8px;
}

.activity-view__actions {
  display: flex;
  align-items: center;
  flex-shrink: 0;
}

.activity-section-card {
  border-radius: 12px;
  background: rgba(255, 255, 255, 0.9) !important;
  border: 1.5px solid rgba(144, 202, 249, 0.5);
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.06);
}
.body--dark .activity-section-card {
  background: rgba(18, 26, 52, 0.85) !important;
  border-color: rgba(100, 160, 255, 0.2) !important;
}

/* fix stats-card label contrast in light mode */
.stats-card .text-caption {
  color: #546e7a !important;
}
.stats-card .text-h5 {
  color: #1a237e !important;
}
.body--dark .stats-card .text-caption {
  color: #7a96b8 !important;
}
.body--dark .stats-card .text-h5 {
  color: #d8e8ff !important;
}

.transactions-table {
  :deep(.q-table__container),
  :deep(.q-table__card) {
    background: transparent !important;
    box-shadow: none;
  }

  :deep(.q-table__middle) {
    background: transparent !important;
  }

  :deep(.q-table__top),
  :deep(.q-table__bottom) {
    background: transparent !important;
    color: #546e7a;
  }

  :deep(thead tr th) {
    background: rgba(144, 202, 249, 0.18);
    color: #1565c0;
    font-weight: 600;
  }

  :deep(tbody tr) {
    background: transparent !important;
  }

  :deep(tbody tr td) {
    color: rgba(0, 0, 0, 0.82);
  }

  :deep(tbody tr:hover td) {
    background: rgba(144, 202, 249, 0.1) !important;
  }
}

.body--dark .transactions-table {
  :deep(thead tr th) {
    background: rgba(40, 60, 120, 0.4) !important;
    color: #90caf9;
    border-bottom-color: rgba(100, 160, 255, 0.3);
  }

  :deep(tbody tr td) {
    color: rgba(255, 255, 255, 0.85);
    border-bottom-color: rgba(255, 255, 255, 0.06);
  }

  :deep(tbody tr:hover td) {
    background: rgba(60, 90, 160, 0.15) !important;
  }

  :deep(.q-table__bottom) {
    color: rgba(255, 255, 255, 0.5);
    border-top-color: rgba(255, 255, 255, 0.1);
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

.tx-detail-dialog {
  width: 92vw;
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
  color: #546e7a !important;
  transition: color 0.15s, background 0.15s;
}
.tx-close-btn:hover {
  color: #1565c0 !important;
  background: rgba(21, 101, 192, 0.1) !important;
}

.body--dark .tx-close-btn {
  color: rgba(255, 255, 255, 0.7) !important;
}
.body--dark .tx-close-btn:hover {
  color: #ffffff !important;
  background: rgba(255, 255, 255, 0.12) !important;
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
  min-width: 140px;
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

/* ── Receipt Dialog ─────────────────────────────────────────────── */
.receipt-dialog {
  width: 92vw;
  max-width: 600px;
  border-radius: 16px !important;
  overflow: hidden;
  border: 1.5px solid rgba(144, 202, 249, 0.5);
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
}

.body--dark .receipt-dialog {
  background: rgba(18, 24, 46, 0.95) !important;
  border-color: rgba(100, 160, 255, 0.25) !important;
}

.receipt-header {
  padding: 20px 20px 16px;
  border-bottom: 1px solid rgba(144, 202, 249, 0.3);
  background: linear-gradient(135deg, rgba(21, 101, 192, 0.08) 0%, rgba(100, 60, 200, 0.05) 100%);
}

.body--dark .receipt-header {
  background: rgba(144, 202, 249, 0.06);
  border-color: rgba(255, 255, 255, 0.07);
}

.receipt-brand {
  font-size: 22px;
  font-weight: 800;
  color: #1a237e;
  letter-spacing: 0.5px;
  line-height: 1.1;
}

.body--dark .receipt-brand {
  color: #c5cae9;
}

.receipt-brand-sub {
  font-size: 11px;
  color: #78909c;
  margin-top: 2px;
}

.body--dark .receipt-brand-sub {
  color: rgba(255, 255, 255, 0.35);
}

.receipt-title-bar {
  padding: 14px 16px;
  border-bottom: 1px solid rgba(144, 202, 249, 0.2);
  background: rgba(0, 0, 0, 0.02);
  color: #37474f;
}

.body--dark .receipt-title-bar {
  background: rgba(255, 255, 255, 0.03);
  color: #cfd8dc;
  border-color: rgba(255, 255, 255, 0.06);
}

.receipt-info-bar {
  background: rgba(0, 0, 0, 0.03);
  border: 1px solid rgba(144, 202, 249, 0.3);
  border-radius: 8px;
  padding: 14px 16px;
}

.body--dark .receipt-info-bar {
  background: rgba(255, 255, 255, 0.04);
  border-color: rgba(100, 160, 255, 0.15);
}

.receipt-field-label {
  font-size: 10px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  color: #90a4ae;
  margin-bottom: 4px;
}

.receipt-field-mono {
  font-size: 13px;
  font-weight: 700;
  font-family: monospace;
  color: #1565c0;
}

.body--dark .receipt-field-mono {
  color: #90caf9;
}

.receipt-field-value {
  font-size: 13px;
  font-weight: 700;
  color: #212121;
}

.body--dark .receipt-field-value {
  color: #eceff1;
}

.receipt-section-title {
  font-size: 11px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  color: #78909c;
  margin-bottom: 8px;
  padding-bottom: 6px;
  border-bottom: 1px solid rgba(144, 202, 249, 0.25);
}

.body--dark .receipt-section-title {
  color: rgba(255, 255, 255, 0.35);
  border-color: rgba(255, 255, 255, 0.08);
}

.receipt-footer {
  text-align: center;
  padding: 16px;
  border-top: 1px solid rgba(144, 202, 249, 0.25);
  color: #546e7a;
}

.body--dark .receipt-footer {
  border-color: rgba(255, 255, 255, 0.08);
  color: rgba(255, 255, 255, 0.45);
}

/* ── Donations Made — mobile card grid ─────────────────────────── */
.transactions-table {
  :deep(.q-table__grid-content) {
    gap: 10px;
    padding: 4px 0;
  }
}

.donation-mobile-card {
  width: 100%;
  border-radius: 14px;
  border: 1.5px solid rgba(21, 101, 192, 0.16);
  background: rgba(255, 255, 255, 0.88);
  overflow: hidden;
  margin-bottom: 2px;
  box-shadow: 0 1px 4px rgba(21, 101, 192, 0.08);
}

.donation-mobile-card__header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 11px 14px 8px;
  border-bottom: 1.5px solid rgba(21, 101, 192, 0.10);
}

.donation-mobile-card__recipient {
  font-size: 14px;
  font-weight: 700;
  color: #1565c0;
  flex: 1;
  min-width: 0;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.donation-mobile-card__body {
  padding: 8px 14px 6px;
  display: flex;
  flex-direction: column;
  gap: 5px;
}

.donation-mobile-card__row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 8px;
  font-size: 13px;
}

.donation-mobile-card__label {
  color: #78909c;
  font-weight: 500;
  flex-shrink: 0;
  min-width: 64px;
}

.donation-mobile-card__value {
  color: rgba(0, 0, 0, 0.82);
  font-weight: 500;
  text-align: right;
}

.donation-mobile-card__footer {
  display: flex;
  align-items: center;
  justify-content: flex-end;
  gap: 2px;
  padding: 4px 8px 6px;
  border-top: 1.5px solid rgba(21, 101, 192, 0.08);
}

/* Dark mode for mobile cards */
.body--dark .donation-mobile-card {
  background: rgba(18, 26, 52, 0.82);
  border-color: rgba(93, 156, 245, 0.22);
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.25);
}

.body--dark .donation-mobile-card__header {
  border-bottom-color: rgba(93, 156, 245, 0.14);
}

.body--dark .donation-mobile-card__recipient {
  color: #90caf9;
}

.body--dark .donation-mobile-card__label {
  color: rgba(255, 255, 255, 0.45);
}

.body--dark .donation-mobile-card__value {
  color: rgba(255, 255, 255, 0.85);
}

.body--dark .donation-mobile-card__footer {
  border-top-color: rgba(93, 156, 245, 0.10);
}

.recipient-history-txid {
  font-size: 11px;
  color: #1565c0;
  margin-top: 2px;
  font-family: monospace;
  word-break: break-all;
  cursor: pointer;
}

@media (max-width: 600px) {
  .recipient-history-row {
    flex-direction: column;
    gap: 8px;
    padding: 10px 12px;
  }

  .recipient-history-label {
    min-width: 0;
    width: 100%;
  }

  .recipient-history-value {
    width: 100%;
    text-align: left;
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 8px;
    flex-wrap: wrap;
  }

  .recipient-history-badge {
    margin-left: 0 !important;
  }

  .recipient-history-txid {
    font-size: 10px;
    line-height: 1.3;
  }
}
</style>

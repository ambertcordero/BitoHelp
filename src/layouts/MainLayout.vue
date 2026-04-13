<template>
  <q-layout view="lHh Lpr lFf">
    <!-- HEADER ini !!!-->
    <q-header reveal class="app-header">
      <q-toolbar class="q-px-lg">
        <!-- Logo ini !!!-->
        <div class="row items-center">
          <q-avatar size="40px">
            <img src="~assets/CrypToCare.png" />
          </q-avatar>

          <div class="app-title q-ml-sm">CrypToCare</div>
        </div>

        <q-space />

        <div class="nav-menu gt-md">
          <q-btn flat no-caps label="Home" class="nav-item" to="/" />
          <q-btn flat no-caps label="Mission" class="nav-item" to="/mission" />
          <q-btn flat no-caps label="Charities" class="nav-item" to="/charities" />

          <q-btn flat no-caps class="nav-item">
            <div class="row items-center no-wrap">
              <span>Get Involved</span>
              <q-icon name="expand_more" size="20px" class="q-ml-xs" />
            </div>
            <q-menu anchor="bottom left" self="top left">
              <q-list style="min-width: 200px">
                <q-item clickable v-ripple to="/donate">
                  <q-item-section>Donate Now</q-item-section>
                </q-item>
                <q-item clickable v-ripple to="/charities">
                  <q-item-section>Browse Charities</q-item-section>
                </q-item>
                <q-item clickable v-ripple to="/contact">
                  <q-item-section>Partner With Us</q-item-section>
                </q-item>
              </q-list>
            </q-menu>
          </q-btn>

          <q-btn flat no-caps class="nav-item">
            <div class="row items-center no-wrap">
              <span>About</span>
              <q-icon name="expand_more" size="20px" class="q-ml-xs" />
            </div>
            <q-menu anchor="bottom left" self="top left">
              <q-list style="min-width: 200px">
                <q-item clickable v-ripple :to="{ path: '/about', query: { tab: 'story' } }">
                  <q-item-section>Our Story</q-item-section>
                </q-item>
                <q-item clickable v-ripple :to="{ path: '/about', query: { tab: 'team' } }">
                  <q-item-section>Team</q-item-section>
                </q-item>
                <q-item clickable v-ripple :to="{ path: '/about', query: { tab: 'impact' } }">
                  <q-item-section>Impact Report</q-item-section>
                </q-item>
              </q-list>
            </q-menu>
          </q-btn>

          <q-btn flat no-caps label="Contact" class="nav-item" to="/contact" />

          <!-- Network selector -->
          <q-btn flat no-caps class="nav-item">
            <div class="row items-center no-wrap">
              <q-icon name="lan" size="18px" class="q-mr-xs" />
              <span>{{ networkStore.networkLabel }}</span>
              <q-icon name="expand_more" size="20px" class="q-ml-xs" />
            </div>
            <q-menu anchor="bottom left" self="top left">
              <q-list style="min-width: 200px">
                <q-item
                  clickable
                  v-ripple
                  @click="networkStore.switchNetwork('chipnet')"
                  :class="{ 'bg-blue-1': networkStore.isChipnet }"
                >
                  <q-item-section avatar><q-icon name="science" color="blue" /></q-item-section>
                  <q-item-section>Chipnet (Testnet)</q-item-section>
                  <q-item-section side v-if="networkStore.isChipnet"
                    ><q-icon name="check" color="primary"
                  /></q-item-section>
                </q-item>
                <q-item
                  clickable
                  v-ripple
                  @click="confirmMainnetSwitch"
                  :class="{ 'bg-orange-1': networkStore.isMainnet }"
                >
                  <q-item-section avatar
                    ><q-icon name="account_balance" color="orange"
                  /></q-item-section>
                  <q-item-section>Mainnet</q-item-section>
                  <q-item-section side v-if="networkStore.isMainnet"
                    ><q-icon name="check" color="orange"
                  /></q-item-section>
                </q-item>
              </q-list>
            </q-menu>
          </q-btn>
        </div>

        <q-space />

        <!-- Header Action Buttons (notification, dark toggle, hamburger) -->
        <div class="header-actions">
          <!-- Notification Bell -->
          <button
            class="notif-btn"
            :class="{ 'notif-btn--active': unreadCount > 0 }"
            @click="onNotifClick"
            aria-label="Notifications"
          >
            <span class="notif-btn__badge" v-if="unreadCount > 0">{{
              unreadCount > 9 ? '9+' : unreadCount
            }}</span>
            <svg viewBox="0 0 24 24" fill="currentColor" class="notif-btn__icon">
              <path
                d="M12 22c1.1 0 2-.9 2-2h-4c0 1.1.9 2 2 2zm6-6v-5c0-3.07-1.63-5.64-4.5-6.32V4c0-.83-.67-1.5-1.5-1.5s-1.5.67-1.5 1.5v.68C7.64 5.36 6 7.92 6 11v5l-2 2v1h16v-1l-2-2z"
              />
            </svg>
            <!-- Desktop dropdown -->
            <q-menu v-if="$q.screen.gt.xs" class="header-notif-menu">
              <q-list style="min-width: 340px; max-width: 92vw">
                <q-item-label header class="row items-center justify-between q-py-sm">
                  <span class="text-weight-bold text-subtitle2">Notifications</span>
                  <q-btn
                    v-if="notifications.length > 0"
                    flat
                    dense
                    size="xs"
                    label="Clear all"
                    color="primary"
                    @click="clearAllNotifications"
                  />
                </q-item-label>
                <q-separator />
                <div v-if="notifications.length === 0" class="q-pa-xl text-center">
                  <q-icon name="notifications_none" size="40px" color="grey-4" />
                  <div class="text-caption text-grey-5 q-mt-sm">No notifications yet</div>
                </div>
                <q-item
                  v-for="notification in notifications"
                  :key="notification.id"
                  clickable
                  v-ripple
                  @click="markAsRead(notification.id)"
                  :class="{ 'bg-blue-1': !notification.read }"
                >
                  <q-item-section avatar>
                    <q-avatar
                      :icon="notification.isCharity ? 'volunteer_activism' : 'check_circle'"
                      :color="notification.isCharity ? 'green' : 'positive'"
                      text-color="white"
                    />
                  </q-item-section>
                  <q-item-section>
                    <q-item-label class="text-weight-medium">{{ notification.title }}</q-item-label>
                    <q-item-label caption lines="2">{{ notification.message }}</q-item-label>
                    <q-item-label caption class="text-grey-6">{{ notification.time }}</q-item-label>
                  </q-item-section>
                  <q-item-section side>
                    <q-btn
                      flat
                      dense
                      round
                      icon="close"
                      size="sm"
                      @click.stop="removeNotification(notification.id)"
                    />
                  </q-item-section>
                </q-item>
              </q-list>
            </q-menu>
          </button>

          <!-- Dark mode pill toggle switch -->
          <button
            class="dark-toggle"
            :class="{ 'dark-toggle--dark': $q.dark.isActive }"
            @click="$q.dark.toggle()"
            :aria-label="$q.dark.isActive ? 'Switch to light mode' : 'Switch to dark mode'"
            role="switch"
            :aria-checked="String(!$q.dark.isActive)"
          >
            <span class="dark-toggle__knob">
              <!-- Sun: shown when light mode is active (knob on right) -->
              <svg
                v-if="!$q.dark.isActive"
                viewBox="0 0 24 24"
                fill="white"
                class="dark-toggle__icon"
              >
                <path
                  d="M12 7c-2.76 0-5 2.24-5 5s2.24 5 5 5 5-2.24 5-5-2.24-5-5-5zM2 13h2c.55 0 1-.45 1-1s-.45-1-1-1H2c-.55 0-1 .45-1 1s.45 1 1 1zm18 0h2c.55 0 1-.45 1-1s-.45-1-1-1h-2c-.55 0-1 .45-1 1s.45 1 1 1zM11 2v2c0 .55.45 1 1 1s1-.45 1-1V2c0-.55-.45-1-1-1s-1 .45-1 1zm0 18v2c0 .55.45 1 1 1s1-.45 1-1v-2c0-.55-.45-1-1-1s-1 .45-1 1z"
                />
              </svg>
              <!-- Moon: shown when dark mode is active (knob on left) -->
              <svg v-else viewBox="0 0 24 24" fill="white" class="dark-toggle__icon">
                <path
                  d="M12 3c-4.97 0-9 4.03-9 9s4.03 9 9 9 9-4.03 9-9c0-.46-.04-.92-.1-1.36-.98 1.37-2.58 2.26-4.4 2.26-2.98 0-5.4-2.42-5.4-5.4 0-1.81.89-3.42 2.26-4.4-.44-.06-.9-.1-1.36-.1z"
                />
              </svg>
            </span>
          </button>

          <!-- Mobile Menu button — visible on mobile only -->
          <button class="menu-btn lt-md" @click="mobileMenuOpen = true" aria-label="Open menu">
            <svg viewBox="0 0 24 24" fill="currentColor" class="menu-btn__icon">
              <path d="M4 6h16v2H4zm0 5h16v2H4zm0 5h16v2H4z" />
            </svg>
          </button>
        </div>

        <!-- Mobile Notification Bottom Sheet -->
        <q-dialog v-model="notifSheetOpen" position="bottom" full-width>
          <q-card class="notif-sheet">
            <div class="notif-sheet__handle"></div>
            <div
              class="notif-sheet__header row items-center justify-between q-px-md q-pt-sm q-pb-xs"
            >
              <span class="text-weight-bold text-subtitle1">Notifications</span>
              <div class="row items-center gap-xs">
                <q-btn
                  v-if="notifications.length > 0"
                  flat
                  dense
                  size="xs"
                  label="Clear all"
                  color="primary"
                  @click="clearAllNotifications"
                />
                <q-btn flat dense round icon="close" size="sm" @click="notifSheetOpen = false" />
              </div>
            </div>
            <q-separator />
            <div v-if="notifications.length === 0" class="q-pa-xl text-center">
              <q-icon name="notifications_none" size="48px" color="grey-4" />
              <div class="text-body2 text-grey-5 q-mt-sm">No notifications yet</div>
            </div>
            <q-scroll-area style="max-height: 60vh; min-height: 120px">
              <q-list>
                <q-item
                  v-for="notification in notifications"
                  :key="notification.id"
                  clickable
                  v-ripple
                  @click="markAsRead(notification.id); notifSheetOpen = false"
                  :class="{ 'bg-blue-1': !notification.read }"
                >
                  <q-item-section avatar>
                    <q-avatar
                      :icon="notification.isCharity ? 'volunteer_activism' : 'check_circle'"
                      :color="notification.isCharity ? 'green' : 'positive'"
                      text-color="white"
                    />
                  </q-item-section>
                  <q-item-section>
                    <q-item-label class="text-weight-medium">{{ notification.title }}</q-item-label>
                    <q-item-label caption lines="3">{{ notification.message }}</q-item-label>
                    <q-item-label caption class="text-grey-6">{{ notification.time }}</q-item-label>
                  </q-item-section>
                  <q-item-section side>
                    <q-btn
                      flat
                      dense
                      round
                      icon="close"
                      size="sm"
                      @click.stop="removeNotification(notification.id)"
                    />
                  </q-item-section>
                </q-item>
              </q-list>
            </q-scroll-area>
            <!-- safe area for home indicator -->
            <div style="height: env(safe-area-inset-bottom, 12px)"></div>
          </q-card>
        </q-dialog>

        <!-- Wallet Toggle Switch ini !!!-->
        <!-- Hidden on mobile — wallet is accessible via the center bottom-nav button -->
        <div class="topbar__wallet gt-sm">
          <div class="topbar__actions">
            <button
              class="wallet-toggle"
              :class="{
                'wallet-toggle--connected': isConnected,
                'wallet-toggle--pending': isConnecting,
              }"
              @click="handleConnect"
            >
              <span
                class="wallet-toggle__icon"
                :class="walletIconClass"
                @mouseenter="handleIdleIconHover"
              >
                <span
                  v-if="isConnecting"
                  ref="bitcoinLoaderContainer"
                  class="wallet-toggle__lottie wallet-toggle__lottie--loader"
                  aria-hidden="true"
                ></span>

                <img
                  v-else-if="walletIconUrl"
                  :src="walletIconUrl"
                  :alt="walletName"
                  @load="iconLoading = false"
                  @error="iconLoading = false"
                />

                <QSkeleton v-if="iconLoading" type="QAvatar" size="36px" class="wallet-skeleton" />

                <span
                  v-else-if="!walletIconUrl"
                  ref="walletLottieContainer"
                  class="wallet-toggle__lottie"
                  aria-hidden="true"
                ></span>
              </span>

              <span v-if="!isConnected && !isConnecting" class="wallet-toggle__label">
                Connect Wallet
              </span>

              <span v-else-if="isConnected" class="wallet-toggle__info">
                <strong>{{ formattedBalance }}</strong>
                <small>{{ shortAddress }}</small>
              </span>
            </button>
          </div>

          <p v-if="walletError" class="wallet-error">{{ walletError }}</p>
        </div>
      </q-toolbar>

      <!-- Mainnet warning banner -->
      <q-banner
        v-if="networkStore.isMainnet"
        dense
        class="bg-orange text-white text-center text-weight-bold"
        style="min-height: 32px; font-size: 0.85rem"
      >
        <q-icon name="warning" class="q-mr-xs" />
        MAINNET — Real funds at risk. Transactions are irreversible.
      </q-banner>
    </q-header>

    <q-page-container class="has-mobile-nav">
      <router-view />
    </q-page-container>

    <!-- Mobile Bottom Nav ini !!!-->
    <!-- wrapper sits at bottom, provides the floating gap -->
    <div class="mobile-bottom-nav-wrap lt-md">
      <!-- the floating pill -->
      <nav class="mobile-bottom-nav">
        <router-link to="/" class="mobile-nav-item" exact-active-class="mobile-nav-item--active">
          <svg class="mobile-nav-svg" viewBox="0 0 24 24" fill="currentColor">
            <path d="M10 20v-6h4v6h5v-8h3L12 3 2 12h3v8z" />
          </svg>
          <span>Home</span>
        </router-link>

        <router-link to="/charities" class="mobile-nav-item" active-class="mobile-nav-item--active">
          <svg class="mobile-nav-svg" viewBox="0 0 24 24" fill="currentColor">
            <path
              d="M12 21.35l-1.45-1.32C5.4 15.36 2 12.28 2 8.5 2 5.42 4.42 3 7.5 3c1.74 0 3.41.81 4.5 2.09C13.09 3.81 14.76 3 16.5 3 19.58 3 22 5.42 22 8.5c0 3.78-3.4 6.86-8.55 11.54L12 21.35z"
            />
          </svg>
          <span>Charities</span>
        </router-link>

        <!-- Center Wallet Button — pops above the pill -->
        <div class="mobile-nav-wallet">
          <button
            class="mobile-wallet-btn"
            :class="{
              'mobile-wallet-btn--connected': isConnected,
              'mobile-wallet-btn--connecting': isConnecting,
            }"
            @click="handleConnect"
          >
            <svg
              v-if="!isConnected && !isConnecting"
              viewBox="0 0 24 24"
              fill="white"
              width="26"
              height="26"
            >
              <path
                d="M21 18v1a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2v1h-9a2 2 0 0 0-2 2v8a2 2 0 0 0 2 2h9zm-9-2h10V8H12v8zm4-2.5a1.5 1.5 0 1 1 0-3 1.5 1.5 0 0 1 0 3z"
              />
            </svg>
            <q-circular-progress v-else-if="isConnecting" indeterminate size="26px" color="white" />
            <svg v-else viewBox="0 0 24 24" fill="white" width="26" height="26">
              <path d="M9 16.17L4.83 12l-1.42 1.41L9 19 21 7l-1.41-1.41z" />
            </svg>
          </button>
          <span class="mobile-nav-wallet-label">{{ isConnected ? 'Connected' : 'Wallet' }}</span>
        </div>

        <router-link to="/about" class="mobile-nav-item" active-class="mobile-nav-item--active">
          <svg class="mobile-nav-svg" viewBox="0 0 24 24" fill="currentColor">
            <path
              d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm1 15h-2v-6h2v6zm0-8h-2V7h2v2z"
            />
          </svg>
          <span>About</span>
        </router-link>

        <router-link to="/donor" class="mobile-nav-item" active-class="mobile-nav-item--active">
          <svg class="mobile-nav-svg" viewBox="0 0 24 24" fill="currentColor">
            <path
              d="M12 12c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm0 2c-2.67 0-8 1.34-8 4v2h16v-2c0-2.66-5.33-4-8-4z"
            />
          </svg>
          <span>Account</span>
        </router-link>
      </nav>
    </div>

    <!-- Mobile Side Drawer ini !!!-->
    <transition name="mobile-drawer-backdrop">
      <div
        v-if="mobileMenuOpen"
        class="mobile-drawer-backdrop lt-md"
        @click="mobileMenuOpen = false"
      />
    </transition>

    <transition name="mobile-drawer">
      <aside v-if="mobileMenuOpen" class="mobile-drawer lt-md">
        <!-- Drawer Header -->
        <div class="mobile-drawer-header">
          <div class="row items-center no-wrap">
            <q-avatar size="34px" class="q-mr-sm">
              <img src="~assets/CrypToCare.png" />
            </q-avatar>
            <span class="mobile-drawer-brand">CrypToCare</span>
          </div>
          <button
            class="mobile-drawer-close"
            @click="mobileMenuOpen = false"
            aria-label="Close menu"
          >
            <svg viewBox="0 0 24 24" fill="currentColor" width="20" height="20">
              <path
                d="M19 6.41L17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12z"
              />
            </svg>
          </button>
        </div>

        <!-- Wallet Hero Card -->
        <div
          class="mobile-drawer-wallet-card"
          :class="{ 'mobile-drawer-wallet-card--connected': isConnected }"
        >
          <div class="mobile-drawer-wallet-card__inner">
            <div class="mobile-drawer-wallet-card__left">
              <div
                class="mobile-drawer-wallet-status-dot"
                :class="isConnected ? 'dot--on' : 'dot--off'"
              />
              <div>
                <div class="mobile-drawer-wallet-card__label">
                  {{ isConnected ? 'Wallet Connected' : 'Not Connected' }}
                </div>
                <div v-if="isConnected" class="mobile-drawer-wallet-card__balance">
                  {{ formattedBalance }}
                </div>
                <div v-if="isConnected" class="mobile-drawer-wallet-card__addr">
                  {{ shortAddress }}
                </div>
              </div>
            </div>
            <button class="mobile-drawer-wallet-card__btn" @click="handleConnect">
              <svg
                v-if="!isConnected"
                viewBox="0 0 24 24"
                fill="currentColor"
                width="16"
                height="16"
              >
                <path
                  d="M21 18v1a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2v1h-9a2 2 0 0 0-2 2v8a2 2 0 0 0 2 2h9zm-9-2h10V8H12v8zm4-2.5a1.5 1.5 0 1 1 0-3 1.5 1.5 0 0 1 0 3z"
                />
              </svg>
              <svg v-else viewBox="0 0 24 24" fill="currentColor" width="16" height="16">
                <path
                  d="M13 3h-2v10h2V3zm4.83 2.17l-1.42 1.42C17.99 7.86 19 9.81 19 12c0 3.87-3.13 7-7 7s-7-3.13-7-7c0-2.19 1.01-4.14 2.58-5.42L6.17 5.17C4.23 6.82 3 9.26 3 12c0 4.97 4.03 9 9 9s9-4.03 9-9c0-2.74-1.23-5.18-3.17-6.83z"
                />
              </svg>
              <span>{{ isConnected ? 'Disconnect' : 'Connect' }}</span>
            </button>
          </div>
        </div>

        <!-- Nav body -->
        <div class="mobile-drawer-body">
          <div class="mobile-drawer-section-label">Main</div>

          <router-link
            to="/"
            class="mobile-drawer-item"
            exact-active-class="mobile-drawer-item--active"
            @click="mobileMenuOpen = false"
          >
            <div class="mobile-drawer-icon mobile-drawer-icon--blue">
              <svg viewBox="0 0 24 24" fill="currentColor" width="18" height="18">
                <path d="M10 20v-6h4v6h5v-8h3L12 3 2 12h3v8z" />
              </svg>
            </div>
            <span>Home</span>
            <svg class="mobile-drawer-chevron" viewBox="0 0 24 24" fill="currentColor">
              <path d="M8.59 16.59L13.17 12 8.59 7.41 10 6l6 6-6 6z" />
            </svg>
          </router-link>

          <router-link
            to="/mission"
            class="mobile-drawer-item"
            active-class="mobile-drawer-item--active"
            @click="mobileMenuOpen = false"
          >
            <div class="mobile-drawer-icon mobile-drawer-icon--amber">
              <svg viewBox="0 0 24 24" fill="currentColor" width="18" height="18">
                <path
                  d="M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7zm0 9.5c-1.38 0-2.5-1.12-2.5-2.5s1.12-2.5 2.5-2.5 2.5 1.12 2.5 2.5-1.12 2.5-2.5 2.5z"
                />
              </svg>
            </div>
            <span>Mission</span>
            <svg class="mobile-drawer-chevron" viewBox="0 0 24 24" fill="currentColor">
              <path d="M8.59 16.59L13.17 12 8.59 7.41 10 6l6 6-6 6z" />
            </svg>
          </router-link>

          <router-link
            to="/charities"
            class="mobile-drawer-item"
            active-class="mobile-drawer-item--active"
            @click="mobileMenuOpen = false"
          >
            <div class="mobile-drawer-icon mobile-drawer-icon--red">
              <svg viewBox="0 0 24 24" fill="currentColor" width="18" height="18">
                <path
                  d="M12 21.35l-1.45-1.32C5.4 15.36 2 12.28 2 8.5 2 5.42 4.42 3 7.5 3c1.74 0 3.41.81 4.5 2.09C13.09 3.81 14.76 3 16.5 3 19.58 3 22 5.42 22 8.5c0 3.78-3.4 6.86-8.55 11.54L12 21.35z"
                />
              </svg>
            </div>
            <span>Charities</span>
            <svg class="mobile-drawer-chevron" viewBox="0 0 24 24" fill="currentColor">
              <path d="M8.59 16.59L13.17 12 8.59 7.41 10 6l6 6-6 6z" />
            </svg>
          </router-link>

          <div class="mobile-drawer-divider" />
          <div class="mobile-drawer-section-label">Get Involved</div>

          <router-link
            to="/donate"
            class="mobile-drawer-item"
            active-class="mobile-drawer-item--active"
            @click="mobileMenuOpen = false"
          >
            <div class="mobile-drawer-icon mobile-drawer-icon--green">
              <svg viewBox="0 0 24 24" fill="currentColor" width="18" height="18">
                <path
                  d="M11.8 10.9c-2.27-.59-3-1.2-3-2.15 0-1.09 1.01-1.85 2.7-1.85 1.78 0 2.44.85 2.5 2.1h2.21c-.07-1.72-1.12-3.3-3.21-3.81V3h-3v2.16c-1.94.42-3.5 1.68-3.5 3.61 0 2.31 1.91 3.46 4.7 4.13 2.5.6 3 1.48 3 2.41 0 .69-.49 1.79-2.7 1.79-2.06 0-2.87-.92-2.98-2.1h-2.2c.12 2.19 1.76 3.42 3.68 3.83V21h3v-2.15c1.95-.37 3.5-1.5 3.5-3.55 0-2.84-2.43-3.81-4.7-4.4z"
                />
              </svg>
            </div>
            <span>Donate Now</span>
            <svg class="mobile-drawer-chevron" viewBox="0 0 24 24" fill="currentColor">
              <path d="M8.59 16.59L13.17 12 8.59 7.41 10 6l6 6-6 6z" />
            </svg>
          </router-link>

          <router-link
            to="/projects"
            class="mobile-drawer-item"
            active-class="mobile-drawer-item--active"
            @click="mobileMenuOpen = false"
          >
            <div class="mobile-drawer-icon mobile-drawer-icon--purple">
              <svg viewBox="0 0 24 24" fill="currentColor" width="18" height="18">
                <path
                  d="M19 3H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zm-7 3c1.93 0 3.5 1.57 3.5 3.5S13.93 13 12 13s-3.5-1.57-3.5-3.5S10.07 6 12 6zm7 13H5v-.23c0-.62.28-1.2.76-1.58C7.47 15.82 9.64 15 12 15s4.53.82 6.24 2.19c.48.38.76.97.76 1.58V19z"
                />
              </svg>
            </div>
            <span>Projects</span>
            <svg class="mobile-drawer-chevron" viewBox="0 0 24 24" fill="currentColor">
              <path d="M8.59 16.59L13.17 12 8.59 7.41 10 6l6 6-6 6z" />
            </svg>
          </router-link>

          <div class="mobile-drawer-divider" />
          <div class="mobile-drawer-section-label">Company</div>

          <router-link
            to="/about"
            class="mobile-drawer-item"
            active-class="mobile-drawer-item--active"
            @click="mobileMenuOpen = false"
          >
            <div class="mobile-drawer-icon mobile-drawer-icon--teal">
              <svg viewBox="0 0 24 24" fill="currentColor" width="18" height="18">
                <path
                  d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm1 15h-2v-6h2v6zm0-8h-2V7h2v2z"
                />
              </svg>
            </div>
            <span>About Us</span>
            <svg class="mobile-drawer-chevron" viewBox="0 0 24 24" fill="currentColor">
              <path d="M8.59 16.59L13.17 12 8.59 7.41 10 6l6 6-6 6z" />
            </svg>
          </router-link>

          <router-link
            to="/contact"
            class="mobile-drawer-item"
            active-class="mobile-drawer-item--active"
            @click="mobileMenuOpen = false"
          >
            <div class="mobile-drawer-icon mobile-drawer-icon--indigo">
              <svg viewBox="0 0 24 24" fill="currentColor" width="18" height="18">
                <path
                  d="M20 4H4c-1.1 0-2 .9-2 2v12c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V6c0-1.1-.9-2-2-2zm0 4l-8 5-8-5V6l8 5 8-5v2z"
                />
              </svg>
            </div>
            <span>Contact</span>
            <svg class="mobile-drawer-chevron" viewBox="0 0 24 24" fill="currentColor">
              <path d="M8.59 16.59L13.17 12 8.59 7.41 10 6l6 6-6 6z" />
            </svg>
          </router-link>

          <div class="mobile-drawer-divider" />
          <div class="mobile-drawer-section-label">Account</div>

          <router-link
            to="/donor"
            class="mobile-drawer-item"
            active-class="mobile-drawer-item--active"
            @click="mobileMenuOpen = false"
          >
            <div class="mobile-drawer-icon mobile-drawer-icon--blue">
              <svg viewBox="0 0 24 24" fill="currentColor" width="18" height="18">
                <path
                  d="M12 12c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm0 2c-2.67 0-8 1.34-8 4v2h16v-2c0-2.66-5.33-4-8-4z"
                />
              </svg>
            </div>
            <span>My Account</span>
            <svg class="mobile-drawer-chevron" viewBox="0 0 24 24" fill="currentColor">
              <path d="M8.59 16.59L13.17 12 8.59 7.41 10 6l6 6-6 6z" />
            </svg>
          </router-link>

          <div class="mobile-drawer-divider" />
          <div class="mobile-drawer-section-label">Network</div>

          <div class="network-switcher">
            <button
              class="network-card"
              :class="{ 'network-card--active network-card--blue': networkStore.isChipnet }"
              @click="networkStore.switchNetwork('chipnet')"
            >
              <div class="network-card__icon network-card__icon--blue">
                <q-icon name="science" size="20px" />
              </div>
              <div class="network-card__info">
                <span class="network-card__name">Chipnet</span>
                <span class="network-card__sub">Testnet</span>
              </div>
              <span v-if="networkStore.isChipnet" class="network-card__dot network-card__dot--blue" />
            </button>

            <button
              class="network-card"
              :class="{ 'network-card--active network-card--amber': networkStore.isMainnet }"
              @click="confirmMainnetSwitch"
            >
              <div class="network-card__icon network-card__icon--amber">
                <q-icon name="account_balance" size="20px" />
              </div>
              <div class="network-card__info">
                <span class="network-card__name">Mainnet</span>
                <span class="network-card__sub">Live</span>
              </div>
              <span v-if="networkStore.isMainnet" class="network-card__dot network-card__dot--amber" />
            </button>
          </div>
        </div>

        <!-- Drawer Footer -->
        <div class="mobile-drawer-footer">
          <!-- Pill dark-mode toggle -->
          <div class="mobile-drawer-footer__toggle-row">
            <span class="mobile-drawer-footer__toggle-label">{{
              $q.dark.isActive ? 'Dark Mode' : 'Light Mode'
            }}</span>
            <button
              class="drawer-dark-toggle"
              :class="{ 'drawer-dark-toggle--dark': $q.dark.isActive }"
              @click="$q.dark.toggle()"
              :aria-label="$q.dark.isActive ? 'Switch to light mode' : 'Switch to dark mode'"
            >
              <span class="drawer-dark-toggle__knob">
                <svg
                  v-if="!$q.dark.isActive"
                  viewBox="0 0 24 24"
                  fill="white"
                  width="13"
                  height="13"
                >
                  <path
                    d="M12 7c-2.76 0-5 2.24-5 5s2.24 5 5 5 5-2.24 5-5-2.24-5-5-5zM2 13h2c.55 0 1-.45 1-1s-.45-1-1-1H2c-.55 0-1 .45-1 1s.45 1 1 1zm18 0h2c.55 0 1-.45 1-1s-.45-1-1-1h-2c-.55 0-1 .45-1 1s.45 1 1 1zM11 2v2c0 .55.45 1 1 1s1-.45 1-1V2c0-.55-.45-1-1-1s-1 .45-1 1zm0 18v2c0 .55.45 1 1 1s1-.45 1-1v-2c0-.55-.45-1-1-1s-1 .45-1 1z"
                  />
                </svg>
                <svg v-else viewBox="0 0 24 24" fill="white" width="13" height="13">
                  <path
                    d="M12 3c-4.97 0-9 4.03-9 9s4.03 9 9 9 9-4.03 9-9c0-.46-.04-.92-.1-1.36-.98 1.37-2.58 2.26-4.4 2.26-2.98 0-5.4-2.42-5.4-5.4 0-1.81.89-3.42 2.26-4.4-.44-.06-.9-.1-1.36-.1z"
                  />
                </svg>
              </span>
            </button>
          </div>
          <!-- Brand strip -->
          <div class="mobile-drawer-footer__brand">
            <svg viewBox="0 0 24 24" fill="#f7931a" width="14" height="14">
              <path
                d="M23.638 14.904c-1.602 6.43-8.113 10.34-14.542 8.736C2.67 22.05-1.244 15.525.362 9.105 1.962 2.67 8.475-1.243 14.9.358c6.43 1.605 10.342 8.115 8.738 14.546z"
              />
            </svg>
            <span>Developed by ESSU Student</span>
          </div>
        </div>
      </aside>
    </transition>

    <KryptoChatHead />
  </q-layout>
</template>

<script setup>
import { computed, nextTick, onBeforeUnmount, onMounted, ref, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { Core as WalletConnectCore } from '@walletconnect/core'
import SignClient from '@walletconnect/sign-client'
import { WalletConnectModal } from '@walletconnect/modal'
import { QSkeleton } from 'quasar'
import lottie from 'lottie-web'
import { useDonationStore } from '../stores/donation-store'
import { useNetworkStore } from '../stores/network-store'
import { useQuasar } from 'quasar'
import { fetchAddressBalance, normalizeAddress } from '../services/bchChipnet'
import { resumeAllAutoWithdraws } from '../services/vaultDonation'
import KryptoChatHead from '../components/KryptoChatHead.vue'

import logoUrl from '../assets/CrypToCare.png'
import bitcoinIcon from '../../wallets/Bitcoin.ico'
import cashonizeIcon from '../../wallets/Cashonize.ico'
import metamaskIcon from '../../wallets/MetaMask.ico'
import paytacaIcon from '../../wallets/Paytaca.ico'
import walletconnectIcon from '../../wallets/Walletconnect.ico'
import walletLottieJson from '../../lottie/WALLET.json'
import bitcoinLoaderJson from '../../lottie/Bitcoin Loader.json'

const $q = useQuasar()
const router = useRouter()
const route = useRoute()
const donationStore = useDonationStore()
const networkStore = useNetworkStore()

const confirmMainnetSwitch = () => {
  if (networkStore.isMainnet) return
  $q.dialog({
    title: 'Switch to Mainnet?',
    message:
      'You are about to switch to Mainnet. Transactions on Mainnet use REAL Bitcoin Cash and are irreversible. Proceed?',
    cancel: { flat: true, label: 'Stay on Chipnet' },
    ok: { color: 'orange', label: 'Switch to Mainnet' },
    persistent: true,
  }).onOk(() => {
    networkStore.switchNetwork('mainnet')
  })
}

// Mobile side drawer
const mobileMenuOpen = ref(false)
watch(
  () => route.path,
  () => {
    mobileMenuOpen.value = false
  },
)

// Notification sheet (mobile)
const notifSheetOpen = ref(false)

// ── WalletConnect constants ──
const projectId = '1e52dff3b9c75d86cfc7b1190c02d3a0'
//(import.meta.env.VITE_WALLETCONNECT_PROJECT_ID || '1e52dff3b9c75d86cfc7b1190c02d3a0').trim()
// Fixed prefix so the same WalletConnect namespace is used across page reloads,
// allowing session restoration after refresh.
const walletConnectStoragePrefix = 'cryptocare-wc'
const walletConnectRelayUrl = 'wss://relay.walletconnect.com'
const bchChains = computed(() => [networkStore.walletConnectChainId])
const evmChains = ['eip155:1', 'eip155:5', 'eip155:11155111']
const evmNativeSymbols = {
  1: 'ETH',
  10: 'ETH',
  56: 'BNB',
  137: 'MATIC',
  250: 'FTM',
  324: 'ETH',
  42161: 'ETH',
  43114: 'AVAX',
  59144: 'ETH',
  8453: 'ETH',
  5: 'ETH',
  11155111: 'ETH',
}
const evmRpcByChain = {
  'eip155:1': 'https://ethereum-rpc.publicnode.com',
  'eip155:5': 'https://ethereum-goerli-rpc.publicnode.com',
  'eip155:11155111': 'https://rpc.sepolia.org',
}

// ── Wallet reactive state ──
const walletAddress = ref('')
const walletBalance = ref(0)
const bchSessionAddresses = ref([])
const walletError = ref('')
const isConnected = ref(false)
const walletIconUrl = ref('')
const walletName = ref('Wallet')
const walletNamespace = ref('')
const walletChain = ref('')
const iconLoading = ref(false)
const isConnecting = ref(false)
const isBalanceLoading = ref(false)

const walletLottieContainer = ref(null)
const bitcoinLoaderContainer = ref(null)

let signClient
let wcModal
let sessionTopic
let sessionWatchdogTimer
let walletLottieAnimation
let walletLottieTimeout
let bitcoinLoaderAnimation
let unsubscribeModalState
let qrDismissed = false
let balanceRequestNonce = 0
let balanceRetryTimer
let balanceRetryDelay = 0
let walletConnectInitPromise

const WALLETCONNECT_SESSION_PING_TIMEOUT_MS = 30000

const WALLET_CONNECTED_STORAGE_KEY = 'cryptocare.wallet.connected'
const WALLET_NAMESPACE_STORAGE_KEY = 'cryptocare.wallet.namespace'
const WALLET_CONNECTED_EVENT = 'cryptocare:wallet-connection-changed'
const WALLET_SNAPSHOT_STORAGE_KEY = 'cryptocare.wallet.snapshot'
const WALLET_BALANCE_ADJUST_EVENT = 'cryptocare:wallet-balance-adjust'
const WALLET_BALANCE_REFRESH_EVENT = 'cryptocare:wallet-balance-refresh'
const WALLET_CLIENT_GLOBAL_KEY = '__cryptocareWalletClient__'

// ── Sync helpers ──
const syncWalletConnectionState = (connected, namespace = '') => {
  localStorage.setItem(WALLET_CONNECTED_STORAGE_KEY, connected ? '1' : '0')
  if (connected && namespace) {
    localStorage.setItem(WALLET_NAMESPACE_STORAGE_KEY, namespace)
  } else {
    localStorage.removeItem(WALLET_NAMESPACE_STORAGE_KEY)
  }
  window.dispatchEvent(
    new CustomEvent(WALLET_CONNECTED_EVENT, { detail: { connected, namespace } }),
  )
}

const syncWalletSnapshot = () => {
  const snapshot = {
    connected: isConnected.value,
    namespace: walletNamespace.value,
    chain: walletChain.value,
    address: walletAddress.value,
    balance: Number(walletBalance.value || 0),
    symbol: walletSymbol.value,
    updatedAt: Date.now(),
  }
  localStorage.setItem(WALLET_SNAPSHOT_STORAGE_KEY, JSON.stringify(snapshot))
  window.dispatchEvent(new CustomEvent(WALLET_CONNECTED_EVENT, { detail: snapshot }))
}

const syncWalletClientBridge = () => {
  if (
    !isConnected.value ||
    !signClient ||
    !sessionTopic ||
    !walletChain.value ||
    !walletNamespace.value ||
    !walletAddress.value
  ) {
    delete window[WALLET_CLIENT_GLOBAL_KEY]
    return
  }

  const session = getWalletConnectSession(sessionTopic)
  const activeTopic = sessionTopic

  const waitForRequestSent = (method, timeoutMs = 5000) =>
    new Promise((resolve) => {
      if (!signClient) {
        resolve(null)
        return
      }
      let settled = false
      let timeoutId
      const cleanup = () => {
        if (timeoutId) window.clearTimeout(timeoutId)
        signClient.off('session_request_sent', handleSent)
      }
      const resolveOnce = (value) => {
        if (settled) return
        settled = true
        cleanup()
        resolve(value)
      }
      const handleSent = (event) => {
        if (event?.topic !== activeTopic || event?.request?.method !== method) return
        resolveOnce({
          id: event.id,
          topic: event.topic,
          chainId: event.chainId,
          request: event.request,
        })
      }
      timeoutId = window.setTimeout(() => resolveOnce(null), timeoutMs)
      signClient.on('session_request_sent', handleSent)
    })

  const getHistoryRecord = async (id) => {
    if (!signClient || id === undefined || id === null) return null
    try {
      return await signClient.core.history.get(activeTopic, id)
    } catch {
      return null
    }
  }

  const getPendingHistory = () => {
    try {
      const pending = signClient?.core?.history?.pending || []
      return pending.filter((entry) => entry?.topic === activeTopic)
    } catch {
      return []
    }
  }

  window[WALLET_CLIENT_GLOBAL_KEY] = {
    namespace: walletNamespace.value,
    chain: walletChain.value,
    address: walletAddress.value,
    topic: activeTopic,
    session,
    ping: () => signClient.ping({ topic: activeTopic }),
    waitForRequestSent,
    getHistoryRecord,
    getPendingHistory,
    request: (payload) => {
      if (walletNamespace.value === 'bch') getWalletConnectSession(activeTopic)
      return signClient.request({ topic: activeTopic, ...payload })
    },
  }
}

// ── Balance event handlers ──
const handleWalletBalanceAdjust = (event) => {
  if (!isConnected.value) return
  const delta = Number(event?.detail?.delta)
  if (!Number.isFinite(delta) || delta === 0) return
  const targetChain = event?.detail?.chain
  const targetAddress = event?.detail?.address
  if (targetChain && targetChain !== walletChain.value) return
  if (
    targetAddress &&
    normalizeAddressForComparison(targetAddress, targetChain || walletChain.value) !==
      normalizeAddressForComparison(walletAddress.value, walletChain.value)
  )
    return
  walletBalance.value = Math.max(0, walletBalance.value + delta)
}

const handleWalletBalanceRefresh = (event) => {
  if (!isConnected.value || !walletAddress.value || !walletChain.value) return
  const targetChain = event?.detail?.chain
  const targetAddress = event?.detail?.address
  if (targetChain && targetChain !== walletChain.value) return
  if (
    targetAddress &&
    normalizeAddressForComparison(targetAddress, targetChain || walletChain.value) !==
      normalizeAddressForComparison(walletAddress.value, walletChain.value)
  )
    return
  fetchBalance(walletAddress.value, walletChain.value)
}

// ── Lottie animations ──
const destroyWalletLottie = () => {
  if (walletLottieTimeout) {
    window.clearTimeout(walletLottieTimeout)
    walletLottieTimeout = undefined
  }
  if (walletLottieAnimation) {
    walletLottieAnimation.destroy()
    walletLottieAnimation = undefined
  }
}
const destroyBitcoinLoader = () => {
  if (bitcoinLoaderAnimation) {
    bitcoinLoaderAnimation.destroy()
    bitcoinLoaderAnimation = undefined
  }
}
const initWalletLottie = () => {
  if (!walletLottieContainer.value || walletLottieAnimation) return
  walletLottieAnimation = lottie.loadAnimation({
    container: walletLottieContainer.value,
    renderer: 'svg',
    loop: false,
    autoplay: false,
    animationData: walletLottieJson,
    rendererSettings: { preserveAspectRatio: 'xMidYMid slice' },
  })
  walletLottieAnimation.goToAndStop(0, true)
}
const initBitcoinLoader = () => {
  if (!bitcoinLoaderContainer.value || bitcoinLoaderAnimation) return
  bitcoinLoaderAnimation = lottie.loadAnimation({
    container: bitcoinLoaderContainer.value,
    renderer: 'svg',
    loop: true,
    autoplay: true,
    animationData: bitcoinLoaderJson,
    rendererSettings: { preserveAspectRatio: 'xMidYMid meet' },
  })
}
const handleIdleIconHover = () => {
  if (isConnected.value || walletIconUrl.value || iconLoading.value) return
  initWalletLottie()
  if (!walletLottieAnimation) return
  if (walletLottieTimeout) window.clearTimeout(walletLottieTimeout)
  walletLottieAnimation.goToAndStop(0, true)
  walletLottieAnimation.play()
  walletLottieTimeout = window.setTimeout(() => {
    walletLottieAnimation?.goToAndStop(0, true)
    walletLottieTimeout = undefined
  }, 1000)
}

// ── Balance retry ──
const clearBalanceRetry = () => {
  if (balanceRetryTimer) {
    window.clearTimeout(balanceRetryTimer)
    balanceRetryTimer = undefined
  }
  balanceRetryDelay = 0
}
const scheduleBalanceRetry = () => {
  clearBalanceRetry()
  if (!isConnected.value || !walletAddress.value) return
  balanceRetryDelay = Math.min((balanceRetryDelay || 15000) * 2, 60000)
  if (balanceRetryDelay === 0) balanceRetryDelay = 15000
  balanceRetryTimer = window.setTimeout(() => {
    balanceRetryTimer = undefined
    if (isConnected.value && walletAddress.value)
      fetchBalance(walletAddress.value, walletChain.value)
  }, balanceRetryDelay)
}

// ── Reset state ──
const stopSessionWatchdog = () => {
  if (sessionWatchdogTimer) {
    clearInterval(sessionWatchdogTimer)
    sessionWatchdogTimer = undefined
  }
}

const startSessionWatchdog = (topic) => {
  stopSessionWatchdog()
  sessionWatchdogTimer = setInterval(() => {
    if (!isConnected.value || !signClient || !topic) return
    // Local session store check — the SDK removes the session when it processes
    // a session_delete / session_expire event. This catches cases where the
    // event was processed silently (e.g. on reconnect) without firing our handler.
    try {
      signClient.session.get(topic)
    } catch {
      resetWalletState()
    }
  }, 20000)
}

const resetWalletState = () => {
  stopSessionWatchdog()
  clearBalanceRetry()
  isConnected.value = false
  isConnecting.value = false
  walletAddress.value = ''
  walletBalance.value = 0
  bchSessionAddresses.value = []
  walletIconUrl.value = ''
  walletName.value = 'Wallet'
  walletNamespace.value = ''
  walletChain.value = ''
  isBalanceLoading.value = false
  iconLoading.value = false
  sessionTopic = undefined
  delete window[WALLET_CLIENT_GLOBAL_KEY]
  destroyBitcoinLoader()
}

const handleQrClosed = () => {
  if (!isConnecting.value || isConnected.value) return
  qrDismissed = true
  wcModal?.closeModal()
  resetWalletState()
}

// ── Computed properties ──
const shortAddress = computed(() => {
  if (!walletAddress.value) return ''
  const display =
    walletNamespace.value === 'bch' && walletAddress.value.includes(':')
      ? walletAddress.value.slice(walletAddress.value.indexOf(':') + 1)
      : walletAddress.value
  return `${display.slice(0, 6)}...${display.slice(-4)}`
})

const walletSymbol = computed(() => {
  if (walletNamespace.value === 'bch') return networkStore.isChipnet ? 'tBCH' : 'BCH'
  if (walletNamespace.value === 'eip155') {
    const chainNumber = walletChain.value.split(':')[1] || ''
    return evmNativeSymbols[chainNumber] || 'NATIVE'
  }
  return 'COIN'
})

const formatBchDisplay = (value) => {
  const floored = Math.floor(value * 1000) / 1000
  return floored
    .toFixed(3)
    .replace(/(\.\d*[1-9])0+$/, '$1')
    .replace(/\.0+$/, '.0')
}

const formattedBalance = computed(() => {
  if (!isConnected.value) return '0.000'
  if (isBalanceLoading.value) return `Loading ${walletSymbol.value}...`
  if (walletNamespace.value === 'bch')
    return `${formatBchDisplay(walletBalance.value)} ${walletSymbol.value}`
  return `${walletBalance.value.toFixed(4)} ${walletSymbol.value}`
})

const walletIconClass = computed(() =>
  isConnected.value ? 'wallet-toggle__icon--connected' : 'wallet-toggle__icon--idle',
)

// ── BCH address parsing ──
const parseBchAccount = (account) => {
  if (!account || !account.startsWith('bch:')) return ''
  const parts = account.split(':')
  if (parts.length >= 4 && parts[2] === 'bchtest')
    return `${parts[2]}:${parts.slice(3).join(':')}`.toLowerCase()
  if (parts.length >= 3 && parts[1] === 'bchtest')
    return `${parts[1]}:${parts.slice(2).join(':')}`.toLowerCase()
  if (parts.length >= 3 && parts[1] === 'chipnet') {
    const addressPart = parts.slice(2).join(':')
    if (addressPart.startsWith('bchtest:')) return addressPart.toLowerCase()
    return `bchtest:${addressPart}`.toLowerCase()
  }
  const addressPart = parts[parts.length - 1]
  if (addressPart && !addressPart.includes(':')) return `bchtest:${addressPart}`.toLowerCase()
  return addressPart.toLowerCase()
}

const parseBchChainFromAccount = (account) => {
  if (!account || !account.startsWith('bch:')) return ''
  const parts = account.split(':')
  if (parts.length < 2) return ''
  return networkStore.walletConnectChainId
}

const hasSupportedNamespace = (session) => {
  const namespaces = session?.namespaces || {}
  return Boolean(namespaces?.bch?.accounts?.length || namespaces?.eip155?.accounts?.length)
}
const hasBchNamespace = (session) => Boolean(session?.namespaces?.bch?.accounts?.length)

const sanitizeWalletConnectSession = (session) => {
  if (!session || !hasBchNamespace(session)) return session
  const peerMetadata = session.peer?.metadata || {}
  const redirect = peerMetadata.redirect || {}
  const sessionConfig = session.sessionConfig || {}
  if (session.transportType !== 'relay') {
    session.transportType = 'relay'
  }
  if (sessionConfig.disableDeepLink !== true) {
    session.sessionConfig = { ...sessionConfig, disableDeepLink: true }
  }
  if (redirect.linkMode || redirect.universal || redirect.native) {
    session.peer = {
      ...session.peer,
      metadata: {
        ...peerMetadata,
        redirect: { ...redirect, linkMode: false, universal: '', native: '' },
      },
    }
  }
  return session
}

const getWalletConnectSession = (topic = sessionTopic) => {
  if (!signClient || !topic) return null
  try {
    return sanitizeWalletConnectSession(signClient.session.get(topic))
  } catch {
    return null
  }
}

const pickStoredSession = (sessions) => {
  if (!Array.isArray(sessions) || sessions.length === 0) return null
  const nowSeconds = Math.floor(Date.now() / 1000)
  const activeSessions = sessions.filter((s) => Number(s?.expiry || 0) > nowSeconds)
  const supportedSessions = activeSessions.filter(hasSupportedNamespace)
  const rankedSessions = (supportedSessions.length ? supportedSessions : activeSessions).slice()
  if (rankedSessions.length === 0) return null
  rankedSessions.sort((l, r) => Number(r?.expiry || 0) - Number(l?.expiry || 0))
  return sanitizeWalletConnectSession(rankedSessions[0] || null)
}

const pingWalletConnectSession = async (
  topic,
  timeoutMs = WALLETCONNECT_SESSION_PING_TIMEOUT_MS,
) => {
  if (!signClient || !topic) return false
  try {
    await Promise.race([
      signClient.ping({ topic }),
      new Promise((_, reject) =>
        window.setTimeout(() => reject(new Error('ping timed out')), timeoutMs),
      ),
    ])
    return true
  } catch {
    return false
  }
}

const getStoredPairings = () => {
  try {
    return signClient?.pairing?.getAll?.() || []
  } catch {
    return []
  }
}

const cleanupInactivePairings = async ({ deletePairings = false } = {}) => {
  if (!signClient) return
  const inactivePairings = getStoredPairings().filter((p) => !p?.active)
  if (inactivePairings.length === 0) return
  for (const pairing of inactivePairings) {
    const topic = pairing?.topic
    if (!topic) continue
    try {
      if (deletePairings) await signClient.core.pairing.disconnect({ topic })
      else await signClient.core.relayer.subscriber.unsubscribe(topic)
    } catch {
      /* best effort */
    }
  }
}

const restartWalletConnectTransport = async () => {
  try {
    await signClient?.core?.relayer?.restartTransport?.()
  } catch {
    /* best effort */
  }
}

const purgeAllWalletConnectStorage = () => {
  if (typeof window === 'undefined') return
  try {
    const keysToDelete = []
    for (let i = 0; i < localStorage.length; i++) {
      const key = localStorage.key(i)
      if (key && (key.includes('wc@2') || key.startsWith('cryptocare-'))) {
        keysToDelete.push(key)
      }
    }
    keysToDelete.forEach((key) => localStorage.removeItem(key))
  } catch {
    /* best effort */
  }
}

const disposeWalletConnectClient = async (purgeStorage = false) => {
  if (signClient) {
    try {
      await disconnectAllWalletConnectSessions()
    } catch {
      /* best effort */
    }
    try {
      await signClient?.core?.relayer?.transportClose?.()
    } catch {
      /* optional */
    }
  }
  // Do NOT set signClient = undefined — the WalletConnectCore singleton
  // cannot be re-initialised in the same page lifetime without triggering
  // "Core is already initialized" and relay decryption failures.
  // We keep the client alive and just purge sessions/pairings instead.
  walletConnectInitPromise = undefined
  // Only purge localStorage when fully tearing down (page unmount),
  // not during reconnect — wiping keys while signClient is alive causes
  // "failed to process inbound message" errors for stale relay messages.
  if (purgeStorage) purgeAllWalletConnectStorage()
}

const disconnectAllWalletConnectSessions = async () => {
  if (!signClient) return
  const sessions = signClient.session.getAll()
  for (const session of sessions) {
    const topic = session?.topic
    if (!topic) continue
    try {
      await signClient.disconnect({ topic, reason: { code: 6000, message: 'User disconnected' } })
    } catch {
      /* best effort */
    }
  }
}

const waitForRelayConnected = async (timeoutMs = 5000) => {
  if (!signClient?.core?.relayer) return
  const relayer = signClient.core.relayer
  if (relayer.connected) return
  await new Promise((resolve) => {
    const timer = setTimeout(resolve, timeoutMs)
    const check = () => {
      if (relayer.connected) {
        clearTimeout(timer)
        resolve()
      }
    }
    relayer.on?.('relayer_connect', () => {
      clearTimeout(timer)
      resolve()
    })
    // Poll as fallback in case the event doesn't fire
    const poll = setInterval(() => {
      if (relayer.connected) {
        clearInterval(poll)
        clearTimeout(timer)
        resolve()
      }
    }, 200)
    setTimeout(() => clearInterval(poll), timeoutMs)
    check()
  })
}

const getWalletConnectFriendlyError = (error) => {
  const rawMessage = String(error?.message || error || '').trim()
  const normalized = rawMessage.toLowerCase()
  if (
    normalized.includes('projectid') ||
    normalized.includes('project id') ||
    normalized.includes('unauthorized') ||
    normalized.includes('forbidden') ||
    normalized.includes('401')
  ) {
    return 'WalletConnect project ID was rejected by the relay. Check VITE_WALLETCONNECT_PROJECT_ID and allowed origins in WalletConnect Cloud.'
  }
  if (
    normalized.includes('websocket') ||
    normalized.includes('relay') ||
    normalized.includes('network') ||
    normalized.includes('transport') ||
    normalized.includes('timeout')
  ) {
    return 'WalletConnect relay is currently unreachable. Check internet/firewall and try again.'
  }
  return rawMessage || 'Wallet connection failed. Please try again.'
}

const prepareFreshWalletConnectConnection = async () => {
  if (!signClient) return
  await disconnectAllWalletConnectSessions()
  await cleanupInactivePairings({ deletePairings: true })
  await restartWalletConnectTransport()
  await waitForRelayConnected()
}

const parseAccount = (account) => {
  if (!account) return ''
  if (account.startsWith('bch:')) return parseBchAccount(account)
  const parts = account.split(':')
  return parts[parts.length - 1] || ''
}

function normalizeAddressForComparison(address, chainId) {
  const raw = String(address || '').trim()
  if (!raw) return ''
  if ((chainId || '').startsWith('bch:')) return normalizeAddress(raw) || raw.toLowerCase()
  return raw.toLowerCase()
}

const nativeDecimalToWei = (value) => {
  const normalized = String(value ?? '').trim()
  if (!normalized) return 0n
  const [integerRaw, fractionRaw = ''] = normalized.split('.')
  const integerPart = integerRaw || '0'
  const paddedFraction = (fractionRaw + '0'.repeat(18)).slice(0, 18)
  return BigInt(integerPart) * 10n ** 18n + BigInt(paddedFraction)
}

const parseBalanceWei = (rawBalance, options = {}) => {
  const { assumeNativeForPlainDecimal = false } = options
  if (typeof rawBalance === 'bigint') return rawBalance
  if (typeof rawBalance === 'number') {
    if (!Number.isFinite(rawBalance) || rawBalance < 0) return 0n
    if (assumeNativeForPlainDecimal) return nativeDecimalToWei(rawBalance.toString())
    return BigInt(Math.trunc(rawBalance))
  }
  if (rawBalance && typeof rawBalance === 'object') {
    const nested = rawBalance.result ?? rawBalance.balance ?? rawBalance.value
    if (nested !== undefined) return parseBalanceWei(nested, options)
    return 0n
  }
  if (typeof rawBalance !== 'string') return 0n
  const value = rawBalance.trim()
  if (!value) return 0n
  if (value.startsWith('0x') || value.startsWith('0X')) return BigInt(value)
  if (assumeNativeForPlainDecimal && /^\d+(\.\d+)?$/.test(value)) return nativeDecimalToWei(value)
  return BigInt(value)
}

const weiToNative = (wei) => Number(wei) / 1e18

const fetchEvmBalanceFromRpc = async (chainId, address) => {
  const rpcUrl = evmRpcByChain[chainId]
  if (!rpcUrl) throw new Error('Unsupported EVM chain RPC')
  const response = await fetch(rpcUrl, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      id: Date.now(),
      jsonrpc: '2.0',
      method: 'eth_getBalance',
      params: [address, 'latest'],
    }),
  })
  if (!response.ok) throw new Error('RPC balance request failed')
  const data = await response.json()
  if (data?.error) throw new Error(data.error?.message || 'RPC returned an error')
  return { rpcUrl, rawWei: data?.result, wei: parseBalanceWei(data?.result) }
}

const parseChainFromAccount = (account) => {
  if (!account) return ''
  if (account.startsWith('bch:')) return parseBchChainFromAccount(account)
  const parts = account.split(':')
  if (parts.length < 2) return ''
  return `${parts[0]}:${parts[1]}`
}

const normalizeEvmChainId = (value) => {
  if (typeof value === 'number' && Number.isFinite(value)) return `eip155:${Math.trunc(value)}`
  if (typeof value !== 'string') return ''
  const normalized = value.trim().toLowerCase()
  if (!normalized) return ''
  if (normalized.startsWith('eip155:')) return normalized
  if (normalized.startsWith('0x')) {
    const chainNumber = Number.parseInt(normalized, 16)
    if (Number.isFinite(chainNumber)) return `eip155:${chainNumber}`
    return ''
  }
  if (/^\d+$/.test(normalized)) return `eip155:${normalized}`
  return ''
}

const selectPreferredAccount = (accounts, preferredChains) => {
  if (!Array.isArray(accounts) || !accounts.length) return ''
  const matched = accounts.find((a) => preferredChains.includes(parseChainFromAccount(a)))
  return matched || accounts[0]
}

const resolveWalletIcon = (name) => {
  const key = (name || '').toLowerCase()
  if (key.includes('react wallet v2')) return walletconnectIcon
  if (key.includes('walletconnect')) return walletconnectIcon
  if (key.includes('paytaca')) return paytacaIcon
  if (key.includes('cashonize')) return cashonizeIcon
  if (key.includes('metamask')) return metamaskIcon
  if (key.includes('bitcoin')) return bitcoinIcon
  return ''
}

// ── Session → state ──
const updateFromSession = (session) => {
  const sanitized = sanitizeWalletConnectSession(session)
  const bchNs = sanitized.namespaces.bch
  const evmNs = sanitized.namespaces.eip155
  let namespaceKey = ''
  let account = ''
  let chain = ''

  if (bchNs?.accounts?.length) {
    namespaceKey = 'bch'
    account = selectPreferredAccount(bchNs.accounts, bchChains.value)
    chain = parseChainFromAccount(account)
    const allNormalized = bchNs.accounts
      .map((a) => normalizeAddress(parseBchAccount(a)))
      .filter(Boolean)
    bchSessionAddresses.value = [...new Set(allNormalized)]
    if (import.meta.env.DEV) {
      console.info('[CrypToCare][bch-session]', {
        topic: sanitized.topic,
        transportType: sanitized.transportType || null,
        sessionConfig: sanitized.sessionConfig || null,
        peerRedirect: sanitized.peer?.metadata?.redirect || null,
        rawAccount: account,
        parsedChain: chain,
        allBchAccounts: bchNs.accounts,
        resolvedAddresses: bchSessionAddresses.value,
      })
    }
  } else if (evmNs?.accounts?.length) {
    namespaceKey = 'eip155'
    account = selectPreferredAccount(evmNs.accounts, evmChains)
    chain = parseChainFromAccount(account)
    if (import.meta.env.DEV) {
      console.info('[CrypToCare][evm-session]', {
        rawAccount: account,
        parsedChain: chain,
        allEvmAccounts: evmNs.accounts,
      })
    }
  }

  if (!account) {
    walletError.value = 'No supported accounts found in the session.'
    return
  }

  walletNamespace.value = namespaceKey
  walletChain.value = chain
  const parsedAddress = parseAccount(account)

  if (namespaceKey === 'bch') {
    const normalized = normalizeAddress(parsedAddress)
    if (!normalized) {
      if (import.meta.env.DEV)
        console.error('[CrypToCare][bch-session] Invalid address', {
          rawAccount: account,
          parsedAddress,
        })
      walletError.value = `Invalid BCH address format: ${parsedAddress}`
      return
    }
    if (import.meta.env.DEV)
      console.info('[CrypToCare][bch-session] Address normalized', {
        raw: parsedAddress,
        normalized,
      })
    walletAddress.value = normalized
  } else {
    walletAddress.value = parsedAddress
  }

  const metadata = sanitized.peer?.metadata
  walletName.value = metadata?.name || 'Wallet'
  walletIconUrl.value = resolveWalletIcon(walletName.value) || metadata?.icons?.[0] || ''
  iconLoading.value = Boolean(walletIconUrl.value)
  fetchBalance(walletAddress.value, walletChain.value)
}

// ── Fetch balance ──
const logWalletBalanceDebug = (stage, details) => {
  if (!import.meta.env.DEV) return
  console.info('[CrypToCare][wallet-balance]', stage, details)
}

const fetchBalance = async (address, chainId = walletChain.value) => {
  const requestNonce = ++balanceRequestNonce
  const finishLoading = () => {
    if (requestNonce === balanceRequestNonce) isBalanceLoading.value = false
  }
  const setBalanceSafely = (next) => {
    if (requestNonce === balanceRequestNonce) walletBalance.value = next
  }
  if (!address) {
    setBalanceSafely(0)
    finishLoading()
    return
  }
  isBalanceLoading.value = true
  logWalletBalanceDebug('request:start', {
    account: address,
    chainId,
    rpc: evmRpcByChain[chainId] || null,
    walletName: walletName.value,
  })
  try {
    if (walletNamespace.value === 'eip155') {
      const isReactWalletV2 = (walletName.value || '').toLowerCase().includes('react wallet v2')
      try {
        if (!signClient || !sessionTopic) throw new Error('No active session')
        const balanceResult = await signClient.request({
          topic: sessionTopic,
          chainId,
          request: { method: 'eth_getBalance', params: [address, 'latest'] },
        })
        logWalletBalanceDebug('walletconnect:response', {
          account: address,
          chainId,
          rawWei: balanceResult,
        })
        const walletBalanceWei = parseBalanceWei(balanceResult, {
          assumeNativeForPlainDecimal: isReactWalletV2,
        })
        try {
          const rpcBalance = await fetchEvmBalanceFromRpc(chainId, address)
          logWalletBalanceDebug('rpc:response', {
            account: address,
            chainId,
            rpc: rpcBalance.rpcUrl,
            rawWei: rpcBalance.rawWei,
          })
          setBalanceSafely(
            weiToNative(rpcBalance.wei > walletBalanceWei ? rpcBalance.wei : walletBalanceWei),
          )
        } catch {
          setBalanceSafely(weiToNative(walletBalanceWei))
        }
      } catch {
        const rpcBalance = await fetchEvmBalanceFromRpc(chainId, address)
        logWalletBalanceDebug('rpc:response:fallback', {
          account: address,
          chainId,
          rpc: rpcBalance.rpcUrl,
          rawWei: rpcBalance.rawWei,
        })
        setBalanceSafely(weiToNative(rpcBalance.wei))
      }
    } else {
      const primaryNorm = normalizeAddress(address)
      const addressList =
        bchSessionAddresses.value.length > 0
          ? bchSessionAddresses.value
          : primaryNorm
            ? [primaryNorm]
            : []
      if (addressList.length === 0) {
        walletError.value = `Cannot fetch BCH balance — unrecognised address: "${address}"`
        setBalanceSafely(0)
        finishLoading()
        return
      }
      console.info('[CrypToCare][bch-balance] fetching all addresses', { addressList })
      let totalBalance = 0
      let firstBalanceError = ''
      for (const addr of addressList) {
        try {
          const chipnetBal = await fetchAddressBalance({ address: addr })
          console.info('[CrypToCare][bch-balance] chipnet result', {
            address: addr,
            balance: chipnetBal,
          })
          totalBalance += chipnetBal
        } catch (e) {
          if (!firstBalanceError) firstBalanceError = String(e?.message || e || '')
        }
      }
      console.info('[CrypToCare][bch-balance] total', { totalBalance, addresses: addressList })
      if (totalBalance === 0 && firstBalanceError) {
        walletError.value = /provider unavailable/i.test(firstBalanceError)
          ? 'BCH balance service temporarily unavailable — retrying...'
          : firstBalanceError
        scheduleBalanceRetry()
      } else {
        walletError.value = ''
        clearBalanceRetry()
      }
      setBalanceSafely(totalBalance)
    }
  } catch (err) {
    logWalletBalanceDebug('error', {
      account: address,
      chainId,
      error: String(err?.message || err),
    })
    if (walletNamespace.value !== 'eip155') {
      walletError.value = /provider unavailable/i.test(String(err?.message || ''))
        ? 'BCH balance service temporarily unavailable — retrying...'
        : `Balance fetch failed: ${err?.message || err}`
      scheduleBalanceRetry()
    }
  } finally {
    finishLoading()
  }
}

// ── Init WalletConnect ──
const initWalletConnect = async () => {
  if (signClient) return
  if (walletConnectInitPromise) {
    await walletConnectInitPromise
    return
  }

  walletConnectInitPromise = (async () => {
    const core = new WalletConnectCore({
      projectId,
      customStoragePrefix: walletConnectStoragePrefix,
      relayUrl: walletConnectRelayUrl,
      telemetryEnabled: false,
    })

    signClient = await SignClient.init({
      core,
      projectId,
      relayUrl: walletConnectRelayUrl,
      telemetryEnabled: false,
      metadata: {
        name: 'CrypToCare',
        description: 'Periodic donations on Bitcoin Cash.',
        url: window.location.origin,
        icons: [logoUrl],
      },
    })

    await cleanupInactivePairings()

    wcModal = new WalletConnectModal({ projectId, themeMode: 'light' })

    if (typeof wcModal.subscribeModal === 'function') {
      unsubscribeModalState = wcModal.subscribeModal((modalState) => {
        if (!modalState?.open) handleQrClosed()
      })
    }

    signClient.on('session_delete', ({ topic }) => {
      if (!sessionTopic || topic === sessionTopic) resetWalletState()
    })

    signClient.on('session_expire', ({ topic }) => {
      if (!sessionTopic || topic === sessionTopic) resetWalletState()
    })

    signClient.on('session_event', ({ topic, params }) => {
      if (!sessionTopic || topic !== sessionTopic) return
      if (params?.event?.name === 'accountsChanged') {
        const accounts = params?.event?.data
        if (Array.isArray(accounts) && accounts.length > 0) {
          const account = accounts[0]
          const accountChain = parseChainFromAccount(account)
          if (accountChain) walletChain.value = accountChain
          const parsedAddress = parseAccount(account)
          if (walletNamespace.value === 'bch') {
            const normalized = normalizeAddress(parsedAddress)
            if (!normalized) {
              walletError.value = `Invalid BCH address: ${parsedAddress}`
              resetWalletState()
              return
            }
            walletAddress.value = normalized
          } else {
            walletAddress.value = parsedAddress
          }
          fetchBalance(walletAddress.value, walletChain.value)
        } else {
          resetWalletState()
        }
        return
      }
      if (params?.event?.name === 'chainChanged') {
        const data = params?.event?.data
        const nextChain = normalizeEvmChainId(
          Array.isArray(data) ? data[0] : (data?.chainId ?? data),
        )
        if (nextChain) walletChain.value = nextChain
        if (walletAddress.value) fetchBalance(walletAddress.value, walletChain.value)
      }
    })

    signClient.on('session_update', ({ topic, params }) => {
      if (!sessionTopic || topic !== sessionTopic) return
      const activeSession = getWalletConnectSession(topic)
      updateFromSession({
        topic,
        namespaces: params.namespaces,
        transportType: activeSession?.transportType,
        sessionConfig: activeSession?.sessionConfig,
        peer: {
          metadata: {
            name: walletName.value,
            icons: walletIconUrl.value ? [walletIconUrl.value] : [],
            redirect: activeSession?.peer?.metadata?.redirect,
          },
        },
      })
    })

    const existingSessions = signClient.session.getAll()
    const session = pickStoredSession(existingSessions)
    if (session) {
      // Optimistic restore: set connected immediately so the UI shows the
      // wallet on refresh without waiting for a relay ping (which can fail
      // if the relay hasn't connected yet on cold load).
      const restoredTopic = session.topic
      sessionTopic = restoredTopic
      isConnected.value = true
      updateFromSession(session)
      startSessionWatchdog(restoredTopic)

      // Verify relay in the background. If unreachable, restart the transport
      // but keep the session — only the wallet or user should trigger a disconnect.
      pingWalletConnectSession(restoredTopic).then((isReachable) => {
        if (!isReachable && sessionTopic === restoredTopic) {
          cleanupInactivePairings({ deletePairings: true })
          restartWalletConnectTransport()
        }
      })
    }
  })()

  try {
    await walletConnectInitPromise
  } finally {
    walletConnectInitPromise = undefined
  }
}

// ── Connect / disconnect toggle ──
const handleConnect = async () => {
  walletError.value = ''
  qrDismissed = false

  if (isConnected.value && sessionTopic) {
    const topicToDisconnect = sessionTopic
    // Reset UI immediately so the user sees it disconnect instantly
    resetWalletState()
    // Best-effort: tell the relay to close the session.
    // We reset first so a relay error doesn't leave the UI stuck "connected".
    try {
      if (signClient) {
        await signClient.disconnect({
          topic: topicToDisconnect,
          reason: { code: 6000, message: 'User disconnected' },
        })
      }
    } catch {
      /* session may already be gone on relay side — ignore */
    }
    return
  }

  try {
    isConnecting.value = true
    await disposeWalletConnectClient()
    await initWalletConnect()
    if (!signClient) throw new Error('WalletConnect client failed to initialize.')
    await prepareFreshWalletConnectConnection()
    let connection
    try {
      connection = await signClient.connect({
        optionalNamespaces: {
          bch: {
            methods: ['bch_signMessage', 'bch_signTransaction', 'bch_sendTransaction'],
            chains: bchChains.value,
            events: [],
          },
        },
      })
    } catch {
      try {
        connection = await signClient.connect({
          optionalNamespaces: {
            bch: {
              methods: ['bch_signMessage', 'bch_signTransaction', 'bch_sendTransaction'],
              chains: bchChains.value,
              events: [],
            },
            eip155: {
              methods: ['eth_getBalance', 'eth_sign', 'personal_sign', 'eth_sendTransaction'],
              chains: evmChains,
              events: ['accountsChanged', 'chainChanged'],
            },
          },
        })
      } catch {
        connection = await signClient.connect({
          optionalNamespaces: {
            eip155: {
              methods: ['eth_getBalance', 'eth_sign', 'personal_sign', 'eth_sendTransaction'],
              chains: evmChains,
              events: ['accountsChanged', 'chainChanged'],
            },
          },
        })
      }
    }
    const { uri, approval } = connection
    if (uri) wcModal.openModal({ uri })
    const session = sanitizeWalletConnectSession(await approval())
    qrDismissed = false
    wcModal.closeModal()
    sessionTopic = session.topic
    isConnecting.value = false
    isConnected.value = true
    updateFromSession(session)
    startSessionWatchdog(session.topic)
  } catch (error) {
    const wasDismissed = qrDismissed
    qrDismissed = false
    isConnecting.value = false
    destroyBitcoinLoader()
    if (import.meta.env.DEV) {
      console.error('[CrypToCare][walletconnect] connection failed', error)
    }
    if (!wasDismissed) walletError.value = getWalletConnectFriendlyError(error)
    wcModal?.closeModal()
  }
}

// ── Notification system ──
const CHARITY_WALLET = 'bitcoincash:qp3wjpa3tjlj042z2wv7hahsldgwhwy0rq9sywjpyy'
const notifications = ref([])
const unreadCount = computed(() => notifications.value.filter((n) => !n.read).length)
const lastCheckedId = ref(null)

watch(
  () => donationStore.latestDonation,
  (newDonation, oldDonation) => {
    if (newDonation && newDonation !== oldDonation) {
      if (newDonation.recipient === CHARITY_WALLET) {
        addCharityNotification({
          title: 'New Donation Received!',
          message: `Received ${newDonation.amount} BCH for ${newDonation.cause}`,
          txid: newDonation.txid,
          amount: newDonation.amount,
          cause: newDonation.cause,
          isCharity: true,
        })
      } else {
        addNotification({
          title: 'Donation Successful!',
          message: `Your donation of ${newDonation.amount} BCH to ${newDonation.cause} was sent successfully.`,
          txid: newDonation.txid,
          isCharity: false,
        })
      }
    }
  },
)

let pollInterval = null

async function checkForNewDonations() {
  try {
    await donationStore.fetchDonations(10)
    const donations = donationStore.donationHistory
    const charityDonations = donations.filter((d) => d.recipient === CHARITY_WALLET)
    if (charityDonations.length > 0) {
      const latestDonation = charityDonations[0]
      if (lastCheckedId.value !== latestDonation.id) {
        lastCheckedId.value = latestDonation.id
        addCharityNotification({
          title: 'New Donation Received!',
          message: `Received ${latestDonation.amount} BCH for ${latestDonation.cause}`,
          txid: latestDonation.txid,
          amount: latestDonation.amount,
          cause: latestDonation.cause,
          donorName: latestDonation.donor_name || 'Anonymous',
          isCharity: true,
        })
      }
    }
  } catch (error) {
    console.error('Error checking for new donations:', error)
  }
}

function addNotification(data) {
  notifications.value.unshift({
    id: Date.now(),
    title: data.title,
    message: data.message,
    time: new Date().toLocaleTimeString(),
    read: false,
    txid: data.txid,
    isCharity: data.isCharity || false,
  })
  if (notifications.value.length > 20) notifications.value = notifications.value.slice(0, 20)
}

function addCharityNotification(data) {
  notifications.value.unshift({
    id: Date.now(),
    title: data.title,
    message: data.message,
    time: new Date().toLocaleTimeString(),
    read: false,
    txid: data.txid,
    amount: data.amount,
    cause: data.cause,
    donorName: data.donorName,
    isCharity: true,
  })
  if (notifications.value.length > 20) notifications.value = notifications.value.slice(0, 20)
  $q.notify({
    type: 'positive',
    message: 'New Donation Received!',
    caption: `${data.amount} BCH for ${data.cause}`,
    position: 'top-right',
    timeout: 5000,
    actions: [
      {
        label: 'View',
        color: 'white',
        handler: () => {
          router.push('/dashboard')
        },
      },
    ],
  })
}

function onNotifClick() {
  toggleNotifications()
  if ($q.screen.lt.sm) notifSheetOpen.value = true
}
function toggleNotifications() {
  notifications.value.forEach((n) => (n.read = true))
}
function markAsRead(id) {
  const n = notifications.value.find((n) => n.id === id)
  if (n) {
    n.read = true
    if (n.isCharity) router.push('/dashboard')
  }
}
function removeNotification(id) {
  const i = notifications.value.findIndex((n) => n.id === id)
  if (i > -1) notifications.value.splice(i, 1)
}
function clearAllNotifications() {
  notifications.value = []
}

// ── Lifecycle ──
onMounted(() => {
  initWalletLottie()
  initWalletConnect().catch((error) => {
    if (import.meta.env.DEV) {
      console.error('[CrypToCare][walletconnect] init failed', error)
    }
    walletError.value = getWalletConnectFriendlyError(error)
  })
  window.addEventListener(WALLET_BALANCE_ADJUST_EVENT, handleWalletBalanceAdjust)
  window.addEventListener(WALLET_BALANCE_REFRESH_EVENT, handleWalletBalanceRefresh)
  pollInterval = setInterval(checkForNewDonations, 30000)
  checkForNewDonations()
  // Resume auto-withdraw timers for all active vaults from previous sessions
  resumeAllAutoWithdraws((cycle) => {
    if (import.meta.env.DEV) {
      console.info('[CrypToCare][vault-autowithdraw:cycle]', cycle)
    }
  })
})

watch(
  () => [isConnected.value, walletNamespace.value],
  async ([connected]) => {
    syncWalletConnectionState(connected, walletNamespace.value)
    if (connected) {
      destroyWalletLottie()
      return
    }
    await nextTick()
    initWalletLottie()
  },
)

watch(
  () => [
    isConnected.value,
    walletNamespace.value,
    walletChain.value,
    walletAddress.value,
    walletBalance.value,
    walletSymbol.value,
  ],
  () => {
    syncWalletSnapshot()
    syncWalletClientBridge()
  },
)

watch(
  () => isConnecting.value,
  async (connecting) => {
    if (connecting) {
      destroyWalletLottie()
      await nextTick()
      initBitcoinLoader()
      return
    }
    destroyBitcoinLoader()
    if (!isConnected.value && !walletIconUrl.value) {
      await nextTick()
      initWalletLottie()
    }
  },
)

onBeforeUnmount(() => {
  window.removeEventListener(WALLET_BALANCE_ADJUST_EVENT, handleWalletBalanceAdjust)
  window.removeEventListener(WALLET_BALANCE_REFRESH_EVENT, handleWalletBalanceRefresh)
  if (typeof unsubscribeModalState === 'function') unsubscribeModalState()
  clearBalanceRetry()
  stopSessionWatchdog()
  void disposeWalletConnectClient(true)
  destroyWalletLottie()
  destroyBitcoinLoader()
  if (pollInterval) clearInterval(pollInterval)
})
</script>

<style scoped>
.nav-menu {
  display: flex;
  align-items: center;
  gap: 8px;
}

.nav-item {
  font-size: 15px;
  font-weight: 500;
  color: #333;
  padding: 8px 16px;
  transition: color 0.2s ease;
}

.nav-item:hover {
  color: #1976d2;
}

.app-title {
  font-size: 20px;
  font-weight: 700;
  color: #333;
}

.app-header {
  background: rgba(255, 255, 255, 0.55);
  backdrop-filter: blur(20px) saturate(180%);
  -webkit-backdrop-filter: blur(20px) saturate(180%);
  color: #333;
  border-bottom: 1px solid rgba(255, 255, 255, 0.7);
  box-shadow: 0 4px 24px rgba(30, 40, 80, 0.08);
}

/* ── Header Action Buttons (notification / dark-toggle / hamburger) ─────── */
.header-actions {
  display: flex;
  align-items: center;
  gap: 2px;
}

.header-action-btn {
  position: relative;
  width: 40px;
  height: 40px;
  border-radius: 12px;
  border: 1.5px solid transparent;
  background: transparent;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  color: #555;
  transition:
    background 0.18s ease,
    color 0.18s ease,
    border-color 0.18s ease,
    transform 0.18s cubic-bezier(0.34, 1.56, 0.64, 1);
  -webkit-tap-highlight-color: transparent;
  outline: none;
}

.header-action-btn:hover {
  background: rgba(46, 88, 216, 0.08);
  border-color: rgba(46, 88, 216, 0.18);
  color: #2e58d8;
  transform: translateY(-2px);
}

.header-action-btn:active {
  transform: scale(0.88) translateY(0);
  transition-duration: 0.08s;
  background: rgba(46, 88, 216, 0.14);
}

.header-action-btn--active {
  color: #2e58d8;
  background: rgba(46, 88, 216, 0.06);
}

.header-action-icon {
  width: 20px;
  height: 20px;
  flex-shrink: 0;
  transition: transform 0.22s cubic-bezier(0.34, 1.56, 0.64, 1);
}

.header-action-btn:hover .header-action-icon {
  transform: scale(1.15);
}

.header-action-btn__badge {
  position: absolute;
  top: 4px;
  right: 4px;
  min-width: 16px;
  height: 16px;
  border-radius: 8px;
  background: #ef5350;
  color: #fff;
  font-size: 9px;
  font-weight: 700;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 0 3px;
  line-height: 1;
  pointer-events: none;
  box-shadow: 0 0 0 2px rgba(255, 255, 255, 0.9);
}

.header-notif-menu {
  border-radius: 16px !important;
  overflow: hidden;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.14) !important;
}

/* ── Mobile Notification Bottom Sheet ─────────────────────────────────── */
.notif-sheet {
  border-radius: 20px 20px 0 0 !important;
  overflow: hidden;
}

.notif-sheet__handle {
  width: 36px;
  height: 4px;
  border-radius: 2px;
  background: rgba(0, 0, 0, 0.15);
  margin: 10px auto 6px;
}

.notif-sheet__header {
  min-height: 48px;
}

.body--dark .notif-sheet {
  background: #1a1d2e;
}

.body--dark .notif-sheet__handle {
  background: rgba(255, 255, 255, 0.2);
}

/* ── Pill Dark-Mode Toggle Switch ──────────────────────────────────────── */
.dark-toggle {
  position: relative;
  width: 66px;
  height: 36px;
  border-radius: 999px;
  background: rgba(255, 255, 255, 0.55);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  border: 1.5px solid rgba(255, 255, 255, 0.75);
  cursor: pointer;
  padding: 0;
  flex-shrink: 0;
  outline: none;
  -webkit-tap-highlight-color: transparent;
  box-shadow:
    0 2px 8px rgba(30, 40, 80, 0.1),
    inset 0 1px 0 rgba(255, 255, 255, 0.8);
  transition:
    background 0.28s ease,
    border-color 0.28s ease,
    box-shadow 0.18s ease;
}

.dark-toggle:hover {
  background: rgba(255, 255, 255, 0.72);
  box-shadow:
    0 4px 16px rgba(46, 88, 216, 0.14),
    inset 0 1px 0 rgba(255, 255, 255, 0.9);
  border-color: rgba(255, 255, 255, 0.9);
}

.dark-toggle__knob {
  position: absolute;
  top: 3px;
  left: 3px;
  width: 28px;
  height: 28px;
  border-radius: 50%;
  background: #00c59a;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 2px 6px rgba(0, 197, 154, 0.45);
  transition:
    transform 0.32s cubic-bezier(0.34, 1.56, 0.64, 1),
    background 0.28s ease,
    box-shadow 0.28s ease;
}

/* Light mode (dark is OFF) → knob slides to right, teal */
.dark-toggle:not(.dark-toggle--dark) .dark-toggle__knob {
  transform: translateX(30px);
  background: #00c59a;
  box-shadow: 0 2px 7px rgba(0, 197, 154, 0.5);
}

/* Dark mode (dark is ON) → knob stays left, indigo */
.dark-toggle--dark .dark-toggle__knob {
  transform: translateX(0);
  background: #5c6bc0;
  box-shadow: 0 2px 7px rgba(92, 107, 192, 0.5);
}

.dark-toggle__icon {
  width: 15px;
  height: 15px;
  flex-shrink: 0;
}

/* ── Rounded Card Notification Button ─────────────────────────────────── */
.notif-btn {
  position: relative;
  width: 44px;
  height: 44px;
  border-radius: 13px;
  background: transparent;
  backdrop-filter: none;
  -webkit-backdrop-filter: none;
  border: none;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  color: #3a3f4b;
  box-shadow: none;
  transition:
    background 0.18s ease,
    transform 0.18s cubic-bezier(0.34, 1.56, 0.64, 1),
    color 0.18s ease;
  -webkit-tap-highlight-color: transparent;
  outline: none;
  flex-shrink: 0;
}

.notif-btn:hover {
  background: rgba(46, 88, 216, 0.08);
  color: #2e58d8;
  transform: translateY(-1px);
}

.notif-btn:active {
  transform: scale(0.9);
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.08);
  transition-duration: 0.08s;
}

.notif-btn--active {
  color: #2e58d8;
}

.notif-btn__icon {
  width: 20px;
  height: 20px;
  flex-shrink: 0;
}

.notif-btn__badge {
  position: absolute;
  top: 6px;
  right: 6px;
  min-width: 16px;
  height: 16px;
  border-radius: 8px;
  background: #ef5350;
  color: #fff;
  font-size: 9px;
  font-weight: 700;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 0 3px;
  line-height: 1;
  pointer-events: none;
  box-shadow: none;
}

/* ── Rounded Card Menu Button ──────────────────────────────────────────── */
.menu-btn {
  width: 44px;
  height: 44px;
  border-radius: 13px;
  background: rgba(255, 255, 255, 0.55);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  border: 1.5px solid rgba(255, 255, 255, 0.75);
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  color: #3a3f4b;
  box-shadow:
    0 2px 8px rgba(30, 40, 80, 0.1),
    inset 0 1px 0 rgba(255, 255, 255, 0.8);
  transition:
    background 0.18s ease,
    box-shadow 0.18s ease,
    transform 0.18s cubic-bezier(0.34, 1.56, 0.64, 1),
    border-color 0.18s ease;
  -webkit-tap-highlight-color: transparent;
  outline: none;
  flex-shrink: 0;
}

.menu-btn:hover {
  background: rgba(255, 255, 255, 0.72);
  border-color: rgba(255, 255, 255, 0.9);
  box-shadow:
    0 4px 16px rgba(46, 88, 216, 0.22),
    0 8px 32px rgba(30, 40, 80, 0.18),
    inset 0 1px 0 rgba(255, 255, 255, 0.9);
  transform: translateY(-1px);
}

.menu-btn:active {
  transform: scale(0.9);
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.08);
  transition-duration: 0.08s;
}

.menu-btn__icon {
  width: 20px;
  height: 20px;
  flex-shrink: 0;
}

/* Dark mode overrides */
.body--dark .app-header {
  background: rgba(15, 17, 28, 0.65);
  backdrop-filter: blur(20px) saturate(180%);
  -webkit-backdrop-filter: blur(20px) saturate(180%);
  color: #e0e0e0;
  border-bottom: 1px solid rgba(255, 255, 255, 0.07);
  box-shadow: 0 4px 24px rgba(0, 0, 0, 0.35);
}

.body--dark .app-title {
  color: #e8eaf6;
}

.body--dark .nav-item {
  color: rgba(220, 225, 245, 0.82) !important;
}

.body--dark .nav-item:hover {
  color: #90caf9 !important;
  background: rgba(130, 177, 255, 0.08) !important;
}

/* Quasar router-link active class on q-btn */
.body--dark .nav-item.router-link-active,
.body--dark .nav-item.router-link-exact-active {
  color: #82b1ff !important;
}

.body--dark .header-action-btn {
  color: rgba(200, 210, 240, 0.7);
}

.body--dark .header-action-btn:hover {
  background: rgba(130, 177, 255, 0.1);
  border-color: rgba(130, 177, 255, 0.2);
  color: #82b1ff;
}

.body--dark .header-action-btn--active {
  color: #82b1ff;
  background: rgba(130, 177, 255, 0.08);
}

.body--dark .header-action-btn__badge {
  box-shadow: 0 0 0 2px rgba(24, 26, 36, 0.9);
}

.body--dark .dark-toggle {
  background: rgba(255, 255, 255, 0.07);
  border-color: rgba(255, 255, 255, 0.12);
  box-shadow:
    0 2px 8px rgba(0, 0, 0, 0.3),
    inset 0 1px 0 rgba(255, 255, 255, 0.08);
}

.body--dark .dark-toggle:hover {
  background: rgba(255, 255, 255, 0.12);
  border-color: rgba(255, 255, 255, 0.22);
  box-shadow:
    0 4px 16px rgba(0, 0, 0, 0.35),
    inset 0 1px 0 rgba(255, 255, 255, 0.1);
}

.body--dark .dark-toggle:hover {
  border-color: rgba(255, 255, 255, 0.2);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.35);
}

.body--dark .menu-btn {
  background: rgba(255, 255, 255, 0.07);
  border-color: rgba(255, 255, 255, 0.12);
  color: rgba(210, 218, 245, 0.85);
  box-shadow:
    0 2px 8px rgba(0, 0, 0, 0.4),
    0 6px 24px rgba(0, 0, 0, 0.3),
    inset 0 1px 0 rgba(255, 255, 255, 0.08);
}

.body--dark .menu-btn:hover {
  background: rgba(255, 255, 255, 0.12);
  border-color: rgba(255, 255, 255, 0.22);
  box-shadow:
    0 4px 16px rgba(0, 0, 0, 0.5),
    0 8px 32px rgba(0, 0, 0, 0.35),
    inset 0 1px 0 rgba(255, 255, 255, 0.1);
}

.body--dark .notif-btn {
  background: transparent;
  border: none;
  color: rgba(210, 218, 245, 0.75);
  box-shadow: none;
}

.body--dark .notif-btn:hover {
  background: rgba(130, 177, 255, 0.1);
  color: #82b1ff;
}

.body--dark .notif-btn--active {
  border-color: rgba(239, 83, 80, 0.5);
  box-shadow: 0 1px 6px rgba(239, 83, 80, 0.25);
}

.body--dark .notif-btn__badge {
  box-shadow: 0 0 0 2px rgba(24, 26, 36, 0.9);
}

/* Wallet Toggle Switch */
.topbar__wallet {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  gap: 0.25rem;
}

.topbar__actions {
  display: flex;
  align-items: center;
  gap: 0.8rem;
}

.wallet-toggle {
  position: relative;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 0.3rem 0.7rem 0.3rem 3.2rem;
  border-radius: 999px;
  border: none;
  background: #2e58d8;
  color: #ffffff;
  font-weight: 700;
  font-size: 0.95rem;
  cursor: pointer;
  width: 200px;
  min-height: 48px;
  text-align: center;
  transition: background-color 0.24s ease;
}

.wallet-toggle__icon {
  position: absolute;
  left: 4px;
  top: 50%;
  transform: translateY(-50%);
  width: 40px;
  height: 40px;
  border-radius: 50%;
  display: grid;
  place-items: center;
  background: #1eb5ce;
  font-size: 1rem;
  font-weight: 700;
  color: #ffffff;
  flex: 0 0 auto;
  z-index: 2;
  overflow: hidden;
  transition:
    left 0.24s cubic-bezier(0.4, 0, 0.2, 1),
    background-color 0.24s ease;
}

.wallet-toggle__icon--connected {
  background: #1c9b7e;
}

.wallet-toggle__icon img {
  width: 70%;
  height: 70%;
  object-fit: contain;
}

.wallet-toggle__lottie {
  width: 100%;
  height: 50%;
  display: block;
  transform: translateY(3px) translateX(1px) scale(4);
  transform-origin: center;
}

.wallet-toggle__lottie svg {
  width: 100% !important;
  height: 100% !important;
  display: block;
}

.wallet-toggle__lottie--loader {
  width: 94%;
  height: 94%;
  transform: none;
}

.wallet-skeleton {
  position: absolute;
  inset: 4px;
  border-radius: 50%;
}

.wallet-toggle__label {
  letter-spacing: 0.02em;
  display: inline-block;
  width: 100%;
  text-align: center;
  padding-right: 0.4rem;
}

.wallet-toggle__info {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  line-height: 1.1;
  width: 100%;
  text-align: center;
  padding-right: 0.3rem;
}

.wallet-toggle__info strong {
  font-size: 1.05rem;
}

.wallet-toggle__info small {
  font-size: 0.75rem;
  opacity: 0.9;
}

.wallet-toggle--connected {
  background: #8cc84a;
  color: #ffffff;
  padding: 0.3rem 3.2rem 0.3rem 0.7rem;
}

.wallet-toggle--connected .wallet-toggle__icon {
  left: calc(100% - 44px);
  background: #1aa6c3;
}

.wallet-toggle--pending {
  padding: 0.3rem 0.7rem;
}

.wallet-toggle--pending .wallet-toggle__icon {
  left: calc(50% - 20px);
}

.wallet-error {
  color: #d32f2f;
  font-weight: 600;
  font-size: 0.75rem;
  margin: 0;
}

@media (max-width: 1024px) {
  .nav-menu {
    display: none;
  }

  .wallet-toggle {
    width: 160px;
    min-height: 40px;
    font-size: 0.8rem;
    padding: 0.25rem 0.5rem 0.25rem 2.6rem;
  }

  .wallet-toggle__icon {
    width: 32px;
    height: 32px;
  }

  .wallet-toggle--connected {
    padding: 0.25rem 2.6rem 0.25rem 0.5rem;
  }

  .wallet-toggle--connected .wallet-toggle__icon {
    left: calc(100% - 36px);
  }

  .wallet-toggle--pending .wallet-toggle__icon {
    left: calc(50% - 16px);
  }
}

/* ── Mobile Bottom Navigation ── */
.has-mobile-nav {
  padding-bottom: 0;
}

@media (max-width: 1023px) {
  .has-mobile-nav {
    /* pill height 64 + 12 bottom gap + 18 wallet overflow */
    padding-bottom: 96px;
  }
}

/* outer wrapper — full-width, sits fixed at bottom, transparent */
.mobile-bottom-nav-wrap {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  z-index: 2000;
  /* extra top padding so the floating wallet button isn't clipped */
  padding: 20px 16px 12px;
  pointer-events: none;
}

/* the floating pill */
.mobile-bottom-nav {
  pointer-events: all;
  display: flex;
  align-items: center;
  justify-content: space-around;
  height: 62px;
  border-radius: 32px;
  /* glassmorphism light */
  background: rgba(255, 255, 255, 0.553);
  backdrop-filter: blur(24px) saturate(180%);
  -webkit-backdrop-filter: blur(24px) saturate(180%);
  border: 1px solid rgba(255, 255, 255, 0.5);
  box-shadow:
    0 8px 32px rgba(0, 0, 0, 0.12),
    0 2px 8px rgba(0, 0, 0, 0.06);
  padding: 0 12px;
  overflow: visible;
}

.body--dark .mobile-bottom-nav {
  /* glassmorphism dark */
  background: rgba(20, 20, 34, 0.75);
  backdrop-filter: blur(24px) saturate(160%);
  -webkit-backdrop-filter: blur(24px) saturate(160%);
  border: 1px solid rgba(255, 255, 255, 0.08);
  box-shadow:
    0 8px 32px rgba(0, 0, 0, 0.45),
    0 2px 8px rgba(0, 0, 0, 0.3);
}

.mobile-nav-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 3px;
  flex: 1;
  text-decoration: none;
  color: rgba(90, 90, 110, 0.65);
  font-size: 10px;
  font-weight: 500;
  padding: 6px 0;
  position: relative;
  -webkit-tap-highlight-color: transparent;
  transition: color 0.2s;
}

/* Pill highlight — springs in on hover, stays for active */
.mobile-nav-item::before {
  content: '';
  position: absolute;
  top: 5px;
  left: 50%;
  transform: translateX(-50%) scale(0.5);
  opacity: 0;
  width: 44px;
  height: 30px;
  border-radius: 14px;
  background: rgba(21, 101, 192, 0.1);
  transition:
    transform 0.28s cubic-bezier(0.34, 1.56, 0.64, 1),
    opacity 0.18s ease;
  pointer-events: none;
}

.mobile-nav-item:hover::before {
  transform: translateX(-50%) scale(1);
  opacity: 1;
}

.mobile-nav-item--active::before {
  transform: translateX(-50%) scale(1);
  opacity: 1;
  background: rgba(21, 101, 192, 0.14);
}

/* Active dot indicator at bottom of icon */
.mobile-nav-item--active::after {
  content: '';
  position: absolute;
  bottom: 4px;
  left: 50%;
  transform: translateX(-50%) scale(1);
  width: 4px;
  height: 4px;
  border-radius: 50%;
  background: #1565c0;
  transition: transform 0.2s cubic-bezier(0.34, 1.56, 0.64, 1);
}

.mobile-nav-svg {
  width: 22px;
  height: 22px;
  flex-shrink: 0;
  transition: transform 0.28s cubic-bezier(0.34, 1.56, 0.64, 1);
}

/* Icon lifts and pops on hover */
.mobile-nav-item:hover .mobile-nav-svg {
  transform: scale(1.22) translateY(-2px);
}

/* Press down feedback */
.mobile-nav-item:active .mobile-nav-svg {
  transform: scale(0.88) translateY(0);
  transition-duration: 0.08s;
}

/* Label lifts subtly on hover */
.mobile-nav-item span {
  display: block;
  transition:
    transform 0.2s ease,
    color 0.2s;
}

.mobile-nav-item:hover span {
  transform: translateY(-1px);
  color: rgba(90, 90, 110, 0.9);
}

.mobile-nav-item--active {
  color: #1565c0;
}

.mobile-nav-item--active .q-icon {
  color: #1565c0;
}

.body--dark .mobile-nav-item {
  color: rgba(160, 160, 190, 0.5);
}

.body--dark .mobile-nav-item::before {
  background: rgba(130, 177, 255, 0.1);
}

.body--dark .mobile-nav-item--active::before {
  background: rgba(130, 177, 255, 0.15);
}

.body--dark .mobile-nav-item--active::after {
  background: #82b1ff;
}

.body--dark .mobile-nav-item:hover span {
  color: rgba(160, 160, 190, 0.9);
}

.body--dark .mobile-nav-item--active {
  color: #82b1ff;
}

.body--dark .mobile-nav-item--active .q-icon {
  color: #82b1ff;
}

/* Center wallet — floats above the pill */
.mobile-nav-wallet {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 3px;
  flex: 1;
  position: relative;
  /* shift up so the circle pops above the pill edge */
  margin-top: -28px;
}

.mobile-wallet-btn {
  width: 56px;
  height: 56px;
  border-radius: 50%;
  background: linear-gradient(145deg, #1976d2, #0d47a1);
  border: none;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  box-shadow: 0 6px 20px rgba(21, 101, 192, 0.55);
  transition:
    background 0.2s,
    transform 0.22s cubic-bezier(0.34, 1.56, 0.64, 1),
    box-shadow 0.22s ease;
  /* white ring like the Paytaca style */
  outline: 3px solid rgba(255, 255, 255, 0.8);
  -webkit-tap-highlight-color: transparent;
}

.body--dark .mobile-wallet-btn {
  outline: 3px solid rgba(30, 30, 50, 0.9);
}

.mobile-wallet-btn:hover {
  transform: scale(1.1) translateY(-3px);
  box-shadow: 0 14px 30px rgba(21, 101, 192, 0.72);
}

.mobile-wallet-btn:active {
  transform: scale(0.92) translateY(0);
  transition-duration: 0.08s;
}

.mobile-wallet-btn--connected {
  background: linear-gradient(145deg, #43a047, #1b5e20);
  box-shadow: 0 6px 20px rgba(46, 125, 50, 0.55);
}

.mobile-wallet-btn--connected:hover {
  box-shadow: 0 14px 30px rgba(46, 125, 50, 0.72);
}

.mobile-wallet-btn--connecting {
  background: linear-gradient(145deg, #fb8c00, #bf360c);
  box-shadow: 0 6px 20px rgba(230, 81, 0, 0.55);
}

.mobile-nav-wallet-label {
  font-size: 10px;
  font-weight: 500;
  color: rgba(90, 90, 110, 0.65);
  margin-top: 2px;
}

.body--dark .mobile-nav-wallet-label {
  color: rgba(160, 160, 190, 0.5);
}

/* ── Mobile Menu button (replaces Account) ───────────────────── */
.mobile-nav-menu-btn {
  background: none;
  border: none;
  cursor: pointer;
  -webkit-tap-highlight-color: transparent;
}

/* ── Mobile Side Drawer ──────────────────────────────────────── */

/* Backdrop */
.mobile-drawer-backdrop {
  position: fixed;
  inset: 0;
  z-index: 3000;
  background: rgba(0, 0, 0, 0.45);
  backdrop-filter: blur(3px);
  -webkit-backdrop-filter: blur(3px);
}

.mobile-drawer-backdrop-enter-active,
.mobile-drawer-backdrop-leave-active {
  transition: opacity 0.25s ease;
}
.mobile-drawer-backdrop-enter-from,
.mobile-drawer-backdrop-leave-to {
  opacity: 0;
}

/* Drawer panel */
/* ═══════════════════════════════════════════════════════════════
   MOBILE SIDE DRAWER
═══════════════════════════════════════════════════════════════ */

/* 1. Glassmorphism + rounded left edge */
.mobile-drawer {
  position: fixed;
  top: 0;
  right: 0;
  bottom: 0;
  z-index: 3001;
  width: min(310px, 86vw);
  display: flex;
  flex-direction: column;
  background: rgba(255, 255, 255, 0.72);
  backdrop-filter: blur(24px) saturate(180%);
  -webkit-backdrop-filter: blur(24px) saturate(180%);
  border-left: 1px solid rgba(255, 255, 255, 0.7);
  border-radius: 5px 0 0 5px;
  box-shadow:
    -4px 0 12px rgba(0, 0, 0, 0.08),
    -16px 0 64px rgba(30, 40, 80, 0.35),
    -32px 0 80px rgba(30, 40, 80, 0.18);
  overflow: hidden;
}

/* 6. Spring slide animation */
.mobile-drawer-enter-active {
  transition: transform 0.38s cubic-bezier(0.34, 1.56, 0.64, 1);
}
.mobile-drawer-leave-active {
  transition: transform 0.26s cubic-bezier(0.4, 0, 0.2, 1);
}
.mobile-drawer-enter-from,
.mobile-drawer-leave-to {
  transform: translateX(100%);
}

/* ── Header ─────────────────────────────────────────────────── */
.mobile-drawer-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 18px 16px 14px;
  border-bottom: 1px solid rgba(0, 0, 0, 0.06);
  flex-shrink: 0;
}

.mobile-drawer-brand {
  font-size: 17px;
  font-weight: 800;
  color: #0d1738;
  letter-spacing: -0.3px;
}

.mobile-drawer-close {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  border: none;
  background: rgba(0, 0, 0, 0.06);
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  color: #555;
  transition:
    background 0.18s,
    transform 0.28s cubic-bezier(0.34, 1.56, 0.64, 1);
  -webkit-tap-highlight-color: transparent;
}

.mobile-drawer-close:hover {
  background: rgba(0, 0, 0, 0.11);
  transform: rotate(90deg) scale(1.1);
}

/* ── 2. Wallet Hero Card ─────────────────────────────────────── */
.mobile-drawer-wallet-card {
  margin: 10px 12px;
  border-radius: 16px;
  background: linear-gradient(135deg, rgba(239, 83, 80, 0.12) 0%, rgba(239, 83, 80, 0.06) 100%);
  border: 1px solid rgba(239, 83, 80, 0.18);
  flex-shrink: 0;
  overflow: hidden;
  transition:
    background 0.3s,
    border-color 0.3s;
}

.mobile-drawer-wallet-card--connected {
  background: linear-gradient(135deg, rgba(0, 197, 154, 0.14) 0%, rgba(46, 88, 216, 0.08) 100%);
  border-color: rgba(0, 197, 154, 0.25);
}

.mobile-drawer-wallet-card__inner {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 12px 14px;
  gap: 10px;
}

.mobile-drawer-wallet-card__left {
  display: flex;
  align-items: center;
  gap: 10px;
  min-width: 0;
}

.mobile-drawer-wallet-status-dot {
  width: 9px;
  height: 9px;
  border-radius: 50%;
  flex-shrink: 0;
  transition: background 0.3s;
}

.dot--on {
  background: #00c59a;
  box-shadow: 0 0 0 3px rgba(0, 197, 154, 0.2);
}

.dot--off {
  background: #ef5350;
  box-shadow: 0 0 0 3px rgba(239, 83, 80, 0.2);
}

.mobile-drawer-wallet-card__label {
  font-size: 12px;
  font-weight: 600;
  color: #555;
}

.mobile-drawer-wallet-card__balance {
  font-size: 15px;
  font-weight: 800;
  color: #0d1738;
  letter-spacing: -0.4px;
  line-height: 1.2;
}

.mobile-drawer-wallet-card__addr {
  font-size: 10.5px;
  color: #888;
  font-family: monospace;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  max-width: 120px;
}

.mobile-drawer-wallet-card__btn {
  display: flex;
  align-items: center;
  gap: 5px;
  padding: 7px 13px;
  border-radius: 99px;
  border: none;
  background: rgba(46, 88, 216, 0.12);
  color: #2e58d8;
  font-size: 12px;
  font-weight: 700;
  cursor: pointer;
  white-space: nowrap;
  flex-shrink: 0;
  transition:
    background 0.18s,
    transform 0.18s cubic-bezier(0.34, 1.56, 0.64, 1);
  -webkit-tap-highlight-color: transparent;
}

.mobile-drawer-wallet-card__btn:hover {
  background: rgba(46, 88, 216, 0.2);
  transform: scale(1.04);
}

.mobile-drawer-wallet-card__btn:active {
  transform: scale(0.96);
}

/* ── Nav Body ────────────────────────────────────────────────── */
.mobile-drawer-body {
  flex: 1;
  overflow-y: auto;
  padding: 6px 8px 8px;
}

.mobile-drawer-section-label {
  font-size: 10px;
  font-weight: 700;
  letter-spacing: 0.9px;
  text-transform: uppercase;
  color: #aaa;
  padding: 8px 10px 3px;
}

.mobile-drawer-divider {
  height: 1px;
  background: rgba(0, 0, 0, 0.06);
  margin: 5px 10px;
}

/* 4. Full-width active pill */
.mobile-drawer-item {
  display: flex;
  align-items: center;
  gap: 11px;
  padding: 9px 10px;
  text-decoration: none;
  color: #444;
  font-size: 14px;
  font-weight: 500;
  border-radius: 12px;
  transition:
    background 0.15s,
    color 0.15s;
  position: relative;
  -webkit-tap-highlight-color: transparent;
}

.mobile-drawer-item:hover {
  background: rgba(46, 88, 216, 0.07);
  color: #2e58d8;
}

.mobile-drawer-item:active {
  background: rgba(46, 88, 216, 0.13);
  transform: scale(0.98);
}

.mobile-drawer-item--active {
  background: linear-gradient(90deg, rgba(46, 88, 216, 0.12) 0%, rgba(46, 88, 216, 0.04) 100%);
  color: #2e58d8;
  font-weight: 700;
}

/* Remove old thin-bar indicator — full pill is the indicator now */
.mobile-drawer-item--active::before {
  display: none;
}

/* 3. Colorful icon boxes */
.mobile-drawer-icon {
  width: 34px;
  height: 34px;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  transition: transform 0.2s cubic-bezier(0.34, 1.56, 0.64, 1);
}

.mobile-drawer-item:hover .mobile-drawer-icon,
.mobile-drawer-item--active .mobile-drawer-icon {
  transform: scale(1.1);
}

.mobile-drawer-icon--blue {
  background: rgba(46, 88, 216, 0.12);
  color: #2e58d8;
}
.mobile-drawer-icon--amber {
  background: rgba(255, 160, 0, 0.13);
  color: #e65100;
}
.mobile-drawer-icon--red {
  background: rgba(239, 83, 80, 0.12);
  color: #c62828;
}
.mobile-drawer-icon--green {
  background: rgba(0, 197, 154, 0.13);
  color: #00796b;
}
.mobile-drawer-icon--purple {
  background: rgba(123, 31, 162, 0.11);
  color: #7b1fa2;
}
.mobile-drawer-icon--teal {
  background: rgba(0, 137, 123, 0.12);
  color: #00897b;
}
.mobile-drawer-icon--indigo {
  background: rgba(57, 73, 171, 0.12);
  color: #3949ab;
}

.mobile-drawer-chevron {
  width: 16px;
  height: 16px;
  margin-left: auto;
  color: #ccc;
  flex-shrink: 0;
  transition:
    transform 0.22s cubic-bezier(0.34, 1.56, 0.64, 1),
    color 0.15s;
}

.mobile-drawer-item:hover .mobile-drawer-chevron,
.mobile-drawer-item--active .mobile-drawer-chevron {
  transform: translateX(3px);
  color: #2e58d8;
}

/* ── Network Switcher ────────────────────────────────────────── */
.network-switcher {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 8px;
  padding: 4px 2px 6px;
}

.network-card {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 6px;
  padding: 12px 8px 10px;
  border-radius: 14px;
  border: 1.5px solid transparent;
  background: rgba(0, 0, 0, 0.04);
  cursor: pointer;
  position: relative;
  transition:
    background 0.18s,
    border-color 0.18s,
    transform 0.15s;
  -webkit-tap-highlight-color: transparent;
}

.network-card:hover {
  background: rgba(46, 88, 216, 0.07);
  transform: translateY(-2px);
}

.network-card:active {
  transform: scale(0.96);
}

.network-card--active.network-card--blue {
  background: linear-gradient(135deg, rgba(46, 88, 216, 0.12) 0%, rgba(46, 88, 216, 0.05) 100%);
  border-color: rgba(46, 88, 216, 0.35);
  box-shadow: 0 2px 10px rgba(46, 88, 216, 0.15);
}

.network-card--active.network-card--amber {
  background: linear-gradient(135deg, rgba(255, 152, 0, 0.14) 0%, rgba(255, 152, 0, 0.05) 100%);
  border-color: rgba(255, 152, 0, 0.4);
  box-shadow: 0 2px 10px rgba(255, 152, 0, 0.18);
}

.network-card__icon {
  width: 40px;
  height: 40px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: transform 0.2s cubic-bezier(0.34, 1.56, 0.64, 1);
}

.network-card:hover .network-card__icon,
.network-card--active .network-card__icon {
  transform: scale(1.1);
}

.network-card__icon--blue {
  background: rgba(46, 88, 216, 0.12);
  color: #2e58d8;
}

.network-card__icon--amber {
  background: rgba(255, 152, 0, 0.14);
  color: #e65100;
}

.network-card__info {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1px;
}

.network-card__name {
  font-size: 13px;
  font-weight: 700;
  color: #333;
  line-height: 1.2;
}

.network-card__sub {
  font-size: 10px;
  font-weight: 500;
  color: #999;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.network-card__dot {
  position: absolute;
  top: 8px;
  right: 8px;
  width: 8px;
  height: 8px;
  border-radius: 50%;
}

.network-card__dot--blue {
  background: #2e58d8;
  box-shadow: 0 0 0 2px rgba(46, 88, 216, 0.25);
}

.network-card__dot--amber {
  background: #ff9800;
  box-shadow: 0 0 0 2px rgba(255, 152, 0, 0.3);
}

/* Dark mode */
.body--dark .network-card {
  background: rgba(255, 255, 255, 0.04);
}

.body--dark .network-card:hover {
  background: rgba(130, 177, 255, 0.08);
}

.body--dark .network-card--active.network-card--blue {
  background: linear-gradient(135deg, rgba(130, 177, 255, 0.16) 0%, rgba(130, 177, 255, 0.06) 100%);
  border-color: rgba(130, 177, 255, 0.4);
  box-shadow: 0 2px 10px rgba(130, 177, 255, 0.15);
}

.body--dark .network-card--active.network-card--amber {
  background: linear-gradient(135deg, rgba(255, 183, 77, 0.18) 0%, rgba(255, 183, 77, 0.06) 100%);
  border-color: rgba(255, 183, 77, 0.45);
  box-shadow: 0 2px 10px rgba(255, 183, 77, 0.2);
}

.body--dark .network-card__icon--blue {
  background: rgba(130, 177, 255, 0.14);
  color: #82b1ff;
}

.body--dark .network-card__icon--amber {
  background: rgba(255, 183, 77, 0.14);
  color: #ffb74d;
}

.body--dark .network-card__name {
  color: rgba(200, 210, 240, 0.9);
}

.body--dark .network-card__sub {
  color: rgba(200, 210, 240, 0.4);
}

.body--dark .network-card__dot--blue {
  background: #82b1ff;
  box-shadow: 0 0 0 2px rgba(130, 177, 255, 0.25);
}

.body--dark .network-card__dot--amber {
  background: #ffb74d;
  box-shadow: 0 0 0 2px rgba(255, 183, 77, 0.3);
}

/* ── 7. Footer with pill toggle + brand strip ────────────────── */
.mobile-drawer-footer {
  padding: 10px 16px 20px;
  border-top: 1px solid rgba(0, 0, 0, 0.06);
  flex-shrink: 0;
}

.mobile-drawer-footer__toggle-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 12px;
}

.mobile-drawer-footer__toggle-label {
  font-size: 13px;
  font-weight: 600;
  color: #555;
}

/* Pill toggle (same style as header) */
.drawer-dark-toggle {
  position: relative;
  width: 58px;
  height: 32px;
  border-radius: 999px;
  background: #ffffff;
  border: 1.5px solid #d0d7e3;
  cursor: pointer;
  padding: 0;
  outline: none;
  -webkit-tap-highlight-color: transparent;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.09);
  transition:
    background 0.28s ease,
    border-color 0.28s ease;
  flex-shrink: 0;
}

.drawer-dark-toggle__knob {
  position: absolute;
  top: 3px;
  left: 3px;
  width: 24px;
  height: 24px;
  border-radius: 50%;
  background: #00c59a;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 2px 6px rgba(0, 197, 154, 0.45);
  transition:
    transform 0.32s cubic-bezier(0.34, 1.56, 0.64, 1),
    background 0.28s ease;
}

.drawer-dark-toggle:not(.drawer-dark-toggle--dark) .drawer-dark-toggle__knob {
  transform: translateX(26px);
  background: #00c59a;
}

.drawer-dark-toggle--dark .drawer-dark-toggle__knob {
  transform: translateX(0);
  background: #5c6bc0;
  box-shadow: 0 2px 7px rgba(92, 107, 192, 0.5);
}

.mobile-drawer-footer__brand {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 5px;
  font-size: 10.5px;
  color: #bbb;
  font-weight: 500;
  letter-spacing: 0.2px;
}

/* ── Dark Mode ───────────────────────────────────────────────── */
.body--dark .mobile-drawer {
  background: rgba(15, 17, 28, 0.82);
  border-left-color: rgba(255, 255, 255, 0.07);
  box-shadow:
    -4px 0 12px rgba(0, 0, 0, 0.2),
    -16px 0 64px rgba(0, 0, 0, 0.65),
    -32px 0 80px rgba(0, 0, 0, 0.4);
}

.body--dark .mobile-drawer-header {
  border-bottom-color: rgba(255, 255, 255, 0.07);
}

.body--dark .mobile-drawer-brand {
  color: #e8eaf6;
}

.body--dark .mobile-drawer-close {
  background: rgba(255, 255, 255, 0.08);
  color: #bbb;
}

.body--dark .mobile-drawer-close:hover {
  background: rgba(255, 255, 255, 0.14);
}

.body--dark .mobile-drawer-wallet-card {
  background: linear-gradient(135deg, rgba(239, 83, 80, 0.15) 0%, rgba(239, 83, 80, 0.06) 100%);
  border-color: rgba(239, 83, 80, 0.22);
}

.body--dark .mobile-drawer-wallet-card--connected {
  background: linear-gradient(135deg, rgba(0, 197, 154, 0.18) 0%, rgba(46, 88, 216, 0.1) 100%);
  border-color: rgba(0, 197, 154, 0.28);
}

.body--dark .mobile-drawer-wallet-card__label {
  color: rgba(200, 210, 240, 0.6);
}

.body--dark .mobile-drawer-wallet-card__balance {
  color: #e8eaf6;
}

.body--dark .mobile-drawer-wallet-card__addr {
  color: rgba(200, 210, 240, 0.5);
}

.body--dark .mobile-drawer-wallet-card__btn {
  background: rgba(130, 177, 255, 0.12);
  color: #82b1ff;
}

.body--dark .mobile-drawer-wallet-card__btn:hover {
  background: rgba(130, 177, 255, 0.22);
}

.body--dark .mobile-drawer-section-label {
  color: #555;
}

.body--dark .mobile-drawer-divider {
  background: rgba(255, 255, 255, 0.07);
}

.body--dark .mobile-drawer-item {
  color: rgba(200, 210, 240, 0.78);
}

.body--dark .mobile-drawer-item:hover {
  background: rgba(130, 177, 255, 0.08);
  color: #82b1ff;
}

.body--dark .mobile-drawer-item--active {
  background: linear-gradient(90deg, rgba(130, 177, 255, 0.14) 0%, rgba(130, 177, 255, 0.04) 100%);
  color: #82b1ff;
}

.body--dark .mobile-drawer-item:hover .mobile-drawer-chevron,
.body--dark .mobile-drawer-item--active .mobile-drawer-chevron {
  color: #82b1ff;
}

.body--dark .mobile-drawer-icon--blue {
  background: rgba(130, 177, 255, 0.12);
  color: #82b1ff;
}
.body--dark .mobile-drawer-icon--amber {
  background: rgba(255, 183, 77, 0.12);
  color: #ffb74d;
}
.body--dark .mobile-drawer-icon--red {
  background: rgba(239, 154, 154, 0.12);
  color: #ef9a9a;
}
.body--dark .mobile-drawer-icon--green {
  background: rgba(128, 222, 234, 0.1);
  color: #80deea;
}
.body--dark .mobile-drawer-icon--purple {
  background: rgba(206, 147, 216, 0.12);
  color: #ce93d8;
}
.body--dark .mobile-drawer-icon--teal {
  background: rgba(128, 203, 196, 0.11);
  color: #80cbc4;
}
.body--dark .mobile-drawer-icon--indigo {
  background: rgba(159, 168, 218, 0.12);
  color: #9fa8da;
}

.body--dark .mobile-drawer-footer {
  border-top-color: rgba(255, 255, 255, 0.07);
}

.body--dark .mobile-drawer-footer__toggle-label {
  color: rgba(200, 210, 240, 0.7);
}

.body--dark .drawer-dark-toggle {
  background: rgba(255, 255, 255, 0.07);
  border-color: rgba(255, 255, 255, 0.12);
}

.body--dark .mobile-drawer-footer__brand {
  color: rgba(255, 255, 255, 0.2);
}
</style>

<template>
  <q-layout view="lHh Lpr lFf">

    <!-- HEADER ini !!!-->
    <q-header class="app-header">
      <q-toolbar class="q-px-lg">

        <!-- Logo ini !!!-->
        <div class="row items-center">
          <q-avatar size="40px">
            <img src="~assets/BitoHelp.png" />
          </q-avatar>

          <div class="app-title q-ml-sm">BitoHelp</div>
        </div>

        <q-space />

        <!-- Wallet Button ini !!!-->
        <q-btn
          unelevated
          icon="mdi-wallet"
          label="Connect Wallet"
          class="wallet-btn"
          @click="connectWallet"
        />

      </q-toolbar>
    </q-header>

    <!-- PAGE CONTENT -->
    <q-page-container>
      <router-view />
    </q-page-container>

  </q-layout>
</template>

<script setup>
const connectWallet = () => {
  console.log('Connect wallet clicked')
}
</script>

<template>
  <q-page class="donation-page">

    <div class="donation-wrapper">

      <!-- LEFT SIDE ini !!!-->
      <div class="donation-form">

        <div class="row items-center q-col-gutter-md">
          <div class="col">
            <h1>Where your crypto creates a better tomorrow.</h1>
            <p class="subtitle">
              By donating crypto, you unlock smarter, more efficient giving.<br/>Support thousands of verified nonprofits through blockchain-powered donations.
            </p>
          </div>
        </div>

        <q-select v-model="form.cause" outlined label="Choose non-profit or a cause" class="q-mb-md" />
        <q-input v-model="form.contract" outlined label="Contract" class="q-mb-md" />
        <div class="row q-col-gutter-md">
          <div class="col">
            <q-select v-model="form.coin" :options="causes" label="Choose a coin" outlined dense class="q-mb-md"/>
          </div>
          <div class="col">
            <q-input v-model="form.amount" outlined label="Coin amount" />
          </div>
        </div>  

        <q-input
          v-model="form.message"
          outlined
          type="textarea"
          label="Message here for non-profit (area of intent)"
          class="q-mt-md"
        />
       
        <div class="section-title">Donor Contact Info</div>

        <q-input v-model="form.email" outlined label="Email address" class="q-mb-md" />
        <q-input v-model="form.name" outlined label="Name of donor" class="q-mb-md" />
        <q-input v-model="form.contact" outlined label="Contact number" />
      </div>

      <!-- RIGHT SIDE ini !!!-->
      <div class="donation-summary">
        <div class="donation-summary-logo">
          <img src="~assets/image1.png" alt="BiToHelp" />
        </div>
        <div class="summary-card">
          <h3>Donation Summary</h3>

          <div class="summary-row">
            <span>Charity Name</span>
            <span>BSP Fund</span>
          </div>

          <div class="summary-row">
            <span>Contract</span>
            <span>5 years</span>
          </div>

          <div class="summary-row">
            <span>Coin</span>
            <span>Bitcoin</span>
          </div>

          <div class="summary-row">
            <span>Amount</span>
            <span>1 Million USD</span>
          </div>

          <div class="summary-divider"></div>

          <q-btn
            class="continue-btn"
            label="Continue"
            unelevated
            to="/continue"
            @click="$router.push('/continue')"
          />

          <p class="terms">
            By selecting continue you agree to our
            <span>terms and conditions</span>
          </p>

        </div>

      </div>

      <div class="donation-footer">
      <div class="footer-brand">
        <img src="~assets/image1.png" alt="BiToHelp" />
        <div class="footer-brand-text">BiToHelp</div>
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
import { ref } from 'vue'


const form = ref({
  cause: null,
  contract: null,
  coin: null,
  amount: null,
  message: '',
  email: '',
  name: '',
  contact: ''
})
</script>

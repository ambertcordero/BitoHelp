<template>
  <q-page class="contact-page">

    <!-- HERO ini !!!-->
    <section class="contact-hero-section">
      <div class="container">
        <div class="row items-center">
          <div class="col-12 col-md-6">
            <h1 class="hero-title text-white">Get In Touch</h1>
            <p class="hero-subtitle text-white">
              Have a question, partnership idea, or just want to say hi?
              Send us a message and our team will get back to you.
            </p>
          </div>
        </div>
      </div>
    </section>


    <!-- Contact Section ini !!!-->
    <section class="q-py-xl q-px-md">
      <div class="container">
        <div class="row q-col-gutter-xl">

          <!-- Form -->
          <div class="col-12 col-md-7">
            <h2 class="text-h5 text-weight-bold q-mb-lg">Send Us a Message</h2>

            <div v-if="messageSent" class="sent-banner q-mb-lg">
              <q-icon name="check_circle" color="positive" size="28px" />
              <div>
                <div class="text-subtitle1 text-weight-bold">Message sent!</div>
                <div class="text-caption text-grey-7">We'll get back to you within 24 hours.</div>
              </div>
            </div>

            <div v-else>
              <div class="row q-col-gutter-md">
                <div class="col-12 col-sm-6">
                  <label class="input-label">Full Name <span class="text-negative">*</span></label>
                  <q-input
                    v-model="form.name"
                    outlined
                    dense
                    placeholder="Juan Dela Cruz"
                    :rules="[val => !!val || 'Name is required']"
                  />
                </div>
                <div class="col-12 col-sm-6">
                  <label class="input-label">Email Address <span class="text-negative">*</span></label>
                  <q-input
                    v-model="form.email"
                    outlined
                    dense
                    placeholder="juan@email.com"
                    type="email"
                    :rules="[val => !!val || 'Email is required']"
                  />
                </div>
                <div class="col-12">
                  <label class="input-label">Subject</label>
                  <q-input
                    v-model="form.subject"
                    outlined
                    dense
                    placeholder="How can we help you?"
                  />
                </div>
                <div class="col-12">
                  <label class="input-label">Message <span class="text-negative">*</span></label>
                  <q-input
                    v-model="form.message"
                    outlined
                    dense
                    type="textarea"
                    rows="5"
                    placeholder="Tell us what you need..."
                    :rules="[val => !!val || 'Message is required']"
                  />
                </div>
                <div class="col-12">
                  <q-btn
                    label="Send Message"
                    unelevated
                    color="primary"
                    size="md"
                    padding="12px 36px"
                    :loading="sending"
                    @click="submitForm"
                  />
                </div>
              </div>
            </div>
          </div>

          <!-- Contact Info -->
          <div class="col-12 col-md-5">
            <h2 class="text-h5 text-weight-bold q-mb-lg">Other Ways to Reach Us</h2>

            <div class="contact-info-card q-mb-md" :class="{ 'contact-info-card--active': selectedCard === 'email' }" @click="selectedCard = selectedCard === 'email' ? null : 'email'">
              <div class="contact-icon-wrap" style="background: #e3f2fd;">
                <q-icon name="email" color="primary" size="22px" />
              </div>
              <div>
                <div class="text-subtitle2 text-weight-bold">Email</div>
                <div class="text-body2 text-grey-7">support@bitohelp.io</div>
                <div class="text-body2 text-grey-7">partnerships@bitohelp.io</div>
              </div>
            </div>

            <div class="contact-info-card q-mb-md" :class="{ 'contact-info-card--active': selectedCard === 'telegram' }" @click="selectedCard = selectedCard === 'telegram' ? null : 'telegram'">
              <div class="contact-icon-wrap" style="background: #e8f5e9;">
                <q-icon name="chat" color="positive" size="22px" />
              </div>
              <div>
                <div class="text-subtitle2 text-weight-bold">Telegram</div>
                <div class="text-body2 text-grey-7">@BitoHelpSupport</div>
                <div class="text-caption text-grey-5">Usually responds in a few hours</div>
              </div>
            </div>

            <div class="contact-info-card q-mb-md" :class="{ 'contact-info-card--active': selectedCard === 'location' }" @click="selectedCard = selectedCard === 'location' ? null : 'location'">
              <div class="contact-icon-wrap" style="background: #fff3e0;">
                <q-icon name="place" color="orange" size="22px" />
              </div>
              <div>
                <div class="text-subtitle2 text-weight-bold">Location</div>
                <div class="text-body2 text-grey-7">Philippines</div>
                <div class="text-caption text-grey-5">Remote-first team</div>
              </div>
            </div>

            <div class="contact-info-card" :class="{ 'contact-info-card--active': selectedCard === 'bch' }" @click="selectedCard = selectedCard === 'bch' ? null : 'bch'">
              <div class="contact-icon-wrap" style="background: #f3e5f5;">
                <q-icon name="currency_bitcoin" color="purple" size="22px" />
              </div>
              <div>
                <div class="text-subtitle2 text-weight-bold">Bitcoin Cash</div>
                <div class="text-body2 text-grey-7">Built on BCH mainnet &amp; chipnet</div>
                <div class="text-caption text-grey-5">0% platform fee</div>
              </div>
            </div>

            <!-- Partner Banner -->
            <div class="partner-banner q-mt-lg">
              <q-icon name="handshake" size="32px" color="primary" class="q-mb-sm" />
              <div class="text-subtitle1 text-weight-bold q-mb-xs">Partner With Us</div>
              <p class="text-body2 text-grey-7 q-mb-md" style="line-height: 1.6">
                Register your nonprofit and receive BCH donations directly to your wallet.
              </p>
              <q-btn
                label="Register a Charity"
                flat
                color="primary"
                padding="8px 24px"
                to="/charities"
              />
            </div>
          </div>
        </div>
      </div>
    </section>


    <!-- FAQ Section ini !!!-->
      <section class="contact-faq-section q-py-xl q-px-md" style="background: #f8f9fa;">
      <div class="container">
        <h2 class="text-h4 text-weight-bold q-mb-sm">Frequently Asked Questions</h2>
        <p class="text-body1 text-grey-7 q-mb-xl">Common questions about BitoHelp.</p>

        <div class="row q-col-gutter-lg">
          <div class="col-12 col-md-8">
            <q-expansion-item
              class="faq-item q-mb-sm"
              :class="{ 'faq-item--active': selectedFaq === 'donate' }"
              @click="selectedFaq = selectedFaq === 'donate' ? null : 'donate'"
              label="How do I donate using Bitcoin Cash?"
              icon="help_outline"
              expand-separator
            >
              <q-card flat>
                <q-card-section class="text-grey-8" style="line-height: 1.8">
                  Connect your BCH wallet through the "Connect Wallet" button, browse charities,
                  choose an amount, and confirm the transaction. Your donation goes directly
                  on-chain — no middleman.
                </q-card-section>
              </q-card>
            </q-expansion-item>

            <q-expansion-item
              class="faq-item q-mb-sm"
              :class="{ 'faq-item--active': selectedFaq === 'verified' }"
              @click="selectedFaq = selectedFaq === 'verified' ? null : 'verified'"
              label="Are the charities on BitoHelp verified?"
              icon="verified"
              expand-separator
            >
              <q-card flat>
                <q-card-section class="text-grey-8" style="line-height: 1.8">
                  Yes. All nonprofits go through a registration and review process before
                  appearing on the platform. Only verified organizations can receive donations.
                </q-card-section>
              </q-card>
            </q-expansion-item>

            <q-expansion-item
              class="faq-item q-mb-sm"
              :class="{ 'faq-item--active': selectedFaq === 'fees' }"
              @click="selectedFaq = selectedFaq === 'fees' ? null : 'fees'"
              label="What are the platform fees?"
              icon="savings"
              expand-separator
            >
              <q-card flat>
                <q-card-section class="text-grey-8" style="line-height: 1.8">
                  BitoHelp charges 0% platform fees. The only cost is the Bitcoin Cash network
                  transaction fee, which is usually less than ₱0.01.
                </q-card-section>
              </q-card>
            </q-expansion-item>

            <q-expansion-item
              class="faq-item q-mb-sm"
              :class="{ 'faq-item--active': selectedFaq === 'recurring' }"
              @click="selectedFaq = selectedFaq === 'recurring' ? null : 'recurring'"
              label="Can I set up recurring donations?"
              icon="repeat"
              expand-separator
            >
              <q-card flat>
                <q-card-section class="text-grey-8" style="line-height: 1.8">
                  Yes! BitoHelp supports recurring donations through smart contracts.
                  You can set a monthly or weekly schedule and cancel anytime.
                </q-card-section>
              </q-card>
            </q-expansion-item>

            <q-expansion-item
              class="faq-item"
              :class="{ 'faq-item--active': selectedFaq === 'register' }"
              @click="selectedFaq = selectedFaq === 'register' ? null : 'register'"
              label="How do I register my charity?"
              icon="business"
              expand-separator
            >
              <q-card flat>
                <q-card-section class="text-grey-8" style="line-height: 1.8">
                  Go to the Charities page and click "Register Nonprofit". Fill in your
                  organization details and BCH wallet address. Our team will review
                  and approve your registration.
                </q-card-section>
              </q-card>
            </q-expansion-item>
          </div>

          <div class="col-12 col-md-4">
            <div class="faq-cta-box">
              <q-icon name="support_agent" size="40px" color="primary" class="q-mb-md" />
              <div class="text-subtitle1 text-weight-bold q-mb-sm">Still have questions?</div>
              <p class="text-body2 text-grey-7 q-mb-lg" style="line-height: 1.6">
                Can't find what you're looking for? Reach out and we'll help.
              </p>
              <q-btn
                label="Contact Support"
                unelevated
                color="primary"
                padding="10px 28px"
                @click="scrollToForm"
              />
            </div>
          </div>
        </div>
      </div>
    </section>

  </q-page>
</template>

<script setup>
import { ref } from 'vue'

const form = ref({
  name: '',
  email: '',
  subject: '',
  message: '',
})
const sending = ref(false)
const messageSent = ref(false)
const selectedCard = ref(null)
const selectedFaq = ref(null)

function scrollToForm () {
  window.scrollTo({ top: 0, behavior: 'smooth' })
}

function submitForm () {
  if (!form.value.name || !form.value.email || !form.value.message) return
  sending.value = true
  setTimeout(() => {
    sending.value = false
    messageSent.value = true
  }, 1200)
}
</script>

<style scoped>
.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 24px;
}

/* HERO */
.contact-hero-section {
  min-height: 45vh;
  background-image: url('../assets/support.jpg');
  background-size: cover;
  background-position: center;
  position: relative;
  display: flex;
  align-items: center;
  padding: 80px 24px;
}

.contact-hero-section::before {
  content: '';
  position: absolute;
  inset: 0;
  background: rgba(13, 71, 161, 0.72);
}

.contact-hero-section .container {
  position: relative;
  z-index: 1;
}

.hero-title {
  font-size: 3.2rem;
  font-weight: 800;
  line-height: 1.1;
  margin-bottom: 18px;
}

.hero-subtitle {
  font-size: 1.1rem;
  line-height: 1.7;
  max-width: 500px;
}

/* input label */
.input-label {
  display: block;
  font-size: 13px;
  font-weight: 600;
  color: #333;
  margin-bottom: 6px;
}

/* Sent banner */
.sent-banner {
  display: flex;
  align-items: center;
  gap: 16px;
  background: #e8f5e9;
  border: 1px solid #a5d6a7;
  border-radius: 12px;
  padding: 16px 20px;
}

/* Contact info cards */
.contact-info-card {
  display: flex;
  align-items: flex-start;
  gap: 16px;
  padding: 16px;
  border: 1.5px solid #e0e0e0;
  border-radius: 12px;
  background: white;
  cursor: pointer;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.08), 0 1px 4px rgba(0, 0, 0, 0.04);
  transition: box-shadow 0.2s ease, transform 0.2s ease, border-color 0.2s ease;
  user-select: none;
}
.contact-info-card:hover {
  box-shadow: 0 8px 28px rgba(0, 0, 0, 0.13), 0 2px 8px rgba(0, 0, 0, 0.07);
  transform: translateY(-3px);
}
.contact-info-card--active {
  border-color: #1565c0 !important;
  box-shadow: 0 0 0 3px rgba(21, 101, 192, 0.18), 0 8px 28px rgba(0, 0, 0, 0.13) !important;
  transform: translateY(-3px);
}

.contact-icon-wrap {
  width: 44px;
  height: 44px;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

/* Partner banner */
.partner-banner {
  background: #e3f2fd;
  border-radius: 16px;
  padding: 24px;
}

/* FAQ items */
.faq-item {
  background: white;
  border: 1.5px solid #e0e0e0;
  border-radius: 12px;
  overflow: hidden;
  cursor: pointer;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.08), 0 1px 4px rgba(0, 0, 0, 0.04);
  transition: box-shadow 0.2s ease, transform 0.2s ease, border-color 0.2s ease;
}
.faq-item:hover {
  box-shadow: 0 8px 28px rgba(0, 0, 0, 0.13), 0 2px 8px rgba(0, 0, 0, 0.07);
  transform: translateY(-3px);
}
.faq-item--active {
  border-color: #1565c0 !important;
  box-shadow: 0 0 0 3px rgba(21, 101, 192, 0.18), 0 8px 28px rgba(0, 0, 0, 0.13) !important;
  transform: translateY(-3px);
}

/* FAQ CTA box */
.faq-cta-box {
  background: white;
  border: 1px solid #e0e0e0;
  border-radius: 16px;
  padding: 28px;
  text-align: center;
  height: 100%;
}

/* ── Dark Mode ──────────────────────────────────────────────── */
.body--dark .contact-page {
  background: #0d1117;
}

/* Contact info cards */
.body--dark .contact-info-card {
  background: #1e2a3a;
  border-color: rgba(255, 255, 255, 0.08);
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.25), 0 1px 4px rgba(0, 0, 0, 0.15);
}
.body--dark .contact-info-card:hover {
  box-shadow: 0 8px 28px rgba(0, 0, 0, 0.4), 0 2px 8px rgba(0, 0, 0, 0.2);
}
.body--dark .contact-info-card--active {
  border-color: #42a5f5 !important;
  box-shadow: 0 0 0 3px rgba(66, 165, 245, 0.22), 0 8px 28px rgba(0, 0, 0, 0.4) !important;
}

.body--dark .contact-icon-wrap {
  background: rgba(255, 255, 255, 0.06) !important;
}

/* Partner banner */
.body--dark .partner-banner {
  background: #1a3558;
}

/* Form panel */
.body--dark .input-label {
  color: #ccc;
}

.body--dark .sent-banner {
  background: rgba(27, 94, 32, 0.3);
  border-color: rgba(76, 175, 80, 0.3);
}

/* FAQ section */
.body--dark .contact-faq-section {
  background: #131d35 !important;
}

.body--dark .faq-item {
  background: #1e2a3a;
  border-color: rgba(255, 255, 255, 0.08);
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.25), 0 1px 4px rgba(0, 0, 0, 0.15);
}
.body--dark .faq-item:hover {
  box-shadow: 0 8px 28px rgba(0, 0, 0, 0.4), 0 2px 8px rgba(0, 0, 0, 0.2);
}
.body--dark .faq-item--active {
  border-color: #42a5f5 !important;
  box-shadow: 0 0 0 3px rgba(66, 165, 245, 0.22), 0 8px 28px rgba(0, 0, 0, 0.4) !important;
}

.body--dark .faq-cta-box {
  background: #1e2a3a;
  border-color: rgba(255, 255, 255, 0.08);
}

/* ── Mobile Responsive ───────────────────────────────────────── */
@media (max-width: 599px) {
  .hero-title {
    font-size: 2.2rem;
    margin-bottom: 14px;
  }

  .hero-subtitle {
    font-size: 1rem;
  }

  .contact-hero-section {
    padding: 60px 16px 40px;
    min-height: 38vh;
  }

  /* FAQ CTA box loses height: 100% on mobile — let it be natural height */
  .faq-cta-box {
    height: auto;
    margin-top: 8px;
  }

  /* Partner banner */
  .partner-banner {
    padding: 18px;
  }
}

@media (min-width: 600px) and (max-width: 1023px) {
  .hero-title {
    font-size: 2.6rem;
  }
}
</style>

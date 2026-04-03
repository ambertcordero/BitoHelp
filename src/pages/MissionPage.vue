<template>
  <q-page class="mission-page">

    <!-- HERO ini !!!-->
    <section class="mission-hero-section">
      <div class="container">
        <div class="row items-center">
          <div class="col-12 col-md-6 hero-content">
            <h1 class="hero-title text-white">
              Our Mission
            </h1>
            <p class="hero-subtitle text-white">
              We believe that giving should be borderless, instant, and transparent. BitoHelp uses
              Bitcoin Cash to connect donors directly with verified nonprofits â€” no middlemen,
              no hidden fees, no delays.
            </p>
            <div class="row q-mt-lg" style="gap: 16px;">
              <q-btn
                unelevated
                color="white"
                text-color="primary"
                label="Start Donating"
                size="lg"
                to="/donate"
              />
              <q-btn
                flat
                color="white"
                label="View Charities"
                size="lg"
                to="/charities"
              />
            </div>
          </div>
        </div>
      </div>
    </section>


    <!-- What We Stand For ini !!!-->
    <section class="q-py-xl q-px-md">
      <div class="container">
        <div class="row">
          <div class="col-12 col-md-5 q-pr-xl">
            <h2 class="mission-heading text-weight-bold q-mb-lg">What We Stand For</h2>

            <p class="text-body1 text-grey-8" style="line-height: 1.8;">
              BitoHelp was built on a simple belief â€” technology can make generosity more
              powerful. We leverage Bitcoin Cash to give donors full visibility over their
              contributions, from wallet to cause.
            </p>

            <p class="text-body1 text-grey-8 q-mt-md" style="line-height: 1.8;">
              Every transaction is recorded on-chain. Every peso is traceable. Every nonprofit
              is verified before they receive a single satoshi.
            </p>

            <div class="row q-col-gutter-sm q-mt-xl">
              <div class="col-6">
                <div class="mission-photo-box">
                  <img src="~assets/unity.jpg" alt="Community" />
                </div>
              </div>
              <div class="col-6">
                <div class="mission-photo-box">
                  <img src="~assets/medically.jpg" alt="Medical Aid" />
                </div>
              </div>
            </div>
          </div>

          <div class="col-12 col-md-7">
            <div class="mission-large-photo q-mb-sm">
              <img src="~assets/teacher.jpg" alt="Education" />
            </div>
            <div class="row q-col-gutter-sm">
              <div class="col-4">
                <div class="mission-photo-box">
                  <img src="~assets/medical.jpg" alt="Medical Support" />
                </div>
              </div>
              <div class="col-4">
                <div class="mission-photo-box">
                  <img src="~assets/rescue.jpg" alt="Rescue" />
                </div>
              </div>
              <div class="col-4">
                <div class="mission-photo-box">
                  <img src="~assets/planting.jpg" alt="Livelihood" />
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Stats ini -->
        <div class="row q-col-gutter-md q-mt-xl q-pt-xl">
          <div class="col-12 col-sm-4 text-center">
            <div class="stat-card q-pa-md">
              <div class="text-h3 text-weight-bold text-primary">500+</div>
              <div class="text-subtitle1 text-grey-7">Donations Processed</div>
            </div>
          </div>
          <div class="col-12 col-sm-4 text-center">
            <div class="stat-card q-pa-md">
              <div class="text-h3 text-weight-bold text-positive">30+</div>
              <div class="text-subtitle1 text-grey-7">Verified Charities</div>
            </div>
          </div>
          <div class="col-12 col-sm-4 text-center">
            <div class="stat-card q-pa-md">
              <div class="text-h3 text-weight-bold text-secondary">100%</div>
              <div class="text-subtitle1 text-grey-7">On-Chain Verified</div>
            </div>
          </div>
        </div>
      </div>
    </section>


    <!-- How It Works ini !!!-->
    <section class="howit-section q-py-xl q-px-md">
      <div class="container">
        <div class="row q-mb-xl">
          <div class="col-12 col-md-8">
            <h2 class="text-h3 text-weight-bold q-mb-md">How It Works</h2>
            <p class="text-body1 text-grey-8" style="line-height: 1.8">
              Donating with BitoHelp takes less than a minute. No bank accounts, no sign-up
              required â€” just connect your wallet and give.
            </p>
          </div>
        </div>

        <div class="row q-col-gutter-lg">
          <div class="col-12 col-md-6">
            <div class="howit-card">
              <div class="howit-number">01</div>
              <h3 class="text-h5 text-weight-bold q-mb-sm">Connect Your Wallet</h3>
              <p class="text-body1 text-grey-8" style="line-height: 1.7">
                Scan the WalletConnect QR code with Paytaca, Cashonize, or any compatible BCH
                wallet. No account needed.
              </p>
              <div class="q-mt-md">
                <q-chip dense color="blue-1" text-color="primary" icon="account_balance_wallet">
                  <span class="text-weight-medium">WalletConnect</span>
                </q-chip>
              </div>
            </div>
          </div>

          <div class="col-12 col-md-6">
            <div class="howit-card">
              <div class="howit-number">02</div>
              <h3 class="text-h5 text-weight-bold q-mb-sm">Choose a Cause</h3>
              <p class="text-body1 text-grey-8" style="line-height: 1.7">
                Browse our list of verified nonprofits and projects. Filter by category â€”
                disaster relief, education, medical, and more.
              </p>
              <div class="q-mt-md">
                <q-chip dense color="green-1" text-color="positive" icon="verified">
                  <span class="text-weight-medium">Verified Nonprofits</span>
                </q-chip>
              </div>
            </div>
          </div>

          <div class="col-12 col-md-6">
            <div class="howit-card">
              <div class="howit-number">03</div>
              <h3 class="text-h5 text-weight-bold q-mb-sm">Send BCH</h3>
              <p class="text-body1 text-grey-8" style="line-height: 1.7">
                Enter the amount, confirm in your wallet, and done. Your donation hits the
                blockchain in seconds with fees under $0.01.
              </p>
              <div class="howit-fee-row q-mt-md">
                <div style="display: flex; align-items: center; gap: 12px;">
                  <span class="text-caption text-grey-6">Traditional fees:</span>
                  <span class="text-weight-bold text-negative">2.9% + $0.30</span>
                </div>
                <div style="display: flex; align-items: center; gap: 12px;">
                  <span class="text-caption text-grey-6">BitoHelp / BCH:</span>
                  <span class="text-weight-bold text-positive">&lt;$0.01</span>
                </div>
              </div>
            </div>
          </div>

          <div class="col-12 col-md-6">
            <div class="howit-card">
              <div class="howit-number">04</div>
              <h3 class="text-h5 text-weight-bold q-mb-sm">Track Your Impact</h3>
              <p class="text-body1 text-grey-8" style="line-height: 1.7">
                Every donation generates an on-chain transaction ID. View your history on the
                donor dashboard and verify anytime on a block explorer.
              </p>
              <div class="q-mt-md">
                <q-chip dense color="purple-1" text-color="purple" icon="timeline">
                  <span class="text-weight-medium">Full transparency</span>
                </q-chip>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>


    <!-- Areas of Impact ini !!!-->
      <section class="mission-causes-section q-py-xl q-px-md" style="background: #f8f9fa;">
      <div class="container">
        <h3 class="text-h5 text-weight-bold q-mb-lg">Where Your Donations Make an Impact</h3>
        <div class="row q-col-gutter-md">
          <div class="col-12 col-sm-6 col-md-3">
            <div class="cause-area-card">
              <div class="cause-icon-wrapper q-mb-sm">
                <img src="~assets/scholar.jpg" alt="Education" class="cause-image" />
              </div>
              <div class="text-subtitle1 text-weight-bold q-mb-xs">Education</div>
              <p class="text-caption text-grey-7">Scholarships & school supplies</p>
            </div>
          </div>
          <div class="col-12 col-sm-6 col-md-3">
            <div class="cause-area-card">
              <div class="cause-icon-wrapper q-mb-sm">
                <img src="~assets/medical.jpg" alt="Healthcare" class="cause-image" />
              </div>
              <div class="text-subtitle1 text-weight-bold q-mb-xs">Healthcare</div>
              <p class="text-caption text-grey-7">Medical care & supplies</p>
            </div>
          </div>
          <div class="col-12 col-sm-6 col-md-3">
            <div class="cause-area-card">
              <div class="cause-icon-wrapper q-mb-sm">
                <img src="~assets/typhoon.jpeg" alt="Disaster Relief" class="cause-image" />
              </div>
              <div class="text-subtitle1 text-weight-bold q-mb-xs">Disaster Relief</div>
              <p class="text-caption text-grey-7">Emergency response</p>
            </div>
          </div>
          <div class="col-12 col-sm-6 col-md-3">
            <div class="cause-area-card">
              <div class="cause-icon-wrapper q-mb-sm">
                <img src="~assets/community.jpg" alt="Community" class="cause-image" />
              </div>
              <div class="text-subtitle1 text-weight-bold q-mb-xs">Community</div>
              <p class="text-caption text-grey-7">Livelihood & development</p>
            </div>
          </div>
        </div>

        <div class="mission-cta-section q-mt-xl q-pt-lg">
          <div class="row items-center">
            <div class="col-12 col-md-7">
              <h3 class="text-h5 text-weight-bold q-mb-sm">Ready to make a difference?</h3>
              <p class="text-body2 text-grey-7">
                Connect your Bitcoin Cash wallet and support a cause today.
              </p>
            </div>
            <div class="col-12 col-md-5 text-right">
              <q-btn
                label="Donate Now"
                color="primary"
                size="lg"
                unelevated
                padding="12px 32px"
                to="/donate"
              />
            </div>
          </div>
        </div>
      </div>
    </section>

  </q-page>
</template>

<script setup>
</script>

<style scoped>
.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 24px;
}

/* HERO */
.mission-hero-section {
  min-height: 60vh;
  background-image: url('../assets/bg.jpg');
  background-size: cover;
  background-position: center;
  position: relative;
  display: flex;
  align-items: center;
  padding: 80px 24px;
}

.mission-hero-section::before {
  content: '';
  position: absolute;
  inset: 0;
  background: rgba(0, 0, 0, 0.55);
}

.mission-hero-section .container {
  position: relative;
  z-index: 1;
}

.hero-title {
  font-size: 3.5rem;
  font-weight: 800;
  line-height: 1.1;
  margin-bottom: 20px;
}

.hero-subtitle {
  font-size: 1.1rem;
  line-height: 1.7;
  margin-bottom: 8px;
  max-width: 520px;
}

.mission-heading {
  font-size: 2.2rem;
  color: #1a237e;
}

/* Photos */
.mission-large-photo {
  width: 100%;
  height: 260px;
  border-radius: 16px;
  overflow: hidden;
}

.mission-large-photo img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.mission-photo-box {
  width: 100%;
  height: 120px;
  border-radius: 12px;
  overflow: hidden;
}

.mission-photo-box img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

/* Stats */
.stat-card {
  border: 1px solid #e0e0e0;
  border-radius: 16px;
  background: white;
}

/* How It Works */
.howit-section {
  background: white;
}

.howit-card {
  padding: 28px;
  border: 1.5px solid #e0e0e0;
  border-radius: 16px;
  background: white;
  height: 100%;
}

.howit-number {
  font-size: 2.5rem;
  font-weight: 900;
  color: #e3f2fd;
  line-height: 1;
  margin-bottom: 12px;
}

.howit-fee-row {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

/* Cause cards */
.cause-area-card {
  background: white;
  border-radius: 16px;
  padding: 16px;
  text-align: center;
  border: 1px solid #e0e0e0;
}

.cause-icon-wrapper {
  width: 100%;
  height: 140px;
  border-radius: 12px;
  overflow: hidden;
}

.cause-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

/* CTA */
.mission-cta-section {
  background: #e3f2fd;
  border-radius: 20px;
  padding: 32px 36px;
}

/* ── Dark Mode ──────────────────────────────────────────────── */
.body--dark .mission-page {
  background: #0d1117;
}

/* What We Stand For section */
.body--dark .stat-card {
  background: #1e2a3a;
  border-color: rgba(255, 255, 255, 0.08);
}

/* How It Works */
.body--dark .howit-section {
  background: #0f1629;
}

.body--dark .howit-card {
  background: #1e2a3a;
  border-color: rgba(255, 255, 255, 0.08);
}

.body--dark .howit-number {
  color: rgba(144, 202, 249, 0.15);
}

/* Cause areas section */
.body--dark .mission-causes-section {
  background: #131d35 !important;
}

.body--dark .cause-area-card {
  background: #1e2a3a;
  border-color: rgba(255, 255, 255, 0.08);
}

/* CTA */
.body--dark .mission-cta-section {
  background: #1a3558;
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

  .mission-hero-section {
    padding: 60px 16px 40px;
    min-height: 50vh;
  }

  .mission-heading {
    font-size: 1.8rem;
  }

  /* Mission left col — strip the q-pr-xl right padding when stacked */
  .col-12.q-pr-xl {
    padding-right: 0 !important;
  }

  .mission-large-photo {
    height: 180px;
  }

  .mission-photo-box {
    height: 90px;
  }

  .howit-card {
    padding: 20px 16px;
  }

  .howit-number {
    font-size: 2rem;
  }

  /* CTA section — center button on mobile */
  .mission-cta-section {
    padding: 24px 20px;
  }

  .mission-cta-section .col-12.text-right {
    text-align: left !important;
    margin-top: 12px;
  }
}

@media (min-width: 600px) and (max-width: 1023px) {
  .hero-title {
    font-size: 2.8rem;
  }

  .col-12.q-pr-xl {
    padding-right: 16px !important;
  }
}
</style>

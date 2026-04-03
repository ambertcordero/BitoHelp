<template>
  <q-page class="about-page">

    <!-- HERO ini !!!-->
    <section class="about-hero-section">
      <div class="container">
        <div class="row items-center">
          <div class="col-12 col-md-6">
            <h1 class="hero-title text-white">
              About BitoHelp
            </h1>
            <p class="hero-subtitle text-white">
              A blockchain-powered donation platform built to make charitable giving faster,
              cheaper, and fully transparent using Bitcoin Cash.
            </p>
          </div>
        </div>
      </div>
    </section>


    <!-- Story Section ini !!!-->
    <section class="q-py-xl q-px-md">
      <div class="container">
        <div class="row q-col-gutter-xl items-center">
          <div class="col-12 col-md-6">
            <div class="about-badge q-mb-md">Our Story</div>
            <h2 class="text-h3 text-weight-bold q-mb-md">Blockchain-Powered Social Impact</h2>
            <p class="text-body1 text-grey-8 q-mb-lg" style="line-height: 1.8">
              BitoHelp started as a capstone project with one question — why do charity platforms
              still charge 5–15% in processing fees when Bitcoin Cash can do it for less than
              a centavo?
            </p>
            <p class="text-body1 text-grey-8 q-mb-xl" style="line-height: 1.8">
              We built BitoHelp to prove that direct, trustless giving is not only possible —
              it is better. Every donation is on-chain, every charity is vetted, and every
              peso goes where it is supposed to go.
            </p>

            <div class="row q-col-gutter-md q-mb-lg">
              <div class="col-12 col-sm-6">
                <div class="feature-box">
                  <q-icon name="verified_user" size="32px" color="primary" class="q-mb-sm" />
                  <div class="text-subtitle1 text-weight-bold q-mb-xs">100% Transparent</div>
                  <p class="text-caption text-grey-7">All transactions on blockchain</p>
                </div>
              </div>
              <div class="col-12 col-sm-6">
                <div class="feature-box">
                  <q-icon name="speed" size="32px" color="positive" class="q-mb-sm" />
                  <div class="text-subtitle1 text-weight-bold q-mb-xs">Instant Transfers</div>
                  <p class="text-caption text-grey-7">Real-time donation processing</p>
                </div>
              </div>
              <div class="col-12 col-sm-6">
                <div class="feature-box">
                  <q-icon name="public" size="32px" color="secondary" class="q-mb-sm" />
                  <div class="text-subtitle1 text-weight-bold q-mb-xs">Global Reach</div>
                  <p class="text-caption text-grey-7">Support causes worldwide</p>
                </div>
              </div>
              <div class="col-12 col-sm-6">
                <div class="feature-box">
                  <q-icon name="security" size="32px" color="orange" class="q-mb-sm" />
                  <div class="text-subtitle1 text-weight-bold q-mb-xs">Secure Platform</div>
                  <p class="text-caption text-grey-7">Smart contract powered</p>
                </div>
              </div>
            </div>
          </div>

          <div class="col-12 col-md-6">
            <div class="about-main-image q-mb-sm">
              <img src="~assets/hero.png" alt="BitoHelp Platform" />
            </div>
            <div class="row q-col-gutter-sm">
              <div class="col-6">
                <div class="about-small-image">
                  <img src="~assets/community.jpg" alt="Community" />
                </div>
              </div>
              <div class="col-6">
                <div class="about-small-image">
                  <img src="~assets/medical.jpg" alt="Medical" />
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>


    <!-- Team Section ini !!!-->
    <section class="team-section q-py-xl q-px-md">
      <div class="container">
        <h2 class="text-h3 text-weight-bold q-mb-sm">Meet the Team</h2>
        <p class="text-body1 text-grey-7 q-mb-xl">
          The developers and advocates behind BitoHelp.
        </p>

        <div class="row q-col-gutter-lg">

          <!-- Card 1 -->
          <div class="col-12 col-sm-6 col-md-3">
            <div class="team-card">
              <div class="team-card-banner" style="background: linear-gradient(135deg, #1565c0, #42a5f5);"></div>
              <div class="team-card-body">
                <div class="team-avatar" style="background: linear-gradient(135deg, #1565c0, #0d47a1);">
                  <span>JD</span>
                </div>
                <div class="team-name">Juan Dela Cruz</div>
                <div class="team-role" style="color: #1565c0;">Lead Developer</div>
                <div class="team-divider"></div>
                <p class="team-bio">Full-stack developer, Vue.js frontend &amp; BCH blockchain integrations.</p>
                <div class="team-tags">
                  <span class="team-tag">Vue.js</span>
                  <span class="team-tag">BCH</span>
                </div>
              </div>
            </div>
          </div>

          <!-- Card 2 -->
          <div class="col-12 col-sm-6 col-md-3">
            <div class="team-card">
              <div class="team-card-banner" style="background: linear-gradient(135deg, #2e7d32, #66bb6a);"></div>
              <div class="team-card-body">
                <div class="team-avatar" style="background: linear-gradient(135deg, #2e7d32, #1b5e20);">
                  <span>BE</span>
                </div>
                <div class="team-name">Backend Engineer</div>
                <div class="team-role" style="color: #2e7d32;">Django / API</div>
                <div class="team-divider"></div>
                <p class="team-bio">REST API design, donation models, payout workflows and admin portal.</p>
                <div class="team-tags">
                  <span class="team-tag">Django</span>
                  <span class="team-tag">REST API</span>
                </div>
              </div>
            </div>
          </div>

          <!-- Card 3 -->
          <div class="col-12 col-sm-6 col-md-3">
            <div class="team-card">
              <div class="team-card-banner" style="background: linear-gradient(135deg, #e65100, #ff8a65);"></div>
              <div class="team-card-body">
                <div class="team-avatar" style="background: linear-gradient(135deg, #e65100, #bf360c);">
                  <span>BS</span>
                </div>
                <div class="team-name">BCH Specialist</div>
                <div class="team-role" style="color: #e65100;">Smart Contracts</div>
                <div class="team-divider"></div>
                <p class="team-bio">CashScript vault contracts and WalletConnect integration.</p>
                <div class="team-tags">
                  <span class="team-tag">CashScript</span>
                  <span class="team-tag">WalletConnect</span>
                </div>
              </div>
            </div>
          </div>

          <!-- Card 4 -->
          <div class="col-12 col-sm-6 col-md-3">
            <div class="team-card">
              <div class="team-card-banner" style="background: linear-gradient(135deg, #6a1b9a, #ce93d8);"></div>
              <div class="team-card-body">
                <div class="team-avatar" style="background: linear-gradient(135deg, #6a1b9a, #4a148c);">
                  <span>UD</span>
                </div>
                <div class="team-name">UI / UX Designer</div>
                <div class="team-role" style="color: #6a1b9a;">Design &amp; Research</div>
                <div class="team-divider"></div>
                <p class="team-bio">User experience &amp; accessible interface design.</p>
                <div class="team-tags">
                  <span class="team-tag">Figma</span>
                  <span class="team-tag">UX Research</span>
                </div>
              </div>
            </div>
          </div>

        </div>
      </div>
    </section>


    <!-- Impact Section ini !!!-->
      <section class="about-impact-section q-py-xl q-px-md" style="background: #f8f9fa;">
      <div class="container">
        <h2 class="text-h3 text-weight-bold q-mb-sm">Impact Report</h2>
        <p class="text-body1 text-grey-7 q-mb-xl">Real numbers, verifiable on-chain.</p>

        <div class="row q-col-gutter-lg q-mb-xl">
          <div class="col-12 col-md-4">
            <div class="metric-card">
              <div class="metric-number text-primary">500+</div>
              <div class="metric-label">Donations Processed</div>
              <div class="metric-description">Transactions recorded on Bitcoin Cash blockchain</div>
              <div class="metric-trend">
                <q-icon name="trending_up" color="positive" size="20px" />
                <span class="text-positive text-caption">Growing every day</span>
              </div>
            </div>
          </div>

          <div class="col-12 col-md-4">
            <div class="metric-card">
              <div class="metric-number text-positive">30+</div>
              <div class="metric-label">Verified Charities</div>
              <div class="metric-description">Nonprofits registered and verified on the platform</div>
              <div class="metric-trend">
                <q-icon name="verified" color="positive" size="20px" />
                <span class="text-grey-7 text-caption">100% vetted</span>
              </div>
            </div>
          </div>

          <div class="col-12 col-md-4">
            <div class="metric-card">
              <div class="metric-number text-secondary">100%</div>
              <div class="metric-label">On-Chain Transparency</div>
              <div class="metric-description">Every donation has a verifiable transaction ID</div>
              <div class="metric-trend">
                <q-icon name="link" color="positive" size="20px" />
                <span class="text-grey-7 text-caption">Explorer verifiable</span>
              </div>
            </div>
          </div>
        </div>

        <!-- Impact stories -->
        <div class="row q-col-gutter-lg">
          <div class="col-12 col-md-6">
            <div class="impact-story-card">
              <div class="row q-col-gutter-md items-center">
                <div class="col-4">
                  <div class="story-image">
                    <img src="~assets/scholar.jpg" alt="Education" />
                  </div>
                </div>
                <div class="col-8">
                  <div class="story-stat text-h4 text-weight-bold text-primary">518</div>
                  <div class="text-subtitle2 text-weight-bold q-mb-xs">Students Received Scholarships</div>
                  <p class="text-body2 text-grey-7">
                    Full-year scholarships, supplies, and devices for students in underserved communities.
                  </p>
                </div>
              </div>
            </div>
          </div>

          <div class="col-12 col-md-6">
            <div class="impact-story-card">
              <div class="row q-col-gutter-md items-center">
                <div class="col-4">
                  <div class="story-image">
                    <img src="~assets/typhoon.jpeg" alt="Disaster" />
                  </div>
                </div>
                <div class="col-8">
                  <div class="story-stat text-h4 text-weight-bold text-orange">892</div>
                  <div class="text-subtitle2 text-weight-bold q-mb-xs">Families Helped in Disasters</div>
                  <p class="text-body2 text-grey-7">
                    Food, shelter, and relief supplies to families hit by typhoons and floods.
                  </p>
                </div>
              </div>
            </div>
          </div>

          <div class="col-12 col-md-6">
            <div class="impact-story-card">
              <div class="row q-col-gutter-md items-center">
                <div class="col-4">
                  <div class="story-image">
                    <img src="~assets/medical.jpg" alt="Medical" />
                  </div>
                </div>
                <div class="col-8">
                  <div class="story-stat text-h4 text-weight-bold text-positive">1,247</div>
                  <div class="text-subtitle2 text-weight-bold q-mb-xs">Medical Treatments Funded</div>
                  <p class="text-body2 text-grey-7">
                    Emergency care and medications for families who couldn't afford treatment.
                  </p>
                </div>
              </div>
            </div>
          </div>

          <div class="col-12 col-md-6">
            <div class="impact-story-card">
              <div class="row q-col-gutter-md items-center">
                <div class="col-4">
                  <div class="story-image">
                    <img src="~assets/community.jpg" alt="Community" />
                  </div>
                </div>
                <div class="col-8">
                  <div class="story-stat text-h4 text-weight-bold text-secondary">43</div>
                  <div class="text-subtitle2 text-weight-bold q-mb-xs">Community Projects Launched</div>
                  <p class="text-body2 text-grey-7">
                    Farming, clean water, and livelihood programs across rural communities.
                  </p>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- CTA -->
        <div class="impact-cta-section q-mt-xl">
          <div class="row items-center q-col-gutter-lg">
            <div class="col-12 col-md-7">
              <h3 class="text-h4 text-weight-bold q-mb-sm">Join Us in Making a Difference</h3>
              <p class="text-body1 text-grey-7">
                Start your donation journey and be part of a global community doing transparent, impactful giving.
              </p>
            </div>
            <div class="col-12 col-md-5 text-right">
              <q-btn
                label="Start Donating"
                size="lg"
                unelevated
                color="primary"
                padding="12px 48px"
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
import { onMounted } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()

onMounted(() => {
  const tab = route.query?.tab
  // tab value can be used for anchor scrolling in future
  if (tab) {
    const el = document.getElementById(`section-${tab}`)
    if (el) el.scrollIntoView({ behavior: 'smooth' })
  }
})
</script>

<style scoped>
.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 24px;
}

/* HERO */
.about-hero-section {
  min-height: 50vh;
  background-image: url('../assets/unity.jpg');
  background-size: cover;
  background-position: center;
  position: relative;
  display: flex;
  align-items: center;
  padding: 80px 24px;
}

.about-hero-section::before {
  content: '';
  position: absolute;
  inset: 0;
  background: rgba(13, 71, 161, 0.72);
}

.about-hero-section .container {
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

/* About badge */
.about-badge {
  display: inline-block;
  background: #e3f2fd;
  color: #1565c0;
  font-size: 12px;
  font-weight: 700;
  letter-spacing: 1px;
  text-transform: uppercase;
  padding: 6px 14px;
  border-radius: 20px;
}

/* Feature boxes */
.feature-box {
  padding: 16px;
  border: 1px solid #e0e0e0;
  border-radius: 12px;
  background: white;
}

/* About images */
.about-main-image {
  width: 100%;
  height: 280px;
  border-radius: 16px;
  overflow: hidden;
}

.about-main-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.about-small-image {
  width: 100%;
  height: 130px;
  border-radius: 12px;
  overflow: hidden;
}

.about-small-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

/* Team */
.team-section {
  background: white;
}

.team-card {
  border-radius: 16px;
  overflow: hidden;
  border: 1px solid #e0e0e0;
  background: white;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.team-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 12px 32px rgba(0, 0, 0, 0.12);
}

.team-card-banner {
  height: 72px;
  width: 100%;
}

.team-card-body {
  padding: 0 20px 24px;
  text-align: center;
}

.team-avatar {
  width: 72px;
  height: 72px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: -36px auto 14px;
  border: 3px solid white;
  box-shadow: 0 4px 14px rgba(0, 0, 0, 0.18);
  font-size: 20px;
  font-weight: 800;
  color: white;
  letter-spacing: 1px;
}

.team-name {
  font-size: 15px;
  font-weight: 700;
  color: #111;
  margin-bottom: 4px;
}

.team-role {
  font-size: 12px;
  font-weight: 600;
  letter-spacing: 0.5px;
  text-transform: uppercase;
  margin-bottom: 12px;
}

.team-divider {
  height: 1px;
  background: #f0f0f0;
  margin: 10px 0 12px;
}

.team-bio {
  font-size: 12.5px;
  color: #666;
  line-height: 1.6;
  margin-bottom: 14px;
}

.team-tags {
  display: flex;
  gap: 6px;
  justify-content: center;
  flex-wrap: wrap;
}

.team-tag {
  font-size: 11px;
  font-weight: 600;
  background: #f0f4ff;
  color: #1565c0;
  padding: 3px 10px;
  border-radius: 20px;
}

/* Metric cards */
.metric-card {
  background: white;
  border-radius: 16px;
  padding: 28px;
  border: 1px solid #e0e0e0;
  height: 100%;
}

.metric-number {
  font-size: 2.8rem;
  font-weight: 800;
  line-height: 1;
  margin-bottom: 8px;
}

.metric-label {
  font-size: 16px;
  font-weight: 700;
  margin-bottom: 8px;
  color: #333;
}

.metric-description {
  font-size: 13px;
  color: #666;
  line-height: 1.6;
  margin-bottom: 12px;
}

.metric-trend {
  display: flex;
  align-items: center;
  gap: 6px;
}

/* Impact stories */
.impact-story-card {
  background: white;
  border-radius: 16px;
  padding: 20px;
  border: 1px solid #e0e0e0;
  margin-bottom: 8px;
}

.story-image {
  width: 100%;
  height: 100px;
  border-radius: 10px;
  overflow: hidden;
}

.story-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.story-stat {
  line-height: 1;
  margin-bottom: 6px;
}

.impact-cta-section {
  background: #e3f2fd;
  border-radius: 20px;
  padding: 32px 36px;
}

/* ── Dark Mode ──────────────────────────────────────────────── */
.body--dark .about-page {
  background: #0d1117;
}

/* Story section */
.body--dark .about-badge {
  background: rgba(21, 101, 192, 0.2);
  color: #90caf9;
}

.body--dark .feature-box {
  background: #1e2a3a;
  border-color: rgba(255, 255, 255, 0.08);
}

/* Team section */
.body--dark .team-section {
  background: #0f1629;
}

.body--dark .team-card {
  background: #1e2a3a;
  border-color: rgba(255, 255, 255, 0.08);
}

.body--dark .team-card:hover {
  box-shadow: 0 12px 32px rgba(0, 0, 0, 0.4);
}

.body--dark .team-card-body .team-avatar {
  border-color: #1e2a3a;
}

.body--dark .team-name {
  color: #e0e0e0;
}

.body--dark .team-bio {
  color: #9e9e9e;
}

.body--dark .team-divider {
  background: rgba(255, 255, 255, 0.08);
}

.body--dark .team-tag {
  background: rgba(21, 101, 192, 0.18);
  color: #90caf9;
}

/* Impact section */
.body--dark .about-impact-section {
  background: #131d35 !important;
}

.body--dark .metric-card {
  background: #1e2a3a;
  border-color: rgba(255, 255, 255, 0.08);
}

.body--dark .metric-label {
  color: #e0e0e0;
}

.body--dark .metric-description {
  color: #9e9e9e;
}

.body--dark .impact-story-card {
  background: #1e2a3a;
  border-color: rgba(255, 255, 255, 0.08);
}

.body--dark .impact-cta-section {
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

  .about-hero-section {
    padding: 60px 16px 40px;
    min-height: 45vh;
  }

  .about-main-image {
    height: 200px;
  }

  .about-small-image {
    height: 90px;
  }

  /* Team cards — single column, no gutter overflow */
  .team-card-body {
    padding: 0 14px 20px;
  }

  .metric-number {
    font-size: 2.2rem;
  }

  .metric-card {
    padding: 20px 16px;
  }

  .impact-story-card {
    padding: 14px;
  }

  .story-image {
    height: 76px;
  }

  /* CTA section */
  .impact-cta-section {
    padding: 24px 20px;
  }

  .impact-cta-section .col-12.text-right {
    text-align: left !important;
    margin-top: 12px;
  }
}

@media (min-width: 600px) and (max-width: 1023px) {
  .hero-title {
    font-size: 2.6rem;
  }

  .about-main-image {
    height: 240px;
  }
}
</style>

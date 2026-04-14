<template>
  <q-page>
    <!-- HERO ini !!!-->
    <section class="hero-section">
      <div class="row items-center justify-between q-pa-xl full-width">
        <div class="col-12 col-md-6 hero-content">
          <h1 class="hero-title">
            Donate Bitcoin<br />
            <span class="highlight">Change Lives</span>
          </h1>

          <p class="hero-subtitle">
            Helping the world with fast, transparent blockchain-powered donations.
          </p>

          <div class="hero-buttons q-mt-lg">
            <q-btn
              v-if="isConnected && isNonprofit"
              label="View Donations"
              color="positive"
              size="lg"
              unelevated
              class="hero-btn"
              icon="dashboard"
              to="/dashboard"
            />
            <q-btn
              v-if="isConnected && !isNonprofit && !checkingRole"
              label="Start Donating"
              color="primary"
              size="lg"
              unelevated
              class="hero-btn"
              to="/donate"
            />
            <q-btn
              label="Learn More"
              size="lg"
              outline
              class="hero-btn-outline"
              @click="$router.push('/donate')"
            />
          </div>
        </div>
      </div>
    </section>

    <section class="featured-projects-section q-py-xl q-px-md">
      <div class="container">
        <div class="q-mb-xl">
          <h2 class="section-title text-h3 text-weight-bold q-mb-sm">Featured Projects</h2>
          <p class="text-subtitle1 text-grey-6">
            Support impactful causes and make a difference in communities worldwide.
          </p>
        </div>
        <div class="row q-col-gutter-lg">
          <div class="col-12 col-sm-6 col-md-3">
            <q-card class="project-card" flat bordered>
              <div class="project-image">
                <img src="~assets/scholar.jpg" alt="Project" />
                <q-badge color="primary" class="project-badge">Open</q-badge>
              </div>
              <q-card-section>
                <div class="text-h6 text-weight-bold q-mb-sm">Education Scholarship Program</div>
                <p class="text-body2 text-grey-7 q-mb-md project-description">
                  Help provide quality education and school supplies to underprivileged children,
                  empowering them with knowledge and opportunity.
                </p>

                <div class="project-progress q-mb-sm">
                  <div class="row items-center justify-between q-mb-xs">
                    <span class="text-caption text-grey-7">Progress</span>
                    <span class="text-caption text-weight-bold">75% Funded</span>
                  </div>
                  <q-linear-progress :value="0.75" color="primary" rounded size="8px" />
                </div>
                <div class="row items-center q-mt-md">
                  <q-avatar size="24px" color="green-2" text-color="green" icon="verified">
                  </q-avatar>
                </div>
              </q-card-section>
            </q-card>
          </div>

          <div class="col-12 col-sm-6 col-md-3">
            <q-card class="project-card" flat bordered>
              <div class="project-image">
                <img src="~assets/medical.jpg" alt="Project" />
                <q-badge color="positive" class="project-badge">Open</q-badge>
              </div>
              <q-card-section>
                <div class="text-h6 text-weight-bold q-mb-sm">Medical Care Support</div>
                <p class="text-body2 text-grey-7 q-mb-md project-description">
                  Provide essential medical supplies, treatments, and healthcare services to
                  communities in need of immediate assistance.
                </p>

                <div class="project-progress q-mb-sm">
                  <div class="row items-center justify-between q-mb-xs">
                    <span class="text-caption text-grey-7">Progress</span>
                    <span class="text-caption text-weight-bold">82% Funded</span>
                  </div>
                  <q-linear-progress :value="0.82" color="positive" rounded size="8px" />
                </div>

                <div class="row items-center q-mt-md">
                  <q-avatar size="24px" color="orange-2" text-color="orange" icon="emoji_events">
                  </q-avatar>
                </div>
              </q-card-section>
            </q-card>
          </div>

          <div class="col-12 col-sm-6 col-md-3">
            <q-card class="project-card" flat bordered>
              <div class="project-image">
                <img src="~assets/typhoon.jpeg" alt="Project" />
                <q-badge color="info" class="project-badge">Open</q-badge>
              </div>
              <q-card-section>
                <div class="text-h6 text-weight-bold q-mb-sm">Disaster Relief Fund</div>
                <p class="text-body2 text-grey-7 q-mb-md project-description">
                  Rapid response support for families affected by typhoons, floods, and natural
                  disasters with food, shelter, and supplies.
                </p>

                <div class="project-progress q-mb-sm">
                  <div class="row items-center justify-between q-mb-xs">
                    <span class="text-caption text-grey-7">Progress</span>
                    <span class="text-caption text-weight-bold">68% Funded</span>
                  </div>
                  <q-linear-progress :value="0.68" color="info" rounded size="8px" />
                </div>

                <div class="row items-center q-mt-md">
                  <q-avatar size="24px" color="blue-2" text-color="blue" icon="favorite">
                  </q-avatar>
                </div>
              </q-card-section>
            </q-card>
          </div>

          <div class="col-12 col-sm-6 col-md-3">
            <q-card class="project-card" flat bordered>
              <div class="project-image">
                <img src="~assets/community.jpg" alt="Project" />
                <q-badge color="positive" class="project-badge">Open</q-badge>
              </div>
              <q-card-section>
                <div class="text-h6 text-weight-bold q-mb-sm">Community Development</div>
                <p class="text-body2 text-grey-7 q-mb-md project-description">
                  Support sustainable farming, livelihood programs, and skill development projects
                  to lift communities out of poverty.
                </p>

                <div class="project-progress q-mb-sm">
                  <div class="row items-center justify-between q-mb-xs">
                    <span class="text-caption text-grey-7">Progress</span>
                    <span class="text-caption text-weight-bold">91% Funded</span>
                  </div>
                  <q-linear-progress :value="0.91" color="positive" rounded size="8px" />
                </div>

                <div class="row items-center q-mt-md">
                  <q-avatar
                    size="24px"
                    color="orange-2"
                    text-color="orange"
                    icon="local_fire_department"
                  >
                  </q-avatar>
                </div>
              </q-card-section>
            </q-card>
          </div>
        </div>
      </div>
    </section>

    <section class="mission-section q-py-xl q-px-md">
      <div class="container">
        <div class="row">
          <div class="col-12 col-md-5 q-pr-xl">
            <h2 class="mission-heading text-weight-bold q-mb-lg">Our Mission</h2>

            <p class="mission-description text-body1 text-grey-8">
              We empower donors and nonprofits by providing a transparent, blockchain-based donation
              platform where every transaction is verifiable and impactful.<br />
              We empower donors and nonprofits by providing a transparent, blockchain-based donation
              platform where every transaction is verifiable and impactful.<br />
              We empower donors and nonprofits.
            </p>

            <div class="mission-visual-grid q-mt-xl">
              <div class="row q-col-gutter-sm">
                <div class="col-6">
                  <div class="mission-photo-box">
                    <img src="~assets/unity.jpg" alt="Donation" />
                  </div>
                </div>
                <div class="col-6">
                  <div class="mission-photo-box">
                    <img src="~assets/medically.jpg" alt="Community" />
                  </div>
                </div>
              </div>
            </div>
          </div>

          <div class="col-12 col-md-7">
            <div class="mission-grid">
              <div class="mission-grid-item mission-large-photo">
                <img src="~assets/teacher.jpg" alt="Helping Community" />
              </div>
              <div class="row q-col-gutter-sm q-mt-sm">
                <div class="col-4">
                  <div class="mission-photo-box">
                    <img src="~assets/medical.jpg" alt="Medical Support" />
                  </div>
                </div>
                <div class="col-4">
                  <div class="mission-photo-box">
                    <img src="~assets/rescue.jpg" alt="Team Collaboration" />
                  </div>
                </div>
                <div class="col-4">
                  <div class="mission-photo-box">
                    <img src="~assets/planting.jpg" alt="Community Project" />
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div class="row q-col-gutter-md q-mt-xl q-pt-xl">
          <div class="col-12 col-sm-4 text-center">
            <div class="stat-card q-pa-md">
              <div class="text-h3 text-weight-bold text-primary">$2.5M+</div>
              <div class="text-subtitle1 text-grey-7">Total Donations</div>
            </div>
          </div>
          <div class="col-12 col-sm-4 text-center">
            <div class="stat-card q-pa-md">
              <div class="text-h3 text-weight-bold text-positive">5,000+</div>
              <div class="text-subtitle1 text-grey-7">Active Donors</div>
            </div>
          </div>
          <div class="col-12 col-sm-4 text-center">
            <div class="stat-card q-pa-md">
              <div class="text-h3 text-weight-bold text-secondary">150+</div>
              <div class="text-subtitle1 text-grey-7">Nonprofits Supported</div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <section class="why-donate-section q-py-xl q-px-md">
      <div class="container">
        <div class="row q-mb-xl">
          <div class="col-12 col-md-8">
            <h2 class="text-h3 text-weight-bold q-mb-md">Why Donate with Cryptocurrency?</h2>
            <p class="text-body1 text-grey-8" style="line-height: 1.8">
              Blockchain technology offers a modern approach to charitable giving. Here's what makes
              cryptocurrency donations different and why organizations are increasingly adopting
              this method.
            </p>
          </div>
        </div>

        <div class="row q-col-gutter-lg q-mb-xl">
          <div class="col-12 col-md-6">
            <div class="crypto-benefit-card">
              <div class="benefit-header q-mb-md">
                <div class="benefit-number">01</div>
                <h3 class="text-h5 text-weight-bold">Complete Transaction Transparency</h3>
              </div>
              <p class="text-body1 text-grey-8 q-mb-md" style="line-height: 1.7">
                Every donation is permanently recorded on the blockchain. You can track exactly
                where your funds go, from your wallet to the nonprofit's address, and verify that
                they were used as intended.
              </p>
              <div class="benefit-detail">
                <q-chip dense color="blue-1" text-color="primary" icon="verified">
                  <span class="text-weight-medium">100% Verifiable</span>
                </q-chip>
                <q-chip dense color="blue-1" text-color="primary" icon="timeline">
                  <span class="text-weight-medium">Real-time Tracking</span>
                </q-chip>
              </div>
            </div>
          </div>

          <div class="col-12 col-md-6">
            <div class="crypto-benefit-card">
              <div class="benefit-header q-mb-md">
                <div class="benefit-number">02</div>
                <h3 class="text-h5 text-weight-bold">Lower Processing Fees</h3>
              </div>
              <p class="text-body1 text-grey-8 q-mb-md" style="line-height: 1.7">
                Traditional payment processors charge 2-3% plus fixed fees. Bitcoin Cash
                transactions typically cost less than $0.01, meaning more of your donation directly
                supports the cause.
              </p>
              <div class="benefit-detail">
                <div class="fee-comparison">
                  <div class="fee-item">
                    <span class="text-caption text-grey-6">Traditional:</span>
                    <span class="text-weight-bold text-negative">2.9% + $0.30</span>
                  </div>
                  <div class="fee-item">
                    <span class="text-caption text-grey-6">Bitcoin Cash:</span>
                    <span class="text-weight-bold text-positive">&lt;$0.01</span>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <div class="col-12 col-md-6">
            <div class="crypto-benefit-card">
              <div class="benefit-header q-mb-md">
                <div class="benefit-number">03</div>
                <h3 class="text-h5 text-weight-bold">Instant Global Transfers</h3>
              </div>
              <p class="text-body1 text-grey-8 q-mb-md" style="line-height: 1.7">
                Send funds anywhere in the world without intermediaries, currency conversion fees,
                or multi-day processing times. Perfect for emergency disaster relief when time is
                critical.
              </p>
              <div class="benefit-detail">
                <q-chip dense color="green-1" text-color="positive" icon="schedule">
                  <span class="text-weight-medium">~10 seconds confirmation</span>
                </q-chip>
              </div>
            </div>
          </div>

          <div class="col-12 col-md-6">
            <div class="crypto-benefit-card">
              <div class="benefit-header q-mb-md">
                <div class="benefit-number">04</div>
                <h3 class="text-h5 text-weight-bold">No Geographic Restrictions</h3>
              </div>
              <p class="text-body1 text-grey-8 q-mb-md" style="line-height: 1.7">
                Support nonprofits in any country without dealing with international wire transfer
                fees, exchange rates, or banking restrictions that can block traditional donations.
              </p>
              <div class="benefit-detail">
                <q-chip dense color="purple-1" text-color="purple" icon="public">
                  <span class="text-weight-medium">158 countries served</span>
                </q-chip>
              </div>
            </div>
          </div>
        </div>

        <div class="q-mb-xl">
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
                <p class="text-caption text-grey-7">Local development programs</p>
              </div>
            </div>
          </div>
        </div>

        <div class="crypto-cta-section q-mt-xl q-pt-lg">
          <div class="row items-center">
            <div class="col-12 col-md-7">
              <h3 class="text-h5 text-weight-bold q-mb-sm">Ready to get started?</h3>
              <p class="text-body2 text-grey-7">
                Connect your Bitcoin Cash wallet and choose from verified nonprofits.
              </p>
            </div>
            <div class="col-12 col-md-5 text-right">
              <q-btn
                label="Explore Projects"
                color="primary"
                size="lg"
                unelevated
                padding="12px 32px"
                to="/charities"
              />
            </div>
          </div>
        </div>
      </div>
    </section>

    <section class="donation-matters-section q-py-xl q-px-md">
      <div class="container">
        <div class="q-mb-xl">
          <div class="row items-center justify-between">
            <div class="col-12 col-md-7">
              <h2 class="text-h3 text-weight-bold q-mb-md">Why Your Donation Matters</h2>
              <p class="text-body1 text-grey-8" style="line-height: 1.8">
                Your contribution through blockchain technology ensures transparency, speed, and
                direct impact. Every donation is tracked on-chain, providing you with complete
                visibility into how your funds make a difference.
              </p>
            </div>
            <div class="col-12 col-md-4 text-right">
              <div class="impact-year-badge">
                <div class="text-h4 text-weight-bold text-primary">2026</div>
                <div class="text-subtitle2 text-grey-7">Impact Report</div>
              </div>
            </div>
          </div>
        </div>

        <div class="row q-col-gutter-lg q-mb-xl">
          <div class="col-12 col-md-4">
            <div class="metric-card">
              <div class="metric-number text-primary">$2.5M+</div>
              <div class="metric-label">Total Raised</div>
              <div class="metric-description">
                In cryptocurrency donations processed through our platform
              </div>
              <div class="metric-trend">
                <q-icon name="trending_up" color="positive" size="20px" />
                <span class="text-positive text-caption">+127% from last year</span>
              </div>
            </div>
          </div>

          <div class="col-12 col-md-4">
            <div class="metric-card">
              <div class="metric-number text-positive">5,273</div>
              <div class="metric-label">Active Donors</div>
              <div class="metric-description">Individuals and organizations supporting causes</div>
              <div class="metric-trend">
                <q-icon name="trending_up" color="positive" size="20px" />
                <span class="text-positive text-caption">+89% from last year</span>
              </div>
            </div>
          </div>

          <div class="col-12 col-md-4">
            <div class="metric-card">
              <div class="metric-number text-secondary">158</div>
              <div class="metric-label">Verified Nonprofits</div>
              <div class="metric-description">Registered and verified organizations worldwide</div>
              <div class="metric-trend">
                <q-icon name="verified" color="positive" size="20px" />
                <span class="text-grey-7 text-caption">100% verified</span>
              </div>
            </div>
          </div>
        </div>

        <div class="row q-col-gutter-lg q-mb-xl">
          <div class="col-12">
            <h3 class="text-h5 text-weight-bold q-mb-md">Real Impact, Real Stories</h3>
          </div>

          <div class="col-12 col-md-6">
            <div class="impact-story-card">
              <div class="row q-col-gutter-md">
                <div class="col-4">
                  <div class="story-image">
                    <img src="~assets/scholar.jpg" alt="Education" />
                  </div>
                </div>
                <div class="col-8">
                  <div class="story-stat text-h4 text-weight-bold text-primary">518</div>
                  <div class="story-title text-subtitle1 text-weight-bold q-mb-sm">
                    Students Received Scholarships
                  </div>
                  <p class="story-text text-body2 text-grey-7">
                    Funded full-year scholarships, school supplies, and educational technology for
                    students in underserved communities.
                  </p>
                </div>
              </div>
            </div>
          </div>

          <div class="col-12 col-md-6">
            <div class="impact-story-card">
              <div class="row q-col-gutter-md">
                <div class="col-4">
                  <div class="story-image">
                    <img src="~assets/medical.jpg" alt="Healthcare" />
                  </div>
                </div>
                <div class="col-8">
                  <div class="story-stat text-h4 text-weight-bold text-positive">1,247</div>
                  <div class="story-title text-subtitle1 text-weight-bold q-mb-sm">
                    Medical Treatments Provided
                  </div>
                  <p class="story-text text-body2 text-grey-7">
                    Emergency medical care, essential medications, and health services delivered to
                    families in crisis situations.
                  </p>
                </div>
              </div>
            </div>
          </div>

          <div class="col-12 col-md-6">
            <div class="impact-story-card">
              <div class="row q-col-gutter-md">
                <div class="col-4">
                  <div class="story-image">
                    <img src="~assets/typhoon.jpeg" alt="Disaster Relief" />
                  </div>
                </div>
                <div class="col-8">
                  <div class="story-stat text-h4 text-weight-bold text-orange">892</div>
                  <div class="story-title text-subtitle1 text-weight-bold q-mb-sm">
                    Families Assisted in Disasters
                  </div>
                  <p class="story-text text-body2 text-grey-7">
                    Rapid response support including food, shelter, and essential supplies for
                    families affected by natural disasters.
                  </p>
                </div>
              </div>
            </div>
          </div>

          <div class="col-12 col-md-6">
            <div class="impact-story-card">
              <div class="row q-col-gutter-md">
                <div class="col-4">
                  <div class="story-image">
                    <img src="~assets/community.jpg" alt="Community" />
                  </div>
                </div>
                <div class="col-8">
                  <div class="story-stat text-h4 text-weight-bold text-secondary">43</div>
                  <div class="story-title text-subtitle1 text-weight-bold q-mb-sm">
                    Community Projects Launched
                  </div>
                  <p class="story-text text-body2 text-grey-7">
                    Sustainable farming, clean water, and livelihood programs helping communities
                    build long-term self-sufficiency.
                  </p>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div class="impact-cta-section q-mt-xl q-pt-xl">
          <div class="row items-center q-col-gutter-lg">
            <div class="col-12 col-md-7">
              <h3 class="text-h4 text-weight-bold q-mb-sm">Join Us in Making a Difference</h3>
              <p class="text-body1 text-grey-7">
                Start your donation journey today and become part of a global community committed to
                transparent, impactful giving.
              </p>
            </div>
            <div class="col-12 col-md-5 text-right">
              <q-btn
                label="Start Donating"
                size="lg"
                unelevated
                color="primary"
                padding="12px 48px"
                to="/donor"
                class="impact-cta-button"
              />
            </div>
          </div>
        </div>
      </div>
    </section>

    <section class="testimonials-section q-py-xl q-px-md">
      <div class="container">
        <div class="text-center q-mb-xl animate-slide-up">
          <h2 class="section-title text-h3 text-weight-bold q-mb-md">What People Are Saying</h2>
          <p class="text-h6 text-grey-7 q-mb-lg" style="max-width: 700px; margin: 0 auto">
            Hear from donors and beneficiaries about their experience with blockchain-powered giving
          </p>
        </div>

        <div class="row q-col-gutter-lg">
          <div
            class="col-12 col-md-4 animate-fade-slide-up"
            v-for="(t, index) in testimonials"
            :key="t.name"
            :style="{ animationDelay: 0.2 + index * 0.2 + 's' }"
          >
            <q-card class="testimonial-card full-height" flat bordered>
              <div class="quote-icon-wrapper">
                <q-icon name="format_quote" size="48px" color="primary" />
              </div>

              <q-card-section class="q-pa-lg">
                <p class="testimonial-text text-body1 q-mb-lg">"{{ t.text }}"</p>

                <div class="row items-center">
                  <q-avatar size="56px" class="q-mr-md">
                    <img :src="t.image" alt="t.name" />
                  </q-avatar>
                  <div>
                    <div class="text-subtitle1 text-weight-bold">{{ t.name }}</div>
                    <div class="text-caption text-grey-7">{{ t.role }}</div>
                  </div>
                </div>
              </q-card-section>

              <q-card-section class="q-pt-none q-px-lg q-pb-lg">
                <div class="row items-center">
                  <q-icon name="star" size="20px" color="amber" v-for="n in 5" :key="n" />
                </div>
              </q-card-section>
            </q-card>
          </div>
        </div>

        <div class="trust-section q-mt-xl q-pt-xl">
          <div class="text-center q-mb-lg animate-slide-up" style="animation-delay: 0.8s">
            <div class="text-h5 text-weight-bold text-grey-8 q-mb-sm">
              Trusted by Organizations Worldwide
            </div>
            <p class="text-body1 text-grey-7">Join thousands of donors making a verified impact</p>
          </div>

          <div class="row q-col-gutter-md justify-center items-center">
            <div class="col-auto trust-badge animate-scale-in" style="animation-delay: 1s">
              <q-icon name="verified" size="32px" color="primary" class="q-mr-sm" />
              <span class="text-weight-medium">Blockchain Verified</span>
            </div>
            <div class="col-auto trust-badge animate-scale-in" style="animation-delay: 1.1s">
              <q-icon name="security" size="32px" color="positive" class="q-mr-sm" />
              <span class="text-weight-medium">Secure Transactions</span>
            </div>
            <div class="col-auto trust-badge animate-scale-in" style="animation-delay: 1.2s">
              <q-icon name="public" size="32px" color="secondary" class="q-mr-sm" />
              <span class="text-weight-medium">Global Network</span>
            </div>
          </div>
        </div>
      </div>
    </section>

    <section class="about-impact-section q-py-xl q-px-md">
      <div class="container">
        <div class="row justify-center">
          <div class="col-12 col-md-10">
            <div class="about-content-professional">
              <div class="row q-col-gutter-xl items-center">
                <div class="col-12 col-md-6">
                  <div class="about-badge q-mb-md">About CrypToCare</div>
                  <h2 class="text-h3 text-weight-bold q-mb-md">Blockchain-Powered Social Impact</h2>
                  <p class="text-body1 text-grey-8 q-mb-lg" style="line-height: 1.8">
                    Founded in 2026, CrypToCare is a cryptocurrency donation platform built on
                    transparency, innovation, and social responsibility. We leverage blockchain
                    technology to create a trusted bridge between donors and verified nonprofits
                    worldwide.
                  </p>
                  <p class="text-body1 text-grey-8 q-mb-xl" style="line-height: 1.8">
                    Every donation is tracked on-chain, ensuring complete visibility and
                    accountability. Our mission is to make charitable giving more accessible,
                    efficient, and impactful through the power of Bitcoin Cash.
                  </p>

                  <div class="key-features">
                    <div class="row q-col-gutter-md q-mb-lg">
                      <div class="col-12 col-sm-6">
                        <div class="feature-box">
                          <q-icon
                            name="verified_user"
                            size="32px"
                            color="primary"
                            class="q-mb-sm"
                          />
                          <div class="text-subtitle1 text-weight-bold q-mb-xs">
                            100% Transparent
                          </div>
                          <p class="text-caption text-grey-7">All transactions on blockchain</p>
                        </div>
                      </div>
                      <div class="col-12 col-sm-6">
                        <div class="feature-box">
                          <q-icon name="speed" size="32px" color="positive" class="q-mb-sm" />
                          <div class="text-subtitle1 text-weight-bold q-mb-xs">
                            Instant Transfers
                          </div>
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
                          <p class="text-caption text-grey-7">Bank-grade encryption</p>
                        </div>
                      </div>
                    </div>
                  </div>

                  <div class="q-mt-lg">
                    <q-btn
                      label="Learn More About Our Mission"
                      color="primary"
                      size="lg"
                      unelevated
                      padding="12px 32px"
                      class="about-cta-btn"
                    />
                  </div>
                </div>

                <div class="col-12 col-md-6">
                  <div class="about-visual-section">
                    <div class="about-main-image q-mb-md">
                      <img src="~assets/hero.png" alt="CrypToCare Platform" />
                    </div>
                    <div class="row q-col-gutter-sm">
                      <div class="col-6">
                        <div class="about-small-image">
                          <img src="~assets/community.jpg" alt="Community Impact" />
                        </div>
                      </div>
                      <div class="col-6">
                        <div class="about-small-image">
                          <img src="~assets/medical.jpg" alt="Healthcare Support" />
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <footer class="main-footer">
      <div class="footer-top">
        <div class="container">
          <div class="row q-col-gutter-lg">
            <div class="col-12 col-md-4">
              <div class="footer-brand-section">
                <div class="footer-logo q-mb-md">
                  <img src="~assets/image1.png" alt="CrypToCare" class="footer-logo-img" />
                  <span class="footer-brand-name">CrypToCare</span>
                </div>
                <p class="footer-description text-body2 q-mb-lg">
                  Empowering social impact through transparent blockchain-powered cryptocurrency
                  donations. Join us in making the world a better place.
                </p>
                <div class="social-links">
                  <a href="#" class="social-link" aria-label="Facebook">
                    <q-icon name="fab fa-facebook" size="24px" />
                  </a>
                  <a href="#" class="social-link" aria-label="Twitter">
                    <q-icon name="fab fa-twitter" size="24px" />
                  </a>
                  <a href="#" class="social-link" aria-label="LinkedIn">
                    <q-icon name="fab fa-linkedin" size="24px" />
                  </a>
                  <a href="#" class="social-link" aria-label="Instagram">
                    <q-icon name="fab fa-instagram" size="24px" />
                  </a>
                </div>
              </div>
            </div>

            <div class="col-6 col-md-2">
              <div class="footer-column">
                <h4 class="footer-title">About</h4>
                <ul class="footer-links">
                  <li><a href="#" class="footer-link">About Us</a></li>
                  <li><a href="#" class="footer-link">Our Mission</a></li>
                  <li><a href="#" class="footer-link">Our Impact</a></li>
                  <li><a href="#" class="footer-link">Team</a></li>
                  <li><a href="#" class="footer-link">Careers</a></li>
                </ul>
              </div>
            </div>

            <div class="col-6 col-md-2">
              <div class="footer-column">
                <h4 class="footer-title">For Donors</h4>
                <ul class="footer-links">
                  <li><a href="/donate" class="footer-link">Donate Now</a></li>
                  <li><a href="#" class="footer-link">Explore Causes</a></li>
                  <li><a href="#" class="footer-link">How It Works</a></li>
                  <li><a href="#" class="footer-link">Transparency</a></li>
                  <li><a href="#" class="footer-link">Tax Receipts</a></li>
                </ul>
              </div>
            </div>

            <div class="col-6 col-md-2">
              <div class="footer-column">
                <h4 class="footer-title">Nonprofits</h4>
                <ul class="footer-links">
                  <li><a href="#" class="footer-link">Getting Started</a></li>
                  <li><a href="#" class="footer-link">Register</a></li>
                  <li><a href="#" class="footer-link">Resources</a></li>
                  <li><a href="#" class="footer-link">Success Stories</a></li>
                  <li><a href="#" class="footer-link">Support</a></li>
                </ul>
              </div>
            </div>

            <div class="col-6 col-md-2">
              <div class="footer-column">
                <h4 class="footer-title">Resources</h4>
                <ul class="footer-links">
                  <li><a href="#" class="footer-link">Blog</a></li>
                  <li><a href="#" class="footer-link">Help Center</a></li>
                  <li><a href="#" class="footer-link">FAQs</a></li>
                  <li><a href="#" class="footer-link">Contact Us</a></li>
                  <li><a href="#" class="footer-link">Press Kit</a></li>
                </ul>
              </div>
            </div>
          </div>

          <div class="footer-newsletter q-mt-xl q-pt-xl">
            <div class="row items-center q-col-gutter-md">
              <div class="col-12 col-md-6">
                <h3 class="newsletter-title text-h5 text-weight-bold q-mb-sm">Stay Updated</h3>
                <p class="newsletter-subtitle text-body2">
                  Subscribe to our newsletter for updates on crypto donations and social impact.
                </p>
              </div>
              <div class="col-12 col-md-6">
                <div class="newsletter-form">
                  <q-input
                    outlined
                    placeholder="Enter your email"
                    dense
                    bg-color="white"
                    class="newsletter-input"
                  >
                    <template v-slot:append>
                      <q-btn
                        color="primary"
                        label="Subscribe"
                        unelevated
                        dense
                        class="newsletter-btn"
                      />
                    </template>
                  </q-input>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="footer-bottom">
        <div class="container">
          <div class="row items-center justify-between">
            <div class="col-12 col-md-6 text-center text-md-left">
              <p class="footer-copyright text-body2">© 2026 CrypToCare. All rights reserved.</p>
            </div>
            <div class="col-12 col-md-6 text-center text-md-right">
              <div class="footer-legal-links">
                <a href="#" class="legal-link">Privacy Policy</a>
                <span class="separator">•</span>
                <a href="#" class="legal-link">Terms of Service</a>
                <span class="separator">•</span>
                <a href="#" class="legal-link">Cookie Policy</a>
              </div>
            </div>
          </div>
        </div>
      </div>
    </footer>
  </q-page>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { api } from 'boot/axios'

const isConnected = ref(localStorage.getItem('cryptocare.wallet.connected') === '1')
const isNonprofit = ref(false)
const checkingRole = ref(false)

const checkWalletRole = async () => {
  if (!isConnected.value) {
    isNonprofit.value = false
    return
  }
  try {
    checkingRole.value = true
    const snapshot = JSON.parse(localStorage.getItem('cryptocare.wallet.snapshot') || '{}')
    const address = snapshot?.address || ''
    if (!address) {
      isNonprofit.value = false
      return
    }
    const response = await api.get('nonprofits/')
    const nonprofits = response.data?.results || response.data || []
    const normalizedAddress = address.toLowerCase().trim()
    isNonprofit.value = nonprofits.some(
      (np) => np.bch_address?.toLowerCase().trim() === normalizedAddress,
    )
  } catch {
    isNonprofit.value = false
  } finally {
    checkingRole.value = false
  }
}

function onWalletChange() {
  isConnected.value = localStorage.getItem('cryptocare.wallet.connected') === '1'
  checkWalletRole()
}
onMounted(() => {
  window.addEventListener('cryptocare:wallet-connection-changed', onWalletChange)
  checkWalletRole()
})
onUnmounted(() =>
  window.removeEventListener('cryptocare:wallet-connection-changed', onWalletChange),
)

const testimonials = [
  {
    name: 'Maria',
    role: 'Typhoon Relief',
    text: 'Crypto donations reached us instantly when we needed it.',
    image: 'https://cdn.quasar.dev/img/parallax2.jpg',
    avatar: '../assets/image.png',
  },
  {
    name: 'Jose',
    role: 'Scholarship Student',
    text: 'My education was funded through blockchain donations.',
    image: 'https://cdn.quasar.dev/img/mountains.jpg',
    avatar: '/avatars/jose.jpg',
  },
  {
    name: 'James',
    role: 'Donor',
    text: 'I trust crypto because every donation is transparent.',
    image: 'https://cdn.quasar.dev/img/mountains.jpg',
    avatar: '/avatars/james.jpg',
  },
]
</script>
<style scoped>
.hero-section {
  min-height: 100vh;
  position: relative;
  display: flex;
  align-items: center;
  overflow: hidden;
  padding-top: 64px; /* Add padding to account for header height */
}

.hero-section::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-image: url('../assets/hero.png');
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
  animation: zoomOut 1.5s ease-out forwards;
  z-index: 0;
}

@keyframes zoomOut {
  from {
    transform: scale(1.2);
  }
  to {
    transform: scale(1);
  }
}

.hero-section .row {
  position: relative;
  width: 100%;
  z-index: 1;
}

.hero-content {
  max-width: 600px;
}

.hero-title {
  font-size: 4.5rem;
  font-weight: 800;
  margin-left: 10%;
  line-height: 1;
  color: white;
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
}

.hero-title .highlight {
  color: #ffd700;
  display: inline-block;
}

.hero-subtitle {
  font-size: 1.25rem;
  line-height: 1.6;
  color: white;
  margin-top: 1.5rem;
  margin-left: 10%;
  text-shadow: 1px 1px 3px rgba(0, 0, 0, 0.3);
}

.hero-buttons {
  display: flex;
  gap: 16px;
  align-items: center;
  margin-left: 10%;
}

.hero-btn {
  font-weight: 600;
  letter-spacing: 0.5px;
  transition: all 0.3s ease;
}

.hero-btn:hover {
  transform: scale(1.05);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.3);
}

.hero-btn-outline {
  font-weight: 600;
  letter-spacing: 0.5px;
  border: 2px solid rgba(255, 255, 255, 0.8);
  color: white;
  border-radius: 12px;
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  transition: all 0.3s ease;
}

.hero-btn-outline:hover {
  background: rgba(255, 255, 255, 0.2);
  border-color: white;
  transform: scale(1.05);
}

.featured-projects-section {
  background: linear-gradient(180deg, #f8f9fa 0%, #ffffff 100%);
  padding: 80px 0;
}

.project-card {
  border-radius: 20px;
  overflow: hidden;
  transition: all 0.3s ease;
  border: 2px solid #e0e0e0;
  background: white;
  height: 100%;
  display: flex;
  flex-direction: column;
}

.project-card:hover {
  transform: translateY(-8px);
  box-shadow: 0 12px 40px rgba(0, 0, 0, 0.12);
  border-color: #1976d2;
}

.project-image {
  position: relative;
  width: 100%;
  height: 200px;
  overflow: hidden;
}

.project-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.3s ease;
}

.project-card:hover .project-image img {
  transform: scale(1.1);
}

.project-badge {
  position: absolute;
  top: 12px;
  right: 12px;
  padding: 6px 16px;
  border-radius: 20px;
  font-weight: 600;
  font-size: 12px;
}

.project-description {
  min-height: 60px;
  line-height: 1.5;
}

.project-progress {
  margin-top: auto;
}

.mission-section {
  background: #ffffff;
  position: relative;
  overflow: hidden;
}

.mission-brand {
  display: flex;
  align-items: center;
  color: #1976d2;
}

.mission-heading {
  font-size: 3.5rem;
  line-height: 1.1;
  color: #1a1a1a;
  margin: 0;
}

.mission-description {
  font-size: 1.1rem;
  line-height: 1.8;
  color: #666;
  max-width: 500px;
}

.mission-grid {
  position: relative;
}

.mission-grid-item {
  position: relative;
  overflow: hidden;
  border-radius: 16px;
}

.mission-large-photo {
  width: 100%;
  height: 350px;
  position: relative;
}

.mission-large-photo img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  border-radius: 16px;
}

.mission-decorative-icon {
  position: absolute;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 100px;
  height: 100px;
  border-radius: 50%;
  background: linear-gradient(135deg, #4caf50 0%, #66bb6a 100%);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.15);
}

.mission-icon-topleft {
  bottom: -30px;
  left: 50%;
  transform: translateX(-50%);
}

.mission-icon-box {
  height: 200px;
  border-radius: 16px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  transition: all 0.3s ease;
}

.mission-icon-person {
  background: linear-gradient(135deg, #1976d2 0%, #42a5f5 100%);
  box-shadow: 0 4px 20px rgba(25, 118, 210, 0.3);
}

.mission-icon-community {
  background: linear-gradient(135deg, #4caf50 0%, #66bb6a 100%);
  box-shadow: 0 4px 20px rgba(76, 175, 80, 0.3);
}

.mission-icon-logo {
  background: linear-gradient(135deg, #9c27b0 0%, #ba68c8 100%);
  box-shadow: 0 4px 20px rgba(156, 39, 176, 0.3);
}

.mission-icon-box:hover {
  transform: translateY(-8px);
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
}

.mission-photo-box {
  height: 200px;
  border-radius: 16px;
  overflow: hidden;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
}

.mission-photo-box img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.mission-photo-box:hover {
  transform: translateY(-8px);
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.15);
}

.mission-visual-grid {
  margin-top: 40px;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
}

.stat-card {
  background: white;
  border-radius: 12px;
  transition: all 0.3s ease;
  border: 1px solid #e0e0e0;
}

.stat-card:hover {
  transform: scale(1.05);
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
}

/* Why Donate Section Styles */
.why-donate-section {
  background: #f8f9fa;
  position: relative;
}

.crypto-benefit-card {
  background: white;
  padding: 32px;
  border-radius: 12px;
  border: 1px solid #e0e0e0;
  transition: all 0.3s ease;
  height: 100%;
}

.crypto-benefit-card:hover {
  border-color: #1976d2;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.08);
  transform: translateY(-4px);
}

.benefit-header {
  display: flex;
  align-items: flex-start;
  gap: 16px;
}

.benefit-number {
  font-size: 2rem;
  font-weight: 800;
  color: #1976d2;
  line-height: 1;
  min-width: 50px;
}

.benefit-detail {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-top: 16px;
}

.fee-comparison {
  display: flex;
  gap: 24px;
  padding: 12px 16px;
  background: #f5f7fa;
  border-radius: 8px;
  width: 100%;
}

.fee-item {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.cause-area-card {
  background: white;
  padding: 20px;
  border-radius: 12px;
  border: 1px solid #e0e0e0;
  transition: all 0.3s ease;
  text-align: center;
}

.cause-area-card:hover {
  border-color: #1976d2;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.08);
}

.cause-icon-wrapper {
  width: 100%;
  height: 80px;
  border-radius: 8px;
  overflow: hidden;
  background: #f5f7fa;
  margin: 0 auto;
}

.cause-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.crypto-cta-section {
  border-top: 1px solid #e0e0e0;
}

.donation-matters-section {
  background: linear-gradient(180deg, #ffffff 0%, #f8f9fa 100%);
  position: relative;
}

.impact-year-badge {
  background: linear-gradient(135deg, #e3f2fd 0%, #f5f7fa 100%);
  padding: 24px 32px;
  border-radius: 12px;
  border: 2px solid #1976d2;
}

.metric-card {
  background: white;
  padding: 32px 24px;
  border-radius: 12px;
  border: 1px solid #e0e0e0;
  transition: all 0.3s ease;
  height: 100%;
}

.metric-card:hover {
  border-color: #1976d2;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.08);
  transform: translateY(-4px);
}

.metric-number {
  font-size: 3rem;
  font-weight: 800;
  line-height: 1;
  margin-bottom: 12px;
}

.metric-label {
  font-size: 1.1rem;
  font-weight: 600;
  color: #1a1a1a;
  margin-bottom: 8px;
}

.metric-description {
  font-size: 0.875rem;
  color: #666;
  line-height: 1.5;
  margin-bottom: 16px;
}

.metric-trend {
  display: flex;
  align-items: center;
  gap: 6px;
  padding-top: 12px;
  border-top: 1px solid #f0f0f0;
}

.impact-story-card {
  background: white;
  padding: 24px;
  border-radius: 12px;
  border: 1px solid #e0e0e0;
  transition: all 0.3s ease;
  height: 100%;
}

.impact-story-card:hover {
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.08);
  transform: translateY(-4px);
}

.story-image {
  width: 100%;
  height: 140px;
  border-radius: 8px;
  overflow: hidden;
  background: #f5f7fa;
}

.story-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.story-stat {
  line-height: 1;
  margin-bottom: 8px;
}

.story-title {
  color: #1a1a1a;
  line-height: 1.3;
}

.story-text {
  line-height: 1.6;
}

.impact-cta-section {
  border-top: 2px solid #e0e0e0;
  padding-top: 48px;
}

.impact-cta-button {
  font-weight: 600;
  border-radius: 8px;
  transition: all 0.3s ease;
}

.impact-cta-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 24px rgba(25, 118, 210, 0.3);
}

.donation-cta-btn {
  font-weight: 700;
  letter-spacing: 1px;
  transition: all 0.3s ease;
  box-shadow: 0 8px 24px rgba(255, 255, 255, 0.3);
}

.donation-cta-btn:hover {
  transform: scale(1.08) translateY(-2px);
  box-shadow: 0 12px 32px rgba(255, 255, 255, 0.5);
}

@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

@keyframes slideUp {
  from {
    opacity: 0;
    transform: translateY(40px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes scaleIn {
  from {
    opacity: 0;
    transform: scale(0.8);
  }
  to {
    opacity: 1;
    transform: scale(1);
  }
}

@keyframes slideInLeft {
  from {
    opacity: 0;
    transform: translateX(-40px);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
}

@keyframes slideInRight {
  from {
    opacity: 0;
    transform: translateX(40px);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
}

@keyframes bounceIn {
  0% {
    opacity: 0;
    transform: scale(0.8) translateY(20px);
  }
  50% {
    transform: scale(1.05) translateY(-5px);
  }
  100% {
    opacity: 1;
    transform: scale(1) translateY(0);
  }
}

@keyframes fadeSlideUp {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.animate-fade-in {
  animation: fadeIn 1s ease-out forwards;
}

.animate-slide-up {
  animation: slideUp 0.8s ease-out forwards;
  animation-delay: 0.2s;
  opacity: 0;
}

.animate-scale-in {
  animation: scaleIn 0.6s ease-out forwards;
  opacity: 0;
}

.animate-slide-in-left {
  animation: slideInLeft 0.8s ease-out forwards;
  opacity: 0;
}

.animate-slide-in-right {
  animation: slideInRight 0.8s ease-out forwards;
  opacity: 0;
}

.animate-bounce-in {
  animation: bounceIn 0.8s ease-out forwards;
  opacity: 0;
}

.animate-fade-slide-up {
  animation: fadeSlideUp 0.8s ease-out forwards;
  opacity: 0;
}

.testimonials-section {
  background: linear-gradient(180deg, #f8f9fa 0%, #ffffff 100%);
}

.testimonial-card {
  border-radius: 16px;
  transition: all 0.3s ease;
  border: 2px solid #e0e0e0;
  position: relative;
  overflow: visible;
  background: white;
}

.testimonial-card:hover {
  transform: translateY(-12px);
  box-shadow: 0 16px 48px rgba(0, 0, 0, 0.15);
  border-color: #1976d2;
}

.quote-icon-wrapper {
  position: absolute;
  top: -24px;
  left: 24px;
  width: 56px;
  height: 56px;
  border-radius: 50%;
  background: white;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  border: 2px solid #e3f2fd;
}

.testimonial-text {
  font-style: italic;
  color: #37474f;
  line-height: 1.8;
  min-height: 100px;
}

.trust-section {
  border-top: 2px solid #e0e0e0;
}

.trust-badge {
  display: flex;
  align-items: center;
  padding: 12px 24px;
  background: white;
  border-radius: 50px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
  transition: all 0.3s ease;
}

.trust-badge:hover {
  transform: translateY(-4px);
  box-shadow: 0 6px 16px rgba(0, 0, 0, 0.12);
}

.about-impact-section {
  background: #ffffff;
}

.about-content-professional {
  background: white;
  padding: 0;
}

.about-badge {
  display: inline-block;
  padding: 8px 20px;
  background: #e3f2fd;
  color: #1976d2;
  border-radius: 6px;
  font-weight: 600;
  font-size: 13px;
  letter-spacing: 0.5px;
  text-transform: uppercase;
}

.key-features {
  margin: 0;
}

.feature-box {
  padding: 20px;
  background: #f8f9fa;
  border-radius: 8px;
  transition: all 0.3s ease;
}

.feature-box:hover {
  background: #e3f2fd;
  transform: translateY(-4px);
}

.about-cta-btn {
  border-radius: 8px;
  font-weight: 600;
  transition: all 0.3s ease;
}

.about-cta-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 24px rgba(25, 118, 210, 0.3);
}

.about-visual-section {
  position: relative;
}

.about-main-image {
  width: 100%;
  height: 350px;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
}

.about-main-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.about-small-image {
  width: 100%;
  height: 160px;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.08);
}

.about-small-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.main-footer {
  background: linear-gradient(135deg, #1a237e 0%, #0d47a1 100%);
  color: white;
}

.footer-top {
  padding: 80px 0 40px;
}

.footer-brand-section {
  padding-right: 20px;
}

.footer-logo {
  display: flex;
  align-items: center;
  gap: 12px;
}

.footer-logo-img {
  width: 48px;
  height: 48px;
  object-fit: contain;
}

.footer-brand-name {
  font-size: 28px;
  font-weight: 700;
  color: white;
}

.footer-description {
  color: rgba(255, 255, 255, 0.8);
  line-height: 1.6;
}

.social-links {
  display: flex;
  gap: 12px;
}

.social-link {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.1);
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  transition: all 0.3s ease;
  text-decoration: none;
}

.social-link:hover {
  background: white;
  color: #1976d2;
  transform: translateY(-4px);
}

.footer-column {
  height: 100%;
}

.footer-title {
  font-size: 18px;
  font-weight: 700;
  margin-bottom: 20px;
  color: white;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.footer-links {
  list-style: none;
  padding: 0;
  margin: 0;
}

.footer-links li {
  margin-bottom: 12px;
}

.footer-link {
  color: rgba(255, 255, 255, 0.8);
  text-decoration: none;
  transition: all 0.3s ease;
  font-size: 14px;
  display: inline-block;
}

.footer-link:hover {
  color: white;
  transform: translateX(4px);
}

.footer-newsletter {
  border-top: 1px solid rgba(255, 255, 255, 0.2);
}

.newsletter-title {
  color: white;
  margin-bottom: 8px;
}

.newsletter-subtitle {
  color: rgba(255, 255, 255, 0.8);
}

.newsletter-form {
  max-width: 500px;
  margin-left: auto;
}

.newsletter-input {
  border-radius: 50px;
}

.newsletter-input :deep(.q-field__control) {
  border-radius: 50px;
}

.newsletter-btn {
  border-radius: 0 50px 50px 0;
  padding: 8px 24px;
}

.footer-bottom {
  background: rgba(0, 0, 0, 0.2);
  padding: 24px 0;
}

.footer-copyright {
  color: rgba(255, 255, 255, 0.8);
  margin: 0;
}

.footer-legal-links {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 12px;
  flex-wrap: wrap;
}

@media (min-width: 768px) {
  .footer-legal-links {
    justify-content: flex-end;
  }
}

.legal-link {
  color: rgba(255, 255, 255, 0.8);
  text-decoration: none;
  font-size: 14px;
  transition: color 0.3s ease;
}

.legal-link:hover {
  color: white;
}

.separator {
  color: rgba(255, 255, 255, 0.4);
}

/* Responsive padding for header overlap fix */
@media (max-width: 599px) {
  .hero-section {
    padding-top: 56px;
  }

  /* Hero text — scale down for phones */
  .hero-title {
    font-size: 2.4rem;
    margin-left: 0;
    line-height: 1.15;
  }

  .hero-subtitle {
    font-size: 1rem;
    margin-left: 0;
  }

  .hero-buttons {
    margin-left: 0;
    flex-wrap: wrap;
  }

  /* Hero row padding — q-pa-xl (48px) is too much on phones */
  .hero-section .row {
    padding: 20px 16px !important;
  }

  /* Container needs side breathing room */
  .container {
    padding: 0 16px;
  }

  /* Mission heading */
  .mission-heading {
    font-size: 2rem;
  }

  /* Remove excessive right padding on stacked mission column */
  .mission-section .q-pr-xl {
    padding-right: 0 !important;
  }

  /* Photo boxes — reduce height on mobile */
  .mission-photo-box {
    height: 140px;
  }

  .mission-large-photo {
    height: 200px;
  }

  /* Mission section bottom stats — stack nicely */
  .stat-card {
    margin-bottom: 4px;
  }

  /* Crypto benefit cards — reduce padding */
  .crypto-benefit-card {
    padding: 20px 16px;
  }

  .benefit-number {
    font-size: 1.5rem;
    min-width: 36px;
  }

  /* Fee comparison — stack vertically on mobile */
  .fee-comparison {
    flex-direction: column;
    gap: 8px;
  }

  /* Impact year badge — center on mobile */
  .impact-year-badge {
    display: inline-block;
    margin-top: 16px;
  }

  /* Metric numbers scale down */
  .metric-number {
    font-size: 2.2rem;
  }

  /* Impact story cards — reduce padding */
  .impact-story-card {
    padding: 16px;
  }

  .story-image {
    height: 90px;
  }

  /* CTA sections — center button on mobile */
  .crypto-cta-section .col-12.text-right,
  .impact-cta-section .col-12.text-right {
    text-align: left !important;
    margin-top: 12px;
  }

  /* Newsletter form — full width on mobile */
  .newsletter-form {
    margin-left: 0;
    max-width: 100%;
  }

  /* Footer top padding */
  .footer-top {
    padding: 40px 0 24px;
  }

  /* Footer columns — remove excess padding */
  .footer-brand-section {
    padding-right: 0;
  }

  /* Section titles */
  .section-title {
    font-size: 1.8rem !important;
  }

  /* Testimonials min-height reduction */
  .testimonial-text {
    min-height: 60px;
  }
}

@media (min-width: 600px) and (max-width: 1023px) {
  .hero-section {
    padding-top: 60px;
  }

  .hero-title {
    font-size: 3rem;
    margin-left: 4%;
  }

  .hero-subtitle {
    margin-left: 4%;
  }

  .hero-buttons {
    margin-left: 4%;
  }

  .container {
    padding: 0 20px;
  }

  .mission-heading {
    font-size: 2.6rem;
  }

  .newsletter-form {
    margin-left: 0;
  }
}

/* ── Index Page Dark Mode ────────────────────────────────────── */

/* Featured Projects */
.body--dark .featured-projects-section {
  background: linear-gradient(180deg, #0f1629 0%, #131d35 100%);
}

.body--dark .project-card {
  background: #1a2240;
  border-color: #2e3f6e;
  color: #d0daf0;
}

.body--dark .project-card:hover {
  border-color: #4d7cc7;
  box-shadow: 0 12px 40px rgba(0, 0, 0, 0.4);
}

/* Mission Section */
.body--dark .mission-section {
  background: #111827;
}

.body--dark .mission-heading {
  color: #e0eaff;
}

.body--dark .mission-description {
  color: #8fa8cb;
}

.body--dark .stat-card {
  background: #1a2240;
  border-color: #2e3f6e;
}

/* Why Donate Section */
.body--dark .why-donate-section {
  background: #0f1629;
}

.body--dark .crypto-benefit-card {
  background: #1a2240;
  border-color: #2e3f6e;
  color: #c8d8f0;
}

.body--dark .crypto-benefit-card:hover {
  border-color: #4d7cc7;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.4);
}

.body--dark .benefit-number {
  color: #5d9cf5;
}

.body--dark .fee-comparison {
  background: #0f1629;
}

.body--dark .cause-area-card {
  background: #1a2240;
  border-color: #2e3f6e;
  color: #c8d8f0;
}

.body--dark .cause-area-card:hover {
  border-color: #4d7cc7;
}

.body--dark .crypto-cta-section {
  border-color: #2e3f6e;
}

/* Donation Matters Section */
.body--dark .donation-matters-section {
  background: linear-gradient(180deg, #111827 0%, #0f1629 100%);
}

.body--dark .impact-year-badge {
  background: linear-gradient(135deg, #1a2a4a 0%, #1a2240 100%);
  border-color: #4d7cc7;
}

.body--dark .metric-card {
  background: #1a2240;
  border-color: #2e3f6e;
}

.body--dark .metric-card:hover {
  border-color: #4d7cc7;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.4);
}

.body--dark .metric-label {
  color: #c8d8f0;
}

.body--dark .metric-description {
  color: #7a96b8;
}

.body--dark .metric-trend {
  border-color: #2e3f6e;
}

.body--dark .impact-story-card {
  background: #1a2240;
  border-color: #2e3f6e;
  color: #c8d8f0;
}

.body--dark .impact-story-card:hover {
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.4);
}

.body--dark .story-title {
  color: #d8e8ff;
}

.body--dark .impact-cta-section {
  border-color: #2e3f6e;
}

/* Testimonials Section */
.body--dark .testimonials-section {
  background: linear-gradient(180deg, #0f1629 0%, #111827 100%);
}

.body--dark .testimonial-card {
  background: #1a2240;
  border-color: #2e3f6e;
}

.body--dark .testimonial-card:hover {
  border-color: #4d7cc7;
  box-shadow: 0 16px 48px rgba(0, 0, 0, 0.45);
}

.body--dark .quote-icon-wrapper {
  background: #1a2240;
  border-color: #2e3f6e;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.4);
}

.body--dark .testimonial-text {
  color: #a0b8d8;
}

.body--dark .trust-section {
  border-color: #2e3f6e;
}

.body--dark .trust-badge {
  background: #1a2240;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.3);
  color: #c8d8f0;
}

.body--dark .trust-badge:hover {
  box-shadow: 0 6px 16px rgba(0, 0, 0, 0.4);
}

/* About Section */
.body--dark .about-impact-section {
  background: #111827;
}

.body--dark .about-content-professional {
  background: transparent;
}

.body--dark .about-badge {
  background: #1a2a4a;
  color: #5d9cf5;
}

.body--dark .feature-box {
  background: #1a2240;
  color: #c8d8f0;
}

.body--dark .feature-box:hover {
  background: #1e3060;
}

/* ── Fix Quasar grey text classes on dark section backgrounds ─ */

/* Featured Projects */
.body--dark .featured-projects-section .text-grey-6,
.body--dark .featured-projects-section .text-grey-7,
.body--dark .featured-projects-section .text-grey-8 {
  color: #8fa8cb !important;
}
.body--dark .project-card .text-h6 {
  color: #d8e8ff !important;
}
.body--dark .project-card .text-grey-7 {
  color: #8fa8cb !important;
}
.body--dark .project-card .text-caption {
  color: #8fa8cb !important;
}

/* Mission */
.body--dark .mission-section .text-h3,
.body--dark .mission-section .text-h4,
.body--dark .mission-section .text-h5 {
  color: #e0eaff !important;
}
.body--dark .mission-section .text-grey-7,
.body--dark .mission-section .text-grey-8 {
  color: #8fa8cb !important;
}
.body--dark .stat-card .text-subtitle1 {
  color: #8fa8cb !important;
}

/* Why Donate */
.body--dark .why-donate-section .text-h3,
.body--dark .why-donate-section .text-h5 {
  color: #e0eaff !important;
}
.body--dark .why-donate-section .text-grey-7,
.body--dark .why-donate-section .text-grey-8 {
  color: #8fa8cb !important;
}
.body--dark .crypto-benefit-card h3 {
  color: #d8e8ff !important;
}
.body--dark .crypto-cta-section h3 {
  color: #e0eaff !important;
}
.body--dark .crypto-cta-section .text-grey-7 {
  color: #8fa8cb !important;
}
.body--dark .cause-area-card .text-subtitle1 {
  color: #d8e8ff !important;
}
.body--dark .cause-area-card .text-grey-7,
.body--dark .cause-area-card .text-caption {
  color: #8fa8cb !important;
}

/* Donation Matters */
.body--dark .donation-matters-section .text-h3,
.body--dark .donation-matters-section .text-h4,
.body--dark .donation-matters-section .text-h5 {
  color: #e0eaff !important;
}
.body--dark .donation-matters-section .text-grey-7,
.body--dark .donation-matters-section .text-grey-8 {
  color: #8fa8cb !important;
}
.body--dark .impact-story-card .text-subtitle1 {
  color: #d8e8ff !important;
}
.body--dark .impact-story-card .text-body2,
.body--dark .impact-story-card .text-grey-7 {
  color: #8fa8cb !important;
}
.body--dark .impact-cta-section h3 {
  color: #e0eaff !important;
}
.body--dark .impact-cta-section .text-grey-7 {
  color: #8fa8cb !important;
}

/* Testimonials */
.body--dark .testimonials-section .text-h3,
.body--dark .testimonials-section .text-h5,
.body--dark .testimonials-section .text-h6 {
  color: #e0eaff !important;
}
.body--dark .testimonials-section .text-grey-7 {
  color: #8fa8cb !important;
}
.body--dark .testimonial-card .text-subtitle1 {
  color: #d8e8ff !important;
}
.body--dark .testimonial-card .text-caption {
  color: #8fa8cb !important;
}
.body--dark .trust-section .text-h5 {
  color: #e0eaff !important;
}
.body--dark .trust-section .text-grey-7,
.body--dark .trust-section .text-grey-8 {
  color: #8fa8cb !important;
}

/* About Section */
.body--dark .about-impact-section .text-h3,
.body--dark .about-impact-section .text-h4,
.body--dark .about-impact-section .text-h5 {
  color: #e0eaff !important;
}
.body--dark .about-impact-section .text-grey-7,
.body--dark .about-impact-section .text-grey-8 {
  color: #8fa8cb !important;
}
.body--dark .feature-box .text-subtitle1 {
  color: #d8e8ff !important;
}
.body--dark .feature-box .text-caption {
  color: #8fa8cb !important;
}
</style>

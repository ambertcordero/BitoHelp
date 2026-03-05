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

          <q-btn
            label="Start Donating"
            color="primary"
            size="lg"
            unelevated
            class="hero-btn q-mt-lg"
            to="/donate"
            @click="$router.push('/donate')"
          />
        </div>

        <div class="col-12 col-md-5">
          <q-img src="Donaciones.gif" />
        </div>

      </div>
    </section>

    <!-- OUR MISSION SECTION -->
    <section class="mission-section q-py-xl q-px-md">
      <div class="container">
        <div class="text-center q-mb-xl">
          <h2 class="section-title text-h3 text-weight-bold q-mb-md">Our Mission</h2>
          <p class="text-h6 text-grey-7 q-mb-lg" style="max-width: 800px; margin: 0 auto;">
            We empower donors and nonprofits by providing a transparent, blockchain-based donation platform where every transaction is verifiable and impactful.
          </p>
        </div>

       
        <div class="row q-col-gutter-lg">
          <div class="col-12 col-md-4">
            <q-card class="mission-card full-height" flat bordered>
              <q-card-section class="text-center q-pa-lg">
                <div class="mission-icon-wrapper q-mb-md">
                  <q-icon name="visibility" size="64px" color="primary" />
                </div>
                <div class="text-h5 text-weight-bold q-mb-md">Full Transparency</div>
                <p class="text-body1 text-grey-7">
                  Every donation is recorded on the blockchain, providing complete transparency and accountability. Track your impact in real-time.
                </p>
              </q-card-section>
            </q-card>
          </div>

        
          <div class="col-12 col-md-4">
            <q-card class="mission-card full-height" flat bordered>
              <q-card-section class="text-center q-pa-lg">
                <div class="mission-icon-wrapper q-mb-md">
                  <q-icon name="bolt" size="64px" color="positive" />
                </div>
                <div class="text-h5 text-weight-bold q-mb-md">Fast & Secure</div>
                <p class="text-body1 text-grey-7">
                  Blockchain-powered donations reach beneficiaries instantly with enterprise-grade security and minimal fees.
                </p>
              </q-card-section>
            </q-card>
          </div>

          
          <div class="col-12 col-md-4">
            <q-card class="mission-card full-height" flat bordered>
              <q-card-section class="text-center q-pa-lg">
                <div class="mission-icon-wrapper q-mb-md">
                  <q-icon name="public" size="64px" color="secondary" />
                </div>
                <div class="text-h5 text-weight-bold q-mb-md">Global Impact</div>
                <p class="text-body1 text-grey-7">
                  Support verified nonprofits worldwide without borders, currency barriers, or intermediaries.
                </p>
              </q-card-section>
            </q-card>
          </div>
        </div>

       
        <div class="row q-col-gutter-md q-mt-xl">
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
        <div class="text-center q-mb-xl">
          <h2 class="section-title text-h3 text-weight-bold q-mb-md">Why Donate with Crypto?</h2>
          <p class="text-h6 text-grey-7 q-mb-lg" style="max-width: 700px; margin: 0 auto;">
            Your cryptocurrency donations create lasting change across multiple causes with unparalleled transparency and efficiency.
          </p>
        </div>

        
        <div class="row q-col-gutter-lg q-mb-xl">
          <div class="col-12 col-sm-6 col-md-3">
            <q-card class="impact-card full-height text-center" flat>
              <q-card-section class="q-pa-lg">
                <div class="impact-icon-container q-mb-md">
                  <q-icon name="school" size="56px" color="white" />
                </div>
                <div class="text-h6 text-weight-bold q-mb-sm">Education</div>
                <p class="text-body2 text-grey-8">
                  Fund scholarships, tutoring programs, and school supplies for underserved communities.
                </p>
              </q-card-section>
            </q-card>
          </div>

      
          <div class="col-12 col-sm-6 col-md-3">
            <q-card class="impact-card full-height text-center" flat>
              <q-card-section class="q-pa-lg">
                <div class="impact-icon-container impact-icon-healthcare q-mb-md">
                  <q-icon name="local_hospital" size="56px" color="white" />
                </div>
                <div class="text-h6 text-weight-bold q-mb-sm">Healthcare</div>
                <p class="text-body2 text-grey-8">
                  Provide medical care, supplies, and health education to those in need.
                </p>
              </q-card-section>
            </q-card>
          </div>

         
          <div class="col-12 col-sm-6 col-md-3">
            <q-card class="impact-card full-height text-center" flat>
              <q-card-section class="q-pa-lg">
                <div class="impact-icon-container impact-icon-relief q-mb-md">
                  <q-icon name="volunteer_activism" size="56px" color="white" />
                </div>
                <div class="text-h6 text-weight-bold q-mb-sm">Disaster Relief</div>
                <p class="text-body2 text-grey-8">
                  Rapid response to typhoons, floods, and natural disasters with instant aid.
                </p>
              </q-card-section>
            </q-card>
          </div>

          
          <div class="col-12 col-sm-6 col-md-3">
            <q-card class="impact-card full-height text-center" flat>
              <q-card-section class="q-pa-lg">
                <div class="impact-icon-container impact-icon-community q-mb-md">
                  <q-icon name="groups" size="56px" color="white" />
                </div>
                <div class="text-h6 text-weight-bold q-mb-sm">Community</div>
                <p class="text-body2 text-grey-8">
                  Support local initiatives, food programs, and skill development projects.
                </p>
              </q-card-section>
            </q-card>
          </div>
        </div>

    
        <div class="row q-col-gutter-md">
          <div class="col-12 col-md-6">
            <q-card class="benefit-card" flat bordered>
              <q-card-section horizontal>
                <q-card-section class="col-3 flex items-center justify-center bg-primary">
                  <q-icon name="lock" size="48px" color="white" />
                </q-card-section>
                <q-card-section class="col-9">
                  <div class="text-h6 text-weight-bold q-mb-sm">Secure & Trustworthy</div>
                  <p class="text-body2 text-grey-7">
                    Every transaction is recorded on the blockchain, ensuring complete transparency and preventing fraud.
                  </p>
                </q-card-section>
              </q-card-section>
            </q-card>
          </div>

          <div class="col-12 col-md-6">
            <q-card class="benefit-card" flat bordered>
              <q-card-section horizontal>
                <q-card-section class="col-3 flex items-center justify-center bg-positive">
                  <q-icon name="savings" size="48px" color="white" />
                </q-card-section>
                <q-card-section class="col-9">
                  <div class="text-h6 text-weight-bold q-mb-sm">Lower Fees, Higher Impact</div>
                  <p class="text-body2 text-grey-7">
                    Minimal transaction fees mean more of your donation reaches those who need it most.
                  </p>
                </q-card-section>
              </q-card-section>
            </q-card>
          </div>
        </div>

        
        <div class="text-center q-mt-xl">
          <q-btn
            label="Start Making an Impact"
            color="primary"
            size="lg"
            unelevated
            rounded
            padding="12px 48px"
            to="/donate"
            class="cta-button"
          />
        </div>
      </div>
    </section>

    <section class="donation-matters-section q-py-xl">
      <div class="parallax-overlay animate-fade-in"></div>
      <div class="container relative-position z-top">
        <div class="text-center q-mb-xl animate-slide-up">
          <h2 class="text-h2 text-weight-bold text-white q-mb-md">Why Your Donation Matters</h2>
          <p class="text-h6 text-white" style="max-width: 800px; margin: 0 auto; opacity: 0.95;">
            Every cryptocurrency donation creates a ripple effect of positive change in communities worldwide
          </p>
        </div>

    
        <div class="row q-col-gutter-lg q-mb-xl">
          <div class="col-12 col-md-4 animate-scale-in" style="animation-delay: 0.2s;">
            <q-card class="impact-metric-card text-center" flat>
              <q-card-section class="q-pa-xl">
                <q-icon name="trending_up" size="64px" color="primary" class="q-mb-md" />
                <div class="text-h3 text-weight-bold text-primary q-mb-sm">100%</div>
                <div class="text-h6 text-weight-medium q-mb-sm">Traceable</div>
                <p class="text-body2 text-grey-7">
                  Track your donation from wallet to beneficiary on the blockchain
                </p>
              </q-card-section>
            </q-card>
          </div>

          <div class="col-12 col-md-4 animate-scale-in" style="animation-delay: 0.4s;">
            <q-card class="impact-metric-card text-center" flat>
              <q-card-section class="q-pa-xl">
                <q-icon name="timer" size="64px" color="positive" class="q-mb-md" />
                <div class="text-h3 text-weight-bold text-positive q-mb-sm">&lt;1 Min</div>
                <div class="text-h6 text-weight-medium q-mb-sm">Processing Time</div>
                <p class="text-body2 text-grey-7">
                  Instant transfers ensure help reaches those in need immediately
                </p>
              </q-card-section>
            </q-card>
          </div>

          <div class="col-12 col-md-4 animate-scale-in" style="animation-delay: 0.6s;">
            <q-card class="impact-metric-card text-center" flat>
              <q-card-section class="q-pa-xl">
                <q-icon name="percent" size="64px" color="orange" class="q-mb-md" />
                <div class="text-h3 text-weight-bold text-orange q-mb-sm">95%+</div>
                <div class="text-h6 text-weight-medium q-mb-sm">Goes Direct</div>
                <p class="text-body2 text-grey-7">
                  Minimal fees mean maximum impact for every donation you make
                </p>
              </q-card-section>
            </q-card>
          </div>
        </div>

        
        <div class="row q-col-gutter-md">
          <div class="col-12 col-md-6 animate-slide-in-left" style="animation-delay: 0.8s;">
            <q-card class="story-card" flat>
              <q-card-section class="q-pa-lg">
                <div class="row items-center q-mb-md">
                  <q-icon name="school" size="40px" color="primary" class="q-mr-md" />
                  <div class="text-h5 text-weight-bold">500+ Students Educated</div>
                </div>
                <p class="text-body1">
                  Your crypto donations funded scholarships, school supplies, and tutoring programs, changing the trajectory of hundreds of lives.
                </p>
              </q-card-section>
            </q-card>
          </div>

          <div class="col-12 col-md-6 animate-slide-in-right" style="animation-delay: 0.8s;">
            <q-card class="story-card" flat>
              <q-card-section class="q-pa-lg">
                <div class="row items-center q-mb-md">
                  <q-icon name="favorite" size="40px" color="red" class="q-mr-md" />
                  <div class="text-h5 text-weight-bold">1,200+ Lives Saved</div>
                </div>
                <p class="text-body1">
                  Emergency medical care and disaster relief reached families within hours thanks to instant blockchain transfers.
                </p>
              </q-card-section>
            </q-card>
          </div>
        </div>

     
        <div class="text-center q-mt-xl animate-bounce-in" style="animation-delay: 1s;">
          <div class="text-h5 text-white text-weight-medium q-mb-lg">
            Ready to make a difference?
          </div>
          <q-btn
            label="Donate Now"
            size="xl"
            unelevated
            rounded
            color="white"
            text-color="primary"
            padding="16px 64px"
            to="/donate"
            class="donation-cta-btn"
          >
            <q-icon name="arrow_forward" size="24px" class="q-ml-sm" />
          </q-btn>
        </div>
      </div>
    </section>


   
    <section class="testimonials-section q-py-xl q-px-md">
      <div class="container">
        <div class="text-center q-mb-xl animate-slide-up">
          <h2 class="section-title text-h3 text-weight-bold q-mb-md">What People Are Saying</h2>
          <p class="text-h6 text-grey-7 q-mb-lg" style="max-width: 700px; margin: 0 auto;">
            Hear from donors and beneficiaries about their experience with blockchain-powered giving
          </p>
        </div>

     
        <div class="row q-col-gutter-lg">
          <div class="col-12 col-md-4 animate-fade-slide-up" v-for="(t, index) in testimonials" :key="t.name" :style="{ animationDelay: (0.2 + index * 0.2) + 's' }">
            <q-card class="testimonial-card full-height" flat bordered>
          
              <div class="quote-icon-wrapper">
                <q-icon name="format_quote" size="48px" color="primary" />
              </div>

              <q-card-section class="q-pa-lg">
                
                <p class="testimonial-text text-body1 q-mb-lg">
                  "{{ t.text }}"
                </p>

             
                <div class="row items-center">
                  <q-avatar size="56px" class="q-mr-md">
                    <img :src="t.image" alt="t.name">
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
          <div class="text-center q-mb-lg animate-slide-up" style="animation-delay: 0.8s;">
            <div class="text-h5 text-weight-bold text-grey-8 q-mb-sm">Trusted by Organizations Worldwide</div>
            <p class="text-body1 text-grey-7">Join thousands of donors making a verified impact</p>
          </div>
          
          <div class="row q-col-gutter-md justify-center items-center">
            <div class="col-auto trust-badge animate-scale-in" style="animation-delay: 1s;">
              <q-icon name="verified" size="32px" color="primary" class="q-mr-sm" />
              <span class="text-weight-medium">Blockchain Verified</span>
            </div>
            <div class="col-auto trust-badge animate-scale-in" style="animation-delay: 1.1s;">
              <q-icon name="security" size="32px" color="positive" class="q-mr-sm" />
              <span class="text-weight-medium">Secure Transactions</span>
            </div>
            <div class="col-auto trust-badge animate-scale-in" style="animation-delay: 1.2s;">
              <q-icon name="public" size="32px" color="secondary" class="q-mr-sm" />
              <span class="text-weight-medium">Global Network</span>
            </div>
          </div>
        </div>
      </div>
    </section>

    
    <section class="about-impact-section q-py-xl q-px-md">
      <div class="container">
        <div class="row q-col-gutter-xl">
          <div class="col-12 col-md-6 animate-slide-in-left">
            <div class="about-content">
              <div class="section-badge q-mb-md">About BiToHelp</div>
              <h2 class="text-h3 text-weight-bold q-mb-md">Blockchain-Powered Social Impact</h2>
              <p class="text-body1 text-grey-8 q-mb-lg" style="line-height: 1.8;">
                Established in 2026, BiToHelp empowers individuals and transforms communities through transparent cryptocurrency donations. We bridge the gap between crypto innovation and humanitarian causes.
              </p>

              
              <div class="feature-list q-mb-lg">
                <div class="feature-item q-mb-md animate-slide-in-left" style="animation-delay: 0.3s;">
                  <q-icon name="check_circle" size="24px" color="positive" class="q-mr-sm" />
                  <span class="text-body1">100% transparent blockchain transactions</span>
                </div>
                <div class="feature-item q-mb-md animate-slide-in-left" style="animation-delay: 0.4s;">
                  <q-icon name="check_circle" size="24px" color="positive" class="q-mr-sm" />
                  <span class="text-body1">Direct donations to verified nonprofits</span>
                </div>
                <div class="feature-item q-mb-md animate-slide-in-left" style="animation-delay: 0.5s;">
                  <q-icon name="check_circle" size="24px" color="positive" class="q-mr-sm" />
                  <span class="text-body1">Real-time impact tracking and reporting</span>
                </div>
                <div class="feature-item q-mb-md animate-slide-in-left" style="animation-delay: 0.6s;">
                  <q-icon name="check_circle" size="24px" color="positive" class="q-mr-sm" />
                  <span class="text-body1">Global reach, local impact</span>
                </div>
              </div>

              <div class="q-mt-xl">
                <q-btn 
                  label="Learn More About Us" 
                  color="primary" 
                  size="lg"
                  unelevated
                  rounded
                  icon-right="arrow_forward"
                  class="feature-btn animate-scale-in"
                  style="animation-delay: 0.7s;"
                />
              </div>
            </div>
          </div>

          
          <div class="col-12 col-md-6 animate-slide-in-right">
            <div class="impact-content">
              <div class="section-badge section-badge-impact q-mb-md">Our Impact</div>
              <h3 class="text-h4 text-weight-bold q-mb-lg">Making a Difference Worldwide</h3>

              <div class="impact-timeline">
                <div class="timeline-item q-mb-lg animate-fade-slide-up" style="animation-delay: 0.3s;">
                  <div class="timeline-marker">
                    <q-icon name="school" size="32px" color="white" />
                  </div>
                  <div class="timeline-content">
                    <h4 class="text-h6 text-weight-bold q-mb-sm">Education Programs</h4>
                    <p class="text-body2 text-grey-8">
                      Funded 500+ scholarships, provided school supplies to 2,000+ students, and established 15 tutoring centers across underserved communities.
                    </p>
                  </div>
                </div>

                <div class="timeline-item q-mb-lg animate-fade-slide-up" style="animation-delay: 0.5s;">
                  <div class="timeline-marker timeline-marker-healthcare">
                    <q-icon name="local_hospital" size="32px" color="white" />
                  </div>
                  <div class="timeline-content">
                    <h4 class="text-h6 text-weight-bold q-mb-sm">Healthcare Initiatives</h4>
                    <p class="text-body2 text-grey-8">
                      Delivered medical supplies to 50+ clinics, funded 1,200+ medical treatments, and provided health education to 3,000+ families.
                    </p>
                  </div>
                </div>

                <div class="timeline-item animate-fade-slide-up" style="animation-delay: 0.7s;">
                  <div class="timeline-marker timeline-marker-relief">
                    <q-icon name="volunteer_activism" size="32px" color="white" />
                  </div>
                  <div class="timeline-content">
                    <h4 class="text-h6 text-weight-bold q-mb-sm">Disaster Relief</h4>
                    <p class="text-body2 text-grey-8">
                      Rapid response to 12 natural disasters, helped 5,000+ families rebuild, and distributed emergency supplies within 24 hours of crisis.
                    </p>
                  </div>
                </div>
              </div>

              <div class="q-mt-xl">
                <q-btn 
                  label="Explore Our Projects" 
                  color="secondary" 
                  size="lg"
                  unelevated
                  rounded
                  icon-right="explore"
                  class="feature-btn animate-scale-in"
                  style="animation-delay: 0.9s;"
                />
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
                  <img src="~assets/image1.png" alt="BiToHelp" class="footer-logo-img" />
                  <span class="footer-brand-name">BiToHelp</span>
                </div>
                <p class="footer-description text-body2 q-mb-lg">
                  Empowering social impact through transparent blockchain-powered cryptocurrency donations. Join us in making the world a better place.
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
                <p class="newsletter-subtitle text-body2">Subscribe to our newsletter for updates on crypto donations and social impact.</p>
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
              <p class="footer-copyright text-body2">
                © 2026 BiToHelp. All rights reserved.
              </p>
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
const testimonials = [
  {
    name: "Maria",
    role: "Typhoon Relief",
    text: "Crypto donations reached us instantly when we needed it.",
    image: "https://cdn.quasar.dev/img/parallax2.jpg",
    avatar: "../assets/image.png"
  },
  {
    name: "Jose",
    role: "Scholarship Student",
    text: "My education was funded through blockchain donations.",
    image: "https://cdn.quasar.dev/img/mountains.jpg",
    avatar: "/avatars/jose.jpg"
  },
  {
    name: "James",
    role: "Donor",
    text: "I trust crypto because every donation is transparent.",
    image: "https://cdn.quasar.dev/img/mountains.jpg",
    avatar: "/avatars/james.jpg"
  },

]
</script>
<style scoped>

.mission-section {
  background: linear-gradient(135deg, #f5f7fa 0%, #ffffff 100%);
  position: relative;
  overflow: hidden;
}

.mission-section::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 4px;
  background: linear-gradient(90deg, #1976d2 0%, #21CBF3 100%);
}

.container {
  max-width: 1200px;
  margin: 0 auto;
}

.mission-card {
  transition: all 0.3s ease;
  border-radius: 12px;
  border: 2px solid #e0e0e0;
  background: white;
}

.mission-card:hover {
  transform: translateY(-8px);
  box-shadow: 0 12px 40px rgba(0, 0, 0, 0.12);
  border-color: #1976d2;
}

.mission-icon-wrapper {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 100px;
  height: 100px;
  border-radius: 50%;
  background: linear-gradient(135deg, #f5f7fa 0%, #e3f2fd 100%);
  margin: 0 auto;
}

.stat-card {
  background: white;
  border-radius: 8px;
  transition: all 0.3s ease;
}

.stat-card:hover {
  transform: scale(1.05);
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
}

/* Why Donate Section Styles */
.why-donate-section {
  background: white;
  position: relative;
}

.impact-card {
  border-radius: 16px;
  overflow: hidden;
  background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
  transition: all 0.3s ease;
  border: 1px solid #e0e0e0;
}

.impact-card:hover {
  transform: translateY(-6px);
  box-shadow: 0 8px 30px rgba(0, 0, 0, 0.1);
}

.impact-icon-container {
  width: 90px;
  height: 90px;
  border-radius: 50%;
  background: linear-gradient(135deg, #1976d2 0%, #42a5f5 100%);
  display: inline-flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 4px 15px rgba(25, 118, 210, 0.3);
}

.impact-icon-healthcare {
  background: linear-gradient(135deg, #4caf50 0%, #66bb6a 100%);
  box-shadow: 0 4px 15px rgba(76, 175, 80, 0.3);
}

.impact-icon-relief {
  background: linear-gradient(135deg, #ff9800 0%, #ffb74d 100%);
  box-shadow: 0 4px 15px rgba(255, 152, 0, 0.3);
}

.impact-icon-community {
  background: linear-gradient(135deg, #9c27b0 0%, #ba68c8 100%);
  box-shadow: 0 4px 15px rgba(156, 39, 176, 0.3);
}

.benefit-card {
  border-radius: 12px;
  transition: all 0.3s ease;
  overflow: hidden;
}

.benefit-card:hover {
  transform: translateX(8px);
  box-shadow: 0 6px 25px rgba(0, 0, 0, 0.12);
}

.cta-button {
  font-weight: 600;
  letter-spacing: 0.5px;
  transition: all 0.3s ease;
}

.cta-button:hover {
  transform: scale(1.05);
  box-shadow: 0 6px 20px rgba(25, 118, 210, 0.4);
}

.donation-matters-section {
  background-image: url('../assets/bg.jpg');
  background-size: cover;
  background-position: center;
  background-attachment: fixed;
  position: relative;
  min-height: 600px;
}

.parallax-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(135deg, rgba(25, 118, 210, 0.9) 0%, rgba(33, 203, 243, 0.85) 100%);
}

.z-top {
  z-index: 1;
}

.impact-metric-card {
  border-radius: 16px;
  transition: all 0.3s ease;
  background: white;
  overflow: hidden;
}

.impact-metric-card:hover {
  transform: translateY(-10px) scale(1.02);
  box-shadow: 0 16px 48px rgba(0, 0, 0, 0.2);
}

.story-card {
  border-radius: 12px;
  background: rgba(255, 255, 255, 0.98);
  backdrop-filter: blur(10px);
  transition: all 0.3s ease;
  border-left: 4px solid #1976d2;
}

.story-card:hover {
  transform: translateX(8px);
  box-shadow: 0 8px 30px rgba(0, 0, 0, 0.15);
  border-left-color: #21CBF3;
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

/* Section 4 Animations */
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

/* Testimonials Section */
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
  background: linear-gradient(135deg, #ffffff 0%, #f5f7fa 100%);
}

.section-badge {
  display: inline-block;
  padding: 8px 20px;
  background: linear-gradient(135deg, #1976d2 0%, #42a5f5 100%);
  color: white;
  border-radius: 50px;
  font-weight: 600;
  font-size: 14px;
  letter-spacing: 0.5px;
  text-transform: uppercase;
}

.section-badge-impact {
  background: linear-gradient(135deg, #9c27b0 0%, #ba68c8 100%);
}

.about-content,
.impact-content {
  height: 100%;
}

.feature-list {
  margin-left: 0;
}

.feature-item {
  display: flex;
  align-items: center;
  transition: all 0.2s ease;
}

.feature-item:hover {
  transform: translateX(8px);
}

.feature-btn {
  font-weight: 600;
  letter-spacing: 0.5px;
  transition: all 0.3s ease;
}

.feature-btn:hover {
  transform: scale(1.05);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.15);
}


.impact-timeline {
  position: relative;
  padding-left: 20px;
}

.impact-timeline::before {
  content: '';
  position: absolute;
  left: 20px;
  top: 16px;
  bottom: 16px;
  width: 2px;
  background: linear-gradient(180deg, #1976d2 0%, #9c27b0 100%);
}

.timeline-item {
  position: relative;
  padding-left: 48px;
}

.timeline-marker {
  position: absolute;
  left: 0;
  top: 0;
  width: 56px;
  height: 56px;
  border-radius: 50%;
  background: linear-gradient(135deg, #1976d2 0%, #42a5f5 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 4px 12px rgba(25, 118, 210, 0.4);
  z-index: 1;
  transition: all 0.3s ease;
}

.timeline-marker-healthcare {
  background: linear-gradient(135deg, #4caf50 0%, #66bb6a 100%);
  box-shadow: 0 4px 12px rgba(76, 175, 80, 0.4);
}

.timeline-marker-relief {
  background: linear-gradient(135deg, #ff9800 0%, #ffb74d 100%);
  box-shadow: 0 4px 12px rgba(255, 152, 0, 0.4);
}

.timeline-item:hover .timeline-marker {
  transform: scale(1.1);
}

.timeline-content {
  background: white;
  padding: 20px;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
  transition: all 0.3s ease;
}

.timeline-content:hover {
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.12);
  transform: translateX(8px);
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
</style>
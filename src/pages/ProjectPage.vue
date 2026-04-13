<template>
  <q-page class="project-page">

    <section class="hero-section">
        <div class="container">
          <div class="row items-center">
            <div class="col-12 col-md-6 hero-content">
              <h1 class="hero-title text-white">
                Empowering Change
                One Project at a Time
              </h1>
                <p class="hero-subtitle text-white">
                    Discover impactful projects and the charities behind them. Explore how your donations are making a difference in communities around the world.
                </p>    
            </div>
          </div>
        </div>
    </section>

  
    <section class="featured-section">
      <div class="container">
        <div class="section-header">
          <h2 class="section-title">Trusted Charities</h2>
        </div>

        <div class="projects-grid">
          <div class="project-card">
            <div class="project-image">
              <img src="../assets/typhoon.jpeg" alt="Typhoon Relief" />
            </div>
            <div class="project-content">
              <h3 class="project-title">Typhoon Relief</h3>
              <p class="project-description">
                Rapid response support for families affected by typhoons, floods, and natural disasters with food, shelter, and supplies.
              </p>
              <div class="project-actions">
                <q-btn
                  unelevated
                  class="donate-btn"
                  label="Donate Now"
                  to="/donate"
                />
                <q-btn
                  flat
                  class="details-btn"
                  label="View details"
                  @click="viewProject(1)"
                />
              </div>
            </div>
          </div>

         
          <div class="project-card">
            <div class="project-image">
              <img src="../assets/medical.jpg" alt="Medical Relief" />
            </div>
            <div class="project-content">
              <h3 class="project-title">Medical Relief</h3>
              <p class="project-description">
                Rapid response support for families affected by typhoons, floods, and natural disasters with food, shelter, and supplies.
              </p>
              <div class="project-actions">
                <q-btn
                  unelevated
                  class="donate-btn"
                  label="Donate Now"
                  to="/donate"
                />
                <q-btn
                  flat
                  class="details-btn"
                  label="View details"
                  @click="viewProject(2)"
                />
              </div>
            </div>
          </div>

     
          <div class="project-card">
            <div class="project-image">
              <img src="../assets/scholar.jpg" alt="Health Support" />
            </div>
            <div class="project-content">
              <h3 class="project-title">Health Support</h3>
              <p class="project-description">
                Rapid response support for families affected by typhoons, floods, and natural disasters with food, shelter, and supplies.
              </p>
              <div class="project-actions">
                <q-btn
                  unelevated
                  class="donate-btn"
                  label="Donate Now"
                  to="/donate"
                />
                <q-btn
                  flat
                  class="details-btn"
                  label="View details"
                  @click="viewProject(3)"
                />
              </div>
            </div>
          </div>

          <div class="project-card">
            <div class="project-image">
              <img src="~assets/food.jpg" alt="Food Security" />
            </div>
            <div class="project-content">
              <h3 class="project-title">Food Security Program</h3>
              <p class="project-description">
                Providing nutritious meals and food assistance to families facing hunger and food insecurity in urban and rural communities.
              </p>
              <div class="project-actions">
                <q-btn
                  unelevated
                  class="donate-btn"
                  label="Donate Now"
                  to="/donate"
                />
                <q-btn
                  flat
                  class="details-btn"
                  label="View details"
                  @click="viewProject(4)"
                />
              </div>
            </div>
          </div>

          <div class="project-card">
            <div class="project-image">
              <img src="~assets/water.jpg" alt="Clean Water Initiative" />
            </div>
            <div class="project-content">
              <h3 class="project-title">Clean Water Initiative</h3>
              <p class="project-description">
                Building water wells and providing clean drinking water access to remote villages and communities without safe water sources.
              </p>
              <div class="project-actions">
                <q-btn
                  unelevated
                  class="donate-btn"
                  label="Donate Now"
                  to="/donate"
                />
                <q-btn
                  flat
                  class="details-btn"
                  label="View details"
                  @click="viewProject(5)"
                />
              </div>
            </div>
          </div>

          <div class="project-card">
            <div class="project-image">
              <img src="~assets/support.jpg" alt="Livelihood Support" />
            </div>
            <div class="project-content">
              <h3 class="project-title">Livelihood Support</h3>
              <p class="project-description">
                Empowering families through skills training, microfinance, and business support to build sustainable income sources.
              </p>
              <div class="project-actions">
                <q-btn
                  unelevated
                  class="donate-btn"
                  label="Donate Now"
                  to="/donate"
                />
                <q-btn
                  flat
                  class="details-btn"
                  label="View details"
                  @click="viewProject(6)"
                />
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    
    <section class="charity-register-section">
      <div class="container">
        <h2 class="register-title">Are you a Charity?</h2>
        <p class="register-subtitle">Register your organization to start receiving donations.</p>
        <q-btn
          unelevated
          class="register-btn"
          label="Register your Charity"
          size="lg"
          @click="showRegisterDialog = true"
        />
      </div>
    </section>


    <q-dialog v-model="showRegisterDialog" :maximized="$q.screen.lt.sm">
      <q-card class="register-dialog-card">

        <!-- Header -->
        <q-card-section class="dialog-header">
          <q-btn
            flat round dense
            icon="close"
            class="dialog-close-btn"
            v-close-popup
          />
          <div class="dialog-icon-wrap">
            <img src="~assets/CrypToCare.png" alt="CrypToCare" class="dialog-logo" />
          </div>
          <div class="dialog-title">Register Your Charity</div>
          <div class="dialog-subtitle">Join our platform to start receiving Bitcoin donations.</div>
        </q-card-section>

        <q-separator class="dialog-separator" />

        <!-- Form body -->
        <q-card-section class="dialog-form-section">

          <div class="form-field">
            <label class="field-label">Charity Name</label>
            <q-input
              v-model="charityForm.name"
              outlined
              dense
              placeholder="Enter charity name"
            />
          </div>

          <div class="form-field">
            <label class="field-label">Charity Address</label>
            <q-input
              v-model="charityForm.address"
              outlined
              dense
              placeholder="Enter address"
            />
          </div>

          <div class="row q-col-gutter-md form-field">
            <div class="col-12 col-sm-6">
              <label class="field-label">Contact Email</label>
              <q-input
                v-model="charityForm.email"
                outlined
                dense
                type="email"
                placeholder="Enter email address"
              />
            </div>
            <div class="col-12 col-sm-6">
              <label class="field-label">Phone Number</label>
              <q-input
                outlined
                dense
                placeholder="Enter phone number"
              />
            </div>
          </div>

          <div class="form-field">
            <label class="field-label">Description</label>
            <q-input
              v-model="charityForm.description"
              outlined
              type="textarea"
              rows="3"
              placeholder="Describe your mission and activities"
            />
          </div>

          <div class="form-field">
            <label class="field-label">Bitcoin Wallet Address</label>
            <q-input
              v-model="charityForm.walletAddress"
              outlined
              dense
              placeholder="Enter Bitcoin wallet address"
            >
              <template v-slot:prepend>
                <q-icon name="account_balance_wallet" color="orange" />
              </template>
            </q-input>
          </div>

          <div class="form-field">
            <label class="field-label">
              Upload Documents
              <span class="optional-label">(optional)</span>
            </label>
            <q-file
              v-model="charityForm.documents"
              outlined
              dense
              placeholder="Choose File"
              class="q-mb-sm"
            >
              <template v-slot:prepend>
                <q-icon name="attach_file" />
              </template>
            </q-file>
            <div class="upload-hint">
              Drag and drop files
              <a href="#" class="dialog-link">here</a>
              or
              <a href="#" class="dialog-link">Browse</a>
            </div>
          </div>

          <q-btn
            unelevated
            class="submit-btn full-width q-mt-sm"
            label="Submit Application"
            no-caps
            @click="submitApplication"
          />

          <div class="terms-text">
            By registering, you agree to our
            <a href="#" class="dialog-link">Terms of service</a>
            and
            <a href="#" class="dialog-link">Privacy policy</a>.
          </div>

        </q-card-section>
      </q-card>
    </q-dialog>

    
    <q-dialog 
      v-model="showDetailsDialog" 
      v-if="selectedProject"
      :maximized="$q.screen.lt.sm"
      transition-show="slide-up"
      transition-hide="slide-down"
    >
      <q-card class="glass-dialog-card responsive-dialog">

        <!-- Hero image with close btn overlay -->
        <div class="details-header-image">
          <img :src="selectedProject.image" :alt="selectedProject.projectTitle" />
          <div class="details-overlay">
            <h2 class="details-project-title">{{ selectedProject.projectTitle }}</h2>
          </div>
          <q-btn
            flat round dense
            icon="close"
            class="details-close-btn"
            v-close-popup
          />
        </div>

        <!-- Scrollable body -->
        <q-card-section class="details-body">

          <!-- Title row -->
          <div class="details-title-row">
            <h3 class="details-org-name">{{ selectedProject.name }}</h3>
            <q-badge :label="selectedProject.status" color="positive" class="details-badge" />
          </div>

          <!-- Category -->
          <div class="details-category">
            <q-icon name="category" size="18px" />
            <span>{{ selectedProject.category }}</span>
          </div>

          <!-- About -->
          <div class="details-section">
            <h4 class="section-label">About This Project</h4>
            <p class="details-text">{{ selectedProject.fullDescription }}</p>
          </div>

          <!-- Mission -->
          <div class="details-section">
            <h4 class="section-label">Mission Statement</h4>
            <p class="details-text details-text--italic">{{ selectedProject.mission }}</p>
          </div>

          <!-- Impact stats -->
          <div class="details-section">
            <h4 class="section-label">Impact Statistics</h4>
            <div class="impact-grid">
              <div v-for="stat in selectedProject.impactStats" :key="stat.label" class="impact-card">
                <div class="impact-value">{{ stat.value }}</div>
                <div class="impact-label">{{ stat.label }}</div>
              </div>
            </div>
          </div>

          <!-- Fundraising progress -->
          <div class="details-section">
            <h4 class="section-label">Fundraising Progress</h4>
            <div class="progress-labels">
              <span class="progress-raised">{{ selectedProject.amountRaised }}</span>
              <span class="progress-goal">Goal: {{ selectedProject.projectGoal }}</span>
            </div>
            <q-linear-progress
              :value="parseInt(selectedProject.amountRaised.replace(/[^0-9]/g, '')) / parseInt(selectedProject.projectGoal.replace(/[^0-9]/g, ''))"
              color="primary"
              size="12px"
              class="progress-bar"
            />
            <div class="progress-beneficiaries">
              Beneficiaries: <strong>{{ selectedProject.beneficiaries }}</strong>
            </div>
          </div>

          <!-- Contact -->
          <div class="details-section">
            <h4 class="section-label">Contact Information</h4>
            <div class="contact-info">
              <div class="contact-item">
                <q-icon name="email" size="20px" color="primary" />
                <div>
                  <div class="contact-label">Email</div>
                  <div class="contact-value">{{ selectedProject.contactEmail }}</div>
                </div>
              </div>
              <div class="contact-item">
                <q-icon name="phone" size="20px" color="primary" />
                <div>
                  <div class="contact-label">Phone</div>
                  <div class="contact-value">{{ selectedProject.contactPhone }}</div>
                </div>
              </div>
              <div class="contact-item">
                <q-icon name="place" size="20px" color="primary" />
                <div>
                  <div class="contact-label">Address</div>
                  <div class="contact-value">{{ selectedProject.address }}</div>
                </div>
              </div>
            </div>
          </div>

          <!-- Wallet -->
          <div class="details-section">
            <h4 class="section-label">Bitcoin Wallet Address</h4>
            <div class="wallet-container">
              <div class="wallet-address">{{ selectedProject.walletAddress }}</div>
              <q-btn
                flat dense
                icon="content_copy"
                color="primary"
                @click="copyWalletAddress(selectedProject.walletAddress)"
              >
                <q-tooltip>Copy Address</q-tooltip>
              </q-btn>
            </div>
          </div>

          <!-- Footer -->
          <div class="details-footer">
            <span>Registered since {{ selectedProject.registrationDate }}</span>
          </div>

        </q-card-section>

        <q-card-actions align="center" class="details-actions">
          <q-btn
            unelevated
            color="primary"
            label="Close"
            no-caps
            class="details-close-action-btn"
            v-close-popup
          />
        </q-card-actions>

      </q-card>
    </q-dialog>
  </q-page>
</template>

<script setup>
import { ref } from 'vue'
import { useQuasar } from 'quasar'
import typhoonImg from '../assets/typhoon.jpeg'
import medicalImg from '../assets/medical.jpg'
import scholarImg from '../assets/scholar.jpg'
import foodImg from '../assets/food.jpg'
import waterImg from '../assets/water.jpg'
import supportImg from '../assets/support.jpg'

const $q = useQuasar()
const showRegisterDialog = ref(false)
const showDetailsDialog = ref(false)
const selectedProject = ref(null)

const charityForm = ref({
  name: '',
  address: '',
  email: '',
  phone: '',
  description: '',
  walletAddress: '',
  documents: null
})


const projectsData = {
  1: {
    id: 1,
    name: 'Philippine Disaster Response Foundation',
    projectTitle: 'Typhoon Relief Program',
    image: typhoonImg,
    shortDescription: 'Rapid response support for families affected by typhoons, floods, and natural disasters with food, shelter, and supplies.',
    fullDescription: 'Our Typhoon Relief Program provides immediate emergency response to communities devastated by natural disasters. We deploy relief teams within 24 hours of a disaster, delivering essential supplies including food packs, clean water, emergency shelter materials, and medical aid. Our program has helped over 50,000 families recover from disasters across the Philippines.',
    mission: 'To provide rapid and effective disaster response, ensuring affected communities receive immediate aid and long-term recovery support.',
    contactEmail: 'relief@pdrf.org.ph',
    contactPhone: '+63 2 8123-4567',
    address: '123 Disaster Response Ave, Quezon City, Metro Manila 1100, Philippines',
    walletAddress: 'bc1qxy2kgdygjrsqtzq2n0yrf2493p83kkfjhx0wlh',
    registrationDate: 'January 15, 2023',
    status: 'Active',
    beneficiaries: '50,000+ families',
    projectGoal: '₱10,000,000',
    amountRaised: '₱6,500,000',
    category: 'Disaster Relief',
    impactStats: [
      { label: 'Relief Operations', value: '150+' },
      { label: 'Communities Served', value: '85' },
      { label: 'Volunteers', value: '500+' }
    ]
  },
  2: {
    id: 2,
    name: 'Healthcare Access Foundation',
    projectTitle: 'Medical Relief Program',
    image: medicalImg,
    shortDescription: 'Providing medical assistance, medicines, and healthcare services to underserved communities.',
    fullDescription: 'The Medical Relief Program delivers comprehensive healthcare services to remote and underserved communities. We operate mobile medical clinics, provide free consultations, distribute essential medicines, and conduct health education programs. Our team of volunteer doctors and nurses has treated over 75,000 patients annually.',
    mission: 'To ensure every Filipino has access to quality healthcare regardless of their economic status or geographic location.',
    contactEmail: 'info@healthcareaccess.org.ph',
    contactPhone: '+63 2 8234-5678',
    address: '456 Health Center Road, Makati City, Metro Manila 1200, Philippines',
    walletAddress: 'bc1qar0srrr7xfkvy5l643lydnw9re59gtzzwf5mdq',
    registrationDate: 'March 10, 2022',
    status: 'Active',
    beneficiaries: '75,000+ patients annually',
    projectGoal: '₱15,000,000',
    amountRaised: '₱9,200,000',
    category: 'Healthcare',
    impactStats: [
      { label: 'Medical Missions', value: '200+' },
      { label: 'Free Consultations', value: '75,000+' },
      { label: 'Partner Hospitals', value: '25' }
    ]
  },
  3: {
    id: 3,
    name: 'Community Health & Wellness Association',
    projectTitle: 'Health Support Initiative',
    image: scholarImg,
    shortDescription: 'Comprehensive health and wellness programs for vulnerable communities.',
    fullDescription: 'Our Health Support Initiative focuses on preventive healthcare, nutrition programs, mental health services, and community wellness education. We run health awareness campaigns, provide vitamin supplementation for children, and offer counseling services for families in need.',
    mission: 'To promote holistic health and wellness in communities, emphasizing prevention and early intervention.',
    contactEmail: 'support@communityhealthph.org',
    contactPhone: '+63 2 8345-6789',
    address: '789 Wellness Street, Pasig City, Metro Manila 1600, Philippines',
    walletAddress: 'bc1qw508d6qejxtdg4y5r3zarvary0c5xw7kv8f3t4',
    registrationDate: 'June 5, 2023',
    status: 'Active',
    beneficiaries: '30,000+ individuals',
    projectGoal: '₱8,000,000',
    amountRaised: '₱5,100,000',
    category: 'Health & Wellness',
    impactStats: [
      { label: 'Health Screenings', value: '30,000+' },
      { label: 'Children Supported', value: '5,000+' },
      { label: 'Wellness Programs', value: '50+' }
    ]
  },
  4: {
    id: 4,
    name: 'Feed the Nation Foundation',
    projectTitle: 'Food Security Program',
    image: foodImg,
    shortDescription: 'Providing nutritious meals and food assistance to families facing hunger and food insecurity.',
    fullDescription: 'The Food Security Program addresses hunger and malnutrition by operating community kitchens, distributing food packs, and implementing sustainable agriculture projects. We serve over 10,000 meals daily and teach families sustainable food production methods.',
    mission: 'To eliminate hunger and achieve food security for all Filipino families through direct aid and sustainable solutions.',
    contactEmail: 'contact@feedthenation.org.ph',
    contactPhone: '+63 2 8456-7890',
    address: '321 Nutrition Boulevard, Mandaluyong City, Metro Manila 1550, Philippines',
    walletAddress: 'bc1q3j8cjnk3h2gstjw2r77qkxh6y9c4vz6rkvkyun',
    registrationDate: 'September 20, 2022',
    status: 'Active',
    beneficiaries: '100,000+ individuals',
    projectGoal: '₱20,000,000',
    amountRaised: '₱12,800,000',
    category: 'Food Security',
    impactStats: [
      { label: 'Daily Meals Served', value: '10,000+' },
      { label: 'Food Pantries', value: '45' },
      { label: 'Urban Gardens', value: '30' }
    ]
  },
  5: {
    id: 5,
    name: 'Water Life Philippines',
    projectTitle: 'Clean Water Initiative',
    image: waterImg,
    shortDescription: 'Building water wells and providing clean drinking water access to remote villages.',
    fullDescription: 'The Clean Water Initiative brings safe, clean drinking water to communities without access to water sources. We construct deep wells, install water filtration systems, and conduct hygiene education programs. To date, we have provided clean water access to over 200 communities.',
    mission: 'To provide sustainable access to clean water and sanitation for every community in the Philippines.',
    contactEmail: 'info@waterlifeph.org',
    contactPhone: '+63 2 8567-8901',
    address: '654 Aqua Street, Taguig City, Metro Manila 1630, Philippines',
    walletAddress: 'bc1qyzzjcm0e0cxy2kqvhukqhk59tksn6gw3xrn8ty',
    registrationDate: 'February 12, 2023',
    status: 'Active',
    beneficiaries: '200+ communities',
    projectGoal: '₱25,000,000',
    amountRaised: '₱18,500,000',
    category: 'Water & Sanitation',
    impactStats: [
      { label: 'Wells Built', value: '150+' },
      { label: 'People Served', value: '120,000+' },
      { label: 'Filtration Systems', value: '80+' }
    ]
  },
  6: {
    id: 6,
    name: 'Empowerment Through Enterprise Foundation',
    projectTitle: 'Livelihood Support Program',
    image: supportImg,
    shortDescription: 'Empowering families through skills training, microfinance, and business support.',
    fullDescription: 'Our Livelihood Support Program helps families achieve financial independence through entrepreneurship training, skills development, microfinance loans, and ongoing business mentorship. We have helped establish over 2,000 micro-enterprises across the Philippines.',
    mission: 'To break the cycle of poverty by empowering individuals with skills, capital, and support to build sustainable businesses.',
    contactEmail: 'support@empowermentph.org',
    contactPhone: '+63 2 8678-9012',
    address: '987 Enterprise Avenue, Parañaque City, Metro Manila 1700, Philippines',
    walletAddress: 'bc1qrv5k8hc2j3sfrnpgqd8evz2vtfk7npvz72u6aw',
    registrationDate: 'April 18, 2022',
    status: 'Active',
    beneficiaries: '15,000+ families',
    projectGoal: '₱12,000,000',
    amountRaised: '₱8,700,000',
    category: 'Livelihood & Enterprise',
    impactStats: [
      { label: 'Businesses Launched', value: '2,000+' },
      { label: 'Jobs Created', value: '5,000+' },
      { label: 'Training Programs', value: '250+' }
    ]
  }
}

const viewProject = (projectId) => {
  selectedProject.value = projectsData[projectId]
  showDetailsDialog.value = true
}

const submitApplication = () => {
  console.log('Submitting charity application:', charityForm.value)
  showRegisterDialog.value = false
}

const copyWalletAddress = (address) => {
  navigator.clipboard.writeText(address)
  $q.notify({
    message: 'Wallet address copied to clipboard!',
    color: 'positive',
    position: 'top',
    timeout: 2000,
    icon: 'check_circle'
  })
}
</script>

<style scoped>
.project-page {
  background: #f5f5f5;
}

.hero-section {
  position: relative;
  min-height: 80vh;
  display: flex;
  align-items: center;
  background-image: url('../assets/project.jpg');
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
  overflow: hidden;
}

.hero-section::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: linear-gradient(135deg, rgba(0, 102, 204, 0.301) 0%, rgba(0, 51, 153, 0.75) 100%);
  z-index: 1;
}

.hero-section .container {
  position: relative;
  z-index: 2;
}

.hero-title {
  font-size: 4rem;
  font-weight: 800;
  line-height: 1.2;
  margin-bottom: 24px;
  text-shadow: 2px 4px 8px rgba(0, 0, 0, 0.6);
}

.hero-subtitle {
  font-size: 1.25rem;
  line-height: 1.6;
  margin-bottom: 32px;
  text-shadow: 1px 2px 4px rgba(0, 0, 0, 0.6);
  max-width: 600px;
}


.featured-section {
  padding: 80px 20px 60px;
  background: #f5f5f5;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 16px;
}

.section-header {
  text-align: center;
  margin-bottom: 50px;
  position: relative;
}

.section-header::before,
.section-header::after {
  content: '';
  position: absolute;
  top: 50%;
  width: 25%;
  height: 2px;
  background: #333;
}

.section-header::before {
  left: 10%;
}

.section-header::after {
  right: 10%;
}

.section-title {
  font-size: 36px;
  font-weight: 700;
  color: #000;
  margin: 0;
  display: inline-block;
  position: relative;
  z-index: 1;
}

.projects-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 30px;
}


.project-card {
  background: white;
  border: 1px solid #2f3030;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(248, 248, 250, 0.509);
  transition: all 0.3s ease;
  overflow: hidden;
}

.project-card:hover {
  transform: translateY(-5px);
  box-shadow: 15px 10px 10px rgba(9, 111, 212, 0.82);
}

.project-image {
  position: relative;
  height: 220px;
  overflow: hidden;
  box-shadow: inset;
}

.project-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.project-content {
  padding: 24px;
}

.project-title {
  font-size: 20px;
  font-weight: 700;
  color: #000;
  margin: 0 0 12px 0;
  text-align: center;
}

.project-description {
  font-size: 14px;
  color: #333;
  line-height: 1.6;
  margin: 0 0 20px 0;
  text-align: left;
  min-height: 72px;
}

.project-actions {
  display: flex;
  gap: 10px;
  align-items: center;
}

.donate-btn {
  background: #0080ff;
  color: white;
  font-weight: 600;
  margin-left: 10px;
  padding: 10px 20px;
  border-radius: 4px;
  text-transform: none;
  font-size: 14px;
  transition: all 0.3s ease;
}

.donate-btn:hover {
  background: #0066cc;
  box-shadow: 0 4px 12px rgba(0, 128, 255, 0.3);
}

.details-btn {
  color: #0080ff;
  font-weight: 600;
  margin-left: 20px;
  padding: 10px 20px;
  text-transform: none;
  font-size: 14px;
  text-decoration: none;
}

.details-btn:hover {
  background: rgba(0, 128, 255, 0.05);
  text-decoration: underline;
}


.charity-register-section {
  padding: 80px 20px;
  background: #f5f5f5;
  text-align: center;
  position: relative;
}

.charity-register-section::before {
  content: '';
  position: absolute;
  top: 50px;
  left: 50%;
  transform: translateX(-50%);
  width: 60%;
  height: 2px;
  background: #333;
}

.register-title {
  font-size: 36px;
  font-weight: 700;
  color: #000;
  margin: 0 0 16px 0;
  padding-top: 30px;
}

.register-subtitle {
  font-size: 16px;
  color: #333;
  margin: 0 0 30px 0;
}

.register-btn {
  background: #0080ff;
  color: white;
  font-weight: 600;
  padding: 14px 40px;
  border-radius: 10px;
  text-transform: none;
  font-size: 16px;
  transition: all 0.3s ease;
}

.register-btn:hover {
  background: #0066cc;
  box-shadow: 0 6px 20px rgba(0, 128, 255, 0.3);
}


@media (max-width: 1024px) {
  .projects-grid {
    grid-template-columns: repeat(2, 1fr);
    gap: 24px;
  }
  
  .section-title {
    font-size: 32px;
  }
  
  .section-header::before,
  .section-header::after {
    width: 20%;
  }
  
  .section-header::before {
    left: 5%;
  }
  
  .section-header::after {
    right: 5%;
  }
}

@media (max-width: 768px) {
  .hero-title {
    font-size: 2.4rem;
  }

  .hero-subtitle {
    font-size: 1rem;
  }

  .featured-section {
    padding: 60px 20px 40px;
  }
  
  .projects-grid {
    grid-template-columns: 1fr;
    gap: 24px;
  }
  
  .section-title,
  .register-title {
    font-size: 28px;
  }
  
  .section-header::before,
  .section-header::after {
    display: none;
  }
  
  .charity-register-section::before {
    width: 80%;
  }
}

@media (max-width: 480px) {
  .section-title,
  .register-title {
    font-size: 24px;
  }
  
  .project-content {
    padding: 20px;
  }
  
  .project-title {
    font-size: 18px;
  }
  
  .project-actions {
    flex-direction: column;
  }
  
  .donate-btn,
  .details-btn {
    width: 100%;
    justify-content: center;
  }
}


/* ── Register Dialog ─────────────────────────────── */
.register-dialog-card {
  width: 100%;
  max-width: 560px;
  border-radius: 16px;
  overflow: hidden;
  display: flex;
  flex-direction: column;
  max-height: 92dvh;
  background: #ffffff;
}

@media (max-width: 599px) {
  .register-dialog-card {
    border-radius: 0;
    max-height: 100dvh;
    min-height: 100dvh;
    max-width: 100vw;
  }
}

/* Header */
.dialog-header {
  position: relative;
  text-align: center;
  padding: 28px 24px 20px;
  background: linear-gradient(135deg, #0080ff 0%, #00bfff 100%);
  color: #fff;
  flex-shrink: 0;
}

.dialog-close-btn {
  position: absolute;
  top: 12px;
  right: 12px;
  color: rgba(255, 255, 255, 0.85) !important;
}

.dialog-close-btn:hover {
  background: rgba(255, 255, 255, 0.15) !important;
}

.dialog-icon-wrap {
  margin-bottom: 12px;
  display: flex;
  justify-content: center;
}

.dialog-logo {
  height: 56px;
  width: auto;
  object-fit: contain;
  filter: drop-shadow(0 2px 6px rgba(0,0,0,0.25));
}

.dialog-title {
  font-size: 22px;
  font-weight: 700;
  color: #fff;
  margin-bottom: 6px;
}

.dialog-subtitle {
  font-size: 14px;
  color: rgba(255, 255, 255, 0.85);
}

.dialog-separator {
  flex-shrink: 0;
}

/* Form body */
.dialog-form-section {
  padding: 24px;
  overflow-y: auto;
  flex: 1 1 auto;
}

.optional-label {
  font-weight: 400;
  color: #999;
  font-size: 12px;
  margin-left: 4px;
}

.upload-hint {
  text-align: center;
  font-size: 13px;
  color: #777;
  margin-top: 4px;
}

.dialog-link {
  color: #0080ff;
  text-decoration: none;
  font-weight: 500;
}

.dialog-link:hover {
  text-decoration: underline;
}

.submit-btn {
  border-radius: 8px;
  padding: 12px 0;
  font-weight: 600;
  font-size: 15px;
  background: linear-gradient(90deg, #0080ff 0%, #00bfff 100%) !important;
  color: #fff !important;
  letter-spacing: 0.3px;
}

.submit-btn:hover {
  opacity: 0.92;
}

.terms-text {
  text-align: center;
  margin-top: 14px;
  font-size: 12px;
  color: #777;
}

/* Mobile form padding */
@media (max-width: 599px) {
  .dialog-form-section {
    padding: 16px;
  }

  .dialog-header {
    padding: 24px 16px 16px;
  }

  .dialog-title {
    font-size: 20px;
  }
}

/* ── Register Dialog — Dark Mode ─────────────────── */
.body--dark .register-dialog-card {
  background: #1a2240;
}

.body--dark .dialog-header {
  background: linear-gradient(135deg, #0d47a1 0%, #0080c8 100%);
}

.body--dark .dialog-separator {
  background: #2e3f6e;
}

.body--dark .dialog-form-section {
  background: #1a2240;
}

.body--dark .field-label {
  color: #c0d4f0;
}

.body--dark .optional-label {
  color: #5a7099;
}

.body--dark .upload-hint {
  color: #6a88aa;
}

.body--dark .dialog-link {
  color: #5d9cf5;
}

.body--dark .terms-text {
  color: #6a88aa;
}


.glass-dialog-card {
  background: #ffffff;
  box-shadow: 0 12px 40px rgba(0, 0, 0, 0.18);
}

.responsive-dialog {
  width: 100%;
  min-width: min(740px, 96vw);
  max-width: 800px;
  border-radius: 12px;
  max-height: 90dvh;
  overflow: hidden;
  display: flex;
  flex-direction: column;
}

/* Header image */
.details-header-image {
  position: relative;
  width: 100%;
  height: 260px;
  overflow: hidden;
  flex-shrink: 0;
}

.details-header-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.details-overlay {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  background: linear-gradient(to top, rgba(0, 0, 0, 0.75) 0%, transparent 100%);
  padding: 40px 20px 16px;
}

.details-project-title {
  color: #fff;
  font-size: 22px;
  font-weight: 700;
  margin: 0;
  text-shadow: 1px 2px 6px rgba(0, 0, 0, 0.5);
}

.details-close-btn {
  position: absolute;
  top: 10px;
  right: 10px;
  color: #fff !important;
  background: rgba(0, 0, 0, 0.35) !important;
  backdrop-filter: blur(4px);
}

.details-close-btn:hover {
  background: rgba(0, 0, 0, 0.55) !important;
}

/* Scrollable body */
.details-body {
  padding: 20px 24px;
  overflow-y: auto;
  flex: 1 1 auto;
}

.details-title-row {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 12px;
  margin-bottom: 10px;
  flex-wrap: wrap;
}

.details-org-name {
  margin: 0;
  font-size: 20px;
  font-weight: 700;
  color: #222;
  flex: 1;
}

.details-badge {
  padding: 5px 10px;
  font-size: 12px;
  white-space: nowrap;
  flex-shrink: 0;
}

.details-category {
  display: flex;
  align-items: center;
  gap: 6px;
  color: #0080ff;
  font-weight: 500;
  font-size: 14px;
  margin-bottom: 20px;
}

.details-section {
  margin-bottom: 22px;
}

.section-label {
  font-size: 15px;
  font-weight: 700;
  color: #222;
  margin-bottom: 10px;
  display: flex;
  align-items: center;
}

.section-label::before {
  content: '';
  width: 4px;
  height: 18px;
  background: #0080ff;
  margin-right: 10px;
  border-radius: 2px;
  flex-shrink: 0;
}

.details-text {
  font-size: 14px;
  line-height: 1.75;
  color: #555;
  margin: 0;
}

.details-text--italic {
  font-style: italic;
  color: #666;
}

/* Progress */
.progress-labels {
  display: flex;
  justify-content: space-between;
  margin-bottom: 8px;
  flex-wrap: wrap;
  gap: 4px;
}

.progress-raised {
  font-weight: 700;
  color: #0080ff;
  font-size: 15px;
}

.progress-goal {
  color: #777;
  font-size: 14px;
}

.progress-bar {
  border-radius: 6px;
  margin-bottom: 8px;
}

.progress-beneficiaries {
  text-align: center;
  color: #777;
  font-size: 13px;
}

/* Impact grid */
.impact-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 14px;
}

.impact-card {
  background: #f0f5ff;
  padding: 18px 14px;
  border: 1px solid #c5d8ff;
  border-radius: 10px;
  text-align: center;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.impact-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 6px 18px rgba(0, 128, 255, 0.2);
}

.impact-value {
  font-size: 26px;
  font-weight: 700;
  color: #0060cc;
  margin-bottom: 6px;
}

.impact-label {
  font-size: 12px;
  color: #555;
  line-height: 1.4;
}

/* Contact */
.contact-info {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.contact-item {
  display: flex;
  align-items: flex-start;
  gap: 12px;
  padding: 12px;
  background: #f8f9fa;
  border-radius: 8px;
}

.contact-label {
  font-size: 11px;
  color: #999;
  margin-bottom: 3px;
  text-transform: uppercase;
  letter-spacing: 0.4px;
}

.contact-value {
  font-size: 14px;
  color: #333;
  font-weight: 500;
  word-break: break-word;
}

/* Wallet */
.wallet-container {
  display: flex;
  align-items: center;
  background: #f8f9fa;
  padding: 12px 16px;
  border-radius: 8px;
  border: 1px solid #e0e0e0;
  gap: 8px;
}

.wallet-address {
  flex: 1;
  font-family: 'Courier New', monospace;
  font-size: 13px;
  color: #333;
  word-break: break-all;
  line-height: 1.5;
}

/* Footer */
.details-footer {
  text-align: center;
  margin-top: 16px;
  padding-top: 16px;
  border-top: 1px solid #ebebeb;
  color: #aaa;
  font-size: 13px;
}

.details-actions {
  padding: 12px 24px 20px;
  flex-shrink: 0;
}

.details-close-action-btn {
  min-width: 130px;
  border-radius: 8px;
  font-weight: 600;
}

/* ── Details Dialog — Mobile ─────────────────────── */
@media (max-width: 768px) {
  .responsive-dialog {
    min-width: 92vw;
    max-width: 96vw;
    max-height: 88dvh;
    border-radius: 10px;
  }

  .details-header-image {
    height: 200px;
  }

  .details-project-title {
    font-size: 18px;
  }

  .details-body {
    padding: 16px;
  }

  .details-org-name {
    font-size: 16px;
  }

  .impact-grid {
    grid-template-columns: repeat(3, 1fr);
    gap: 10px;
  }

  .impact-value {
    font-size: 20px;
  }
}

@media (max-width: 480px) {
  .responsive-dialog {
    min-width: 96vw;
    max-width: 98vw;
    max-height: 88dvh;
    border-radius: 8px;
  }

  .details-header-image {
    height: 160px;
  }

  .details-project-title {
    font-size: 15px;
  }

  .details-org-name {
    font-size: 14px;
  }

  .section-label {
    font-size: 13px;
  }

  .details-text {
    font-size: 13px;
  }

  .impact-grid {
    grid-template-columns: 1fr;
    gap: 10px;
  }

  .impact-value {
    font-size: 22px;
  }

  .wallet-address {
    font-size: 11px;
  }

  .contact-item {
    padding: 10px 8px;
  }

  .progress-raised {
    font-size: 14px;
  }
}

/* shared util */
.q-dialog__backdrop {
  backdrop-filter: blur(4px);
  -webkit-backdrop-filter: blur(4px);
}

.form-field {
  margin-bottom: 20px;
}

.field-label {
  display: block;
  font-size: 14px;
  font-weight: 600;
  color: #000;
  margin-bottom: 8px;
}

/* ── ProjectPage Dark Mode ───────────────────────────────────── */
.body--dark .project-page {
  background: #0f1629;
}

/* Featured section */
.body--dark .featured-section {
  background: #0f1629;
}

.body--dark .section-header::before,
.body--dark .section-header::after {
  background: #2e3f6e;
}

.body--dark .section-title {
  color: #e0eaff;
}

/* Project cards */
.body--dark .project-card {
  background: #1a2240;
  border-color: #2e3f6e;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
}

.body--dark .project-card:hover {
  box-shadow: 0 10px 28px rgba(9, 111, 212, 0.45);
}

.body--dark .project-title {
  color: #d8e8ff;
}

.body--dark .project-description {
  color: #8fa8cb;
}

.body--dark .details-btn {
  color: #5d9cf5;
}

.body--dark .details-btn:hover {
  background: rgba(93, 156, 245, 0.1);
}

/* Register section */
.body--dark .charity-register-section {
  background: #0f1629;
}

.body--dark .charity-register-section::before {
  background: #2e3f6e;
}

.body--dark .register-title {
  color: #e0eaff;
}

.body--dark .register-subtitle {
  color: #8fa8cb;
}

/* ── Details Dialog — Dark Mode ──────────────────── */
.body--dark .glass-dialog-card {
  background: #131e35;
}

.body--dark .details-org-name {
  color: #dce8ff;
}

.body--dark .details-category {
  color: #5d9cf5;
}

.body--dark .section-label {
  color: #c0d4f0;
}

.body--dark .details-text {
  color: #8fa8cb;
}

.body--dark .details-text--italic {
  color: #7a96b8;
}

.body--dark .progress-goal {
  color: #6a88aa;
}

.body--dark .progress-beneficiaries {
  color: #6a88aa;
}

.body--dark .impact-card {
  background: #1a2a4a;
  border-color: #2e3f6e;
}

.body--dark .impact-value {
  color: #7ecbff;
}

.body--dark .impact-label {
  color: #8fa8cb;
}

.body--dark .contact-item {
  background: #0f1a2e;
}

.body--dark .contact-label {
  color: #5a7099;
}

.body--dark .contact-value {
  color: #c0d4f0;
}

.body--dark .wallet-container {
  background: #0f1a2e;
  border-color: #2e3f6e;
}

.body--dark .wallet-address {
  color: #7ecbff;
}

.body--dark .details-footer {
  border-top-color: #1e2e4a;
  color: #5a7099;
}

.body--dark .details-actions {
  background: #131e35;
}
</style>
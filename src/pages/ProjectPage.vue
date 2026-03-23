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


    <q-dialog v-model="showRegisterDialog">
      <q-card style="min-width: 500px; max-width: 600px; border-radius: 5px;">
        <q-card-section class="text-center" style="padding: 24px 24px 16px;">
          <div style="margin-bottom: 16px;">
            <q-icon name="currency_bitcoin" size="48px" color="orange" />
          </div>
          <div class="dialog-title">Register Your Charity</div>
          <div class="dialog-subtitle">Join our platform to start receiving Bitcoins donations.</div>
        </q-card-section>

        <q-card-section style="padding: 0 24px 24px;">
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
            <div class="col-6">
              <label class="field-label">Contact Email</label>
              <q-input
                v-model="charityForm.email"
                outlined
                dense
                type="email"
                placeholder="Enter email address"
              />
            </div>
            <div class="col-6">
              <label class="field-label">Phone Number</label>
              <q-input
                v-model="charityForm.phone"
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
            />
          </div>

          <div class="form-field">
            <label class="field-label">Upload Documents <span style="color: #999;">(optional)</span></label>
            <q-file
              v-model="charityForm.documents"
              outlined
              dense
              placeholder="Choose File"
              style="margin-bottom: 8px;"
            >
              <template v-slot:prepend>
                <q-icon name="attach_file" />
              </template>
            </q-file>
            <div style="text-align: center; font-size: 13px; color: #666;">
              Drag and drop files <a href="#" style="color: #0080ff; text-decoration: none;">here</a> or <a href="#" style="color: #0080ff; text-decoration: none;">Browse</a>
            </div>
          </div>

          <q-btn
            unelevated
            class="submit-btn"
            label="Submit Application"
            color="primary"
            style="width: 100%; padding: 12px; background: #00BFFF; font-weight: 600; font-size: 15px; margin-top: 8px;"
            @click="submitApplication"
          />

          <div style="text-align: center; margin-top: 16px; font-size: 13px; color: #666;">
            By registering, you agree to our 
            <a href="#" style="color: #0080ff; text-decoration: none;">Terms of service</a> 
            and 
            <a href="#" style="color: #0080ff; text-decoration: none;">Privacy policy</a>.
          </div>
        </q-card-section>
      </q-card>
    </q-dialog>

    
    <q-dialog 
      v-model="showDetailsDialog" 
      v-if="selectedProject"
      :maximized="false"
      transition-show="slide-up"
      transition-hide="slide-down"
    >
      <q-card class="glass-dialog-card responsive-dialog">
        <div class="details-header-image">
          <img :src="selectedProject.image" :alt="selectedProject.projectTitle" />
          <div class="details-overlay">
            <h2 class="details-project-title">{{ selectedProject.projectTitle }}</h2>
          </div>
        </div>

        <q-card-section style="padding: 24px;">
          <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px;">
            <h3 style="margin: 0; font-size: 24px; color: #333;">{{ selectedProject.name }}</h3>
            <q-badge :label="selectedProject.status" color="positive" style="padding: 6px 12px; font-size: 12px;" />
          </div>

          <div style="display: flex; align-items: center; margin-bottom: 20px; color: #0080ff;">
            <q-icon name="category" size="20px" style="margin-right: 8px;" />
            <span style="font-weight: 500;">{{ selectedProject.category }}</span>
          </div>

    
          <div class="details-section">
            <h4 class="section-label">About This Project</h4>
            <p class="details-text">{{ selectedProject.fullDescription }}</p>
          </div>

          
          <div class="details-section">
            <h4 class="section-label">Mission Statement</h4>
            <p class="details-text" style="font-style: italic; color: #555;">{{ selectedProject.mission }}</p>
          </div>

     
          <div class="details-section">
            <h4 class="section-label">Impact Statistics</h4>
            <div class="impact-grid">
              <div v-for="stat in selectedProject.impactStats" :key="stat.label" class="impact-card">
                <div class="impact-value">{{ stat.value }}</div>
                <div class="impact-label">{{ stat.label }}</div>
              </div>
            </div>
          </div>

         
          <div class="details-section">
            <h4 class="section-label">Fundraising Progress</h4>
            <div style="display: flex; justify-content: space-between; margin-bottom: 8px;">
              <span style="font-weight: 600; color: #0080ff;">{{ selectedProject.amountRaised }}</span>
              <span style="color: #666;">Goal: {{ selectedProject.projectGoal }}</span>
            </div>
            <q-linear-progress 
              :value="parseInt(selectedProject.amountRaised.replace(/[^0-9]/g, '')) / parseInt(selectedProject.projectGoal.replace(/[^0-9]/g, ''))" 
              color="primary" 
              size="12px" 
              style="border-radius: 6px; margin-bottom: 8px;"
            />
            <div style="text-align: center; color: #666; font-size: 13px;">
              Beneficiaries: <strong>{{ selectedProject.beneficiaries }}</strong>
            </div>
          </div>

          
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

        
          <div class="details-section">
            <h4 class="section-label">Bitcoin Wallet Address</h4>
            <div class="wallet-container">
              <div class="wallet-address">{{ selectedProject.walletAddress }}</div>
              <q-btn 
                flat 
                dense 
                icon="content_copy" 
                color="primary"
                @click="copyWalletAddress(selectedProject.walletAddress)"
              >
                <q-tooltip>Copy Address</q-tooltip>
              </q-btn>
            </div>
          </div>

         
          <div style="text-align: center; margin-top: 20px; padding-top: 20px; border-top: 1px solid #e0e0e0;">
            <span style="color: #999; font-size: 13px;">
              Registered since {{ selectedProject.registrationDate }}
            </span>
          </div>
        </q-card-section>

        
        <q-card-actions align="center" style="padding: 0 24px 24px;">
          <q-btn 
            unelevated
            color="primary"
            label="Close" 
            size="lg"
            style="max-width: 200px; padding: 12px; background: #0080ff; font-weight: 600;"
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


.dialog-title {
  font-size: 24px;
  font-weight: 700;
  color: #000;
  margin-bottom: 8px;
}

.dialog-subtitle {
  font-size: 14px;
  color: #666;
}


.glass-dialog-card {
  background: rgba(255, 255, 255, 0.95) !important;
  backdrop-filter: blur(10px) saturate(180%);
  -webkit-backdrop-filter: blur(10px) saturate(180%);
  box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.2);
}

.responsive-dialog {
  min-width: 700px;
  max-width: 800px;
  width: 100%;
  border-radius: 10px;
  max-height: 90vh;
  overflow: hidden;
  display: flex;
  flex-direction: column;
}

.responsive-dialog .q-card__section {
  overflow-y: auto;
}

/* Responsive breakpoints */
@media (max-width: 1024px) {
  .responsive-dialog {
    min-width: 600px;
    max-width: 700px;
  }
  
  .details-header-image {
    height: 500px !important;
  }
}

@media (max-width: 768px) {
  .responsive-dialog {
    min-width: 90vw;
    max-width: 95vw;
    max-height: 85vh;
  }
  
  .details-header-image {
    height: 450px !important;
  }
  
  .details-project-title {
    font-size: 20px !important;
  }
  
  .responsive-dialog .q-card__section {
    padding: 16px !important;
  }
  
  .impact-grid {
    grid-template-columns: 1fr !important;
    gap: 12px !important;
  }
}

@media (max-width: 480px) {
  .responsive-dialog {
    min-width: 95vw;
    max-width: 98vw;
    max-height: 80vh;
    border-radius: 8px;
  }
  
  .details-header-image {
    height: 400px !important;
  }
  
  .details-project-title {
    font-size: 18px !important;
  }
  
  .responsive-dialog h3 {
    font-size: 16px !important;
  }
  
  .section-label {
    font-size: 14px !important;
  }
  
  .details-text {
    font-size: 13px !important;
  }
  
  .contact-item {
    padding: 8px !important;
  }
  
  .wallet-address {
    font-size: 10px !important;
  }
}

.glass-dialog-card .q-card__section {
  background: transparent;
}


.q-dialog__backdrop {
  background: rgba(0, 0, 0, 0.3) !important;
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

.submit-btn {
  border-radius: 8px;
}


.details-header-image {
  position: relative;
  width: 100%;
  height: 600px;
  overflow: hidden;
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
  background: linear-gradient(to top, rgba(0, 0, 0, 0.8) 0%, transparent 100%);
  padding: 30px 24px 20px;
}

.details-project-title {
  color: white;
  font-size: 28px;
  font-weight: 700;
  margin: 0;
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5);
}

.details-section {
  margin-bottom: 24px;
}

.section-label {
  font-size: 16px;
  font-weight: 700;
  color: #333;
  margin-bottom: 12px;
  display: flex;
  align-items: center;
}

.section-label::before {
  content: '';
  width: 4px;
  height: 20px;
  background: #0080ff;
  margin-right: 10px;
  border-radius: 2px;
}

.details-text {
  font-size: 15px;
  line-height: 1.7;
  color: #555;
  margin: 0;
}

.impact-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 16px;
}

.impact-card {
  background: linear-gradient(135deg, #f7f8fa80 0%, #edf0f252 100%);
  padding: 20px;
  border: #1449e8 solid 1px;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgb(13, 114, 229);
  transition: all 0.3s ease;
}

.impact-card:hover {
  transform: translateY(-5px);
  text-align: center;
  color: rgb(239, 233, 233);
}

.impact-value {
  font-size: 32px;
  font-weight: 700;
  margin-bottom: 8px;
}

.impact-label {
  font-size: 13px;
  opacity: 0.95;
}

.contact-info {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.contact-item {
  display: flex;
  align-items: start;
  gap: 12px;
  padding: 12px;
  background: #f8f9fa;
  border-radius: 8px;
}

.contact-label {
  font-size: 12px;
  color: #999;
  margin-bottom: 4px;
}

.contact-value {
  font-size: 14px;
  color: #333;
  font-weight: 500;
}

.wallet-container {
  display: flex;
  align-items: center;
  background: #f8f9fa;
  padding: 12px 16px;
  border-radius: 8px;
  border: 1px solid #e0e0e0;
}

.wallet-address {
  flex: 1;
  font-family: 'Courier New', monospace;
  font-size: 14px;
  color: #333;
  word-break: break-all;
}
</style>
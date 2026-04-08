# CrypToCare Frontend-Backend Connection Guide

Complete guide for connecting your Quasar/Vue frontend with Django REST Framework backend for your Bitcoin Cash donation platform.

**Last Updated:** March 16, 2026

---

## ⚡ Essential Backend Requirements (Start Here!)

### What You MUST Implement for Core Functionality

#### 🎯 Phase 1: Minimum Viable Backend (2-3 hours)

**1. Nonprofit Model & API** ⭐ **CRITICAL - DO THIS FIRST**
- Your frontend dropdown needs real nonprofit data
- Without this, users can't select who to donate to
- **Files to create:**
  - `backend/nonprofits/models.py` - Nonprofit model
  - `backend/nonprofits/serializers.py` - API serializer
  - `backend/nonprofits/views.py` - API endpoints
  - `backend/nonprofits/urls.py` - URL routing
- **API endpoint needed:** `GET /api/nonprofits/` (returns list of verified nonprofits)

**2. Update Donation Model**
- Link donations to nonprofits (ForeignKey relationship)
- Store blockchain transaction details (txid, amount, recipient address)
- **File to update:** `backend/donations/models.py`

**3. Environment Configuration**
- Create `.env` files for security
- Store SECRET_KEY, DEBUG, database config
- **Files to create:** `backend/.env` and `.env` (frontend root)

#### 🔧 Phase 2: Frontend Connection (1-2 hours)

**4. Frontend API Integration**
- Update nonprofit selector to fetch from API
- Add loading states and error handling
- **File to update:** `src/pages/DonatePage.vue` or component with nonprofit dropdown

#### 📊 What This Gives You

✅ Users can select real charities from database  
✅ Donations are saved with proper nonprofit tracking  
✅ Basic CRUD operations work  
✅ Foundation for all future features  

#### ❌ What Can Wait Until Later

- User authentication (Phase 3)
- Recurring donations (Phase 5)
- Advanced analytics
- Email notifications
- Celery/background tasks

---

## Table of Contents
1. [Overview](#overview)
2. [Current Setup Status](#current-setup-status)
3. [Basic Connection Setup](#basic-connection-setup)
4. [Missing Features & Requirements](#missing-features--requirements)
5. [Implementation Priority](#implementation-priority)
6. [Detailed Setup Instructions](#detailed-setup-instructions)
7. [API Endpoints Reference](#api-endpoints-reference)
8. [Troubleshooting](#troubleshooting)

---

## Overview

**CrypToCare** is a blockchain-powered donation platform that enables:
- Cryptocurrency donations (Bitcoin Cash)
- Smart contract-based recurring donations
- Nonprofit organization management
- Transparent transaction tracking
- Donor management and analytics

**Tech Stack:**
- **Frontend:** Vue 3 + Quasar Framework + Pinia
- **Backend:** Django 5.2 + Django REST Framework
- **Blockchain:** Bitcoin Cash (CashScript + mainnet-js)
- **Database:** SQLite (development)

---

## Current Setup Status

### ✅ Already Configured

**Backend:**
- ✅ Django REST Framework installed
- ✅ CORS headers configured for ports 9000, 9001, 8080
- ✅ Donations app with model, serializer, views
- ✅ API endpoints: `/api/donations/`, `/api/stats/`, `/api/health/`
- ✅ WhiteNoise for static files

**Frontend:**
- ✅ Axios configured with base URL `http://localhost:8000/api/`
- ✅ Request/response interceptors for debugging
- ✅ Pinia store for donation management
- ✅ BCH wallet integration utilities
- ✅ CashScript contract composables

### ⚠️ Missing / Not Implemented

**Backend:**
- ❌ Nonprofit model & API
- ❌ User authentication system
- ❌ Recurring donation tracking
- ❌ Smart contract state management
- ❌ Environment variables configuration

**Frontend:**
- ❌ Environment-based configuration
- ❌ Nonprofit API integration
- ❌ User authentication flow
- ❌ Complete blockchain transaction flow
- ❌ Error handling strategy

---

## Basic Connection Setup

### Step 1: Install Dependencies

#### Backend Setup
```powershell
# Navigate to backend folder
cd backend

# Create virtual environment (if not exists)
python -m venv venv

# Activate virtual environment
venv\Scripts\activate

# Install Python dependencies
pip install -r requirements.txt

# Run migrations
python manage.py makemigrations
python manage.py migrate

# Create superuser (optional)
python manage.py createsuperuser
```

#### Frontend Setup
```powershell
# From root directory
pnpm install
# or
npm install
```

### Step 2: Verify Configuration

#### Check Backend CORS Settings
File: `backend/CrypToCare_api/settings.py`

```python
# Should already have:
INSTALLED_APPS = [
    # ...
    'rest_framework',
    'corsheaders',
    'donations',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',  # Before CommonMiddleware
    # ...
]

CORS_ALLOWED_ORIGINS = [
    "http://localhost:9000",
    "http://localhost:9001",
    "http://localhost:8080",
]
```

#### Check Frontend Axios Configuration
File: `src/boot/axios.js`

```javascript
// Should already have:
const api = axios.create({ 
  baseURL: 'http://localhost:8000/api/',
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 10000,
})
```

#### Check Quasar Boot Files
File: `quasar.config.js`

```javascript
// Should include:
boot: ['axios'],
```

### Step 3: Start Development Servers

#### Option A - Separate Terminals

**Terminal 1 - Backend:**
```powershell
cd backend
venv\Scripts\activate
python manage.py runserver
# Runs on http://localhost:8000
```

**Terminal 2 - Frontend:**
```powershell
quasar dev
# or
npm run dev
# Runs on http://localhost:9000
```

#### Option B - Concurrent (if configured)
```powershell
npm run start:all
```

### Step 4: Test Connection

#### Test Backend Health
Open browser: `http://localhost:8000/api/health/`

Expected response:
```json
{
  "status": "healthy",
  "message": "CrypToCare API is running"
}
```

#### Test from Frontend
Open browser console (F12) on `http://localhost:9000` and run:
```javascript
// Your axios interceptors will log the request/response
$api.get('health/')
```

### Step 5: Using API in Vue Components

#### Method 1 - Options API (global instance)
```vue
<script>
export default {
  methods: {
    async fetchDonations() {
      try {
        const response = await this.$api.get('donations/')
        console.log(response.data)
      } catch (error) {
        console.error('API Error:', error)
      }
    }
  }
}
</script>
```

#### Method 2 - Composition API (import)
```vue
<script setup>
import { api } from 'boot/axios'
import { ref } from 'vue'

const donations = ref([])

const fetchDonations = async () => {
  try {
    const response = await api.get('donations/')
    donations.value = response.data
  } catch (error) {
    console.error('API Error:', error)
  }
}
</script>
```

#### Method 3 - Using Pinia Store
```vue
<script setup>
import { useDonationStore } from 'stores/donation-store'

const donationStore = useDonationStore()

const loadDonations = async () => {
  await donationStore.fetchDonations()
}
</script>
```

---

## Missing Features & Requirements

### 1. Blockchain Integration Setup

**What's Missing:**
- Environment-based network configuration (testnet vs mainnet)
- Wallet provider error handling
- Transaction confirmation monitoring
- Gas/fee estimation
- Blockchain explorer integration

**Required Implementation:**
```javascript
// .env file needed
VITE_BCH_NETWORK=chipnet        # or mainnet
VITE_EXPLORER_URL=https://chipnet.chaingraph.cash
VITE_MIN_DONATION=0.0001        # BCH
```

**Files to Update:**
- `src/composables/useBCHContract.js` - add environment config
- `src/utils/bchUtils.js` - connect to .env variables

---

### 2. Nonprofit Management System

**What's Missing:**
- Nonprofit model in backend
- API endpoints for nonprofits
- Frontend nonprofit selector connected to API
- Nonprofit verification system

**Backend Implementation Needed:**

File: `backend/nonprofits/models.py`
```python
from django.db import models

class Nonprofit(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    bch_address = models.CharField(max_length=255, unique=True)
    website = models.URLField(blank=True)
    verified = models.BooleanField(default=False)
    category = models.CharField(max_length=100)
    logo_url = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name
```

**API Endpoints Needed:**
- `GET /api/nonprofits/` - List all verified nonprofits
- `POST /api/nonprofits/` - Create nonprofit (admin)
- `GET /api/nonprofits/{id}/` - Get nonprofit details
- `GET /api/nonprofits/{id}/donations/` - Get nonprofit's donations

---

### 3. User Authentication System

**What's Missing:**
- User model extension
- JWT token authentication
- Login/Register endpoints
- Protected routes
- User donation history

**Backend Implementation Needed:**

Install JWT:
```bash
pip install djangorestframework-simplejwt
```

Configure in `settings.py`:
```python
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
}
```

**API Endpoints Needed:**
- `POST /api/auth/register/` - User registration
- `POST /api/auth/login/` - Get JWT tokens
- `POST /api/auth/refresh/` - Refresh access token
- `GET /api/auth/profile/` - Get user profile
- `GET /api/auth/donations/` - User's donation history

**Frontend Updates Needed:**
- Store JWT in localStorage
- Add Authorization header to axios
- Login/Register pages
- Protected route guards

---

### 4. Recurring Donations & Smart Contracts

**What's Missing:**
- Contract model to track smart contracts
- Scheduled task system (Celery)
- Contract state monitoring
- Payment execution logic

**Backend Implementation Needed:**

File: `backend/donations/models.py` (addition)
```python
class RecurringDonation(models.Model):
    INTERVAL_CHOICES = [
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
        ('yearly', 'Yearly'),
    ]
    
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('paused', 'Paused'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    nonprofit = models.ForeignKey('nonprofits.Nonprofit', on_delete=models.CASCADE)
    donor = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=16, decimal_places=8)
    interval = models.CharField(max_length=20, choices=INTERVAL_CHOICES)
    contract_address = models.CharField(max_length=255)
    contract_duration = models.IntegerField(help_text="Duration in months")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    next_payment_date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
```

**Celery Setup Required:**
```bash
pip install celery redis
```

**Tasks Needed:**
- Execute scheduled donations
- Monitor contract balance
- Send payment notifications
- Handle payment failures

---

### 5. Environment Configuration

**Frontend `.env` File:**

Create: `.env`
```bash
# API Configuration
VITE_API_BASE_URL=http://localhost:8000/api/

# Blockchain Configuration
VITE_BCH_NETWORK=chipnet
VITE_EXPLORER_URL=https://chipnet.chaingraph.cash
VITE_MIN_DONATION=0.0001
VITE_MAX_DONATION=1000

# App Configuration
VITE_APP_MODE=development
VITE_APP_NAME=CrypToCare
```

**Backend `.env` File:**

Create: `backend/.env`
```bash
# Django Configuration
SECRET_KEY=your-super-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database
DATABASE_URL=sqlite:///db.sqlite3

# CORS
CORS_ALLOWED_ORIGINS=http://localhost:9000,http://localhost:9001

# Blockchain
BCH_NETWORK=chipnet
MIN_CONFIRMATION=1
```

**Install python-decouple** (already in requirements.txt):
```python
# In settings.py
from decouple import config

SECRET_KEY = config('SECRET_KEY')
DEBUG = config('DEBUG', default=False, cast=bool)
```

---

### 6. Complete Donation Flow

**Current Flow (Incomplete):**
1. User fills form ✅
2. ❌ BCH wallet connection
3. ❌ Transaction signing
4. ✅ Save to backend
5. ✅ Update Pinia store

**Complete Flow Should Be:**

```
┌─────────────────────────────────────────────────────────────┐
│ 1. User fills donation form                                 │
│    - Select nonprofit                                       │
│    - Enter amount                                           │
│    - Choose interval (one-time or recurring)                │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│ 2. Frontend validation                                      │
│    - Validate BCH address                                   │
│    - Validate amount (min/max)                              │
│    - Check form completeness                                │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│ 3. Connect BCH wallet                                       │
│    - Request wallet connection                              │
│    - Get wallet address                                     │
│    - Check balance                                          │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│ 4. Deploy smart contract (if recurring)                     │
│    - Create Mecenas contract                                │
│    - Set recipient address                                  │
│    - Set amount and interval                                │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│ 5. Sign & broadcast transaction                             │
│    - Create transaction                                     │
│    - User signs with wallet                                 │
│    - Broadcast to BCH network                               │
│    - Wait for confirmation                                  │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│ 6. Get transaction details                                  │
│    - Extract txid                                           │
│    - Generate explorer URL                                  │
│    - Get transaction timestamp                              │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│ 7. Save to backend database                                 │
│    - POST /api/donations/                                   │
│    - Include txid, amount, nonprofit, etc.                  │
│    - Handle API errors (fallback to local storage)          │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│ 8. Update Pinia store                                       │
│    - Add donation to history                                │
│    - Update total donated                                   │
│    - Trigger UI updates                                     │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│ 9. Show confirmation                                        │
│    - Display success message                                │
│    - Show transaction ID                                    │
│    - Provide explorer link                                  │
│    - Show receipt/download option                           │
└─────────────────────────────────────────────────────────────┘
```

---

### 7. Form Validation & Error Handling

**Validation Needed:**

Frontend validation:
```javascript
// Amount validation
const validateAmount = (amount) => {
  const minDonation = parseFloat(import.meta.env.VITE_MIN_DONATION)
  const maxDonation = parseFloat(import.meta.env.VITE_MAX_DONATION)
  
  if (amount < minDonation) {
    return `Minimum donation is ${minDonation} BCH`
  }
  if (amount > maxDonation) {
    return `Maximum donation is ${maxDonation} BCH`
  }
  return null
}

// BCH address validation (already exists in bchUtils.js)
import { isValidBCHAddress } from 'utils/bchUtils'
```

**Error Handling Strategy:**

```javascript
// In donation submission
try {
  // 1. Validate form
  const validationError = validateDonationForm(form)
  if (validationError) throw new Error(validationError)
  
  // 2. Connect wallet
  const wallet = await connectWallet()
  
  // 3. Create transaction
  const tx = await createTransaction(form)
  
  // 4. Save to backend
  const donation = await saveDonation(tx)
  
  // 5. Update UI
  showSuccess(donation)
  
} catch (error) {
  if (error.code === 'WALLET_REJECTED') {
    showError('Transaction cancelled by user')
  } else if (error.code === 'INSUFFICIENT_FUNDS') {
    showError('Insufficient balance in wallet')
  } else if (error.response?.status === 500) {
    showError('Server error. Donation saved locally.')
  } else {
    showError('Transaction failed: ' + error.message)
  }
}
```

---

### 8. Data Persistence Strategy

**Current Issue:**
- Frontend saves to local storage on API failure
- No sync mechanism when backend comes back online
- No offline-first strategy

**Recommended Strategy:**

```javascript
// In Pinia store
const syncWithBackend = async () => {
  // Get locally saved donations
  const localDonations = getLocalDonations()
  const unsynced = localDonations.filter(d => !d.synced)
  
  for (const donation of unsynced) {
    try {
      await api.post('donations/', donation)
      markAsSynced(donation.id)
    } catch (error) {
      console.error('Sync failed for donation:', donation.id)
    }
  }
}

// Call on app mount
onMounted(() => {
  syncWithBackend()
})
```

---

## Implementation Priority

### Phase 1: Core Backend Setup (Do First!) 🔥

**Tasks:**
1. ✅ Create `.env` files for backend and frontend
2. ✅ Create Nonprofit model and migrations
3. ✅ Create Nonprofit API endpoints (CRUD)
4. ✅ Seed initial nonprofits data
5. ✅ Test nonprofit API endpoints

**Why First:**
Your frontend dropdown needs real nonprofit data from the API.

**Estimated Time:** 1-2 hours

---

### Phase 2: Frontend Integration ⚡

**Tasks:**
6. ✅ Update nonprofit selector to fetch from API
7. ✅ Add environment variable support
8. ✅ Implement form validation
9. ✅ Add loading states
10. ✅ Improve error handling

**Why Second:**
Connect your existing UI to the real backend data.

**Estimated Time:** 2-3 hours

---

### Phase 3: User Authentication 🔐

**Tasks:**
11. ✅ Install and configure JWT
12. ✅ Create User model extension
13. ✅ Create auth endpoints (login/register)
14. ✅ Frontend login/register pages
15. ✅ Store JWT tokens
16. ✅ Add auth guards to routes
17. ✅ Link donations to users

**Why Third:**
Track who's making donations and build user profiles.

**Estimated Time:** 3-4 hours

---

### Phase 4: Complete Blockchain Integration 🔗

**Tasks:**
18. ✅ Configure BCH network from environment
19. ✅ Implement wallet connection flow
20. ✅ Add transaction signing
21. ✅ Handle transaction confirmation
22. ✅ Generate explorer URLs
23. ✅ Save txid to backend

**Why Fourth:**
Make actual blockchain transactions work end-to-end.

**Estimated Time:** 4-5 hours

---

### Phase 5: Recurring Donations 🔄

**Tasks:**
24. ✅ Create RecurringDonation model
25. ✅ Implement smart contract deployment
26. ✅ Set up Celery for scheduled tasks
27. ✅ Create payment execution task
28. ✅ Add contract monitoring
29. ✅ Build recurring donation UI

**Why Fifth:**
Advanced feature that depends on everything else.

**Estimated Time:** 6-8 hours

---

### Phase 6: Polish & Production 🚀

**Tasks:**
30. ✅ Add analytics dashboard
31. ✅ Implement donation receipts
32. ✅ Add email notifications
33. ✅ Set up logging
34. ✅ Add error tracking (Sentry)
35. ✅ Performance optimization
36. ✅ Security audit
37. ✅ Deploy to production

**Estimated Time:** 8-10 hours

---

## Detailed Setup Instructions

### Setting Up Nonprofits Backend

#### 1. Create Nonprofit Model

File: `backend/nonprofits/models.py`
```python
from django.db import models

class Nonprofit(models.Model):
    CATEGORY_CHOICES = [
        ('education', 'Education'),
        ('health', 'Health & Medical'),
        ('environment', 'Environment'),
        ('poverty', 'Poverty & Housing'),
        ('animals', 'Animal Welfare'),
        ('arts', 'Arts & Culture'),
        ('human_rights', 'Human Rights'),
        ('disaster', 'Disaster Relief'),
        ('other', 'Other'),
    ]
    
    name = models.CharField(max_length=255)
    description = models.TextField()
    bch_address = models.CharField(max_length=255, unique=True, db_index=True)
    website = models.URLField(blank=True)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=50, blank=True)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    logo_url = models.URLField(blank=True)
    verified = models.BooleanField(default=False)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Statistics (optional, can be computed)
    total_donations_received = models.DecimalField(
        max_digits=16, 
        decimal_places=8, 
        default=0
    )
    donation_count = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['-verified', 'name']
        verbose_name = 'Nonprofit Organization'
        verbose_name_plural = 'Nonprofit Organizations'
    
    def __str__(self):
        return self.name
    
    def update_donation_stats(self):
        """Update donation statistics"""
        from donations.models import Donation
        donations = Donation.objects.filter(nonprofit=self)
        self.donation_count = donations.count()
        self.total_donations_received = donations.aggregate(
            total=models.Sum('amount')
        )['total'] or 0
        self.save()
```

#### 2. Create Nonprofit Serializer

File: `backend/nonprofits/serializers.py`
```python
from rest_framework import serializers
from .models import Nonprofit

class NonprofitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Nonprofit
        fields = [
            'id', 'name', 'description', 'bch_address', 
            'website', 'email', 'category', 'logo_url',
            'verified', 'active', 'total_donations_received',
            'donation_count', 'created_at'
        ]
        read_only_fields = ['total_donations_received', 'donation_count']

class NonprofitListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for list views"""
    class Meta:
        model = Nonprofit
        fields = ['id', 'name', 'bch_address', 'category', 'verified']
```

#### 3. Create Nonprofit Views

File: `backend/nonprofits/views.py`
```python
from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Nonprofit
from .serializers import NonprofitSerializer, NonprofitListSerializer

class NonprofitViewSet(viewsets.ModelViewSet):
    queryset = Nonprofit.objects.filter(active=True)
    serializer_class = NonprofitSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'verified']
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'created_at', 'total_donations_received']
    
    def get_serializer_class(self):
        if self.action == 'list':
            return NonprofitListSerializer
        return NonprofitSerializer
    
    @action(detail=False, methods=['get'])
    def verified(self, request):
        """Get only verified nonprofits"""
        nonprofits = self.queryset.filter(verified=True)
        serializer = self.get_serializer(nonprofits, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def donations(self, request, pk=None):
        """Get donations for this nonprofit"""
        nonprofit = self.get_object()
        from donations.models import Donation
        from donations.serializers import DonationSerializer
        
        donations = Donation.objects.filter(nonprofit=nonprofit)
        serializer = DonationSerializer(donations, many=True)
        return Response(serializer.data)
```

#### 4. Create Nonprofit URLs

File: `backend/nonprofits/urls.py`
```python
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import NonprofitViewSet

router = DefaultRouter()
router.register(r'nonprofits', NonprofitViewSet, basename='nonprofit')

urlpatterns = [
    path('', include(router.urls)),
]
```

#### 5. Update Main URLs

File: `backend/CrypToCare_api/urls.py`
```python
from django.contrib import admin
from django.urls import path, include
from .views import api_root

urlpatterns = [
    path('', api_root, name='api-root'),
    path('admin/', admin.site.urls),
    path('api/', include('donations.urls')),
    path('api/', include('nonprofits.urls')),  # Add this
]
```

#### 6. Update Donation Model

File: `backend/donations/models.py`
```python
from django.db import models

class Donation(models.Model):
    txid = models.CharField(max_length=255, unique=True, db_index=True)
    nonprofit = models.ForeignKey(
        'nonprofits.Nonprofit',
        on_delete=models.CASCADE,
        related_name='donations',
        null=True  # Temporary, for migration
    )
    recipient = models.CharField(max_length=255)  # BCH address
    amount = models.DecimalField(max_digits=16, decimal_places=8)
    coin = models.CharField(max_length=20, default='BCH')
    cause = models.CharField(max_length=255)  # Deprecated, use nonprofit
    message = models.TextField(blank=True)
    donor_name = models.CharField(max_length=255, blank=True)
    donor_email = models.EmailField(blank=True)
    donor_contact = models.CharField(max_length=50, blank=True)
    explorer_url = models.URLField()
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-timestamp']
        verbose_name = 'Donation'
        verbose_name_plural = 'Donations'
    
    def __str__(self):
        return f"{self.donor_name or 'Anonymous'} - {self.amount} {self.coin}"
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Update nonprofit stats
        if self.nonprofit:
            self.nonprofit.update_donation_stats()
```

#### 7. Run Migrations
```bash
python manage.py makemigrations nonprofits
python manage.py makemigrations donations
python manage.py migrate
```

#### 8. Register in Admin

File: `backend/nonprofits/admin.py`
```python
from django.contrib import admin
from .models import Nonprofit

@admin.register(Nonprofit)
class NonprofitAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'verified', 'active', 'donation_count', 'created_at']
    list_filter = ['category', 'verified', 'active']
    search_fields = ['name', 'description', 'bch_address']
    ordering = ['-verified', 'name']
```

#### 9. Create Sample Data

File: `backend/seed_nonprofits.py`
```python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'CrypToCare_api.settings')
django.setup()

from nonprofits.models import Nonprofit

nonprofits_data = [
    {
        'name': 'Red Cross',
        'description': 'International humanitarian organization providing emergency assistance',
        'bch_address': 'bitcoincash:qp3wjpa3tjlj042z2wv7hahsldgwhwy0rq9sywjpyy',
        'website': 'https://www.redcross.org',
        'category': 'disaster',
        'verified': True,
    },
    {
        'name': 'UNICEF',
        'description': 'United Nations Children\'s Fund working for children\'s rights',
        'bch_address': 'bitcoincash:qqfx3wcg8ts09mt5l3zey06wenapyfqq2qrcyj5x0s',
        'website': 'https://www.unicef.org',
        'category': 'human_rights',
        'verified': True,
    },
    {
        'name': 'World Wildlife Fund',
        'description': 'Conservation organization working to preserve nature',
        'bch_address': 'bitcoincash:qr5agtachyxvrwxu76vzszan5pnvuzy8duhv4lxry',
        'website': 'https://www.worldwildlife.org',
        'category': 'environment',
        'verified': True,
    },
    {
        'name': 'Doctors Without Borders',
        'description': 'Medical humanitarian organization',
        'bch_address': 'bitcoincash:qzp42c8gpklf7h4rgw0cxj69mqt3hnlufq35yl6gn5',
        'website': 'https://www.doctorswithoutborders.org',
        'category': 'health',
        'verified': True,
    },
]

for data in nonprofits_data:
    nonprofit, created = Nonprofit.objects.get_or_create(
        name=data['name'],
        defaults=data
    )
    if created:
        print(f'Created: {nonprofit.name}')
    else:
        print(f'Already exists: {nonprofit.name}')

print('Seeding complete!')
```

Run:
```bash
python seed_nonprofits.py
```

---

## API Endpoints Reference

### Current Endpoints

#### Health Check
```
GET /api/health/
```
Response:
```json
{
  "status": "healthy",
  "message": "CrypToCare API is running"
}
```

#### List Donations
```
GET /api/donations/
GET /api/donations/?limit=10
```
Response:
```json
[
  {
    "id": 1,
    "txid": "abc123...",
    "recipient": "bitcoincash:qp3w...",
    "amount": "0.05000000",
    "coin": "BCH",
    "cause": "Education",
    "donor_name": "John Doe",
    "timestamp": "2026-03-15T10:30:00Z",
    "explorer_url": "https://..."
  }
]
```

#### Create Donation
```
POST /api/donations/
Content-Type: application/json

{
  "txid": "unique-transaction-id",
  "recipient": "bitcoincash:qp3wjpa3tjlj042z2wv7hahsldgwhwy0rq9sywjpyy",
  "amount": "0.05",
  "coin": "BCH",
  "cause": "Education",
  "message": "For school supplies",
  "donor_name": "John Doe",
  "donor_email": "john@example.com",
  "explorer_url": "https://explorer.com/tx/..."
}
```

#### Get Donation Stats
```
GET /api/stats/
```
Response:
```json
{
  "total_donations": 150,
  "total_amount": 7.5,
  "total_by_cause": {
    "Education": {"amount": 3.5, "count": 75},
    "Health": {"amount": 4.0, "count": 75}
  },
  "total_by_coin": {
    "BCH": {"amount": 7.5, "count": 150}
  }
}
```

#### Recent Donations
```
GET /api/donations/recent/?limit=10
```

#### Donations by Cause
```
GET /api/donations/by_cause/?cause=Education
```

### New Endpoints (After Implementation)

#### List Nonprofits
```
GET /api/nonprofits/
GET /api/nonprofits/?verified=true
GET /api/nonprofits/?category=education
GET /api/nonprofits/?search=red+cross
```

#### Get Nonprofit Details
```
GET /api/nonprofits/{id}/
```

#### Get Nonprofit Donations
```
GET /api/nonprofits/{id}/donations/
```

---

## Troubleshooting

### Common Issues

#### 1. CORS Errors
**Problem:** Frontend can't connect to backend, CORS errors in console

**Solutions:**
```python
# Check backend/CrypToCare_api/settings.py
CORS_ALLOWED_ORIGINS = [
    "http://localhost:9000",  # Add your frontend port
]

# Or allow all (development only!)
CORS_ALLOW_ALL_ORIGINS = True
```

#### 2. Connection Refused
**Problem:** ERR_CONNECTION_REFUSED

**Solutions:**
- Ensure backend is running: `python manage.py runserver`
- Check backend is on port 8000: `http://localhost:8000/api/health/`
- Check firewall settings

#### 3. 404 Not Found
**Problem:** API endpoint returns 404

**Solutions:**
- Verify URL pattern in `urls.py`
- Check router registration
- Test endpoint directly in browser
- Check axios baseURL includes `/api/`

#### 4. Network Timeout
**Problem:** Requests timeout after 10 seconds

**Solutions:**
```javascript
// Increase timeout in src/boot/axios.js
const api = axios.create({ 
  baseURL: 'http://localhost:8000/api/',
  timeout: 30000,  // 30 seconds
})
```

#### 5. Data Not Showing
**Problem:** API works but data doesn't appear in UI

**Debug Steps:**
1. Check browser console for errors
2. Check Network tab for API response
3. Verify data structure matches frontend expectations
4. Check Vue DevTools for reactive state
5. Verify component is awaiting async calls

#### 6. Blockchain Wallet Won't Connect
**Problem:** Wallet connection fails

**Solutions:**
- Check if using test mode: `isTestMode = true`
- Install BCH wallet extension
- Check network (testnet vs mainnet)
- Verify wallet is unlocked

#### 7. Migrations Fail
**Problem:** `python manage.py migrate` errors

**Solutions:**
```bash
# Reset migrations (development only!)
python manage.py migrate nonprofits zero
python manage.py migrate donations zero
rm -rf nonprofits/migrations/0*.py
rm -rf donations/migrations/0*.py

# Recreate
python manage.py makemigrations
python manage.py migrate
```

---

## Development Workflow

### Making Changes

#### Backend Changes
```bash
# 1. Modify models
# 2. Create migrations
python manage.py makemigrations

# 3. Apply migrations
python manage.py migrate

# 4. Test in Django shell
python manage.py shell
>>> from nonprofits.models import Nonprofit
>>> Nonprofit.objects.all()

# 5. Test API with curl or Postman
curl http://localhost:8000/api/nonprofits/
```

#### Frontend Changes
```bash
# 1. Modify components/pages
# 2. Hot reload happens automatically
# 3. Check browser console for errors
# 4. Test in browser
```

### Testing Tips

#### Test Backend API with Browser
```
http://localhost:8000/api/health/
http://localhost:8000/api/donations/
http://localhost:8000/api/nonprofits/
```

#### Test with curl
```bash
# GET request
curl http://localhost:8000/api/nonprofits/

# POST request
curl -X POST http://localhost:8000/api/donations/ \
  -H "Content-Type: application/json" \
  -d '{"txid":"test123","recipient":"bitcoincash:qp3w...","amount":"0.01",...}'
```

#### Test Frontend API Calls
```javascript
// In browser console on http://localhost:9000
$api.get('nonprofits/').then(console.log)
```

---

## 📋 Quick Reference: Essential Backend Files

### Files You MUST Create for Core Functionality

```
backend/
├── .env                           # ⭐ Environment variables (SECRET_KEY, DEBUG)
├── nonprofits/
│   ├── __init__.py
│   ├── models.py                  # ⭐ Nonprofit model (name, address, category)
│   ├── serializers.py             # ⭐ API data serialization
│   ├── views.py                   # ⭐ API viewsets (list, detail)
│   ├── urls.py                    # ⭐ URL routing
│   ├── admin.py                   # Admin panel registration
│   └── migrations/                # Database migrations (auto-generated)
└── donations/
    └── models.py                  # ⭐ UPDATE: Add nonprofit ForeignKey
```

### Frontend Files to Update

```
frontend/
├── .env                           # ⭐ API URL, BCH network config
└── src/
    ├── pages/
    │   └── DonatePage.vue         # ⭐ UPDATE: Fetch nonprofits from API
    └── stores/
        └── donation-store.js      # ⭐ UPDATE: Handle API calls
```

### Essential API Endpoints to Implement

| Method | Endpoint | Purpose | Priority |
|--------|----------|---------|----------|
| `GET` | `/api/nonprofits/` | List all verified nonprofits | ⭐ Critical |
| `GET` | `/api/nonprofits/{id}/` | Get nonprofit details | ⭐ Critical |
| `POST` | `/api/donations/` | Create new donation | ⭐ Critical |
| `GET` | `/api/donations/` | List all donations | Important |
| `GET` | `/api/stats/` | Get donation statistics | Nice to have |

### Database Schema (Minimum Required)

**Nonprofit Table:**
```
- id (auto)
- name (string, required)
- description (text)
- bch_address (string, unique, required)
- category (string, choices)
- verified (boolean, default=False)
- active (boolean, default=True)
```

**Donation Table:**
```
- id (auto)
- nonprofit_id (ForeignKey to Nonprofit) ⭐ ADD THIS
- txid (string, unique, required)
- recipient (string, BCH address)
- amount (decimal)
- donor_name (string, optional)
- donor_email (string, optional)
- timestamp (datetime, auto)
```

---

## Next Steps

### Ready to Implement?

Choose a phase to start:

1. **"Implement Phase 1"** - Set up nonprofits backend ⭐ **Start here!**
2. **"Implement Phase 2"** - Connect frontend to nonprofits API
3. **"Implement Phase 3"** - Add user authentication
4. **"Implement Phase 4"** - Complete blockchain integration
5. **"Implement Phase 5"** - Add recurring donations
6. **"Implement everything"** - Full systematic implementation

---

## Resources

### Documentation
- [Django REST Framework](https://www.django-rest-framework.org/)
- [Quasar Framework](https://quasar.dev/)
- [CashScript](https://cashscript.org/)
- [Bitcoin Cash](https://www.bitcoincash.org/)

### Tools
- [Postman](https://www.postman.com/) - API testing
- [Vue DevTools](https://devtools.vuejs.org/) - Vue debugging
- [BCH Explorer](https://chipnet.chaingraph.cash/) - Testnet explorer

---

**Last Updated:** March 15, 2026  
**Version:** 1.0  
**Author:** CrypToCare Development Team

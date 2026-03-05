# BiToHelp - Cryptocurrency Donation Platform

A blockchain-powered donation platform built with Quasar (Vue 3) and Django REST Framework. Enables transparent cryptocurrency donations to verified nonprofits using Bitcoin Cash (BCH) and CashScript smart contracts.

## 🏗️ Project Structure

```
bitohelp/
├── backend/                    # Django REST API
│   ├── bitohelp_api/          # Django project settings
│   ├── donations/             # Donations app (models, views, API)
│   ├── manage.py              # Django management
│   └── requirements.txt       # Python dependencies
├── src/                       # Quasar/Vue frontend
│   ├── components/           
│   ├── composables/           # useBCHContract.js (CashScript integration)
│   ├── contracts/             # DonationContract.cash (Smart contract)
│   ├── pages/                 # DonatePage, UserPage, etc.
│   ├── stores/                # Pinia stores (donation-store.js)
│   ├── utils/                 # bchUtils.js (BCH helpers)
│   └── boot/                  # axios.js (API configuration)
├── start-dev.ps1              # PowerShell: Start both servers
├── start-dev.bat              # Batch: Start both servers
└── package.json               # Node dependencies
```

## 🚀 Quick Start

### Option 1: Run Both Servers Automatically

**PowerShell:**
```powershell
.\start-dev.ps1
```

**Command Prompt:**
```cmd
start-dev.bat
```

### Option 2: Run Manually

**Terminal 1 - Backend (Django):**
```bash
cd backend
.\venv\Scripts\Activate.ps1  # Windows PowerShell
python manage.py runserver
```

**Terminal 2 - Frontend (Quasar):**
```bash
pnpm dev
# or
npm run dev
```

## 📦 Installation

### Frontend Dependencies
```bash
pnpm install
# or
npm install
```

### Backend Setup
```bash
cd backend
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser  # Optional: for admin panel
```

## 🌐 Access Points

- **Frontend**: http://localhost:9000
- **Backend API**: http://localhost:8000/api/
- **Django Admin**: http://localhost:8000/admin/
- **API Docs**: http://localhost:8000/

## 🔑 Key Features

- ✅ **CashScript Integration**: Smart contract-based donations
- ✅ **BCH Wallet Support**: Bitcoin.com wallet + TestNetWallet
- ✅ **Test Mode**: Development without spending real BCH
- ✅ **Django REST API**: Persistent donation tracking
- ✅ **Real-time Updates**: Vue 3 Composition API + Pinia
- ✅ **Blockchain Explorer**: Direct transaction links

## 📚 Documentation

- [CashScript Integration Guide](BCH_INTEGRATION_GUIDE.md)
- [Test Mode Guide](TEST_MODE_GUIDE.md)
- [Backend API Documentation](backend/README.md)

## 🛠️ Development

### Frontend Commands
```bash
pnpm dev          # Start dev server
pnpm build        # Build for production
pnpm lint         # Lint files
pnpm format       # Format with Prettier
```

### Backend Commands
```bash
cd backend
python manage.py runserver           # Start server
python manage.py makemigrations      # Create migrations
python manage.py migrate              # Apply migrations
python manage.py createsuperuser     # Create admin user
```

## 🔧 Tech Stack

### Frontend
- **Framework**: Quasar v2 + Vue 3
- **State**: Pinia
- **Blockchain**: CashScript + mainnet-js
- **HTTP**: Axios

### Backend
- **Framework**: Django 5.2
- **API**: Django REST Framework
- **Database**: SQLite (dev) / PostgreSQL (production)
- **CORS**: django-cors-headers

## 📝 API Endpoints

- `GET  /api/donations/` - List all donations
- `POST /api/donations/` - Create donation
- `GET  /api/donations/{id}/` - Get donation details
- `GET  /api/stats/` - Donation statistics
- `GET  /api/health/` - Health check

## 🎯 Environment

**Test Mode** is enabled by default in `src/composables/useBCHContract.js`:
```javascript
const isTestMode = ref(true)  // Set to false for real transactions
const isTestnet = ref(true)   // chipnet vs mainnet
```

## 📄 License

MIT License

## 👥 Contributors

Built with ❤️ for transparent charitable giving

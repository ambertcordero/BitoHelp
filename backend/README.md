# BiToHelp Backend (Django API)

Django REST API backend for BiToHelp cryptocurrency donation platform.

## Setup

### 1. Create Virtual Environment (if not exists)
```bash
cd backend
python -m venv venv
```

### 2. Activate Virtual Environment

**Windows PowerShell:**
```powershell
.\venv\Scripts\Activate.ps1
```

**Windows CMD:**
```cmd
.\venv\Scripts\activate.bat
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run Migrations
```bash
python manage.py migrate
```

### 5. Create Superuser (Optional)
```bash
python manage.py createsuperuser
```

### 6. Run Development Server
```bash
python manage.py runserver
```

The API will be available at: `http://localhost:8000/`

## API Endpoints

- **Root**: `http://localhost:8000/` - API info
- **Donations List**: `http://localhost:8000/api/donations/` - GET all, POST new
- **Donation Detail**: `http://localhost:8000/api/donations/{id}/` - GET, PUT, DELETE
- **Stats**: `http://localhost:8000/api/stats/` - GET donation statistics
- **Health**: `http://localhost:8000/api/health/` - Health check
- **Admin Panel**: `http://localhost:8000/admin/` - Django admin (requires superuser)

## Project Structure

```
backend/
├── bitohelp_api/       # Main Django project
│   ├── settings.py     # Django settings (CORS, REST framework)
│   ├── urls.py         # Main URL configuration
│   └── views.py        # Root endpoint view
├── donations/          # Donations app
│   ├── models.py       # Donation model
│   ├── serializers.py  # DRF serializers
│   ├── views.py        # API views
│   ├── urls.py         # App URLs
│   └── admin.py        # Admin configuration
├── manage.py           # Django management script
└── requirements.txt    # Python dependencies
```

## Development

### View API in Browser
Visit `http://localhost:8000/api/donations/` with Django REST Framework's browsable API.

### Make Migrations After Model Changes
```bash
python manage.py makemigrations
python manage.py migrate
```

### Access Admin Panel
1. Create superuser: `python manage.py createsuperuser`
2. Visit: `http://localhost:8000/admin/`

## Frontend Integration

The frontend (Quasar app) connects to this backend via Axios at `http://localhost:8000/api/`.

Make sure both servers are running:
- **Backend**: `http://localhost:8000`
- **Frontend**: `http://localhost:9000`

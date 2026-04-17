# CrypToCare Production Deployment

This folder contains the production deployment configuration for CrypToCare.

## Prerequisites

### 1. Python Fabric

Fabric is used for automated deployment to the remote server. Install it:

```bash
pip install fabric patchwork python-dotenv
```

Or add to your requirements:

```
fabric>=3.0.0
patchwork>=1.0.0
python-dotenv>=1.0.0
```

## Environment Files

### `.env_fabfile` - Deployment Configuration

**Purpose:** SSH connection settings for remote server deployment.

**Required variables:**

```
ENV=prod                          # Environment name
SERVER_HOST=204.168.249.146     # Your server IP or hostname
SERVER_USER=root                 # SSH username
SERVER_SSH_KEY=/path/to/key     # Path to your SSH private key
```

**Security:** Keep this file secure and never commit it to version control.

### `.env_prod` - Production Application Configuration

**Purpose:** Runtime environment variables for all Docker containers (DB, backend, frontend).

**Sections:**

#### PostgreSQL Database

```
POSTGRES_USER=postgres           # Database username
POSTGRES_PASSWORD=badpassword   # Database password (CHANGE THIS!)
POSTGRES_DB=cryptocare          # Database name
```

#### Django Backend

```
DATABASE_URL=postgres://postgres:badpassword@db:5432/cryptocare
ALLOWED_HOSTS=bitohelp.scibiz.dev          # Your domain
CORS_ALLOWED_ORIGINS=https://bitohelp.scibiz.dev
CSRF_TRUSTED_ORIGINS=https://bitohelp.scibiz.dev
OPENAI_API_KEY=acc2c4k2e-3d2...
```

#### Frontend (Vite/Quasar)

```
DOCKER=1                                    # Tells Quasar to bind to 0.0.0.0
VITE_API_URL=https://bitohelp.scibiz.dev/api/  # API URL for frontend
```

## Deployment Commands

All commands are run from this directory:

```bash
cd deployment/
```

### Available Fabric Commands

```bash
# Full deployment (sync, build, restart)
fab deploy

# Individual commands:
fab sync      # Sync project files to remote server via rsync
fab build     # Build Docker images on remote server
fab up        # Start containers on remote server
fab down      # Stop containers on remote server
fab nginx     # Update Nginx configuration on remote server
fab streamlogs --tail=100  # Stream container logs
```

### Docker Compose Commands (on remote server)

```bash
# Start all services
docker compose -f prod.yml up -d

# View logs
docker compose -f prod.yml logs -f

# View specific service logs
docker compose -f prod.yml logs -f backend

# Restart a service
docker compose -f prod.yml restart backend

# Stop all services
docker compose -f prod.yml down
```

## Architecture

```
┌─────────────┐
│   Nginx     │ ← /etc/nginx/sites-enabled/cryptocare
│  (reverse   │   (Listens on 80, proxies to containers)
│   proxy)    │
└──────┬──────┘
       │
       ├──→ Frontend (Nginx container) :9000
       │      └─ Serves static Quasar build
       │
       └──→ Backend (Gunicorn) :8000
              └─ Django REST API
                     │
                     └──→ PostgreSQL :5432 (internal network only)
```

## Setup Steps

1. **Configure environment files:**

   ```bash
   cp .env_fabfile.example .env_fabfile   # Edit with your server details
   cp .env_prod.example .env_prod         # Edit with your production values
   ```

2. **Update `nginx.conf`:**
   - Change `server_name` to your domain
   - Adjust proxy ports if needed

3. **First deployment:**

   ```bash
   fab deploy
   fab nginx
   ```

4. **Verify deployment:**
   ```bash
   fab streamlogs
   ```

## Security Checklist

- [ ] Change default PostgreSQL password in `.env_prod`
- [ ] Set strong secrets in backend `.env` file
- [ ] Ensure `.env_fabfile` and `.env_prod` are in `.gitignore`
- [ ] Restrict SSH key permissions: `chmod 600 /path/to/key`
- [ ] Enable firewall (ufw) on remote server
- [ ] Set up SSL/TLS with Let's Encrypt
- [ ] Disable password authentication for SSH
- [ ] Regular security updates on server

## Troubleshooting

### Connection refused errors

- Verify SSH key path in `.env_fabfile`
- Check if server is reachable: `ping SERVER_HOST`

### Database connection issues

- Verify `DATABASE_URL` matches `POSTGRES_*` credentials
- Check if db container is healthy: `docker compose -f prod.yml ps`

### Nginx 502 errors

- Verify containers are running: `fab up`
- Check backend logs: `docker compose -f prod.yml logs backend`
- Verify port bindings match `nginx.conf`

## File Structure

```
deployment/
├── fabfile.py          # Fabric deployment scripts
├── prod.yml            # Production Docker Compose
├── nginx.conf          # Nginx reverse proxy config
├── .env_fabfile        # SSH credentials (gitignored)
└── .env_prod           # App configuration (gitignored)
```

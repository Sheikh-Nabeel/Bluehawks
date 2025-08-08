# 🚀 Bluehawks Security Services - Deployment Guide

## 📋 Overview

This guide explains how to deploy your Bluehawks Security Services website with **separate frontend and backend** deployments. This approach provides better scalability, maintenance, and flexibility.

## 🏗️ Architecture Options

### **Option 1: Traditional Django Deployment (Recommended for Start)**
- **Backend**: Django + Gunicorn + Nginx
- **Frontend**: Served by Django (current setup)
- **Database**: PostgreSQL/MySQL
- **Hosting**: VPS (DigitalOcean, AWS, Vultr)

### **Option 2: Modern Separated Deployment**
- **Backend**: Django API + Gunicorn + Nginx
- **Frontend**: React/Vue.js + Nginx/CDN
- **Database**: PostgreSQL/MySQL
- **Hosting**: Separate servers or containers

### **Option 3: Containerized Deployment**
- **Backend**: Docker + Django API
- **Frontend**: Docker + React/Vue.js
- **Database**: Docker + PostgreSQL
- **Orchestration**: Docker Compose/Kubernetes

## 🎯 Recommended Deployment Strategy

For your current Django project, I recommend **Option 1** (Traditional Django) as it's:
- ✅ **Simplest to implement**
- ✅ **Cost-effective**
- ✅ **Perfect for security services websites**
- ✅ **Easy to maintain**

## 📦 Option 1: Traditional Django Deployment

### **Step 1: Prepare Your Project**

```bash
# 1. Create production settings
cd backend
cp bluehawks/settings.py bluehawks/settings_production.py

# 2. Update production settings
# Edit bluehawks/settings_production.py with production values

# 3. Create requirements file
pip freeze > requirements.txt

# 4. Create .env file for production
# SECRET_KEY=your-production-secret-key
# DEBUG=False
# ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
# DATABASE_URL=postgresql://user:password@localhost:5432/dbname
```

### **Step 2: Server Setup**

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install required packages
sudo apt install -y python3 python3-pip python3-venv nginx postgresql postgresql-contrib git

# Create application directory
sudo mkdir -p /var/www/bluehawks
sudo chown $USER:$USER /var/www/bluehawks
```

### **Step 3: Deploy Backend**

```bash
# Clone your project
git clone your-repo-url /var/www/bluehawks
cd /var/www/bluehawks

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r backend/requirements.txt

# Set up environment variables
cp backend/env.example backend/.env
# Edit backend/.env with production values

# Run migrations
cd backend
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Collect static files
python manage.py collectstatic --noinput

# Set permissions
sudo chown -R www-data:www-data /var/www/bluehawks
sudo chmod -R 755 /var/www/bluehawks
```

### **Step 4: Configure Gunicorn**

```bash
# Create Gunicorn service file
sudo tee /etc/systemd/system/bluehawks.service << EOF
[Unit]
Description=Bluehawks Security Services
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/var/www/bluehawks/backend
Environment="PATH=/var/www/bluehawks/venv/bin"
ExecStart=/var/www/bluehawks/venv/bin/gunicorn --config gunicorn.conf.py bluehawks.wsgi:application
ExecReload=/bin/kill -s HUP \$MAINPID
Restart=always

[Install]
WantedBy=multi-user.target
EOF

# Start and enable service
sudo systemctl daemon-reload
sudo systemctl start bluehawks
sudo systemctl enable bluehawks
```

### **Step 5: Configure Nginx**

```bash
# Create Nginx configuration
sudo tee /etc/nginx/sites-available/bluehawks << EOF
server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;

    # Security headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header Referrer-Policy "no-referrer-when-downgrade" always;
    add_header Content-Security-Policy "default-src 'self' http: https: data: blob: 'unsafe-inline'" always;

    # Static files
    location /static/ {
        alias /var/www/bluehawks/backend/staticfiles/;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }

    # Media files (if any)
    location /media/ {
        alias /var/www/bluehawks/backend/media/;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }

    # Main application
    location / {
        proxy_pass http://unix:/run/bluehawks.sock;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }
}
EOF

# Enable site
sudo ln -s /etc/nginx/sites-available/bluehawks /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### **Step 6: SSL Certificate**

```bash
# Install Certbot
sudo apt install certbot python3-certbot-nginx

# Get SSL certificate
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com

# Auto-renewal
sudo crontab -e
# Add: 0 12 * * * /usr/bin/certbot renew --quiet
```

## 🌐 Option 2: Modern Separated Deployment

### **Backend Deployment (Django API)**

```bash
# 1. Convert Django to API
# Install Django REST Framework
pip install djangorestframework django-cors-headers

# 2. Update settings
INSTALLED_APPS = [
    # ... existing apps
    'rest_framework',
    'corsheaders',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',  # Add this
    # ... existing middleware
]

# 3. Configure CORS
CORS_ALLOWED_ORIGINS = [
    "https://your-frontend-domain.com",
    "http://localhost:3000",  # For development
]

# 4. Create API views
# Create serializers.py and api_views.py
```

### **Frontend Deployment (React/Vue.js)**

```bash
# 1. Create React app
npx create-react-app bluehawks-frontend
cd bluehawks-frontend

# 2. Install dependencies
npm install axios react-router-dom

# 3. Build for production
npm run build

# 4. Deploy to CDN or static hosting
# - Netlify
# - Vercel
# - AWS S3 + CloudFront
# - GitHub Pages
```

## 🐳 Option 3: Containerized Deployment

### **Docker Setup**

```dockerfile
# backend/Dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
RUN python manage.py collectstatic --noinput

EXPOSE 8000
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "bluehawks.wsgi:application"]
```

```yaml
# docker-compose.yml
version: '3.8'

services:
  db:
    image: postgres:13
    environment:
      POSTGRES_DB: bluehawks
      POSTGRES_USER: bluehawks
      POSTGRES_PASSWORD: your_password
    volumes:
      - postgres_data:/var/lib/postgresql/data

  backend:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://bluehawks:your_password@db:5432/bluehawks
    depends_on:
      - db

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./ssl:/etc/nginx/ssl
    depends_on:
      - backend

volumes:
  postgres_data:
```

## 🔧 Environment Variables

Create `.env` file in backend directory:

```env
# Django Settings
SECRET_KEY=your-production-secret-key-here
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com

# Database
DATABASE_URL=postgresql://user:password@localhost:5432/bluehawks

# Email (if needed)
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password

# Security
CSRF_TRUSTED_ORIGINS=https://yourdomain.com,https://www.yourdomain.com
```

## 📊 Monitoring & Maintenance

### **Logs**
```bash
# View application logs
sudo journalctl -u bluehawks -f

# View Nginx logs
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log
```

### **Backup**
```bash
# Database backup
pg_dump bluehawks > backup_$(date +%Y%m%d_%H%M%S).sql

# Static files backup
tar -czf static_backup_$(date +%Y%m%d_%H%M%S).tar.gz /var/www/bluehawks/backend/staticfiles/
```

### **Updates**
```bash
# Pull latest code
cd /var/www/bluehawks
git pull origin main

# Update dependencies
source venv/bin/activate
pip install -r backend/requirements.txt

# Run migrations
cd backend
python manage.py migrate

# Collect static files
python manage.py collectstatic --noinput

# Restart services
sudo systemctl restart bluehawks
sudo systemctl restart nginx
```

## 🚀 Quick Deployment Commands

### **For Option 1 (Traditional Django)**

```bash
# 1. Prepare project
cd backend
python manage.py collectstatic --noinput

# 2. Upload to server
scp -r . user@your-server:/var/www/bluehawks/

# 3. On server
cd /var/www/bluehawks/backend
python manage.py migrate
sudo systemctl restart bluehawks
sudo systemctl restart nginx
```

## 📞 Support & Troubleshooting

### **Common Issues**

1. **Static files not loading**
   ```bash
   python manage.py collectstatic --noinput
   sudo chown -R www-data:www-data /var/www/bluehawks/backend/staticfiles/
   ```

2. **Database connection issues**
   ```bash
   sudo systemctl status postgresql
   sudo -u postgres psql -c "CREATE DATABASE bluehawks;"
   ```

3. **Permission issues**
   ```bash
   sudo chown -R www-data:www-data /var/www/bluehawks
   sudo chmod -R 755 /var/www/bluehawks
   ```

### **Performance Optimization**

1. **Enable Gzip compression in Nginx**
2. **Use CDN for static files**
3. **Implement caching (Redis)**
4. **Database optimization**

## 🎯 Recommended Hosting Providers

### **Budget-Friendly**
- **DigitalOcean**: $5-10/month
- **Vultr**: $5-10/month
- **Linode**: $5-10/month

### **Professional**
- **AWS EC2**: Pay-as-you-go
- **Google Cloud**: Pay-as-you-go
- **Azure**: Pay-as-you-go

### **Managed**
- **Heroku**: Easy deployment
- **Railway**: Simple setup
- **Render**: Free tier available

## 📋 Deployment Checklist

- [ ] Environment variables configured
- [ ] Database set up and migrated
- [ ] Static files collected
- [ ] SSL certificate installed
- [ ] Domain DNS configured
- [ ] Monitoring set up
- [ ] Backup strategy implemented
- [ ] Security headers configured
- [ ] Performance optimized
- [ ] Testing completed

---

**Bluehawks Security Services** - Professional deployment guide for your security services website.

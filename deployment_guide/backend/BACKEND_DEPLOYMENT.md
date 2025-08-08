# 🚀 Backend Deployment Guide - Bluehawks Security Services

## 📋 Overview

This guide covers deploying the Django backend for Bluehawks Security Services to production.

## 🏗️ Backend Architecture

- **Framework**: Django 5.2.4
- **Database**: PostgreSQL (recommended) / MySQL
- **Web Server**: Nginx
- **Application Server**: Gunicorn
- **Static Files**: WhiteNoise
- **Environment**: Python 3.11+

## 📦 Prerequisites

### **System Requirements**
- Ubuntu 20.04+ / CentOS 8+ / Debian 11+
- 1GB RAM minimum (2GB recommended)
- 20GB storage
- Python 3.11+

### **Domain & SSL**
- Domain name (e.g., yourdomain.com)
- SSL certificate (Let's Encrypt - free)

## 🔧 Step-by-Step Backend Deployment

### **Step 1: Server Setup**

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install required packages
sudo apt install -y python3 python3-pip python3-venv nginx postgresql postgresql-contrib git curl

# Create application directory
sudo mkdir -p /var/www/bluehawks
sudo chown $USER:$USER /var/www/bluehawks

# Create log directory
sudo mkdir -p /var/log/bluehawks
sudo chown www-data:www-data /var/log/bluehawks
```

### **Step 2: Database Setup**

```bash
# Install PostgreSQL
sudo apt install -y postgresql postgresql-contrib

# Start PostgreSQL service
sudo systemctl start postgresql
sudo systemctl enable postgresql

# Create database and user
sudo -u postgres psql -c "CREATE DATABASE bluehawks;"
sudo -u postgres psql -c "CREATE USER bluehawks WITH PASSWORD 'your-secure-password';"
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE bluehawks TO bluehawks;"
sudo -u postgres psql -c "ALTER USER bluehawks CREATEDB;"
```

### **Step 3: Upload Project**

```bash
# Clone or upload your project
git clone your-repo-url /var/www/bluehawks
# OR upload via SCP/SFTP

cd /var/www/bluehawks
```

### **Step 4: Python Environment**

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r backend/requirements.txt

# Install additional production packages
pip install gunicorn psycopg2-binary redis
```

### **Step 5: Environment Configuration**

```bash
# Copy environment template
cp deployment_guide/backend/env.production.template backend/.env

# Edit environment file
nano backend/.env
```

**Environment Variables to Configure:**
```env
# Django Settings
SECRET_KEY=your-production-secret-key-here
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com

# Database Settings
DB_NAME=bluehawks
DB_USER=bluehawks
DB_PASSWORD=your-secure-database-password
DB_HOST=localhost
DB_PORT=5432

# Security Settings
CSRF_TRUSTED_ORIGINS=https://yourdomain.com,https://www.yourdomain.com

# Email Settings (Optional)
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password

# Redis Settings (Optional - for caching)
REDIS_URL=redis://127.0.0.1:6379/1
```

### **Step 6: Django Configuration**

```bash
# Copy production settings
cp deployment_guide/backend/settings_production.py backend/bluehawks/settings.py

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

### **Step 7: Gunicorn Configuration**

```bash
# Create Gunicorn config
cat > backend/gunicorn.conf.py << EOF
bind = "unix:/run/bluehawks.sock"
workers = 3
worker_class = "sync"
worker_connections = 1000
max_requests = 1000
max_requests_jitter = 50
timeout = 30
keepalive = 2
preload_app = True
EOF

# Create systemd service
sudo tee /etc/systemd/system/bluehawks.service << EOF
[Unit]
Description=Bluehawks Security Services
After=network.target postgresql.service

[Service]
User=www-data
Group=www-data
WorkingDirectory=/var/www/bluehawks/backend
Environment="PATH=/var/www/bluehawks/venv/bin"
Environment="DJANGO_SETTINGS_MODULE=bluehawks.settings"
ExecStart=/var/www/bluehawks/venv/bin/gunicorn --config gunicorn.conf.py bluehawks.wsgi:application
ExecReload=/bin/kill -s HUP \$MAINPID
Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
EOF

# Start and enable service
sudo systemctl daemon-reload
sudo systemctl start bluehawks
sudo systemctl enable bluehawks
```

### **Step 8: Nginx Configuration**

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

    # Gzip compression
    gzip on;
    gzip_vary on;
    gzip_min_length 1024;
    gzip_types text/plain text/css text/xml text/javascript application/javascript application/xml+rss application/json;

    # Static files
    location /static/ {
        alias /var/www/bluehawks/backend/staticfiles/;
        expires 1y;
        add_header Cache-Control "public, immutable";
        access_log off;
    }

    # Media files
    location /media/ {
        alias /var/www/bluehawks/backend/media/;
        expires 1y;
        add_header Cache-Control "public, immutable";
        access_log off;
    }

    # Main application
    location / {
        proxy_pass http://unix:/run/bluehawks.sock;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
        proxy_redirect off;
        proxy_connect_timeout 30s;
        proxy_send_timeout 30s;
        proxy_read_timeout 30s;
    }

    # Admin panel
    location /admin/ {
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
sudo rm -f /etc/nginx/sites-enabled/default

# Test and restart Nginx
sudo nginx -t
sudo systemctl restart nginx
```

### **Step 9: SSL Certificate**

```bash
# Install Certbot
sudo apt install -y certbot python3-certbot-nginx

# Get SSL certificate
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com

# Auto-renewal
sudo crontab -e
# Add: 0 12 * * * /usr/bin/certbot renew --quiet
```

### **Step 10: Redis Setup (Optional - for caching)**

```bash
# Install Redis
sudo apt install -y redis-server

# Configure Redis
sudo nano /etc/redis/redis.conf
# Set: maxmemory 256mb
# Set: maxmemory-policy allkeys-lru

# Start Redis
sudo systemctl start redis-server
sudo systemctl enable redis-server
```

## 📊 Monitoring & Maintenance

### **Service Management**
```bash
# Check service status
sudo systemctl status bluehawks
sudo systemctl status nginx
sudo systemctl status postgresql

# View logs
sudo journalctl -u bluehawks -f
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log
```

### **Backup Strategy**
```bash
# Database backup
pg_dump bluehawks > backup_$(date +%Y%m%d_%H%M%S).sql

# Static files backup
tar -czf static_backup_$(date +%Y%m%d_%H%M%S).tar.gz /var/www/bluehawks/backend/staticfiles/

# Full project backup
tar -czf project_backup_$(date +%Y%m%d_%H%M%S).tar.gz /var/www/bluehawks/
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

## 🔧 Troubleshooting

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

4. **Gunicorn not starting**
   ```bash
   sudo journalctl -u bluehawks -f
   sudo systemctl restart bluehawks
   ```

## 📋 Backend Deployment Checklist

- [ ] Server setup completed
- [ ] Database installed and configured
- [ ] Project uploaded to server
- [ ] Virtual environment created
- [ ] Dependencies installed
- [ ] Environment variables configured
- [ ] Production settings applied
- [ ] Database migrations run
- [ ] Static files collected
- [ ] Gunicorn configured and running
- [ ] Nginx configured and running
- [ ] SSL certificate installed
- [ ] Domain DNS configured
- [ ] Monitoring set up
- [ ] Backup strategy implemented
- [ ] Security headers configured
- [ ] Performance optimized
- [ ] Testing completed

---

**Bluehawks Security Services** - Backend deployment guide for production environment.


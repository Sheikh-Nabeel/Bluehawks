#!/bin/bash

# Bluehawks Security Services - Deployment Script
# This script helps deploy the Django application to a VPS

echo "🚀 Starting Bluehawks deployment..."

# Update system packages
echo "📦 Updating system packages..."
sudo apt update && sudo apt upgrade -y

# Install required system packages
echo "🔧 Installing system dependencies..."
sudo apt install -y python3 python3-pip python3-venv nginx git

# Create application directory
echo "📁 Setting up application directory..."
sudo mkdir -p /var/www/bluehawks
sudo chown $USER:$USER /var/www/bluehawks

# Clone or copy your project
echo "📋 Copying project files..."
# If using git: git clone your-repo-url /var/www/bluehawks
# Or copy files manually to /var/www/bluehawks

# Navigate to project directory
cd /var/www/bluehawks

# Create virtual environment
echo "🐍 Setting up Python virtual environment..."
python3 -m venv venv
source venv/bin/activate

# Install Python dependencies
echo "📦 Installing Python dependencies..."
pip install -r requirements.txt

# Create .env file
echo "🔐 Setting up environment variables..."
cp env.example .env
# Edit .env file with your actual values

# Run Django migrations
echo "🗄️ Setting up database..."
python manage.py migrate

# Collect static files
echo "📁 Collecting static files..."
python manage.py collectstatic --noinput

# Create superuser (optional)
echo "👤 Creating superuser..."
python manage.py createsuperuser

# Configure Nginx
echo "🌐 Configuring Nginx..."
sudo tee /etc/nginx/sites-available/bluehawks << EOF
server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;

    location = /favicon.ico { access_log off; log_not_found off; }
    
    location /static/ {
        root /var/www/bluehawks;
    }

    location /media/ {
        root /var/www/bluehawks;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/run/bluehawks.sock;
    }
}
EOF

# Enable the site
sudo ln -s /etc/nginx/sites-available/bluehawks /etc/nginx/sites-enabled
sudo nginx -t
sudo systemctl restart nginx

# Configure Gunicorn service
echo "⚙️ Configuring Gunicorn service..."
sudo tee /etc/systemd/system/bluehawks.service << EOF
[Unit]
Description=Bluehawks Security Services
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/var/www/bluehawks
Environment="PATH=/var/www/bluehawks/venv/bin"
ExecStart=/var/www/bluehawks/venv/bin/gunicorn --config gunicorn.conf.py bluehawks.wsgi:application
ExecReload=/bin/kill -s HUP \$MAINPID
Restart=always

[Install]
WantedBy=multi-user.target
EOF

# Set permissions
sudo chown -R www-data:www-data /var/www/bluehawks
sudo chmod -R 755 /var/www/bluehawks

# Start and enable services
echo "🚀 Starting services..."
sudo systemctl daemon-reload
sudo systemctl start bluehawks
sudo systemctl enable bluehawks

# Configure firewall
echo "🔥 Configuring firewall..."
sudo ufw allow 'Nginx Full'
sudo ufw allow ssh
sudo ufw enable

echo "✅ Deployment completed successfully!"
echo "🌐 Your site should be available at: http://yourdomain.com"
echo "📝 Don't forget to:"
echo "   - Update your domain DNS settings"
echo "   - Configure SSL certificate with Let's Encrypt"
echo "   - Update .env file with production values" 
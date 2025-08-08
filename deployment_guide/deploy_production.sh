#!/bin/bash

# Bluehawks Security Services - Production Deployment Script
# This script helps deploy the Django application to production

echo "🚀 Starting Bluehawks Production Deployment..."

# Check if running as root
if [ "$EUID" -ne 0 ]; then
    echo "❌ Please run as root (use sudo)"
    exit 1
fi

# Update system packages
echo "📦 Updating system packages..."
apt update && apt upgrade -y

# Install required system packages
echo "🔧 Installing system dependencies..."
apt install -y python3 python3-pip python3-venv nginx postgresql postgresql-contrib git certbot python3-certbot-nginx

# Create application directory
echo "📁 Setting up application directory..."
mkdir -p /var/www/bluehawks
chown $SUDO_USER:$SUDO_USER /var/www/bluehawks

# Create log directory
mkdir -p /var/log/bluehawks
chown www-data:www-data /var/log/bluehawks

echo "✅ System setup completed!"
echo ""
echo "📋 Next Steps:"
echo "1. Upload your project to /var/www/bluehawks/"
echo "2. Copy env.production.template to .env and configure it"
echo "3. Run: cd /var/www/bluehawks/backend"
echo "4. Run: python3 -m venv venv"
echo "5. Run: source venv/bin/activate"
echo "6. Run: pip install -r requirements.txt"
echo "7. Run: python manage.py migrate"
echo "8. Run: python manage.py collectstatic --noinput"
echo "9. Configure Gunicorn and Nginx"
echo "10. Set up SSL certificate"
echo ""
echo "📖 See DEPLOYMENT_GUIDE.md for detailed instructions"

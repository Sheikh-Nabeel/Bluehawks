# 🚀 Quick Render Deployment Steps

## Step 1: Push to GitHub
```bash
git add .
git commit -m "Ready for Render deployment"
git push origin main
```

## Step 2: Deploy on Render

### Option A: Using Blueprint (Recommended)
1. Go to [dashboard.render.com](https://dashboard.render.com)
2. Click "New +" → "Blueprint"
3. Connect your GitHub repository
4. Click "Apply" - Render will automatically create everything!

### Option B: Manual Setup
1. Go to [dashboard.render.com](https://dashboard.render.com)
2. Click "New +" → "Web Service"
3. Connect your GitHub repository
4. Configure:
   - **Name**: `bluehawks`
   - **Build Command**: `cd backend && chmod +x build.sh && ./build.sh`
   - **Start Command**: `cd backend && gunicorn bluehawks.wsgi:application --bind 0.0.0.0:$PORT`
5. Add Environment Variables:
   ```
   PYTHON_VERSION=3.11.0
   DEBUG=false
   DJANGO_SETTINGS_MODULE=bluehawks.settings_production
   ALLOWED_HOSTS=.onrender.com
   ```
6. Create PostgreSQL database and link it
7. Deploy!

## Step 3: Create Admin User
After deployment, in Render Shell:
```bash
cd backend
export DJANGO_SETTINGS_MODULE=bluehawks.settings_production
python manage.py createsuperuser
```

## Step 4: Access Your Site
- **Main Site**: `https://your-app-name.onrender.com`
- **Admin**: `https://your-app-name.onrender.com/admin`

## ✅ Done! Your Bluehawks Security Services is now live! 
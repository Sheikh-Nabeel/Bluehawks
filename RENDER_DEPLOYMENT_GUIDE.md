# 🚀 Bluehawks Security Services - Render Deployment Guide

## 📋 Prerequisites

Before deploying to Render, ensure you have:

1. **GitHub Account**: Your code should be in a GitHub repository
2. **Render Account**: Sign up at [render.com](https://render.com)
3. **Project Ready**: Your Django project should be working locally

## 🎯 Quick Deployment Steps

### Step 1: Prepare Your Repository

1. **Push your code to GitHub** (if not already done):
   ```bash
   git add .
   git commit -m "Prepare for Render deployment"
   git push origin main
   ```

### Step 2: Deploy on Render

1. **Go to Render Dashboard**: Visit [dashboard.render.com](https://dashboard.render.com)

2. **Create New Web Service**:
   - Click "New +"
   - Select "Web Service"
   - Connect your GitHub repository
   - Select the repository containing your Bluehawks project

3. **Configure the Service**:
   - **Name**: `bluehawks` (or your preferred name)
   - **Environment**: `Python 3`
   - **Build Command**: `cd backend && chmod +x build.sh && ./build.sh`
   - **Start Command**: `cd backend && gunicorn bluehawks.wsgi:application --bind 0.0.0.0:$PORT`

4. **Environment Variables** (Add these):
   ```
   PYTHON_VERSION=3.11.0
   SECRET_KEY=[Render will generate this automatically]
   DEBUG=false
   DJANGO_SETTINGS_MODULE=bluehawks.settings_production
   ALLOWED_HOSTS=.onrender.com
   ```

5. **Create Database**:
   - Go to "New +" → "PostgreSQL"
   - Name: `bluehawks-db`
   - Plan: Free
   - Copy the connection string

6. **Link Database**:
   - Go back to your web service
   - Add environment variable:
     - Key: `DATABASE_URL`
     - Value: [Paste the PostgreSQL connection string]

7. **Deploy**:
   - Click "Create Web Service"
   - Render will automatically build and deploy your application

## 🔧 Alternative: Using render.yaml (Recommended)

If you have the `render.yaml` file in your repository:

1. **Go to Render Dashboard**
2. **Click "New +" → "Blueprint"**
3. **Connect your GitHub repository**
4. **Render will automatically detect the `render.yaml` file**
5. **Click "Apply" to create all services**

This will automatically create:
- PostgreSQL database
- Web service with all configurations
- Environment variables

## 🌐 Access Your Application

After deployment:

- **Main Site**: `https://your-app-name.onrender.com`
- **Admin Panel**: `https://your-app-name.onrender.com/admin`

## 🔐 Create Admin User

After deployment, you need to create a superuser:

1. **Go to your Render dashboard**
2. **Select your web service**
3. **Go to "Shell" tab**
4. **Run these commands**:
   ```bash
   cd backend
   export DJANGO_SETTINGS_MODULE=bluehawks.settings_production
   python manage.py createsuperuser
   ```

## 🔍 Troubleshooting

### Common Issues:

1. **Build Fails**:
   - Check the build logs in Render dashboard
   - Ensure all dependencies are in `requirements.txt`
   - Verify the build script has execute permissions

2. **Database Connection Issues**:
   - Verify `DATABASE_URL` environment variable is set
   - Check if PostgreSQL service is running
   - Ensure `dj-database-url` is in requirements.txt

3. **Static Files Not Loading**:
   - Check if `collectstatic` ran successfully
   - Verify `STATIC_ROOT` is set correctly
   - Ensure WhiteNoise is configured

4. **500 Internal Server Error**:
   - Check application logs in Render dashboard
   - Verify all environment variables are set
   - Check if migrations ran successfully

### Debug Commands:

```bash
# Check Django settings
python manage.py check --deploy

# Check database connection
python manage.py dbshell

# Check static files
python manage.py collectstatic --dry-run

# Run migrations manually
python manage.py migrate
```

## 📊 Monitoring Your Application

### Render Dashboard Features:

1. **Logs**: View real-time application logs
2. **Metrics**: Monitor CPU, memory, and request metrics
3. **Events**: Track deployments and service events
4. **Shell**: Access your application environment

### Health Checks:

- Render automatically checks your application health
- If the application fails to respond, it will restart
- Monitor the "Health" tab in your service dashboard

## 🔄 Updating Your Application

### Automatic Deployments:

- Render automatically deploys when you push to your main branch
- You can configure branch-specific deployments
- Manual deployments are also available

### Manual Deployment:

1. **Push changes to GitHub**
2. **Go to Render dashboard**
3. **Click "Manual Deploy"**
4. **Select the branch/commit to deploy**

## 💰 Free Tier Limitations

### Render Free Tier:

- **Web Services**: 750 hours/month (enough for 1 service running 24/7)
- **PostgreSQL**: 90 days free trial
- **Bandwidth**: 100GB/month
- **Sleep Mode**: Services sleep after 15 minutes of inactivity

### Upgrading:

- **Paid Plans**: Start at $7/month for always-on services
- **Database**: $7/month for persistent PostgreSQL
- **Custom Domains**: Available on paid plans

## 🚀 Performance Optimization

### For Better Performance:

1. **Enable Caching**:
   ```python
   # Add to settings_production.py
   CACHES = {
       'default': {
           'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
       }
   }
   ```

2. **Optimize Database Queries**:
   - Use `select_related()` and `prefetch_related()`
   - Add database indexes
   - Monitor slow queries

3. **Static File Optimization**:
   - Enable WhiteNoise compression
   - Use CDN for static files (on paid plans)

## 🔒 Security Best Practices

### Environment Variables:

- Never commit sensitive data to Git
- Use Render's environment variable system
- Rotate secrets regularly

### Django Security:

- Keep Django and dependencies updated
- Use HTTPS (enabled by default on Render)
- Enable security headers
- Regular security audits

## 📞 Support

### Render Support:

- **Documentation**: [docs.render.com](https://docs.render.com)
- **Community**: [community.render.com](https://community.render.com)
- **Email Support**: Available on paid plans

### Project-Specific Issues:

- Check the logs in Render dashboard
- Review Django error logs
- Test locally with production settings

## 🎉 Success Checklist

After deployment, verify:

- [ ] Application loads without errors
- [ ] Database migrations completed
- [ ] Static files are served correctly
- [ ] Admin panel is accessible
- [ ] Forms and functionality work
- [ ] HTTPS is working
- [ ] Environment variables are set correctly

---

**🎯 Your Bluehawks Security Services application is now live on Render!**

**Main URL**: `https://your-app-name.onrender.com`
**Admin URL**: `https://your-app-name.onrender.com/admin`

Remember to:
- Create a superuser account
- Test all functionality
- Monitor the application logs
- Set up monitoring and alerts if needed 
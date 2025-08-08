# 🎨 Frontend Deployment Guide - Bluehawks Security Services

## 📋 Overview

This guide covers deploying the frontend for Bluehawks Security Services. Since your current setup uses Django templates, this guide provides options for both traditional Django frontend and modern separated frontend deployments.

## 🏗️ Frontend Architecture Options

### **Option 1: Traditional Django Frontend (Current Setup)**
- **Technology**: Django Templates + HTML/CSS/JavaScript
- **Deployment**: Served by Django backend
- **Advantages**: Simple, integrated, SEO-friendly
- **Best for**: Business websites, content-heavy sites

### **Option 2: Modern Separated Frontend**
- **Technology**: React/Vue.js + API
- **Deployment**: CDN/Static hosting
- **Advantages**: Scalable, modern, better UX
- **Best for**: Dynamic applications, SPAs

## 📦 Option 1: Traditional Django Frontend Deployment

Since your current setup uses Django templates, the frontend is deployed with the backend. Follow the **Backend Deployment Guide** for complete deployment.

### **Frontend-Specific Optimizations**

```bash
# Optimize static files
cd backend
python manage.py collectstatic --noinput

# Compress CSS/JS (if using django-compressor)
pip install django-compressor

# Add to settings.py
INSTALLED_APPS = [
    # ... existing apps
    'compressor',
]

STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',
]

COMPRESS_ENABLED = True
COMPRESS_CSS_FILTERS = ['compressor.filters.css_default.CssAbsoluteFilter', 'compressor.filters.cssmin.rCSSMinFilter']
COMPRESS_JS_FILTERS = ['compressor.filters.jsmin.JSMinFilter']
```

### **Nginx Configuration for Frontend**

```nginx
# Add to your Nginx configuration
location /static/ {
    alias /var/www/bluehawks/backend/staticfiles/;
    expires 1y;
    add_header Cache-Control "public, immutable";
    access_log off;
    
    # Gzip compression
    gzip_static on;
    
    # Security headers
    add_header X-Content-Type-Options nosniff;
    add_header X-Frame-Options DENY;
}

# Optimize images
location ~* \.(jpg|jpeg|png|gif|ico|svg)$ {
    expires 1y;
    add_header Cache-Control "public, immutable";
    access_log off;
}

# Optimize fonts
location ~* \.(woff|woff2|ttf|eot)$ {
    expires 1y;
    add_header Cache-Control "public, immutable";
    access_log off;
}
```

## 🌐 Option 2: Modern Separated Frontend Deployment

### **Step 1: Create React Frontend**

```bash
# Create React app
npx create-react-app bluehawks-frontend
cd bluehawks-frontend

# Install dependencies
npm install axios react-router-dom @mui/material @emotion/react @emotion/styled
npm install @mui/icons-material react-helmet-async

# Install development dependencies
npm install --save-dev @babel/plugin-proposal-private-property-in-object
```

### **Step 2: Frontend Structure**

```
bluehawks-frontend/
├── public/
│   ├── index.html
│   ├── favicon.ico
│   └── manifest.json
├── src/
│   ├── components/
│   │   ├── Header.js
│   │   ├── Footer.js
│   │   ├── Navigation.js
│   │   └── ServiceCard.js
│   ├── pages/
│   │   ├── Home.js
│   │   ├── About.js
│   │   ├── Services.js
│   │   ├── Contact.js
│   │   └── ServiceDetail.js
│   ├── services/
│   │   └── api.js
│   ├── utils/
│   │   └── constants.js
│   ├── App.js
│   └── index.js
├── package.json
└── README.md
```

### **Step 3: API Integration**

```javascript
// src/services/api.js
import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const getServices = async () => {
  const response = await api.get('/services/');
  return response.data;
};

export const getServiceDetail = async (slug) => {
  const response = await api.get(`/services/${slug}/`);
  return response.data;
};

export const submitContact = async (data) => {
  const response = await api.post('/contact/', data);
  return response.data;
};

export const submitAirportBooking = async (data) => {
  const response = await api.post('/airport-bookings/', data);
  return response.data;
};

export default api;
```

### **Step 4: Build for Production**

```bash
# Build the application
npm run build

# The build folder contains optimized static files
ls build/
# index.html, static/css/, static/js/, static/media/
```

## 🚀 Frontend Deployment Options

### **Option A: Netlify (Recommended for Start)**

```bash
# Install Netlify CLI
npm install -g netlify-cli

# Deploy to Netlify
netlify deploy --prod --dir=build

# Or connect to Git repository
netlify sites:create --name bluehawks-security
```

**Netlify Configuration (`netlify.toml`):**
```toml
[build]
  publish = "build"
  command = "npm run build"

[build.environment]
  REACT_APP_API_URL = "https://your-backend-domain.com/api"

[[redirects]]
  from = "/*"
  to = "/index.html"
  status = 200
```

### **Option B: Vercel**

```bash
# Install Vercel CLI
npm install -g vercel

# Deploy to Vercel
vercel --prod

# Or connect to Git repository
vercel --name bluehawks-security
```

**Vercel Configuration (`vercel.json`):**
```json
{
  "version": 2,
  "builds": [
    {
      "src": "package.json",
      "use": "@vercel/static-build",
      "config": {
        "distDir": "build"
      }
    }
  ],
  "routes": [
    {
      "src": "/static/(.*)",
      "dest": "/static/$1"
    },
    {
      "src": "/(.*)",
      "dest": "/index.html"
    }
  ],
  "env": {
    "REACT_APP_API_URL": "https://your-backend-domain.com/api"
  }
}
```

### **Option C: AWS S3 + CloudFront**

```bash
# Install AWS CLI
pip install awscli

# Configure AWS
aws configure

# Create S3 bucket
aws s3 mb s3://bluehawks-frontend

# Upload build files
aws s3 sync build/ s3://bluehawks-frontend --delete

# Configure CloudFront distribution
aws cloudfront create-distribution --distribution-config file://cloudfront-config.json
```

### **Option D: GitHub Pages**

```bash
# Install gh-pages
npm install --save-dev gh-pages

# Add to package.json
{
  "scripts": {
    "predeploy": "npm run build",
    "deploy": "gh-pages -d build"
  },
  "homepage": "https://yourusername.github.io/bluehawks-frontend"
}

# Deploy
npm run deploy
```

## 🔧 Environment Configuration

### **Development Environment**

```bash
# .env.development
REACT_APP_API_URL=http://localhost:8000/api
REACT_APP_SITE_NAME=Bluehawks Security Services
REACT_APP_SITE_URL=http://localhost:3000
```

### **Production Environment**

```bash
# .env.production
REACT_APP_API_URL=https://api.yourdomain.com
REACT_APP_SITE_NAME=Bluehawks Security Services
REACT_APP_SITE_URL=https://yourdomain.com
```

## 📊 Performance Optimization

### **Code Splitting**

```javascript
// src/App.js
import React, { Suspense, lazy } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';

const Home = lazy(() => import('./pages/Home'));
const About = lazy(() => import('./pages/About'));
const Services = lazy(() => import('./pages/Services'));
const Contact = lazy(() => import('./pages/Contact'));

function App() {
  return (
    <Router>
      <Suspense fallback={<div>Loading...</div>}>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/about" element={<About />} />
          <Route path="/services" element={<Services />} />
          <Route path="/contact" element={<Contact />} />
        </Routes>
      </Suspense>
    </Router>
  );
}
```

### **Image Optimization**

```bash
# Install image optimization tools
npm install --save-dev imagemin imagemin-webp imagemin-mozjpeg imagemin-pngquant

# Add to package.json scripts
{
  "scripts": {
    "optimize-images": "imagemin src/images/* --out-dir=src/images/optimized"
  }
}
```

### **Lazy Loading**

```javascript
// Lazy load images
import { LazyLoadImage } from 'react-lazy-load-image-component';
import 'react-lazy-load-image-component/src/effects/blur.css';

<LazyLoadImage
  src={imageUrl}
  alt={altText}
  effect="blur"
  width={400}
  height={300}
/>
```

## 🔒 Security Configuration

### **Content Security Policy**

```html
<!-- public/index.html -->
<meta http-equiv="Content-Security-Policy" content="
  default-src 'self';
  script-src 'self' 'unsafe-inline' 'unsafe-eval';
  style-src 'self' 'unsafe-inline' https://fonts.googleapis.com;
  font-src 'self' https://fonts.gstatic.com;
  img-src 'self' data: https:;
  connect-src 'self' https://api.yourdomain.com;
">
```

### **HTTPS Configuration**

```javascript
// Force HTTPS in production
if (process.env.NODE_ENV === 'production') {
  if (window.location.protocol === 'http:') {
    window.location.href = window.location.href.replace('http:', 'https:');
  }
}
```

## 📱 PWA Configuration

### **Service Worker**

```javascript
// src/serviceWorker.js
const CACHE_NAME = 'bluehawks-v1';
const urlsToCache = [
  '/',
  '/static/css/main.css',
  '/static/js/main.js',
];

self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then((cache) => cache.addAll(urlsToCache))
  );
});

self.addEventListener('fetch', (event) => {
  event.respondWith(
    caches.match(event.request)
      .then((response) => response || fetch(event.request))
  );
});
```

### **Manifest Configuration**

```json
// public/manifest.json
{
  "short_name": "Bluehawks",
  "name": "Bluehawks Security Services",
  "icons": [
    {
      "src": "favicon.ico",
      "sizes": "64x64 32x32 24x24 16x16",
      "type": "image/x-icon"
    }
  ],
  "start_url": ".",
  "display": "standalone",
  "theme_color": "#000000",
  "background_color": "#ffffff"
}
```

## 📊 Monitoring & Analytics

### **Google Analytics**

```javascript
// src/utils/analytics.js
import ReactGA from 'react-ga';

ReactGA.initialize('GA_TRACKING_ID');

export const trackPageView = (page) => {
  ReactGA.pageview(page);
};

export const trackEvent = (category, action, label) => {
  ReactGA.event({
    category,
    action,
    label,
  });
};
```

### **Error Tracking**

```javascript
// src/utils/errorTracking.js
import * as Sentry from '@sentry/react';

Sentry.init({
  dsn: 'YOUR_SENTRY_DSN',
  environment: process.env.NODE_ENV,
});

export const captureException = (error) => {
  Sentry.captureException(error);
};
```

## 📋 Frontend Deployment Checklist

### **For Traditional Django Frontend:**
- [ ] Static files collected and optimized
- [ ] CSS/JS minification configured
- [ ] Image optimization completed
- [ ] Gzip compression enabled
- [ ] Cache headers configured
- [ ] Security headers set
- [ ] Mobile responsiveness tested
- [ ] Cross-browser compatibility verified

### **For Modern Separated Frontend:**
- [ ] React/Vue.js application built
- [ ] Environment variables configured
- [ ] API endpoints integrated
- [ ] Performance optimizations applied
- [ ] PWA features implemented
- [ ] SEO meta tags added
- [ ] Analytics configured
- [ ] Error tracking set up
- [ ] CDN deployment completed
- [ ] SSL certificate installed
- [ ] Domain DNS configured
- [ ] Testing completed

## 🎯 Recommended Approach

For your security services website, I recommend:

1. **Start with Traditional Django Frontend** (Option 1)
   - ✅ Simple to implement
   - ✅ Cost-effective
   - ✅ SEO-friendly
   - ✅ Easy to maintain

2. **Upgrade to Modern Frontend later** (Option 2)
   - When you need more dynamic features
   - When you want better user experience
   - When you have more development resources

---

**Bluehawks Security Services** - Frontend deployment guide for modern web applications.


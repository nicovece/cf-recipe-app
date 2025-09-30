# 🚀 Render.com Deployment Checklist

## ✅ Pre-Deployment (Completed)

- [x] Environment variables configured
- [x] New SECRET_KEY generated
- [x] Security settings implemented
- [x] Requirements.txt updated with gunicorn
- [x] Render.yaml configuration created
- [x] .gitignore updated
- [x] Local testing completed

## 🎯 Render.com Deployment Steps

### 1. Push to GitHub

```bash
git add .
git commit -m "Add production security settings and deployment config"
git push origin main
```

### 2. Connect to Render.com

1. Go to [render.com](https://render.com)
2. Sign up/Login with your GitHub account
3. Click "New +" → "Web Service"
4. Connect your GitHub repository

### 3. Configure Render Service

- **Name**: `django-recipe-app` (or your preferred name)
- **Environment**: `Python 3`
- **Build Command**:
  ```bash
  pip install -r requirements.txt; cd src; python manage.py collectstatic --noinput; python manage.py migrate
  ```
- **Start Command**:
  ```bash
  cd src; gunicorn recipe_project.wsgi:application
  ```

### 4. Set Environment Variables in Render

In the Render dashboard, add these environment variables:

| Key                              | Value                                               |
| -------------------------------- | --------------------------------------------------- |
| `SECRET_KEY`                     | (Generate new one in Render or use your .env value) |
| `DEBUG`                          | `False`                                             |
| `ALLOWED_HOSTS`                  | `your-app-name.onrender.com`                        |
| `SECURE_SSL_REDIRECT`            | `True`                                              |
| `SECURE_HSTS_SECONDS`            | `31536000`                                          |
| `SECURE_HSTS_INCLUDE_SUBDOMAINS` | `True`                                              |
| `SECURE_HSTS_PRELOAD`            | `True`                                              |
| `SECURE_CONTENT_TYPE_NOSNIFF`    | `True`                                              |
| `SECURE_BROWSER_XSS_FILTER`      | `True`                                              |
| `X_FRAME_OPTIONS`                | `DENY`                                              |
| `SECURE_REFERRER_POLICY`         | `strict-origin-when-cross-origin`                   |

### 5. Deploy

1. Click "Create Web Service"
2. Wait for deployment to complete
3. Your app will be available at `https://your-app-name.onrender.com`

## 🔍 Post-Deployment Verification

### Test These Features:

- [ ] Home page loads
- [ ] Login/logout works
- [ ] Recipe list displays
- [ ] Recipe search works
- [ ] Static files (CSS) load correctly
- [ ] Media files (images) display
- [ ] HTTPS is working (green lock icon)
- [ ] No debug information shown in errors

### Security Check:

- [ ] Visit your site and check for HTTPS
- [ ] Test with [securityheaders.com](https://securityheaders.com)
- [ ] Verify no sensitive information in error pages

## 🚨 Common Issues & Solutions

### Static Files Not Loading

**Solution**: Ensure `collectstatic` runs during build

### Media Files Not Accessible

**Solution**: Consider using AWS S3 or Cloudinary for production media storage

### Database Errors

**Solution**: Ensure all migrations are applied

### Environment Variables Not Working

**Solution**: Double-check variable names and values in Render dashboard

## 📞 Support

If you encounter issues:

1. Check Render deployment logs
2. Verify environment variables are set correctly
3. Ensure all dependencies are in requirements.txt
4. Test locally first with `DEBUG=False`

## 🎉 Success!

Once deployed, your Django Recipe App will be:

- ✅ Secure with production-grade security headers
- ✅ Fast with optimized static file serving
- ✅ Scalable with proper WSGI configuration
- ✅ Professional with HTTPS and security best practices

Your app is now production-ready! 🚀

# 🚀 TaskFlow AI - Complete Deployment Guide

This guide will help you deploy your TaskFlow AI Customer Success Agent to production using **free tier** services.

## 📋 Prerequisites

- GitHub account (for code hosting)
- Vercel account (free - for frontend)
- Hugging Face account (free - for backend)
- Neon.tech or Supabase account (free - for PostgreSQL)
- OpenAI API key (paid - for AI agent)
- Twilio account (for WhatsApp)
- Google Cloud account (for Gmail API)

---

## 🗂️ Project Structure

```
Hackathon 5/
├── backend/          # FastAPI backend (deploy to Hugging Face Spaces)
│   ├── src/
│   ├── alembic/
│   ├── context/
│   ├── Dockerfile
│   ├── requirements.txt
│   └── .env.example
├── frontend/         # Next.js frontend (deploy to Vercel)
│   ├── app/
│   ├── components/
│   ├── lib/
│   ├── package.json
│   └── vercel.json
└── DEPLOYMENT_GUIDE.md (this file)
```

---

## 📦 Step 1: Setup Free PostgreSQL Database

### Option A: Neon.tech (Recommended)

1. Go to https://neon.tech
2. Sign up for free account
3. Click "Create Project"
4. Project name: `taskflow-ai`
5. Region: Choose closest to you
6. PostgreSQL version: 16 (latest)
7. Click "Create Project"
8. Copy the connection string (looks like):
   ```
   postgresql://username:password@ep-cool-name-123456.us-east-2.aws.neon.tech/neondb?sslmode=require
   ```
9. Save this - you'll need it for backend deployment

### Option B: Supabase

1. Go to https://supabase.com
2. Sign up for free account
3. Click "New Project"
4. Project name: `taskflow-ai`
5. Database password: Create strong password
6. Region: Choose closest to you
7. Wait for project to be created (~2 minutes)
8. Go to Settings → Database
9. Copy "Connection string" under "Connection pooling"
10. Replace `[YOUR-PASSWORD]` with your actual password
11. Save this connection string

---

## 🐳 Step 2: Deploy Backend to Hugging Face Spaces

### 2.1 Create Hugging Face Space

1. Go to https://huggingface.co/spaces
2. Click "Create new Space"
3. Fill in details:
   - **Space name:** `taskflow-ai-backend`
   - **License:** Apache 2.0
   - **Select SDK:** Docker
   - **Space hardware:** CPU basic (free)
   - **Visibility:** Public (or Private if you prefer)
4. Click "Create Space"

### 2.2 Upload Backend Files

You have two options:

**Option A: Git Push (Recommended)**

```bash
cd backend
git init
git remote add space https://huggingface.co/spaces/YOUR_USERNAME/taskflow-ai-backend
git add .
git commit -m "Initial backend deployment"
git push space main
```

**Option B: Web Upload**

1. In your Space, click "Files" tab
2. Click "Add file" → "Upload files"
3. Upload all files from `backend/` folder:
   - `src/` (entire folder)
   - `alembic/` (entire folder)
   - `context/` (entire folder)
   - `Dockerfile`
   - `requirements.txt`
   - `alembic.ini`

### 2.3 Configure Environment Variables (Secrets)

1. In your Space, click "Settings" tab
2. Scroll to "Repository secrets"
3. Add these secrets one by one:

**Required Secrets:**

```bash
# Database
DATABASE_URL=postgresql://user:pass@host:5432/db?sslmode=require

# Application
APP_ENV=production
USE_SIMPLE_CONFIG=false
LOG_LEVEL=INFO

# OpenAI
OPENAI_API_KEY=sk-...

# Twilio WhatsApp
TWILIO_ACCOUNT_SID=AC...
TWILIO_AUTH_TOKEN=...
TWILIO_WHATSAPP_NUMBER=whatsapp:+14155238886

# Gmail (paste entire JSON as one line)
GMAIL_CREDENTIALS_JSON={"installed":{"client_id":"...","project_id":"...","auth_uri":"https://accounts.google.com/o/oauth2/auth","token_uri":"https://oauth2.googleapis.com/token","auth_provider_x509_cert_url":"https://www.googleapis.com/oauth2/v1/certs","client_secret":"...","redirect_uris":["http://localhost"]}}

# Features
ENABLE_EMAIL_POLLING=true
EMAIL_POLL_INTERVAL=60
ENABLE_DAILY_REPORTS=true
ENABLE_METRICS=false

# API
API_HOST=0.0.0.0
API_PORT=7860
API_WORKERS=1
CORS_ORIGINS=*
```

4. Click "Save" after adding each secret

### 2.4 Wait for Build

1. Go to "Logs" tab
2. Watch the build process (takes 3-5 minutes)
3. Wait for "Running on http://0.0.0.0:7860"
4. Your backend is now live!

### 2.5 Test Backend

Your backend URL will be:
```
https://YOUR_USERNAME-taskflow-ai-backend.hf.space
```

Test it:
```bash
curl https://YOUR_USERNAME-taskflow-ai-backend.hf.space/api/health
```

Should return:
```json
{
  "status": "healthy",
  "database": "connected",
  "timestamp": "2024-..."
}
```

---

## 🌐 Step 3: Deploy Frontend to Vercel

### 3.1 Push Code to GitHub

If not already done:

```bash
# In project root
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/taskflow-ai.git
git push -u origin main
```

### 3.2 Deploy to Vercel

1. Go to https://vercel.com
2. Sign up / Log in with GitHub
3. Click "Add New Project"
4. Import your GitHub repository
5. Configure project:
   - **Framework Preset:** Next.js (auto-detected)
   - **Root Directory:** `frontend`
   - **Build Command:** `npm run build` (default)
   - **Output Directory:** `.next` (default)
   - **Install Command:** `npm install` (default)

6. Add Environment Variable:
   - Key: `NEXT_PUBLIC_BACKEND_URL`
   - Value: `https://YOUR_USERNAME-taskflow-ai-backend.hf.space`
   - (Replace with your actual Hugging Face Space URL)

7. Click "Deploy"
8. Wait 2-3 minutes for deployment

### 3.3 Get Frontend URL

After deployment completes:
- Production URL: `https://your-project.vercel.app`
- Dashboard: `https://your-project.vercel.app/dashboard`
- Web Form: `https://your-project.vercel.app/web-form`

---

## 🔗 Step 4: Connect Twilio Webhook

### 4.1 Update Twilio WhatsApp Webhook

1. Go to https://console.twilio.com/
2. Navigate to Messaging → Try it out → Send a WhatsApp message
3. Click on your WhatsApp Sandbox
4. Under "Sandbox Configuration"
5. Set "When a message comes in" to:
   ```
   https://YOUR_USERNAME-taskflow-ai-backend.hf.space/api/webhooks/whatsapp
   ```
6. Method: `POST`
7. Click "Save"

### 4.2 Test WhatsApp

1. Send WhatsApp message to your Twilio number
2. Join sandbox: `join <your-sandbox-code>`
3. Send test message: `Hello, I need help`
4. Should receive AI response within seconds

---

## 📧 Step 5: Setup Gmail Integration

### 5.1 Enable Gmail API

1. Go to https://console.cloud.google.com/
2. Create new project: "TaskFlow AI"
3. Enable Gmail API:
   - APIs & Services → Library
   - Search "Gmail API"
   - Click "Enable"

### 5.2 Create OAuth Credentials

1. APIs & Services → Credentials
2. Click "Create Credentials" → "OAuth client ID"
3. Application type: "Desktop app"
4. Name: "TaskFlow Gmail Integration"
5. Click "Create"
6. Download JSON file
7. Copy entire JSON content (as single line)
8. Add to Hugging Face Space secrets as `GMAIL_CREDENTIALS_JSON`

### 5.3 Authorize Gmail Access (One-time)

This needs to be done locally first:

```bash
cd backend
pip install -r requirements.txt
python -c "from src.channels.gmail_channel import GmailChannel; GmailChannel().authenticate()"
```

Follow OAuth flow in browser, then upload generated `token.json` to Hugging Face Space.

---

## ✅ Step 6: Testing All Channels

### Test 1: Health Check

```bash
curl https://YOUR_USERNAME-taskflow-ai-backend.hf.space/api/health
```

### Test 2: Web Form

1. Go to `https://your-project.vercel.app/web-form`
2. Fill in form:
   - Name: Test User
   - Email: test@example.com
   - Subject: Test inquiry
   - Message: I need help with my account
3. Submit
4. Check dashboard for new conversation

### Test 3: WhatsApp

1. Send message to Twilio WhatsApp number
2. Should receive AI response
3. Check dashboard for conversation

### Test 4: Gmail

1. Send email to your support email
2. Wait 60 seconds (polling interval)
3. Should receive AI response
4. Check dashboard for conversation

### Test 5: Dashboard

1. Go to `https://your-project.vercel.app/dashboard`
2. Should see:
   - Total conversations
   - Channel breakdown
   - Recent activity
   - Sentiment analysis
   - Response times

---

## 🔧 Troubleshooting

### Backend Issues

**Space won't start:**
- Check Logs tab for errors
- Verify all required secrets are set
- Check DATABASE_URL format

**Database connection failed:**
- Test connection string locally
- Check Neon/Supabase firewall rules
- Ensure `?sslmode=require` is in connection string

**Gmail not working:**
- Verify GMAIL_CREDENTIALS_JSON is valid JSON (no line breaks)
- Check ENABLE_EMAIL_POLLING=true
- Upload token.json to Space

### Frontend Issues

**API calls failing:**
- Check NEXT_PUBLIC_BACKEND_URL is correct
- Verify backend is running (check health endpoint)
- Check browser console for CORS errors

**Build fails:**
- Check Vercel build logs
- Verify all dependencies in package.json
- Try local build: `npm run build`

### Channel Issues

**WhatsApp not responding:**
- Check Twilio webhook URL is correct
- Verify Twilio credentials in backend secrets
- Check backend logs for errors

**Email not responding:**
- Check Gmail polling is enabled
- Verify token.json is uploaded
- Check backend logs for Gmail errors

---

## 📊 Monitoring & Logs

### Backend Logs (Hugging Face)
1. Go to your Space
2. Click "Logs" tab
3. Monitor real-time logs

### Frontend Logs (Vercel)
1. Go to Vercel dashboard
2. Select your project
3. Click "Logs" tab

### Database Monitoring (Neon)
1. Go to Neon dashboard
2. Select your project
3. View "Monitoring" tab for queries, connections

---

## 💰 Cost Breakdown

- **Hugging Face Spaces:** FREE (CPU basic)
- **Vercel:** FREE (hobby plan)
- **Neon.tech:** FREE (0.5GB storage, 3GB data transfer)
- **OpenAI API:** ~$0.002 per conversation (pay as you go)
- **Twilio:** ~$0.005 per WhatsApp message
- **Google Gmail API:** FREE

**Estimated monthly cost:** $5-20 depending on usage

---

## 🎉 You're Done!

Your TaskFlow AI Customer Success Agent is now live and handling customer inquiries 24/7 across three channels!

**Next Steps:**
- Monitor dashboard for conversations
- Adjust AI prompts in `backend/context/` folder
- Add more channels if needed
- Scale up Hugging Face Space if traffic increases

**Support:**
- Backend issues: Check Hugging Face Space logs
- Frontend issues: Check Vercel deployment logs
- Database issues: Check Neon/Supabase dashboard

Happy deploying! 🚀

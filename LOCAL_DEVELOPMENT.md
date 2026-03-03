# 🧪 Local Development Guide

Complete guide for running TaskFlow AI locally before deployment.

## 📋 Prerequisites

- Python 3.11+
- Node.js 20+
- PostgreSQL (local or cloud)
- Git

## 🗄️ Step 1: Setup Database

### Option A: Local PostgreSQL

```bash
# Install PostgreSQL (if not installed)
# macOS: brew install postgresql
# Ubuntu: sudo apt-get install postgresql
# Windows: Download from postgresql.org

# Start PostgreSQL
# macOS: brew services start postgresql
# Ubuntu: sudo service postgresql start
# Windows: Start from Services

# Create database
psql postgres
CREATE DATABASE taskflow_crm;
CREATE USER taskflow WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE taskflow_crm TO taskflow;
\q
```

Your DATABASE_URL:
```
postgresql://taskflow:your_password@localhost:5432/taskflow_crm
```

### Option B: Cloud Database (Neon.tech)

1. Go to https://neon.tech
2. Create free account
3. Create new project
4. Copy connection string

## 🐍 Step 2: Setup Backend

```bash
# Navigate to backend
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# macOS/Linux:
source venv/bin/activate
# Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env

# Edit .env with your credentials
# Required:
# - DATABASE_URL
# - OPENAI_API_KEY
# - TWILIO credentials (for WhatsApp)
# - GMAIL credentials (for Email)
```

### Configure Environment Variables

Edit `backend/.env`:

```bash
# Database
DATABASE_URL=postgresql://taskflow:password@localhost:5432/taskflow_crm

# OpenAI
OPENAI_API_KEY=sk-your-key-here

# Twilio (get from console.twilio.com)
TWILIO_ACCOUNT_SID=ACxxxxx
TWILIO_AUTH_TOKEN=xxxxx
TWILIO_WHATSAPP_NUMBER=whatsapp:+14155238886

# Gmail (see Gmail Setup below)
GMAIL_CREDENTIALS_JSON={"installed":{...}}
ENABLE_EMAIL_POLLING=true

# App settings
APP_ENV=development
USE_SIMPLE_CONFIG=true
API_PORT=7860
LOG_LEVEL=INFO
```

### Run Database Migrations

```bash
# Create tables
alembic upgrade head
```

### Start Backend Server

```bash
# Run with auto-reload
python -m uvicorn src.main:app --host 0.0.0.0 --port 7860 --reload

# Or simply:
python src/main.py
```

Backend will be available at: http://localhost:7860

Test it:
```bash
curl http://localhost:7860/api/health
```

## 🌐 Step 3: Setup Frontend

Open a new terminal:

```bash
# Navigate to frontend
cd frontend

# Install dependencies
npm install

# Create .env.local
echo "NEXT_PUBLIC_BACKEND_URL=http://localhost:7860" > .env.local

# Start development server
npm run dev
```

Frontend will be available at: http://localhost:3000

## 📧 Step 4: Setup Gmail Integration (Optional)

### Enable Gmail API

1. Go to https://console.cloud.google.com/
2. Create new project: "TaskFlow AI Local"
3. Enable Gmail API:
   - APIs & Services → Library
   - Search "Gmail API"
   - Click "Enable"

### Create OAuth Credentials

1. APIs & Services → Credentials
2. Click "Create Credentials" → "OAuth client ID"
3. Application type: "Desktop app"
4. Name: "TaskFlow Local Dev"
5. Click "Create"
6. Download JSON file
7. Save as `backend/credentials/gmail-credentials.json`

### Authorize Gmail Access

```bash
cd backend
python -c "from src.channels.gmail_channel import GmailChannel; GmailChannel().authenticate()"
```

Follow OAuth flow in browser. This creates `token.json`.

### Update .env

Copy the content of `gmail-credentials.json` as a single line:

```bash
GMAIL_CREDENTIALS_JSON={"installed":{"client_id":"...","project_id":"...",...}}
```

## 📱 Step 5: Setup Twilio WhatsApp (Optional)

### Get Twilio Sandbox

1. Go to https://console.twilio.com/
2. Navigate to Messaging → Try it out → Send a WhatsApp message
3. Note your sandbox number
4. Get Account SID and Auth Token from dashboard

### Configure Webhook (for local testing)

Use ngrok to expose local server:

```bash
# Install ngrok: https://ngrok.com/download
ngrok http 7860
```

Copy the HTTPS URL (e.g., `https://abc123.ngrok.io`)

In Twilio Console:
1. Go to WhatsApp Sandbox settings
2. Set "When a message comes in" to:
   ```
   https://abc123.ngrok.io/api/webhooks/whatsapp
   ```
3. Method: POST
4. Save

### Test WhatsApp

1. Send WhatsApp to your Twilio number
2. Join sandbox: `join <your-code>`
3. Send: "Hello, I need help"
4. Should receive AI response

## 🧪 Step 6: Test All Features

### Test Health Check

```bash
curl http://localhost:7860/api/health
```

Expected response:
```json
{
  "status": "healthy",
  "database": "connected",
  "timestamp": "2024-..."
}
```

### Test Web Form

1. Go to http://localhost:3000/web-form
2. Fill in form:
   - Name: Test User
   - Email: test@example.com
   - Subject: Test inquiry
   - Message: I need help
3. Submit
4. Check backend logs for processing
5. Go to http://localhost:3000/dashboard
6. Should see new conversation

### Test Dashboard

1. Go to http://localhost:3000/dashboard
2. Should see:
   - Total conversations
   - Channel breakdown
   - Recent activity
   - Sentiment analysis

### Test WhatsApp (if configured)

1. Send WhatsApp message to Twilio number
2. Check backend logs
3. Should receive AI response
4. Check dashboard for new conversation

### Test Email (if configured)

1. Send email to your support email
2. Wait 60 seconds (polling interval)
3. Check backend logs
4. Should receive AI response
5. Check dashboard for conversation

## 🐛 Troubleshooting

### Backend Issues

**Database connection failed:**
```bash
# Check PostgreSQL is running
psql -U taskflow -d taskflow_crm -c "SELECT 1;"

# Check connection string format
# Should be: postgresql://user:pass@host:port/database
```

**Import errors:**
```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

**Port already in use:**
```bash
# Find process using port 7860
# macOS/Linux:
lsof -i :7860
# Windows:
netstat -ano | findstr :7860

# Kill the process or use different port
python -m uvicorn src.main:app --port 8000
```

### Frontend Issues

**API calls failing:**
- Check NEXT_PUBLIC_BACKEND_URL in .env.local
- Verify backend is running on port 7860
- Check browser console for errors

**Build errors:**
```bash
# Clear cache and reinstall
rm -rf .next node_modules package-lock.json
npm install
npm run dev
```

**Environment variable not working:**
- Must start with NEXT_PUBLIC_ to be exposed to browser
- Restart dev server after changing .env.local
- Clear browser cache

### Gmail Issues

**OAuth flow fails:**
- Check redirect URI in Google Cloud Console
- Should be: http://localhost
- Verify Gmail API is enabled

**Polling not working:**
- Check ENABLE_EMAIL_POLLING=true in .env
- Check backend logs for errors
- Verify token.json exists and is valid

### WhatsApp Issues

**Webhook not receiving messages:**
- Check ngrok is running
- Verify webhook URL in Twilio console
- Check ngrok web interface: http://localhost:4040
- Verify TWILIO credentials in .env

## 📊 Monitoring Logs

### Backend Logs

Backend logs appear in terminal where you ran uvicorn:
```
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:7860
```

### Frontend Logs

Frontend logs appear in terminal where you ran npm:
```
▲ Next.js 16.1.6
- Local:        http://localhost:3000
- Ready in 2.3s
```

### Database Logs

Check PostgreSQL logs:
```bash
# macOS:
tail -f /usr/local/var/log/postgres.log

# Ubuntu:
sudo tail -f /var/log/postgresql/postgresql-*.log
```

## 🎉 You're Ready!

Your local development environment is set up! You can now:

1. Develop new features
2. Test changes locally
3. Debug issues
4. Prepare for deployment

When ready to deploy, follow:
- [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)
- [DEPLOYMENT_CHECKLIST.md](DEPLOYMENT_CHECKLIST.md)

Happy coding! 🚀

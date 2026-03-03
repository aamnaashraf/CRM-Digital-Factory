# TaskFlow AI Backend - Hugging Face Spaces Deployment

## 🚀 Quick Deploy to Hugging Face Spaces

### 1. Create New Space
- Go to https://huggingface.co/spaces
- Click "Create new Space"
- Name: `taskflow-ai-backend`
- License: Apache 2.0
- Select: **Docker** (SDK)
- Hardware: **CPU basic** (free tier)
- Visibility: Public or Private

### 2. Upload Files
Upload this entire `backend` folder to your Space:
```
backend/
├── src/
├── alembic/
├── context/
├── Dockerfile
├── requirements.txt
├── alembic.ini
└── .env.example
```

### 3. Configure Environment Variables (Secrets)
In your Space settings, add these secrets:

**Required:**
```
DATABASE_URL=postgresql://user:pass@host:5432/dbname
OPENAI_API_KEY=sk-...
APP_ENV=production
USE_SIMPLE_CONFIG=false
```

**Twilio (WhatsApp):**
```
TWILIO_ACCOUNT_SID=AC...
TWILIO_AUTH_TOKEN=...
TWILIO_WHATSAPP_NUMBER=whatsapp:+14155238886
```

**Gmail:**
```
GMAIL_CREDENTIALS_JSON={"installed":{"client_id":"...","project_id":"...","auth_uri":"...","token_uri":"...","auth_provider_x509_cert_url":"...","client_secret":"...","redirect_uris":["..."]}}
ENABLE_EMAIL_POLLING=true
```

**Optional:**
```
ANTHROPIC_API_KEY=sk-ant-...
ENABLE_METRICS=false
LOG_LEVEL=INFO
```

### 4. Database Setup (Free PostgreSQL)

**Option A: Neon.tech (Recommended)**
1. Go to https://neon.tech
2. Create free account
3. Create new project
4. Copy connection string
5. Add to `DATABASE_URL` secret

**Option B: Supabase**
1. Go to https://supabase.com
2. Create free project
3. Get connection string from Settings > Database
4. Add to `DATABASE_URL` secret

### 5. Deploy
- Push code to Space
- Space will automatically build and deploy
- Your API will be available at: `https://YOUR_USERNAME-taskflow-ai-backend.hf.space`

### 6. Update Twilio Webhook
Set Twilio WhatsApp webhook to:
```
https://YOUR_USERNAME-taskflow-ai-backend.hf.space/api/webhooks/whatsapp
```

## 📝 API Endpoints

- Health: `GET /api/health`
- WhatsApp Webhook: `POST /api/webhooks/whatsapp`
- Email Webhook: `POST /api/webhooks/email`
- Web Form: `POST /api/webhooks/web-form`
- Dashboard: `GET /api/dashboard/stats`
- Support: `GET /api/support/conversations`

## 🔧 Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Set environment variables
cp .env.example .env
# Edit .env with your credentials

# Run locally
python -m uvicorn src.main:app --host 0.0.0.0 --port 7860 --reload
```

## 📊 Monitoring

Check logs in Hugging Face Spaces:
- Go to your Space
- Click "Logs" tab
- Monitor real-time application logs

## 🐛 Troubleshooting

**Space won't start:**
- Check logs for errors
- Verify all required secrets are set
- Ensure DATABASE_URL is valid

**Gmail not working:**
- Verify GMAIL_CREDENTIALS_JSON is valid JSON
- Check ENABLE_EMAIL_POLLING=true
- Run OAuth flow locally first to get token

**Database connection failed:**
- Test connection string locally
- Check firewall rules (Neon/Supabase)
- Verify SSL mode in connection string

# 🚀 TaskFlow AI - Quick Start Checklist

## ✅ Pre-Deployment Checklist

### 1. Database Setup
- [ ] Created Neon.tech or Supabase account
- [ ] Created PostgreSQL database
- [ ] Copied connection string
- [ ] Tested connection locally

### 2. API Keys
- [ ] OpenAI API key obtained
- [ ] Twilio account created
- [ ] Twilio WhatsApp sandbox configured
- [ ] Gmail API enabled in Google Cloud
- [ ] Gmail OAuth credentials downloaded

### 3. Code Repository
- [ ] Code pushed to GitHub
- [ ] Backend folder contains all files
- [ ] Frontend folder contains all files

---

## 🐳 Backend Deployment (Hugging Face Spaces)

### Step 1: Create Space
- [ ] Go to https://huggingface.co/spaces
- [ ] Create new Space with Docker SDK
- [ ] Name: `taskflow-ai-backend`
- [ ] Hardware: CPU basic (free)

### Step 2: Upload Files
- [ ] Upload entire `backend/` folder
- [ ] Verify Dockerfile is present
- [ ] Verify requirements.txt is present

### Step 3: Configure Secrets
Add these in Space Settings → Repository secrets:

- [ ] `DATABASE_URL` - PostgreSQL connection string
- [ ] `APP_ENV=production`
- [ ] `USE_SIMPLE_CONFIG=false`
- [ ] `OPENAI_API_KEY` - Your OpenAI key
- [ ] `TWILIO_ACCOUNT_SID` - From Twilio console
- [ ] `TWILIO_AUTH_TOKEN` - From Twilio console
- [ ] `TWILIO_WHATSAPP_NUMBER` - Your WhatsApp number
- [ ] `GMAIL_CREDENTIALS_JSON` - OAuth credentials (one line)
- [ ] `ENABLE_EMAIL_POLLING=true`
- [ ] `API_PORT=7860`
- [ ] `CORS_ORIGINS=*`

### Step 4: Verify Deployment
- [ ] Check Logs tab for "Running on http://0.0.0.0:7860"
- [ ] Test health endpoint: `curl https://YOUR_USERNAME-taskflow-ai-backend.hf.space/api/health`
- [ ] Copy your Space URL for frontend

**Your Backend URL:**
```
https://YOUR_USERNAME-taskflow-ai-backend.hf.space
```

---

## 🌐 Frontend Deployment (Vercel)

### Step 1: Import Project
- [ ] Go to https://vercel.com
- [ ] Click "Add New Project"
- [ ] Import GitHub repository
- [ ] Set Root Directory: `frontend`

### Step 2: Configure Environment
- [ ] Add environment variable:
  - Key: `NEXT_PUBLIC_BACKEND_URL`
  - Value: Your Hugging Face Space URL

### Step 3: Deploy
- [ ] Click "Deploy"
- [ ] Wait for build to complete
- [ ] Copy production URL

**Your Frontend URL:**
```
https://your-project.vercel.app
```

---

## 🔗 Connect Services

### Twilio Webhook
- [ ] Go to Twilio Console
- [ ] Navigate to WhatsApp Sandbox
- [ ] Set webhook URL: `https://YOUR_USERNAME-taskflow-ai-backend.hf.space/api/webhooks/whatsapp`
- [ ] Method: POST
- [ ] Save configuration

### Gmail OAuth (One-time setup)
Run locally first:
```bash
cd backend
pip install -r requirements.txt
python -c "from src.channels.gmail_channel import GmailChannel; GmailChannel().authenticate()"
```
- [ ] Complete OAuth flow in browser
- [ ] Upload generated `token.json` to Hugging Face Space

---

## 🧪 Testing

### Test Backend
```bash
# Health check
curl https://YOUR_USERNAME-taskflow-ai-backend.hf.space/api/health

# Should return: {"status":"healthy","database":"connected"}
```

### Test Frontend
- [ ] Visit: `https://your-project.vercel.app`
- [ ] Check dashboard loads
- [ ] Check web form works

### Test Channels

**WhatsApp:**
- [ ] Send message to Twilio number
- [ ] Join sandbox: `join <code>`
- [ ] Send test: "Hello, I need help"
- [ ] Receive AI response

**Web Form:**
- [ ] Go to `/web-form`
- [ ] Submit test inquiry
- [ ] Check dashboard for new conversation

**Gmail:**
- [ ] Send email to support address
- [ ] Wait 60 seconds
- [ ] Check for AI response
- [ ] Verify in dashboard

---

## 📊 Monitoring

### Backend Logs
- [ ] Hugging Face Space → Logs tab
- [ ] Monitor for errors

### Frontend Logs
- [ ] Vercel Dashboard → Logs tab
- [ ] Check for API errors

### Database
- [ ] Neon/Supabase dashboard
- [ ] Monitor connections and queries

---

## 🐛 Common Issues

### Backend won't start
- Check all secrets are set correctly
- Verify DATABASE_URL format includes `?sslmode=require`
- Check Logs tab for specific errors

### Frontend can't connect to backend
- Verify NEXT_PUBLIC_BACKEND_URL is correct
- Check backend health endpoint works
- Look for CORS errors in browser console

### WhatsApp not responding
- Verify webhook URL is correct
- Check Twilio credentials in secrets
- Test webhook manually with curl

### Gmail not working
- Verify GMAIL_CREDENTIALS_JSON is valid JSON (no line breaks)
- Check token.json is uploaded
- Verify ENABLE_EMAIL_POLLING=true

---

## ✅ Deployment Complete!

Your TaskFlow AI is now live! 🎉

**URLs:**
- Frontend: `https://your-project.vercel.app`
- Backend: `https://YOUR_USERNAME-taskflow-ai-backend.hf.space`
- Dashboard: `https://your-project.vercel.app/dashboard`
- Web Form: `https://your-project.vercel.app/web-form`

**Next Steps:**
1. Monitor dashboard for incoming conversations
2. Adjust AI prompts in `backend/context/` if needed
3. Scale up if traffic increases
4. Add more channels as needed

**Support:**
- Check DEPLOYMENT_GUIDE.md for detailed instructions
- Review logs for troubleshooting
- Test each channel individually

Happy deploying! 🚀

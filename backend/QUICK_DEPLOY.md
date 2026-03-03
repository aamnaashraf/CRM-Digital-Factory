# ⚡ Quick Deploy Guide - 15 Minutes to Production

## 🎯 Goal
Deploy TaskFlow AI to production in 3 simple steps using free tiers.

---

## Step 1: Database (2 minutes)

### Neon.tech (Recommended)
1. Visit: https://neon.tech
2. Sign up → Create Project → Name: `taskflow-ai`
3. Copy connection string (looks like):
   ```
   postgresql://user:pass@ep-xxx.us-east-2.aws.neon.tech/neondb?sslmode=require
   ```
4. Save it for Step 2

---

## Step 2: Backend - Hugging Face Spaces (10 minutes)

### 2.1 Create Space
1. Visit: https://huggingface.co/spaces
2. Click "Create new Space"
3. Settings:
   - Name: `taskflow-ai-backend`
   - SDK: **Docker**
   - Hardware: **CPU basic** (free)
4. Click "Create Space"

### 2.2 Upload Files
```bash
cd backend
git init
git remote add space https://huggingface.co/spaces/YOUR_USERNAME/taskflow-ai-backend
git add .
git commit -m "Deploy backend"
git push space main
```

### 2.3 Add Secrets (Space Settings → Repository secrets)
**Required:**
```
DATABASE_URL=postgresql://user:pass@host/db?sslmode=require
OPENAI_API_KEY=sk-...
APP_ENV=production
API_PORT=7860
USE_SIMPLE_CONFIG=false
```

**For WhatsApp:**
```
TWILIO_ACCOUNT_SID=AC...
TWILIO_AUTH_TOKEN=...
TWILIO_WHATSAPP_NUMBER=whatsapp:+14155238886
```

**For Email:**
```
GMAIL_CREDENTIALS_JSON={"installed":{...}}
ENABLE_EMAIL_POLLING=true
```

### 2.4 Wait for Build
- Go to "Logs" tab
- Wait for "Running on http://0.0.0.0:7860" (~3-5 min)
- Your backend URL: `https://YOUR_USERNAME-taskflow-ai-backend.hf.space`

### 2.5 Test
```bash
curl https://YOUR_USERNAME-taskflow-ai-backend.hf.space/api/health
```

---

## Step 3: Frontend - Vercel (3 minutes)

### 3.1 Deploy
1. Visit: https://vercel.com
2. Click "Add New Project"
3. Import your GitHub repo
4. Settings:
   - Framework: **Next.js** (auto-detected)
   - Root Directory: **frontend**
5. Add Environment Variable:
   - Key: `NEXT_PUBLIC_BACKEND_URL`
   - Value: `https://YOUR_USERNAME-taskflow-ai-backend.hf.space`
6. Click "Deploy"

### 3.2 Done!
- Frontend URL: `https://your-project.vercel.app`
- Dashboard: `https://your-project.vercel.app/dashboard`
- Web Form: `https://your-project.vercel.app/web-form`

---

## 🔗 Connect Twilio (Optional - 1 minute)

1. Go to: https://console.twilio.com/
2. Messaging → WhatsApp Sandbox
3. Set webhook: `https://YOUR_USERNAME-taskflow-ai-backend.hf.space/api/webhooks/whatsapp`
4. Method: POST
5. Save

---

## ✅ Test Everything

### Health Check
```bash
curl https://YOUR_USERNAME-taskflow-ai-backend.hf.space/api/health
```

### Web Form
1. Go to: `https://your-project.vercel.app/web-form`
2. Submit test inquiry
3. Check dashboard

### WhatsApp (if configured)
1. Send message to Twilio number
2. Join sandbox: `join <code>`
3. Send: "Hello"
4. Get AI response

### Dashboard
1. Go to: `https://your-project.vercel.app/dashboard`
2. See conversations, stats, analytics

---

## 🎉 You're Live!

Your AI customer success agent is now handling inquiries 24/7!

**Costs:**
- Hugging Face: FREE
- Vercel: FREE
- Neon.tech: FREE
- OpenAI: ~$0.002/conversation
- Total: ~$5-20/month

**Need help?**
- Full guide: `DEPLOYMENT_GUIDE.md`
- Checklist: `DEPLOYMENT_CHECKLIST.md`
- Local dev: `LOCAL_DEVELOPMENT.md`

---

## 🐛 Troubleshooting

**Backend won't start:**
- Check all secrets are set
- Verify DATABASE_URL format
- Check Logs tab

**Frontend can't connect:**
- Verify NEXT_PUBLIC_BACKEND_URL
- Test backend health endpoint
- Check browser console

**Channels not working:**
- WhatsApp: Check webhook URL
- Email: Verify Gmail credentials
- Web Form: Test backend directly

---

**Ready? Start with Step 1!** 🚀

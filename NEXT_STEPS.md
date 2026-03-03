# 🎯 NEXT STEPS - Deploy Your App

## You Are Here: ✅ Setup Complete

Your project is ready to deploy! Follow these steps in order.

---

## Step 1: Deploy Backend (10 minutes)

### Quick Method:
```bash
cd backend
bash deploy.sh
```

The script will guide you through:
1. Checking all files are present
2. Pushing to Hugging Face Spaces
3. Showing you what secrets to add

### Manual Method:
```bash
cd backend
git init
git remote add space https://huggingface.co/spaces/YOUR_USERNAME/taskflow-ai-backend
git add .
git commit -m "Deploy backend"
git push space main
```

Then add secrets in Space Settings → Repository secrets:
- `DATABASE_URL` (from Neon.tech)
- `OPENAI_API_KEY`
- `TWILIO_ACCOUNT_SID`, `TWILIO_AUTH_TOKEN`, `TWILIO_WHATSAPP_NUMBER`
- `GMAIL_CREDENTIALS_JSON`
- `APP_ENV=production`
- `API_PORT=7860`
- `USE_SIMPLE_CONFIG=false`
- `ENABLE_EMAIL_POLLING=true`

**Your backend URL will be:**
```
https://YOUR_USERNAME-taskflow-ai-backend.hf.space
```

---

## Step 2: Deploy Frontend (3 minutes)

### Via Vercel Dashboard:
1. Go to https://vercel.com
2. Click "Add New Project"
3. Import your GitHub repo
4. Set Root Directory: `frontend`
5. Add environment variable:
   - Key: `NEXT_PUBLIC_BACKEND_URL`
   - Value: `https://YOUR_USERNAME-taskflow-ai-backend.hf.space`
6. Click "Deploy"

### Via Vercel CLI:
```bash
cd frontend
npm install -g vercel
vercel login
vercel
```

**Your frontend URL will be:**
```
https://your-project.vercel.app
```

---

## Step 3: Connect Twilio Webhook (1 minute)

1. Go to https://console.twilio.com/
2. Messaging → WhatsApp Sandbox
3. Set webhook URL:
   ```
   https://YOUR_USERNAME-taskflow-ai-backend.hf.space/api/webhooks/whatsapp
   ```
4. Method: POST
5. Save

---

## Step 4: Test Everything (2 minutes)

### Test Backend:
```bash
curl https://YOUR_USERNAME-taskflow-ai-backend.hf.space/api/health
```

Should return:
```json
{"status":"healthy","database":"connected"}
```

### Test Frontend:
Visit: `https://your-project.vercel.app`

### Test Web Form:
1. Go to: `https://your-project.vercel.app/web-form`
2. Submit test inquiry
3. Check dashboard for new conversation

### Test WhatsApp:
1. Send message to Twilio number
2. Join sandbox: `join <code>`
3. Send: "Hello"
4. Get AI response

### Test Dashboard:
Visit: `https://your-project.vercel.app/dashboard`

---

## 🎉 You're Live!

Once all tests pass, your AI customer success agent is handling inquiries 24/7!

**Your URLs:**
- Backend API: `https://YOUR_USERNAME-taskflow-ai-backend.hf.space`
- Frontend: `https://your-project.vercel.app`
- Dashboard: `https://your-project.vercel.app/dashboard`
- Web Form: `https://your-project.vercel.app/web-form`

---

## 📚 Documentation Reference

- **Quick Deploy:** `QUICK_DEPLOY.md` (15-min guide)
- **Complete Guide:** `DEPLOYMENT_GUIDE.md` (detailed instructions)
- **Checklist:** `DEPLOYMENT_CHECKLIST.md` (step-by-step)
- **Local Dev:** `LOCAL_DEVELOPMENT.md` (run locally)
- **Backend:** `backend/README.md` (backend-specific)
- **Frontend:** `frontend/README.md` (frontend-specific)

---

## 🐛 Troubleshooting

**Backend won't start:**
- Check all secrets are set in HF Space settings
- Verify DATABASE_URL format includes `?sslmode=require`
- Check Logs tab for specific errors

**Frontend can't connect:**
- Verify NEXT_PUBLIC_BACKEND_URL is correct
- Test backend health endpoint
- Check browser console for errors

**Channels not working:**
- WhatsApp: Verify webhook URL in Twilio
- Email: Check Gmail credentials and token
- Web Form: Test backend endpoint directly

---

## 💰 Costs

- Hugging Face Spaces: **FREE**
- Vercel: **FREE**
- Neon.tech: **FREE**
- OpenAI API: **~$0.002/conversation**
- Twilio: **~$0.005/message**

**Total: ~$5-20/month** depending on usage

---

## 🚀 Ready to Deploy?

Start with Step 1 above, or run:
```bash
cd backend
bash deploy.sh
```

Good luck! 🎉

#!/bin/bash

# 🚀 DEPLOYMENT SCRIPT - Run this to deploy your backend to Hugging Face Spaces

echo "╔══════════════════════════════════════════════════════════════╗"
echo "║                                                              ║"
echo "║   🚀 TaskFlow AI - Backend Deployment to HF Spaces         ║"
echo "║                                                              ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""

# Check if we're in the backend folder
if [ ! -f "Dockerfile" ] || [ ! -f "requirements.txt" ]; then
    echo "❌ Error: Please run this script from the backend/ folder"
    echo "   cd backend && bash deploy.sh"
    exit 1
fi

echo "📋 Pre-deployment Checklist:"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Check for required files
echo "✓ Checking required files..."
files=("Dockerfile" "requirements.txt" "src/main.py" "alembic.ini")
for file in "${files[@]}"; do
    if [ -f "$file" ]; then
        echo "  ✅ $file"
    else
        echo "  ❌ $file - MISSING!"
        exit 1
    fi
done
echo ""

echo "📝 Before deploying, make sure you have:"
echo "  1. Created a Hugging Face account at https://huggingface.co"
echo "  2. Created a new Space with Docker SDK"
echo "  3. Have your Space URL ready"
echo ""

read -p "Have you created your Hugging Face Space? (y/n): " -n 1 -r
echo ""
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo ""
    echo "Please create your Space first:"
    echo "  1. Go to https://huggingface.co/spaces"
    echo "  2. Click 'Create new Space'"
    echo "  3. Name: taskflow-ai-backend"
    echo "  4. SDK: Docker"
    echo "  5. Hardware: CPU basic (free)"
    echo ""
    exit 1
fi

echo ""
read -p "Enter your Hugging Face username: " HF_USERNAME
echo ""

if [ -z "$HF_USERNAME" ]; then
    echo "❌ Username cannot be empty"
    exit 1
fi

SPACE_URL="https://huggingface.co/spaces/$HF_USERNAME/taskflow-ai-backend"

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🚀 Deploying to: $SPACE_URL"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Initialize git if not already
if [ ! -d ".git" ]; then
    echo "📦 Initializing git repository..."
    git init
    echo ""
fi

# Add remote
echo "🔗 Adding Hugging Face remote..."
git remote remove space 2>/dev/null
git remote add space https://huggingface.co/spaces/$HF_USERNAME/taskflow-ai-backend
echo ""

# Stage files
echo "📝 Staging files..."
git add .
echo ""

# Commit
echo "💾 Creating commit..."
git commit -m "Deploy TaskFlow AI backend to Hugging Face Spaces" || echo "No changes to commit"
echo ""

# Push
echo "🚀 Pushing to Hugging Face Spaces..."
echo ""
echo "⚠️  You may be prompted for your Hugging Face credentials:"
echo "   Username: $HF_USERNAME"
echo "   Password: Use your HF Access Token (not your password!)"
echo "   Get token from: https://huggingface.co/settings/tokens"
echo ""

git push space main || git push space master

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ Code pushed to Hugging Face Spaces!"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "🔧 NEXT STEPS:"
echo ""
echo "1. Go to your Space: $SPACE_URL"
echo ""
echo "2. Click 'Settings' tab"
echo ""
echo "3. Add these Repository secrets:"
echo "   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "   DATABASE_URL=postgresql://user:pass@host/db?sslmode=require"
echo "   OPENAI_API_KEY=sk-..."
echo "   APP_ENV=production"
echo "   API_PORT=7860"
echo "   USE_SIMPLE_CONFIG=false"
echo "   TWILIO_ACCOUNT_SID=AC..."
echo "   TWILIO_AUTH_TOKEN=..."
echo "   TWILIO_WHATSAPP_NUMBER=whatsapp:+14155238886"
echo "   GMAIL_CREDENTIALS_JSON={\"installed\":{...}}"
echo "   ENABLE_EMAIL_POLLING=true"
echo "   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "4. Wait for build to complete (3-5 minutes)"
echo "   - Check 'Logs' tab for progress"
echo "   - Look for: 'Running on http://0.0.0.0:7860'"
echo ""
echo "5. Test your backend:"
echo "   curl https://$HF_USERNAME-taskflow-ai-backend.hf.space/api/health"
echo ""
echo "6. Your backend URL for frontend:"
echo "   https://$HF_USERNAME-taskflow-ai-backend.hf.space"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "📚 Need help? Check:"
echo "   - README.md in this folder"
echo "   - ../DEPLOYMENT_GUIDE.md for complete guide"
echo "   - ../QUICK_DEPLOY.md for quick reference"
echo ""
echo "🎉 Happy deploying!"
echo ""

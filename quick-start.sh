#!/bin/bash

# Quick Start Script for Local Development
# Run this to set up and start both backend and frontend

set -e

echo "🚀 TaskFlow AI - Quick Start"
echo "=============================="
echo ""

# Check if we're in the right directory
if [ ! -d "backend" ] || [ ! -d "frontend" ]; then
    echo "❌ Error: Please run this script from the project root directory"
    exit 1
fi

# Backend setup
echo "📦 Setting up backend..."
cd backend

if [ ! -d "venv" ]; then
    echo "  Creating virtual environment..."
    python -m venv venv
fi

echo "  Activating virtual environment..."
source venv/bin/activate 2>/dev/null || source venv/Scripts/activate 2>/dev/null || {
    echo "  ⚠️  Could not activate venv automatically. Please activate manually:"
    echo "     macOS/Linux: source backend/venv/bin/activate"
    echo "     Windows: backend\\venv\\Scripts\\activate"
}

if [ ! -f ".env" ]; then
    echo "  Creating .env file from template..."
    cp .env.example .env
    echo "  ⚠️  Please edit backend/.env with your credentials before starting!"
fi

echo "  Installing Python dependencies..."
pip install -q -r requirements.txt

cd ..

# Frontend setup
echo ""
echo "📦 Setting up frontend..."
cd frontend

if [ ! -d "node_modules" ]; then
    echo "  Installing Node dependencies..."
    npm install
fi

if [ ! -f ".env.local" ]; then
    echo "  Creating .env.local..."
    echo "NEXT_PUBLIC_BACKEND_URL=http://localhost:7860" > .env.local
fi

cd ..

echo ""
echo "✅ Setup complete!"
echo ""
echo "📝 Next steps:"
echo "  1. Edit backend/.env with your credentials (DATABASE_URL, OPENAI_API_KEY, etc.)"
echo "  2. Run database migrations: cd backend && alembic upgrade head"
echo "  3. Start backend: cd backend && python -m uvicorn src.main:app --host 0.0.0.0 --port 7860 --reload"
echo "  4. Start frontend (in new terminal): cd frontend && npm run dev"
echo ""
echo "📚 Documentation:"
echo "  - LOCAL_DEVELOPMENT.md - Complete local setup guide"
echo "  - DEPLOYMENT_GUIDE.md - Production deployment guide"
echo "  - DEPLOYMENT_CHECKLIST.md - Quick deployment checklist"
echo ""
echo "🌐 URLs:"
echo "  - Backend: http://localhost:7860"
echo "  - Frontend: http://localhost:3000"
echo "  - Dashboard: http://localhost:3000/dashboard"
echo "  - Web Form: http://localhost:3000/web-form"
echo ""

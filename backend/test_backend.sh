#!/bin/bash

# TaskFlow AI - Backend Health Check Script
# Tests if backend is running and all endpoints are accessible

BACKEND_URL="${1:-http://localhost:7860}"

echo "🔍 Testing TaskFlow AI Backend at: $BACKEND_URL"
echo "================================================"
echo ""

# Test 1: Health Check
echo "✓ Testing health endpoint..."
HEALTH_RESPONSE=$(curl -s "$BACKEND_URL/api/health")
if [ $? -eq 0 ]; then
    echo "  ✅ Health check passed"
    echo "  Response: $HEALTH_RESPONSE"
else
    echo "  ❌ Health check failed"
    exit 1
fi
echo ""

# Test 2: Root endpoint
echo "✓ Testing root endpoint..."
ROOT_RESPONSE=$(curl -s "$BACKEND_URL/")
if [ $? -eq 0 ]; then
    echo "  ✅ Root endpoint accessible"
    echo "  Response: $ROOT_RESPONSE"
else
    echo "  ❌ Root endpoint failed"
fi
echo ""

# Test 3: Dashboard stats
echo "✓ Testing dashboard stats..."
STATS_RESPONSE=$(curl -s "$BACKEND_URL/api/dashboard/metrics")
if [ $? -eq 0 ]; then
    echo "  ✅ Dashboard stats accessible"
else
    echo "  ❌ Dashboard stats failed"
fi
echo ""

# Test 4: Activity feed
echo "✓ Testing activity feed..."
ACTIVITY_RESPONSE=$(curl -s "$BACKEND_URL/api/dashboard/activity")
if [ $? -eq 0 ]; then
    echo "  ✅ Activity feed accessible"
else
    echo "  ❌ Activity feed failed"
fi
echo ""

echo "================================================"
echo "✅ Backend health check complete!"
echo ""
echo "📝 Available endpoints:"
echo "  - Health: $BACKEND_URL/api/health"
echo "  - Dashboard: $BACKEND_URL/api/dashboard/metrics"
echo "  - Activity: $BACKEND_URL/api/dashboard/activity"
echo "  - WhatsApp Webhook: $BACKEND_URL/api/webhooks/whatsapp"
echo "  - Email Webhook: $BACKEND_URL/api/webhooks/email"
echo "  - Web Form: $BACKEND_URL/api/webhooks/web-form"
echo ""

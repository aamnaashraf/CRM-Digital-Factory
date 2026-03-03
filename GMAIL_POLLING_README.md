# Gmail Email Polling Feature - Testing Instructions

## Overview
This update adds robust Gmail polling functionality to properly handle inbound customer emails and distinguish them from emails sent by the support system.

## Key Changes Made

1. **Fixed Email Filtering**:
   - Improved query to exclude emails from the support address: `is:unread in:inbox -from:aamnaashraf501@gmail.com`
   - Added secondary validation to ensure emails are from customers, not internal

2. **Automatic Background Polling**:
   - Continuous polling runs in the background every 60 seconds (configurable)
   - Processes inbound emails into the ticket system with `channel="email"`
   - Automatically marks processed emails as read

3. **Email Processing**:
   - Creates tickets with proper channel metadata (channel="email")
   - Maintains conversation threads when replying
   - Applies agent processing for responses

## Configuration Settings

- `POLL_INTERVAL_SECONDS=60` - How often to check for new emails (default: 60 seconds)
- `ENABLE_EMAIL_POLLING=true` - Whether to enable background polling (default: true)

## Testing Steps

### 1. Start the Application
```bash
python run_simple.py
```

### 2. Verify Polling is Running
Check the startup logs for:
```
Starting Gmail polling task...
Gmail polling started with interval: 60s
```

You can also check the polling status via API:
```bash
curl http://localhost:8000/api/webhooks/gmail/poll/status
```

### 3. Send Test Email
Send an email from another Gmail account to: `aamnaashraf501@gmail.com`

### 4. Wait for Processing
- Wait up to 60 seconds (or your configured polling interval)
- The system will automatically process the email

### 5. Check Results
#### Check Database:
```bash
python check_email_processing_fixed.py
```

Look for:
- New conversation with `Channel: email`
- Customer email address as the `Customer` field
- Correct `Subject` from the email

#### Check Dashboard:
- Visit the dashboard at `http://localhost:3000`
- The new ticket should show `Channel: email` (not "web")

### 6. Manual Polling (Optional)
If you want to trigger polling immediately without waiting:
```bash
curl -X POST http://localhost:8000/api/webhooks/gmail/poll
```

### 7. Manual Test Script
You can also run the manual test script:
```bash
python test_email_polling.py
```

## Additional Endpoints

- `POST /api/webhooks/gmail/poll` - Manually trigger email polling
- `GET /api/webhooks/gmail/poll/status` - Check polling status
- `POST /api/webhooks/gmail/setup-push` - Setup push notifications (if available)

## What Happens When an Email Arrives

1. **Polling Cycle**: Every 60 seconds, the system checks for unread emails
2. **Filtering**: Only emails not from `aamnaashraf501@gmail.com` are processed
3. **Database**: Creates conversation with `channel="email"`
4. **Agent Processing**: AI processes the email and generates response
5. **Reply**: Response sent back to customer via Gmail API
6. **Mark Read**: Email is marked as read to prevent reprocessing

## Troubleshooting

- If emails aren't appearing in dashboard as "email" channel, verify the email was sent from a different address
- Check application logs for polling activity
- Ensure Gmail API credentials are correctly configured
- Verify `gmail-token.json` file exists and has proper permissions
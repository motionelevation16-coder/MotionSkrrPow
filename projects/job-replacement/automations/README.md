# Motion Elevation — n8n Automation Library

**Plug-and-play automations for done-for-you AI automation clients.**  
Each workflow deploys in under 60 minutes. No code required after setup.

---

## 🚀 Quick Start

1. Open your n8n instance
2. Click **Import** → paste the JSON file content
3. Follow the setup checklist for that workflow (see below)
4. Replace all `REPLACE_WITH_*` placeholders with real values
5. Set up credentials in n8n Settings → Credentials
6. Toggle the workflow **Active**
7. Test with a manual execution first

---

## 📦 Workflow Library

### 01 — Email Triage + Auto-Reply
**File:** `01-email-triage-autoreply.json`  
**Deploy time:** ~30 minutes  
**Category:** Email Automation

**What it does:**
- Polls inbox every 5 minutes for unread emails
- Classifies each email as URGENT, NORMAL, or LOW priority using keyword matching
- Sends a tailored auto-reply (urgent: 2-hour SLA promise / normal: 24-hour)
- Skips newsletters and no-reply addresses to prevent loops
- Logs all emails to a Google Sheet

**Credentials needed:**
- IMAP (to read emails — Gmail, Outlook, etc.)
- SMTP (to send replies)
- Google Sheets OAuth2

**Google Sheet setup:**
Create a sheet with tab `Email_Log` and columns:
`Timestamp | From | Subject | Priority | Reason | MessageID`

**Customize:**
- Edit urgency keywords in the "Classify Email Priority" node
- Edit email templates in the reply nodes
- Adjust polling interval in the Schedule Trigger

---

### 02 — Lead Capture → CRM Entry
**File:** `02-lead-capture-crm.json`  
**Deploy time:** ~45 minutes  
**Category:** Sales Automation

**What it does:**
- Receives leads from any form (Typeform, website contact, Webflow, etc.) via webhook
- Validates email and normalizes field names across form builders
- Scores the lead 0–100 based on data completeness
- Logs to Google Sheets (free CRM) AND optionally pushes to a real CRM API
- Sends instant confirmation email to the lead
- Alerts the business owner with full lead details

**Credentials needed:**
- SMTP (for confirmation + owner notification emails)
- Google Sheets OAuth2
- CRM API key (optional — delete that node if not needed)

**Google Sheet setup:**
Create a sheet with tab `Leads` and columns:
`Lead ID | Name | Email | Phone | Company | Message | Source | Score | Status | Created At`

**Webhook URL:**
After activating, copy the webhook URL from the trigger node and paste it into your form's "submission webhook" setting.

**Compatible CRMs (edit the HTTP node URL):**
- HubSpot: `https://api.hubapi.com/crm/v3/objects/contacts`
- Pipedrive: `https://api.pipedrive.com/v1/persons`
- GoHighLevel: `https://rest.gohighlevel.com/v1/contacts/`

---

### 03 — Invoice Reminder Sequence
**File:** `03-invoice-reminder.json`  
**Deploy time:** ~30 minutes  
**Category:** Finance Automation

**What it does:**
- Runs every weekday morning at 8 AM
- Reads unpaid invoices from a Google Sheet
- Sends escalating reminder emails based on days past due:
  - **-3 days:** Friendly heads-up before due date
  - **Due day:** Payment reminder
  - **+3 days:** Gentle first overdue notice
  - **+7 days:** Firmer second notice
  - **+14 days:** Urgent third notice
  - **+30 days:** Final notice (repeats every 2 weeks)
- Tracks reminder count per invoice to avoid duplicate emails
- Auto-marks invoices as "Overdue" status

**Credentials needed:**
- SMTP (to send reminders)
- Google Sheets OAuth2

**Google Sheet setup:**
Create a sheet with tab `Invoices` and columns:
`Invoice_ID | Client_Name | Client_Email | Amount | Currency | Due_Date | Status | Reminder_Count | Last_Reminder_Date`

**Status values:** `Unpaid`, `Paid`, `Overdue`, `Cancelled`  
Mark invoices as `Paid` or `Cancelled` to stop reminders.

**Customize:**
- Edit reminder thresholds in the "Filter Overdue Invoices" node
- Edit email templates in the "Build Reminder Email" node
- Add late fees language to the FINAL_NOTICE template

---

### 04 — AI Customer Support Chatbot
**File:** `04-customer-support-chatbot.json`  
**Deploy time:** ~60 minutes  
**Category:** Customer Support

**What it does:**
- Receives chat messages via webhook (integrates with any chat widget)
- Detects intent: pricing, hours, refund, contact, escalate-to-human
- Routes "speak to human" requests immediately to a real agent via email
- Sends all other queries to GPT-4o-mini with a custom system prompt about the business
- Logs all conversations to Google Sheets for review and training
- Returns AI response to the chat widget in real-time

**Credentials needed:**
- OpenAI API key
- SMTP (for escalation alerts)
- Google Sheets OAuth2

**Cost:** ~$0.0001 per message (GPT-4o-mini) = $0.10 per 1,000 messages

**Google Sheet setup:**
Create tab `Chat_Log` with columns:
`Timestamp | Session_ID | Customer | Email | Intent | Customer_Message | Bot_Reply | Escalated`

**Customize (important):**
In the "AI Response (OpenAI)" node system prompt, replace:
- `[REPLACE_WITH_COMPANY_NAME]` — your company name
- `[REPLACE_WITH_COMPANY_DESCRIPTION]` — 2-3 sentence description
- `[REPLACE_WITH_HOURS]` — business hours
- `[REPLACE_WITH_FAQ_1/2/3]` — your top 3 FAQ answers

**Chat widget integration:**
POST to the webhook URL with: `{ "sessionId": "...", "message": "...", "customerName": "..." }`

---

### 05 — Meeting Booking Confirmation + Prep Flow
**File:** `05-meeting-booking-confirmation.json`  
**Deploy time:** ~45 minutes  
**Category:** Operations Automation

**What it does (two flows in one):**

**Flow A — Instant booking confirmation:**
- Receives booking webhook from Calendly, Cal.com, TidyCal, etc.
- Parses booking details (date, time, join URL) automatically
- Sends beautiful HTML confirmation email to the guest with prep tips
- Notifies the meeting host via email
- Logs booking to Google Sheets

**Flow B — Daily 24-hour reminders:**
- Runs every morning at 8 AM
- Checks Google Sheet for tomorrow's meetings
- Sends reminder emails to each guest with their join link

**Credentials needed:**
- SMTP
- Google Sheets OAuth2

**Google Sheet setup:**
Create tab `Bookings` with columns:
`Booking_ID | Guest_Name | Guest_Email | Meeting_Title | Date | Time | Timezone | Platform | Join_URL | Status | Created_At`

**Calendly setup:**
1. Go to Calendly → Integrations → Webhooks
2. Add your n8n webhook URL
3. Subscribe to `invitee.created` events

---

## 🔑 Credentials Setup Guide

### IMAP (Email reading)
- Gmail: Enable 2FA → Google Account → App Passwords → generate "Mail" password
- Outlook: Settings → Mail → IMAP access → enable it
- In n8n: Settings → Credentials → New → IMAP Email

### SMTP (Email sending)
- Gmail: Same App Password as above, SMTP host: `smtp.gmail.com`, port: `465`
- Outlook: `smtp.office365.com`, port: `587`
- In n8n: Settings → Credentials → New → SMTP

### Google Sheets OAuth2
1. Google Cloud Console → New Project → Enable Google Sheets API
2. Credentials → OAuth 2.0 Client → Web Application
3. Add your n8n URL to authorized redirect URIs
4. In n8n: Settings → Credentials → New → Google Sheets OAuth2 API

### OpenAI API
1. platform.openai.com → API Keys → Create new key
2. In n8n: Settings → Credentials → New → OpenAI API

---

## 📊 Deployment Checklist

For each workflow before going live:

- [ ] Import JSON into n8n
- [ ] Create required Google Sheet tabs with correct columns
- [ ] Set up all required credentials in n8n
- [ ] Replace ALL `REPLACE_WITH_*` placeholders in node configs
- [ ] Run a manual test execution
- [ ] Check execution logs for errors
- [ ] Toggle workflow **Active**
- [ ] Test with a real sample (send a test email, submit a test form, etc.)
- [ ] Confirm output in Google Sheet

---

## 💰 Pricing These to Clients

Suggested Motion Elevation pricing for these workflows:

| Workflow | Setup Fee | Monthly Retainer |
|----------|-----------|------------------|
| Email Triage | €297 | €97/mo |
| Lead Capture CRM | €497 | €147/mo |
| Invoice Reminder | €397 | €97/mo |
| AI Chatbot | €797 | €247/mo |
| Meeting Booking | €397 | €97/mo |
| **Full Bundle (all 5)** | **€1,497** | **€497/mo** |

---

## 🔮 What's Next

Recommended workflows to build next:
1. **Social Media Post Scheduler** — Approve content in Google Sheet → auto-post to Instagram/LinkedIn/Twitter via Buffer API
2. **E-commerce Order Notification** — Shopify webhook → WhatsApp/email order confirmation + review request 3 days later
3. **Onboarding Sequence** — New client signs up → automated 7-day email drip + task creation in project management tool

---

*Built by Motion Elevation | Version 1.0.0*

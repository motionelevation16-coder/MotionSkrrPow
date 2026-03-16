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

---

## 🆕 Workflows 12–19 (Niche Edition)

---

### 12 — Dental Clinic Patient Follow-Up + Review Requests
**File:** `12-dental-followup-review.json`  
**Deploy time:** ~45 minutes  
**Category:** Healthcare Automation  
**Suggested Price:** €597 setup + €97/month

**What it does:**
- Runs every morning at 9am scanning the Patients sheet
- **Day 1** after visit: sends post-care instructions email (medication tips, what to avoid, emergency contact)
- **Day 3**: sends a warm Google Review request (gentle, personal tone)
- **6 months**: sends a recall/rebooking reminder with booking link
- All sends are logged back to the sheet (Followup_Sent, Review_Sent, Recall_Sent = "Yes") to prevent duplicates

**Credentials needed:**
- SMTP (clinic email address)
- Google Sheets OAuth2

**Google Sheet setup:**
Create a sheet with tab `Patients` and columns:
`Name | Email | Phone | Visit_Date | Treatment | Followup_Sent | Review_Sent | Recall_Sent | Notes`

- `Visit_Date` format: YYYY-MM-DD (e.g. 2024-06-15)
- `Treatment` examples: Cleaning, Crown, Root Canal, Whitening
- Followup_Sent / Review_Sent / Recall_Sent: leave blank initially; workflow fills "Yes"

**Customize:**
- `REPLACE_WITH_CLINIC_NAME` — your practice name
- `REPLACE_WITH_CLINIC_PHONE` — for the after-care email
- `REPLACE_WITH_CLINIC_ADDRESS` — footer of all emails
- `REPLACE_WITH_GOOGLE_REVIEW_URL` — your Google Maps review link (share → copy link)
- `REPLACE_WITH_BOOKING_URL` — Calendly, Doctolib, or your booking page

**Sell this to:** Any dental clinic that isn't already doing post-visit follow-up (most aren't). A single additional crown booked from a recall email = €800+. ROI is obvious.

---

### 13 — Fitness Studio Class Reminder + Churn Prevention
**File:** `13-fitness-class-reminder-churn.json`  
**Deploy time:** ~45 minutes  
**Category:** Fitness & Wellness Automation  
**Suggested Price:** €497 setup + €97/month

**What it does:**
- Runs daily at 7am
- **Class reminder**: if a member has a class tomorrow and reminder not sent → day-before email with class details, location, cancel link
- **Churn detection**: if a member hasn't visited in 14+ days → sends "we miss you" email with free class offer
- **Low engagement**: mid-month (day 15+), if member has fewer than 4 classes attended → nudge email with schedule link
- All actions logged to sheet to prevent duplicate sends

**Credentials needed:**
- SMTP
- Google Sheets OAuth2

**Google Sheet setup:**
Tab `Members` with columns:
`Name | Email | Phone | Next_Class_Date | Next_Class_Time | Next_Class_Name | Last_Visit_Date | Membership_Type | Classes_This_Month | Reminder_Sent | Churn_Email_Sent | Status`

- Reset `Reminder_Sent` to "No" each week via a separate simple workflow or manually
- Reset `Classes_This_Month` counter at the start of each month
- `Status`: Active or Cancelled

**Customize:**
- `REPLACE_WITH_STUDIO_NAME` / `REPLACE_WITH_STUDIO_ADDRESS` / `REPLACE_WITH_STUDIO_PHONE`
- `REPLACE_WITH_CANCEL_URL` — late cancellation link
- `REPLACE_WITH_BOOKING_URL` / `REPLACE_WITH_SCHEDULE_URL`
- Edit the promo code format in the churn email (currently `COMEBACK + first 3 letters of name`)

**Sell this to:** Yoga studios, CrossFit boxes, pilates studios, gyms. Every 1% reduction in monthly churn = significant ARR. Price this confidently.

---

### 14 — Restaurant Reservation Confirmation + No-Show Follow-Up
**File:** `14-restaurant-reservation-noshow.json`  
**Deploy time:** ~60 minutes  
**Category:** Restaurant & Hospitality Automation  
**Suggested Price:** €797 setup + €127/month

**What it does:**
- **Flow A (Webhook):** Receives reservation from booking widget → logs to sheet → sends instant confirmation email with modify/cancel links → returns confirmation code
- **Flow B (Daily 10am schedule):**
  - Day-of: sends morning reminder email with address and timing
  - Next day (status still "Confirmed" = no-show): sends recovery email with rebook link + complimentary drink offer
  - Next day (status "Completed"): sends post-dinner review request for Google

**Credentials needed:**
- SMTP
- Google Sheets OAuth2

**Google Sheet setup:**
Tab `Reservations` with columns:
`Name | Email | Phone | Date | Time | Party_Size | Special_Requests | Confirmation_Code | Status | Reminder_Sent | Noshow_Followup_Sent | Review_Sent | Created_At`

- Status values: `Confirmed` (default), `Seated` (update when they arrive), `Completed` (after dinner), `No-Show` (auto-set), `Cancelled`
- Staff must update Status to "Completed" or "Seated" on the day — this is the key manual step

**Webhook setup:**
1. Activate the workflow
2. Copy the webhook URL from the "Webhook: New Reservation" node
3. Paste it into your booking system (OpenTable, Resy, or custom form)
4. Required fields: name, email, date (YYYY-MM-DD), time, party_size

**Customize:**
- `REPLACE_WITH_RESTAURANT_NAME` / `REPLACE_WITH_RESTAURANT_ADDRESS` / `REPLACE_WITH_RESTAURANT_PHONE`
- `REPLACE_WITH_GOOGLE_REVIEW_URL` — Google Maps review link
- `REPLACE_WITH_INSTAGRAM_HANDLE` — for the post-dinner email
- `REPLACE_WITH_BOOKING_URL` — for rebook links
- `REPLACE_WITH_CANCEL_URL` / `REPLACE_WITH_MODIFY_URL`

---

### 15 — Real Estate Open House Follow-Up Sequence
**File:** `15-real-estate-open-house-followup.json`  
**Deploy time:** ~60 minutes  
**Category:** Real Estate Automation  
**Suggested Price:** €997 setup + €147/month

**What it does:**
- **Webhook**: iPad sign-in at open house → automatically logs visitor, scores lead (0-100), sends instant thank-you email with property details, alerts agent (urgency flag for score 70+)
- **Daily 9am schedule:**
  - Day 3: neighbourhood insights email + similar listings
  - Day 7: urgency email with market stats + book-a-call CTA

**Lead scoring:**
- Base: 50 points
- High interest: +30, Medium: +10
- Pre-approved financing: +20
- Phone provided: +10

**Credentials needed:**
- SMTP
- Google Sheets OAuth2

**Google Sheet setup:**
Tab `Open_House_Leads` with columns:
`Name | Email | Phone | Property | Visit_Date | Interest | Preapproved | Notes | Lead_Score | Email1_Sent | Email2_Sent | Email3_Sent | Status | Created_At`

- `Interest`: high / medium / low (from sign-in form dropdown)
- `Preapproved`: yes / no
- `Status`: New, Contacted, Viewing Booked, Offer Made, Closed, Unsubscribed

**iPad sign-in setup:**
Use Tally.so (free) or Google Forms embedded on iPad. Set the form webhook URL to the n8n webhook URL. Required fields: name, email, property_address, interest_level, preapproved.

**Customize:**
- All property details (sqm, bedrooms, price, availability)
- `REPLACE_WITH_AGENT_NAME` / `REPLACE_WITH_AGENT_EMAIL` / `REPLACE_WITH_AGENT_PHONE` / `REPLACE_WITH_AGENT_LICENSE`
- `REPLACE_WITH_CALENDLY_URL` — agent's booking link
- School ratings, transport info, market data in Email 2
- Average days on market stat in Email 3

---

### 16 — Freelancer Project Update + Invoice Automation
**File:** `16-freelancer-project-invoice.json`  
**Deploy time:** ~45 minutes  
**Category:** Freelancer Automation  
**Suggested Price:** €397 setup + €67/month

**What it does:**
- Runs Mon/Wed/Fri at 9am
- **Project updates**: for any project with status "In Progress" that hasn't had an update email in 48h → sends branded progress report with % completion bar
- **Invoice reminders**: for unpaid invoices past due date → sends escalating reminders (friendly → firm → final notice), max 3 attempts
- **Completion webhook**: separate webhook that sends a project completion + delivery email when triggered

**Email escalation:**
- Reminder 1: friendly "just a reminder"
- Reminder 2: firm follow-up
- Reminder 3: final notice with consequence language

**Credentials needed:**
- SMTP
- Google Sheets OAuth2

**Google Sheet setup:**
Tab `Projects` with columns:
`Client_Name | Client_Email | Project_Name | Status | Progress_Pct | Deadline | Last_Update_Sent | Invoice_Amount | Invoice_Due_Date | Invoice_Status | Invoice_Reminder_Count | Notes`

- `Status`: In Progress, Completed, Cancelled, On-Hold
- `Progress_Pct`: 0 to 100 (no % sign)
- `Invoice_Status`: unpaid / paid
- `Invoice_Reminder_Count`: starts at 0, auto-incremented

**Customize:**
- `REPLACE_WITH_YOUR_NAME` / `REPLACE_WITH_YOUR_EMAIL` / `REPLACE_WITH_YOUR_WEBSITE`
- `REPLACE_WITH_PAYMENT_LINK` — PayPal, Stripe, IBAN transfer instructions
- `REPLACE_WITH_PAYMENT_METHODS` — "Bank transfer, PayPal, or Stripe"
- Edit notes field to include what was completed (put this in the Notes column each update cycle)

---

### 17 — Coach Session Prep + Follow-Up Drip
**File:** `17-coach-session-prep-followup.json`  
**Deploy time:** ~45 minutes  
**Category:** Coaching Automation  
**Suggested Price:** €497 setup + €97/month

**What it does:**
- Runs daily at 8am — checks the Sessions sheet for 4 types of actions:
  - **Day -1 (prep):** session is tomorrow → sends prep email with 3 reflection questions + Zoom link
  - **Day 0 (recap):** session was yesterday, status = Completed → sends recap email with action steps (pulled from Notes column)
  - **Day +3:** accountability check-in with 3 reflection prompts
  - **Day +7:** rebook nudge with next session CTA

**Credentials needed:**
- SMTP
- Google Sheets OAuth2

**Google Sheet setup:**
Tab `Sessions` with columns:
`Client_Name | Client_Email | Session_Date | Session_Time | Session_Number | Focus_Area | Goals | Prep_Email_Sent | Followup_Email_Sent | Day3_Sent | Day7_Sent | Status | Notes`

- `Session_Date`: YYYY-MM-DD format
- `Status`: Scheduled / Completed / Cancelled / No-Show
- `Notes`: coach fills these in after each session — these appear in the recap email
- `Focus_Area`: e.g. "Confidence", "Business growth", "Relationships"

**Key workflow:**
1. Coach logs new session in sheet (Status: Scheduled)
2. Prep email auto-sends the day before
3. Coach marks Status = "Completed" after session, fills in Notes
4. Recap email auto-sends next morning
5. Day 3 and Day 7 emails auto-send on schedule

**Customize:**
- `REPLACE_WITH_COACH_NAME` / `REPLACE_WITH_COACH_EMAIL` / `REPLACE_WITH_COACH_WEBSITE`
- `REPLACE_WITH_ZOOM_LINK` — fixed Zoom personal room link, or use dynamic booking URL
- `REPLACE_WITH_BOOKING_URL` — Calendly for rebook CTA

---

### 18 — E-Commerce Review Request + Upsell Sequence
**File:** `18-ecommerce-review-upsell.json`  
**Deploy time:** ~60 minutes  
**Category:** E-Commerce Automation  
**Suggested Price:** €697 setup + €127/month

**What it does:**
- **Flow A (Order shipped webhook):** Logs order → sends shipping confirmation with tracking link
- **Flow B (Daily 10am):**
  - Day 5 after shipping: review request email with star rating visual + complaint safety net ("not happy? just reply")
  - Day 7: upsell email with 2 recommended products + 10% loyalty discount code

**Credentials needed:**
- SMTP
- Google Sheets OAuth2

**Google Sheet setup:**
Tab `Orders` with columns:
`Customer_Name | Customer_Email | Order_ID | Order_Total | Product_Name | Product_Category | Tracking_URL | Shipped_At | Review_Sent | Upsell_Sent`

**Shopify webhook setup:**
1. Shopify Admin → Settings → Notifications → Webhooks
2. Event: "Order fulfilled" (when shipping label is created)
3. URL: your n8n webhook URL
4. Format: JSON
5. Map Shopify fields to expected webhook body fields in the Parse node

**WooCommerce webhook setup:**
1. WooCommerce → Settings → Advanced → Webhooks → Add webhook
2. Event: "Order updated" → Status: Shipped/Completed
3. Delivery URL: your n8n webhook

**Customize:**
- `REPLACE_WITH_STORE_EMAIL` — your store's sending address
- `REPLACE_WITH_REVIEW_URL` — your Google/Trustpilot/product review link
- `REPLACE_WITH_UPSELL_PRODUCT_*` — set 2 complementary products with names, descriptions, prices, and URLs
- `REPLACE_WITH_DELIVERY_ESTIMATE` — "3–5 business days"
- Discount code: currently "THANKYOU10" — change in the upsell email node

---

### 19 — Legal Intake Form → CRM → Client Onboarding
**File:** `19-legal-intake-crm-onboarding.json`  
**Deploy time:** ~60 minutes  
**Category:** Legal Automation  
**Suggested Price:** €1,197 setup + €197/month

**What it does:**
- **Flow A (Intake webhook):**
  - Receives form submission → parses and classifies (urgent vs standard based on matter type + urgency flag)
  - Logs to Intake CRM sheet with reference number
  - Sends professional acknowledgment email to prospective client
  - Alerts attorney by email (urgent matters get red flag + "contact within 2 hours" notice)
  - Returns confirmation JSON to the form

- **Flow B (Client accepted webhook):**
  - Triggered when attorney accepts a client (after consultation)
  - Sends full onboarding email: engagement agreement link, retainer payment, client information form, document checklist
  - Updates CRM status to "Active Client"

**Credentials needed:**
- SMTP (professional firm email address)
- Google Sheets OAuth2

**Google Sheet setup:**
Tab `Intake_CRM` with columns:
`Intake_Ref | Full_Name | Email | Phone | Matter_Type | Description | Urgency | Priority | Preferred_Contact | How_Heard | Status | Acknowledgment_Sent | Consultation_Booked | Onboarding_Sent | Created_At`

- `Priority`: auto-set by workflow (urgent / standard)
- `Status`: New Inquiry → Consultation Scheduled → Active Client → Closed
- `Urgency`: field from the intake form (urgent / normal)

**Matter type urgency triggers:**
The workflow auto-flags "urgent" for matters containing: criminal, custody, DUI, injunction, restraining order. Edit in the Parse & Classify node.

**Intake form setup (Typeform recommended):**
Questions to ask:
1. Full name
2. Email address
3. Phone number
4. Type of matter (dropdown): Criminal, Family, Property, Employment, Business, Immigration, Other
5. Briefly describe your situation (text area)
6. How urgently do you need help? (dropdown: urgent / within 2 weeks / within a month)
7. Preferred contact method (email / phone / either)
8. How did you hear about us?

**Customize:**
- `REPLACE_WITH_FIRM_NAME` / `REPLACE_WITH_FIRM_EMAIL` / `REPLACE_WITH_FIRM_ADDRESS` / `REPLACE_WITH_FIRM_PHONE`
- `REPLACE_WITH_ATTORNEY_EMAIL` — where the intake alert goes
- `REPLACE_WITH_PARALEGAL_NAME` / `REPLACE_WITH_PARALEGAL_EMAIL` — ongoing point of contact
- `REPLACE_WITH_ENGAGEMENT_AGREEMENT_URL` — DocuSign, HelloSign, or PDF link
- `REPLACE_WITH_CLIENT_INFO_FORM_URL` — detailed client intake questionnaire
- `REPLACE_WITH_PAYMENT_URL` — retainer payment link (Stripe, bank transfer page)

**Compliance note:** Advise legal clients to have their attorney review the email templates to ensure they comply with local bar association advertising rules and privilege disclaimers.

---

## 💰 Updated Pricing Table (Workflows 12–19)

| Workflow | Niche | Setup Fee | Monthly |
|----------|-------|-----------|---------|
| 12 — Dental Follow-Up | Healthcare | €597 | €97/mo |
| 13 — Fitness Churn Prevention | Wellness | €497 | €97/mo |
| 14 — Restaurant Reservations | Hospitality | €797 | €127/mo |
| 15 — Real Estate Open House | Property | €997 | €147/mo |
| 16 — Freelancer Invoicing | Freelancers | €397 | €67/mo |
| 17 — Coach Session Drip | Coaching | €497 | €97/mo |
| 18 — E-Commerce Post-Purchase | Retail | €697 | €127/mo |
| 19 — Legal Intake → CRM | Legal | €1,197 | €197/mo |

**Bundle deals to offer:**
- Any 3 workflows: 20% off setup
- Healthcare bundle (12 + fitness): €997 setup
- Professional services bundle (16 + 17 + 19): €1,797 setup

---

*Workflows 12–19 built by Motion Elevation | Version 1.0.0*

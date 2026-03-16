# n8n Lead Capture Workflow Spec
**Tally.so → Score → Brevo → Welcome Email → VIP Alert**

---

## Overview

This workflow automatically handles every new lead that submits your Tally.so form:

```
Tally Form Submission
        ↓
  Score the Lead
        ↓
Add to Brevo List
        ↓
Send Welcome Email
        ↓
  High Value? → Notify Lyubo (Telegram/Slack)
```

---

## Prerequisites

Before importing the workflow, you need:

1. **Tally.so account** with a form created
2. **Brevo account** with an API key (see `brevo-setup.md`)
3. **Brevo email list ID** (you'll get this after creating a list)
4. **Telegram Bot Token** (from @BotFather) OR Slack Webhook URL
5. **n8n running** at http://13.62.48.252:5678

---

## Workflow Nodes (Detailed Spec)

### Node 1: Webhook (Trigger)
- **Type:** Webhook
- **HTTP Method:** POST
- **Path:** `/tally-lead` (auto-generates full URL)
- **Full URL will be:** `http://13.62.48.252:5678/webhook/tally-lead`
- **Response Mode:** Immediately (respond with 200 OK right away)

**What it captures from Tally:**
Tally sends JSON like this when someone submits your form:
```json
{
  "eventType": "FORM_RESPONSE",
  "data": {
    "fields": [
      { "label": "Full Name", "value": "John Smith" },
      { "label": "Email", "value": "john@example.com" },
      { "label": "What's your budget?", "value": "€1000-5000" },
      { "label": "How soon do you want to start?", "value": "This month" },
      { "label": "What service are you interested in?", "value": "Full automation setup" }
    ]
  }
}
```

---

### Node 2: Set Variables (Extract Fields)
- **Type:** Set
- **Purpose:** Pull out individual fields for easier use downstream

Extracts:
```
name     = {{ $json.data.fields[0].value }}
email    = {{ $json.data.fields[1].value }}
budget   = {{ $json.data.fields[2].value }}
timeline = {{ $json.data.fields[3].value }}
service  = {{ $json.data.fields[4].value }}
```

> 💡 Adjust field indexes to match your actual Tally form order

---

### Node 3: Code (Lead Scoring)
- **Type:** Code (JavaScript)
- **Purpose:** Calculate a score from 0–100 based on form answers

**Scoring Logic:**
```javascript
const budget = $input.first().json.budget || '';
const timeline = $input.first().json.timeline || '';
const service = $input.first().json.service || '';

let score = 0;

// Budget scoring (0-40 points)
if (budget.includes('10000') || budget.includes('10k+')) score += 40;
else if (budget.includes('5000') || budget.includes('5k')) score += 30;
else if (budget.includes('1000') || budget.includes('1k')) score += 20;
else if (budget.includes('500')) score += 10;
else score += 5; // "Not sure" or low budget

// Timeline scoring (0-30 points)
if (timeline.toLowerCase().includes('this week') || timeline.toLowerCase().includes('asap')) score += 30;
else if (timeline.toLowerCase().includes('this month')) score += 20;
else if (timeline.toLowerCase().includes('3 month')) score += 10;
else score += 5;

// Service scoring (0-30 points)
if (service.toLowerCase().includes('full') || service.toLowerCase().includes('complete')) score += 30;
else if (service.toLowerCase().includes('automation')) score += 20;
else score += 10;

// Determine tier
let tier, tag;
if (score >= 70) { tier = 'HIGH'; tag = 'vip-lead'; }
else if (score >= 40) { tier = 'MEDIUM'; tag = 'warm-lead'; }
else { tier = 'LOW'; tag = 'cold-lead'; }

return [{ json: { ...$input.first().json, score, tier, tag } }];
```

**Output adds to the data:**
```
score: 75
tier:  "HIGH"
tag:   "vip-lead"
```

---

### Node 4: HTTP Request (Add to Brevo)
- **Type:** HTTP Request
- **Method:** POST
- **URL:** `https://api.brevo.com/v3/contacts`
- **Headers:**
  - `api-key: YOUR_BREVO_API_KEY`
  - `Content-Type: application/json`
- **Body:**
```json
{
  "email": "={{ $json.email }}",
  "attributes": {
    "FIRSTNAME": "={{ $json.name.split(' ')[0] }}",
    "LASTNAME": "={{ $json.name.split(' ')[1] || '' }}",
    "LEAD_SCORE": "={{ $json.score }}",
    "LEAD_TIER": "={{ $json.tier }}"
  },
  "listIds": [YOUR_LIST_ID],
  "tags": ["={{ $json.tag }}", "tally-form"],
  "updateEnabled": true
}
```

> Replace `YOUR_LIST_ID` with the numeric ID from your Brevo list (e.g., `3`)

---

### Node 5: HTTP Request (Send Welcome Email via Brevo)
- **Type:** HTTP Request
- **Method:** POST
- **URL:** `https://api.brevo.com/v3/smtp/email`
- **Headers:**
  - `api-key: YOUR_BREVO_API_KEY`
  - `Content-Type: application/json`
- **Body:**
```json
{
  "sender": {
    "name": "Lyubo at Motion Elevation",
    "email": "hello@yourdomain.com"
  },
  "to": [{ "email": "={{ $json.email }}", "name": "={{ $json.name }}" }],
  "subject": "Welcome to Motion Elevation — here's what happens next",
  "htmlContent": "<h2>Hey {{ params.name }},</h2><p>Thanks for reaching out! I got your message and I'll personally review your details.</p><p>Expect to hear from me within <strong>24–48 hours</strong>.</p><p>In the meantime, check out what we do at <a href='https://yourdomain.com'>Motion Elevation</a>.</p><p>Talk soon,<br>Lyubo</p>",
  "params": {
    "name": "={{ $json.name.split(' ')[0] }}"
  }
}
```

---

### Node 6: IF (High-Value Filter)
- **Type:** IF
- **Condition:** `{{ $json.tier }}` equals `HIGH`
- **True branch** → Send VIP alert
- **False branch** → End workflow (no notification needed)

---

### Node 7: Telegram (VIP Alert) — IF Node True Branch
- **Type:** Telegram
- **Operation:** Send Message
- **Chat ID:** Your Telegram chat ID (get it from @userinfobot)
- **Text:**
```
🔥 HIGH-VALUE LEAD ALERT

Name: {{ $json.name }}
Email: {{ $json.email }}
Score: {{ $json.score }}/100
Budget: {{ $json.budget }}
Timeline: {{ $json.timeline }}
Service: {{ $json.service }}

→ Reply fast — they're hot!
```

**Alternative: Slack notification**
- Use Slack node instead
- Webhook URL from Slack app settings
- Same message content

---

## How to Import

1. Go to **http://13.62.48.252:5678**
2. Log in (username: lyubo)
3. Click **"+"** to create a new workflow
4. Click the **three-dot menu (⋮)** → **"Import from File"**
5. Select the file `n8n-lead-workflow.json` from this folder
6. The workflow will appear — update all credentials (API keys, chat IDs)
7. Click **"Activate"** toggle at the top right

---

## How to Connect Tally

1. In n8n, click on the Webhook node
2. Copy the **"Webhook URL"** (looks like `http://13.62.48.252:5678/webhook/tally-lead`)
3. In Tally.so, open your form → **Integrations** → **Webhooks**
4. Paste the URL
5. Set trigger to: **"Form submitted"**
6. Save

Test by submitting your own form — you should see:
- Contact added to Brevo ✅
- Welcome email received ✅
- (If high score) Telegram alert received ✅

---

## Updating the Scoring Logic

To change how leads are scored, go to the **Code node** in n8n and edit the JavaScript directly. Key things you can adjust:

- **Change budget thresholds** — match your actual Tally budget options
- **Change point values** — make budget worth more or less
- **Add new scoring criteria** — e.g., add points if they found you via referral

---

*Last updated: 2026-03-06 | Motion Elevation Infrastructure*

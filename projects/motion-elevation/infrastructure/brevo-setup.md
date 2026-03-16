# Brevo Setup Guide
**Free Email Marketing for Motion Elevation**
**Level: Beginner-friendly | 300 emails/day free**

---

## What is Brevo?

Brevo (formerly Sendinblue) is an email marketing platform. You'll use it to:
- Send automated welcome emails to new leads
- Build an email list you actually own
- Send newsletters and campaigns
- Connect to n8n for full automation

Free tier: **300 emails/day**, unlimited contacts.

---

## Part 1: Create Your Brevo Account

### Step 1: Sign Up

1. Go to **https://www.brevo.com**
2. Click **"Sign Up Free"** (top right)
3. Enter your email address
4. Create a password (save it somewhere safe)
5. Click **"Create Account"**
6. Check your email — click the verification link

> 📸 *[Screenshot: Brevo homepage with "Sign Up Free" button in the top right corner, and a sign-up form with email/password fields]*

### Step 2: Complete Your Profile

Brevo needs your business info to approve your account for sending:

1. Enter **Company/Brand name:** `Motion Elevation`
2. Enter your **phone number** (required for verification)
3. **What do you plan to send?** → Select "Transactional emails" and/or "Marketing emails"
4. **How many contacts do you have?** → Select "Less than 500" (honest answer)
5. Click **"Continue"**

> 📸 *[Screenshot: Brevo onboarding form asking for company name, phone number, and contact count]*

### Step 3: Verify Your Phone

Brevo will send a text message with a code. Enter it when prompted.

---

## Part 2: Set Up Your Sender Email (DNS)

This is the most technical part, but super important. Without it, your emails land in spam.

### Why DNS Matters

When you send an email from `hello@yourdomain.com`, other email servers check:
- **SPF** — "Is this server allowed to send from this domain?"
- **DKIM** — "Is this email cryptographically signed and untampered?"
- **DMARC** — "What to do if SPF/DKIM fail?"

Without these, Gmail/Outlook marks your emails as spam. With them, you land in the inbox.

---

### Step 4: Add Your Sending Domain

1. In Brevo, click **"Senders & IP"** in the left sidebar (or go to Settings → Senders)
2. Click **"Domains"**
3. Click **"Add a domain"**
4. Enter your domain: `yourdomain.com` (whatever domain you're using)
5. Click **"Save"**

> 📸 *[Screenshot: Brevo Senders page with "Domains" tab selected and an "Add a domain" button]*

Brevo will show you 3 DNS records to add. They look like this:

```
Type: TXT
Name: @  (or yourdomain.com)
Value: v=spf1 include:sendinblue.com ~all

Type: TXT  
Name: mail._domainkey
Value: k=rsa; p=MIGf....(long string)....

Type: TXT
Name: _dmarc
Value: v=DMARC1; p=none; rua=mailto:dmarc-reports@yourdomain.com
```

Keep this page open — you'll need these values in the next steps.

---

### Step 5: Add DNS Records (Namecheap example)

> If your domain is with a different registrar (GoDaddy, Cloudflare, etc.), the steps are similar — look for "DNS Records" or "DNS Management" in their dashboard.

**For Namecheap:**
1. Log into **https://www.namecheap.com**
2. Go to **Domain List** → click **Manage** next to your domain
3. Click **Advanced DNS** tab
4. Click **"Add New Record"** for each of the 3 records:

**Record 1 — SPF:**
- Type: `TXT`
- Host: `@`
- Value: `v=spf1 include:sendinblue.com ~all`
- TTL: `Automatic`
- Click ✓ Save

**Record 2 — DKIM:**
- Type: `TXT`
- Host: `mail._domainkey`
- Value: (paste the long string from Brevo)
- TTL: `Automatic`
- Click ✓ Save

**Record 3 — DMARC:**
- Type: `TXT`
- Host: `_dmarc`
- Value: `v=DMARC1; p=none; rua=mailto:your@email.com`
- TTL: `Automatic`
- Click ✓ Save

> 📸 *[Screenshot: Namecheap Advanced DNS tab showing the list of DNS records with TXT type records visible]*

### Step 6: Verify in Brevo

1. Go back to Brevo → **Senders → Domains**
2. Click **"Verify"** next to your domain
3. DNS can take up to 48 hours to propagate — but usually works within 1 hour
4. When verified, you'll see a green checkmark ✅ next to each record

> 💡 **Test DNS propagation:** Go to https://mxtoolbox.com/spf.aspx and enter your domain to check if SPF is working.

---

## Part 3: Create Email Lists

### Step 7: Create Your Main Lists

1. In Brevo, click **"Contacts"** in the left sidebar
2. Click **"Lists"**
3. Click **"Create a list"**

Create these lists:

| List Name | Purpose |
|-----------|---------|
| `All Leads` | Every new lead from Tally |
| `Hot Leads` | Score 70+ (VIP treatment) |
| `Newsletter` | People who opted in for updates |

For each list:
- Click **"Create a list"**
- Enter the name
- Click **"Create"**

Note the **List ID number** (e.g., `3`) that appears — you'll need it for n8n.

> 📸 *[Screenshot: Brevo Contacts → Lists page showing a table of lists with columns: Name, ID, Contacts count]*

---

## Part 4: Get Your API Key

The API key lets n8n talk to Brevo automatically.

### Step 8: Generate API Key

1. Click your **profile icon** (top right) → **SMTP & API**
2. Or go directly to: **https://app.brevo.com/settings/keys/api**
3. Click **"Generate a new API key"**
4. Name it: `n8n-automation`
5. Click **"Generate"**
6. **COPY the key immediately** — you won't see it again!

> 📸 *[Screenshot: Brevo API Keys page with a "Generate a new API key" button and a list of existing keys]*

It looks like: `xkeysib-abc123def456...` (long string)

Store it safely — you'll paste it into n8n next.

---

## Part 5: Connect Brevo to n8n

### Step 9: Add API Key to n8n

1. Open n8n: **http://13.62.48.252:5678**
2. Go to **Settings** (bottom left gear icon) → **Credentials**
3. Click **"Add Credential"**
4. Search for: `HTTP Header Auth` (Brevo doesn't have a native n8n node, so we use the HTTP Request node with header auth)
5. Fill in:
   - **Name:** `Brevo API`
   - **Name (header):** `api-key`
   - **Value:** (paste your Brevo API key)
6. Click **"Save"**

> 📸 *[Screenshot: n8n Credentials page showing a form for HTTP Header Auth with "api-key" in the Name field]*

### Step 10: Import the Lead Workflow

1. In n8n, click **"+"** → **"Import from file"**
2. Select `n8n-lead-workflow.json` from this folder
3. The workflow will load
4. Update the **"Add to Brevo"** node:
   - Click the node
   - Find `"listIds": [1]` in the JSON body
   - Replace `1` with your actual list ID from Step 7
5. Update the **Brevo API** credential in both HTTP request nodes
6. Save and **Activate** the workflow

---

## Part 6: Test Everything

### Step 11: Send a Test Email

1. In Brevo, go to **Campaigns** → **Email Campaigns** → **"Create an email campaign"**
2. Create a simple test campaign
3. Send to yourself first before sending to real leads

### Step 12: Submit a Test Lead

1. Submit your Tally.so form with a test entry
2. Check:
   - n8n execution log shows success (green checkmarks on all nodes)
   - Test contact appears in Brevo → Contacts
   - Welcome email arrives in your inbox
   - (If high score) Telegram notification received

---

## Brevo Free Tier Limits

| Feature | Free Limit |
|---------|-----------|
| Emails per day | 300 |
| Contacts | Unlimited |
| Email campaigns | Unlimited |
| Transactional emails | Unlimited (within 300/day) |
| Brevo branding | Yes (on free tier) |
| Support | Email only |

> When you hit 300 leads/month: Brevo Starter plan is ~€25/month for 20,000 emails. Still cheap.

---

## DNS Cheat Sheet

If you need to set up DNS for a new domain, use these exact values from Brevo:

```
# SPF (tells email servers Brevo is allowed to send for you)
Type: TXT
Host: @
Value: v=spf1 include:sendinblue.com ~all

# DKIM (cryptographic signature — get actual value from Brevo dashboard)
Type: TXT
Host: mail._domainkey
Value: k=rsa; p=<get from Brevo>

# DMARC (what to do with failed emails — start with p=none, upgrade to p=quarantine later)
Type: TXT
Host: _dmarc
Value: v=DMARC1; p=none; rua=mailto:lyubo@yourdomain.com
```

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| Emails going to spam | Check DNS verification in Brevo — all 3 records must be green |
| DNS not verifying | Wait 24 hours, then re-check. DNS propagation takes time. |
| API key not working in n8n | Make sure header is `api-key` (lowercase, hyphen) |
| Contact not appearing in Brevo | Check n8n execution log for HTTP 4xx errors — likely API key or list ID issue |
| Getting "email not verified" error | Make sure sender email matches a verified domain in Brevo |

---

## Quick Reference

| Item | Where to Find It |
|------|-----------------|
| API Key | Brevo → Settings → SMTP & API |
| List ID | Brevo → Contacts → Lists (number in the ID column) |
| DNS Records | Brevo → Senders → Domains |
| Webhook URL for n8n | n8n → Webhook node → Copy URL |

---

*Last updated: 2026-03-06 | Motion Elevation Infrastructure*

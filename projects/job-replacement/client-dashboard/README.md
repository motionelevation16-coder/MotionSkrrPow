# Motion Elevation — Client Dashboard

A secure, white-label client dashboard for Motion Elevation's automation agency.
Clients pay €150-200/month and trigger their n8n automations without ever seeing n8n.

---

## Files

```
client-dashboard/
├── login.html       # Magic-link login page
├── dashboard.html   # Main client dashboard
├── styles.css       # Shared design system
├── demo-data.js     # Fake data for ?demo=true mode
└── README.md        # This file
```

---

## Deploy (Vercel — recommended)

1. Push this folder to a GitHub repo (e.g. `motion-elevation/client-dashboard`)
2. Go to [vercel.com](https://vercel.com) → New Project → Import that repo
3. Framework: **Other** (it's just static HTML)
4. Deploy — you'll get a URL like `https://dashboard.motion-elevation.com`

### Vercel Custom Domain
- Project Settings → Domains → Add your domain
- Point your DNS `CNAME` to `cname.vercel-dns.com`

### Netlify (alternative)
```bash
npm install -g netlify-cli
netlify deploy --dir . --prod
```

---

## How to Issue Client Tokens

Each client gets a **unique token** that authenticates all their webhook calls.

### Option A — n8n Generates Tokens (recommended)
Build a one-time setup workflow in n8n:
1. Trigger: new client signed up (Stripe webhook, form submit, etc.)
2. Generate a random token: `crypto.randomUUID()` or a custom function node
3. Store `{ email, token, clientId, plan, active: true }` in your database (Airtable, Notion, Postgres, etc.)
4. Send the client a welcome email with their magic link:
   ```
   https://your-dashboard.com/dashboard.html?token=TOKEN&email=CLIENT_EMAIL
   ```
   (The dashboard picks up `?token=` and `?email=` from the URL and saves to localStorage automatically.)

### Option B — Manual (small teams)
Use any UUID generator (e.g. `uuidgen` in terminal, or [uuidgenerator.net](https://www.uuidgenerator.net/)).
Save to your records and email the client their link manually.

### Magic Link Format
```
https://your-dashboard.com/dashboard.html?token=abc123&email=client@company.com
```
The dashboard JS handles the rest — stores token to localStorage, cleans the URL.

---

## How to Connect Webhooks (n8n Setup)

### 1. Client Data Endpoint
Create an n8n webhook workflow that the dashboard calls on load.

**Trigger:** `POST /webhook/client-data`
**Headers:** `X-Client-Token: <token>`
**Body:** `{ email: "client@example.com" }`

**Workflow logic:**
1. Receive request
2. Look up token in your database
3. If not found or expired → respond `401 Unauthorized`
4. If found → respond with:
```json
{
  "client": {
    "id": "client-001",
    "name": "Acme GmbH",
    "email": "client@acme.de",
    "subscriptionStatus": "active",
    "subscriptionPlan": "Growth",
    "subscriptionRenewal": "2026-04-01",
    "avatarInitials": "AG"
  },
  "stats": {
    "runsThisMonth": 247,
    "emailsSent": 1840,
    "leadsCaptures": 38,
    "timeSavedHours": 23,
    "successRate": 98.4
  },
  "automations": [
    {
      "id": "email-triage",
      "icon": "📧",
      "name": "Email Triage & Auto-Reply",
      "description": "...",
      "status": "active",
      "lastRun": "2026-03-07T00:47:00Z",
      "runsThisMonth": 89,
      "webhookUrl": "https://your-n8n.domain/webhook/email-triage",
      "enabled": true
    }
    // ... more automations
  ]
}
```

### 2. Per-Automation Webhooks
Each automation card fires its own n8n webhook. The URL is stored in your database and returned with the client data.

**Every automation webhook must:**
1. Extract `X-Client-Token` from headers
2. Validate token → if invalid, respond `401`
3. Check `active: true` in client record
4. Execute the automation logic
5. Respond with a result message:
```json
{ "message": "✅ 12 emails triaged. 3 auto-replies sent." }
```

**Security pattern (n8n function node):**
```javascript
const token = $input.first().headers['x-client-token'];
const record = await lookupToken(token); // your DB query
if (!record || !record.active) {
  return [{ json: { error: 'Unauthorized' }, statusCode: 401 }];
}
// proceed with automation...
```

### 3. Magic Link Auth Webhook
**Trigger:** `POST /webhook/auth/magic-link`
**Body:** `{ email: "client@example.com" }`

**Workflow:**
1. Look up email in your client database
2. If not found → respond with a generic success (don't leak emails)
3. If found → generate a short-lived token (15-min expiry), store it
4. Send email via your mail provider (SMTP, SendGrid, Postmark):
   ```
   Subject: Your Motion Elevation Dashboard Link
   Body: Click here to sign in: https://your-dashboard.com/dashboard.html?token=TOKEN&email=EMAIL
   ```

---

## Security Notes

| Concern | Mitigation |
|---|---|
| Token theft via XSS | Tokens in localStorage are XSS-vulnerable. For higher security, use HttpOnly cookies via a thin backend proxy. |
| Token rotation | Rotate tokens monthly or on suspicious activity. |
| Rate limiting | Add rate limiting to your n8n webhooks (n8n Enterprise or Cloudflare proxy). |
| HTTPS only | Always serve the dashboard over HTTPS (Vercel/Netlify do this automatically). |
| CORS | n8n webhook CORS headers should allow only your dashboard domain. |

---

## Subscription Status

The `subscriptionStatus` field in the client record drives the dashboard:
- `"active"` → all automations enabled
- `"inactive"` → all buttons disabled, "Renew Subscription" overlay shown
- `"trial"` → works same as active (add a trial badge if desired)

**Automate subscription management** via Stripe webhooks:
- `customer.subscription.deleted` → set `active: false` in your DB
- `customer.subscription.updated` → update plan name

---

## Demo Mode

Visit `dashboard.html?demo=true` — no login required, shows fake data from `demo-data.js`.
Use this link in sales calls, proposals, and your landing page.

---

## Customisation Checklist

- [ ] Update `CONFIG.n8nBase` in `dashboard.html` with your n8n URL
- [ ] Update support/billing email addresses throughout
- [ ] Replace `motion-elevation.com` with your actual domain
- [ ] Build the n8n `client-data` endpoint
- [ ] Build per-automation webhook endpoints
- [ ] Build magic-link auth endpoint
- [ ] Set up Stripe → n8n subscription sync
- [ ] (Optional) Add more automation cards in `demo-data.js`

---

## Architecture Diagram

```
Client Browser
     │
     ├─► login.html → POST /webhook/auth/magic-link → n8n → Email
     │
     ├─► dashboard.html?token=XXX
     │        │
     │        ├─► POST /webhook/client-data (validates token)
     │        │        └─► returns client + stats + automation list
     │        │
     │        └─► [Run Now] → POST /webhook/{automation-id} (includes X-Client-Token)
     │                              └─► validates token → runs workflow → returns result
     │
     └─► dashboard.html?demo=true (no auth, uses demo-data.js)
```

---

Built by Motion Elevation · [motion-elevation.com](https://motion-elevation.com)

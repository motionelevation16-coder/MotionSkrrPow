# MOTION ELEVATION — Full Context Brief
*For: Claude / External AI assistance*
*Last updated: 2026-03-15*
*Created by: Motion 🐋 (AI agent) + Lyubo (founder)*

---

## WHO IS LYUBO?

- University student + German-language part-time job on the side
- Goal: build independent income online, escape employee life
- First milestone: €50/month from something online = proof it works
- Not a developer — but ambitious, fast-moving, wants execution not theory
- Timezone: CET/CEST (Central Europe)
- Communication: direct, no fluff, values speed

---

## THE BUSINESS: Motion Elevation

**Type:** Done-for-You Automation Agency (Automation-as-a-Service)
**Tagline:** "We replace your busywork with bots."
**Model:** Monthly retainer + one-time builds
**Primary market:** DACH (Germany/Austria/Switzerland) + Netherlands
**Secondary market:** English-speaking solopreneurs globally

### Pricing Tiers
| Tier | Price | What's Included |
|------|-------|----------------|
| Starter | €297/month | 1 automation, monthly maintenance, email support |
| Growth | €697/month | 3 automations, CRM integration, weekly report, priority support, monthly call |
| Scale | €1,497/month | Unlimited automations, full integration, custom dev, weekly calls |
| One-Time Build | €500–5,000 | Custom projects |

**Margin:** 75–90% (all tools are free tier or nearly free)

---

## TECH STACK (CURRENT STATE)

### Server
- **AWS EC2** instance running in Frankfurt region
- IP: 13.62.48.252
- OS: Ubuntu Linux
- **n8n** running in Docker on port 5678 (auth enabled — user: lyubo)
- **UFW firewall** active: ports 22 (SSH) and 5678 open
- ⚠️ **BLOCKER:** Port 5678 in AWS Security Group is NOT yet open to the internet (needs phone MFA to unlock). n8n is running but only accessible via SSH tunnel currently.

### Automation Engine
- **n8n** (self-hosted, Docker) — the core tool for building all client workflows
- 267 pre-built n8n workflow templates downloaded and stored at `projects/n8n-templates/`
- Templates organized by category (see section below)

### Free Tool Stack (Zero-Cost Launch)
| Need | Tool | Notes |
|------|------|-------|
| Automation engine | n8n (self-hosted) | Already running on AWS |
| Database | Supabase | Free tier (500MB), already has project set up |
| Email marketing | Brevo | 300 emails/day free, GDPR-compliant |
| Landing page | Carrd / Vercel | Carrd free or Vercel (deployed) |
| Lead capture / quiz | Tally.so | Free, webhook-enabled |
| Payments | Stripe | Free to set up, 1.4%+€0.25/txn |
| Scheduling | Calendly / Cal.com | Calendly free (1 event type) |
| CRM | HubSpot free / Google Sheets | HubSpot unlimited free contacts |
| AI/LLM | Gemini (free) + Groq (free) | For client automations, $0 cost |
| AI/LLM | OpenAI GPT-4 | Pay-as-you-go when needed |
| Video walkthroughs | Loom | 25 free videos |
| Design | Canva | Free tier |
| Content editing | CapCut | Free, for Reels/TikTok |

---

## WHAT'S BEEN BUILT SO FAR

### Strategic Documents (all in `projects/job-replacement/`)
- `STRATEGY.md` — full go-to-market strategy
- `LAUNCH-BRIEF.md` — day-by-day action plan (Week 1 plan, offer structure, scripts)
- `PRICING-RESEARCH.md` — competitor pricing analysis
- `COMPETITOR-ANALYSIS-DACH.md` — DACH market competitors
- `ZERO-COST-STACK.md` — every tool, free tier, and when to upgrade
- `PLUG-AND-PLAY.md` — delivery system (onboarding → build → launch flow)
- `OBJECTIONS.md` — common sales objections + responses
- `CLIENT-JOURNEY.md` — full client lifecycle
- `CLIENT-SETUP-GUIDE.md` — how to onboard a client
- `CLIENT-TROUBLESHOOTING.md` — support playbook
- `DELIVERY-VARIANTS.md` — what to deliver per niche
- `BACKTEST-REPORT.md` — projected numbers and validation
- `EMAIL-INFRASTRUCTURE.md` — email sending setup (Zoho + Brevo)

### Sales Materials
- `sales-package/cold-emails-DE-EN.md` — cold email templates (German + English)
- `outreach/COLD-EMAILS-GERMAN.md` — German outreach scripts
- `outreach/COLD-EMAILS-ENGLISH.md` — English outreach scripts
- `outreach/COLD-EMAILS-FRENCH.md` — French outreach scripts
- `outreach/COLD-EMAILS-ITALIAN.md` — Italian outreach scripts
- `outreach/COLD-EMAILS-SPANISH.md` — Spanish outreach scripts
- `sales-package/sales-call-script.md` — full discovery call script
- `SALES-CALL-SCRIPT.md` — discovery + close script
- `cold-outreach-scripts.md` — DM templates (LinkedIn, Instagram, Reddit)
- `AFFILIATE-PROGRAM.md` — affiliate flywheel structure
- `sales-package/subject-line-bank.md` — email subject lines
- `sales-package/outreach-tracker-template.md` — CRM tracking sheet

### Lead Lists
- `prospect-list-DE-realestate.md` — German real estate prospects
- `prospect-list-DE-all-niches.md` — German prospects across niches
- `prospect-list-DE-coaches.md` — German coaches prospects
- `LEAD-LIST.md` — general lead list

### Landing Pages
- `landing-page/index.html` — main landing page (HTML)
- `landing-page/roi-calculator.html` — ROI calculator tool
- `sales-package/index.html` — sales page
- `sales-package/landing-page-copy.md` — copywriting for landing pages
- `motion-elevation-site/index.html` — Motion Elevation website
- `motion-elevation-site/coaches.html` — coaches niche page
- `motion-elevation-site/restaurants.html` — restaurants niche page

### Automation Templates (pre-built n8n workflows in `templates/`)
- `email-triage-bot.json` — AI email sorting and labeling
- `social-media-autoposter.json` — content scheduling bot
- `lead-followup-sequence.json` — automated lead nurture
- `templates/N8N-WORKFLOWS-DETAILED.md` — detailed workflow specs

### Niche-Specific READMEs (what to sell + deliver per vertical)
- `customer-support/README.md`
- `marketing/README.md`
- `sales/README.md`
- `hr-recruiting/README.md`
- `finance/README.md`
- `operations/README.md`
- `admin-executive/README.md`
- `it-devops/README.md`
- `security/README.md`
- `ecommerce-retail/README.md`
- `healthcare-medical/README.md`
- `legal-compliance/README.md`
- `data-analysis/README.md`

### Content
- `content/instagram-captions.md` — ready-to-post Instagram captions
- `content/linkedin-posts.md` — LinkedIn content
- `FACELESS-CONTENT.md` — faceless content strategy
- `OVERNIGHT-CREATIVE.md` — overnight content production ideas

### Motion Elevation Sub-Project (`projects/motion-elevation/`)
- `FUNNEL-BLUEPRINT.md` — full quiz funnel design (6-question audit → score → email sequence)
- `EMAIL-SEQUENCE.md` — 6-email nurture sequence (post-quiz)
- `LAUNCH-ROADMAP.md` — 90-day roadmap (Phase 1: pre-launch, Phase 2: soft launch, Phase 3: growth)
- `QUICK-WINS.md` — fastest paths to first revenue
- `COMPETITOR-RESEARCH.md` — competitor deep-dive

### Client Dashboard
- `client-dashboard/index.html` — login page
- `client-dashboard/dashboard.html` — client-facing dashboard
- `client-dashboard/styles.css`
- `client-dashboard/demo-data.js`

### Scripts
- `scripts/linkedin_outreach.py` — LinkedIn outreach automation script
- `scripts/lead_finder.py` — lead finding automation

---

## N8N TEMPLATES LIBRARY (267 templates)

Stored at: `projects/n8n-templates/`

| Category | Count | Key Use Cases |
|----------|-------|--------------|
| OpenAI & LLMs | 81 | AI agents, chatbots, text generation, summarization |
| AI Research & RAG | 40 | Document Q&A, knowledge bases, vector search |
| Gmail & Email | 20 | AI email triage, auto-reply, labeling, phishing detection |
| Telegram | 21 | AI chatbots, voice bots, image analysis, moderation |
| Google Drive/Sheets | 17 | Lead qualification, content pipelines, doc summarization |
| PDF & Documents | 17 | Invoice extraction, resume parsing, PDF chat |
| Other Integrations | 29 | CRM, Stripe, webhooks, scheduling, data routing |
| Instagram/Twitter/Social | 10 | Content scheduling, social automation |
| Notion | 10 | Competitor research, LinkedIn outreach, knowledge base AI |
| WhatsApp | 4 | WhatsApp business bots |
| WordPress | 6 | AI blog creation, auto-tagging, chatbot integration |
| HR & Recruitment | 4 | Resume screening, job application handling |
| Forms & Surveys | 3 | Lead capture, routing, form processing |
| Database & Storage | 5 | Supabase, Postgres, SQL with AI |

**How to import:** n8n → Workflows → Import from File → select `.json`

---

## CORE PRODUCT: THE 5 STARTER AUTOMATIONS

These are what Lyubo will deliver to first clients (fast, proven, high-value):

### 1. Email Inbox Triage Bot
**Build time:** 3h | **Client value:** Saves 5-10h/week
- Scans Gmail → labels by priority/category via AI
- Drafts replies for common email types
- Sends Telegram alert for urgent items
- Tools: n8n + Gmail API + Gemini (free)

### 2. Social Media Auto-Poster
**Build time:** 2h | **Client value:** Saves 8-15h/week
- Client puts content in Google Sheet
- n8n posts at scheduled times to Instagram, TikTok, LinkedIn, Twitter
- Updates status column when posted
- Tools: n8n + Google Sheets + platform APIs

### 3. Lead Follow-Up Sequence
**Build time:** 2h | **Client value:** Never miss a lead
- New lead form submission → welcome email
- Day 2: value email, Day 4: case study, Day 7: check-in
- Stops when they reply
- Tools: n8n + Gmail + Google Sheets

### 4. AI FAQ Chatbot
**Build time:** 4h | **Client value:** 24/7 customer support
- Embedded on website or via Telegram/WhatsApp
- Trained on client's FAQ/documents
- Collects lead info, escalates complex queries
- Tools: n8n + Supabase + OpenAI/Gemini

### 5. Invoice Reminder System
**Build time:** 2h | **Client value:** Recovers unpaid revenue
- Monitors Google Sheets / Stripe for unpaid invoices
- Sends polite reminders at Day 7, 14, 21
- Stops when paid
- Tools: n8n + Gmail + Google Sheets

---

## THE FUNNEL (Automation Audit)

### Entry Points
- Instagram Reels / TikTok: "How many hours does your business waste on tasks a robot could do?"
- Reddit replies in entrepreneur subs
- LinkedIn DMs
- Affiliate posts

### The Quiz (6 Questions — 90 seconds)
1. Business type (Freelancer/Solo | Small team | Agency | Local business | E-commerce)
2. Hours/week on repetitive tasks (< 5h | 5-15h | 15-30h | 30h+)
3. Biggest time drain (Support/emails | Invoicing/admin | Social media | Lead follow-up | Team coordination)
4. Current automation tools (None/manual | Some tools | Zapier/Make | Full stack)
5. Monthly revenue (< €2k | €2-5k | €5-15k | €15-50k | €50k+)
6. Goal (Save time | Grow without hiring | Cut costs | All of the above)

### Output
- Score 0-100 ("Your Automation Score")
- Top 3 personalized automation recommendations
- Triggers 6-email nurture sequence (via Brevo)

### Email Sequence (Post-Quiz)
- Email 1 (immediate): Your score + personalized recommendations
- Email 2 (Day 2): Real case study (before/after, specific hours saved)
- Email 3 (Day 3): "The automation hiding in plain sight" (specific to their pain point)
- Email 4 (Day 4): FAQ / objection handling
- Email 5 (Day 5): Limited offer / beta pricing
- Email 6 (Day 7): Last chance / affiliate pitch

---

## DELIVERY PROCESS (The 48h Promise)

```
Client pays → Welcome email + setup form (auto, via n8n)
Hour 2: Review setup form, plan their 2-3 automations
Hour 12: Start building in n8n
Hour 24: First automation live → send Loom walkthrough
Hour 48: Full delivery → webhook URLs, docs, "control panel"
Ongoing: Weekly check (automations running) + monthly report
```

---

## OUTREACH STRATEGY

### Primary Targets
1. **Content Creators** (10k-500k followers) — IG, TikTok, YouTube, Twitter
2. **Local service businesses** — HVAC, plumbing, dental, restaurants (Google Maps)
3. **German solopreneurs/freelancers** — LinkedIn, XING, Facebook groups

### DM Template (LinkedIn, German)
```
Hallo [Name],

ich hab gesehen, dass du als [Freelancer/Agenturinhaber] in [Branche] arbeitest.

Ich baue gerade Motion Elevation auf – ein Done-for-You Automatisierungsservice für Selbstständige. Grundidee: du sagst mir, was dich die meiste Zeit kostet, ich baue die Automatisierung in 48h, und es läuft.

Gerade suche ich meine ersten 3 Beta-Kunden für Feedback. Das heißt: deutlich reduzierter Preis, dafür ehrliches Feedback danach.

Würde dich interessieren, was automatisierbar wäre bei dir?

Viele Grüße, Lyubo
```

### DM Template (Instagram, casual)
```
Hey [Name]! Dein Content zu [topic] ist richtig gut.

Ich launch gerade einen Automatisierungsservice für Selbstständige und suche 3 Beta-Tester. Idee: du sagst mir welche Aufgaben dich am meisten Zeit kosten, ich bau die Automatisierung in 48h.

Interessiert dich das? 🤙
```

---

## CURRENT STATUS & BLOCKERS

### ✅ Done
- Business name: Motion Elevation
- Full strategy + pricing documented
- Sales materials in 5 languages
- 267 n8n templates downloaded and ready
- n8n running on AWS EC2 (Docker, port 5678)
- Landing pages built (HTML)
- Cold email sequences written
- Prospect lists built (DACH)
- Client dashboard built

### ⏳ Pending (Lyubo's actions needed)
1. **Open AWS Security Group port 5678** — needs phone MFA — this unlocks the n8n UI
2. **Register domain** (motionelevation.com or .de) — ~€10/year on Namecheap
3. **Create Tally.so account** → build the 6-question quiz
4. **Create Brevo account** → set up SPF/DKIM → import email sequence
5. **Create Stripe account** → set up payment products (€297/mo, €697/mo, €1,497/mo)
6. **Deploy landing page** → connect to quiz CTA
7. **Get first free/beta client** from personal network → deliver → get testimonial
8. **Start outreach** — 50 DMs per day

### 🔒 The Single Biggest Blocker
Opening the AWS port (phone MFA). Once that's done, n8n is usable and the entire automation infrastructure is live.

---

## GDPR COMPLIANCE (Critical for German Market)

- **Double opt-in is MANDATORY in Germany** — Brevo supports this natively
- **Impressum required** on every page (full name, address, phone)
- **Datenschutzerklärung** (Privacy Policy) — use datenschutz-generator.de
- **Cookie banner** — skip analytics for now to avoid complexity
- **Separate email consent checkbox** in quiz — pre-checked = illegal in DE
- **Physical address in every email footer** (legally required)
- Brevo is EU-based and GDPR-compliant ✅

---

## 90-DAY TARGETS

| Milestone | 30 Days | 60 Days | 90 Days |
|-----------|---------|---------|---------|
| Clients | 3–5 | 8–12 | 20–30 |
| MRR | €200–400 | €800–1,200 | €2,000–3,000 |
| Quiz completions | 50+ | 200+ | 500+ |
| Email list | 50 | 100+ | 500+ |
| Content (Reels) | 6 | 20 | 50 |
| Affiliates | 0 | 2+ | 5+ |

---

## THE CORE TRUTH

> "You don't need a perfect product. You need one paying customer."
> Close ONE deal. Deliver. Get a testimonial. Then scale.

---

*Built by Motion 🐋 — Lyubo's AI agent*
*All files live in: `/home/ubuntu/.openclaw/workspace/projects/`*

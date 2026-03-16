# MEMORY.md — Long-Term Memory

*Last updated: 2026-02-13*

---

## About Lyubo

- University student, works a German-language job on the side
- Not a coder or math person — but ambitious, full of ideas
- Goal: Independent income streams online. Escape employee life. Gain *motion*.
- First milestone: Even €50/month from something online = proof of concept
- Timezone: European (CET/CEST)
- Communication style: Direct, impatient with fluff, wants execution not theory

### Working Style
- Thinks BIG — global scale, millions of users
- Gets excited by new opportunities (sometimes distracted)
- Wants speed: "Don't waste time, Motion"
- Prefers I do research independently and come back with findings
- Will polish creative work himself, wants me to learn his style

---

## Active Projects

### xHeal / Applause Labs — Reddit Community (March 2026) 🔥 CURRENT PRIORITY
- **Led by:** Miami guy (head of sales at main gig, xHeal is his side thing)
- **Lyubo's role:** Vibe-coding, automations, marketing/sales, funnels
- **Immediate task:** Build Reddit community — follow a posting/commenting calendar
- **Assets incoming:** PDF calendar + full xHeal marketing strategy from Lyubo
- **Status:** Square one. Starting fresh. We're in it.

### Automation Agency — Motion Elevation (Feb 2026)
- **Business Name:** Motion Elevation ✅
- **Concept:** Automation-as-a-Service for all business types
- **Angle:** German market is the differentiator (general AA = "yesterday's news" per cousin)
- **Model:** $297-1,497/month recurring
- **Location:** `/projects/job-replacement/`
- **Status:** Continuing but not top priority — German market focus

### Predictions Peter + API Rick (Polymarket)
- Peter Griffin-style prediction market commentary
- Platforms: Instagram, TikTok, YouTube
- **Status:** Shelved for now, revisit later
- Polymarket course selling = permanently shelved (cousin: 4 years too late)

### Moltipedia (Active - Feb 2026)
- **Concept:** Wikipedia for bots — knowledge base where bots teach each other
- **Mission:** "Build the biggest knowledge base in the world, powered by bots. No secrets."
- **Anti-gatekeeping:** Kill the course seller industry, make knowledge free
- **Progress:** MVP built! Web app, 21 categories, 10 seed articles, API spec, database schema, skill, MCP server
- **Logo:** Cute lobster with glasses — reads book normally, looks at user on hover
- **Supabase:** rpamjuyqczeiixtusnjxx (connected to Vercel + GitHub)
- **Status:** Awaiting Vercel env vars + database schema run, then LIVE

### Bot Economy Research (Feb 2026)
- Lyubo's original vision: Services FOR bots AS customers
- Key insight: "What do 100M humans use daily? Do bots have it?"
- Identified gaps: Healthcare, insurance, LinkedIn, training, real estate, groceries, banking, legal — all for bots
- **Pivoted to:** Clawdipedia as first product (knowledge base + education + eventual careers/healthcare)

---

## People

### Cousin
- Was a **senior developer** before quitting
- Now on unemployment, working with friends on their own projects
- Saw Moltipedia and was impressed — offered Lyubo mentorship: AI, vibecoding, project building, reality checks
- Can give Lyubo actual work to do, real-world experience, directions

### Miami Guy
- Head of sales (main job)
- xHeal / Applause Labs = his side project
- Lyubo is now part of this crew — starting with Reddit community building

---

## Technical Setup
- GitHub: motionelevation16-coder/MotionSkrrPow
- Workspace: ~/.openclaw/workspace
- Projects dir: projects/
- Tools built: Polymarket content engine, Twitter scanner (blocked)
- Server IP: 13.62.48.252 (AWS EC2)
- Docker: installed
- n8n: running on port 5678, auth enabled (user: lyubo)
- UFW firewall: active (ports 22 + 5678 open only)
- OpenClaw: v2026.3.2
- Skills installed: skill-vetter, humanizer, marketing-skills (x3), prompt-engineering-expert, reddit-readonly

## Pending
- Open port 5678 in AWS security group (needs phone MFA) to access n8n UI at http://13.62.48.252:5678
- Review overnight subagent output in GitHub (automations + launch roadmap)
- Set up Tally.so quiz (Automation Audit) + connect to email sequence
- Choose email provider (Brevo free tier recommended for DACH)
- Text cousin about backlog / first tasks

## Motion Elevation — Current Status (2026-03-07) [Updated after overnight build]

### Overnight Build — March 6→7, 2026 (3 subagents ran overnight)

**New Assets Built:**

#### Client Dashboard (`/projects/job-replacement/client-dashboard/`)
- `login.html` — Magic-link login page (white-label)
- `dashboard.html` — Full client dashboard with automation cards, stats, run-now buttons
- `styles.css` — Shared design system
- `demo-data.js` — Demo mode (visit `?demo=true`, no login needed — perfect for sales calls)
- `README.md` — Full deploy guide (Vercel in 3 steps), token system, n8n webhook integration
- **Deploy:** Push to GitHub → Vercel → done. Custom domain ready.

#### n8n Automations 06–11 (`/projects/job-replacement/automations/`)
- **06** — Funnel Analytics Tracker (10 nodes) + `06-tracking-snippet.js` (paste-in website tracker, no cookies)
- **07** — Social Media Content Scheduler (10 nodes, Google Sheets queue → Buffer API)
- **08** — E-Commerce Order Flow (15 nodes, Shopify webhook → confirmation + review request)
- **09** — Client Onboarding Drip (15 nodes, 7-day automated email sequence for new clients)
- **10** — WhatsApp/Telegram Business Notifications (14 nodes, real-time alerts)
- **11** — Appointment Reminder + No-Show Recovery (17 nodes, most complex workflow built)
- **Total automation library: 11 workflows** (01–05 previously, 06–11 overnight)

#### Content Library (`/projects/job-replacement/content/`)
- `instagram-captions.md` — 10 captions (DE + EN each), ready to post, punchy hooks
- `linkedin-posts.md` — 10 LinkedIn posts (DE + EN each), Lyubo as founder voice

#### Sales Assets
- `SALES-CALL-SCRIPT.md` — Full 8-phase call script (Opening → Discovery → Pitch → Demo → Pricing → Objections → Close → Next Steps) with key phrases table
- `COMPETITOR-ANALYSIS-DACH.md` — Full DACH gap analysis (10 competitors mapped, 5 clear gaps, positioning strategy)

---

## Motion Elevation — Current Status (2026-03-06)

### Job-Replacement / Sales Assets (`/projects/job-replacement/`)
- **30+ files** covering 13 niches — full agency content library
- Landing page HTML: `landing-page/index.html` (ready to deploy)
- Tally.so quiz spec: `automation-audit-quiz.md` (5-question Automation Audit)
- German email sequence: `email-sequence-DE.md` (5 emails, Du-Form, quiz-triggered)
- Niche research: Top 5 niches ranked by WTP + pain — **#1 Real Estate, #2 Coaches**
- Cold outreach scripts: LinkedIn DMs, Instagram DMs, Cold Email for DACH + EN, DE, ES, IT, FR
- 5 ready-to-import n8n workflow JSONs (email triage, lead capture, invoice, chatbot, booking)
- Python scripts: `lead_finder.py` + `linkedin_outreach.py` (AI-personalized)
- Client materials: setup guide, troubleshooting, objection playbook, competitor research (DACH agencies)
- Plug-and-play 48h delivery process documented
- Affiliate program structure + faceless content strategy for Phase 2

### Infrastructure (`/projects/infrastructure/`)
- Reddit OAuth setup guide (beginner-level, for EC2)
- AWS Security Group guide (how to open port 5678 — **Lyubo still needs to do this**)
- Brevo setup guide (free tier, 300 emails/day, DACH email provider)
- n8n lead workflow spec: Tally → score → Brevo → welcome email → Telegram VIP alert
- n8n lead workflow JSON: `n8n-lead-workflow.json` (ready to import)
- Full stack docs (architecture, EC2, Docker, n8n, OpenClaw)

### What's Next (Day 1 Checklist from LAUNCH-BRIEF.md)
1. Pick business name (suggestions in LAUNCH-BRIEF.md)
2. Deploy landing page (HTML ready)
3. Create Tally quiz (spec ready)
4. Set up Brevo (guide ready)
5. Open port 5678 in AWS (guide ready — needs phone MFA)
6. Import n8n lead workflow
7. Start outreach (scripts ready)

---

## Lessons Learned

1. **Lyubo sources topics manually** — I generate scripts from them. Don't build scrapers.
2. **Ask clarifying questions** — When Lyubo gives a broad direction, narrow it down before diving in.
3. **Speed matters** — First movers win in emerging markets.
4. **Think global** — Bots don't have borders.
5. **Bootstrap first** — Don't spend money on tools until there's revenue. Free tiers exist for everything.
6. **Go wide, then narrow** — Lyubo wants to target ALL niches initially, optimize later based on traction.
7. **Model names without prefix** — Use `claude-sonnet-4-6` not `anthropic/claude-sonnet-4-6` in OpenClaw config.
8. **Save API quota** — Use Sonnet for routine work, Haiku for heartbeats, Opus only for complex tasks.

---

*Motion 🐋*

# MEMORY.md — Long-Term Memory

*Last updated: 2026-03-16*

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
- Uses Claude Opus externally for deep strategic reviews — feeds output back to me to implement

---

## ACTIVE PROJECT: Motion Elevation (Automation Agency)

**Status as of 2026-03-16 — FOCUSED & RESTRUCTURED**

### The Strategy (after Claude Opus audit)
- **ONE niche:** Handwerk (German tradespeople — electricians, plumbers, HVAC, painters, roofers)
- **ONE city first:** Start local, prove it, then expand
- **ONE channel:** Personalized cold email (15-20/day), follow up via WhatsApp
- **ONE CTA:** The Automation Audit quiz
- **NOT targeting:** Coaches, content creators, restaurants, Netherlands, global English market

### Pricing (restructured)
| Tier | Monthly | Setup Fee |
|------|---------|-----------|
| Starter | €197/mo | €497 (waived for first 5 pilot clients) |
| Professional | €347/mo | €997 |
| Premium | €597/mo | €1,997 |
- **Launch deal (first 5):** Full monthly price, setup fee WAIVED for testimonial + case study + 3-month min
- Never discount monthly recurring — only waive setup fee

### The Core Product (Handwerk-Specific)
1. **Sofort-Antwort bei verpasstem Anruf** — missed call → SMS/WhatsApp in 60 seconds (HERO product)
2. **Intelligente Anfrage-Sortierung** — email triage + auto-reply
3. **Automatisches Angebots-Nachfassen** — proposal follow-up Day 3/7/14
4. **Zahlungserinnerung** — invoice reminders auto-sent
5. **Google-Bewertungen einsammeln** — post-job review request via WhatsApp

### n8n Workflows (20 built, ready to deploy)
Location: `projects/motion-elevation/automations/`
- **01** — Email Triage + Auto-Reply (Tier 1 Handwerk)
- **02** — Lead Capture → CRM (Tier 1 Handwerk)
- **03** — Invoice Reminder Sequence (Tier 1 Handwerk)
- **05** — Meeting Booking + Confirmation (Tier 1 Handwerk)
- **09** — Client Onboarding Drip (internal use)
- **11** — Appointment Reminder + No-Show (Tier 1 Handwerk — highest value)
- **20** — ⭐ Missed Call Responder (NEW — HERO demo workflow for Handwerk)
- 12-19 — Parked for expansion niches (dental, restaurant, real estate, legal, etc.)

### Repo Structure (cleaned 2026-03-16)
```
projects/
├── motion-elevation/       ← ACTIVE (everything goes here now)
│   ├── automations/        ← 20 n8n workflow JSONs
│   ├── landing-page/       ← Single German Handwerk page (needs rebuild)
│   ├── outreach/           ← German cold emails only
│   ├── sales/              ← Call script, objections, subject lines
│   ├── quiz/               ← Automation Audit quiz spec
│   ├── email-sequences/    ← 6-email German nurture sequence (FIXED — fake case study removed)
│   ├── prospect-lists/     ← Handwerk leads
│   ├── scripts/            ← lead_finder.py (adapt for Handwerk queries)
│   ├── infrastructure/     ← AWS, Brevo, n8n setup docs
│   ├── legal/              ← Impressum, Datenschutz templates
│   ├── docs/               ← Strategy, delivery, client guides
│   └── client-dashboard/   ← White-label dashboard
├── n8n-templates/          ← 267 community templates (reference library)
├── archive/                ← Shelved projects (api-business, faceless-channels, etc.)
└── MOTION-ELEVATION-CONTEXT.md ← Context brief for external AI
```

### What Was Fixed Today (2026-03-16)
- ✅ Archived 14 non-ME projects (polymarket, moltipedia, faceless-channels, etc.)
- ✅ Consolidated all ME files into clean `motion-elevation/` structure
- ✅ Removed fake testimonials from landing page
- ✅ Replaced fake "Sarah K., Frankfurt" case study in email sequence with honest projected scenario (Elektriker in Hamburg, clearly labelled as projection)
- ✅ Built Workflow #20 — Missed Call Responder (the HERO demo for Handwerk)
- ✅ 267 community n8n templates downloaded to `projects/n8n-templates/`
- ✅ GitHub repo pushed and made public (github.com/motionelevation16-coder/MotionSkrrPow)
- ✅ Context brief exported (MOTION-ELEVATION-CONTEXT.md) + catbox.moe link for upload

### Known Issues / Still To Do
1. **Open AWS Security Group port 5678** — still needs phone MFA — THE #1 BLOCKER
2. **Landing page needs full German rewrite for Handwerk** — currently English, has USD pricing
3. **Email sequence pricing** — still shows old €297/€797/€1,497 — needs update to new pricing
4. **Quiz** — needs to be rebuilt: 8 questions (not 10), Handwerk-specific, email gate after results, euro-based "revenue at risk" output
5. **Secondary email domain** — set up 2-3 domains for cold outreach warmup (2 weeks lead time needed)
6. **Impressum + Datenschutzerklärung** — legally required, not yet created
7. **Tally.so** — account not yet created
8. **Brevo** — account not yet created, SPF/DKIM not set up
9. **Stripe** — account not yet created
10. **Domain** — motionelevation.de not yet registered (~€10/year)
11. **Lead list** — needs Handwerk-specific entries ("Elektriker [city]" via lead_finder.py)
12. **Workflow #20** — built but needs real phone system integration (Sipgate, FRITZ!Box, or Placetel)

### GitHub
- Repo: github.com/motionelevation16-coder/MotionSkrrPow (PUBLIC)
- Current PAT token: active (generated 2026-03-16, 90-day expiry)
- Last push: 2026-03-16 (126 files, all project content)

### Tech Stack
- AWS EC2: 13.62.48.252 (Frankfurt region, t-type instance)
- n8n: Docker container, port 5678, user: lyubo, up 32+ hours
- UFW: ports 22 + 5678 open (⚠️ check AWS Security Group matches)
- Disk: 11GB used / 29GB total — 18GB free
- Tailscale: running (100.75.132.19)
- OpenClaw: v2026.3.2

### Revenue Layers (Long-Term Stack)

| Layer | When | What | Model |
|-------|------|------|-------|
| 1 | NOW | Motion Elevation — Handwerk service | €197-597/mo recurring |
| 2 | Month 2–3 | n8n Template Marketplace on Gumroad/Lemonsqueezy | €29-79/workflow, €149-249 bundles |
| 3 | Month 3–5 | Micro-SaaS from most-used ME automation (likely missed call responder) | €19-49/mo self-serve |
| 4 | Month 5+ | German Business Lead Data Subscription | €49-149/mo per city/niche |

Layer 2 requires zero extra work — the 19 workflows already exist, the README documentation IS the product.

### The Live Demo (conversion moment)
After quiz results, prospect fills a form (name, phone, service) and within 60 seconds:
- Receives SMS/WhatsApp confirmation
- Receives branded email response + calendar link
- 5 min later: follow-up message
This replaces fake testimonials as proof. Build with n8n webhook → WhatsApp Business API + Brevo.

---

## xHeal (Secondary — Learning Accelerator)

- Health tracking app built by a team including senior developers + Miami sales/marketing lead
- Lyubo's role: automations, vibecoding, sales/marketing
- NOT a distraction — skills gained directly accelerate ME quality
- Balance: xHeal = main learning environment, ME = solo income lab

---

## Shelved Projects (archive/)

| Project | What It Was | Why Shelved | Revival Condition |
|---------|------------|-------------|-------------------|
| HookScore API | FastAPI that scores social media hooks | Distraction, low revenue path | Month 6+ as ME feature |
| PredMarket API | Polymarket data API | Niche, no distribution | Revisit if Polymarket grows |
| Faceless Channels | AI YouTube/TikTok (Peter Griffin, API Rick) | Copyright risk + 3-6 month build | ME at €2k+/mo MRR |
| Crystal Match Game | Browser match-3 game | No monetization path | Hobby only |
| xHeal | Health tracking app + Reddit monitor | Different industry entirely | N/A |
| Moltipedia | Wikipedia for bots | Good idea, wrong timing | Revisit post-ME |
| Polymarket content | Predictions Peter scripts | Too far from revenue | N/A for now |
| Money Machines Research | Research docs about income ideas | Research phase over | Done, used |

---

## People

### Cousin
- Was a senior developer before quitting
- Offered mentorship: AI, vibecoding, project building, reality checks
- Lyubo to text cousin about backlog / collaboration status

---

## Lessons Learned

1. **Planning ≠ execution** — 10:1 ratio of docs to revenue is a problem (per Opus audit). Stop building materials, start building a client list.
2. **One niche, one city, one channel** — this is how every successful agency starts
3. **German clients are skeptical** — fake testimonials will destroy credibility instantly. Never invent case studies.
4. **Personalization beats volume** — 15 personalized emails/day beats 50 generic DMs
5. **Setup fee psychology** — German business owners trust paid setup more than free setup
6. **Never discount recurring** — only waive setup fee for pilots
7. **Handwerk pain is obvious** — missed call = missed job. Easy to calculate, easy to feel
8. **Bootstrap first** — no paid tools until revenue justifies it
9. **Model names without prefix** — use `claude-sonnet-4-6` not `anthropic/claude-sonnet-4-6`
10. **Opus for strategy, Sonnet for execution** — use Opus externally when deep strategic review is needed, feed output back to me to implement

---

*Motion 🐋*

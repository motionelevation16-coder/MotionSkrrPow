# Motion Elevation — Launch Roadmap
_Comprehensive, actionable, zero-fluff. Built for Lyubo. Date: 2026-03-05_

---

## THE BIG PICTURE

You have the funnel. You have the email sequence. You have the tech stack (n8n on AWS EC2).
What you're missing: live infrastructure, testimonials, and paying clients.

This roadmap takes you from zero to first €300 MRR in 30 days, and to €1,000+ MRR by Day 90.

**The single most important truth:** Don't wait until everything is perfect. Ship at 70%.
The first 3 clients don't care about a polished brand — they care if it works.

---

## PHASE 1: PRE-LAUNCH (Days 1–7)
### Goal: Build the infrastructure. Nothing public yet.

### What to build before going public:

#### 1. The Quiz (Tally.so — FREE)
- Create at Tally.so (free plan)
- 6 questions exactly as in FUNNEL-BLUEPRINT.md
- End screen: "Check your email for your personalized Automation Score"
- Collect: name, email, business type, hours wasted, pain point, revenue range, goal
- Set up Tally webhook → triggers n8n workflow

#### 2. The Email Pipeline (Brevo — FREE up to 300 emails/day)
- Create account at brevo.com (free, GDPR-compliant, EU servers)
- Set up sender domain authentication (SPF + DKIM) — critical for DE deliverability
- Import the 6-email sequence from EMAIL-SEQUENCE.md
- Create automation: webhook trigger → welcome list → 5-day sequence
- Test with your own email address before touching anything else

#### 3. The n8n Logic (AWS EC2 — already running)
- Build the quiz result calculator workflow:
  - Input: Tally webhook payload
  - Logic: calculate score (0–100) based on Q2 + Q4 answers
  - Output: personalized score + top 3 recommendations based on Q3 + Q1
  - Action: POST to Brevo API to add contact + trigger sequence
- Build the onboarding workflow:
  - Trigger: Stripe payment webhook
  - Actions: send welcome email → send setup form (Tally) → notify Lyubo on Telegram

#### 4. The Landing Page (Carrd — FREE)
- carrd.co free plan (1 page, custom domain on paid plan $9/year — worth it)
- Structure exactly as in FUNNEL-BLUEPRINT.md Sales Page section
- CTA buttons all link to Tally quiz
- Pricing section: €100/month + €500 lifetime
- Testimonials section: leave blank with placeholder text for now ("First 3 clients coming soon")
- Add Impressum + Datenschutzerklärung links (MANDATORY for .de audience — use datenschutz-generator.de)

#### 5. Payment (Stripe — FREE to set up)
- Create Stripe account
- Set up €100/month subscription product
- Set up €500 one-time lifetime product
- Enable SEPA Direct Debit (critical for Germany — many prefer this over card)
- Connect Stripe webhook → n8n onboarding workflow

#### 6. Affiliate Tracking (Simple spreadsheet for now)
- Create a Google Sheet: Affiliate Name | Link Code | Clicks | Conversions | Earnings
- Each affiliate gets a unique link: motionelevation.com/?ref=CODENAME
- n8n reads the ref param from the Tally form → logs to sheet
- Upgrade to Rewardful ($29/month) once you have 5+ affiliates

---

## PHASE 2: SOFT LAUNCH (Days 8–21)
### Goal: 3 paying (or free/discounted) clients. Get testimonials. Prove delivery.

### The 3-Client Strategy:

**Client 1 (Days 8–10): Free**
- Reach out to someone you know personally — a freelancer, local business owner, anyone who runs their own thing
- Offer the full service free for 30 days in exchange for a detailed testimonial + permission to use their results
- You get: a testimonial with real numbers ("saved 8h/month"), a case study for Email 2, and proof your delivery pipeline works

**Client 2 (Days 11–14): 50% discount**
- Go to LinkedIn, look for solopreneurs in DE/AT/NL who post about being busy/overwhelmed
- Send the DM template below
- Offer: €50/month first month (or €250 lifetime) → "beta pricing for feedback"
- Require: a written testimonial after 2 weeks

**Client 3 (Days 15–21): Full price**
- By now you have 1–2 testimonials on the sales page
- Post in German entrepreneur communities (see distribution list below)
- Run the quiz funnel live for the first time
- First full-price client validates product-market fit

### The 48h Delivery Promise — How to Fulfill It:

**When a client signs up:**
- Hour 0: Automated welcome email (already in n8n)
- Hour 2: Review their setup form — pick the 2 automations with highest ROI for their specific situation
- Hour 12: Start building in n8n
- Hour 24: First automation live — send Loom video walkthrough (use loom.com free plan)
- Hour 48: Full package delivered — webhook URLs, trigger instructions, "control panel" doc

**What to actually build for them (pick 2–3 based on their Q3 answer):**
- Lead follow-up: Contact form → CRM entry + auto-reply email
- Invoice reminders: Google Sheets / Stripe → automatic overdue email sequence
- Email triage: Gmail labels + priority tagging via n8n + Gmail API
- Social scheduling: Google Sheet → Buffer/Later publish queue
- Customer support: FAQ chatbot via n8n + OpenAI + WhatsApp/email

---

## PHASE 3: GROWTH (Days 22–90)
### Goal: Affiliate flywheel spinning. €1,000+ MRR. Content driving leads.

### The Affiliate Flywheel:

**Step 1:** Every client who pays gets an affiliate link in their onboarding email
**Step 2:** Include affiliate pitch in Email 5 and Email 6 of the sequence
**Step 3:** Send monthly "your affiliate report" email — even if they've earned €0 yet (keeps it top of mind)
**Step 4:** When someone earns their first €15, send a celebration email with their "next milestone" (€50, €100)
**Step 5:** "Refer 7 = free for life" — make this social-worthy. When they hit 7, send them a certificate/badge they can post

**Why this compounds:** A client who refers 2 people saves €100/month. They're now financially motivated to keep referring. Their audience trusts them more than any ad you could run.

### Content Strategy (Instagram + TikTok):

**Core Format — The "2-Minute Audit" Reel:**
- Hook: "I just automated [specific business owner]'s entire invoicing in 47 minutes"
- Show: the n8n workflow running (screen record — no face required if you don't want)
- Result: "She just got back 6 hours a month"
- CTA: "Find out what's wasting your time → link in bio" (links to quiz)

**Content Pillars (rotate these):**
1. **"Before/After"** — manual task → automated version. Takes 60 seconds. Gets saved.
2. **"The €X you're leaving on the table"** — ROI calculator content. Very shareable in entrepreneur communities.
3. **"What does [automation name] actually do?"** — demystify. Calm the fear of tech.
4. **"Behind the scenes"** — build a workflow live in 90 seconds. No explanation. Just show the result.
5. **"Myth busting"** — "You don't need to know how to code to automate your business" → repeat this 100 times

**Posting Schedule:**
- Week 1–4: 3x/week on Reels + TikTok (same content, posted separately)
- Week 5+: 5x/week once you have a content rhythm
- Never post "check out my service." Only post things that make people feel the pain or see the solution. Quiz link in bio does the selling.

**Hashtags (DE market):**
- #selbstständig #freelancer #unternehmerin #solopreneur #automatisierung #zeitsparen #n8n #agentur #digitalisierung #ki

**Growth hack for NL market:**
- NL has a massive freelancer culture (ZZP'ers) — post the same content with Dutch captions
- Hashtags: #zzp #ondernemer #automatisering #tijdbesparen #freelancernl

---

## DAY-BY-DAY ACTION PLAN: FIRST 14 DAYS

### DAY 1 (Thursday)
- [ ] Create Tally.so account → build the 6-question quiz (2h)
- [ ] Create Brevo account → verify domain → set up SPF/DKIM (1h)
- [ ] Create Stripe account → add bank account (30min)
- [ ] Register domain on Namecheap (~€10/year) — motionelevation.com or motion-elevation.de

### DAY 2 (Friday)
- [ ] Build the quiz result calculator in n8n (3h)
- [ ] Import Email 1-6 into Brevo → set up automation trigger (2h)
- [ ] Test full flow: quiz → score → email sequence (1h)

### DAY 3 (Weekend)
- [ ] Create Carrd landing page — hero section + pricing + about + CTA buttons (3h)
- [ ] Generate Impressum + Datenschutzerklärung at datenschutz-generator.de (30min)
- [ ] Add to Carrd page (mandatory)

### DAY 4 (Weekend)
- [ ] Write Loom welcome video script (5 minutes max)
- [ ] Build n8n onboarding workflow: Stripe webhook → welcome email → setup form → Telegram notification (2h)
- [ ] Test purchase flow end-to-end with €1 Stripe test payment

### DAY 5 (Monday)
- [ ] Identify first free client (personal network — freelancer, small business owner, anyone)
- [ ] Send them the setup form manually (don't wait for full automation)
- [ ] Build their first 2 automations (4h)
- [ ] Send Loom walkthrough

### DAY 6 (Tuesday)
- [ ] Client 1: follow up — is everything working? Any issues?
- [ ] Create LinkedIn profile for Motion Elevation if not already done
- [ ] Start writing first 3 Instagram/TikTok scripts (use the "Before/After" format)

### DAY 7 (Wednesday)
- [ ] Record first 3 Reels (screen record + voiceover, no face needed)
- [ ] Post first Reel on Instagram + TikTok
- [ ] Find 5 potential Client 2 candidates on LinkedIn (DACH solopreneurs posting about being busy)

### DAY 8 (Thursday)
- [ ] Send 5 DMs using the script below
- [ ] Ask Client 1 for testimonial (if they've had the service 3+ days)
- [ ] Post second Reel

### DAY 9 (Friday)
- [ ] Follow up on DMs (don't be weird, just one follow-up if no reply in 48h)
- [ ] Add Client 1 testimonial to Carrd landing page (even if it's just "saved me 8h/month — [First name], Freelancer")
- [ ] Post third Reel

### DAY 10 (Weekend)
- [ ] Close Client 2 at beta price (€50/month or €250 lifetime)
- [ ] Build their automations within 48h
- [ ] Research and identify 10 more outreach targets for next week

### DAY 11 (Monday)
- [ ] Post Reel #4 (if Client 2 consented, use their case as anonymous "before/after")
- [ ] Deliver Client 2 automations + Loom
- [ ] Find Reddit threads where your target audience is complaining about manual work

### DAY 12 (Tuesday)
- [ ] Reply helpfully in r/selbststaendig, r/Existenzgründung, r/freelance (German-language subs)
- [ ] No spammy links. Add value first. Mention Motion Elevation only if directly asked.
- [ ] Post Reel #5
- [ ] Ask Client 2 for testimonial

### DAY 13 (Wednesday)
- [ ] Send 10 more DMs to new prospects (now with 2 testimonials to reference)
- [ ] Post to German Facebook groups: "Selbstständige DE", "Freelancer Netzwerk", "Gründer Talk"
- [ ] Check Brevo stats: open rates, click rates on the 6 emails

### DAY 14 (Thursday)
- [ ] Review: how many leads came through the quiz? How many opened all 6 emails? Where do they drop off?
- [ ] Optimize the subject line of the lowest-performing email
- [ ] Target: 3 clients total by end of today (free/discounted counts)
- [ ] Post Reel #6 + write a short post celebrating "first week of automations delivered" (social proof)

---

## TOOL STACK (ALL FREE TIER)

| Tool | Purpose | Free Tier |
|------|---------|-----------|
| **Tally.so** | Quiz / lead capture form | Unlimited forms, 100 submissions/month |
| **n8n (self-hosted)** | All automation logic | Already on AWS EC2 — free |
| **Brevo** | Email marketing + sequences | 300 emails/day, unlimited contacts |
| **Carrd** | Landing page | 1 site free, $9/year for custom domain |
| **Stripe** | Payments | Free to set up, 1.4% + €0.25 per transaction |
| **Loom** | Delivery walkthroughs | 25 videos free |
| **Namecheap** | Domain | ~€10/year |
| **Google Sheets** | Affiliate tracking (Phase 1) | Free |
| **Notion** | Client management | Free |
| **CapCut** | Reel/TikTok editing | Free |
| **Canva** | Thumbnails, promo graphics | Free |
| **datenschutz-generator.de** | GDPR docs (Impressum, PP) | Free |

**When to upgrade (only if revenue justifies it):**
- Brevo paid plan (€19/month): when list > 1,000 people
- Rewardful ($29/month): when you have 5+ active affiliates
- Carrd paid ($9/year): from Day 1 if you want custom domain

---

## GDPR COMPLIANCE CHECKLIST 🇩🇪
### (Critical for DE/AT email marketing — ignore this and you risk €50k fines)

#### Before Collecting Any Emails:
- [ ] **Double opt-in is MANDATORY in Germany** — Brevo supports this natively. Turn it on. No exceptions.
- [ ] **Impressum** on every page — full name, address, email, phone number (legally required for .de businesses)
- [ ] **Datenschutzerklärung** (Privacy Policy) — use datenschutz-generator.de, update it to mention Brevo + Tally + Stripe by name
- [ ] **Cookie consent banner** — if using analytics. Easiest: don't use Google Analytics, use no-JS analytics like counter.dev (free) or skip analytics entirely for now
- [ ] **Separate email consent checkbox** in quiz — pre-checked boxes are illegal in Germany. Must be opt-in.

#### In Every Email:
- [ ] **Unsubscribe link** — Brevo adds this automatically. Verify it's working.
- [ ] **Physical address** in email footer — your full address (or registered business address)
- [ ] **Company name** in footer (even if it's just "Motion Elevation, [Your Name]")

#### For the Email Sequence:
- [ ] The Brevo automation must use **double opt-in confirmation** before sending Email 1
- [ ] Keep a record of when/how each contact gave consent (Brevo does this automatically — verify it in settings)
- [ ] **Do not import cold email lists** — only people who opted in through your quiz

#### Data Processing:
- [ ] **Brevo is GDPR-compliant** (EU-based servers, DPA available) — ✅ good choice
- [ ] **Tally.so** — review their privacy policy, add them to your Datenschutzerklärung
- [ ] **Stripe** — add as data processor in your Datenschutzerklärung
- [ ] **AWS EC2** — if n8n processes personal data (names, emails), note this in your privacy policy

#### Legal Structure Consideration:
- If operating in Germany as a natural person (Einzelunternehmer), your home address goes in the Impressum — this is public. If privacy is a concern, get a registered address (Impressumspflicht-Adresse) from services like Anschrift24 (~€3/month)

---

## OUTREACH SCRIPTS (DM Templates)

### Template 1 — LinkedIn (German)
**Subject line:** Kurze Frage zu deinem Business

Hallo [Name],

ich hab gesehen, dass du als [Freelancer/Agenturinhaber/...] in [Branche] arbeitest.

Ich baue gerade Motion Elevation auf – ein Done-for-You Automatisierungsservice für Selbstständige. Grundidee: du sagst mir, was dich die meiste Zeit kostet, ich baue die Automatisierung in 48h, und es läuft.

Gerade suche ich meine ersten 3 Beta-Kunden für Feedback. Das heißt: deutlich reduzierter Preis, dafür ehrliches Feedback danach.

Würde dich interessieren, was automatisierbar wäre bei dir? Ich hab einen kurzen Audit-Quiz, der in 90 Sekunden zeigt, wo du Zeit verlierst.

Kein Pitch, kein Druck – nur neugierig ob's passt.

Viele Grüße,
Lyubo

---

### Template 2 — LinkedIn (English, for NL market)
**Subject line:** Quick question about your workflow

Hey [Name],

I noticed you're running [type of business] — looks like you've got a solid operation going.

I'm launching Motion Elevation, a done-for-you automation service for small businesses and solopreneurs. The idea is simple: you tell me what's eating your time, I build the automations in 48h, and they run without you.

Looking for my first 3 beta clients right now — reduced price, honest feedback afterward.

No obligation — I built a 90-second quiz that shows exactly where you're losing time. Would you be curious to see your score?

Best,
Lyubo

---

### Template 3 — Instagram DM (short, casual)
Hey [Name]! Ich folg dir schon ne Weile – dein Content zu [topic] ist richtig gut.

Ich launch gerade einen Automatisierungsservice für Selbstständige und suche 3 Beta-Tester. Idee: du sagst mir welche Aufgaben dich am meisten Zeit kosten, ich bau die Automatisierung in 48h.

Interessiert dich das? Kein Pitch, nur ein kurzer Audit wenn du neugierig bist 🤙

---

### Template 4 — Reddit comment (organic, not spammy)
Wenn jemand klagt über Zeitverschwendung durch Admin-Arbeit:

> Ich bin gerade dabei, einen Automatisierungsservice speziell für Selbstständige zu launchen. Die häufigsten Zeitfresser die ich bei Freelancern sehe: Rechnungserinnerungen, Lead-Follow-ups und E-Mail-Sortierung. Das lässt sich alles automatisieren ohne dass man technisch sein muss.
>
> Falls du neugierig bist, wieviel Zeit du monatlich verlierst: ich hab einen kostenlosen Audit gebaut der in 90 Sekunden zeigt was bei dir automatisierbar wäre. Schreib mir kurz wenn du den Link willst.

---

## KPIs & WHAT SUCCESS LOOKS LIKE

### 30 Days:
- [ ] Quiz live and functional ✓
- [ ] 3 clients (1 free, 1 discounted, 1 full price) ✓
- [ ] 2 testimonials with real numbers ✓
- [ ] 50+ quiz completions ✓
- [ ] €100–200 MRR ✓
- [ ] Email sequence open rates: >40% (DE average is 26%) ✓
- [ ] 3 Reels/TikToks posted ✓

### 60 Days:
- [ ] 8–12 active clients ✓
- [ ] €800–1,200 MRR ✓
- [ ] 2+ affiliate links distributed ✓
- [ ] First affiliate referral ✓
- [ ] 200+ quiz completions ✓
- [ ] Email list: 100+ contacts ✓
- [ ] 1 piece of content hit 1,000+ views ✓

### 90 Days:
- [ ] 20–30 active clients ✓
- [ ] €2,000–3,000 MRR ✓
- [ ] 5+ active affiliates in the flywheel ✓
- [ ] 1 piece of content hit 10,000+ views (organic) ✓
- [ ] First affiliate earns free month ✓
- [ ] Email list: 500+ contacts ✓
- [ ] Product-market fit confirmed: <20% churn in first cohort ✓

### The Numbers That Actually Matter:
- **Quiz completion rate** (target: >60%)
- **Email → purchase conversion** (target: 2–5% of quiz takers)
- **Client retention rate** (target: >80% after 3 months)
- **Affiliate referral rate** (target: 20% of clients become affiliates)
- **Delivery time** (target: always <48h — this is your core promise)

---

## DISTRIBUTION CHANNELS (Where to find clients)

### Germany:
- LinkedIn — search "Freelancer" + "Agentur" + "selbstständig" in DE
- Reddit: r/selbststaendig, r/Existenzgründung, r/freelance (German posts)
- Facebook Groups: "Selbstständige Deutschland", "Freelancer Network Germany", "Online Business Deutschsprachig"
- XING (more popular in DE than LinkedIn for some demographics)
- German Twitter/X (still active, #Selbstständig, #Freelancer)

### Netherlands:
- LinkedIn — search "ZZP'er", "ondernemer", "freelance NL"
- Reddit: r/DutchBiz, r/Netherlands
- Facebook: "ZZP Nederland", "Freelancers NL"

### Austria:
- LinkedIn + Facebook Groups: "Selbstständige Österreich", "Unternehmer AT"

### Universal:
- Product Hunt — launch the quiz as a free tool ("Get your Automation Score in 90 seconds")
- Indie Hackers — post your journey/progress, the community loves transparent founder stories
- Hacker News "Show HN" — if you make something technically interesting

---

_Motion 🐋 — Built to move._

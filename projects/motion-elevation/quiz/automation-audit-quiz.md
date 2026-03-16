# Motion Elevation — Automation Audit Quiz
### Tally.so Implementation Guide

**Purpose:** Qualify inbound leads, identify pain points, segment by value tier, and trigger the correct follow-up sequence.

**Platform:** Tally.so (free plan supports logic jumps and email capture)  
**Estimated completion time:** 3–4 minutes  
**Trigger:** Shown after CTA click on landing page

---

## Quiz Header Copy

**Title:** "Your Free Automation Audit — Find Out Where You're Leaking Time & Money"

**Subheading:** "Answer 10 quick questions. We'll analyze your business and show you exactly which tasks you should never do manually again."

**Progress bar:** On (show progress at top)

---

## Question Flow

---

### Q1 — Email Capture (Gate)

**Field type:** Email input  
**Question:** "What's your best email address? (We'll send your personalized audit results here)"  
**Placeholder:** your@email.com  
**Required:** Yes  

**Signal:** Required to enter funnel. This is collected first so partial completions still capture the lead.

---

### Q2 — Business Type

**Field type:** Single choice  
**Question:** "What best describes your business?"

| Option | Signal |
|--------|--------|
| A) Real estate agent / team | High WTP niche — tag: `niche:realestate` |
| B) Online coach or course creator | High WTP niche — tag: `niche:coach` |
| C) E-commerce store | High revenue potential — tag: `niche:ecom` |
| D) Local service business (dental, salon, clinic, etc.) | Solid niche — tag: `niche:local` |
| E) Marketing or creative agency | White-label opportunity — tag: `niche:agency` |
| F) Other / Freelancer / Solopreneur | Needs nurture — tag: `niche:other` |

---

### Q3 — Business Size

**Field type:** Single choice  
**Question:** "How many people work in your business (including yourself)?"

| Option | Points | Signal |
|--------|--------|--------|
| A) Just me | 1 | Solo — likely budget-sensitive |
| B) 2–5 people | 2 | Small team — growing pains |
| C) 6–20 people | 3 | Established — strong automation candidate |
| D) 20+ people | 3 | Enterprise potential — escalate |

---

### Q4 — Monthly Revenue

**Field type:** Single choice  
**Question:** "What's your approximate monthly revenue?"

| Option | Points | Signal |
|--------|--------|--------|
| A) Under €1,000/month | 0 | Pre-revenue — nurture only |
| B) €1,000 – €5,000/month | 1 | Early stage — Starter tier candidate |
| C) €5,000 – €15,000/month | 2 | Growth stage — Growth tier candidate |
| D) €15,000 – €50,000/month | 3 | Established — Scale tier candidate |
| E) €50,000+/month | 3 | Enterprise — premium client |

**Logic:** If A → send to low-value nurture sequence only (don't book a call)

---

### Q5 — Biggest Time Drain

**Field type:** Single choice (with "pick the worst one")  
**Question:** "Which of these is your biggest time drain right now?"

| Option | Points | Signal |
|--------|--------|--------|
| A) Following up with leads and prospects | 3 | Lead nurture automation — high urgency |
| B) Scheduling meetings and appointments | 2 | Booking automation — quick win |
| C) Sending invoices and chasing payments | 2 | Revenue automation — clear ROI |
| D) Creating and sending reports | 2 | Reporting automation |
| E) Onboarding new clients or customers | 2 | CX automation |
| F) Customer support / answering the same questions | 3 | Chatbot / FAQ automation — high urgency |

---

### Q6 — Current Tool Stack

**Field type:** Single choice  
**Question:** "Do you currently use any CRM or marketing automation tools?"

| Option | Points | Signal |
|--------|--------|--------|
| A) No, I do everything manually or through email | 3 | Maximum pain — easiest sell |
| B) Yes, but I barely use its features | 2 | Tool graveyard — needs setup help |
| C) Yes, and I use it actively | 1 | Needs enhancement, not replacement |
| D) I have a full tech stack and it works well | 0 | Low urgency — hard sell |

---

### Q7 — Lead Volume

**Field type:** Single choice  
**Question:** "How many new leads or inquiries do you receive per month?"

| Option | Points | Signal |
|--------|--------|--------|
| A) 0–5 | 0 | Needs traffic first — automation is premature |
| B) 6–20 | 1 | Good foundation — automation will 2x conversions |
| C) 21–50 | 2 | Strong volume — leaking without automation |
| D) 50+ | 3 | Critical — losing money every day without it |

**Logic:** If A → tag `lead_volume:low` and don't pitch lead nurture automation; focus on other pain points.

---

### Q8 — Speed to Follow-Up

**Field type:** Single choice  
**Question:** "When a new lead comes in, how quickly do you typically respond?"

| Option | Points | Signal |
|--------|--------|--------|
| A) Within 5 minutes | 0 | On top of it — pitch other use cases |
| B) Within 1 hour | 1 | Good but improvable |
| C) Within 24 hours | 2 | Losing leads to faster competitors |
| D) It depends / sometimes days | 3 | Critical pain point — open with this in audit |
| E) Honestly, some fall through the cracks | 3 | Very high urgency — use in sales conversation |

---

### Q9 — Automation Familiarity

**Field type:** Single choice  
**Question:** "How familiar are you with business automation (tools like Zapier, Make, n8n)?"

| Option | Signal |
|--------|--------|
| A) Never heard of them | Tag: `skill:zero` — needs full onboarding |
| B) Heard of them but never used them | Tag: `skill:low` — light education needed |
| C) Used them a bit but gave up | Tag: `skill:mid` — overcame objection: complexity |
| D) I use them actively | Tag: `skill:high` — peer-level conversation, focus on ROI |

*This question doesn't affect score — it affects HOW you speak to them, not whether to pitch.*

---

### Q10 — Investment Readiness

**Field type:** Single choice  
**Question:** "If we could identify and fix your #1 automation gap this week, what would you be willing to invest per month to make that happen?"

| Option | Points | Signal |
|--------|--------|--------|
| A) I'm not ready to invest right now | 0 | Nurture only — send value content |
| B) €100–€300/month | 1 | Starter tier — pitch $297 plan |
| C) €300–€800/month | 2 | Growth tier — pitch $797 plan |
| D) €800–€1,500/month | 3 | Scale tier — book discovery call |
| E) More than €1,500/month | 3 | Enterprise — flag for personal outreach |

---

## Scoring System

**Add up points from Q3, Q4, Q5, Q6, Q7, Q8, Q10**  
Maximum possible: 21 points

| Score Range | Lead Tier | Action |
|-------------|-----------|--------|
| 0–6 | 🟡 Low Value | Nurture email sequence → free content → soft pitch in 30 days |
| 7–13 | 🟠 Mid Value | Email sequence → invite to group call or webinar → Starter/Growth pitch |
| 14–21 | 🔴 High Value | Personalized audit email within 24h → book 1-on-1 discovery call → Scale pitch |

---

## Lead Tier Actions

### 🟡 Low Value Lead (0–6 points)
**What it means:** Pre-revenue, not ready to invest, or very early stage.

**Action:**
1. Send welcome email with 3 "free automation wins you can implement today"
2. Add to long-term nurture sequence (monthly value emails)
3. Do NOT invite to sales call — waste of time
4. Re-score in 60 days if they open emails consistently
5. Offer a free Notion template or checklist as a trust builder

---

### 🟠 Mid Value Lead (7–13 points)
**What it means:** Active business, real pain points, some budget. Not quite ready to buy — needs proof.

**Action:**
1. Send personalized audit email referencing their specific answers
2. Invite to free group webinar: "5 Automation Wins in 30 Days"
3. Pitch Starter tier ($297/mo) with money-back framing
4. Follow up 3 days later with a case study relevant to their niche
5. If no reply after 7 days: send "still struggling with [pain point]?" email

---

### 🔴 High Value Lead (14–21 points)
**What it means:** Established business, active pain, budget available, ready to buy.

**Action:**
1. Send personalized audit within 24 hours — reference their exact answers
2. Include 1-page PDF showing what their automation stack could look like
3. Book a 45-minute 1-on-1 discovery call (Calendly link in email)
4. Come to the call with 3 specific automation wins pre-identified for their niche
5. Pitch Growth ($797) or Scale ($1,497) tier on the call
6. Send proposal within 24h of call

---

## Tally.so Setup Notes

**Form settings:**
- Redirect after submit: Thank-you page with "Check your inbox" message
- Email notifications: Notify you on every submission
- Integrations: Connect to your CRM (HubSpot free / Notion / Airtable) via Zapier
- Logic jumps: Hide Q7/Q8 if Q4 = "Under €1,000/month" (not ready for lead nurture pitch)

**Tag system:** Use Tally's hidden fields or webhook to pass tags to your email platform (ActiveCampaign, ConvertKit, MailerLite)

**Thank-you page copy:**
> "Your audit is on its way. Check your inbox in the next 10 minutes — we've analyzed your answers and are putting together your personalized automation roadmap. Can't wait? Book a call directly: [Calendly link]"

---

*Last updated: March 2026 | Motion Elevation*

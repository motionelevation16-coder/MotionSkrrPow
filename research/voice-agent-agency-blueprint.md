# 🎙️ Voice Agent Agency Blueprint

*Detailed implementation guide for our AI agency play*

---

## The Business Model

### What We're Selling
AI-powered phone agents that:
- Answer calls 24/7
- Book appointments
- Qualify leads
- Handle FAQs
- Transfer to humans when needed

### Why Businesses Will Pay
1. **Cost savings** — Human receptionist: $3,000-$4,000/month. Our AI: $500-$2,000/month
2. **24/7 coverage** — Never miss a call, even at 2 AM
3. **Consistency** — Same professional experience every time
4. **Scalability** — Handle 100 calls as easily as 1

---

## Target Market: Dental Clinics (Recommended First Niche)

### Why Dental?
- **High call volume** — Average dental office gets 50-100 calls/day
- **Repetitive inquiries** — "What insurance do you take?" "Do you have availability Tuesday?"
- **High patient value** — New patient worth $500-$2,000/year
- **Tech-friendly** — Already use practice management software
- **Clear ROI** — Every missed call = potential lost patient

### Market Size
- 200,000+ dental practices in US
- Average spends $3,500/month on front desk staff
- Even capturing 0.1% = 200 clients = **$200k-$400k MRR potential**

### Pain Points We Solve
1. Missed calls during lunch, after hours, busy times
2. Staff spending time on routine questions
3. No-shows (AI can handle reminders/confirmations)
4. New patient intake (AI collects info before visit)

---

## Service Packages

### Package 1: "Smart Answering" — $500/month
**What's included:**
- AI answers during business hours overflow
- Handles basic FAQs (hours, location, insurance)
- Takes messages for callbacks
- Transfers urgent calls

**Setup fee:** $1,000

### Package 2: "AI Receptionist" — $1,500/month
**What's included:**
- Everything in Smart Answering
- 24/7 coverage
- Appointment booking (integrated with calendar)
- New patient intake
- Appointment confirmations/reminders

**Setup fee:** $3,000

### Package 3: "Full Front Desk AI" — $3,000/month
**What's included:**
- Everything in AI Receptionist
- Insurance verification calls (outbound)
- Patient recall campaigns
- Review request follow-ups
- Custom workflows
- Monthly optimization calls

**Setup fee:** $5,000

---

## Tech Stack

### Core Platform Options

#### Option A: Bland AI (Recommended for starting)
- **Pros:** Easy to set up, good voice quality, native integrations
- **Cons:** Less customizable
- **Cost:** ~$0.09/minute
- **Best for:** Quick deployment, simpler use cases

#### Option B: Vapi AI
- **Pros:** Very customizable, good API
- **Cons:** Steeper learning curve
- **Cost:** ~$0.05-0.10/minute
- **Best for:** Complex workflows

#### Option C: Retell AI
- **Pros:** Enterprise-ready, great voice quality
- **Cons:** Higher cost
- **Cost:** ~$0.10-0.15/minute
- **Best for:** Premium clients

### Supporting Tools
- **Twilio** — Phone numbers, SMS
- **Cal.com** or **Calendly** — Appointment scheduling
- **Make.com** — Workflow automation
- **Airtable** — Client database, call logs

### Integration Points
- Practice management software (Dentrix, Eaglesoft, Open Dental)
- Google Calendar / Outlook
- CRM systems
- Payment processors (for deposits)

---

## Agent Prompt Template (Dental)

```markdown
# Dental Office AI Receptionist

## Your Identity
You are Sarah, a friendly and professional receptionist at [Practice Name].
You speak naturally, with warmth and efficiency.
You NEVER mention you're an AI unless directly asked.

## Practice Information
- Name: [Practice Name]
- Address: [Address]
- Phone: [Phone]
- Hours: Monday-Friday 8am-5pm, Saturday 9am-1pm
- Dentists: Dr. [Name 1], Dr. [Name 2]
- Services: General dentistry, cosmetics, implants, orthodontics
- Insurance: We accept most major plans including Delta, Cigna, Aetna, MetLife
- Emergency: For dental emergencies outside hours, call [emergency number]

## Call Handling Rules

### New Patient Inquiries
1. Warmly greet them
2. Ask what brought them to call today
3. Collect: Name, phone, email, insurance (if any)
4. Ask about their primary concern
5. Offer next available appointment
6. Confirm all details

### Existing Patient - Appointment
1. Verify identity (name, DOB)
2. Check availability
3. Book or reschedule as needed
4. Confirm date/time
5. Send text confirmation

### Insurance Questions
1. Ask which insurance they have
2. If we accept it, confirm and offer to verify benefits
3. If unsure, offer to have someone call them back with details

### Emergencies
If caller mentions: severe pain, swelling, bleeding, knocked out tooth, broken tooth:
1. Express concern
2. Ask brief questions about the issue
3. Offer same-day emergency appointment OR
4. Transfer to staff immediately if during hours
5. Provide emergency number if after hours

### Transfer Triggers
Transfer to human staff when:
- Caller requests to speak with a person
- Complex insurance issues
- Complaints
- Caller seems confused or frustrated
- Medical questions beyond scheduling

## Conversation Style
- Be warm but efficient
- Use the caller's name
- Confirm important details by repeating them
- End calls positively: "We look forward to seeing you!"
```

---

## Sales Process

### Lead Generation
1. **Google My Business** — "AI receptionist for dentists"
2. **Facebook Ads** — Target dental practice owners
3. **Cold Email** — Scrape dental office emails, personalized outreach
4. **LinkedIn** — Connect with practice managers
5. **Dental Conferences** — Virtual booths, speaking slots
6. **Referrals** — Offer $500 for successful referrals

### Sales Script (Cold Call/Email)

**Subject:** Never miss another patient call at [Practice Name]

Hi [Name],

Quick question: How many calls does [Practice Name] miss during lunch, after hours, or when the front desk is busy?

For most dental offices, it's 20-30% of calls. At $500+ per new patient, that adds up fast.

We've built an AI receptionist specifically for dental practices that:
- Answers every call 24/7
- Books appointments directly into your calendar  
- Handles insurance questions
- Costs less than a part-time hire

Practices using it report 40% more appointments booked and zero missed calls.

Worth a 15-minute demo? I can show you exactly how it would work for [Practice Name].

[Calendar Link]

Best,
[Name]

### Demo Flow
1. **Show, don't tell** — Call the demo number live on Zoom
2. **Play back recordings** — Real calls from other dental offices
3. **Show the dashboard** — Call logs, analytics, easy management
4. **Calculate ROI** — "If you're missing 10 calls/week and 20% are new patients..."
5. **Offer trial** — "Let's test it for 2 weeks, free"

---

## Operational Setup

### Client Onboarding (Week 1)
1. **Kickoff call** (30 min)
   - Collect practice info
   - Understand their specific needs
   - Get calendar access
   - Set up phone forwarding

2. **Agent customization** (2-3 hours)
   - Build custom prompt with their info
   - Set up integrations
   - Test all scenarios

3. **Training call** (30 min)
   - Show them the dashboard
   - Explain how to update info
   - Set expectations

4. **Go live** (monitored)
   - Forward calls to AI
   - Monitor first 20-30 calls
   - Quick adjustments

### Ongoing Management (per client)
- **Weekly:** Review call logs, catch issues (15 min)
- **Monthly:** Analytics report, optimization suggestions (30 min)
- **Quarterly:** Strategy call, upsell opportunities (30 min)

**Time per client after setup:** ~2-3 hours/month

### Scaling Math
- 10 clients = 20-30 hours/month = part-time
- 20 clients = 40-60 hours/month = full-time equivalent
- 50+ clients = Need to systematize or hire

---

## Financial Model

### Unit Economics (per client)
| Item | Package 2 ($1,500/mo) |
|------|----------------------|
| Revenue | $1,500 |
| AI costs (~500 min/mo) | -$50 |
| Twilio | -$30 |
| Tools (prorated) | -$20 |
| **Gross Profit** | **$1,400 (93%)** |

### Path to $10k MRR
| Month | Clients | MRR | Notes |
|-------|---------|-----|-------|
| 1 | 1 | $1,500 | First client (hustle!) |
| 2 | 3 | $4,500 | Referral + cold outreach |
| 3 | 5 | $7,500 | Systems working |
| 4 | 7 | $10,500 | **$10k MRR achieved** |

**Setup fees in Month 1-4: $15,000-$25,000 additional**

---

## What I (Motion) Can Build

### Ready to Build NOW
1. ✅ Prompt templates for dental, real estate, HVAC
2. ✅ Demo voice agent for pitching
3. ✅ Client onboarding checklist
4. ✅ Integration scripts (calendar, CRM)
5. ✅ Analytics dashboard template

### Need Lyubo For
1. Choose platform (Bland AI vs Vapi vs Retell)
2. Set up business entity / payments
3. First sales calls
4. Client relationship management

---

## Next Steps

1. [ ] **Today:** Pick platform, sign up for free trial
2. [ ] **This week:** Build demo agent (I do this)
3. [ ] **This week:** Create landing page (I do this)
4. [ ] **Next week:** Cold outreach to 50 dental offices (Lyubo)
5. [ ] **Week 3:** First demo calls
6. [ ] **Week 4:** First paying client

---

*Blueprint by Motion 🐋*
*Let's build this thing.*

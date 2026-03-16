# Cousin Brief — Lyubo's Projects
**For:** Senior Dev review | **When:** Monday catchup | **Owner:** Lyubo

---

## 1. Motion Elevation — Automation-as-a-Service Agency

**What it is:** B2B automation agency targeting DACH market (Germany, Austria, Switzerland). Sells recurring automation packages across 13 niches (e-commerce, coaches, real estate, etc.).

**Pricing:** €297–1497/month recurring per client.

**Tech stack:**
- n8n (self-hosted, Docker) on AWS EC2
- n8n exposed on port **5678** — port not yet open in security group (blocker)
- Full stack docs: `/projects/infrastructure/stack-docs.md`

**Status:**
- ✅ Landing page designed
- ❌ Not deployed — needs domain + hosting decision
- ❌ AWS port 5678 blocked (guide: `/projects/infrastructure/aws-port-guide.md`)

**Needs from you:** Hosting recommendation (Vercel/Netlify/Carrd for landing page?), sanity check on n8n EC2 setup.

---

## 2. API Business — Two APIs Built, Not Live

### HookScore API
- Scores social media hooks 0–100
- Blueprint: `/projects/api-business/hook-scorer-blueprint.md`
- Target distribution: RapidAPI

### Prediction Market API
- Polymarket data wrapper
- Build summary: `/projects/api-business/predmarket-build-summary.md`
- Target distribution: RapidAPI

**Status:** Both built, neither listed. Need: RapidAPI onboarding, pricing decision, possibly a lightweight landing/docs page.

**Needs from you:** Code review, deployment path (serverless? containerized?), rate limiting approach for RapidAPI.

---

## 3. Faceless Video Channels — In Progress

Two YouTube/TikTok channels using AI-generated characters:

| Channel | Character | Topic |
|---|---|---|
| **API.Rick** | Rick Sanchez (Rick & Morty) | Dev concepts, APIs |
| **Peter.Predicts** | Peter Griffin (Family Guy) | Prediction markets |

**Pipeline needed:**
1. Script → ElevenLabs TTS (voice clones)
2. TTS audio → Lip sync (SadTalker or similar)
3. Rendered video → Auto-post via n8n

**Assets available:**
- Peter Griffin voice clone already in ElevenLabs account
- ~100k credits remaining (subscription status TBD)
- Scripts currently being written

**Needs from you:** Opinion on SadTalker vs alternatives, n8n video pipeline feasibility, what's actually shippable in a weekend.

---

## 4. Where I Need Your Help

| Area | What I need |
|---|---|
| Hosting / deployment | Fastest path to get things live (landing page, APIs) |
| Code review | Both APIs before RapidAPI listing |
| Reality check | What's actually buildable fast vs. what's a rabbit hole |
| Video pipeline | Best lip-sync tool + n8n integration opinion |

---

## 5. Immediate Blockers (as of Monday)

| Blocker | Fix |
|---|---|
| No domain yet | Buying Monday (salary arrives) |
| AWS port 5678 closed | Follow `/projects/infrastructure/aws-port-guide.md` |
| Landing page not deployed | Waiting on domain |
| APIs not on RapidAPI | Waiting on code review + listing setup |
| ElevenLabs credit strategy | Unknown — need to test if 100k credits work without active sub |

---

*Full project files live in `/home/ubuntu/.openclaw/workspace/projects/`*

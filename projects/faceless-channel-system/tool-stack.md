# Faceless Channel — Complete Tool Stack
*Prices current as of early 2026. All verdict choices are commitments, not suggestions.*

---

## 1. Script Generation (AI)

### Option A: Claude 3.5 Sonnet (Anthropic)
- **Price:** $20/month (Claude Pro) or pay-per-use via API ($3/1M input tokens)
- **What it does:** Best-in-class long-form script writing. Maintains consistent tone, follows complex formatting instructions, doesn't hallucinate as much as GPT on factual content.
- **Free tier:** Yes — Claude.ai has a free tier (limited messages/day)
- **Verdict note:** Best for nuanced, editorial scripts

### Option B: ChatGPT-4o (OpenAI)
- **Price:** $20/month (ChatGPT Plus) or API ($5/1M input tokens for 4o)
- **What it does:** Excellent for structured scripts, listicles, YouTube-style hooks. GPT Store has pre-built script writer GPTs.
- **Free tier:** Yes — GPT-3.5 free, GPT-4o has limited free access
- **Verdict note:** Best for short-form, formulaic content

### Option C: Perplexity AI
- **Price:** $20/month (Pro)
- **What it does:** Writes scripts WITH cited sources in real-time. Perfect for news/finance content where accuracy matters.
- **Free tier:** Yes — limited queries/day

**✅ VERDICT: Use Claude for script writing.** It produces cleaner, more natural-sounding narration than GPT-4o. The output requires less editing. Set up via API and integrate directly into n8n. For news-style content, use Perplexity to research → paste into Claude to write.

---

## 2. Voiceover / TTS

### Option A: ElevenLabs
- **Price:** $5/month (Starter: 30k chars), $22/month (Creator: 100k chars), $99/month (Pro: 500k chars)
- **What it does:** Industry-leading voice cloning and TTS. 3,000+ voices. Voice cloning from 1 min of audio. API available.
- **Free tier:** Yes — 10k characters/month
- **Verdict note:** Best quality, best API

### Option B: Murf.ai
- **Price:** $29/month (Basic), $59/month (Pro)
- **What it does:** Good TTS with built-in video sync. More of an all-in-one editor but voice quality is slightly below ElevenLabs.
- **Free tier:** Yes — 10 min of audio/month
- **Verdict note:** Good if you want built-in editor, overkill otherwise

### Option C: Play.ht
- **Price:** $31.2/month (Creator), $49/month (Unlimited)
- **What it does:** Competitive TTS with ultra-realistic voices. Good API. Emotion control.
- **Free tier:** Yes — 12,500 chars/month
- **Verdict note:** Solid alternative if ElevenLabs pricing gets too high at volume

**✅ VERDICT: ElevenLabs, Creator plan ($22/month).** The API integration with n8n is seamless, the voice quality is unmatched, and 100k chars/month covers ~40-50 short videos or ~10-15 long-form videos. Start with a pre-made voice (Adam, Rachel, or Bella are popular) before cloning your own.

---

## 3. AI Video Generation

### Option A: Kling AI (Kuaishou)
- **Price:** Free tier (limited), Pro ~$10/month (~600 credits), ~$0.035/credit for standard clips
- **What it does:** Chinese AI video tool that produces stunning 5-10 second clips. Best at realistic motion, facial expressions, cinematic scenes. Kling 2.0 is state-of-art.
- **Free tier:** Yes — limited daily credits
- **Verdict note:** Best quality/price ratio for short clips

### Option B: Runway Gen-4
- **Price:** $15/month (Standard: 625 credits), $35/month (Pro: 2,250 credits). ~1 credit per second of video.
- **What it does:** Western alternative to Kling. Excellent for abstract/cinematic visuals. Better at consistency with reference images.
- **Free tier:** Yes — 125 credits free
- **Verdict note:** Better for abstract/art-style content

### Option C: Pika Labs
- **Price:** $8/month (Basic), $28/month (Pro)
- **What it does:** Fast generation, good for animated-style content and motion graphics. Less realistic than Kling but faster.
- **Free tier:** Yes — limited generations
- **Verdict note:** Good for animated explainer style

**✅ VERDICT: Kling AI for realistic scenes, Runway for cinematic/abstract.** You'll likely use both. Start with Kling's free tier to test. Budget $10-35/month combined at start.

---

## 4. Stock Footage Sources

### Option A: Pexels / Pixabay
- **Price:** Free
- **What it does:** Royalty-free stock footage. 50k+ clips. No attribution required on Pexels.
- **Free tier:** Fully free
- **Verdict note:** Use for filler footage, backgrounds, generic scenes

### Option B: Storyblocks (now Envato Elements competitor)
- **Price:** $15/month (Individual), $30/month (Business)
- **What it does:** Unlimited HD/4K stock footage downloads. 1M+ clips. Also includes music, sound effects, templates.
- **Free tier:** No, but 7-day trial
- **Verdict note:** If you're doing high volume, unlimited downloads pays off fast

### Option C: Artgrid
- **Price:** $199/year (~$16.50/month)
- **What it does:** Premium cinematic stock footage shot by independent filmmakers. Much higher quality than Pexels.
- **Free tier:** No, but 30-day trial
- **Verdict note:** For premium channels that need cinematic B-roll

**✅ VERDICT: Start with Pexels (free) + Storyblocks ($15/month) once you're producing 5+ videos/week.** The unlimited model makes economic sense at volume. Artgrid only if you're running a premium history/documentary-style channel.

---

## 5. AI Avatar Tools

### Option A: HeyGen
- **Price:** $29/month (Creator: 3 avatars, 15 min video), $89/month (Business: unlimited)
- **What it does:** Best AI avatar platform. Realistic talking head videos from script. 100+ stock avatars. Custom avatar creation. Multilingual dubbing.
- **Free tier:** Yes — 1 min free video/month
- **Verdict note:** Industry standard. Best quality.

### Option B: Synthesia
- **Price:** $30/month (Starter: 10 min/month), $90/month (Creator: 30 min)
- **What it does:** Professional-grade avatars, popular for corporate/training content. 230+ avatars, 140 languages.
- **Free tier:** No (free demo video only)
- **Verdict note:** Slightly more "corporate" look than HeyGen

### Option C: D-ID
- **Price:** $5.9/month (Lite: 10 min), $49.9/month (Pro: 100 min)
- **What it does:** Animates still photos to talk. Good for custom avatar look. Also does streaming avatars.
- **Free tier:** Yes — 5 min trial
- **Verdict note:** Most affordable entry point. Quality lower than HeyGen.

**✅ VERDICT: HeyGen at $29/month.** The quality gap between HeyGen and competitors is significant. For a "faceless" channel, having a believable talking head is the whole point — don't cheap out here.

---

## 6. Video Editing / Assembly

### Option A: CapCut (Desktop)
- **Price:** Free (CapCut desktop), $7.99/month (Pro for team/advanced features)
- **What it does:** Most powerful free video editor for content creators. Auto-captions, templates, transitions, background removal, speed controls, beat sync. Direct TikTok/YouTube export.
- **Free tier:** Yes — desktop version is essentially full-featured free
- **Verdict note:** Best free option. Mobile app also excellent.

### Option B: Descript
- **Price:** $24/month (Creator), $40/month (Business)
- **What it does:** Edit video by editing the transcript. Delete words from text = deletes from video. Auto-filler-word removal, overdub (clone your voice to fix mistakes), screen recording.
- **Free tier:** Yes — 1 hour transcription/month
- **Verdict note:** Revolutionary for voiceover-heavy content. Edit script = edit video.

### Option C: Pictory
- **Price:** $25/month (Starter: 200 min/month), $49/month (Professional: 600 min)
- **What it does:** Paste a script → auto-generates video with stock footage, captions, music. Designed for exactly this workflow.
- **Free tier:** Yes — 3 projects free
- **Verdict note:** Most automated but least control

**✅ VERDICT: CapCut for assembly (free), Descript for editing ($24/month if doing voiceover-heavy content).** Use CapCut as your primary editor — the free tier is genuinely powerful. Add Descript only if you're editing lots of long-form voiceover content where transcript editing saves significant time.

---

## 7. Thumbnail Generation

### Option A: Canva (AI features)
- **Price:** Free (basic), $14.99/month (Pro)
- **What it does:** Drag-and-drop design with AI image generation, background removal, Magic Design templates. 1M+ templates.
- **Free tier:** Yes — generous free tier
- **Verdict note:** Best for quick thumbnail iteration

### Option B: Midjourney
- **Price:** $10/month (Basic: 200 images/month), $30/month (Standard: unlimited relaxed)
- **What it does:** Best-in-class AI image generation. Thumbnail backgrounds, dramatic scenes, custom illustrations. Requires Discord.
- **Free tier:** No (removed in 2024)
- **Verdict note:** Highest quality for AI-generated thumbnail images

### Option C: Adobe Firefly (via Photoshop)
- **Price:** Included in Adobe CC ($55/month), or standalone $9.99/month (100 credits)
- **What it does:** AI image generation with commercial license. Integrates with Photoshop for precise editing.
- **Free tier:** Yes — 25 generative credits/month

**✅ VERDICT: Canva Pro ($14.99/month) + Midjourney Basic ($10/month).** Canva for the layout/text/design, Midjourney for the background image. Generate the hero image in Midjourney → import into Canva → add text overlay + channel branding. This produces thumbnails that look genuinely professional.

---

## 8. Auto-Publishing / Scheduling

### Option A: n8n (self-hosted or cloud)
- **Price:** Free (self-hosted), $20/month (Cloud Starter), $50/month (Cloud Pro)
- **What it does:** Workflow automation. Connect Google Sheets → ElevenLabs → YouTube → Telegram. The backbone of the entire automation stack.
- **Free tier:** Yes — fully free self-hosted. Cloud has free trial.
- **Verdict note:** The single most important tool in the stack

### Option B: Zapier
- **Price:** $19.99/month (Starter: 750 tasks), $49/month (Professional: 2k tasks)
- **What it does:** Same concept as n8n but simpler, less powerful, more expensive per task.
- **Free tier:** Yes — 100 tasks/month (barely useful)
- **Verdict note:** n8n is better in every way except ease of setup

### Option C: YouTube Studio Scheduling (native)
- **Price:** Free
- **What it does:** Schedule videos up to 6 months in advance directly in YouTube Studio. No API needed.
- **Free tier:** Fully free
- **Verdict note:** Use this for manual scheduling when n8n isn't set up yet

**✅ VERDICT: n8n (cloud $20/month or self-hosted free).** If you have any technical ability at all, self-host n8n on a $6/month Hetzner VPS. It's free forever and handles unlimited workflows. If not, $20/month cloud plan covers the basics.

---

## 9. Analytics

### Option A: YouTube Studio (native)
- **Price:** Free
- **What it does:** Full analytics — impressions, CTR, watch time, audience retention, revenue, traffic sources. Everything you actually need.
- **Free tier:** Fully free (built into YouTube)
- **Verdict note:** Start here. Don't overthink analytics tools.

### Option B: VidIQ
- **Price:** Free (basic), $16.58/month (Pro), $49.50/month (Max)
- **What it does:** SEO optimization, keyword research, competitor analysis, daily ideas, view velocity tracking. Browser extension overlays data on YouTube.
- **Free tier:** Yes — basic keyword research and competitor tracking
- **Verdict note:** Best YouTube SEO tool

### Option C: TubeBuddy
- **Price:** Free (basic), $4.99/month (Pro), $14.99/month (Legend)
- **What it does:** Similar to VidIQ. Tag explorer, A/B thumbnail testing, bulk processing.
- **Free tier:** Yes — more generous than VidIQ's free tier
- **Verdict note:** Better free tier, slightly less powerful paid tier

**✅ VERDICT: YouTube Studio (free) + VidIQ free tier for keyword research.** You don't need to pay for analytics until you're doing 100k+ views/month. Focus on making videos, not analyzing them obsessively at the start.

---

## Full Stack Monthly Cost Summary

| Tool | Plan | Cost/month |
|------|------|-----------|
| Claude API | Pay-per-use | ~€5-15 |
| ElevenLabs | Creator | €22 |
| Kling AI | Pro | €10 |
| Pexels | Free | €0 |
| HeyGen | Creator | €29 |
| CapCut | Free | €0 |
| Canva | Pro | €15 |
| Midjourney | Basic | €10 |
| n8n | Self-hosted | €6 (VPS only) |
| VidIQ | Free | €0 |
| **Total (with avatar)** | | **~€97/month** |
| **Total (without avatar)** | | **~€68/month** |

**Note:** You don't need all of these on Day 1. Start with the free tiers. Only pay when the free tier becomes a bottleneck.

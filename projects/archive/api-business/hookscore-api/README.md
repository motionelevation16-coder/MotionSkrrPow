# HookScore API

Score, classify, rewrite, and compare social media hooks using AI.
Built with FastAPI + OpenAI GPT-4o-mini.

---

## What It Does

HookScore is an API that helps content creators write better hooks — the first line of a TikTok, Instagram caption, YouTube title, tweet, or LinkedIn post. It:

- **Scores** any hook 0-100 with grade, strengths, and weaknesses
- **Suggests** 5 improved rewrites in your chosen tone
- **Compares** two hooks head-to-head
- **Classifies** the hook type (curiosity gap, hot take, story hook, etc.)
- **Batch ranks** up to 20 hooks at once
- **Analyzes** emoji impact on hook performance

---

## Setup (Run Locally)

### 1. Prerequisites

- Python 3.10 or higher ([download](https://www.python.org/downloads/))
- An OpenAI API key ([get one here](https://platform.openai.com/api-keys))

### 2. Clone / Download the files

Put all the project files in one folder.

### 3. Install dependencies

Open a terminal in the project folder and run:

```bash
pip install -r requirements.txt
```

### 4. Set your OpenAI API key

Copy `.env.example` to `.env`:

```bash
cp .env.example .env
```

Open `.env` and replace `your_key_here` with your actual OpenAI API key:

```
OPENAI_API_KEY=sk-proj-...your-key-here...
```

### 5. Start the server

```bash
uvicorn main:app --reload
```

The API will be available at: `http://localhost:8000`

Visit `http://localhost:8000/docs` for the interactive documentation.

---

## Deploy to Railway.app

Railway is the easiest way to get this API live on the internet (free tier available).

### Step-by-step:

1. **Create a Railway account** at [railway.app](https://railway.app) (sign in with GitHub)

2. **Push your code to GitHub:**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin https://github.com/YOUR_USERNAME/hookscore-api.git
   git push -u origin main
   ```

3. **Create a new Railway project:**
   - Go to [railway.app](https://railway.app) → New Project
   - Choose "Deploy from GitHub repo"
   - Select your `hookscore-api` repository

4. **Set the environment variable:**
   - In Railway, go to your project → Variables tab
   - Click "New Variable"
   - Name: `OPENAI_API_KEY`
   - Value: your OpenAI API key (starts with `sk-`)
   - Click Add

5. **Deploy:**
   - Railway will auto-deploy. Wait ~1-2 minutes.
   - Click "Generate Domain" in the Settings tab to get a public URL

6. **Test it:**
   - Visit `https://your-app.railway.app/health` — should return `{"status":"ok","version":"1.0.0"}`
   - Visit `https://your-app.railway.app/docs` for the full interactive docs

---

## List on RapidAPI

Once your Railway URL is live:

1. **Create a RapidAPI account** at [rapidapi.com](https://rapidapi.com/provider) → "Add New API"

2. **Fill in the basics:**
   - API Name: `HookScore`
   - Category: `Social`
   - Description: (see `rapidapi-listing.md` for full copy)

3. **Add your base URL:**
   - Base URL: `https://your-app.railway.app`

4. **Create endpoints** (one by one in RapidAPI UI):
   - POST `/score` — Hook Scorer
   - POST `/suggest` — Hook Rewriter
   - POST `/compare` — Hook Comparator
   - POST `/classify` — Hook Classifier
   - POST `/batch` — Batch Ranker
   - POST `/emoji-impact` — Emoji Impact Analyzer

5. **Set pricing:**
   - Free plan: 50 requests/day
   - Basic plan: 500 requests/day — $9.99/month
   - Pro plan: 5,000 requests/day — $29.99/month

6. **Publish** — RapidAPI handles all rate limiting, billing, and key management.

---

## API Quick Reference

### Score a hook
```bash
curl -X POST https://your-app.railway.app/score \
  -H "Content-Type: application/json" \
  -d '{"hook": "I quit my 9-5 and made more in one week", "platform": "tiktok"}'
```

### Get rewrite suggestions
```bash
curl -X POST https://your-app.railway.app/suggest \
  -H "Content-Type: application/json" \
  -d '{"hook": "Tips for growing on Instagram", "platform": "instagram", "tone": "shocking"}'
```

### Compare two hooks
```bash
curl -X POST https://your-app.railway.app/compare \
  -H "Content-Type: application/json" \
  -d '{"hook_a": "5 habits that changed my life", "hook_b": "The one habit billionaires share", "platform": "youtube"}'
```

### Classify a hook
```bash
curl -X POST https://your-app.railway.app/classify \
  -H "Content-Type: application/json" \
  -d '{"hook": "Nobody talks about this investment strategy"}'
```

### Batch rank hooks
```bash
curl -X POST https://your-app.railway.app/batch \
  -H "Content-Type: application/json" \
  -d '{"hooks": ["Hook one", "Hook two", "Hook three"], "platform": "tiktok"}'
```

### Analyze emoji impact
```bash
curl -X POST https://your-app.railway.app/emoji-impact \
  -H "Content-Type: application/json" \
  -d '{"hook": "🔥 This productivity hack will change your life 💯"}'
```

---

## Environment Variables

| Variable | Required | Description |
|---|---|---|
| `OPENAI_API_KEY` | ✅ Yes | Your OpenAI API key |
| `PORT` | Auto-set by Railway | Port to run on (Railway sets this automatically) |

---

## Costs

This API calls OpenAI GPT-4o-mini. Approximate costs:
- `/score`: ~$0.0005 per request
- `/suggest`: ~$0.001 per request
- `/batch` (20 hooks): ~$0.003 per request
- All others: ~$0.0005–0.001 per request

GPT-4o-mini is extremely affordable. 1,000 requests ≈ $0.50–1.00 in OpenAI costs.

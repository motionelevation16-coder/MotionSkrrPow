# Reddit OAuth Setup Guide
**For: OpenClaw reddit-readonly skill on AWS EC2**
**Level: Beginner-friendly**

---

## Why You Need This

Reddit blocks scraping from server IPs (AWS, DigitalOcean, etc.) unless you authenticate properly with OAuth. This guide walks you through creating a Reddit "app" that gives OpenClaw permission to read Reddit data legitimately.

Total time: ~10 minutes.

---

## Step 1: Log Into Reddit

1. Go to **https://www.reddit.com**
2. Log in with your Reddit account (or create one — free)
3. Make sure you're logged in before continuing

> 💡 Use your personal Reddit account. You're just reading data, not posting anything.

---

## Step 2: Go to the Reddit App Developer Page

1. In your browser, go to: **https://www.reddit.com/prefs/apps**
2. You'll see a page titled **"authorized applications"**
3. Scroll to the very bottom — you'll see a button that says **"create another app..."** or **"create app"**

> 📸 *[Screenshot: The Reddit prefs/apps page with a grey "create app" button at the bottom of the page]*

---

## Step 3: Create a New App

Click **"create app"** (or "create another app"). A form will appear.

Fill it in like this:

| Field | What to Enter |
|-------|--------------|
| **name** | `MotionElevation-Reader` (or anything you like) |
| **App type** | Select **"script"** (important!) |
| **description** | Leave blank |
| **about url** | Leave blank |
| **redirect uri** | Type: `http://localhost:8080` |
| **permissions** | Leave as default |

> 📸 *[Screenshot: The app creation form with "script" selected as the app type and localhost:8080 as redirect URI]*

Click the **"create app"** button at the bottom of the form.

---

## Step 4: Copy Your Credentials

After clicking create, you'll see your new app listed. It looks like a small card with text on it.

You need **two pieces of information**:

1. **client_id** — This is the string of random characters shown **directly under the app name** (looks like: `aBcDeFgH1234567`)
2. **client_secret** — This is labeled "secret" in the app card (looks like: `xYzAbCdEfGhIjKlMnOpQrStUvWxYz`)

> 📸 *[Screenshot: The app card showing the client_id under the app name (a short alphanumeric string) and the "secret" field below it]*

> ⚠️ **Keep these secret.** Don't share them publicly or commit them to GitHub.

Write them down or copy them to a secure note:
```
client_id:     ________________________
client_secret: ________________________
```

---

## Step 5: Configure OpenClaw

Now tell OpenClaw to use your Reddit credentials.

### Option A: Environment Variables (Recommended)

SSH into your server and run:

```bash
ssh ubuntu@13.62.48.252
```

Then open the OpenClaw config file:

```bash
nano ~/.openclaw/.env
```

Add these lines (replace with your actual values):

```env
REDDIT_CLIENT_ID=your_client_id_here
REDDIT_CLIENT_SECRET=your_client_secret_here
REDDIT_USERNAME=your_reddit_username
REDDIT_PASSWORD=your_reddit_password
```

Save the file: press `Ctrl+X`, then `Y`, then `Enter`.

### Option B: OpenClaw Skill Config

Check if the reddit skill has its own config file:

```bash
ls ~/.npm-global/lib/node_modules/openclaw/skills/reddit-readonly/
```

If there's a `config.json` or `.env.example`, follow the format shown there.

---

## Step 6: Restart OpenClaw

After saving your credentials:

```bash
openclaw gateway restart
```

Wait 10 seconds, then test:

```bash
openclaw chat "Search Reddit for posts about n8n automation"
```

If it works, you'll get real Reddit posts back instead of an error. ✅

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| "401 Unauthorized" | Double-check client_id and client_secret — no extra spaces |
| "403 Forbidden" | Make sure you selected "script" as app type (not "web app") |
| Still getting blocked | Reddit may rate-limit new apps — wait 5 minutes and try again |
| Can't find client_id | It's the short string directly under your app name on the prefs/apps page |

---

## Security Notes

- Never share your `client_secret` publicly
- The app only has **read** access — it cannot post on your behalf
- Your Reddit credentials are stored locally on the server only
- If credentials are ever compromised, go to https://www.reddit.com/prefs/apps and click "delete app"

---

*Last updated: 2026-03-06 | Motion Elevation Infrastructure*

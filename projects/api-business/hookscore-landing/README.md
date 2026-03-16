# 🎣 HookScore Landing Page

Professional landing page for the **HookScore API** — score, rewrite, and A/B test short-form content hooks.

## Deploy to GitHub Pages in 3 Steps

### Step 1 — Push to GitHub

```bash
# If you haven't already, initialize git in this folder
git init
git add .
git commit -m "feat: HookScore landing page"

# Create a new repo on GitHub, then:
git remote add origin https://github.com/YOUR_USERNAME/hookscore-landing.git
git branch -M main
git push -u origin main
```

### Step 2 — Enable GitHub Pages

1. Go to your repo on GitHub
2. Click **Settings** → **Pages** (left sidebar)
3. Under **Source**, select **Deploy from a branch**
4. Choose `main` branch, `/ (root)` folder
5. Click **Save**

### Step 3 — Visit Your Live Page

After ~60 seconds, your page will be live at:

```
https://YOUR_USERNAME.github.io/hookscore-landing/
```

That's it. No build step. No npm. No config files. Just push and ship. 🚀

---

## Files

| File | Purpose |
|------|---------|
| `index.html` | Full landing page (all sections) |
| `style.css` | All styles — dark SaaS aesthetic |
| `README.md` | This file |

## Customizing

- **RapidAPI URL** — search for `rapidapi.com/search/hookscore` in `index.html` and replace with your actual listing URL
- **Colors** — change `--accent` in `style.css` (`:root`) to any hex color
- **Copy** — all text is in plain HTML, easy to find and edit
- **Contact email** — update `hello@hookscore.dev` in the footer

## Tech Stack

- Pure HTML5 + CSS3 + vanilla JavaScript
- Google Fonts (Inter + Space Grotesk)
- Zero dependencies, zero build tools
- Mobile responsive
- Works offline (except fonts)

---

Built for the creator economy. © 2026 HookScore API.

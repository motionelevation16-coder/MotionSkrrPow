# 🐋 Twitter Scanner for Polymarket

Scans Twitter for viral posts, news accounts, and prediction market gurus.
Built for Peter Griffin Polymarket persona content ideas.

## ⚠️ Current Status

**Twitter/X has locked down scraping** — both snscrape and Nitter are blocked/down.

**Working options:**
1. **Twitter API** — $100/month (Basic tier), reliable
2. **RapidAPI Twitter scrapers** — $10-30/month, some work
3. **Manual browser automation** — Free but requires your login cookies

For now, the config and structure are ready. Add your API key when available.

## Setup

```bash
cd projects/polymarket/twitter-scanner
pip install -r requirements.txt
```

## Usage

### Full scan (default 24 hours)
```bash
python scanner.py
```

### Quick scan (last 6 hours)
```bash
python scanner.py --hours 6
```

### Custom config
```bash
python scanner.py --config my-config.json
```

## Configuration

Edit `config.json` to customize:

- **accounts**: Twitter accounts to monitor (news, gurus, traders)
- **hashtags**: Hashtags to track
- **keywords**: Keywords to search
- **viral_threshold**: Minimum engagement for "viral" classification
- **scan_hours**: How far back to scan

## Output

Results are saved to `output/`:
- `scan_YYYYMMDD_HHMM.json` — Full data
- `summary_YYYYMMDD_HHMM.md` — Readable summary
- `latest.json` / `latest.md` — Symlinks to most recent scan

## Content Ideas

The scanner generates content angles for Peter Griffin style posts:
- Political betting takes with degen humor
- Whale watching commentary
- Odds analysis with meme reactions
- L compilations / copium content
- W celebrations / gains content

## Automation

Add to cron for daily scans:
```bash
0 9 * * * cd /path/to/twitter-scanner && python scanner.py >> scan.log 2>&1
```

---
*Part of the Motion workspace 🐋*

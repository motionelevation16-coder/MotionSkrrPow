# 🐋 Polymarket Content Engine

Automated content discovery for Peter Griffin Predictions persona.

## What It Does

1. **Polymarket Scanner** - Finds hot markets, big moves, controversial bets
2. **Reddit Scanner** - Monitors r/polymarket, r/PredictionMarket discussions
3. **Daily Briefing** - Combined alert with script prompts ready to use

## Quick Start

```bash
cd projects/polymarket/content-engine

# Run daily scan (saves to output/)
python3 daily_scan.py

# Or run individually:
python3 polymarket_scanner.py --alert
python3 reddit_scanner.py
```

## Output

After running, check `output/TODAY.md` for:
- Top 5 Polymarket opportunities
- Top 5 Reddit discussions
- Ready-to-paste ChatGPT script prompts
- Today's action checklist

## Daily Workflow

1. Run `python3 daily_scan.py`
2. Open `output/TODAY.md`
3. Pick ONE topic
4. Copy script prompt → paste into ChatGPT
5. Edit script, record, post

## Automation

Ask Motion to set up a cron job for daily scans:
```
0 10 * * * cd /path/to/content-engine && python3 daily_scan.py
```

---
*Part of the Motion workspace 🐋*

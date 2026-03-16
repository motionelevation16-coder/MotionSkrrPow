# Motion Elevation — Full Stack Documentation
**For: Senior Developer Onboarding**
**Read time: ~10 minutes**

---

## TL;DR

A single AWS EC2 instance running Ubuntu, Docker, and n8n. n8n is the automation engine. OpenClaw is an AI agent assistant. GitHub stores code. Stack is minimal, self-hosted, and designed for fast iteration by a non-technical founder.

---

## Architecture Overview

```
Internet
    │
    ▼
[AWS EC2 Instance]
IP: 13.62.48.252
OS: Ubuntu (LTS)
    │
    ├── UFW Firewall
    │     ├── Port 22  → SSH
    │     └── Port 5678 → n8n
    │
    ├── Docker
    │     └── n8n container (port 5678)
    │           └── Auth: username/password enabled
    │
    └── OpenClaw (v2026.3.2)
          └── AI agent runtime (installed globally via npm)
```

---

## Components

### 1. AWS EC2 Instance

| Property | Value |
|----------|-------|
| Provider | AWS (region: eu-north-1 or eu-west based on IP) |
| Public IP | 13.62.48.252 |
| OS | Ubuntu 22.04+ LTS |
| Access | SSH via port 22 |
| SSH User | `ubuntu` |

**SSH Access:**
```bash
ssh ubuntu@13.62.48.252
```
(Requires the private key `.pem` file stored locally)

**Security Groups (AWS-level firewall):**
- Port 22 open (SSH)
- Port 5678 open (n8n)

**UFW (OS-level firewall):**
```bash
sudo ufw status
# Should show: 22 and 5678 ALLOW
```

---

### 2. Docker

Docker is the containerization layer. n8n runs inside Docker rather than being installed directly on the OS — this makes it easier to update, restart, and isolate.

**Useful commands:**
```bash
# See running containers
docker ps

# See all containers (including stopped)
docker ps -a

# View n8n logs
docker logs n8n --tail=50 -f

# Restart n8n
docker restart n8n

# Stop n8n
docker stop n8n

# Start n8n
docker start n8n
```

**n8n Container Details:**
```bash
docker inspect n8n
# Check: ports, volumes, env variables
```

**Data persistence:**
n8n stores its data in a Docker volume. Check with:
```bash
docker volume ls
docker volume inspect n8n_data  # or similar name
```

---

### 3. n8n (Automation Engine)

n8n is a workflow automation tool — like Zapier/Make, but self-hosted. Lyubo uses it to connect services and automate business processes.

| Property | Value |
|----------|-------|
| URL | http://13.62.48.252:5678 |
| Auth | Username/password enabled |
| Username | lyubo |
| Protocol | HTTP (not HTTPS — see Security section) |

**Current / Planned Workflows:**
- Tally.so form → Lead scoring → Brevo → Telegram alert
- (Future) Social media post scheduling
- (Future) Prediction market monitoring

**n8n folder structure (inside container):**
```
/home/node/.n8n/
├── config           # n8n configuration
├── database.sqlite  # SQLite DB (all workflow data)
└── nodes/           # Custom nodes if any
```

**To update n8n:**
```bash
docker pull n8nio/n8n
docker stop n8n
docker rm n8n
# Re-run with original docker run command (check command history or startup script)
docker run -d \
  --name n8n \
  -p 5678:5678 \
  -e N8N_BASIC_AUTH_ACTIVE=true \
  -e N8N_BASIC_AUTH_USER=lyubo \
  -e N8N_BASIC_AUTH_PASSWORD=<password> \
  -v n8n_data:/home/node/.n8n \
  n8nio/n8n
```

> ⚠️ Check the exact docker run command used on this server before updating:
> ```bash
> docker inspect n8n | grep -A 20 '"Cmd"'
> ```

---

### 4. OpenClaw (AI Agent Runtime)

OpenClaw is an AI agent platform that turns Claude (Anthropic's AI) into a persistent assistant with access to the server and external services.

| Property | Value |
|----------|-------|
| Version | v2026.3.2 |
| Installation | npm global (`~/.npm-global/`) |
| Config dir | `~/.openclaw/` |
| Workspace | `~/.openclaw/workspace/` |
| Channel | Telegram (Lyubo chats with it via Telegram) |

**Key files:**
```
~/.openclaw/
├── workspace/
│   ├── SOUL.md      # Agent personality
│   ├── USER.md      # Info about Lyubo
│   ├── MEMORY.md    # Long-term agent memory
│   ├── memory/      # Daily logs
│   └── projects/    # Project files (like this one)
└── .env             # API keys and config
```

**Skills (plugins):**
Located at: `~/.npm-global/lib/node_modules/openclaw/skills/`
- `reddit-readonly` — Browse Reddit
- `weather` — Weather queries
- `tmux` — Terminal session control
- `healthcheck` — Security auditing
- `skill-creator` — Build new skills

**Restart OpenClaw gateway:**
```bash
openclaw gateway restart
openclaw gateway status
```

---

### 5. GitHub

| Property | Value |
|----------|-------|
| Account | motionelevation16-coder |
| Repo | MotionSkrrPow |
| URL | https://github.com/motionelevation16-coder/MotionSkrrPow |

Currently used for: code storage, possibly automation scripts.

---

## Network Topology

```
[Lyubo's Phone/Laptop]
         │
         │ HTTPS (Telegram API)
         ▼
  [Telegram Servers]
         │
         │ (OpenClaw connects to Telegram)
         ▼
  [EC2: 13.62.48.252]
         │
         ├── OpenClaw listens for Telegram messages
         │
         └── n8n receives webhooks from:
               - Tally.so (form submissions)
               - Future: other services
```

---

## External Services (Connected or Planned)

| Service | Purpose | Status |
|---------|---------|--------|
| Telegram | Lyubo ↔ OpenClaw chat | ✅ Active |
| Tally.so | Lead capture forms | 🔧 Configuring |
| Brevo | Email marketing | 🔧 Configuring |
| Reddit API | Content research | 🔧 Needs OAuth |
| Slack | VIP lead notifications | 📋 Planned |
| GitHub | Code repository | ✅ Active |

---

## Security Posture

### Current State (Honest Assessment)

| Area | Status | Notes |
|------|--------|-------|
| SSH | ✅ Key-based | Good |
| UFW firewall | ✅ Minimal ports | Good |
| n8n auth | ✅ Password required | Good |
| HTTPS/TLS | ❌ HTTP only | Risk — data in plaintext |
| Fail2ban | ❓ Unknown | Check: `sudo systemctl status fail2ban` |
| Automatic updates | ❓ Unknown | Check: `apt list --upgradable` |
| Backups | ❓ Unknown | n8n SQLite not backed up? |

### Recommended Improvements (Priority Order)

1. **Add HTTPS to n8n** — Install Nginx + Certbot (Let's Encrypt)
   ```bash
   # Install nginx + certbot
   sudo apt install nginx certbot python3-certbot-nginx
   ```
   Requires a domain name pointed at the server IP.

2. **Enable automatic security updates**
   ```bash
   sudo apt install unattended-upgrades
   sudo dpkg-reconfigure --priority=low unattended-upgrades
   ```

3. **Install fail2ban** (blocks brute force SSH attempts)
   ```bash
   sudo apt install fail2ban
   sudo systemctl enable fail2ban
   ```

4. **Set up daily n8n SQLite backup** to S3 or GitHub

---

## Maintenance Runbook

### Daily Checks (Quick)
```bash
# Are things running?
docker ps

# Any disk issues?
df -h

# Check n8n logs for errors
docker logs n8n --tail=20
```

### Weekly Checks
```bash
# Security updates available?
sudo apt list --upgradable

# OpenClaw status
openclaw gateway status
```

### How to Restart Everything After a Reboot
```bash
# n8n should auto-start if --restart=always was set in docker run
# Check:
docker inspect n8n | grep RestartPolicy

# If not auto-starting:
docker start n8n
openclaw gateway start
```

### Backup n8n Data
```bash
# Copy SQLite database off the server
# Run this from your local machine:
scp ubuntu@13.62.48.252:/path/to/n8n/database.sqlite ./n8n-backup-$(date +%Y%m%d).sqlite
```

---

## Cost Breakdown (Estimated Monthly)

| Service | Cost |
|---------|------|
| EC2 instance (t3.micro or similar) | ~€8–15/month |
| AWS data transfer | ~€0–2/month |
| Brevo (free tier, 300/day) | €0 |
| Tally.so (free tier) | €0 |
| Telegram | €0 |
| **Total** | **~€8–17/month** |

---

## Common Issues & Fixes

| Problem | Diagnosis | Fix |
|---------|-----------|-----|
| n8n not accessible | `docker ps` — is n8n running? | `docker start n8n` |
| n8n workflow not triggering | Check webhook URL matches | Verify URL in Tally settings |
| OpenClaw not responding | `openclaw gateway status` | `openclaw gateway restart` |
| Server unreachable | Check AWS Console → EC2 → Instance state | Start instance if stopped |
| Disk full | `df -h` shows 100% | Clear Docker logs: `docker system prune` |

---

## Contacts & Ownership

- **Owner:** Lyubo (motionelevation16-coder)
- **GitHub:** https://github.com/motionelevation16-coder/MotionSkrrPow
- **Server IP:** 13.62.48.252
- **Infrastructure docs:** `~/.openclaw/workspace/projects/infrastructure/`

---

*Last updated: 2026-03-06 | Motion Elevation Infrastructure*

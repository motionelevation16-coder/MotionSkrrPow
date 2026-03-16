# AWS Security Group Guide
**How to Open Port 5678 for n8n**
**Level: Complete beginner**

---

## What This Does

Your EC2 server has a "Security Group" — think of it as a bouncer at the door. Right now, it might be blocking port 5678 (the port n8n runs on) from outside access. This guide shows you how to tell AWS: "Let port 5678 through."

Total time: ~5 minutes.

---

## Before You Start

You'll need:
- ✅ Your AWS account login (email + password)
- ✅ Your MFA device (phone with Authenticator app)
- ✅ Know which EC2 instance is your server (IP: `13.62.48.252`)

---

## Step 1: Log Into AWS Console

1. Go to **https://console.aws.amazon.com**
2. Enter your **email address** and click **Next**
3. Enter your **password** and click **Sign in**
4. When prompted for MFA, open your **Authenticator app** (Google Authenticator, Authy, etc.) and enter the 6-digit code

> 📸 *[Screenshot: AWS sign-in page with email field, then password field, then MFA prompt showing a 6-digit code input box]*

You're in! You'll see the AWS Management Console dashboard.

---

## Step 2: Find Your EC2 Instance

1. In the **search bar at the top** of the page, type: `EC2`
2. Click on **"EC2"** in the dropdown (it has an orange/yellow server icon)

> 📸 *[Screenshot: AWS top navigation bar with search field showing "EC2" typed, and the EC2 service appearing in dropdown results]*

3. On the left sidebar, click **"Instances"**
4. You'll see a list of your servers. Find the one with IP **13.62.48.252**
   - Check the **"Public IPv4 address"** column

> 📸 *[Screenshot: EC2 Instances list showing a table with columns including Instance ID, Instance state, Public IPv4 address]*

5. **Click on the Instance ID** (the link that starts with `i-`) of your server

---

## Step 3: Find the Security Group

1. After clicking your instance, you'll see a details panel at the bottom
2. Click the **"Security"** tab (it's one of several tabs: Details, Security, Networking, etc.)
3. Under **"Security groups"**, you'll see a link like `sg-0abc123def456` — click it

> 📸 *[Screenshot: EC2 instance detail page with Security tab selected, showing a security group link like "sg-0abc123def456 (launch-wizard-1)"]*

---

## Step 4: Edit Inbound Rules

1. You're now on the Security Group page
2. Click the **"Inbound rules"** tab
3. Click the orange button: **"Edit inbound rules"**

> 📸 *[Screenshot: Security Group page showing Inbound rules tab with a list of existing rules (SSH on port 22, etc.) and an "Edit inbound rules" button]*

---

## Step 5: Add the New Rule for Port 5678

You'll see a table of rules. There's already one for SSH (port 22). Now add one for n8n.

1. Click **"Add rule"** at the bottom of the table
2. A new row appears. Fill it in:

| Column | What to Select/Type |
|--------|---------------------|
| **Type** | Select `Custom TCP` from dropdown |
| **Protocol** | Auto-fills to `TCP` |
| **Port range** | Type `5678` |
| **Source** | Select `Anywhere-IPv4` (this allows all IPs) |
| **Description** | Type `n8n web interface` |

> 📸 *[Screenshot: Edit inbound rules form with a new row added showing "Custom TCP", "TCP", "5678", "0.0.0.0/0" (Anywhere-IPv4), and description "n8n web interface"]*

> ⚠️ **Security note:** Selecting "Anywhere-IPv4" means anyone on the internet can reach port 5678. Since n8n has a login (username + password), this is acceptable. If you want extra security later, you can restrict to your home IP only.

---

## Step 6: Save the Rule

1. Click the orange **"Save rules"** button at the bottom right
2. You'll see a green success banner: **"Inbound rules successfully modified"**

> 📸 *[Screenshot: Success banner in green at the top of the page saying "Inbound rules successfully modified"]*

---

## Step 7: Test It!

Open your browser and go to:

```
http://13.62.48.252:5678
```

You should see the **n8n login page**! Log in with:
- Username: `lyubo`
- Password: (the one you set when you installed n8n)

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| Page won't load | Make sure n8n is running: SSH in and run `docker ps` to check |
| Still blocked | Double-check the port is `5678` and source is `0.0.0.0/0` |
| "Connection refused" | n8n container may have stopped — run `docker start $(docker ps -a -q --filter name=n8n)` |
| AWS Console looks different | AWS updates its UI — look for "Security Groups" in the EC2 left sidebar if you get lost |

---

## Optional: Lock It Down to Your IP Only (More Secure)

If you only want to access n8n from your home/office:

1. Google "what is my IP" — you'll see something like `87.123.45.67`
2. In the Source column, instead of "Anywhere-IPv4", type your IP with `/32` at the end: `87.123.45.67/32`
3. Save rules

Now only your IP can access n8n.

---

## Quick Reference: Current Firewall Status

| Port | Service | Status |
|------|---------|--------|
| 22 | SSH | ✅ Open |
| 5678 | n8n | ✅ Open (after this guide) |

---

*Last updated: 2026-03-06 | Motion Elevation Infrastructure*

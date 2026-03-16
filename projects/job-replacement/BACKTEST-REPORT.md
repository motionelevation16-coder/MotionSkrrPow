# n8n Workflow Backtest Report

*Analyzed: 2026-03-04 | By: Motion (subagent)*

---

## Summary Table

| Workflow | Status | Critical Bugs | Minor Issues |
|---|---|---|---|
| Email Triage Bot | ⚠️ Needs Fix | 1 | 3 |
| Lead Follow-Up Sequence | ❌ Broken | 3 | 2 |
| Social Media Auto-Poster | ⚠️ Needs Fix | 2 | 3 |

---

## 1. AI Email Triage Bot ⚠️ Needs Fix

**What it's supposed to do:** Poll Gmail for unread emails → AI classifies + drafts response → apply labels, send urgent alerts via Telegram, create drafts, log to Sheet.

**Logic & flow:** Conceptually solid. The Gemini API call, parse step, branching by priority/response-needed — all makes sense.

### Critical Bug

**Node 4 (Code) has 4 output connections — impossible.**  
```json
"4": {"main": [
  [{"node": "5"}],  // output 0
  [{"node": "6"}],  // output 1
  [{"node": "8"}],  // output 2
  [{"node": "10"}]  // output 3
]}
```
A Code node in n8n only has **1 output**. This JSON implies 4 parallel branches, which n8n will not execute correctly — nodes 6, 8, and 10 simply won't trigger. This needs to be restructured.

**Fix:** Chain the nodes sequentially after node 4:
`4 → 5 (Apply Labels) → 6 (Check Urgent) → [branch] → 8 (Check Response) → [branch] → 10 (Log)`

### Minor Issues

1. **Gmail label IDs vs names:** Node 5 feeds `$json.labels` (which are label *names* from the AI) directly into `labelIds`. Gmail API needs actual label IDs, not human-readable names. Fix: either pre-map label names to IDs, or create a lookup step.

2. **`sheetId` parameter name:** Node 10 uses `sheetId` but newer n8n Google Sheets nodes expect `documentId`. Will fail silently or error on import depending on n8n version.

3. **Gemini JSON body construction:** The prompt body is a deeply escaped JSON string embedded in a JSON value. This works but is extremely fragile — any special characters in the email body (quotes, backslashes) can break the parse. Suggested fix: use n8n's Code node to build the request body programmatically instead.

---

## 2. Automated Lead Follow-Up Sequence ❌ Broken

**What it's supposed to do:** Receive new lead via webhook → send 3 emails spaced 2-3 days apart → skip remaining emails if lead responds → update sheet stage.

**Logic & flow:** The email sequence concept is good. The timing and content of the 3 emails are well-written. But the implementation has fundamental n8n mechanics issues.

### Critical Bugs

**Bug 1: Cross-wait node data references are broken.**  
Nodes 6 and 10 (Filter) reference `$node['Add to Sheet'].json.email` — data from node 2, which ran before the `Wait` nodes. After a Wait node resumes, **n8n only carries the data from the node immediately before the wait**. The original lead email is lost.

**Fix:** Before each Wait node, store the lead email in a static location (env var won't work per-run). The correct pattern is to use a webhook resume with the email as a query param, or store the lead's row number and re-fetch from the sheet using a field that identifies this specific run. Alternatively, pass data through via the Wait node's "Resume" functionality using a unique key.

**Bug 2: `$json.row` in Node 12 doesn't exist.**  
`"range": "Leads!F{{$json.row}}"` — `$json.row` is not a property returned by Google Sheets read operations by default. Without enabling "Return Row Numbers" option on the Sheets read node, this will be `undefined` and the update will target `Leads!Fundefined`.

**Fix:** Enable "Return Row Numbers" on the Sheets read nodes (nodes 5 and 9), and update the range expression accordingly.

**Bug 3: Response detection is not implemented.**  
The filter nodes check `$json.responded == "no"` but nothing in this workflow ever sets `responded = yes`. The doc mentions a "separate workflow" for this, but it's not included. Without it, **every lead gets all 3 emails regardless of whether they responded.** A client could receive a breakup email after already booking a call.

**Fix:** Either include the reply-detection workflow in the package, or clearly document (with a setup step) that this critical piece must be configured separately before the sequence is used.

### Minor Issues

4. **Filter logic after reads:** Nodes 6 and 10 filter the entire sheet to find this lead's row — but with hundreds of leads this will iterate many rows. Low impact at small scale but should use a lookup-by-email approach instead.

5. **No Gmail credential setup guidance:** The workflow uses Gmail for sending but there's no mention of needing `sendTo` permission (which requires the Gmail node to be set up with send access, not just read access used in the triage bot).

---

## 3. Social Media Auto-Poster ⚠️ Needs Fix

**What it's supposed to do:** Every 3 hours, read a Google Sheet, find posts scheduled for now or past, post to Twitter/Instagram/LinkedIn, mark as posted, alert on errors.

**Logic & flow:** Good structure. The two-step Instagram API (create container → publish) is correct. Error handler concept is right.

### Critical Bugs

**Bug 1: Missing `=` prefix on env var expressions (Node 2 and Node 9).**  
```json
"sheetId": "{{$env.GOOGLE_SHEET_ID}}"
```
Should be:
```json
"sheetId": "={{$env.GOOGLE_SHEET_ID}}"
```
Without the leading `=`, n8n treats this as a literal string, not an expression. The sheet lookup will fail with an invalid sheet ID error. Same issue in Node 9.

**Bug 2: Error trigger node (10) is misused.**  
The `errorTrigger` node type is meant to be the *start* of a **separate** error-handling workflow — not embedded inside the main workflow. The `"settings": {"errorWorkflow": "10"}` references node ID 10, but n8n's `errorWorkflow` setting expects a **workflow ID** (a different workflow entirely), not a node ID within the current workflow.

**Fix:** Create a separate "Error Handler" workflow that starts with an `errorTrigger` node. Set the main workflow's error workflow setting to that workflow's ID. Remove nodes 10 and 11 from the main workflow.

### Minor Issues

3. **Twitter node may be outdated:** `n8n-nodes-base.twitter` has been deprecated in favor of `n8n-nodes-base.twitterV2` in n8n v1.x. Depending on client's n8n version, this node won't exist and the workflow will fail to import cleanly.

4. **`row_number` not available by default:** Node 9 uses `$json.row_number` to target the correct row for the status update. Google Sheets read doesn't return row numbers unless explicitly enabled. Fix: enable "Return Row Numbers" option on Node 2.

5. **Switch node exact-match only:** The `Route by Platform` switch only handles `twitter`, `instagram`, `linkedin` as exact string matches. If the sheet has `"twitter,instagram"` (multi-platform post), the switch falls through with no match and nothing gets posted. The detailed guide mentions supporting multi-platform posts. Fix: either use IF nodes with `contains` conditions instead of Switch, or require one row per platform in the sheet.

---

## Comparison with N8N-WORKFLOWS-DETAILED.md

The detailed guide is written in German and documents 3 *different* workflows (Content Creator, E-Commerce/Shopify, Coach/Calendly onboarding) — not the same 3 workflows in the JSON files. The JSON templates appear to be a simplified/adapted English version aimed at automation freelancers selling to clients.

The guide itself is solid reference material. Key things in the guide that are **missing or weaker** in the JSON templates:
- Guide specifies cron times (09:00, 14:00, 19:00) — JSON uses "every 3 hours" (no specific time)
- Guide mentions LinkedIn via HTTP Request with proper API structure — JSON uses `n8n-nodes-base.linkedIn` node (simpler but version-dependent)
- Guide documents HMAC webhook validation for Shopify — not relevant to these workflows but shows more security awareness
- Guide has a dedicated Logs sheet for every workflow — JSON templates only partially implement this

---

## Overall Verdict: **Needs Work Before Selling**

These are **promising templates at 70% completion**, not production-ready products. A client who imports these and follows the setup instructions will hit walls:

- Lead Follow-Up will spam responded leads ❌
- Social Auto-Poster env vars won't work (missing `=`) ❌  
- Email Triage logging and branching will silently fail ⚠️

**What needs to happen before selling:**

| Priority | Fix |
|---|---|
| 🔴 High | Fix Email Triage node 4 multi-output (restructure connections) |
| 🔴 High | Fix Social Poster env var expressions (add `=` prefix) |
| 🔴 High | Fix Lead Sequence cross-wait references + add response detection |
| 🔴 High | Fix Lead Sequence row update (`$json.row` → actual row number) |
| 🟡 Medium | Fix Error Handler — move to separate workflow |
| 🟡 Medium | Fix Gmail label IDs vs names |
| 🟡 Medium | Update Twitter node type to v2 |
| 🟢 Low | Enable row numbers on all Sheets read nodes |
| 🟢 Low | Add multi-platform handling to Switch node |

**Estimated fix time:** 3-5 hours of n8n hands-on work to patch all issues and test with live credentials.

**After fixes:** These are genuinely useful, well-scoped workflows. The email content, AI classification approach, and overall architecture are solid. Worth selling at the planned price point once patched.

---

*Report generated by Motion subagent for Lyubo's job-replacement project.*

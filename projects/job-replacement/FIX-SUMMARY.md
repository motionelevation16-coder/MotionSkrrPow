# Fix Summary — n8n Workflow JSON Patches

*Fixed: 2026-03-04 | By: Motion (subagent)*

---

## 1. AI Email Triage Bot ✅ Fixed

**Critical bug fixed:**
- **Node 4 multi-output**: Removed the impossible 4-output connection from the Code node. Restructured connections to chain sequentially: `4 → 5 (Apply Labels) → 6 (Check Urgent) → [urgent branch → 7] → 8 (Check Response) → [response branch → 9] → 10 (Log)`. Both IF branches merge back into the next step so logging always fires.

**Minor fixes:**
- **`sheetId` → `documentId`**: Fixed parameter name on Node 10 (Log to Sheet) for modern n8n Google Sheets node compatibility.
- **Gmail label ID warning**: Added a detailed note to Node 5 (Apply Labels) explaining that AI-generated label *names* must be mapped to actual Gmail label *IDs* before this node will work. Included step-by-step guidance in the node note.
- **Setup instructions updated**: Added step 4 about the label ID mapping requirement.

---

## 2. Automated Lead Follow-Up Sequence ✅ Fixed

**Critical bugs fixed:**
- **Cross-wait data loss**: Added two new Set nodes:
  - `3a` — "Preserve Lead Email (Pre-Wait 1)": runs after welcome email, before Wait node 4. Stores `lead_email`, `lead_name`, `lead_company`.
  - `7a` — "Preserve Lead Email (Pre-Wait 2)": runs after follow-up 1, before Wait node 8. Same fields.
  - Filter nodes 6 and 10 now reference `$node['Preserve Lead Email (Pre-Wait X)'].json.lead_email` instead of the broken `$node['Add to Sheet'].json.email`.

- **`$json.row` → `$json._row`**: Fixed the range expression in Node 12 (Update Stage to Closed) from `Leads!F{{$json.row}}` to `Leads!F{{$json._row}}`. Also enabled `returnRowNumbers: true` on Node 9 (Check Responded Again) so the field is actually populated.

- **Response detection**: Added a sticky note (node `99`) with a red warning that the response detection workflow is **required separately** and that the sequence must NOT be activated in production without it. Detailed the exact workflow needed.

---

## 3. Social Media Auto-Poster ✅ Fixed

**Critical bugs fixed:**
- **Missing `=` prefix on env var expressions**: Fixed in Node 2 (`"sheetId": "{{$env.GOOGLE_SHEET_ID}}"` → `"sheetId": "={{$env.GOOGLE_SHEET_ID}}"`) and Node 9 (same fix).
- **Error workflow misuse**: Removed nodes 10 (errorTrigger) and 11 (Telegram alert) from the main workflow — these cannot live inside a main workflow in n8n. Cleared the invalid `"errorWorkflow": "10"` setting. Added a sticky note (node `98`) explaining exactly how to create the separate error handler workflow and link it.

**Minor fixes:**
- **Twitter node type**: Updated Node 5 from `n8n-nodes-base.twitter` (deprecated) to `n8n-nodes-base.twitterV2` for n8n v1.x compatibility. Parameters unchanged.
- **`returnRowNumbers` enabled**: Added `"returnRowNumbers": true` to Node 2 (Get Content from Sheet) so `$json._row` is available in Node 9 for the row update.
- **`$json.row_number` → `$json._row`**: Fixed the range expression in Node 9 from `Content!A{{$json.row_number}}:G{{$json.row_number}}` to `Content!A{{$json._row}}:G{{$json._row}}`.

---

## Status After Fixes

| Workflow | Before | After |
|---|---|---|
| Email Triage Bot | ⚠️ Broken branching, wrong param | ✅ Sequential chain, correct params |
| Lead Follow-Up | ❌ Data lost after waits, broken row ref | ✅ Email preserved, row ref fixed, warning added |
| Social Auto-Poster | ⚠️ Env vars failed, wrong node type | ✅ Expressions fixed, twitterV2, error note added |

All three workflows should now import into n8n without errors. The remaining setup steps (Gmail label ID mapping, response detection workflow, error handler workflow) are documented in node notes and sticky notes within each workflow.

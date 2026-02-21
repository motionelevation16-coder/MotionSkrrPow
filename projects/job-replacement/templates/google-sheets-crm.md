# Free CRM: Google Sheets Template

Copy this structure to create a simple but effective CRM.

---

## Sheet 1: Leads

| Column | Format | Notes |
|--------|--------|-------|
| A: Created | Date | Auto: =TODAY() on entry |
| B: Name | Text | Full name |
| C: Email | Text | Primary email |
| D: Company | Text | Company name |
| E: Title | Text | Job title |
| F: Source | Dropdown | LinkedIn, Twitter, Cold Email, Referral, Inbound |
| G: Niche | Dropdown | Content Creator, E-commerce, Local Service, Agency, etc. |
| H: Status | Dropdown | New, Contacted, Replied, Call Scheduled, Proposal, Won, Lost |
| I: Last Contact | Date | When you last reached out |
| J: Next Action | Text | What to do next |
| K: Next Date | Date | When to do it |
| L: Notes | Text | Context, conversation notes |
| M: Value | Currency | Estimated monthly value |
| N: LinkedIn | URL | Profile link |
| O: Website | URL | Company website |

---

## Sheet 2: Pipeline

| Column | Format | Notes |
|--------|--------|-------|
| A: Lead Name | Text | Link to Leads sheet |
| B: Stage | Dropdown | Discovery, Proposal, Negotiation, Closing |
| C: Value | Currency | Monthly recurring |
| D: Close Date | Date | Expected close |
| E: Probability | Percent | 25%, 50%, 75%, 90% |
| F: Weighted | Formula | =C*E |
| G: Owner | Text | Who's handling |
| H: Next Step | Text | Immediate action |
| I: Blockers | Text | What's slowing it down |

### Pipeline Formula (Monthly Forecast)
```
=SUMPRODUCT(C:C, E:E)
```

---

## Sheet 3: Clients

| Column | Format | Notes |
|--------|--------|-------|
| A: Name | Text | Company name |
| B: Contact | Text | Primary contact |
| C: Email | Text | Contact email |
| D: Package | Dropdown | Starter, Growth, Scale |
| E: MRR | Currency | Monthly value |
| F: Start Date | Date | When they started |
| G: Status | Dropdown | Active, Paused, Churned |
| H: Health | Dropdown | 🟢 Good, 🟡 At Risk, 🔴 Churning |
| I: Last Check-in | Date | Last time you talked |
| J: Automations | Text | What's running for them |
| K: Notes | Text | Account notes |

### Total MRR Formula
```
=SUMIF(G:G, "Active", E:E)
```

---

## Sheet 4: Outreach Log

| Column | Format | Notes |
|--------|--------|-------|
| A: Date | Date | When sent |
| B: Lead Name | Text | Link to Leads |
| C: Channel | Dropdown | Email, LinkedIn, Twitter, Instagram, Phone |
| D: Type | Dropdown | Cold, Follow-up 1, Follow-up 2, Breakup |
| E: Message | Text | Copy of what you sent |
| F: Opened | Checkbox | If tracked |
| G: Replied | Checkbox | Yes/no |
| H: Reply Date | Date | When they replied |
| I: Sentiment | Dropdown | Positive, Neutral, Negative |

### Daily Outreach Count
```
=COUNTIF(A:A, TODAY())
```

### Reply Rate
```
=COUNTIF(G:G, TRUE) / COUNTA(A:A)
```

---

## Sheet 5: Dashboard

### Key Metrics

| Metric | Formula |
|--------|---------|
| Total Leads | `=COUNTA(Leads!B:B)-1` |
| Active Pipeline | `=SUMIF(Leads!H:H, "<>Won", Leads!M:M)` |
| Total MRR | `=SUMIF(Clients!G:G, "Active", Clients!E:E)` |
| This Month Won | `=SUMIFS(Leads!M:M, Leads!H:H, "Won", Leads!I:I, ">="&DATE(YEAR(TODAY()),MONTH(TODAY()),1))` |
| Reply Rate | `='Outreach Log'!ReplyRate` |

### Charts to Create
1. **Pipeline by Stage** (Pie chart from Pipeline sheet)
2. **MRR Over Time** (Line chart, needs date tracking)
3. **Lead Sources** (Bar chart from Leads!F:F)
4. **Outreach Volume** (Bar chart, daily/weekly)

---

## Automations to Add

### With n8n (free)

1. **New Lead Alert**
   - Trigger: New row in Leads sheet
   - Action: Send Telegram/Slack notification

2. **Follow-up Reminder**
   - Trigger: Daily at 9 AM
   - Filter: Where Next Date = TODAY()
   - Action: Send reminder with lead details

3. **Stale Lead Alert**
   - Trigger: Daily
   - Filter: Where Last Contact > 7 days ago AND Status not in (Won, Lost)
   - Action: Alert to follow up

4. **Weekly Report**
   - Trigger: Every Monday 9 AM
   - Action: Generate summary and send email

---

## Google Sheets Tips

### Data Validation (Dropdowns)
1. Select column
2. Data → Data validation
3. Criteria: List of items
4. Enter options comma-separated

### Conditional Formatting
- Green: Status = Won
- Yellow: Next Date = TODAY()
- Red: Last Contact > 7 days ago

### Protect Formulas
1. Select formula cells
2. Data → Protect sheets and ranges
3. Prevent accidental edits

---

## Make a Copy

Create this template in your Google Drive:
1. Create new Google Sheet
2. Rename to "Automation Agency CRM"
3. Create 5 tabs as described above
4. Add columns and formulas
5. Set up data validation for dropdowns
6. Add conditional formatting
7. Share with team (if any)

---

*Free. Powerful. Gets the job done until you need something bigger.*

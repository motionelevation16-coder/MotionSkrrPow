# European Lead Scraping System 🇪🇺

*Find businesses that need automation. Target Europe first.*

---

## Target Markets (Priority Order)

### Tier 1: English-Native
| Country | Population | Why |
|---------|------------|-----|
| 🇬🇧 UK | 67M | Native English, big SMB market |
| 🇮🇪 Ireland | 5M | English, tech-savvy, EU access |

### Tier 2: High English Proficiency
| Country | Population | English Level | Why |
|---------|------------|---------------|-----|
| 🇳🇱 Netherlands | 17M | 93% | Very business-forward |
| 🇸🇪 Sweden | 10M | 91% | Tech-savvy, early adopters |
| 🇩🇰 Denmark | 6M | 90% | High purchasing power |
| 🇳🇴 Norway | 5M | 90% | Wealthy, open to innovation |
| 🇫🇮 Finland | 6M | 75% | Tech-forward |

### Tier 3: Major Markets (English OK)
| Country | Population | Notes |
|---------|------------|-------|
| 🇩🇪 Germany | 84M | Biggest EU economy, 60% English |
| 🇫🇷 France | 68M | Big market, lower English |
| 🇪🇸 Spain | 47M | Growing startup scene |

**Start with:** UK + Netherlands + Nordics

---

## Lead Sources

### 1. Google Maps Scraping (Free)

**Best for:** Local services, retail, restaurants, agencies

**Tool:** Outscraper, PhantomBuster, or DIY

**Search queries:**
```
"marketing agency" London
"accounting firm" Amsterdam
"real estate agency" Dublin
"dental clinic" Stockholm
"law firm" Manchester
"restaurant" Berlin
"ecommerce" Copenhagen
```

**Data extracted:**
- Business name
- Address
- Phone
- Website
- Rating
- Reviews count

**Volume:** 100-500 leads per search

---

### 2. LinkedIn Sales Navigator

**Best for:** B2B, agencies, consultants, SaaS

**Cost:** €79/mo (or free trial)

**Filters for Europe:**
```
Location: United Kingdom, Netherlands, Sweden, Germany
Company size: 1-50 employees
Industry: Marketing, Legal, Healthcare, etc.
```

**Search examples:**
```
"Marketing Agency" + "Owner" + "United Kingdom"
"Founder" + "E-commerce" + "Netherlands"
"Managing Director" + "Consulting" + "Germany"
```

**Data extracted:**
- Name
- Title
- Company
- LinkedIn URL
- (Email via enrichment)

---

### 3. Apollo.io

**Best for:** Verified emails, B2B contacts

**Cost:** Free (50 credits/mo) or $49/mo

**European filters:**
```
Location: Europe
Employees: 1-50
Technologies: Shopify, WordPress, HubSpot
Industry: Select target niches
```

**Data extracted:**
- Name
- Email (verified)
- Company
- Title
- Phone
- LinkedIn

**Quality:** High — emails are verified

---

### 4. Industry Directories

| Niche | Directory | Region |
|-------|-----------|--------|
| Agencies | Clutch.co, DesignRush | Global |
| E-commerce | BuiltWith, Store Leads | Global |
| Real Estate | Rightmove (UK), Funda (NL) | Country-specific |
| Law | Legal500, Chambers | UK/EU |
| Healthcare | NHS directory (UK), local lists | Country-specific |
| Restaurants | TripAdvisor, Google Maps | Global |

---

### 5. Local Business Directories

| Country | Directories |
|---------|-------------|
| 🇬🇧 UK | Yell.com, Thomson Local, Yelp UK |
| 🇩🇪 Germany | Gelbe Seiten, Das Telefonbuch |
| 🇳🇱 Netherlands | Gouden Gids, Detelefoongids |
| 🇫🇷 France | Pages Jaunes |
| 🇸🇪 Sweden | Eniro, Hitta |

---

## Scraping Workflows

### Google Maps → Leads (n8n)

```
┌─────────────────────────────────────────────┐
│           GOOGLE MAPS SCRAPER               │
│                                             │
│  Trigger: Manual or scheduled               │
│                                             │
│  1. Input: Category + City list             │
│     "marketing agency", ["London",          │
│      "Manchester", "Birmingham"]            │
│                                             │
│  2. Call Outscraper API (or SerpAPI)        │
│     → Get business listings                 │
│                                             │
│  3. Extract:                                │
│     - Name, Address, Phone                  │
│     - Website, Email (if listed)            │
│     - Rating, Review count                  │
│                                             │
│  4. Enrich with Hunter.io                   │
│     → Find email from domain                │
│                                             │
│  5. Save to Google Sheets / Airtable        │
│                                             │
│  6. Push to Instantly.ai campaign           │
│                                             │
└─────────────────────────────────────────────┘
```

### LinkedIn → Leads (PhantomBuster)

```
┌─────────────────────────────────────────────┐
│         LINKEDIN LEAD SCRAPER               │
│                                             │
│  1. Sales Navigator search URL              │
│     (filtered by location, industry)        │
│                                             │
│  2. PhantomBuster "Sales Nav Search Export" │
│     → Extracts profiles                     │
│                                             │
│  3. PhantomBuster "LinkedIn Profile Scraper"│
│     → Gets full profile data                │
│                                             │
│  4. Enrich emails via:                      │
│     - Apollo.io                             │
│     - Hunter.io                             │
│     - Snov.io                               │
│                                             │
│  5. Export to CSV / Sheets                  │
│                                             │
│  6. Import to Instantly.ai                  │
│                                             │
└─────────────────────────────────────────────┘
```

---

## Lead Qualification

### Scoring Criteria

| Signal | Points | Why |
|--------|--------|-----|
| Has website | +10 | Basic tech presence |
| Website is outdated | +15 | Needs help |
| No social media automation | +20 | Clear pain point |
| 10-50 employees | +15 | Budget + need |
| High review count | +10 | Established business |
| Recent hiring posts | +20 | Growing, has budget |
| Uses manual tools | +25 | Perfect target |

**Score 50+ = High priority**

### Disqualification

| Signal | Action |
|--------|--------|
| No website | Skip (too small) |
| 500+ employees | Skip (enterprise sales cycle) |
| Already automated | Skip (no pain) |
| No email found | Try LinkedIn DM |

---

## Niche-Specific Searches (Europe)

### Marketing Agencies
```
Google Maps: "marketing agency" + [city]
LinkedIn: "Marketing Agency" + "Founder" + [country]
Clutch.co: Filter by EU location
```

### E-commerce Stores
```
BuiltWith: Shopify stores in UK
Store Leads: Filter by EU
Google: "shop" OR "store" + [city]
```

### Real Estate
```
Google Maps: "real estate agent" + [city]
LinkedIn: "Estate Agent" + "Director" + UK
Rightmove: Agent directory
```

### Law Firms
```
Google Maps: "solicitor" OR "law firm" + [city]
LinkedIn: "Partner" + "Law Firm" + [country]
Legal500: UK law firm rankings
```

### Healthcare/Dental
```
Google Maps: "dentist" OR "clinic" + [city]
LinkedIn: "Practice Manager" + "Dental" + [country]
```

### Restaurants/Hospitality
```
Google Maps: "restaurant" + [city]
TripAdvisor: Top restaurants by city
```

---

## City Target List

### UK (Start Here)
```
Tier 1: London, Manchester, Birmingham
Tier 2: Leeds, Glasgow, Liverpool, Bristol
Tier 3: Edinburgh, Sheffield, Newcastle, Cardiff
```

### Netherlands
```
Tier 1: Amsterdam, Rotterdam, The Hague
Tier 2: Utrecht, Eindhoven, Tilburg
```

### Germany
```
Tier 1: Berlin, Munich, Hamburg
Tier 2: Frankfurt, Cologne, Düsseldorf
Tier 3: Stuttgart, Leipzig, Dresden
```

### Nordics
```
Sweden: Stockholm, Gothenburg, Malmö
Denmark: Copenhagen, Aarhus
Norway: Oslo, Bergen
Finland: Helsinki, Tampere
```

---

## Daily Lead Generation Workflow

### Morning (30 mins)

1. **Run Google Maps scrape** (1-2 cities, 1 niche)
   - Input: "marketing agency" + "Manchester"
   - Output: 50-100 leads

2. **Run LinkedIn phantom** (1 search)
   - Input: Sales Nav search URL
   - Output: 25-50 leads

3. **Enrich emails** (Apollo/Hunter)
   - Input: Domains from scrape
   - Output: Verified emails

### Afternoon (15 mins)

4. **Quality check**
   - Remove duplicates
   - Score leads
   - Remove disqualified

5. **Upload to Instantly**
   - Add to campaign
   - Personalization variables filled

### Results

```
Daily: 50-100 qualified leads
Weekly: 350-700 leads
Monthly: 1,500-3,000 leads
```

---

## Tool Stack (Budget)

### Free Tier
| Tool | Free Limit | Use |
|------|------------|-----|
| Apollo.io | 50 credits/mo | Email finding |
| Hunter.io | 25 searches/mo | Email verification |
| Google Maps (manual) | Unlimited | Basic scraping |
| LinkedIn (free) | Limited searches | Finding people |

### Paid (Recommended)
| Tool | Cost | Use |
|------|------|-----|
| Instantly.ai | $37/mo | Sending + warmup |
| Apollo.io | $49/mo | Lead data |
| PhantomBuster | $69/mo | LinkedIn automation |
| Outscraper | $29/mo | Google Maps API |
| **Total** | **~$185/mo** | |

### Alternative (Cheaper)
| Tool | Cost | Use |
|------|------|-----|
| Instantly.ai | $37/mo | Sending |
| Hunter.io | $49/mo | Email finding |
| Manual scraping | Free | Google Maps |
| **Total** | **~$86/mo** | |

---

## Quick Start (This Week)

### Day 1
- [ ] Sign up: Apollo.io (free), Hunter.io (free)
- [ ] Pick first niche (recommend: Marketing Agencies)
- [ ] Pick first city (recommend: London)

### Day 2
- [ ] Manual Google Maps scrape (50 agencies)
- [ ] Find emails via Apollo/Hunter
- [ ] Create Google Sheet with leads

### Day 3-4
- [ ] Write email sequence (use OUTREACH.md templates)
- [ ] Set up Instantly.ai
- [ ] Import leads

### Day 5-7
- [ ] Start warmup
- [ ] Scrape more cities
- [ ] Build lead pipeline

### Week 2+
- [ ] Start sending
- [ ] Scale to more cities/niches
- [ ] Handle responses

---

## Sample Lead Sheet

| Company | Contact | Email | City | Niche | Website | Score |
|---------|---------|-------|------|-------|---------|-------|
| ABC Marketing | John Smith | john@abcmkt.co.uk | London | Agency | abcmkt.co.uk | 75 |
| XYZ Dental | Dr. Jane | info@xyzdental.com | Manchester | Healthcare | xyzdental.com | 60 |

---

*Europe first. Find them. Email them. Close them.*

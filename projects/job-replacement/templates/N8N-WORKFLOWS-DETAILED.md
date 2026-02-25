# n8n Workflow-Templates — Detailliert

*Für Content Creator, E-Commerce, Coach/Consultant*

---

## Workflow 1: Content Creator — Social Media Auto-Posting

### Use Case
Content Creator hat Inhalte in Google Sheet → Auto-Post auf Instagram, TikTok, LinkedIn, Twitter

### Trigger
- Zeitgesteuert: Täglich um 09:00, 14:00, 19:00 Uhr
- ODER: Neuer Eintrag in Google Sheet

### Workflow-Struktur

```
[Schedule Trigger]
       ↓
[Google Sheets: Get Rows]
       ↓
[Filter: Status = "Geplant"]
       ↓
[Branch: Platform Check]
    ↙     ↘
[Instagram] [LinkedIn] [Twitter] [TikTok]
    ↘     ↙
[Google Sheets: Update Status → "Gepostet"]
       ↓
[Slack/Email: Notification]
```

### Nodes im Detail

**1. Schedule Trigger**
```
Node: Schedule Trigger
Settings:
  - Mode: Cron
  - Cron Expression: 0 9,14,19 * * *
  - Timezone: Europe/Berlin
```

**2. Google Sheets: Get Rows**
```
Node: Google Sheets
Operation: Read Rows
Settings:
  - Document ID: [Sheet ID]
  - Sheet: "Content Plan"
  - Options:
    - Range: A:H
    - Data Location: First Row Contains Headers
```

**3. Filter: Status = "Geplant"**
```
Node: Filter
Conditions:
  - Field: Status
  - Operation: Equals
  - Value: "Geplant"
```

**4. IF: Platform Check**
```
Node: IF
Conditions:
  - Instagram? → platform contains "instagram"
  - LinkedIn? → platform contains "linkedin"
  - Twitter? → platform contains "twitter"
```

**5. Instagram: Post**
```
Node: HTTP Request (Instagram Graph API)
Method: POST
URL: https://graph.facebook.com/v18.0/{{instagram_account_id}}/media
Body:
  - image_url: {{image_url}}
  - caption: {{caption}}
  - access_token: {{access_token}}

Then:
Node: HTTP Request (Publish)
Method: POST  
URL: https://graph.facebook.com/v18.0/{{instagram_account_id}}/media_publish
Body:
  - creation_id: {{media_id}}
  - access_token: {{access_token}}
```

**6. LinkedIn: Post**
```
Node: HTTP Request (LinkedIn API)
Method: POST
URL: https://api.linkedin.com/v2/ugcPosts
Headers:
  - Authorization: Bearer {{linkedin_token}}
Body:
{
  "author": "urn:li:person:{{person_id}}",
  "lifecycleState": "PUBLISHED",
  "specificContent": {
    "com.linkedin.ugc.ShareContent": {
      "shareCommentary": {
        "text": "{{caption}}"
      },
      "shareMediaCategory": "IMAGE",
      "media": [{
        "status": "READY",
        "media": "{{image_urn}}"
      }]
    }
  },
  "visibility": {
    "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
  }
}
```

**7. Twitter/X: Post**
```
Node: Twitter
Operation: Create Tweet
Settings:
  - Text: {{caption}}
  - Media: {{image_url}} (if exists)
```

**8. Update Google Sheet**
```
Node: Google Sheets
Operation: Update Row
Settings:
  - Row Number: {{row_number}}
  - Column: Status
  - Value: "Gepostet"
  - Column: Gepostet_Am
  - Value: {{$now}}
```

**9. Slack Notification**
```
Node: Slack
Channel: #content-updates
Message: "✅ Neuer Post veröffentlicht: {{caption}}"
```

### Google Sheet Struktur

| ID | Plattform | Caption | Bild_URL | Status | Geplant_Für | Gepostet_Am |
|----|-----------|---------|----------|--------|-------------|-------------|
| 1 | instagram,linkedin | Heute neu... | https://... | Geplant | 2026-02-25 | |
| 2 | twitter | Thread: ... | | Geplant | 2026-02-25 | |

### Error Handling

```
Node: Error Trigger (nach jedem Post-Node)
On Error:
  - Continue (don't stop workflow)
  - Log to Error Sheet
  - Send Slack Alert: "⚠️ Post fehlgeschlagen: {{error_message}}"
```

---

## Workflow 2: E-Commerce — Order Processing

### Use Case
Neue Shopify-Bestellung → Bestätigung → Rechnung → Versand-Tracking → Review-Request

### Trigger
- Shopify Webhook: Order Created

### Workflow-Struktur

```
[Shopify Webhook: New Order]
           ↓
[Set Variables: Kundendaten]
           ↓
[FastBill/Lexoffice: Rechnung erstellen]
           ↓
[Email: Bestätigung an Kunde]
           ↓
[Wait: 1 Tag]
           ↓
[Check: Versand-Status]
       ↙     ↘
[Versendet]  [Noch nicht]
     ↓            ↓
[Email: Tracking]  [Wait 12h → Check again]
     ↓
[Wait: 7 Tage nach Lieferung]
     ↓
[Email: Review-Request]
     ↓
[Google Sheets: Update Kunde-Status]
```

### Nodes im Detail

**1. Shopify Webhook**
```
Node: Webhook
Method: POST
Path: /shopify-order
Authentication: Header Auth
  - Header: X-Shopify-Hmac-SHA256
```

**2. Set Variables**
```
Node: Set
Variables:
  - order_id: {{$json.id}}
  - customer_email: {{$json.email}}
  - customer_name: {{$json.customer.first_name}}
  - total: {{$json.total_price}}
  - items: {{$json.line_items}}
  - shipping_address: {{$json.shipping_address}}
```

**3. Rechnung erstellen (FastBill)**
```
Node: HTTP Request
Method: POST
URL: https://my.fastbill.com/api/1.0/api.php
Body:
{
  "SERVICE": "invoice.create",
  "DATA": {
    "CUSTOMER_ID": "{{customer_id}}",
    "ITEMS": {{items_array}},
    "TEMPLATE_ID": "{{template_id}}"
  }
}
```

**4. Bestätigungs-Email**
```
Node: Send Email (Gmail/SMTP)
To: {{customer_email}}
Subject: Deine Bestellung #{{order_id}} ist eingegangen! ✅
Body: 
"Hallo {{customer_name}},

vielen Dank für deine Bestellung!

Bestellnummer: #{{order_id}}
Summe: {{total}}€

Wir melden uns, sobald dein Paket unterwegs ist.

Beste Grüße"
```

**5. Wait Node**
```
Node: Wait
Resume: After Time Interval
Amount: 1
Unit: Days
```

**6. Check Fulfillment Status**
```
Node: Shopify
Operation: Get Order
Order ID: {{order_id}}

Then:
Node: IF
Condition: fulfillment_status == "fulfilled"
```

**7. Tracking Email**
```
Node: Send Email
To: {{customer_email}}
Subject: Dein Paket ist unterwegs! 📦
Body:
"Hallo {{customer_name}},

gute Nachrichten: Deine Bestellung ist auf dem Weg!

Tracking-Link: {{tracking_url}}

Beste Grüße"
```

**8. Review Request (7 Tage später)**
```
Node: Send Email
To: {{customer_email}}
Subject: Wie war's? ⭐
Body:
"Hallo {{customer_name}},

dein Paket sollte angekommen sein. 
Wir hoffen, alles gefällt dir!

Hast du 30 Sekunden für eine kurze Bewertung?
[Review-Link]

Danke!
"
```

### Error Handling

```
- Webhook-Validierung (Shopify HMAC)
- Retry bei API-Fehlern (3x mit Backoff)
- Dead Letter Queue für fehlgeschlagene Orders
- Slack-Alert bei kritischen Fehlern
```

---

## Workflow 3: Coach/Consultant — Client Onboarding

### Use Case
Neue Buchung über Calendly → Willkommens-Email → Fragebogen → Reminder → Session-Prep → Follow-up

### Trigger
- Calendly Webhook: Event Created

### Workflow-Struktur

```
[Calendly Webhook: New Booking]
           ↓
[Set: Kundendaten extrahieren]
           ↓
[Google Sheets: Kunde anlegen]
           ↓
[Email: Willkommen + Fragebogen]
           ↓
[Wait: 24h]
           ↓
[Check: Fragebogen ausgefüllt?]
       ↙     ↘
[Ja]        [Nein]
 ↓            ↓
[Continue]   [Email: Reminder]
             ↓
           [Wait: 24h]
             ↓
           [Check again]
           
[24h vor Termin]
       ↓
[Email: Reminder + Vorbereitung]
       ↓
[Session findet statt]
       ↓
[1h nach Session]
       ↓
[Email: Zusammenfassung + nächste Schritte]
       ↓
[7 Tage später]
       ↓
[Email: Follow-up + Testimonial-Request]
```

### Nodes im Detail

**1. Calendly Webhook**
```
Node: Webhook
Path: /calendly-booking
Events: invitee.created
```

**2. Set Variables**
```
Node: Set
Variables:
  - client_name: {{$json.payload.invitee.name}}
  - client_email: {{$json.payload.invitee.email}}
  - session_time: {{$json.payload.event.start_time}}
  - session_type: {{$json.payload.event.event_type}}
  - questions_answers: {{$json.payload.questions_and_answers}}
```

**3. Google Sheets: Kunde anlegen**
```
Node: Google Sheets
Operation: Append Row
Sheet: "Clients"
Values:
  - Name: {{client_name}}
  - Email: {{client_email}}
  - Session: {{session_time}}
  - Status: "Gebucht"
  - Fragebogen: "Ausstehend"
```

**4. Willkommens-Email**
```
Node: Send Email
To: {{client_email}}
Subject: Willkommen! Hier ist dein Vorbereitungs-Fragebogen 📋
Body:
"Hallo {{client_name}},

ich freue mich auf unsere Session am {{session_date}}!

Damit wir die Zeit optimal nutzen, fülle bitte diesen 
kurzen Fragebogen aus (5 Min):

[Fragebogen-Link]

Bis bald!"
```

**5. Tally Webhook: Fragebogen ausgefüllt**
```
(Separater Workflow)
Node: Webhook (Tally)
Path: /questionnaire-completed

→ Update Google Sheet: Fragebogen = "Ausgefüllt"
→ Speichere Antworten in Sheet
```

**6. Check Fragebogen-Status**
```
Node: Google Sheets - Get Row
Filter: client_email = {{client_email}}

Node: IF
Condition: Fragebogen == "Ausgefüllt"
```

**7. Reminder Email (falls nicht ausgefüllt)**
```
Node: Send Email
To: {{client_email}}
Subject: Kurze Erinnerung: Fragebogen 📝
Body:
"Hey {{client_name}},

nur eine kurze Erinnerung: Ich würde mich freuen, 
wenn du den Fragebogen vor unserer Session ausfüllst.

[Link]

Dauert nur 5 Minuten und hilft mir, 
mich optimal vorzubereiten.

Danke!"
```

**8. Session Reminder (24h vorher)**
```
Node: Schedule Trigger (24h vor session_time)

Node: Send Email
To: {{client_email}}
Subject: Morgen geht's los! 🚀
Body:
"Hey {{client_name}},

morgen um {{session_time}} Uhr ist es soweit!

Hier ist der Link für unser Meeting:
{{meeting_link}}

Bis morgen!"
```

**9. Follow-up Email (1h nach Session)**
```
Node: Wait
Until: session_end_time + 1 hour

Node: Send Email
To: {{client_email}}
Subject: Zusammenfassung + nächste Schritte
Body:
"Hey {{client_name}},

vielen Dank für die tolle Session!

Hier nochmal die wichtigsten Punkte:
{{session_notes}} (manuell oder KI-generiert)

Nächste Schritte:
- ...
- ...

Bei Fragen → einfach schreiben.

Beste Grüße"
```

**10. Testimonial Request (7 Tage später)**
```
Node: Wait
Duration: 7 days

Node: Send Email
To: {{client_email}}
Subject: Wie war's? 💬
Body:
"Hey {{client_name}},

ich hoffe, du konntest schon erste Fortschritte machen!

Falls ja — würdest du mir eine kurze Bewertung schreiben? 
Dauert 2 Minuten und hilft mir sehr.

[Testimonial-Link]

Danke!"
```

---

## Allgemeine Best Practices

### Error Handling (alle Workflows)

```yaml
Global Error Handler:
  - Catch all errors
  - Log to Google Sheet "Errors"
  - Send Slack notification
  - Retry 3x with exponential backoff
  - Dead letter queue for permanent failures
```

### Logging (alle Workflows)

```yaml
Every workflow run:
  - Log Start Time
  - Log End Time
  - Log Status (Success/Fail)
  - Log Key Variables
  - Log to: Separate "Logs" Sheet
```

### Variables & Secrets

```yaml
Environment Variables (in n8n):
  - GOOGLE_SHEET_ID
  - SLACK_WEBHOOK_URL
  - INSTAGRAM_ACCESS_TOKEN
  - SHOPIFY_API_KEY
  # etc.

Never hardcode credentials!
```

### Testing

```yaml
Before deploying:
  - Test with dummy data
  - Test error scenarios
  - Test edge cases (empty fields, special characters)
  - Test rate limits
  - Run for 24h in staging before production
```

---

*Diese Templates als Basis — für jeden Kunden anpassen!*

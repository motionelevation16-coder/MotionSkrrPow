# Tally Onboarding-Formular — Motion Elevation

*Kopierfertig für Tally.so*

---

## Formular-Struktur

### Seite 1: Willkommen

**Überschrift:**
```
Willkommen bei Motion Elevation! 🚀

Fülle dieses Formular aus (5-10 Minuten).
Je genauer deine Angaben, desto schneller können wir starten.
```

---

### Seite 2: Dein Unternehmen

**Frage 1: Firmenname**
- Typ: Kurztext
- Pflichtfeld: Ja
- Placeholder: "z.B. Mustermann GmbH"

**Frage 2: Website**
- Typ: URL
- Pflichtfeld: Nein
- Placeholder: "https://deine-website.de"

**Frage 3: Branche**
- Typ: Dropdown
- Pflichtfeld: Ja
- Optionen:
  - E-Commerce / Online-Shop
  - Agentur (Marketing, Design, etc.)
  - Coaching / Beratung
  - Immobilien
  - Handwerk / Lokale Dienstleistung
  - IT / Software
  - Gesundheit / Medizin
  - Recht / Steuerberatung
  - Sonstige

**Frage 4: Unternehmensgröße**
- Typ: Single Choice
- Pflichtfeld: Ja
- Optionen:
  - Solo / Freiberufler
  - 2-5 Mitarbeiter
  - 6-20 Mitarbeiter
  - 21-50 Mitarbeiter
  - 51+ Mitarbeiter

---

### Seite 3: Was möchtest du automatisieren?

**Frage 5: Automations-Bereiche**
- Typ: Multiple Choice (Checkboxen)
- Pflichtfeld: Ja (mindestens 1)
- Optionen:
  - 📧 Lead-Management & CRM
  - 📱 Social Media & Content
  - 🛒 E-Commerce & Bestellungen
  - 📞 Kundensupport & Tickets
  - 📄 Dokumente & Verträge
  - 💰 Rechnungen & Buchhaltung
  - 📅 Termine & Kalender
  - 🤖 KI-Chatbot / Assistenten
  - Sonstiges

**Frage 6: Beschreibe dein Hauptproblem**
- Typ: Langtext
- Pflichtfeld: Ja
- Placeholder: "z.B. Ich verbringe 2 Stunden täglich damit, Leads manuell in mein CRM einzutragen..."
- Hilfetext: "Was kostet dich aktuell die meiste Zeit?"

**Frage 7: Was ist dein Ziel?**
- Typ: Langtext
- Pflichtfeld: Ja
- Placeholder: "z.B. Ich möchte, dass neue Anfragen automatisch erfasst und beantwortet werden..."

---

### Seite 4: Deine Tools

**Frage 8: Welche Tools nutzt du bereits?**
- Typ: Multiple Choice (Checkboxen)
- Pflichtfeld: Nein
- Optionen gruppiert:

**E-Mail:**
- Gmail / Google Workspace
- Outlook / Microsoft 365
- Andere

**CRM:**
- HubSpot
- Salesforce
- Pipedrive
- Notion
- Google Sheets
- Keins
- Andere

**Social Media:**
- Instagram
- TikTok
- LinkedIn
- Twitter/X
- Facebook
- YouTube

**E-Commerce:**
- Shopify
- WooCommerce
- Wix
- Andere

**Kalender:**
- Google Calendar
- Outlook
- Cal.com / Calendly

**Kommunikation:**
- Slack
- Microsoft Teams
- Discord
- WhatsApp Business

**Frage 9: Gibt es Tools, die wir noch verbinden sollen?**
- Typ: Kurztext
- Pflichtfeld: Nein
- Placeholder: "z.B. FastBill, Lexoffice, Custom API..."

---

### Seite 5: Besonderheiten

**Frage 10: Gibt es Ausnahmen oder Sonderregeln?**
- Typ: Langtext
- Pflichtfeld: Nein
- Placeholder: "z.B. Anfragen aus Österreich sollen anders behandelt werden..."
- Hilfetext: "Alles, was wir wissen sollten, damit die Automation perfekt für dich funktioniert."

**Frage 11: Datenschutz-Anforderungen?**
- Typ: Single Choice
- Pflichtfeld: Ja
- Optionen:
  - Standard (DSGVO-konform reicht)
  - Erhöht (z.B. Gesundheitsdaten, Finanzdaten)
  - Keine besonderen Anforderungen

---

### Seite 6: Ansprechpartner

**Frage 12: Dein Name**
- Typ: Kurztext
- Pflichtfeld: Ja

**Frage 13: Deine E-Mail**
- Typ: E-Mail
- Pflichtfeld: Ja

**Frage 14: Telefon (optional)**
- Typ: Telefon
- Pflichtfeld: Nein
- Hilfetext: "Falls wir dich schnell erreichen müssen"

**Frage 15: Technischer Ansprechpartner (falls anders)**
- Typ: Kurztext
- Pflichtfeld: Nein
- Placeholder: "Name und E-Mail"
- Hilfetext: "Falls jemand anderes die Tool-Verbindungen machen soll"

**Frage 16: Zeitzone**
- Typ: Dropdown
- Pflichtfeld: Ja
- Default: Europe/Berlin
- Optionen:
  - Europe/Berlin (Deutschland)
  - Europe/Vienna (Österreich)
  - Europe/Zurich (Schweiz)
  - Andere

---

### Seite 7: Abschluss

**Überschrift:**
```
Perfekt! 🎉

Wir melden uns innerhalb von 24 Stunden mit dem nächsten Schritt.

Du bekommst eine E-Mail mit den Links, um deine Accounts zu verbinden.
```

**Bestätigungs-E-Mail:** Ja (automatisch)

---

## Tally-Einstellungen

### Design
- Theme: Hell
- Akzentfarbe: Motion Elevation Blau (#3B82F6)
- Logo: Motion Elevation Logo oben

### Logik (Conditional)

**Wenn Branche = "E-Commerce":**
→ Zeige zusätzlich: "Welches Shop-System nutzt du?"

**Wenn Branche = "Agentur":**
→ Zeige zusätzlich: "Wie viele Kunden betreust du gleichzeitig?"

**Wenn "KI-Chatbot" ausgewählt:**
→ Zeige zusätzlich: "Wo soll der Chatbot eingesetzt werden? (Website, WhatsApp, etc.)"

### Integrationen

**Webhook an n8n:**
- URL: [n8n Webhook URL]
- Trigger: Bei Absenden
- Payload: Alle Felder als JSON

**E-Mail-Notification:**
- An: team@motionelevation.com
- Betreff: "Neuer Kunde: {Firmenname}"

**Google Sheets:**
- Neuer Eintrag für jeden Kunden
- Tracking: Datum, Name, Status

---

## E-Mail-Templates (Tally Auto-Response)

### Bestätigungs-E-Mail an Kunde

**Betreff:** Wir haben deine Angaben erhalten! ✅

**Text:**
```
Hallo {Name},

vielen Dank! Wir haben deine Angaben erhalten.

Was passiert jetzt?

1. Wir schauen uns alles an (heute noch)
2. Du bekommst eine E-Mail mit Links zum Verbinden deiner Accounts
3. Wir richten alles ein (24-48 Stunden)
4. Deine Automation ist live! 🚀

Bei Fragen → einfach auf diese E-Mail antworten.

Beste Grüße,
Dein Motion Elevation Team
```

---

## Test-Checkliste

Vor Go-Live testen:

- [ ] Formular auf Desktop funktioniert
- [ ] Formular auf Mobile funktioniert
- [ ] Conditional Logic funktioniert
- [ ] Webhook wird gesendet
- [ ] Bestätigungs-E-Mail kommt an
- [ ] Notification-E-Mail kommt an
- [ ] Google Sheets wird aktualisiert
- [ ] Alle Pflichtfelder validieren korrekt

---

*Tally-Formular erstellen: tally.so → Create Form → Diese Struktur kopieren*

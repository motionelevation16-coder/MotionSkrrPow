# Client Journey — Complete Flow 🗺️

*Von der ersten E-Mail bis zur fertigen Automation*

---

## Overview

```
COLD EMAIL
    ↓
REPLY / INTERESSE
    ↓
DISCOVERY CALL (15 min)
    ↓
ANGEBOT SENDEN
    ↓
ZAHLUNG
    ↓
ONBOARDING (Client füllt Formular aus)
    ↓
SETUP (wir bauen)
    ↓
CLIENT VERBINDET ACCOUNTS
    ↓
TESTING
    ↓
LIVE 🚀
    ↓
SUPPORT & MAINTENANCE
```

---

## Phase 1: Outreach (Cold Email)

### Ziel: Antwort bekommen

**Sequenz:**
- Tag 0: Erste E-Mail (Pain Question oder Observation)
- Tag 2: Kurzer Follow-up
- Tag 5: Value Add (Resource/Video)
- Tag 8: Breakup E-Mail

**Siehe:** `outreach/COLD-EMAILS-GERMAN.md` für deutsche Templates

### Tracking
| Metrik | Ziel |
|--------|------|
| Öffnungsrate | >50% |
| Antwortrate | >5% |
| Positive Antworten | >2% |

---

## Phase 2: Reply Handling

### Szenario A: Interesse ✅

**Client schreibt:**
> "Klingt interessant, erzähl mir mehr"

**Deine Antwort:**
```
Hallo {Name},

freut mich! Hier ist mein Kalender — such dir einen passenden Termin aus:
{Calendly/Cal.com Link}

15 Minuten reichen. Ich zeige dir kurz, was für {Firma} möglich wäre.

Beste Grüße,
{Dein Name}
```

### Szenario B: Mehr Info gewünscht

**Client schreibt:**
> "Was genau macht ihr?"

**Deine Antwort:**
```
Hallo {Name},

kurz gesagt: Wir bauen Automationen, die dir {X Stunden pro Woche} sparen.

Beispiel: {Relevantes Beispiel für ihre Branche}

Hier ein kurzes Video (2 min): {Loom Link}

Lohnt sich ein 15-min Gespräch? {Kalender Link}

Beste Grüße,
{Dein Name}
```

### Szenario C: "Jetzt nicht"

**Deine Antwort:**
```
Kein Problem — Timing ist wichtig.

Darf ich in {3 Monaten} nochmal nachfragen?

Beste Grüße
```
→ Reminder setzen, erneut kontaktieren

### Szenario D: "Nein danke"

**Deine Antwort:**
```
Verstehe ich, danke für die Rückmeldung!

Falls sich etwas ändert, bin ich erreichbar.

Viel Erfolg mit {Firma}!
```
→ Aus Liste entfernen, respektieren

---

## Phase 3: Discovery Call (15 min)

### Ziel: Verstehen, ob wir helfen können

**Ablauf:**

**Minute 0-2: Small Talk**
- "Wie läuft's bei {Firma}?"
- Locker, kein Sales-Druck

**Minute 2-5: Pain Discovery**
- "Was hat dich an meiner E-Mail angesprochen?"
- "Wo verlierst du aktuell die meiste Zeit?"
- "Was würdest du als erstes automatisieren, wenn alles möglich wäre?"

**Minute 5-10: Lösung zeigen**
- "Das können wir lösen. So funktioniert's..."
- Kurze Demo oder Screen-Share (wenn sinnvoll)
- "Andere in {Branche} sparen damit {X} Stunden/Woche"

**Minute 10-12: Einwände klären**
- "Was müsste passieren, damit das für dich Sinn macht?"
- Siehe: `OBJECTIONS.md`

**Minute 12-15: Next Steps**
- "Das passt gut zu unserem {Paket}-Paket für €{Preis}/Monat"
- "Willst du heute starten oder brauchst du noch Zeit?"

### Nach dem Call

**Bei JA:**
1. Zahlungslink senden (Stripe)
2. "Sobald die Zahlung durch ist, bekommst du das Onboarding-Formular"

**Bei "Ich überlege":**
1. Zusammenfassung per E-Mail senden
2. Follow-up nach 2-3 Tagen

**Bei NEIN:**
1. Fragen: "Was war der Hauptgrund?"
2. Notizen machen für zukünftige Verbesserung

---

## Phase 4: Angebot & Zahlung

### Preise (in EUR für DACH)

| Paket | Preis/Monat | Inhalt |
|-------|-------------|--------|
| Starter | €197 | 1 Automation |
| Growth | €397 | 3 Automationen |
| Scale | €797 | Unbegrenzt |

### Zahlung

**Option A: Stripe Payment Link**
- Einmalig + Recurring
- Client klickt → zahlt → fertig

**Option B: Rechnung**
- Für größere Firmen mit Procurement
- 14 Tage Zahlungsziel

### Nach Zahlungseingang

Automatisch (via Stripe Webhook):
1. ✉️ Willkommens-E-Mail mit Onboarding-Link
2. 📋 Onboarding-Formular (Tally/Typeform)
3. 📁 Client-Ordner anlegen
4. 🔔 Slack-Notification an dich

---

## Phase 5: Onboarding

### Willkommens-E-Mail (automatisch)

```
Betreff: Willkommen bei Motion Elevation! 🚀

Hallo {Name},

Zahlung erhalten — vielen Dank!

Nächster Schritt: Füll bitte dieses kurze Formular aus (5-10 min):
{Onboarding Formular Link}

Je genauer deine Angaben, desto schneller läuft's.

Danach bekommst du eine E-Mail mit den Verbindungen zu deinen Tools.

Fragen? Einfach antworten.

Beste Grüße,
{Dein Name}
Motion Elevation
```

### Onboarding-Formular

**Fragen:**
1. Firmenname
2. Website
3. Branche (Dropdown)
4. Welche Automation(en) möchtest du? (Checkboxes)
5. Welche Tools nutzt du? (CRM, E-Mail, Social, etc.)
6. Was soll automatisiert werden? (Freitext)
7. Gibt es Besonderheiten oder Ausnahmen?
8. Wer ist der technische Ansprechpartner? (Name, E-Mail)
9. Zeitzone

---

## Phase 6: Setup (Wir bauen)

### Varianten — Welches Tool nutzen?

| Option | Pro | Contra | Für wen |
|--------|-----|--------|---------|
| **n8n Cloud** | Einfach, wir hosten | €20+/Monat extra | Meiste Clients |
| **n8n Self-Hosted** | Kostenlos, volle Kontrolle | Client braucht Server | Tech-affine Clients |
| **Make** | Sehr einfach | Teuer bei Volumen | Nicht-technische Clients |
| **Zapier** | Bekannt | Am teuersten | Enterprise |

### Empfehlung

**Standard:** n8n Cloud (wir hosten für Client)
- Client zahlt uns, wir zahlen n8n
- Client muss nichts technisches tun

**Budget-Option:** n8n Self-Hosted auf Client-Server
- Wir richten ein, Client hostet
- Spare dem Client €20+/Monat

### Setup-Prozess

**Tag 1:**
1. Onboarding-Formular prüfen
2. n8n Instance erstellen
3. Basis-Workflows aus Templates laden
4. Anpassen an Client-Anforderungen

**Tag 2:**
1. OAuth-Verbindungen vorbereiten
2. Setup-Guide an Client senden
3. Client verbindet Accounts
4. Warten auf Verbindungen

**Tag 3:**
1. Alle Verbindungen testen
2. End-to-End Tests
3. Feintuning
4. Go-Live

---

## Phase 7: Client verbindet Accounts

### Setup-Guide (wird separat an Client gesendet)

**Siehe:** `CLIENT-SETUP-GUIDE.md`

Dieser Guide ist extra simpel gehalten:
- Screenshots für jeden Schritt
- Keine Fachbegriffe
- Video-Tutorials als Backup
- FAQ für häufige Probleme

### Was Client tun muss

1. E-Mail öffnen
2. Link klicken
3. "Mit Google verbinden" (oder jeweilige Plattform)
4. Erlauben
5. Fertig

**Für jede Plattform:** Eigener Link, eigene Anleitung

---

## Phase 8: Testing

### Checkliste vor Go-Live

```
□ Alle OAuth-Tokens gültig
□ Test-Workflow läuft durch
□ Fehlerbehandlung funktioniert
□ Benachrichtigungen konfiguriert
□ Client-Dashboard Zugang funktioniert
□ Dokumentation gesendet
□ SLA erklärt
```

### Test-Szenarien (je nach Automation)

**E-Mail-Automation:**
- Test-E-Mail senden → Wird richtig kategorisiert?
- Antwort-Vorschlag prüfen

**Social Media:**
- Test-Post planen → Wird gepostet?
- Zeiten stimmen?

**Chatbot:**
- Test-Fragen stellen
- Edge Cases prüfen

---

## Phase 9: Go-Live 🚀

### Launch-E-Mail an Client

```
Betreff: Deine Automation ist live! 🎉

Hallo {Name},

alles ist eingerichtet und läuft!

Was jetzt passiert:
- {Automation 1} → läuft automatisch
- {Automation 2} → läuft automatisch
- Du bekommst jeden {Tag} einen Report

Dein Dashboard: {Link}
Support: {E-Mail/Telegram}

Die ersten 48 Stunden überwachen wir alles extra genau.

Bei Fragen → einfach antworten.

Beste Grüße,
{Dein Name}
```

### Erste Woche

- Tag 1-2: Stündlich Monitoring
- Tag 3-7: Täglich Check
- Aktiv auf Probleme reagieren
- Client proaktiv updaten

---

## Phase 10: Support & Maintenance

### Support-Kanäle

| Kanal | Response Time | Für |
|-------|--------------|-----|
| E-Mail | <24h | Normale Fragen |
| Telegram | <4h | Urgente Probleme |
| Telefon | Termin | Komplexe Themen |

### Monatliche Tasks

- [ ] Performance-Report senden
- [ ] Check-in (optional)
- [ ] Optimierungen vorschlagen
- [ ] Feedback sammeln

### Upselling

Nach 30 Tagen:
- "Läuft {Automation 1} gut? Wollen wir {Automation 2} angehen?"
- "Andere Clients in {Branche} nutzen auch..."

---

## Troubleshooting (Häufige Probleme)

### Problem: OAuth Token abgelaufen

**Symptom:** Automation stoppt plötzlich
**Lösung:** Client muss neu verbinden
**Prävention:** Token-Expiry-Alerts einrichten

### Problem: API-Limit erreicht

**Symptom:** Fehler "Rate Limit"
**Lösung:** Workflow drosseln oder API-Plan upgraden
**Prävention:** Limits im Voraus klären

### Problem: Client ändert Passwort

**Symptom:** Verbindung bricht ab
**Lösung:** Neu verbinden
**Prävention:** Client informieren, dass wir benachrichtigt werden müssen

### Problem: Workflow läuft nicht

**Symptom:** Keine Aktivität
**Lösung:** Logs prüfen → Trigger prüfen → Test manuell
**Prävention:** Monitoring-Alerts

---

## Templates & Automatisierungen

### Empfohlene Tools

| Zweck | Tool | Kosten |
|-------|------|--------|
| Formulare | Tally | Gratis |
| Kalender | Cal.com | Gratis |
| Zahlung | Stripe | % Gebühr |
| E-Mail | Gmail + Aliases | Gratis |
| Workflows | n8n | Gratis (self-hosted) |
| CRM | Google Sheets | Gratis |

### Automatisierungen für dich

1. **Zahlung → Onboarding-E-Mail** (Stripe Webhook)
2. **Formular ausgefüllt → Slack-Notification**
3. **OAuth verbunden → Status-Update**
4. **Wöchentlicher Report → Client**

---

*Vom Erstkontakt zum zufriedenen Langzeit-Kunden.*

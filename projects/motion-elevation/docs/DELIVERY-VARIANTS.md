# Delivery Variants — Setup-Optionen 🛠️

*Welche Technik für welchen Kunden?*

---

## Übersicht

| Option | Kosten/Monat | Wer hostet | Technisch | Für wen |
|--------|-------------|------------|-----------|---------|
| **n8n Cloud (wir)** | In Preis inklusive | Wir | Einfach | Standard — 80% der Kunden |
| **n8n Cloud (client)** | €20+ (zahlt Client) | Client | Mittel | Tech-affine, will Kontrolle |
| **n8n Self-Hosted** | €0 | Client | Komplex | Budget-bewusst + tech-affin |
| **Make** | €0-29+ | Make | Sehr einfach | Absolut nicht-technisch |
| **Zapier** | €0-49+ | Zapier | Sehr einfach | Kennt Zapier bereits |

---

# Option 1: n8n Cloud (von uns gehostet) ⭐

**Empfohlen für: 80% der Kunden**

### Was wir tun:
- Wir haben einen n8n Cloud Account
- Jeder Kunde bekommt einen Workspace
- Wir verwalten alles

### Was der Kunde tut:
- Accounts verbinden (OAuth)
- Fertig

### Vorteile:
- ✅ Client muss nichts technisches tun
- ✅ Wir haben volle Kontrolle
- ✅ Schnelle Problemlösung
- ✅ Einfaches Monitoring

### Nachteile:
- ⚠️ Wir tragen die Hosting-Kosten
- ⚠️ Bei vielen Kunden: unsere Kosten steigen

### Kosten für uns:
- n8n Cloud Starter: €20/Monat für ~5 Workflows
- n8n Cloud Pro: €50/Monat für mehr

### Kalkulation:
Bei €197/Monat pro Client, €20 für n8n = €177 Marge ✅

---

# Option 2: n8n Cloud (Client zahlt selbst)

**Für: Tech-affine Kunden, die Kontrolle wollen**

### Was wir tun:
- Workflows bauen
- Client fügt uns als Collaborator hinzu
- Wir verwalten, Client besitzt

### Was der Kunde tut:
1. n8n Cloud Account erstellen (5 min)
2. Plan auswählen
3. Uns als Collaborator einladen
4. Accounts verbinden

### Client-Anleitung:

**Schritt 1: Account erstellen**
```
1. Gehe zu https://n8n.io
2. Klicke "Start Free"
3. Erstelle Account mit deiner E-Mail
4. Wähle "Cloud" (nicht Self-Hosted)
```

**Schritt 2: Plan auswählen**
```
Starter: €20/Monat — für 1-2 Automationen
Pro: €50/Monat — für mehr
```

**Schritt 3: Uns einladen**
```
1. Klicke auf dein Profil (oben rechts)
2. Settings → Members
3. Invite Member
4. E-Mail: team@motionelevation.com
5. Role: Editor
6. Send Invite
```

### Vorteile:
- ✅ Client hat volle Kontrolle
- ✅ Wir haben keine Hosting-Kosten
- ✅ Client kann selbst Sachen anpassen

### Nachteile:
- ⚠️ Client muss zahlen
- ⚠️ Etwas mehr Setup-Aufwand

---

# Option 3: n8n Self-Hosted

**Für: Budget-bewusste + technische Kunden**

### Voraussetzungen:
- Client hat Server (VPS, eigener Server)
- Client kann Docker/Terminal bedienen
- ODER: Client zahlt uns für Setup

### Was wir tun:
- n8n auf Client-Server installieren
- Workflows einrichten
- Remote-Zugang für Maintenance

### Client-Server-Optionen:

| Anbieter | Min. Kosten | Empfohlen |
|----------|------------|-----------|
| Hetzner | €3.99/Monat | ✅ DACH |
| DigitalOcean | $6/Monat | ✅ International |
| Contabo | €4.99/Monat | ✅ Budget |
| AWS/Azure | Variabel | Enterprise |

### Installation (vereinfacht):

**Via Docker Compose:**
```yaml
version: '3'
services:
  n8n:
    image: n8nio/n8n
    ports:
      - "5678:5678"
    environment:
      - N8N_BASIC_AUTH_USER=admin
      - N8N_BASIC_AUTH_PASSWORD=strongpassword
    volumes:
      - n8n_data:/home/node/.n8n
volumes:
  n8n_data:
```

**Befehle:**
```bash
# Server vorbereiten
sudo apt update && sudo apt install docker.io docker-compose -y

# n8n starten
docker-compose up -d

# Erreichbar unter: http://server-ip:5678
```

### Vorteile:
- ✅ Keine monatlichen n8n-Kosten
- ✅ Volle Kontrolle
- ✅ Keine Workflow-Limits

### Nachteile:
- ⚠️ Client braucht Server
- ⚠️ Mehr Setup-Aufwand
- ⚠️ Wir brauchen SSH-Zugang für Maintenance

---

# Option 4: Make (ehemals Integromat)

**Für: Absolut nicht-technische Kunden**

### Wann Make statt n8n?
- Kunde hat schon Make
- Kunde will es selbst sehen/verstehen
- Sehr einfache Workflows

### Kosten für Client:
| Plan | Preis | Ops/Monat |
|------|-------|-----------|
| Free | €0 | 1.000 |
| Core | €9 | 10.000 |
| Pro | €16 | 10.000 + features |

### Was wir tun:
- Workflows in Make bauen
- Client gibt uns Zugang

### Vorteile:
- ✅ Sehr visuell
- ✅ Einfach zu verstehen
- ✅ Client kann selbst Dinge ändern

### Nachteile:
- ⚠️ Teuer bei vielen Operationen
- ⚠️ Weniger flexibel als n8n
- ⚠️ AI-Features kosten extra

---

# Option 5: Zapier

**Für: Kunden die Zapier schon nutzen**

### Wann Zapier?
- Kunde hat schon Zapier-Konto
- Kunde will bei bekanntem Tool bleiben
- Enterprise-Firmen

### Kosten für Client:
| Plan | Preis | Tasks/Monat |
|------|-------|-------------|
| Free | €0 | 100 |
| Starter | €19.99 | 750 |
| Professional | €49 | 2.000 |

### Vorteile:
- ✅ Bekannteste Plattform
- ✅ Meiste Integrationen
- ✅ Enterprise-Support

### Nachteile:
- ⚠️ Am teuersten
- ⚠️ Wenig Flexibilität
- ⚠️ Limits schnell erreicht

---

# Entscheidungsbaum

```
Ist der Kunde technisch?
├── JA → Will er selbst hosten?
│   ├── JA → Option 3: n8n Self-Hosted
│   └── NEIN → Option 2: n8n Cloud (Client zahlt)
│
└── NEIN → Hat er schon Make/Zapier?
    ├── JA, Make → Option 4: Make
    ├── JA, Zapier → Option 5: Zapier
    └── NEIN → Option 1: n8n Cloud (wir hosten) ⭐
```

---

# Hybrid-Ansatz

Für größere Kunden mit verschiedenen Bedürfnissen:

| Automation | Tool | Grund |
|------------|------|-------|
| Einfache Sachen | Make/Zapier | Client kann selbst anpassen |
| Komplexe Workflows | n8n | Mehr Kontrolle für uns |
| AI-Workflows | n8n | Besser + günstiger |

---

# Preisanpassung nach Variante

| Variante | Unser Preis | Unsere Marge |
|----------|-------------|--------------|
| n8n Cloud (wir hosten) | €197/Monat | ~€170 |
| n8n Cloud (Client zahlt) | €147/Monat | ~€147 |
| n8n Self-Hosted | €147/Monat | ~€147 |
| Make/Zapier (Client zahlt) | €147/Monat | ~€147 |

**Logik:** Wenn Client selbst Hosting zahlt, reduzieren wir unseren Preis um €50.

---

# Migration zwischen Varianten

## Make → n8n
- Export nicht direkt möglich
- Workflows müssen neu gebaut werden
- Angebot: Migration für €200 einmalig

## Zapier → n8n
- Gleich wie Make
- Keine direkte Migration

## n8n Cloud → Self-Hosted
- Export als JSON möglich
- Import auf Self-Hosted
- Relativ einfach

---

*Die richtige Variante = weniger Support + zufriedener Kunde*

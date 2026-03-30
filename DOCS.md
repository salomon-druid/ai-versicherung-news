# ai-versicherung-news – Projekt-Dokumentation

**Erstellt:** 2026-03-28  
**Letzte Aktualisierung:** 2026-03-30  
**Status:** Aktiv  

---

## Übersicht

**ai-versicherung.news** ist ein automatisiertes Nachrichtenportal für die Versicherungsbranche, das täglich kuratierte Artikel zu KI, Versicherern, Maklern, Produkten, Regulierung und Risiken veröffentlicht.

- **Live-URL:** https://ai-versicherung-news.vercel.app
- **GitHub:** https://github.com/salomon-druid/ai-versicherung-news
- **Hosting:** Vercel (automatisches Deployment bei Push zu `main`)
- **GitHub-Token:** In Keyring, erfordert ggf. `gh auth login` nach Reboot

---

## Tech Stack

| Komponente | Technologie |
|------------|-------------|
| Framework | Astro 5.x (Static Site Generator) |
| Styling | Tailwind CSS 3.x |
| Content | Markdown + MDX (Astro Content Collections) |
| Validierung | Zod-Schemas für Frontmatter |
| Deployment | Vercel |
| Versionierung | GitHub |
| Bilder | Unsplash API (per Artikel-Slug) |
| Firmenlogos | Clearbit Logo API |
| SEO | Schema.org (NewsArticle), Sitemap, robots.txt |
| Datenbank | JSON-Datei (`data/articles-db.json`) |

---

## Farbschema

| Farbe | HEX | Verwendung |
|-------|-----|------------|
| Primary (Grün) | `#3e7339` | Links, Buttons, Akzente |
| Dark | `#1F2933` | Text, Header, Footer |
| Background | `#F5F4F1` | Seitenhintergrund |
| Gold | `#D4AF37` | Hover-Effekte, Top-Story-Marker |

---

## Seitenstruktur (69 Seiten)

```
/                           → Startseite (mit Top-Story Hero)
/news                       → Alle News
/{category}                 → 6 Kategorie-Seiten
/news/{slug}                → Einzelartikel (~57)
/glossar                    → 33 Begriffe in 6 Kategorien
/about                      → Über uns
/datenschutz                → Datenschutzerklärung
/impressum                  → Impressum
```

---

## Content-Kategorien (6)

| Kategorie | Slug | Beschreibung |
|-----------|------|--------------|
| 🤖 KI & Digitalisierung | `ki-digitalisierung` | KI, InsurTech, Tech |
| 🏢 Versicherer | `versicherer` | Unternehmen, Quartalszahlen, Fusionen |
| 📦 Versicherungsprodukte | `versicherungsprodukte` | Neue Tarife, Innovationen |
| 🌍 Umfeld & Regulierung | `versicherungsumfeld` | EU, BaFin, Markt |
| 🏠 Makler | `makler` | Vertrieb, Verbände, Vergütung |
| ⚡ Risiken & Schäden | `risiken-schaeden` | Naturkatastrophen, Cyber, Haftung |

---

## Content-Schema (Zod)

```typescript
{
  title: string,           // Artikel-Titel
  description: string,     // Meta-Description
  pubDate: Date,           // Veröffentlichungsdatum
  category: enum,          // Eine der 6 Kategorien
  tags?: string[],         // Optionale Tags
  author?: string,         // Standard: "ai-versicherung-news"
  image?: string,          // Überschreibt automatisches Bild
  company?: string,        // Firmenname (optional)
  companyDomain?: string,  // Für Clearbit-Logo (optional)
  sources: [{              // Quellenangaben (Pflicht)
    title: string,
    url: string,
    date?: string,
    outlet?: string,
  }],
  featured?: boolean,      // Top-Story-Marker
}
```

⚠️ **WICHTIG:** YAML-Frontmatter darf KEINE typografischen Anführungszeichen (`„"`) oder doppelte Anführungszeichen innerhalb von Strings enthalten. Siehe Fix-Skripte unten.

---

## Bilder-System

### Struktur
```
public/images/
├── articles/              ← Einzigartig pro Artikel (Slug-basiert)
│   ├── {slug}.jpg
│   └── {slug}.json        ← Metadaten (Photographer, URL)
├── {category}.jpg         ← Kategorie-Fallback
└── default.jpg            ← Letzter Fallback
```

### Unsplash-Zugangsdaten
- App ID: 908110
- Access Key: In `.env` Datei (gitignored)

### Skripte
- `scripts/fetch-article-image.sh <slug> <category>` – Holt einziges Bild pro Artikel
- `scripts/fetch-unsplash-images.sh` – Holt Kategorie-Fallback-Bilder

---

## Artikel-Datenbank

### Datei: `data/articles-db.json`
Enthält alle Artikel mit Metadaten zur Duplikat-Erkennung.

### Skripte
- `scripts/rebuild-db.py` – Datenbank aus Markdown-Dateien neu aufbauen
- `scripts/check-duplicate.py "Titel"` – Prüft ob ähnlicher Artikel existiert (>70% Ähnlichkeit)
- `scripts/fix-yaml.py` – Fixt typografische Anführungszeichen (v1)
- `scripts/fix-yaml-v2.py` – Aggressiverer YAML-Fix (doppelte Quotes)

---

## CronJobs (Automatisierung)

### Übersicht

| Job | Uhrzeit | Beschreibung |
|-----|---------|--------------|
| 📰 Chefredaktion | 06:30 | Top Story wählen, montags Deep Dive |
| 🤖 KI & Digitalisierung | 07:00 | 4-6 Artikel |
| 🏢 Versicherer & Produkte | 09:00 | 4-6 Artikel |
| 🌍 Umfeld & Regulierung | 11:00 | 4-6 Artikel |
| 🏠 Makler & Risiken | 13:00 | 4-6 Artikel |
| 📧 E-Mails | Alle 30 Min | Google Mail prüfen |

### Konfiguration
- CronJobs in: `~/.openclaw/cron/jobs.json`
- **Gateway-Neustart erforderlich** nach Änderungen
- Alle News-Jobs: `rebuild-db.py` + Duplikat-Check enthalten

### Chefredakteur (06:30)
- Wählt täglich den besten Artikel als Top Story (`featured: true`)
- **Montags:** Generiert zusätzlich einen Deep Dive-Artikel (800-1200 Wörter)
- Nur EIN Artikel darf `featured: true` haben

---

## Layout (Redesign 29.03.2026)

### Header (Masthead)
- Aktuelles Datum oben
- Zentriertes Logo mit „News & Analyse"
- Navigation mit Pipe-Trennzeichen
- Gold/grün Akzentlinie

### Homepage (Newspaper-Grid)
- **Top:** Großer Featured-Artikel (2/3) + 3 Sidebar-Karten (1/3)
- **Mitte:** 2-Spalten-Grid + Sidebar mit Meistgelesen, Themen, Stats
- **Kategorien:** 6-Karten-Reihe
- **Newsletter CTA**

### Artikel-Seiten
- Breadcrumbs (Home > News > Kategorie > Titel)
- Lesezeit-Anzeige
- Social-Sharing (X, LinkedIn, E-Mail)
- Verwandte Artikel mit Bildern
- „Was könnte Sie sonst noch interessieren?" (andere Kategorien)
- Vor/Zurück Navigation

---

## Komponenten

| Datei | Beschreibung |
|-------|--------------|
| `Header.astro` | Masthead mit Datum, Logo, Navigation |
| `Footer.astro` | 4-Spalten Footer mit Kategorien, Rechtliches |
| `NewsCard.astro` | Artikel-Karte mit Bild, Logo, Kategorie |
| `SmallNewsCard.astro` | Kompakte Karte für „Meistgelesen" Sidebar |
| `CategoryBadge.astro` | Farbige Kategorie-Badges |
| `BaseLayout.astro` | Grundlayout mit SEO-Meta |
| `ArticleLayout.astro` | Artikel-Layout mit Hero, Quellen, Navigation |

---

## Bekannte Issues

1. **YAML-Sonderzeichen:** CronJobs produzieren manchmal kaputtes YAML (typografische Quotes). Fix: `scripts/fix-yaml-v2.py`
2. **GitHub-Auth:** Token kann nach Reboot/Keyring-Unlock verfallen. Fix: `gh auth setup-git` + Remote-URL mit Token setzen
3. **Gateway-Restart:** Neue/veränderte CronJobs erfordern Gateway-Restart
4. **Bild-Wiederverwendung:** Kategorie-Fallback kann sich wiederholen (Artikel-Bilder sind einzig)

---

## Git-Auth Fix (falls Push nicht klappt)

```bash
# Token aus gh holen und in Remote-URL setzen
gh auth setup-git
cd ~/.openclaw/workspace/ai-versicherung-news
git remote set-url origin https://salomon-druid:$(gh auth token)@github.com/salomon-druid/ai-versicherung-news.git
git push
```

---

## TODOs

- [ ] Google News Publisher anmelden
- [ ] RSS Feed einrichten
- [ ] Newsletter-Funktion (Mailchimp/Brevo)
- [ ] Web Push-Benachrichtigungen
- [ ] LinkedIn-Integration (automatische Posts)
- [ ] Premium-Newsletter testen
- [ ] Google AdSense
- [ ] Impressum/Datenschutz mit echten Daten füllen
- [ ] YAML-Validierung in CronJob-Prompts verbessern (präventiv)
- [ ] Memory Search mit Gemini (Key konfiguriert, Index ggf. noch aufzubauen)
- [ ] Deep Dive am Montag testen (Chefredakteur-CronJob)
- [ ] Meta-Tags für Artikel-Bilder (OG Image) prüfen

---

## Projekt-Historie

| Datum | Meilenstein |
|-------|-------------|
| 27.03.2026 | Projekt gestartet, 6 erste Artikel, GitHub + Vercel |
| 27.03.2026 | Farbschema (#3e7339), Glossar (33 Begriffe), Unsplash-Bilder |
| 28.03.2026 | Scope erweitert (6 Themenfelder, Firmenlogos, 4 CronJobs) |
| 28.03.2026 | 10 Artikel, 22 Seiten, Sub-Agenten für News-Generierung |
| 29.03.2026 | 28 Artikel an einem Tag, YAML-Fixes, Artikel-Datenbank |
| 29.03.2026 | Top-Story, Verwandte Artikel, Chefredakteur-CronJob |
| 29.03.2026 | News-Portal Redesign (Masthead, Newspaper-Grid) |
| 30.03.2026 | 57 Artikel, 69 Seiten, YAML-Fix, Git-Auth Fix |

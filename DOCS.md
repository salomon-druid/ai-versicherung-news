# ai-versicherung-news – Projekt-Dokumentation

**Erstellt:** 2026-03-28  
**Letzte Aktualisierung:** 2026-03-28  
**Status:** Aktiv  

---

## Übersicht

**ai-versicherung.news** ist ein automatisiertes Nachrichtenportal für die Versicherungsbranche, das täglich kuratierte Artikel zu KI, Versicherern, Maklern, Produkten, Regulierung und Risiken veröffentlicht.

- **Live-URL:** https://ai-versicherung-news.vercel.app
- **GitHub:** https://github.com/salomon-druid/ai-versicherung-news
- **Hosting:** Vercel (automatisches Deployment bei Push zu `main`)

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

---

## Farbschema

| Farbe | HEX | Verwendung |
|-------|-----|------------|
| Primary (Grün) | `#3e7339` | Links, Buttons, Akzente |
| Dark | `#1F2933` | Text, Header, Footer |
| Background | `#F5F4F1` | Seitenhintergrund |
| Gold | `#D4AF37` | Hover-Effekte, Top-Story-Marker |

---

## Seitenstruktur (22 Seiten)

```
/                           → Startseite
/news                       → Alle News (10 Artikel)
/ki-digitalisierung         → Kategorie: KI & Digitalisierung
/versicherer                → Kategorie: Versicherer
/versicherungsprodukte      → Kategorie: Produkte
/versicherungsumfeld        → Kategorie: Umfeld & Regulierung
/makler                     → Kategorie: Makler
/risiken-schaeden           → Kategorie: Risiken & Schäden
/news/{slug}                → Einzelartikel (×10)
/glossar                    → 33 Begriffe in 6 Kategorien
/about                      → Über uns
/datenschutz                → Datenschutzerklärung
/impressum                  → Impressum
```

---

## Content-Kategorien

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

### Scripts
- `scripts/fetch-article-image.sh <slug> <category>` – Holt einziges Bild pro Artikel
- `scripts/fetch-unsplash-images.sh` – Holt Kategorie-Fallback-Bilder

### Unsplash-Zugangsdaten
- Gespeichert in `.env` (gitignored)
- App ID: 908110

---

## CronJobs (Automatisierung)

### News-Generierung (4 Jobs, verteilt 07:00-13:00)

| Job | Uhrzeit | Themen |
|-----|---------|--------|
| `news-ki-digitalisierung` | 07:00 | KI, InsurTech, Tech |
| `news-versicherer-produkte` | 09:00 | Versicherer, Produkte |
| `news-umfeld-regulierung` | 11:00 | Regulierung, Markt |
| `news-makler-risiken` | 13:00 | Makler, Risiken, Schäden |

### E-Mail-Automatisierung
| Job | Intervall | Beschreibung |
|-----|-----------|--------------|
| `E-Mails` | Alle 30 Min | Google Mail prüfen, Kontakte laden |

### Jeder News-Job:
1. Sucht Web nach aktuellen Nachrichten
2. Generiert deutschen Artikel (300-500 Wörter)
3. Holt einziges Unsplash-Bild
4. Committet und pusht zu GitHub
5. Vercel baut automatisch

---

## Komponenten

| Datei | Beschreibung |
|-------|--------------|
| `Header.astro` | Navigation mit Kategorie-Links |
| `Footer.astro` | Links zu Kategorien, Rechtliches |
| `NewsCard.astro` | Artikel-Karte mit Bild, Logo, Kategorie |
| `CategoryBadge.astro` | Farbige Kategorie-Badges |
| `BaseLayout.astro` | Grundlayout mit SEO-Meta |
| `ArticleLayout.astro` | Artikel-Layout mit Hero-Bild, Quellen |

---

## SEO

- **Schema.org:** `NewsArticle` pro Artikel, `WebSite` global
- **Sitemap:** Automatisch generiert (`sitemap-index.xml`)
- **robots.txt:** Erlaubt alles, verweist auf Sitemap
- **Meta-Tags:** Open Graph, Twitter Cards, Canonical URLs
- **Google News:** Noch nicht angemeldet (TODO)

---

## Konfiguration

### openclaw.json (relevant)
- Primary Model: `openrouter/xiaomi/mimo-v2-pro`
- Fallbacks: arcee-ai/trinity-mini, step-3.5-flash, nvidia/nemotron

### astro.config.mjs
- Site: `https://ai-versicherung-news.vercel.app`
- Integrations: Sitemap, Tailwind
- Output: Static

### vercel.json
- Framework: Astro
- trailingSlash: true
- cleanUrls: true

---

## Bekannte Issues

1. **YAML-Sonderzeichen:** Artikel-Frontmatter darf keine `„"` (typografische Anführungszeichen) enthalten – bricht den Build
2. **CronJob-Neustart:** Neue CronJobs erfordern Gateway-Restart
3. **Bild-Wiederverwendung:** Aktuell pro Artikel einzig, aber Kategorie-Fallback kann sich wiederholen

---

## TODOs

- [ ] Google News Publisher anmelden
- [ ] RSS Feed einrichten
- [ ] Newsletter-Funktion (Mailchimp/Brevo)
- [ ] Web Push-Benachrichtigungen
- [ ] LinkedIn-Integration
- [ ] Premium-Newsletter testen
- [ ] Google AdSense
- [ ] Impressum/Datenschutz mit echten Daten füllen

---

## Projekt-Historie

| Datum | Meilenstein |
|-------|-------------|
| 27.03.2026 | Projekt gestartet, Astro-Setup, 6 erste Artikel |
| 27.03.2026 | GitHub + Vercel Deployment |
| 27.03.2026 | Farbschema angepasst (#3e7339 Primary) |
| 27.03.2026 | Glossar hinzugefügt (33 Begriffe) |
| 27.03.2026 | Unsplash-Bilder pro Artikel |
| 28.03.2026 | Scope erweitert (6 Themenfelder, Firmenlogos) |
| 28.03.2026 | 4 CronJobs eingerichtet (07:00-13:00) |
| 28.03.2026 | 10 Artikel, 22 Seiten live |

---
title: ArtiFix — Report di Stato
type: report
version: v7.4
date: 2026-09-17
session: #12 (Dominio Custom + Screenshot)
generated_by: Alex + AI (DeepSeek)
description: Manuale v7.4 completo + 10 regole + stato corrente
link_stable: true
next_version: report_v7.5.md
---

# ArtiFix — Report di Stato v7.4 + Manuale Tecnico Completo

**Versione report:** v7.4
**Versione manuale:** v7.4
**Data:** 17 Settembre 2026
**Sessione:** #12 (Dominio Custom + Screenshot)
**Stato sistema:** 🟢 Attivo
**Freeze:** ❌ Non attivo

---

## 📊 STATO CORRENTE

### Versioni correnti
- **Manuale Tecnico:** v7.4
- **App Streamlit:** v7.4
- **Libreria mesh2u3d:** v0.1.0 (commit `666be25`)
- **Viewer HTML:** v7.4 (dominio `viewer.artifix.it`)

### Componenti attivi
| Componente | Stato |
|------------|-------|
| App Streamlit | ✅ Funzionante |
| Landing Page | ✅ Pubblicata |
| Dominio `viewer.artifix.it` | ✅ Attivo |
| DNS Cloudflare | ✅ Configurato |
| Google Sheet Sponsor | ✅ Attivo |
| Apps Script (3 trigger) | ✅ Attivi |
| GitHub Actions | ✅ Attivo |
| UptimeRobot | ✅ Attivo |
| HTTPS (Let's Encrypt) | ✅ Attivo |

### Task completati (sessione #12)
- ✅ Dominio custom `viewer.artifix.it`
- ✅ Pulsanti "📸 Scatta foto" + "💾 Scarica HTML"
- ✅ Layout uniforme pannello info + troncamento nome file
- ✅ Reset automatico uploader al cambio lingua
- ✅ Rimozione PDF 3D
- ✅ Nuovi moduli `converter`, `cli`, `prc`
- ✅ Sezione informativa HTML 3D Viewer
- ✅ Pin `mesh2u3d@666be25`
- ✅ Registro link auto-descrittivi (`REGISTRY.md`)

### Task in corso
- 🚧 Setup sistema Roadmap automatico (15%)

### Prossimi step
1. Creare Google Sheet "Roadmap ArtiFix"
2. Configurare token con scope minimo
3. Salvare token nei Secrets
4. Scrivere workflow GitHub Actions per verifica oraria
5. Scrivere Apps Script per KPI + report 6h
6. Scrivere dashboard Streamlit `roadmap.artifix.it`
7. Configurare sottodominio `roadmap.artifix.it`

### KPI
- Task completati: 9
- Tempo medio: 25 min
- Errori rilevati: 0
- Uptime: 100%
- Verifiche orarie: N/A (sistema in setup)

---

## 📜 REGOLE FONDAMENTALI (10)

1. **Verifica oraria + auto-correzione** — ogni ora, controlla e corregge i processi
2. **Report continuativo tra sessioni** — link stabile, self-contained
3. **Sincerità e limiti** — l'AI dichiara sempre i propri limiti
4. **Congelamento manuale + automatico + temporaneo** — flag `SYSTEM_FROZEN`
5. **Notifiche raggruppate ogni 6 ore** — email a info@artifix.it
6. **Versioning progressivo del manuale** — v7.4 → v7.5 → v7.6 → ...
7. **Link stabile al report** — sempre lo stesso link, contenuto aggiornato
8. **Manuale completo su GitHub, aggiornamenti in chat** — GitHub = fonte di verità
9. **Versioning progressivo dei report** — `report_v7.4.md`, `report_v7.5.md`, ...
10. **Link auto-descrittivi** — ogni link ha nome + intestazione YAML + registro

---

Manuale Tecnico ArtiFix v7.4
Piattaforma di Riparazione, Conversione e Visualizzazione File CAD/CAM
Versione: 7.4 — Edizione Consolidata + Libreria mesh2u3d + Viewer HTML 3D con Dominio Custom
Data di rilascio: 16 Settembre 2026
Autore: alexcool-project
Repository principali:
•	https://github.com/alexcool-project/Artifix (piattaforma)
•	https://github.com/alexcool-project/mesh2u3d (libreria Python)
•	https://github.com/alexcool-project/mesh2u3d-viewer (hosting viewer)
URL pubblici:
•	Sito: https://www.artifix.it
•	App: https://artifix.streamlit.app
•	Viewer: https://viewer.artifix.it
________________________________________
PREFAZIONE
Il Manuale Tecnico ArtiFix v7.4 rappresenta la documentazione consolidata del progetto ArtiFix, redatta secondo una logica di replicabilità integrale: ogni sezione contiene le informazioni necessarie per comprendere, ricostruire e aggiornare il progetto da zero, anche in assenza di contesto storico.
Questa edizione recepisce:
•	L'architettura storica del progetto (v1.0 → v7.3)
•	La sessione pomeridiana del 16 Settembre 2026 che ha introdotto il dominio custom, i pulsanti del viewer e il reset automatico degli uploader
•	Le correzioni tecniche delle sessioni precedenti
•	La documentazione legale completa
•	Il sistema di automazione della sponsorizzazione
•	Il sistema anti-sleep a tripla ridondanza
Nota per l'uso con AI: questo manuale è ottimizzato per essere allegato come contesto a una conversazione con un modello linguistico. Ogni sezione è autoconclusiva e strutturata per permettere la ricostruzione del progetto senza ambiguità.
________________________________________
INDICE GENERALE
PARTE I — VISIONE E ARCHITETTURA
1.	Panoramica del Progetto
2.	Architettura Generale
3.	Struttura del Repository
PARTE II — COMPONENTI DELLA PIATTAFORMA
4.	App Streamlit (Core)
5.	Moduli Python
6.	Landing Page SEO
7.	Dominio, DNS ed Email
8.	Database Sponsor (Google Sheets)
9.	Dominio Custom viewer.artifix.it
PARTE III — AUTOMAZIONE SPONSORIZZAZIONE
10.	Architettura Automazione
11.	Google Apps Script — Configurazione
12.	Trigger Automatici
13.	Sistema Auto-Risposta
14.	Sistema Ringraziamento Donazioni
15.	Sistema Gestione Scadenze
16.	Logica Classificazione Email
17.	Filtri Gmail e Notifiche
PARTE IV — DOCUMENTAZIONE LEGALE
18.	Privacy Policy (IT + EN)
19.	Cookie Policy (IT + EN)
20.	Termini di Servizio (IT + EN)
21.	Licenza d'Uso (LICENSE.md)
22.	README.md — Badge e Link Legali
PARTE V — SISTEMA ANTI-SLEEP E MONITORAGGIO
23.	GitHub Actions (keep-alive.yml)
24.	UptimeRobot
25.	Pagine Intermedie (apri.html / open.html)
PARTE VI — MATERIALI COMMERCIALI
26.	Pacchetto Sponsor PDF
27.	Locandina Professionale
28.	Template Email Proposta
29.	Campagna Email Target
PARTE VII — LIBRERIA mesh2u3d
30.	Visione e Obiettivi della Libreria
31.	Architettura del Pacchetto
32.	Modulo MeshReader
33.	Modulo U3DWriter
34.	Modulo HTMLWriter
35.	Modulo PDFEmbedder
36.	Modulo Validator
37.	Modulo Converter
38.	Modulo CLI
39.	Modulo PRC Writer
40.	API di Alto Livello
41.	Esempi e Test
42.	Roadmap mesh2u3d
PARTE VIII — VIEWER HTML 3D E CONDIVISIONE
43.	Viewer HTML 3D Universale
44.	Funzionalità del Viewer
45.	Controlli Interattivi
46.	Pannello Info (layout uniforme)
47.	Pulsante "Scatta foto"
48.	Pulsante "Scarica HTML"
49.	Pulsante Donazione
50.	Sistema di Condivisione Link + QR
51.	Integrazione in ArtiFix
PARTE IX — GUIDA UTENTE
52.	Dashboard
53.	Centro Riparazione File
54.	Viewer 3D
55.	Conversione Formati
56.	Progetto ArtiFix e Sponsor
PARTE X — DIAGNOSTICA E MANUTENZIONE
57.	Diagnosi Intelligente delle Mesh
58.	Errori Comuni e Soluzioni
59.	Procedure di Manutenzione Periodica
PARTE XI — STORIA E SVILUPPO
60.	Timeline delle Versioni (v1.0 → v7.4)
61.	Roadmap Futura
62.	Strategia di Sponsorizzazione Consolidata
PARTE XII — CHANGELOG SESSIONI
63.	Sessione 16 Settembre 2026 (Mattina) — Fix Traduzioni IT/EN
64.	Sessione 16 Settembre 2026 (Pomeriggio) — Dominio Custom + Screenshot
APPENDICI
•	A. Formati Supportati
•	B. Riferimenti Tecnici
•	C. FAQ
•	D. Glossario Tecnico
•	E. 50 Aziende Target
________________________________________
PARTE I — VISIONE E ARCHITETTURA
1. Panoramica del Progetto
ArtiFix è una piattaforma web gratuita e open source per la riparazione, conversione e visualizzazione di file CAD/CAM e mesh 3D. Il progetto nasce come strumento professionale per ingegneri, architetti, progettisti, studenti e appassionati di modellazione 3D.
L'architettura del progetto si articola su tre pilastri:
1.	App Streamlit dinamica — elabora i file degli utenti in tempo reale
2.	Landing page statica — vetrina SEO e documentazione legale
3.	Viewer HTML condivisibile — condivisione di modelli 3D tramite link e QR code
Nel corso delle versioni (v1.0 → v7.4) il progetto ha subito un'evoluzione architetturale progressiva, documentata integralmente nella Parte XI.
1.1 App Streamlit (Core)
L'applicazione interattiva che costituisce il cuore del progetto, accessibile su https://artifix.streamlit.app.
Funzionalità principali:
•	Riparazione automatica di mesh 3D con diagnosi intelligente
•	Conversione universale tra oltre 50 formati
•	Viewer 3D WebGL interattivo
•	Report diagnostico PDF professionale
•	Interfaccia bilingue IT/EN completa
•	Sistema sponsor dinamico (banner rotanti)
•	Generazione viewer HTML 3D condivisibile (v7.2+)
•	Reset automatico degli uploader al cambio lingua (v7.4)
1.2 Landing Page SEO (GitHub Pages)
Sito vetrina statico, ospitato su GitHub Pages, raggiungibile da https://www.artifix.it.
Caratteristiche:
•	Homepage bilingue IT/EN
•	7 guide SEO per lingua (14 totali)
•	Pagine legali complete (Privacy, Cookie, Termini) IT + EN
•	Pagine intermedie anti-sleep
•	Schema.org e hreflang IT/EN
•	Sitemap a 22 URL
•	Sezione informativa "Cos'è l'HTML 3D Viewer?" (v7.4)
1.3 Dominio ed Email (IONOS + Cloudflare + Gmail)
Stack tecnologico:
Componente	Provider
Registrar	IONOS
DNS	Cloudflare
Email ricezione	Cloudflare Email Routing → Gmail
Email invio	Gmail SMTP (App Password)
Dominio viewer	viewer.artifix.it (v7.4)
1.4 Database Sponsor (Google Sheets)
•	Strumento: Google Sheets "Artifix Sponsors"
•	Automazione: Google Apps Script (v2.3)
1.5 Libreria mesh2u3d
Libreria Python open source (licenza MIT) per la conversione di mesh 3D in U3D, HTML 3D e PDF 3D.
Obiettivi:
•	100% from scratch (nessuna dipendenza da SDK proprietari)
•	Supporto multi-formato in input (STL, OBJ, PLY, GLB, GLTF, OFF, DAE, 3MF, FBX)
•	Output universale: HTML 3D (three.js), U3D (ECMA-363), PDF 3D
•	API Python + CLI
•	Pubblicazione su PyPI (roadmap Q4 2026)
________________________________________
2. Architettura Generale
2.1 Diagramma Architetturale
text
UTENTE / BROWSER
    │
    ├── www.artifix.it (Landing) ─ GitHub Pages
    │
    ├── artifix.streamlit.app (App) ─ Streamlit Cloud
    │         │
    │         ├── Google Sheet (Sponsor DB)
    │         ├── GitHub Raw (Loghi, Asset)
    │         ├── Libreria mesh2u3d
    │         │
    │         └── Viewer HTML 3D (condivisibile)
    │              ├── viewer.artifix.it (dominio custom v7.4)
    │              ├── Link + QR Code
    │              ├── Pulsanti Screenshot + Download HTML
    │              └── Zero Adobe richiesto
2.2 Flusso di Esecuzione App Streamlit
1.	Utente → richiesta HTTPS
2.	Streamlit Cloud → avvia container Python 3.12
3.	app.py → entry point
4.	Router interno → gestisce navigazione
5.	Moduli specifici → eseguono la logica
6.	Output → HTML/CSS/JS nel browser
2.3 Automazione Sponsor
1.	Trigger cron → attiva funzioni Apps Script
2.	Apps Script → legge/scrive su Google Sheet + Gmail
3.	Gmail → invia/riceve email sponsor
4.	Google Sheet → traccia sponsor, log risposte, log donazioni
2.4 Flusso Libreria mesh2u3d
text
Mesh 3D (STL/OBJ/PLY/GLB/GLTF/OFF/DAE/3MF/FBX)
    ↓
MeshReader.read() → MeshData (vertices, triangles, normals, name)
    ↓
U3DWriter.mesh_to_u3d() → file .u3d (ECMA-363)
HTMLWriter.mesh_to_html() → file .html (three.js) [IT + EN]
PRCWriter.mesh_to_prc() → file .prc (ISO 14739, v7.4 minimale)
PDFEmbedder.mesh_to_pdf() → file .pdf (PRC embedded, roadmap)
2.5 Flusso Viewer HTML (v7.4)
text
Utente carica file su ArtiFix
    ↓
ArtiFix genera HTML con mesh embedded
    ↓
HTML caricato su GitHub Pages (repo mesh2u3d-viewer)
    ↓
ArtiFix genera URL: https://viewer.artifix.it/v/A3F-XXXXX.html
    ↓
Progettista copia link + QR Code
    ↓
Cliente apre link nel browser → vede 3D interattivo
    ↓
Pulsanti: 📸 Scatta foto | 💾 Scarica HTML
________________________________________
3. Struttura del Repository
3.1 Repository ArtiFix
text
Artifix/
├── .github/workflows/keep-alive.yml    # Anti-sleep (ogni 1 ora)
├── .streamlit/config.toml              # Tema Light + maxUploadSize
├── docs/                                # Landing Page
│   ├── index.html                       # Homepage IT
│   ├── privacy.html                     # Privacy Policy IT
│   ├── cookie.html                      # Cookie Policy IT
│   ├── termini.html                     # Termini IT
│   ├── apri.html                        # Anti-sleep IT
│   ├── convertire-*.html                # 7 guide SEO IT
│   ├── styles.css, script.js
│   ├── sitemap.xml, robots.txt
│   ├── CNAME                            # www.artifix.it
│   ├── images/
│   └── en/                              # Versione EN
├── app.py                               # App Streamlit
├── translations.py                      # Dizionario IT/EN completo
├── sponsors.py                          # Gestione sponsor
├── repair_page.py                       # Logica riparazione
├── mesh_analyzer.py                     # Analisi + riparazione + PDF
├── share_utils.py                       # Condivisione viewer
├── requirements.txt                     # Dipendenze (pin mesh2u3d@666be25)
├── README.md, LICENSE.md
└── assets grafici
3.2 Repository mesh2u3d (separato)
text
mesh2u3d/
├── mesh2u3d/
│   ├── __init__.py                      # API pubblica
│   ├── io/mesh_reader.py                # MeshReader + MeshData
│   ├── u3d/                             # U3DWriter + Validator
│   ├── html/writer.py                   # HTMLWriter (v7.4 aggiornato)
│   ├── prc/                             # PRCWriter (v7.4)
│   ├── pdf/embedder.py                  # PDFEmbedder
│   ├── converter/convert.py             # Converter universale (v7.4)
│   ├── cli/main.py                      # CLI (v7.4)
│   └── share.py                         # Pubblicazione viewer (v7.4)
├── examples/, tests/, reference/
├── pyproject.toml
└── README.md, LICENSE
3.3 Repository mesh2u3d-viewer (hosting)
text
mesh2u3d-viewer/
├── assets/ArchiFix_cubo-logo.png
├── v/                                   # Viewer HTML generati
│   ├── A3F-XXXXX1.html
│   └── ...
├── CNAME                                # viewer.artifix.it
└── README.md
________________________________________
PARTE II — COMPONENTI DELLA PIATTAFORMA
4. App Streamlit (Core)
4.1 Tecnologia
•	Linguaggio: Python 3.12
•	Framework: Streamlit 1.40+
•	Hosting: Streamlit Community Cloud
•	Secrets: SMTP, SPONSORS_CSV_URL, GITHUB_TOKEN, GITHUB_USERNAME, GITHUB_REPO
4.2 Funzionalità
Bilingue IT/EN:
•	Rilevamento automatico lingua browser
•	Selettore manuale nella sidebar
•	Tutte le stringhe centralizzate in translations.py
•	Navigazione stabile al cambio lingua
•	Reset automatico uploader al cambio lingua (v7.4)
Riparazione file:
•	Analisi completa mesh
•	Diagnosi intelligente con suggerimenti
•	Report PDF dettagliato
Viewer 3D interno:
•	Rendering WebGL con Three.js
•	Rotazione, pan, zoom
•	Legenda assi tradotta (IT/EN)
Conversione formati:
•	11 formati mesh + DXF + PDF
•	Matrice di 150+ combinazioni
•	Nome file originale preservato
Generazione Viewer HTML:
•	Pulsante "Genera file condivisibile"
•	File HTML self-contained con three.js
•	Link con dominio custom viewer.artifix.it (v7.4)
•	Pulsanti "📸 Scatta foto" + "💾 Scarica HTML" (v7.4)
•	Pannello info con layout uniforme (v7.4)
•	QR Code scaricabile
4.3 Tema Light Forzato
toml
[theme]
base = "light"
primaryColor = "#1f77b4"
backgroundColor = "#ffffff"
secondaryBackgroundColor = "#f0f2f6"
textColor = "#0f172a"
font = "sans serif"

[server]
maxUploadSize = 5000
headless = true

[browser]
gatherUsageStats = false
________________________________________
5. Moduli Python
5.1 translations.py
Responsabilità: gestione completa delle traduzioni IT/EN.
Chiavi principali:
•	nav_* — navigazione
•	dash_* — dashboard
•	repair_* / report_* — riparazione e report
•	type_* — tipi di formato
•	viewer_* — viewer 3D
•	convert_* — conversione
•	sponsor_* — sponsor
•	privacy_* / cookie_* — pagine legali
•	share_* — condivisione link/QR
•	html_viewer_* — sezione informativa HTML 3D Viewer (v7.4)
•	notes_expander_* — tendina formati proprietari
5.2 sponsors.py
Responsabilità: gestione banner sponsor dinamici.
Funzionalità:
•	load_sponsors() — legge Google Sheet CSV
•	render_sponsor_band(lang) — banda scorrevole
•	sponsor_band_placeholder(lang) — placeholder
•	Cache: @st.cache_data(ttl=300)
5.3 repair_page.py
Responsabilità: logica pagina "Ripara File" step-by-step.
5.4 mesh_analyzer.py
Responsabilità: motore di analisi, riparazione, diagnosi, PDF.
5.5 share_utils.py
Responsabilità: condivisione viewer HTML.
v7.4: Rimossa opzione PDF, solo HTML con dominio custom.
________________________________________
6. Landing Page SEO
Stack: HTML5 + CSS3 + JS vanilla, ospitato su GitHub Pages.
Struttura bilingue:
•	IT: /docs/
•	EN: /docs/en/
SEO: Meta tag, Open Graph, Twitter Card, Schema.org, hreflang, sitemap 22 URL.
________________________________________
7. Dominio, DNS ed Email
7.1 Dominio
•	Registrar: IONOS
•	Dominio: artifix.it
7.2 DNS (Cloudflare)
Record A (GitHub Pages):
text
A @ 185.199.108.153
A @ 185.199.109.153
A @ 185.199.110.153
A @ 185.199.111.153
Record CNAME:
text
CNAME www alexcool-project.github.io
CNAME viewer alexcool-project.github.io  (v7.4)
7.3 Email
•	Ricezione: Cloudflare Email Routing → Gmail
•	Invio: Gmail SMTP con alias info@artifix.it
________________________________________
8. Database Sponsor (Google Sheets)
Struttura: foglio "Artifix Sponsors" con colonne nome, logo_url, sito_url, email, data_inizio, giorni, attivo, note, email_reminder_inviata, data_disattivazione.
Log: Log_Risposte, Log_Donazioni.
Regola loghi: URL Raw GitHub obbligatori.
________________________________________
9. Dominio Custom viewer.artifix.it (v7.4)
9.1 Obiettivo
Sostituire l'URL GitHub Pages (alexcool-project.github.io/mesh2u3d-viewer/) con un dominio brandizzato (viewer.artifix.it) per migliorare brand identity e fiducia.
9.2 Configurazione DNS
Record aggiunto su Cloudflare:
Campo	Valore
Type	CNAME
Name	viewer
Target	alexcool-project.github.io

Proxy	DNS only (nuvola grigia)
TTL	Auto
9.3 Configurazione GitHub Pages
1.	Settings → Pages
2.	Custom domain: viewer.artifix.it
3.	Salva → GitHub crea file CNAME
4.	Attendi "DNS check successful"
5.	Spunta "Enforce HTTPS" (5-10 min per certificato SSL)
9.4 Modifica al Codice
Nel file share.py:
python
PUBLIC_BASE_URL = "https://viewer.artifix.it"
url = f"{PUBLIC_BASE_URL}/v/{viewer_id}.html"
9.5 Risultato
Prima: https://alexcool-project.github.io/mesh2u3d-viewer/v/A3F-8JYRGR.html
Dopo: https://viewer.artifix.it/v/A3F-8JYRGR.html
I vecchi link restano funzionanti (alias).
________________________________________
PARTE III — AUTOMAZIONE SPONSORIZZAZIONE
(invariata rispetto alla v7.3 — vedi sezioni 10-17)
________________________________________
PARTE IV — DOCUMENTAZIONE LEGALE
(invariata rispetto alla v7.3 — vedi sezioni 18-22)
________________________________________
PARTE V — SISTEMA ANTI-SLEEP E MONITORAGGIO
(invariata rispetto alla v7.3 — vedi sezioni 23-25)
________________________________________
PARTE VI — MATERIALI COMMERCIALI
(invariata rispetto alla v7.3 — vedi sezioni 26-29)
________________________________________
PARTE VII — LIBRERIA mesh2u3d
(invariata rispetto alla v7.3, con le seguenti aggiunte v7.4)
37. Modulo Converter (v7.4)
File: mesh2u3d/converter/convert.py
Funzionalità:
•	convert_3d_file(input, output) — conversione universale
•	convert_3d_files(inputs, output_dir) — batch processing
API:
python
from mesh2u3d import convert_3d_file
result = convert_3d_file("cube.stl", "cube.u3d")
38. Modulo CLI (v7.4)
File: mesh2u3d/cli/main.py
Comandi:
•	mesh2u3d convert input.stl output.u3d
•	mesh2u3d batch *.stl --output-dir ./out
•	mesh2u3d info input.stl
•	mesh2u3d validate input.u3d
39. Modulo PRC Writer (v7.4)
File: mesh2u3d/prc/writer.py
Funzionalità: Generazione file PRC (ISO 14739-1) minimali.
Limitazione: Adobe Acrobat rifiuta la struttura semplificata. Viewer tolleranti (Foxit) lo accettano.
________________________________________
PARTE VIII — VIEWER HTML 3D E CONDIVISIONE
43. Viewer HTML 3D Universale
File .html self-contained con three.js embedded.
44. Funzionalità del Viewer
Desktop: pannello info, controlli, reset, hints, logo ArtiFix cliccabile.
Mobile: pannello info compatto, pulsante ingranaggio modale.
45. Controlli Interattivi
•	Slider opacità: 10% → 100%
•	Wireframe, Griglia, Assi
•	Materiali: Solido, Flat, X-Ray
46. Pannello Info (layout uniforme v7.4)
text
File         Project Modern Bath Tray Br...
Vertici      4.383
Triangoli    2.939
Formato      OBJ
CSS chiave: max-width: 320px, troncamento con ... se supera 180px.
47. Pulsante "Scatta foto" (v7.4)
Posizione: in alto a sinistra.
Funzione: cattura canvas WebGL + watermark con dati file.
Salvataggio: PNG {project}_{data}.png.
48. Pulsante "Scarica HTML" (v7.4)
Posizione: in alto a sinistra.
Funzione: salva il file HTML self-contained per uso offline.
49. Pulsante Donazione
Formula: "Aiutaci a mantenere ArtiFix gratuito".
50. Sistema di Condivisione Link + QR
Dominio custom: viewer.artifix.it.
URL generato: https://viewer.artifix.it/v/A3F-XXXXX.html.
51. Integrazione in ArtiFix
(invariata rispetto alla v7.3, con aggiunte v7.4)
________________________________________
PARTE IX — GUIDA UTENTE
(invariata rispetto alla v7.3 — vedi sezioni 52-56)
________________________________________
PARTE X — DIAGNOSTICA E MANUTENZIONE
(invariata rispetto alla v7.3 — vedi sezioni 57-59)
________________________________________
PARTE XI — STORIA E SVILUPPO
60. Timeline delle Versioni (v1.0 → v7.4)
v1.0 — Prototipo (2025)
Prima versione sperimentale. Streamlit come base, conversione elementare tra pochi formati. Nome originale: "ArchiFix".
v2.0 — Evoluzione (2026)
Introduzione del viewer 3D WebGL e della riparazione base delle mesh.
v3.0 — Consolidamento (Settembre 2026)
Ribattezzato ArtiFix. Pipeline di riparazione strutturata, report PDF, tema Light forzato.
v4.0 — Sviluppo intermedio
Migrazione URL immagini, multilingua parziale, sponsor band, cookie banner.
v5.0 — Documentazione operativa
Manuale v5.0, sistema anti-sleep, bilinguismo completo, guide SEO, DNS Cloudflare, email professionale.
v6.0 — Consolidamento definitivo
Migrazione Streamlit Cloud, refactoring modulare, fix copy(), tema Light, bilinguismo completo.
v6.1 — Diagnosi Intelligente
Diagnosi mesh, PDF con diagnosi, messaggio contestuale, fix radio button.
v6.2 — Manutenzione Documentata
Commenti # NOTA MANUTENZIONE FUTURA in sponsors.py e app.py.
v6.3 — UX Conversion Fix (13 Settembre 2026)
Nome file originale preservato, messaggio download chiaro, rimozione time.sleep(1) inutile.
v7.0 — Automazione Sponsor Completa (14 Settembre 2026)
Automazione Google Apps Script v2.3 (3 trigger), sistema auto-risposta, ringraziamento donazioni, logica classificazione email robusta, materiali commerciali, notifiche Gmail, fix SMTP, fix emoji.
v7.1 — Documentazione Legale Completa (15 Settembre 2026)
Termini IT+EN, Privacy aggiornata, Licenza bilingue, README con badge, sitemap 22 URL, pulsante Termini nella sidebar, anti-sleep tripla ridondanza, Google Search Console.
v7.2 — Libreria mesh2u3d + Viewer HTML 3D (15 Settembre 2026)
Libreria Python open source, viewer HTML universale con three.js, sistema di condivisione link + QR, integrazione in ArtiFix, correzioni tecniche.
v7.3 — Fix Traduzioni IT/EN Complete (16 Settembre 2026, mattina)
Completamento translations.py, aggiunta chiavi share_* e viewer_legend_axes, passaggio del parametro lang, pinning mesh2u3d@7ae1132.
v7.4 — Dominio Custom + Screenshot (16 Settembre 2026, pomeriggio)
•	Dominio custom viewer.artifix.it con HTTPS
•	Pulsanti "📸 Scatta foto" + "💾 Scarica HTML"
•	Pannello info uniforme con troncamento nome file
•	Reset automatico uploader al cambio lingua
•	Rimozione PDF 3D
•	Aggiunta moduli converter, cli, prc
•	Sezione informativa HTML 3D Viewer
•	Pin mesh2u3d@666be25
________________________________________
61. Roadmap Futura
Q4 2026:
•	Pubblicazione mesh2u3d su PyPI
•	Campagna sponsorizzazione email
•	Product Hunt, Slant, G2, Capterra
•	Link Manuale in sidebar
Q1 2027:
•	U3D Base Profile completo (Adobe)
•	Texture PBR (GLB/GLTF)
•	Sezioni trasversali, exploded view, X-ray
•	Batch processing, editor mesh integrato
•	App mobile PWA
•	AI riparazione avanzata
Q2 2027:
•	Community condivisione
•	Marketplace sponsor
•	Supporto DWG, RVT
•	Commenti cliente sul 3D
•	Versioning progetti
________________________________________
62. Strategia di Sponsorizzazione Consolidata
(invariata rispetto alla v7.3 — vedi sezione 62)
________________________________________
PARTE XII — CHANGELOG SESSIONI
63. Sessione 16 Settembre 2026 (Mattina) — Fix Traduzioni IT/EN
(vedi Manuale v7.3, Parte XII, sezione 56)
________________________________________
64. Sessione 16 Settembre 2026 (Pomeriggio) — Dominio Custom + Screenshot
64.1 Obiettivo della Sessione
Aggiungere dominio custom per i link condivisibili e pulsanti professionali nel viewer HTML.
64.2 Problemi Rilevati
1.	Link condivisibili usavano URL GitHub Pages non brandizzati
2.	Viewer HTML non aveva pulsanti screenshot/download
3.	Pannello info del viewer non uniforme (nome file in grassetto blu)
4.	Nome file lungo allargava eccessivamente il pannello
5.	Uploader non si resettava al cambio lingua
6.	PDF 3D non compatibile con Adobe Acrobat
64.3 Soluzioni Applicate
File 1 — mesh2u3d/html/writer.py
Aggiunti pulsanti e layout uniforme.
Commit: [UX] Viewer info panel: uniform label/value style, filename truncated (666be25)
File 2 — mesh2u3d/share.py
Aggiunta costante PUBLIC_BASE_URL.
Commit: [FEAT] Use custom domain viewer.artifix.it for share links (5faab63)
File 3 — Artifix/share_utils.py
Rimossa opzione PDF 3D.
Commit: [CLEANUP] Remove PDF 3D option from share form - HTML only (f0864e1)
File 4 — Artifix/translations.py
Aggiunte 10 chiavi html_viewer_*, rimosse 2 chiavi convert_expander_*.
Commit: [I18N] Add HTML 3D Viewer info translations (IT/EN)
File 5 — Artifix/app.py
Aggiunta sezione informativa, reset uploader, rimozione tendina duplicata.
Commit: [FEAT] Add HTML 3D Viewer info section + [FIX] Remove duplicate expander + [UX] Reset file uploaders on language switch
File 6 — Artifix/requirements.txt
Pin mesh2u3d@666be25.
Commit: [CHORE] Pin mesh2u3d to commit 666be25
File 7-9 — Moduli converter, cli, prc
Nuovi moduli della libreria.
64.4 Configurazione Dominio Custom
Vedi Parte II, sezione 9.
64.5 Checklist di Verifica Finale
Elemento	IT	EN
Dominio viewer.artifix.it attivo
✅	✅
HTTPS attivo	✅	✅
Pulsanti Screenshot + Download	✅	✅
Layout uniforme pannello info	✅	✅
Troncamento nome file	✅	✅
Reset uploader al cambio lingua	✅	✅
Sezione info HTML 3D Viewer	✅	✅
64.6 Note Tecniche Importanti
1.	Cache Streamlit: pinning al commit + reboot + 3-4 minuti di attesa
2.	Cache DNS Cloudflare: 5-30 minuti di propagazione
3.	Certificato SSL Let's Encrypt: 5-10 minuti
4.	Viewer HTML statico: non si aggiorna, va rigenerato
5.	Vecchi link: restano funzionanti (alias)
64.7 Riepilogo Azioni Rapide (TL;DR)
Vedi Parte II, sezione 9.4.
________________________________________
APPENDICI
A. Formati Supportati
(invariata rispetto alla v7.3)
B. Riferimenti Tecnici
(invariata rispetto alla v7.3, con aggiunte v7.4)
URL aggiornati:
•	https://www.artifix.it
•	https://artifix.streamlit.app
•	https://viewer.artifix.it (v7.4)
•	https://github.com/alexcool-project/Artifix
•	https://github.com/alexcool-project/mesh2u3d
•	https://github.com/alexcool-project/mesh2u3d-viewer
C. FAQ
(invariata rispetto alla v7.3, con le seguenti aggiunte v7.4)
C.10 Dominio Custom
Q: Cos'è viewer.artifix.it?
A: Dominio custom brandizzato per i viewer HTML condivisibili.
Q: I vecchi link GitHub Pages funzionano ancora?
A: Sì, il dominio custom è un alias.
C.11 Pulsanti Viewer
Q: Cos'è il pulsante "📸 Scatta foto"?
A: Salva uno screenshot professionale con i dati del file.
Q: Cos'è il pulsante "💾 Scarica HTML"?
A: Salva il file HTML per uso offline.
C.12 UX
Q: Cosa succede al cambio lingua con file caricato?
A: L'uploader si resetta automaticamente.
Q: Perché il PDF 3D non è più disponibile?
A: Non era compatibile con Adobe Acrobat base/Pro.
D. Glossario Tecnico
(invariato rispetto alla v7.3, con aggiunte v7.4)
Aggiunti: CNAME, DNS only, Enforce HTTPS, Let's Encrypt, PUBLIC_BASE_URL, Reset uploader.
E. 50 Aziende Target
(invariata rispetto alla v7.3)
________________________________________
CONCLUSIONE
Il Manuale Tecnico ArtiFix v7.4 rappresenta la documentazione definitiva del progetto, con focus su:
•	Libreria mesh2u3d (open source, MIT, from scratch)
•	Libreria estesa: converter, CLI, PRC Writer
•	Viewer HTML 3D universale (three.js, zero Adobe)
•	Viewer HTML bilingue IT/EN completo
•	Dominio custom viewer.artifix.it (brandizzato, HTTPS)
•	Pulsanti "📸 Scatta foto" e "💾 Scarica HTML"
•	Layout uniforme pannello info + troncamento nome file
•	Reset automatico uploader al cambio lingua
•	Sistema di condivisione (link + QR)
•	Automazione completa della sponsorizzazione
•	Documentazione legale completa
•	Sistema anti-sleep a tripla ridondanza
•	SEO ottimizzato
•	Materiali commerciali pronti
Stato del Progetto
Componente	Stato
App Streamlit	✅ Funzionante al 100%
Landing Page	✅ Pubblicata
Dominio + Email	✅ Configurati
Dominio Custom viewer.artifix.it
✅ Attivo (v7.4)
Database Sponsor	✅ Attivo
Automazione Apps Script	✅ 3 trigger attivi
Auto-risposta Sponsor	✅ Testata
Ringraziamento Donazioni	✅ Configurato
Pacchetto Sponsor PDF	✅ Pronto
Locandina	✅ Pronta
Campagna Email Target	✅ Programmate
Documentazione Legale	✅ Completa
Sistema Anti-Sleep	✅ Tripla protezione
README	✅ Aggiornato
Sitemap	✅ 22 URL
Google Search Console	✅ 22 pagine
Libreria mesh2u3d v0.1.0	✅ Funzionante
Modulo Converter	✅ Funzionante (v7.4)
Modulo CLI	✅ Funzionante (v7.4)
Modulo PRC Writer	✅ Funzionante (v7.4)
Viewer HTML 3D	✅ Funzionante
Pulsanti Screenshot + Download	✅ Funzionanti (v7.4)
Traduzioni IT/EN	✅ Complete
Sistema Condivisione Link + QR	✅ Funzionante
Integrazione in ArtiFix	✅ Funzionante
U3D Base Profile completo	📅 Roadmap Q1 2027
Pubblicazione PyPI	📅 Roadmap Q4 2026
Prossimi Traguardi
Breve termine (settimana): Pubblicazione mesh2u3d su PyPI, aggiornamento manuale v7.4, test campagna sponsor.
Medio termine (mese): U3D Base Profile completo, texture PBR, sezioni trasversali.
Lungo termine (trimestre): Exploded view, X-ray mode, app mobile PWA, AI riparazione.
________________________________________
© 2026 ArtiFix — Tutti i diritti riservati
Documento aggiornato al 16 Settembre 2026




---

## 📋 CHECKLIST PER NUOVA SESSIONE

Prima di iniziare a lavorare, verifica:

- [ ] Il report è stato letto integralmente
- [ ] Lo stato corrente è chiaro
- [ ] Le 10 regole sono state comprese
- [ ] I prossimi step sono chiari
- [ ] Il prossimo report da creare è identificato (`report_v7.5.md`)
- [ ] Il registro link è aggiornato (`docs/links/REGISTRY.md`)

---

## 📚 RIFERIMENTI RAPIDI

### Repository
- ArtiFix: `https://github.com/alexcool-project/Artifix`
- mesh2u3d: `https://github.com/alexcool-project/mesh2u3d`
- mesh2u3d-viewer: `https://github.com/alexcool-project/mesh2u3d-viewer`

### URL pubblici
- Landing: `https://www.artifix.it`
- App: `https://artifix.streamlit.app`
- Viewer: `https://viewer.artifix.it`

### File critici
- `app.py` — App Streamlit
- `translations.py` — Traduzioni IT/EN
- `share_utils.py` — Condivisione viewer
- `requirements.txt` — Dipendenze (pin `mesh2u3d@666be25`)
- `docs/links/REGISTRY.md` — Registro link
- `docs/roadmap/report_v7.4.md` — Questo report

---

## 🎯 REGOLE ATTIVE (10)

1. **Verifica oraria + auto-correzione** — ogni ora, controlla e corregge i processi
2. **Report continuativo tra sessioni** — link stabile, self-contained
3. **Sincerità e limiti** — l'AI dichiara sempre i propri limiti
4. **Congelamento manuale + automatico + temporaneo** — flag `SYSTEM_FROZEN`
5. **Notifiche raggruppate ogni 6 ore** — email a info@artifix.it
6. **Versioning progressivo del manuale** — v7.4 → v7.5 → v7.6 → ...
7. **Link stabile al report** — sempre lo stesso link, contenuto aggiornato
8. **Manuale completo su GitHub, aggiornamenti in chat** — GitHub = fonte di verità
9. **Versioning progressivo dei report** — `report_v7.4.md`, `report_v7.5.md`, ...
10. **Link auto-descrittivi** — ogni link ha nome + intestazione YAML + registro

---

## 📌 LINKS CORRETTI PER GITHUB

**Regola:** quando si crea un file nuovo su GitHub, il link deve puntare alla **cartella**, non al file.

| Situazione | Link corretto | Cosa scrivere nel "Name your file" |
|-----------|---------------|-----------------------------------|
| Creare file nuovo | `/new/main/[cartella]/` | Solo il nome file (`report_v7.5.md`) |
| Modificare file esistente | `/edit/main/[cartella]/[file]` | Niente (GitHub lo precompila) |
| Visualizzare file | `/blob/main/[cartella]/[file]` | Niente (solo lettura) |

---

## 📖 COME FUNZIONA IL VERSIONING

**Manuale:**
- Ogni modifica sostanziale incrementa di `0.1` (v7.4 → v7.5 → v7.6 → ...)
- Non si salta mai un numero

**Report:**
- Ogni sessione crea un nuovo file (`report_v7.4.md`, `report_v7.5.md`, ...)
- Ogni file è self-contained (contiene manuale + stato + regole)
- Il link cambia ad ogni versione

**Registro link:**
- `docs/links/REGISTRY.md` elenca tutti i report (attivo + storici)
- Il report attivo è quello con la versione più alta

---

## 📋 PROSSIMI STEP DOPO IL COMMIT

**Quando `report_v7.4.md` è committato:**

1. **Aggiorna `docs/links/REGISTRY.md`** con il link a `report_v7.4.md` (se non è già presente)
2. **Inizia la FASE A** (consolidamento stato stabile):
   - Creare Git tag `v7.4-stable` sui 3 repository
   - Backup dei file critici in `docs/backups/`
   - Documentare `STABLE_STATE_v7.4.md`
3. **Poi FASE B** (setup sistema Roadmap):
   - Google Sheet "Roadmap ArtiFix"
   - Configurazione token
   - Salvataggio nei Secrets
   - Scrittura workflow GitHub Actions
   - Scrittura Apps Script
   - Scrittura dashboard Streamlit
   - Configurazione `roadmap.artifix.it`

---

**© 2026 ArtiFix — Report v7.4**
**Ultimo aggiornamento:** 17 Settembre 2026
**Prossimo report:** `report_v7.5.md`

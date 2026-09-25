# translations.py
# Dizionario completo delle traduzioni IT/EN per ArtiFix

TRANSLATIONS = {
    "it": {
        # --- GENERALE ---
        "app_title": "ArtiFix - Riparazione CAD/CAM Universale",
        "lang_flag": "🇮🇹 Italiano",
        "sidebar_navigation": "Navigazione",
        "sidebar_lang_select": "Lingua / Language",
        "welcome": "Benvenuto su ArtiFix",

        # --- MENU SIDEBAR ---
        "nav_dashboard": "Dashboard",
        "nav_repair": "Ripara File",
        "nav_viewer": "Viewer 3D",
        "nav_convert": "Converti Formati",
        "nav_project": "Progetto ArtiFix",
        "nav_sponsor": "Diventa Sponsor",
        "nav_privacy": "🔒 Privacy Policy",
        "nav_cookie": "🍪 Cookie Policy",
        "nav_terms": "📜 Termini di Servizio",
        "nav_donate": "💙 Dona con PayPal",
        "nav_become_sponsor": "🤝 Diventa Sponsor",

        # --- CONDIVIDI VIEWER 3D (v8.0) ---
        "share_button": "📤 Condividi il file 3D generato",
        "share_info_tooltip": "ℹ️ Cos'è questo pulsante?",
        "share_info_title": "🔗 Condividi il tuo modello 3D",
        "share_info_body": "Puoi condividere il tuo modello 3D in **2 formati diversi**, scegliendo quello più adatto al tuo cliente.",
        "share_info_features": "**Cosa ottiene il tuo cliente:**\n- ✅ Apre il file **senza installare nulla**\n- ✅ Funziona su **PC, Mac, Linux, smartphone**\n- ✅ **Link permanente** o **file scaricabile**",
        "share_info_use_cases": "**🎯 Formati disponibili:**\n- 🌐 **HTML 3D** — link condivisibile + QR code\n- 📄 **PDF 3D** — visualizzabile in Foxit Reader, PDF-XChange, ecc.",
        "share_project_title": "Nome del progetto (visibile al cliente)",
        "share_generate_qr": "Genera anche il QR Code",
        "share_generate_button": "🚀 Genera file condivisibile",
        "share_status_loading": "📖 Lettura del modello...",
        "share_status_processing": "🔧 Elaborazione mesh ({v} vertici, {f} triangoli)...",
        "share_status_publishing": "☁️ Pubblicazione su GitHub Pages...",
        "share_status_done": "✅ Pubblicazione completata!",
        "share_success": "🎉 **File generato!** È pronto per essere condiviso.",
        "share_warning_propagation": "⏱️ **Attendi 30-90 secondi** prima di aprire il link. GitHub Pages impiega fino a 1 minuto per pubblicare il file. Se apri il link subito, potresti vedere un errore **404** — riprova dopo qualche secondo.",
        "share_result_title": "📎 File condivisibile",
        "share_result_url": "URL pubblico:",
        "share_copy_link": "Copia link",
        "share_copy_success": "✅ Link copiato!",
        "share_copy_error": "❌ Errore",
        "share_qr_title": "📱 QR Code",
        "share_qr_caption": "Scansiona con il telefono per aprire il viewer",
        "share_download_qr": "📥 Scarica QR Code (PNG)",
        "share_info_id": "💡 **ID Viewer:** `{id}` — Conserva questo codice per riferimento futuro.",
        "share_error": "❌ **Errore durante la generazione:** {error}",

        # --- FORMATO OUTPUT ---
        "share_format_label": "Formato di output",
        "share_format_html": "🌐 HTML 3D (visualizzabile in qualsiasi browser)",
        "share_format_pdf_u3d": "📄 PDF 3D (compatibile Foxit, PDF-XChange, ecc.)",
        "share_download_pdf": "Scarica PDF 3D",

        # --- HTML 3D VIEWER INFO SECTION (NOVITÀ v7.4) ---
        "html_viewer_title": "🌐 Cos'è l'HTML 3D Viewer?",
        "html_viewer_intro": "L'<strong>HTML 3D Viewer</strong> è un file autonomo che mostra il tuo modello 3D in <strong>qualsiasi browser moderno</strong>, senza installazioni, senza account, senza Adobe.",
        "html_viewer_modes": "Puoi condividerlo in <strong>tre modi</strong>: <strong>link pubblico</strong> (con QR code), <strong>file scaricabile</strong> (.html), oppure <strong>screenshot professionale</strong> per presentazioni e cataloghi.",
        "html_viewer_benefit1_title": "Zero installazioni",
        "html_viewer_benefit1_desc": "Si apre con doppio click nel browser.",
        "html_viewer_benefit2_title": "Zero Adobe",
        "html_viewer_benefit2_desc": "Non serve Acrobat Pro. Funziona con qualsiasi browser.",
        "html_viewer_benefit3_title": "Mobile-ready",
        "html_viewer_benefit3_desc": "Smartphone, tablet, desktop. Nessuna limitazione.",
        "html_viewer_benefit4_title": "Interattivo",
        "html_viewer_benefit4_desc": "Ruota, zooma, cambia materiale, X-Ray, wireframe.",
        "html_viewer_benefit5_title": "Link + QR",
        "html_viewer_benefit5_desc": "Condividi via email, WhatsApp, SMS.",
        "html_viewer_benefit6_title": "Persistente",
        "html_viewer_benefit6_desc": "Il file è tuo, per sempre. Funziona anche offline.",

        # --- BOX FORMATI PROPRIETARI (DWG/SKP/RVT) ---
        "prop_title": "🔓 Hai un file DWG, SKP o RVT?",
        "prop_intro": "Nessun problema! ArtiFix supporta **tutti i formati CAD più comuni**. Basta una semplice esportazione dal tuo software per accedere a tutti i servizi ArtiFix.",
        "prop_step1_title": "Apri il file",
        "prop_step1_desc": "nel software originale (AutoCAD, SketchUp, Revit, ecc.)",
        "prop_step2_title": "Esporta in DAE (Collada)",
        "prop_step2_desc": "o **OBJ** — formati universali e gratuiti",
        "prop_step3_title": "Carica su ArtiFix",
        "prop_step3_desc": "e converti in qualsiasi formato (STL, 3D PDF, DXF, ecc.)",
        "prop_btn_guide": "📖 Guida: esportare DWG in DAE",
        "prop_note": "💡 **DAE (Collada)** e **OBJ** sono formati universali che possono essere esportati dalla quasi totalità dei software CAD 3D presenti sul mercato.",

        # --- TENDINA NOTE FORMATI PROPRIETARI ---
        "notes_expander_title": "📝 Note: formati proprietari (DWG, SKP, RVT, STEP, IGES)",
        "notes_expander_intro": "ArtiFix supporta nativamente oltre 50 formati. **Alcuni formati proprietari non possono essere letti direttamente** perché richiedono librerie commerciali. Ecco come procedere:",
        "notes_expander_native": "**✅ Supportati nativamente:** STL, OBJ, PLY, GLB, GLTF, FBX, 3MF, DAE, WRL, OFF, U3D, DXF, 3D PDF, SVG, DOCX, XLSX, IFC, SHP, GeoJSON, KML, GPX.",
        "notes_expander_not_supported": "**❌ NON supportati direttamente:** DWG, SKP, RVT, STEP, IGES, DGN, DWT.",
        "notes_expander_howto": "**🔧 Come procedere per i formati non supportati:**",
        "notes_expander_steps": """1. **Apri il file** nel software con cui è stato creato (AutoCAD, SketchUp, Revit, FreeCAD, ecc.)
2. **Esporta in DAE (Collada)** o **OBJ** — formati universali e gratuiti
3. **Carica il file DAE/OBJ** su ArtiFix e converti in qualsiasi altro formato (STL, 3D PDF, GLB, ecc.)""",
        "notes_expander_tip": "💡 **Suggerimento:** la quasi totalità dei software CAD 3D (AutoCAD, SketchUp, Revit, Rhino, FreeCAD) può esportare in DAE o OBJ con un semplice click su **File → Esporta → DAE/OBJ**.",
        "notes_expander_guide_link": "📖 Leggi la guida completa: esportare DWG in DAE",

        # --- COOKIE BANNER ---
        "cookie_title": "🍪 Cookie Policy",
        "cookie_text": "Noi e terze parti selezionate utilizziamo cookie o tecnologie simili per finalità tecniche e, con il tuo consenso, anche per altre finalità come specificato nella cookie policy. Il rifiuto del consenso può rendere non disponibili le relative funzioni. Usa il pulsante \"Accetta tutti i cookie\" per acconsentire. Usa il pulsante \"Accetta solo i cookie necessari\" per continuare senza accettare.",
        "cookie_check_privacy": "Consulta la Privacy Policy tramite il pulsante apposito",
        "cookie_accept_necessary": "Accetta solo i cookie necessari",
        "cookie_accept_all": "Accetta tutti i cookie",

        # --- DASHBOARD ---
        "dash_header": "📊 Dashboard",
        "dash_metric_repaired": "File Riparati",
        "dash_metric_conversions": "Conversioni",
        "dash_metric_formats": "Formati",
        "dash_metric_online": "Online",
        "dash_metric_uptime": "Uptime 30 giorni",
        "dash_error_load": "⚠️ Impossibile caricare le metriche dal foglio. Mostro i valori di fallback.",
        "dash_supported_formats": "📁 Formati Supportati (50+ estensioni)",
        "dash_info_select": "👈 Seleziona una funzionalità dal menu.",

        # --- RIPARA FILE ---
        "repair_header": "🛠️ Centro Riparazione File",
        "repair_upload": "Seleziona un file",
        "repair_upload_hint": "💡 **Formati supportati:** DXF, STL, OBJ, PLY, GLB, GLTF, FBX, 3MF, DAE, WRL, OFF, U3D, IFC, SHP, GEOJSON, KML, GPX, SVG, **3D PDF** (con modello 3D incorporato **.u3d**), DOCX, XLSX. I formati proprietari (DWG, SKP, RVT, STEP, IGES) devono essere esportati in DAE o OBJ.",
        "repair_status_analyzing": "Analisi del file in corso... (30%)",
        "repair_status_verifying": "Verifica del risultato... (60%)",
        "repair_status_completing": "Completamento... (100%)",
        "repair_status_error": "Errore durante l'analisi",
        "repair_details": "Dettagli",
        "repair_button_repair": "🔧 Ripara",
        "repair_button_download": "📥 Scarica",
        "repair_success": "✅ Riparato!",

        # --- ERRORI RIPARAZIONE ---
        "repair_error_non_mesh_title": "❌ **Formato non supportato per la riparazione.**",
        "repair_error_non_mesh_desc": "Il file `{ext}` è un file di **{tipo}**, non una mesh 3D.",
        "repair_error_non_mesh_hint": "Per lavorare con file {tipo}, usa la sezione **Converti Formati** o il **Viewer 3D**.",
        "repair_error_pdf_hint": "⚠️ **Attenzione:** i PDF standard (non 3D) non possono essere riparati, convertiti o visualizzati. Solo i **3D PDF** con modello 3D incorporato (**U3D**) possono essere visualizzati nel **Viewer 3D**.",
        "repair_error_invalid_mesh_title": "❌ **Impossibile riparare questo file.**",
        "repair_error_invalid_mesh_desc": "Il file `{ext}` non contiene una mesh 3D valida con vertici e facce.",
        "repair_error_invalid_mesh_hint": "Formati supportati: **STL, OBJ, PLY, GLB, GLTF, FBX, 3MF, DAE, WRL, OFF, U3D**.",

        # --- TIPI DI FORMATO NON-MESH ---
        "type_svg": "grafica vettoriale 2D",
        "type_pdf": "documento PDF",
        "type_docx": "documento Word",
        "type_xlsx": "foglio di calcolo Excel",
        "type_dxf": "disegno CAD 2D",
        "type_dwg": "disegno CAD 2D proprietario",

        # --- REPORT RIPARAZIONE ---
        "report_header": "📊 Report Riparazione Dettagliato",
        "report_subtitle": "Analisi completa delle modifiche apportate al file.",
        "report_before": "Stato Iniziale (Prima)",
        "report_after": "Stato Finale (Dopo)",
        "report_actions": "Azioni Applicate",
        "report_summary": "Riepilogo Finale",
        "report_metric": "Metrica",
        "report_value_before": "Valore Iniziale",
        "report_value_after": "Valore Finale",
        "report_vertices": "Vertici",
        "report_faces": "Facce",
        "report_watertight": "Watertight",
        "report_non_manifold": "Spigoli Non-Manifold",
        "report_degenerate": "Triangoli Degeneri",
        "report_duplicates": "Vertici Duplicati",
        "report_holes": "Buchi",
        "report_fixed": "Risolto",
        "report_not_fixed": "Non Risolto",
        "report_action_merged_vertices": "Vertici duplicati uniti",
        "report_action_removed_degenerate": "Triangoli degeneri rimossi",
        "report_action_fixed_normals": "Normali invertite corrette",
        "report_action_filled_holes": "Buchi chiusi",
        "report_action_fix_inversion": "Inversione volume corretta",
        "report_action_removed_duplicate_faces": "Facce duplicate rimosse",
        "report_summary_issues": "Problemi risolti",
        "report_summary_watertight": "Watertight",
        "report_download_pdf": "📥 Scarica Report PDF",
        "report_no_issues": "✅ Nessun problema rilevato. Il file è già ottimale.",

        # --- VIEWER 3D ---
        "viewer_header": "🖥️ Viewer 3D",
        "viewer_upload": "Carica modello 3D",
        "viewer_upload_hint": "💡 **Formati supportati:** STL, OBJ, PLY, GLB, GLTF, FBX, 3MF, DAE, WRL, OFF, U3D, **3D PDF** (il file PDF deve contenere un modello 3D incorporato in formato **.u3d**).",
        "viewer_status_loading": "Caricamento del modello... (30%)",
        "viewer_status_processing": "Elaborazione vertici e facce... (60%)",
        "viewer_status_building": "Costruzione della vista 3D... (100%)",
        "viewer_success": "✅ {vertices} vertici, {faces} facce",
        "viewer_error_processing": "❌ Errore nel processamento della mesh.",
        "viewer_warning_no_model": "⚠️ Impossibile caricare il modello.",
        "viewer_error_generic": "❌ Errore: {error}",
        "viewer_legend": "🔄 Trascina per ruotare | 🖱️ Tasto destro per spostare | 🖱️ Rotella per zoom",
        "viewer_legend_axes": "X (Rosso) | Y (Verde) | Z (Blu)",

        # --- 3D PDF DETECTION ---
        "pdf_no_3d_title": "❌ **Il PDF non contiene un modello 3D incorporato.**",
        "pdf_no_3d_desc": "Il file `{filename}` è un PDF standard, non un 3D PDF. Per visualizzarlo nel Viewer 3D, deve contenere un modello 3D in formato **U3D**.",
        "pdf_no_3d_howto_title": "📖 Come creare un 3D PDF",
        "pdf_no_3d_howto_steps": """1. Apri il tuo modello in un software CAD (AutoCAD, SketchUp, Revit, FreeCAD, ecc.)
2. Esporta il modello in formato **U3D** (formato 3D incorporabile)
3. Usa **Adobe Acrobat Pro** o **Foxit PhantomPDF** per creare un 3D PDF:
   - Apri un PDF vuoto
   - Vai su **Strumenti → 3D → Aggiungi 3D**
   - Seleziona il file U3D esportato
   - Salva il PDF
4. Carica il 3D PDF su ArtiFix per visualizzarlo""",
        "pdf_no_3d_alternative": "💡 **Alternativa più semplice:** carica direttamente il file **U3D** nel Viewer 3D (è supportato nativamente, senza bisogno del PDF).",
        "pdf_3d_detected": "✅ **3D PDF rilevato!** Contiene un modello 3D incorporato. Elaborazione in corso...",

        # --- CONVERTI FORMATI ---
        "convert_header": "🔄 Conversione Formati Universale",
        "convert_subtitle": "Converti file tra **tutti i formati** supportati con **tutte le combinazioni** possibili.",
        "convert_expander_matrix": "📋 Matrice delle conversioni disponibili",
        "convert_caption_matrix": "✅ = Conversione supportata | ❌ = Conversione non supportata",
        "convert_upload": "Carica un file da convertire",
        "convert_upload_hint": "💡 Clicca per cercare il file sul tuo computer, oppure trascina e rilascia il file qui.",
        "convert_target_format": "Formato di destinazione",
        "convert_button_convert": "🔄 Converti in {format}",
        "convert_status_loading": "Caricamento e analisi del modello... (20%)",
        "convert_status_converting": "Conversione in corso... (70%)",
        "convert_status_saving": "Salvataggio del file... (100%)",
        "convert_success": "✅ Conversione in {format} completata!",
        "convert_info_ready": "📥 Il file è pronto! Clicca il pulsante qui sotto per scaricarlo.",
        "convert_button_download": "📥 Scarica .{format}",
        "convert_error": "❌ Conversione in {format} fallita. Riprova con un altro formato.",
        "convert_error_load": "❌ Impossibile caricare il modello. Assicurati che il file sia un modello 3D valido.",
        "convert_button_preview": "🖥️ Mostra anteprima interattiva (ruota con il mouse)",
        "convert_info_preview": "💡 Ruota il modello a 360° con il mouse o il touchpad",
        "convert_warning_format": "⚠️ Il formato **.{format}** non può essere convertito in altri formati.",
        "convert_info_formats": "💡 I formati convertibili sono: **STL, OBJ, PLY, GLB, GLTF, FBX, 3MF, DAE, WRL, OFF, DXF, PDF**.",
        "convert_warning_no_target": "⚠️ Nessun formato di destinazione disponibile per questo file.",
        "convert_warning_no_preview": "⚠️ Impossibile caricare il modello per l'anteprima. Assicurati che il file sia un modello 3D valido.",
        "convert_file_type": "Tipo: {type} | Estensione: .{ext}",

        # --- PROGETTO ARTIFIX ---
        "project_header": "🚀 Progetto ArtiFix",
        "project_text": """**ArtiFix** è una piattaforma professionale per la riparazione, conversione e visualizzazione di file CAD/CAM.
Questo progetto è in continua evoluzione. Per richieste di informazioni, collaborazioni o assistenza tecnica, contattaci.""",
        "project_contact": "📧 Contattaci",
        "project_contact_text": "Invia una richiesta a info@artifix.it",
        "project_form_name": "Il tuo nome",
        "project_form_email": "La tua email",
        "project_form_message": "Messaggio",
        "project_form_submit": "Invia",
        "project_success": "Email inviata con successo!",
        "project_error": "Errore: {error}",
        "project_warning": "Compila tutti i campi prima di inviare.",

        # --- DIVENTA SPONSOR ---
        "sponsor_header": "🤝 Diventa Sponsor di ArtiFix",
        "sponsor_intro": """**ArtiFix** è un progetto indipendente che offre strumenti gratuiti per la riparazione, conversione e visualizzazione di file CAD/CAM.

Ogni giorno centinaia di professionisti, studenti e appassionati utilizzano i servizi di ArtiFix. Se anche tu credi in questo progetto e vuoi sostenerlo, puoi diventare **sponsor**.""",
        "sponsor_format_title": "📐 Formato banner richiesto",
        "sponsor_format_text": """- **Dimensioni:** 300 × 100 px
- **Formato file:** PNG (preferito) o JPG
- **Sfondo:** trasparente o neutro
- **Peso massimo:** 200 KB
- **Contenuto:** logo aziendale + eventuale payoff breve""",
        "sponsor_how_title": "💶 Come funziona",
        "sponsor_how_text": """1. Effettui una **donazione liberale** tramite il pulsante PayPal qui sotto.
2. Compili il form con i dati del tuo brand (nome, sito, email, logo).
3. Entro 24-48h il tuo banner viene pubblicato nella banda laterale di ArtiFix per **30 giorni**.
4. Al termine dei 30 giorni, se desideri rinnovare, puoi donare nuovamente.""",
        "sponsor_donate_button": "💙 Dona con PayPal",
        "sponsor_form_title": "📤 Invia la tua richiesta",
        "sponsor_form_caption": "Dopo aver effettuato la donazione, compila questo form con i dati del tuo brand.",
        "sponsor_form_brand": "Nome brand/azienda *",
        "sponsor_form_email": "Email di riferimento *",
        "sponsor_form_site": "Sito web (URL completo, es. https://www.miosito.it) *",
        "sponsor_form_logo": "URL Raw di GitHub del logo (es. https://raw.githubusercontent.com/.../logo.png) — 300×100 px, PNG o JPG, max 200 KB *",
        "sponsor_form_message": "Messaggio opzionale (breve descrizione attività)",
        "sponsor_form_submit": "Invia richiesta sponsor",
        "sponsor_form_success": "✅ Richiesta inviata! Ti contatteremo entro 48h.",
        "sponsor_form_error": "Errore invio: {error}",
        "sponsor_form_warning": "Compila tutti i campi obbligatori (*).",
        "sponsor_form_info": "💡 Dopo la donazione, invia la richiesta tramite questo form. Il tuo banner sarà attivo entro 24-48h.",

        # --- PRIVACY POLICY ---
        "privacy_header": "🔒 Privacy Policy",
        "privacy_subtitle": "**ArtiFix - Riparazione File CAD/CAM Universale**",
        "privacy_updated": "Ultimo aggiornamento: 15 settembre 2026",
        "privacy_back": "← Torna alla Dashboard",
        "privacy_content": """La presente Privacy Policy è resa ai sensi dell'Art. 13 del Regolamento (UE) 2016/679 (GDPR), relativo alla protezione delle persone fisiche con riguardo al trattamento dei dati personali.

### 1. Titolare del Trattamento
Il Titolare del trattamento dei dati è **ArtiFix**, con sede in Italia. Per qualsiasi richiesta è possibile contattare il Titolare all'indirizzo email: **info@artifix.it**.

### 2. Dati raccolti e finalità
**Dati forniti volontariamente dall'utente**: Attraverso il form "Contattaci" vengono raccolti nome, indirizzo email e messaggio, al fine di rispondere alle richieste pervenute.
**Dati di navigazione**: Il sito utilizza cookie tecnici (per il funzionamento) e cookie di analytics (facoltativi) come descritto nella Cookie Policy.
**File caricati**: I file caricati dagli utenti per la conversione vengono elaborati temporaneamente in memoria sul server e non vengono conservati dopo l'elaborazione.

### 3. Dati raccolti per Donazioni e Sponsorizzazioni
**Dati del Donatore**: nome, email, importo, data, metodo di pagamento.
**Dati dello Sponsor**: nome brand, logo URL, sito web, email di riferimento, telefono (facoltativo), data inizio, durata.
**Base giuridica**: consenso (Art. 6, par. 1, lett. a GDPR) + liberalità (Art. 6, par. 1, lett. b GDPR).
**Conservazione**: 10 anni per donazioni, 24 mesi per sponsorizzazioni.

### 4. Diritti dell'interessato
Ai sensi degli Artt. 15-22 del GDPR, l'utente ha il diritto di: accesso, rettifica, cancellazione, limitazione, opposizione, portabilità, revoca del consenso.
Per esercitare tali diritti: **info@artifix.it**

### 5. Comunicazione e diffusione
I dati non saranno ceduti a terzi per finalità di marketing o venduti. Possono essere comunicati a PayPal (pagamenti), Google (archiviazione), commercialista (obblighi fiscali), autorità competenti.

### 6. Trasferimento dei dati
I dati non vengono trasferiti al di fuori dell'Unione Europea. L'app è ospitata su Streamlit Cloud (USA), ma il trattamento dei file avviene in memoria.

### 7. Modifiche alla Privacy Policy
La presente Privacy Policy può essere soggetta ad aggiornamenti. La versione aggiornata sarà sempre disponibile su questa pagina.""",

        # --- COOKIE POLICY ---
        "cookie_policy_header": "🍪 Cookie Policy",
        "cookie_policy_subtitle": "**ArtiFix - Riparazione File CAD/CAM Universale**",
        "cookie_policy_updated": "Ultimo aggiornamento: 15 settembre 2026",
        "cookie_policy_back": "← Torna alla Dashboard",
        "cookie_policy_content": """La presente Cookie Policy è resa ai sensi dell'art. 13 del Regolamento (UE) 2016/679 (GDPR) e del Provvedimento del Garante per la Protezione dei Dati Personali del 10 giugno 2021.

### 1. Titolare del Trattamento
Il Titolare del trattamento dei dati è **ArtiFix**, con sede in Italia. Per qualsiasi richiesta è possibile contattare il Titolare all'indirizzo email: **info@artifix.it**.

### 2. Cosa sono i Cookie
I cookie sono piccoli file di testo che i siti web inviano e registrano sul computer o dispositivo mobile dell'utente, per essere poi ritrasmessi agli stessi siti alle visite successive. Servono a ricordare le azioni e le preferenze dell'utente.

### 3. Tipologie di Cookie utilizzate
Questo sito utilizza esclusivamente **Cookie Tecnici (o strettamente necessari)**. Questi cookie sono essenziali per il funzionamento del sito e non richiedono il consenso preventivo dell'utente.

*   **Cookie di Sessione**: Vengono eliminati automaticamente alla chiusura del browser.
*   **Cookie di Funzionalità**: Permettono di ricordare le scelte dell'utente (es. limite di upload 5GB).

**Cookie di Terze Parti / Profilazione**: Questo sito **non utilizza** cookie di profilazione, di marketing o di terze parti.

### 4. Gestione del Consenso
Al primo accesso, l'utente può scegliere se accettare o rifiutare i cookie tramite l'apposito banner.

### 5. Come disabilitare i Cookie tramite il Browser
*   **Google Chrome**: [Istruzioni](https://support.google.com/chrome/answer/95647)
*   **Mozilla Firefox**: [Istruzioni](https://support.mozilla.org/kb/block-websites-storing-cookies)
*   **Microsoft Edge**: [Istruzioni](https://support.microsoft.com/microsoft-edge/delete-cookies-in-microsoft-edge)
*   **Safari**: [Istruzioni](https://support.apple.com/guide/safari/manage-cookies)

### 6. Diritti dell'Interessato
Ai sensi degli artt. 15-22 del GDPR, l'utente ha il diritto di accesso, rettifica, cancellazione, limitazione, opposizione e portabilità dei propri dati personali. Per esercitare tali diritti: **info@artifix.it**.

### 7. Aggiornamenti
La presente Cookie Policy può essere soggetta ad aggiornamenti.""",

        # --- FOOTER ---
        "footer": "© 2026 ArtiFix | Tutti i diritti riservati",
    },

    "en": {
        # --- GENERAL ---
        "app_title": "ArtiFix - Universal CAD/CAM Repair",
        "lang_flag": "🇬🇧 English",
        "sidebar_navigation": "Navigation",
        "sidebar_lang_select": "Lingua / Language",
        "welcome": "Welcome to ArtiFix",

        # --- SIDEBAR MENU ---
        "nav_dashboard": "Dashboard",
        "nav_repair": "Repair File",
        "nav_viewer": "3D Viewer",
        "nav_convert": "Convert Formats",
        "nav_project": "ArtiFix Project",
        "nav_sponsor": "Become a Sponsor",
        "nav_privacy": "🔒 Privacy Policy",
        "nav_cookie": "🍪 Cookie Policy",
        "nav_terms": "📜 Terms of Service",
        "nav_donate": "💙 Donate with PayPal",
        "nav_become_sponsor": "🤝 Become a Sponsor",

        # --- SHARE 3D VIEWER (v8.0) ---
        "share_button": "📤 Share the generated 3D file",
        "share_info_tooltip": "ℹ️ What is this button?",
        "share_info_title": "🔗 Share your 3D model",
        "share_info_body": "You can share your 3D model in **2 different formats**, choosing the one that best suits your client.",
        "share_info_features": "**What your client gets:**\n- ✅ Opens the file **without installing anything**\n- ✅ Works on **PC, Mac, Linux, smartphone**\n- ✅ **Permanent link** or **downloadable file**",
        "share_info_use_cases": "**🎯 Available formats:**\n- 🌐 **HTML 3D** — shareable link + QR code\n- 📄 **PDF 3D** — viewable in Foxit Reader, PDF-XChange, etc.",
        "share_project_title": "Project name (visible to client)",
        "share_generate_qr": "Also generate QR Code",
        "share_generate_button": "🚀 Generate shareable file",
        "share_status_loading": "📖 Reading model...",
        "share_status_processing": "🔧 Processing mesh ({v} vertices, {f} triangles)...",
        "share_status_publishing": "☁️ Publishing to GitHub Pages...",
        "share_status_done": "✅ Publishing completed!",
        "share_success": "🎉 **File generated!** It's ready to be shared.",
        "share_warning_propagation": "⏱️ **Wait 30-90 seconds** before opening the link. GitHub Pages takes up to 1 minute to publish the file. If you open the link immediately, you may see a **404** error — try again after a few seconds.",
        "share_result_title": "📎 Shareable file",
        "share_result_url": "Public URL:",
        "share_copy_link": "Copy link",
        "share_copy_success": "✅ Link copied!",
        "share_copy_error": "❌ Error",
        "share_qr_title": "📱 QR Code",
        "share_qr_caption": "Scan with your phone to open the viewer",
        "share_download_qr": "📥 Download QR Code (PNG)",
        "share_info_id": "💡 **Viewer ID:** `{id}` — Keep this code for future reference.",
        "share_error": "❌ **Generation error:** {error}",

        # --- OUTPUT FORMAT ---
        "share_format_label": "Output format",
        "share_format_html": "🌐 HTML 3D (viewable in any browser)",
        "share_format_pdf_u3d": "📄 3D PDF (Foxit, PDF-XChange compatible)",
        "share_download_pdf": "Download 3D PDF",

        # --- HTML 3D VIEWER INFO SECTION (NEW v7.4) ---
        "html_viewer_title": "🌐 What is the HTML 3D Viewer?",
        "html_viewer_intro": "The <strong>HTML 3D Viewer</strong> is a standalone file that shows your 3D model in <strong>any modern browser</strong>, without installations, without accounts, without Adobe.",
        "html_viewer_modes": "You can share it in <strong>three ways</strong>: <strong>public link</strong> (with QR code), <strong>downloadable file</strong> (.html), or <strong>professional screenshot</strong> for presentations and catalogs.",
        "html_viewer_benefit1_title": "Zero installations",
        "html_viewer_benefit1_desc": "Opens with a double click in the browser.",
        "html_viewer_benefit2_title": "Zero Adobe",
        "html_viewer_benefit2_desc": "No Acrobat Pro needed. Works with any browser.",
        "html_viewer_benefit3_title": "Mobile-ready",
        "html_viewer_benefit3_desc": "Smartphone, tablet, desktop. No limitations.",
        "html_viewer_benefit4_title": "Interactive",
        "html_viewer_benefit4_desc": "Rotate, zoom, change material, X-Ray, wireframe.",
        "html_viewer_benefit5_title": "Link + QR",
        "html_viewer_benefit5_desc": "Share via email, WhatsApp, SMS.",
        "html_viewer_benefit6_title": "Persistent",
        "html_viewer_benefit6_desc": "The file is yours, forever. Works offline too.",

        # --- PROPRIETARY FORMATS BOX (DWG/SKP/RVT) ---
        "prop_title": "🔓 Have a DWG, SKP or RVT file?",
        "prop_intro": "No problem! ArtiFix supports **all common CAD formats**. A simple export from your software gives you access to all ArtiFix services.",
        "prop_step1_title": "Open the file",
        "prop_step1_desc": "in the original software (AutoCAD, SketchUp, Revit, etc.)",
        "prop_step2_title": "Export to DAE (Collada)",
        "prop_step2_desc": "or **OBJ** — universal, free formats",
        "prop_step3_title": "Upload to ArtiFix",
        "prop_step3_desc": "and convert to any format (STL, 3D PDF, DXF, etc.)",
        "prop_btn_guide": "📖 Guide: export DWG to DAE",
        "prop_note": "💡 **DAE (Collada)** and **OBJ** are universal formats that can be exported from almost all 3D CAD software on the market.",

        # --- NOTES EXPANDER: PROPRIETARY FORMATS ---
        "notes_expander_title": "📝 Note: proprietary formats (DWG, SKP, RVT, STEP, IGES)",
        "notes_expander_intro": "ArtiFix natively supports 50+ formats. **Some proprietary formats cannot be read directly** because they require commercial libraries. Here's how to proceed:",
        "notes_expander_native": "**✅ Natively supported:** STL, OBJ, PLY, GLB, GLTF, FBX, 3MF, DAE, WRL, OFF, U3D, DXF, 3D PDF, SVG, DOCX, XLSX, IFC, SHP, GeoJSON, KML, GPX.",
        "notes_expander_not_supported": "**❌ NOT directly supported:** DWG, SKP, RVT, STEP, IGES, DGN, DWT.",
        "notes_expander_howto": "**🔧 How to proceed for unsupported formats:**",
        "notes_expander_steps": """1. **Open the file** in the software it was created with (AutoCAD, SketchUp, Revit, FreeCAD, etc.)
2. **Export to DAE (Collada)** or **OBJ** — universal, free formats
3. **Upload the DAE/OBJ file** to ArtiFix and convert to any other format (STL, 3D PDF, GLB, etc.)""",
        "notes_expander_tip": "💡 **Tip:** almost all 3D CAD software (AutoCAD, SketchUp, Revit, Rhino, FreeCAD) can export to DAE or OBJ with a simple click on **File → Export → DAE/OBJ**.",
        "notes_expander_guide_link": "📖 Read the full guide: export DWG to DAE",

        # --- COOKIE BANNER ---
        "cookie_title": "🍪 Cookie Policy",
        "cookie_text": "We and selected third parties use cookies or similar technologies for technical purposes and, with your consent, also for other purposes as specified in the cookie policy. Denying consent may make related features unavailable. Use the \"Accept all cookies\" button to consent. Use the \"Accept only necessary cookies\" button to continue without accepting.",
        "cookie_check_privacy": "View the Privacy Policy using the dedicated button",
        "cookie_accept_necessary": "Accept only necessary cookies",
        "cookie_accept_all": "Accept all cookies",

        # --- DASHBOARD ---
        "dash_header": "📊 Dashboard",
        "dash_metric_repaired": "Repaired Files",
        "dash_metric_conversions": "Conversions",
        "dash_metric_formats": "Formats",
        "dash_metric_online": "Online",
        "dash_metric_uptime": "30-day Uptime",
        "dash_error_load": "⚠️ Unable to load metrics from sheet. Showing fallback values.",
        "dash_supported_formats": "📁 Supported Formats (50+ extensions)",
        "dash_info_select": "👈 Select a feature from the menu.",

        # --- REPAIR FILE (EN) ---
        "repair_header": "🛠️ File Repair Center",
        "repair_upload": "Select a file",
        "repair_upload_hint": "💡 **Supported formats:** DXF, STL, OBJ, PLY, GLB, GLTF, FBX, 3MF, DAE, WRL, OFF, U3D, IFC, SHP, GEOJSON, KML, GPX, SVG, **3D PDF** (with embedded 3D model **.u3d**), DOCX, XLSX. Proprietary formats (DWG, SKP, RVT, STEP, IGES) must be exported to DAE or OBJ.",
        "repair_status_analyzing": "Analyzing file... (30%)",
        "repair_status_verifying": "Verifying result... (60%)",
        "repair_status_completing": "Completing... (100%)",
        "repair_status_error": "Error during analysis",
        "repair_details": "Details",
        "repair_button_repair": "🔧 Repair",
        "repair_button_download": "📥 Download",
        "repair_success": "✅ Repaired!",

        # --- REPAIR ERRORS (EN) ---
        "repair_error_non_mesh_title": "❌ **Format not supported for repair.**",
        "repair_error_non_mesh_desc": "The file `{ext}` is a **{tipo}** file, not a 3D mesh.",
        "repair_error_non_mesh_hint": "To work with {tipo} files, use the **Convert Formats** section or the **3D Viewer**.",
        "repair_error_pdf_hint": "⚠️ **Warning:** standard PDFs (non-3D) cannot be repaired, converted, or viewed. Only **3D PDFs** with embedded 3D models (**U3D**) can be viewed in the **3D Viewer**.",
        "repair_error_invalid_mesh_title": "❌ **Unable to repair this file.**",
        "repair_error_invalid_mesh_desc": "The file `{ext}` does not contain a valid 3D mesh with vertices and faces.",
        "repair_error_invalid_mesh_hint": "Supported formats: **STL, OBJ, PLY, GLB, GLTF, FBX, 3MF, DAE, WRL, OFF, U3D**.",

        # --- FORMAT TYPES (EN) ---
        "type_svg": "2D vector graphics",
        "type_pdf": "PDF document",
        "type_docx": "Word document",
        "type_xlsx": "Excel spreadsheet",
        "type_dxf": "2D CAD drawing",
        "type_dwg": "proprietary 2D CAD drawing",

        # --- REPAIR REPORT (EN) ---
        "report_header": "📊 Detailed Repair Report",
        "report_subtitle": "Complete analysis of changes made to the file.",
        "report_before": "Initial State (Before)",
        "report_after": "Final State (After)",
        "report_actions": "Applied Actions",
        "report_summary": "Final Summary",
        "report_metric": "Metric",
        "report_value_before": "Initial Value",
        "report_value_after": "Final Value",
        "report_vertices": "Vertices",
        "report_faces": "Faces",
        "report_watertight": "Watertight",
        "report_non_manifold": "Non-Manifold Edges",
        "report_degenerate": "Degenerate Triangles",
        "report_duplicates": "Duplicate Vertices",
        "report_holes": "Holes",
        "report_fixed": "Fixed",
        "report_not_fixed": "Not Fixed",
        "report_action_merged_vertices": "Merged duplicate vertices",
        "report_action_removed_degenerate": "Removed degenerate triangles",
        "report_action_fixed_normals": "Fixed inverted normals",
        "report_action_filled_holes": "Filled holes",
        "report_action_fix_inversion": "Fixed volume inversion",
        "report_action_removed_duplicate_faces": "Removed duplicate faces",
        "report_summary_issues": "Issues resolved",
        "report_summary_watertight": "Watertight",
        "report_download_pdf": "📥 Download PDF Report",
        "report_no_issues": "✅ No issues detected. The file is already optimal.",

        # --- 3D VIEWER (EN) ---
        "viewer_header": "🖥️ 3D Viewer",
        "viewer_upload": "Upload 3D model",
        "viewer_upload_hint": "💡 **Supported formats:** STL, OBJ, PLY, GLB, GLTF, FBX, 3MF, DAE, WRL, OFF, U3D, **3D PDF** (the PDF file must contain an embedded 3D model in **.u3d** format).",
        "viewer_status_loading": "Loading model... (30%)",
        "viewer_status_processing": "Processing vertices and faces... (60%)",
        "viewer_status_building": "Building 3D view... (100%)",
        "viewer_success": "✅ {vertices} vertices, {faces} faces",
        "viewer_error_processing": "❌ Error processing mesh.",
        "viewer_warning_no_model": "⚠️ Unable to load model.",
        "viewer_error_generic": "❌ Error: {error}",
        "viewer_legend": "🔄 Drag to rotate | 🖱️ Right click to pan | 🖱️ Scroll to zoom",
        "viewer_legend_axes": "X (Red) | Y (Green) | Z (Blue)",

        # --- 3D PDF DETECTION (EN) ---
        "pdf_no_3d_title": "❌ **The PDF does not contain an embedded 3D model.**",
        "pdf_no_3d_desc": "The file `{filename}` is a standard PDF, not a 3D PDF. To view it in the 3D Viewer, it must contain a 3D model in **U3D** format.",
        "pdf_no_3d_howto_title": "📖 How to create a 3D PDF",
        "pdf_no_3d_howto_steps": """1. Open your model in CAD software (AutoCAD, SketchUp, Revit, FreeCAD, etc.)
2. Export the model to **U3D** format (embeddable 3D format)
3. Use **Adobe Acrobat Pro** or **Foxit PhantomPDF** to create a 3D PDF:
   - Open a blank PDF
   - Go to **Tools → 3D → Add 3D**
   - Select the exported U3D file
   - Save the PDF
4. Upload the 3D PDF to ArtiFix to view it""",
        "pdf_no_3d_alternative": "💡 **Simpler alternative:** upload the **U3D** file directly to the 3D Viewer (it is natively supported, no PDF needed).",
        "pdf_3d_detected": "✅ **3D PDF detected!** It contains an embedded 3D model. Processing...",

        # --- CONVERT FORMATS (EN) ---
        "convert_header": "🔄 Universal Format Conversion",
        "convert_subtitle": "Convert files between **all supported formats** with **all possible combinations**.",
        "convert_expander_matrix": "📋 Available conversion matrix",
        "convert_caption_matrix": "✅ = Supported conversion | ❌ = Unsupported conversion",
        "convert_upload": "Upload a file to convert",
        "convert_upload_hint": "💡 Click to browse for the file on your computer, or drag and drop the file here.",
        "convert_target_format": "Target format",
        "convert_button_convert": "🔄 Convert to {format}",
        "convert_status_loading": "Loading and analyzing model... (20%)",
        "convert_status_converting": "Converting... (70%)",
        "convert_status_saving": "Saving file... (100%)",
        "convert_success": "✅ Conversion to {format} completed!",
        "convert_info_ready": "📥 The file is ready! Click the button below to download it.",
        "convert_button_download": "📥 Download .{format}",
        "convert_error": "❌ Conversion to {format} failed. Try another format.",
        "convert_error_load": "❌ Unable to load model. Make sure the file is a valid 3D model.",
        "convert_button_preview": "🖥️ Show interactive preview (rotate with mouse)",
        "convert_info_preview": "💡 Rotate the model 360° with the mouse or touchpad",
        "convert_warning_format": "⚠️ The **.{format}** format cannot be converted to other formats.",
        "convert_info_formats": "💡 Convertible formats are: **STL, OBJ, PLY, GLB, GLTF, FBX, 3MF, DAE, WRL, OFF, DXF, PDF**.",
        "convert_warning_no_target": "⚠️ No target format available for this file.",
        "convert_warning_no_preview": "⚠️ Unable to load model for preview. Make sure the file is a valid 3D model.",
        "convert_file_type": "Type: {type} | Extension: .{ext}",

        # --- ARTIFIX PROJECT (EN) ---
        "project_header": "🚀 ArtiFix Project",
        "project_text": """**ArtiFix** is a professional platform for repairing, converting, and viewing CAD/CAM files.
This project is constantly evolving. For information requests, collaborations, or technical assistance, contact us.""",
        "project_contact": "📧 Contact Us",
        "project_contact_text": "Send a request to info@artifix.it",
        "project_form_name": "Your name",
        "project_form_email": "Your email",
        "project_form_message": "Message",
        "project_form_submit": "Send",
        "project_success": "Email sent successfully!",
        "project_error": "Error: {error}",
        "project_warning": "Fill in all fields before sending.",

        # --- BECOME A SPONSOR (EN) ---
        "sponsor_header": "🤝 Become an ArtiFix Sponsor",
        "sponsor_intro": """**ArtiFix** is an independent project offering free tools for repairing, converting, and viewing CAD/CAM files.

Every day hundreds of professionals, students, and enthusiasts use ArtiFix services. If you also believe in this project and want to support it, you can become a **sponsor**.""",
        "sponsor_format_title": "📐 Required banner format",
        "sponsor_format_text": """- **Dimensions:** 300 × 100 px
- **File format:** PNG (preferred) or JPG
- **Background:** transparent or neutral
- **Maximum weight:** 200 KB
- **Content:** company logo + optional short tagline""",
        "sponsor_how_title": "💶 How it works",
        "sponsor_how_text": """1. Make a **liberal donation** via the PayPal button below.
2. Fill out the form with your brand details (name, website, email, logo).
3. Within 24-48h your banner is published in the ArtiFix sidebar for **30 days**.
4. At the end of the 30 days, if you wish to renew, you can donate again.""",
        "sponsor_donate_button": "💙 Donate with PayPal",
        "sponsor_form_title": "📤 Send your request",
        "sponsor_form_caption": "After making the donation, fill out this form with your brand details.",
        "sponsor_form_brand": "Brand/company name *",
        "sponsor_form_email": "Reference email *",
        "sponsor_form_site": "Website (full URL, e.g., https://www.mysite.com) *",
        "sponsor_form_logo": "GitHub Raw URL of the logo (e.g., https://raw.githubusercontent.com/.../logo.png) — 300×100 px, PNG or JPG, max 200 KB *",
        "sponsor_form_message": "Optional message (brief business description)",
        "sponsor_form_submit": "Send sponsor request",
        "sponsor_form_success": "✅ Request sent! We will contact you within 48h.",
        "sponsor_form_error": "Send error: {error}",
        "sponsor_form_warning": "Fill in all required fields (*).",
        "sponsor_form_info": "💡 After donating, send the request via this form. Your banner will be active within 24-48h.",

        # --- PRIVACY POLICY (EN) ---
        "privacy_header": "🔒 Privacy Policy",
        "privacy_subtitle": "**ArtiFix - Universal CAD/CAM File Repair**",
        "privacy_updated": "Last updated: September 15, 2026",
        "privacy_back": "← Back to Dashboard",
        "privacy_content": """This Privacy Policy is provided pursuant to Art. 13 of Regulation (EU) 2016/679 (GDPR), regarding the protection of natural persons with regard to the processing of personal data.

### 1. Data Controller
The Data Controller is **ArtiFix**, based in Italy. For any requests, you can contact the Controller at: **info@artifix.it**.

### 2. Data collected and purposes
**Data voluntarily provided by the user**: Through the "Contact Us" form, name, email address, and message are collected to respond to requests.
**Navigation data**: The site uses technical cookies (for operation) and analytics cookies (optional) as described in the Cookie Policy.
**Uploaded files**: Files uploaded by users for conversion are processed temporarily in memory on the server and are not stored after processing.

### 3. Data collected for Donations and Sponsorships
**Donor Data**: name, email, amount, date, payment method.
**Sponsor Data**: brand name, logo URL, website, reference email, phone (optional), start date, duration.
**Legal basis**: consent (Art. 6, par. 1, lett. a GDPR) + liberality (Art. 6, par. 1, lett. b GDPR).
**Retention**: 10 years for donations, 24 months for sponsorships.

### 4. Data subject rights
Pursuant to Arts. 15-22 of the GDPR, the user has the right to: access, rectification, erasure, restriction, objection, portability, withdrawal of consent.
To exercise these rights: **info@artifix.it**

### 5. Communication and dissemination
Data will not be transferred to third parties for marketing purposes or sold. They may be communicated to PayPal (payments), Google (storage), accountant (tax obligations), competent authorities.

### 6. Data transfer
Data is not transferred outside the European Union. The app is hosted on Streamlit Cloud (USA), but file processing occurs in memory.

### 7. Changes to the Privacy Policy
This Privacy Policy may be subject to updates. The updated version will always be available on this page.""",

        # --- COOKIE POLICY (EN) ---
        "cookie_policy_header": "🍪 Cookie Policy",
        "cookie_policy_subtitle": "**ArtiFix - Universal CAD/CAM File Repair**",
        "cookie_policy_updated": "Last updated: September 15, 2026",
        "cookie_policy_back": "← Back to Dashboard",
        "cookie_policy_content": """This Cookie Policy is provided pursuant to Art. 13 of Regulation (EU) 2016/679 (GDPR) and the Provision of the Italian Data Protection Authority of June 10, 2021.

### 1. Data Controller
The Data Controller is **ArtiFix**, based in Italy. For any requests, you can contact the Controller at: **info@artifix.it**.

### 2. What are Cookies
Cookies are small text files that websites send and record on the user's computer or mobile device, to be retransmitted to the same sites on subsequent visits. They are used to remember user actions and preferences.

### 3. Types of Cookies used
This site uses exclusively **Technical Cookies (or strictly necessary)**. These cookies are essential for the operation of the site and do not require prior consent from the user.

*   **Session Cookies**: Automatically deleted when the browser is closed.
*   **Functionality Cookies**: Allow remembering user choices (e.g., 5GB upload limit).

**Third-Party / Profiling Cookies**: This site **does not use** profiling, marketing, or third-party cookies.

### 4. Consent Management
On first access, the user can choose whether to accept or reject cookies via the appropriate banner.

### 5. How to disable Cookies via Browser
*   **Google Chrome**: [Instructions](https://support.google.com/chrome/answer/95647)
*   **Mozilla Firefox**: [Instructions](https://support.mozilla.org/kb/block-websites-storing-cookies)
*   **Microsoft Edge**: [Instructions](https://support.microsoft.com/microsoft-edge/delete-cookies-in-microsoft-edge)
*   **Safari**: [Instructions](https://support.apple.com/guide/safari/manage-cookies)

### 6. Data Subject Rights
Pursuant to Arts. 15-22 of the GDPR, the user has the right to access, rectification, erasure, restriction, objection, and portability of their personal data. To exercise these rights: **info@artifix.it**.

### 7. Updates
This Cookie Policy may be subject to updates.""",

        # --- FOOTER (EN) ---
        "footer": "© 2026 ArtiFix | All rights reserved",
    }
}

# Funzione helper per recuperare una traduzione
def get_text(key, lang="it", **kwargs):
    lang = lang if lang in TRANSLATIONS else "it"
    text = TRANSLATIONS[lang].get(key, key)
    if kwargs:
        try:
            text = text.format(**kwargs)
        except (KeyError, IndexError):
            pass
    return text

# Rilevamento lingua browser
def detect_browser_language():
    try:
        import streamlit as st
        browser_lang = st.context.headers.get('Accept-Language', 'it')
        if browser_lang:
            primary_lang = browser_lang.split(',')[0].split(';')[0].split('-')[0].lower()
            if primary_lang == 'en':
                return 'en'
        return 'it'
    except Exception:
        return 'it'

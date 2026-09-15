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
        "dash_supported_formats": "📁 Formati Supportati (50+ estensioni)",
        "dash_info_select": "👈 Seleziona una funzionalità dal menu.",
        
        # --- RIPARA FILE ---
        "repair_header": "🛠️ Centro Riparazione File",
        "repair_upload": "Seleziona un file",
        "repair_upload_hint": "💡 **Formati supportati:** DXF, STL, OBJ, PLY, GLB, GLTF, FBX, 3MF, DAE, WRL, OFF, U3D, IFC, SHP, GEOJSON, KML, GPX, SVG, **3D PDF** (con modello 3D incorporato **.u3d** o **.prc**), DOCX, XLSX. I formati proprietari (DWG, SKP, RVT, STEP, IGES) devono essere esportati in DAE o OBJ.",
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
        "repair_error_pdf_hint": "⚠️ **Attenzione:** i PDF standard (non 3D) non possono essere riparati, convertiti o visualizzati. Solo i **3D PDF** con modello 3D incorporato (**U3D** o **PRC**) possono essere visualizzati nel **Viewer 3D**.",
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
        "viewer_upload_hint": "💡 **Formati supportati:** STL, OBJ, PLY, GLB, GLTF, FBX, 3MF, DAE, WRL, OFF, U3D, **3D PDF** (il file PDF deve contenere un modello 3D incorporato in formato **.u3d** o **.prc**).",
        "viewer_status_loading": "Caricamento del modello... (30%)",
        "viewer_status_processing": "Elaborazione vertici e facce... (60%)",
        "viewer_status_building": "Costruzione della vista 3D... (100%)",
        "viewer_success": "✅ {vertices} vertici, {faces} facce",
        "viewer_error_processing": "❌ Errore nel processamento della mesh.",
        "viewer_warning_no_model": "⚠️ Impossibile caricare il modello.",
        "viewer_error_generic": "❌ Errore: {error}",
        "viewer_legend": "🔄 Trascina per ruotare | 🖱️ Tasto destro per spostare | 🖱️ Rotella per zoom",
        
        # --- 3D PDF DETECTION ---
        "pdf_no_3d_title": "❌ **Il PDF non contiene un modello 3D incorporato.**",
        "pdf_no_3d_desc": "Il file `{filename}` è un PDF standard, non un 3D PDF. Per visualizzarlo nel Viewer 3D, deve contenere un modello 3D in formato **U3D** o **PRC**.",
        "pdf_no_3d_howto_title": "📖 Come creare un 3D PDF",
        "pdf_no_3d_howto_steps": """1. Apri il tuo modello in un software CAD (AutoCAD, SketchUp, Revit, FreeCAD, ecc.)
2. Esporta il modello in formato **U3D** o **PRC** (formati 3D incorporabili)
3. Usa **Adobe Acrobat Pro** o **Foxit PhantomPDF** per creare un 3D PDF:
   - Apri un PDF vuoto
   - Vai su **Strumenti → 3D → Aggiungi 3D**
   - Seleziona il file U3D o PRC esportato
   - Salva il PDF
4. Carica il 3D PDF su ArtiFix per visualizzarlo""",
        "pdf_no_3d_alternative": "💡 **Alternativa più semplice:** carica direttamente il file **U3D** o **PRC** nel Viewer 3D (sono supportati nativamente, senza bisogno del PDF).",
        "pdf_3d_detected": "✅ **3D PDF rilevato!** Contiene un modello 3D incorporato. Elaborazione in corso...",
        
        # --- CONVERTI FORMATI ---
        "convert_header": "🔄 Conversione Formati Universale",
        "convert_subtitle": "Converti file tra **tutti i formati** supportati con **tutte le combinazioni** possibili.",
        "convert_expander_note": "ℹ️ Nota sui formati proprietari e a pagamento",
        "convert_note_text": """**ArtiFix non può leggere direttamente i formati proprietari e a pagamento** (come DWG, SKP, RVT, STEP, IGES, ecc.) perché richiedono librerie commerciali e server dedicati.

**Come risolvere?** Se il tuo file è in un formato proprietario, ti consigliamo di:
1. Aprire il file nel software con cui è stato creato (es. AutoCAD, SketchUp, Revit).
2. Utilizzare la funzione **"Esporta"** o **"Salva con nome"** per convertirlo in **DAE (Collada)** o **OBJ**.
3. Caricare il file DAE o OBJ su ArtiFix e convertirlo qui in qualsiasi altro formato mesh (STL, PLY, GLB, GLTF, ecc.) o 3D PDF.

*DAE (Collada) e OBJ sono formati universali e gratuiti che possono essere esportati dalla quasi totalità dei software CAD 3D presenti sul mercato.*""",
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
        "dash_supported_formats": "📁 Supported Formats (50+ extensions)",
        "dash_info_select": "👈 Select a feature from the menu.",
        
        # --- REPAIR FILE ---
        "repair_header": "🛠️ File Repair Center",
        "repair_upload": "Select a file",
        "repair_upload_hint": "💡 **Supported formats:** DXF, STL, OBJ, PLY, GLB, GLTF, FBX, 3MF, DAE, WRL, OFF, U3D, IFC, SHP, GEOJSON, KML, GPX, SVG, **3D PDF** (with embedded 3D model in **.u3d** or **.prc**), DOCX, XLSX. Proprietary formats (DWG, SKP, RVT, STEP, IGES) must be exported to DAE or OBJ.",
        "repair_status_analyzing": "Analyzing file... (30%)",
        "repair_status_verifying": "Verifying result... (60%)",
        "repair_status_completing": "Completing... (100%)",
        "repair_status_error": "Error during analysis",
        "repair_details": "Details",
        "repair_button_repair": "🔧 Repair",
        "repair_button_download": "📥 Download",
        "repair_success": "✅ Repaired!",

        # --- REPAIR ERRORS ---
        "repair_error_non_mesh_title": "❌ **Format not supported for repair.**",
        "repair_error_non_mesh_desc": "The file `{ext}` is a **{tipo}** file, not a 3D mesh.",
        "repair_error_non_mesh_hint": "To work with {tipo} files, use the **Format Conversion** or **3D Viewer** section.",
        "repair_error_pdf_hint": "⚠️ **Warning:** standard PDFs (non-3D) cannot be repaired, converted, or viewed. Only **3D PDFs** with an embedded 3D model (**U3D** or **PRC**) can be viewed in the **3D Viewer**.",
        "repair_error_invalid_mesh_title": "❌ **Cannot repair this file.**",
        "repair_error_invalid_mesh_desc": "The file `{ext}` does not contain a valid 3D mesh with vertices and faces.",
        "repair_error_invalid_mesh_hint": "Supported formats: **STL, OBJ, PLY, GLB, GLTF, FBX, 3MF, DAE, WRL, OFF, U3D**.",

        # --- NON-MESH FORMAT TYPES ---
        "type_svg": "2D vector graphics",
        "type_pdf": "PDF document",
        "type_docx": "Word document",
        "type_xlsx": "spreadsheet",
        "type_dxf": "2D CAD drawing",
        "type_dwg": "proprietary 2D CAD drawing",

        # --- REPAIR REPORT ---
        "report_header": "📊 Detailed Repair Report",
        "report_subtitle": "Complete analysis of the changes applied to the file.",
        "report_before": "Initial State (Before)",
        "report_

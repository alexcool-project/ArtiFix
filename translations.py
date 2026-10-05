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

        # --- DASHBOARD ---
        "dash_header": "📊 Dashboard",
        "dash_error_load": "⚠️ Impossibile caricare le metriche dal fogli Google. Mostro i valori di fallback.",
        "dash_metric_repaired": "File Riparati",
        "dash_metric_conversions": "Conversioni",
        "dash_metric_formats": "Formati Supportati",
        "dash_metric_online": "Stato Servizio",
        "dash_metric_uptime": "Uptime 30gg",
        "dash_metric_sponsors": "Sponsor Attivi",
        "dash_metric_last_update": "Ultimo Aggiornamento",
        "dash_metric_last_deploy": "Ultimo Deploy",
        "dash_supported_formats": "📁 Formati Supportati (50+ estensioni)",
        "dash_info_select": "👈 Seleziona una funzionalità dal menu.",
        "dashboard_title": "Dashboard",
        "dashboard_subtitle": "Convertitore CAD/CAM Universale",
        "dashboard_description": "ArtiFix è la piattaforma professionale per convertire file CAD/CAM in 3D PDF, STL, OBJ e altri formati.",
        "dashboard_metric_formats": "Formati supportati",
        "dashboard_metric_viewer": "Viewer 3D",
        "dashboard_metric_free": "Gratuito",

        # --- COOKIE BANNER ---
        "cookie_banner_title": "Cookie",
        "cookie_banner_text": "Questo sito utilizza cookie tecnici per migliorare l'esperienza utente. Nessun dato viene condiviso con terze parti.",
        "cookie_accept": "Accetta",

        # --- COOKIE POLICY POPUP (blocco grande) ---
        "cookie_title": "🍪 Cookie Policy",
        "cookie_text": "Noi e terze parti selezionate utilizziamo cookie o tecnologie simili per finalità tecniche e, con il tuo consenso, anche per altre finalità come specificato nella cookie policy. Il rifiuto del consenso può rendere non disponibili le relative funzioni. Usa il pulsante \"Accetta tutti i cookie\" per acconsentire. Usa il pulsante \"Accetta solo i cookie necessari\" per continuare senza accettare.",
        "cookie_check_privacy": "Consulta la Privacy Policy tramite il pulsante apposito",
        "cookie_accept_necessary": "Accetta solo i cookie necessari",
        "cookie_accept_all": "Accetta tutti i cookie",
        "cookie_content": "Questo sito utilizza esclusivamente cookie tecnici necessari al funzionamento. Non utilizziamo cookie di profilazione, marketing o di terze parti.",
        "cookie_policy_header": "🍪 Cookie Policy",
        "cookie_policy_subtitle": "**ArtiFix - Riparazione File CAD/CAM Universale**",
        "cookie_policy_updated": "Ultimo aggiornamento: 15 settembre 2026",
        "cookie_policy_back": "← Torna alla Dashboard",
        "cookie_policy_content": "La presente Cookie Policy è resa ai sensi dell'art. 13 del Regolamento (UE) 2016/679 (GDPR) e del Provvedimento del Garante per la Protezione dei Dati Personali del 10 giugno 2021. **Titolare del Trattamento**: ArtiFix, con sede in Italia (info@artifix.it). **Cookie utilizzati**: esclusivamente cookie tecnici (sessione e funzionalità). **Cookie di terze parti**: nessuno. **Come disabilitare i cookie**: tramite le impostazioni del browser (Chrome, Firefox, Edge, Safari). **Diritti dell'interessato**: ai sensi degli artt. 15-22 GDPR, puoi esercitare i tuoi diritti scrivendo a info@artifix.it.",

        # --- RIPARA FILE ---
        "repair_title": "🛠️ Centro Riparazione File",
        "repair_info": "Carica un file danneggiato o corrotto per tentare di ripararlo.",
        "repair_upload": "Seleziona un file da riparare",
        "repair_result": "Risultato",
        "repair_file_name": "Nome file",
        "repair_file_size": "Dimensione",

        # --- VIEWER 3D ---
        "viewer_title": "🖥️ Viewer 3D",
        "viewer_header": "🖥️ Viewer 3D",
        "viewer_upload": "Carica modello 3D",
        "viewer_upload_hint": "💡 Formati supportati: STL, OBJ, PLY, GLB, GLTF, FBX, 3MF, DAE, WRL, OFF, U3D, 3D PDF.",
        "viewer_loaded": "File caricato",
        "viewer_vertices": "Vertici",
        "viewer_faces": "Facce",
        "viewer_watertight": "Watertight",
        "viewer_error": "❌ Impossibile caricare il modello 3D.",
        "viewer_status_loading": "📖 Caricamento del modello...",
        "viewer_status_processing": "🔧 Elaborazione vertici e facce...",
        "viewer_status_building": "🎨 Costruzione della vista 3D...",
        "viewer_success": "✅ {vertices} vertici, {faces} facce",
        "viewer_error_processing": "❌ Errore nel processamento della mesh.",
        "viewer_warning_no_model": "⚠️ Impossibile caricare il modello.",
        "viewer_error_generic": "❌ Errore: {error}",
        "viewer_legend": "🔄 Trascina per ruotare | 🖱️ Tasto destro per spostare | 🖱️ Rotella per zoom",
        "viewer_legend_axes": "X (Rosso) | Y (Verde) | Z (Blu)",

        # --- 3D PDF DETECTION ---
        "pdf_no_3d_title": "❌ **Il PDF non contiene un modello 3D incorporato.**",
        "pdf_no_3d_desc": "Il file `{filename}` è un PDF standard, non un 3D PDF. Per visualizzarlo nel Viewer 3D, deve contenere un modello 3D in formato U3D.",
        "pdf_no_3d_howto_title": "📖 Come creare un 3D PDF",
        "pdf_no_3d_howto_steps": "1. Apri il modello in CAD\n2. Esporta in formato U3D\n3. Usa Adobe Acrobat Pro per creare il 3D PDF\n4. Carica il 3D PDF su ArtiFix",
        "pdf_no_3d_alternative": "💡 Alternativa: carica direttamente il file U3D nel Viewer 3D (supportato nativamente).",
        "pdf_3d_detected": "✅ **3D PDF rilevato!** Contiene un modello 3D incorporato. Elaborazione in corso...",

        # --- CONVERTI FORMATI ---
        "convert_title": "🔄 Conversione Formati",
        "convert_header": "🔄 Conversione Formati Universale",
        "convert_subtitle": "Converti file tra **tutti i formati** supportati.",
        "convert_description": "Converti file tra tutti i formati supportati.",
        "convert_expander_matrix": "📋 Matrice delle conversioni disponibili",
        "convert_caption_matrix": "✅ = Conversione supportata",
        "convert_upload": "Carica un file da convertire",
        "convert_upload_hint": "💡 Clicca per cercare il file sul tuo computer, oppure trascina e rilascia il file qui.",
        "convert_target": "Formato di destinazione",
        "convert_target_format": "Formato di destinazione",
        "convert_button": "🔄 Converti",
        "convert_button_convert": "🔄 Converti in {format}",
        "convert_converting": "Conversione in corso...",
        "convert_status_loading": "📖 Caricamento e analisi del modello...",
        "convert_status_converting": "🔄 Conversione in corso...",
        "convert_status_saving": "💾 Salvataggio del file...",
        "convert_success": "✅ Conversione in {format} completata!",
        "convert_info_ready": "📥 Il file è pronto! Clicca il pulsante qui sotto per scaricarlo.",
        "convert_button_download": "📥 Scarica .{format}",
        "convert_download": "📥 Scarica",
        "convert_error": "❌ Conversione in {format} fallita. Riprova con un altro formato.",
        "convert_error_load": "❌ Impossibile caricare il modello.",
        "convert_no_formats": "⚠️ Nessun formato di destinazione disponibile per questo file.",
        "convert_load_error": "❌ Impossibile caricare il modello.",
        "convert_warning_no_target": "⚠️ Nessun formato di destinazione disponibile per questo file.",
        "convert_warning_no_preview": "⚠️ Impossibile caricare il modello per l'anteprima.",
        "convert_button_preview": "🖥️ Mostra anteprima interattiva",
        "convert_info_preview": "💡 Ruota il modello a 360° con il mouse",
        "convert_file_type": "Tipo: {type} | Estensione: .{ext}",

        # --- HTML 3D VIEWER INFO ---
        "html_viewer_title": "🌐 Cos'è l'HTML 3D Viewer?",
        "html_viewer_intro": "L'<strong>HTML 3D Viewer</strong> è un file autonomo che mostra il tuo modello 3D in <strong>qualsiasi browser moderno</strong>, senza installazioni, senza account, senza Adobe.",
        "html_viewer_modes": "Puoi condividerlo in <strong>tre modi</strong>: <strong>link pubblico</strong> (con QR code), <strong>file scaricabile</strong> (.html), oppure <strong>screenshot professionale</strong>.",
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

        # --- NOTE FORMATI PROPRIETARI ---
        "notes_expander_title": "📝 Note: formati proprietari (DWG, SKP, RVT, STEP, IGES)",
        "notes_expander_intro": "ArtiFix supporta nativamente oltre 50 formati. **Alcuni formati proprietari non possono essere letti direttamente** perché richiedono librerie commerciali. Ecco come procedere:",
        "notes_expander_native": "**✅ Supportati nativamente:** STL, OBJ, PLY, GLB, GLTF, FBX, 3MF, DAE, WRL, OFF, U3D, DXF, 3D PDF, SVG, DOCX, XLSX, IFC, SHP, GeoJSON, KML, GPX.",
        "notes_expander_not_supported": "**❌ NON supportati direttamente:** DWG, SKP, RVT, STEP, IGES, DGN, DWT.",
        "notes_expander_howto": "**🔧 Come procedere per i formati non supportati:**",
        "notes_expander_steps": "1. **Apri il file** nel software originale\n2. **Esporta in DAE (Collada)** o **OBJ**\n3. **Carica il file DAE/OBJ** su ArtiFix",
        "notes_expander_tip": "💡 **Suggerimento:** quasi tutti i software CAD 3D possono esportare in DAE o OBJ con un click su **File → Esporta → DAE/OBJ**.",
        "notes_expander_guide_link": "📖 Leggi la guida completa: esportare DWG in DAE",

        # --- PROGETTO ---
        "project_title": "🚀 Progetto ArtiFix",
        "project_header": "🚀 Progetto ArtiFix",
        "project_description": "**ArtiFix** è una piattaforma professionale per la riparazione, conversione e visualizzazione di file CAD/CAM. Il progetto è in continua evoluzione.",
        "project_text": "**ArtiFix** è una piattaforma professionale per la riparazione, conversione e visualizzazione di file CAD/CAM. Questo progetto è in continua evoluzione. Per richieste di informazioni, collaborazioni o assistenza tecnica, contattaci.",
        "project_contact": "📧 Contattaci",
        "project_contact_text": "Invia una richiesta a info@artifix.it",
        "project_form_name": "Il tuo nome",
        "project_form_email": "La tua email",
        "project_form_message": "Messaggio",
        "project_form_submit": "Invia",
        "project_success": "Email inviata con successo!",
        "project_error": "Errore: {error}",
        "project_warning": "Compila tutti i campi prima di inviare.",
        "project_roadmap": "Roadmap",
        "project_support": "Sostieni il progetto",

        # --- SPONSOR ---
        "sponsor_title": "🤝 Diventa Sponsor di ArtiFix",
        "sponsor_header": "🤝 Diventa Sponsor di ArtiFix",
        "sponsor_description": "Sostieni ArtiFix e ottieni visibilità sulla piattaforma.",
        "sponsor_intro": "**ArtiFix** è un progetto indipendente che offre strumenti gratuiti per la riparazione, conversione e visualizzazione di file CAD/CAM. Ogni giorno centinaia di professionisti, studenti e appassionati utilizzano i servizi di ArtiFix. Se anche tu credi in questo progetto e vuoi sostenerlo, puoi diventare **sponsor**.",
        "sponsor_current": "Sponsor attuali",
        "sponsor_no_sponsors": "Nessuno sponsor al momento. Sii il primo!",
        "sponsor_howto": "Come diventare sponsor",
        "sponsor_howto_text": "Effettua una donazione PayPal e compila il form via email. Il tuo logo sarà visibile entro 24-48h.",
        "sponsor_contact": "Contatta per sponsorizzazione",
        "sponsor_donate": "💙 Dona con PayPal",
        "sponsor_format_title": "📐 Formato banner richiesto",
        "sponsor_format_text": "- **Dimensioni:** 300 × 100 px\n- **Formato file:** PNG (preferito) o JPG\n- **Sfondo:** trasparente o neutro\n- **Peso massimo:** 200 KB",
        "sponsor_how_title": "💶 Come funziona",
        "sponsor_how_text": "1. Effettui una **donazione liberale** tramite PayPal.\n2. Compili il form con i dati del tuo brand.\n3. Entro 24-48h il tuo banner viene pubblicato per **30 giorni**.\n4. Al termine, se desideri rinnovare, puoi donare nuovamente.",
        "sponsor_donate_button": "💙 Dona con PayPal",
        "sponsor_form_title": "📤 Invia la tua richiesta",
        "sponsor_form_caption": "Dopo aver effettuato la donazione, compila questo form.",
        "sponsor_form_brand": "Nome brand/azienda *",
        "sponsor_form_email": "Email di riferimento *",
        "sponsor_form_site": "Sito web (URL completo) *",
        "sponsor_form_logo": "URL Raw di GitHub del logo (300×100 px, PNG o JPG, max 200 KB) *",
        "sponsor_form_message": "Messaggio opzionale",
        "sponsor_form_submit": "Invia richiesta sponsor",
        "sponsor_form_success": "✅ Richiesta inviata! Ti contatteremo entro 48h.",
        "sponsor_form_error": "Errore invio: {error}",
        "sponsor_form_warning": "Compila tutti i campi obbligatori (*).",
        "sponsor_form_info": "💡 Dopo la donazione, invia la richiesta tramite questo form. Il tuo banner sarà attivo entro 24-48h.",

        # --- PRIVACY POLICY ---
        "privacy_title": "🔒 Privacy Policy",
        "privacy_header": "🔒 Privacy Policy",
        "privacy_subtitle": "**ArtiFix - Riparazione File CAD/CAM Universale**",
        "privacy_updated": "Ultimo aggiornamento: 15 settembre 2026",
        "privacy_back": "← Torna alla Dashboard",
        "privacy_content": "La presente Privacy Policy è resa ai sensi dell'Art. 13 del Regolamento (UE) 2016/679 (GDPR). **Titolare del Trattamento**: ArtiFix, con sede in Italia (info@artifix.it). **Dati raccolti**: nome, email, messaggio (form contatti). **Dati donazioni/sponsor**: nome, email, importo, metodo di pagamento (conservazione 10 anni). **File caricati**: elaborati in memoria, mai conservati. **Diritti dell'interessato**: accesso, rettifica, cancellazione, limitazione, opposizione, portabilità (info@artifix.it).",

        # --- FOOTER ---
        "footer": "© 2026 ArtiFix | Tutti i diritti riservati",
        "back_to_home": "Torna alla Dashboard",
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

        # --- DASHBOARD ---
        "dash_header": "📊 Dashboard",
        "dash_error_load": "⚠️ Unable to load metrics from Google Sheets. Showing fallback values.",
        "dash_metric_repaired": "Repaired Files",
        "dash_metric_conversions": "Conversions",
        "dash_metric_formats": "Supported Formats",
        "dash_metric_online": "Service Status",
        "dash_metric_uptime": "30-day Uptime",
        "dash_metric_sponsors": "Active Sponsors",
        "dash_metric_last_update": "Last Update",
        "dash_metric_last_deploy": "Last Deploy",
        "dash_supported_formats": "📁 Supported Formats (50+ extensions)",
        "dash_info_select": "👈 Select a feature from the menu.",
        "dashboard_title": "Dashboard",
        "dashboard_subtitle": "Universal CAD/CAM Converter",
        "dashboard_description": "ArtiFix is the professional platform to convert CAD/CAM files to 3D PDF, STL, OBJ and other formats.",
        "dashboard_metric_formats": "Supported formats",
        "dashboard_metric_viewer": "3D Viewer",
        "dashboard_metric_free": "Free",

        # --- COOKIE BANNER ---
        "cookie_banner_title": "Cookies",
        "cookie_banner_text": "This site uses technical cookies to improve user experience. No data is shared with third parties.",
        "cookie_accept": "Accept",

        # --- COOKIE POLICY POPUP (big block) ---
        "cookie_title": "🍪 Cookie Policy",
        "cookie_text": "We and selected third parties use cookies or similar technologies for technical purposes and, with your consent, also for other purposes as specified in the cookie policy. Denying consent may make related features unavailable. Use the \"Accept all cookies\" button to consent. Use the \"Accept only necessary cookies\" button to continue without accepting.",
        "cookie_check_privacy": "View the Privacy Policy using the dedicated button",
        "cookie_accept_necessary": "Accept only necessary cookies",
        "cookie_accept_all": "Accept all cookies",
        "cookie_content": "This site uses exclusively technical cookies necessary for operation. We do not use profiling, marketing, or third-party cookies.",
        "cookie_policy_header": "🍪 Cookie Policy",
        "cookie_policy_subtitle": "**ArtiFix - Universal CAD/CAM File Repair**",
        "cookie_policy_updated": "Last updated: September 15, 2026",
        "cookie_policy_back": "← Back to Dashboard",
        "cookie_policy_content": "This Cookie Policy is provided pursuant to Art. 13 of Regulation (EU) 2016/679 (GDPR) and the Provision of the Italian Data Protection Authority of June 10, 2021. **Data Controller**: ArtiFix, based in Italy (info@artifix.it). **Cookies used**: technical cookies only (session and functionality). **Third-party cookies**: none. **How to disable cookies**: via browser settings (Chrome, Firefox, Edge, Safari). **Data subject rights**: pursuant to Arts. 15-22 GDPR, you can exercise your rights by writing to info@artifix.it.",

        # --- REPAIR ---
        "repair_title": "🛠️ File Repair Center",
        "repair_info": "Upload a damaged or corrupted file to attempt repair.",
        "repair_upload": "Select a file to repair",
        "repair_result": "Result",
        "repair_file_name": "File name",
        "repair_file_size": "Size",

        # --- 3D VIEWER ---
        "viewer_title": "🖥️ 3D Viewer",
        "viewer_header": "🖥️ 3D Viewer",
        "viewer_upload": "Upload 3D model",
        "viewer_upload_hint": "💡 Supported formats: STL, OBJ, PLY, GLB, GLTF, FBX, 3MF, DAE, WRL, OFF, U3D, 3D PDF.",
        "viewer_loaded": "File loaded",
        "viewer_vertices": "Vertices",
        "viewer_faces": "Faces",
        "viewer_watertight": "Watertight",
        "viewer_error": "❌ Unable to load the 3D model.",
        "viewer_status_loading": "📖 Loading model...",
        "viewer_status_processing": "🔧 Processing vertices and faces...",
        "viewer_status_building": "🎨 Building 3D view...",
        "viewer_success": "✅ {vertices} vertices, {faces} faces",
        "viewer_error_processing": "❌ Error processing mesh.",
        "viewer_warning_no_model": "⚠️ Unable to load model.",
        "viewer_error_generic": "❌ Error: {error}",
        "viewer_legend": "🔄 Drag to rotate | 🖱️ Right click to pan | 🖱️ Scroll to zoom",
        "viewer_legend_axes": "X (Red) | Y (Green) | Z (Blue)",

        # --- 3D PDF DETECTION ---
        "pdf_no_3d_title": "❌ **The PDF does not contain an embedded 3D model.**",
        "pdf_no_3d_desc": "The file `{filename}` is a standard PDF, not a 3D PDF. To view it in the 3D Viewer, it must contain a 3D model in U3D format.",
        "pdf_no_3d_howto_title": "📖 How to create a 3D PDF",
        "pdf_no_3d_howto_steps": "1. Open the model in CAD\n2. Export to U3D format\n3. Use Adobe Acrobat Pro to create the 3D PDF\n4. Upload the 3D PDF to ArtiFix",
        "pdf_no_3d_alternative": "💡 Alternative: upload the U3D file directly to the 3D Viewer (natively supported).",
        "pdf_3d_detected": "✅ **3D PDF detected!** It contains an embedded 3D model. Processing...",

        # --- CONVERT ---
        "convert_title": "🔄 Format Conversion",
        "convert_header": "🔄 Universal Format Conversion",
        "convert_subtitle": "Convert files between **all supported formats**.",
        "convert_description": "Convert files between all supported formats.",
        "convert_expander_matrix": "📋 Available conversion matrix",
        "convert_caption_matrix": "✅ = Supported conversion",
        "convert_upload": "Upload a file to convert",
        "convert_upload_hint": "💡 Click to browse for the file on your computer, or drag and drop the file here.",
        "convert_target": "Target format",
        "convert_target_format": "Target format",
        "convert_button": "🔄 Convert",
        "convert_button_convert": "🔄 Convert to {format}",
        "convert_converting": "Converting...",
        "convert_status_loading": "📖 Loading and analyzing model...",
        "convert_status_converting": "🔄 Converting...",
        "convert_status_saving": "💾 Saving file...",
        "convert_success": "✅ Conversion to {format} completed!",
        "convert_info_ready": "📥 The file is ready! Click the button below to download it.",
        "convert_button_download": "📥 Download .{format}",
        "convert_download": "📥 Download",
        "convert_error": "❌ Conversion to {format} failed. Try another format.",
        "convert_error_load": "❌ Unable to load model.",
        "convert_no_formats": "⚠️ No target format available for this file.",
        "convert_load_error": "❌ Unable to load the model.",
        "convert_warning_no_target": "⚠️ No target format available for this file.",
        "convert_warning_no_preview": "⚠️ Unable to load model for preview.",
        "convert_button_preview": "🖥️ Show interactive preview",
        "convert_info_preview": "💡 Rotate the model 360° with the mouse",
        "convert_file_type": "Type: {type} | Extension: .{ext}",

        # --- HTML 3D VIEWER INFO ---
        "html_viewer_title": "🌐 What is the HTML 3D Viewer?",
        "html_viewer_intro": "The <strong>HTML 3D Viewer</strong> is a standalone file that shows your 3D model in <strong>any modern browser</strong>, without installations, without accounts, without Adobe.",
        "html_viewer_modes": "You can share it in <strong>three ways</strong>: <strong>public link</strong> (with QR code), <strong>downloadable file</strong> (.html), or <strong>professional screenshot</strong>.",
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

        # --- PROPRIETARY FORMATS ---
        "notes_expander_title": "📝 Note: proprietary formats (DWG, SKP, RVT, STEP, IGES)",
        "notes_expander_intro": "ArtiFix natively supports 50+ formats. **Some proprietary formats cannot be read directly** because they require commercial libraries. Here's how to proceed:",
        "notes_expander_native": "**✅ Natively supported:** STL, OBJ, PLY, GLB, GLTF, FBX, 3MF, DAE, WRL, OFF, U3D, DXF, 3D PDF, SVG, DOCX, XLSX, IFC, SHP, GeoJSON, KML, GPX.",
        "notes_expander_not_supported": "**❌ NOT directly supported:** DWG, SKP, RVT, STEP, IGES, DGN, DWT.",
        "notes_expander_howto": "**🔧 How to proceed for unsupported formats:**",
        "notes_expander_steps": "1. **Open the file** in the original software\n2. **Export to DAE (Collada)** or **OBJ**\n3. **Upload the DAE/OBJ file** to ArtiFix",
        "notes_expander_tip": "💡 **Tip:** almost all 3D CAD software can export to DAE or OBJ with a click on **File → Export → DAE/OBJ**.",
        "notes_expander_guide_link": "📖 Read the full guide: export DWG to DAE",

        # --- PROJECT ---
        "project_title": "🚀 ArtiFix Project",
        "project_header": "🚀 ArtiFix Project",
        "project_description": "**ArtiFix** is a professional platform for repairing, converting, and viewing CAD/CAM files. The project is constantly evolving.",
        "project_text": "**ArtiFix** is a professional platform for repairing, converting, and viewing CAD/CAM files. This project is constantly evolving. For information requests, collaborations, or technical assistance, contact us.",
        "project_contact": "📧 Contact Us",
        "project_contact_text": "Send a request to info@artifix.it",
        "project_form_name": "Your name",
        "project_form_email": "Your email",
        "project_form_message": "Message",
        "project_form_submit": "Send",
        "project_success": "Email sent successfully!",
        "project_error": "Error: {error}",
        "project_warning": "Fill in all fields before sending.",
        "project_roadmap": "Roadmap",
        "project_support": "Support the project",

        # --- SPONSOR ---
        "sponsor_title": "🤝 Become an ArtiFix Sponsor",
        "sponsor_header": "🤝 Become an ArtiFix Sponsor",
        "sponsor_description": "Support ArtiFix and gain visibility on the platform.",
        "sponsor_intro": "**ArtiFix** is an independent project offering free tools for repairing, converting, and viewing CAD/CAM files. Every day hundreds of professionals, students, and enthusiasts use ArtiFix services. If you also believe in this project and want to support it, you can become a **sponsor**.",
        "sponsor_current": "Current sponsors",
        "sponsor_no_sponsors": "No sponsors at the moment. Be the first!",
        "sponsor_howto": "How to become a sponsor",
        "sponsor_howto_text": "Make a PayPal donation and fill out the form via email. Your logo will be visible within 24-48h.",
        "sponsor_contact": "Contact for sponsorship",
        "sponsor_donate": "💙 Donate with PayPal",
        "sponsor_format_title": "📐 Required banner format",
        "sponsor_format_text": "- **Dimensions:** 300 × 100 px\n- **File format:** PNG (preferred) or JPG\n- **Background:** transparent or neutral\n- **Maximum weight:** 200 KB",
        "sponsor_how_title": "💶 How it works",
        "sponsor_how_text": "1. Make a **liberal donation** via PayPal.\n2. Fill out the form with your brand details.\n3. Within 24-48h your banner is published for **30 days**.\n4. At the end, if you wish to renew, you can donate again.",
        "sponsor_donate_button": "💙 Donate with PayPal",
        "sponsor_form_title": "📤 Send your request",
        "sponsor_form_caption": "After making the donation, fill out this form.",
        "sponsor_form_brand": "Brand/company name *",
        "sponsor_form_email": "Reference email *",
        "sponsor_form_site": "Website (full URL) *",
        "sponsor_form_logo": "GitHub Raw URL of the logo (300×100 px, PNG or JPG, max 200 KB) *",
        "sponsor_form_message": "Optional message",
        "sponsor_form_submit": "Send sponsor request",
        "sponsor_form_success": "✅ Request sent! We will contact you within 48h.",
        "sponsor_form_error": "Send error: {error}",
        "sponsor_form_warning": "Fill in all required fields (*).",
        "sponsor_form_info": "💡 After donating, send the request via this form. Your banner will be active within 24-48h.",

        # --- PRIVACY POLICY ---
        "privacy_title": "🔒 Privacy Policy",
        "privacy_header": "🔒 Privacy Policy",
        "privacy_subtitle": "**ArtiFix - Universal CAD/CAM File Repair**",
        "privacy_updated": "Last updated: September 15, 2026",
        "privacy_back": "← Back to Dashboard",
        "privacy_content": "This Privacy Policy is provided pursuant to Art. 13 of Regulation (EU) 2016/679 (GDPR). **Data Controller**: ArtiFix, based in Italy (info@artifix.it). **Data collected**: name, email, message (contact form). **Donation/sponsor data**: name, email, amount, payment method (retention 10 years). **Uploaded files**: processed in memory, never stored. **Data subject rights**: access, rectification, erasure, restriction, objection, portability (info@artifix.it).",

        # --- FOOTER ---
        "footer": "© 2026 ArtiFix | All rights reserved",
        "back_to_home": "Back to Dashboard",
    }
}


def get_text(key, lang="it", **kwargs):
    lang = lang if lang in TRANSLATIONS else "it"
    text = TRANSLATIONS[lang].get(key, key)
    if kwargs:
        try:
            text = text.format(**kwargs)
        except (KeyError, IndexError):
            pass
    return text


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

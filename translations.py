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

        # --- DASHBOARD (dinamica) ---
        "dash_header": "📊 Dashboard",
        "dash_error_load": "⚠️ Impossibile caricare le metriche dal foglio Google. Mostro i valori di fallback.",
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

        # --- COOKIE BANNER (semplice) ---
        "cookie_banner_title": "Cookie",
        "cookie_banner_text": "Questo sito utilizza cookie tecnici per migliorare l'esperienza utente. Nessun dato viene condiviso con terze parti.",
        "cookie_accept": "Accetta",

        # --- RIPARA FILE ---
        "repair_title": "🛠️ Centro Riparazione File",
        "repair_info": "Carica un file danneggiato o corrotto per tentare di ripararlo.",
        "repair_upload": "Seleziona un file da riparare",
        "repair_result": "Risultato",
        "repair_file_name": "Nome file",
        "repair_file_size": "Dimensione",

        # --- VIEWER 3D ---
        "viewer_title": "🖥️ Viewer 3D",
        "viewer_upload": "Carica modello 3D",
        "viewer_loaded": "File caricato",
        "viewer_vertices": "Vertici",
        "viewer_faces": "Facce",
        "viewer_watertight": "Watertight",
        "viewer_error": "❌ Impossibile caricare il modello 3D.",

        # --- CONVERTI FORMATI ---
        "convert_title": "🔄 Conversione Formati",
        "convert_description": "Converti file tra tutti i formati supportati.",
        "convert_upload": "Carica un file da convertire",
        "convert_target": "Formato di destinazione",
        "convert_button": "🔄 Converti",
        "convert_converting": "Conversione in corso...",
        "convert_success": "✅ Conversione completata!",
        "convert_download": "📥 Scarica",
        "convert_error": "❌ Conversione fallita. Riprova con un altro formato.",
        "convert_no_formats": "⚠️ Nessun formato di destinazione disponibile per questo file.",
        "convert_load_error": "❌ Impossibile caricare il modello.",

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
        "project_description": "**ArtiFix** è una piattaforma professionale per la riparazione, conversione e visualizzazione di file CAD/CAM. Il progetto è in continua evoluzione.",
        "project_roadmap": "Roadmap",
        "project_support": "Sostieni il progetto",

        # --- SPONSOR ---
        "sponsor_title": "🤝 Diventa Sponsor di ArtiFix",
        "sponsor_description": "Sostieni ArtiFix e ottieni visibilità sulla piattaforma.",
        "sponsor_current": "Sponsor attuali",
        "sponsor_no_sponsors": "Nessuno sponsor al momento. Sii il primo!",
        "sponsor_howto": "Come diventare sponsor",
        "sponsor_howto_text": "Effettua una donazione PayPal e compila il form via email. Il tuo logo sarà visibile entro 24-48h.",
        "sponsor_contact": "Contatta per sponsorizzazione",
        "sponsor_donate": "💙 Dona con PayPal",

        # --- PRIVACY / COOKIE ---
        "privacy_title": "🔒 Privacy Policy",
        "privacy_content": "La presente Privacy Policy è resa ai sensi dell'Art. 13 del Regolamento (UE) 2016/679 (GDPR). Titolare del trattamento: **ArtiFix** (info@artifix.it). I file caricati vengono elaborati temporaneamente in memoria e non vengono conservati.",
        "cookie_title": "🍪 Cookie Policy",
        "cookie_content": "Questo sito utilizza esclusivamente cookie tecnici necessari al funzionamento. Non utilizziamo cookie di profilazione, marketing o di terze parti.",
        "back_to_home": "Torna alla Dashboard",

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

        # --- DASHBOARD (dynamic) ---
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

        # --- COOKIE BANNER (simple) ---
        "cookie_banner_title": "Cookies",
        "cookie_banner_text": "This site uses technical cookies to improve user experience. No data is shared with third parties.",
        "cookie_accept": "Accept",

        # --- REPAIR ---
        "repair_title": "🛠️ File Repair Center",
        "repair_info": "Upload a damaged or corrupted file to attempt repair.",
        "repair_upload": "Select a file to repair",
        "repair_result": "Result",
        "repair_file_name": "File name",
        "repair_file_size": "Size",

        # --- 3D VIEWER ---
        "viewer_title": "🖥️ 3D Viewer",
        "viewer_upload": "Upload 3D model",
        "viewer_loaded": "File loaded",
        "viewer_vertices": "Vertices",
        "viewer_faces": "Faces",
        "viewer_watertight": "Watertight",
        "viewer_error": "❌ Unable to load the 3D model.",

        # --- CONVERT ---
        "convert_title": "🔄 Format Conversion",
        "convert_description": "Convert files between all supported formats.",
        "convert_upload": "Upload a file to convert",
        "convert_target": "Target format",
        "convert_button": "🔄 Convert",
        "convert_converting": "Converting...",
        "convert_success": "✅ Conversion completed!",
        "convert_download": "📥 Download",
        "convert_error": "❌ Conversion failed. Try another format.",
        "convert_no_formats": "⚠️ No target format available for this file.",
        "convert_load_error": "❌ Unable to load the model.",

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
        "project_description": "**ArtiFix** is a professional platform for repairing, converting, and viewing CAD/CAM files. The project is constantly evolving.",
        "project_roadmap": "Roadmap",
        "project_support": "Support the project",

        # --- SPONSOR ---
        "sponsor_title": "🤝 Become an ArtiFix Sponsor",
        "sponsor_description": "Support ArtiFix and gain visibility on the platform.",
        "sponsor_current": "Current sponsors",
        "sponsor_no_sponsors": "No sponsors at the moment. Be the first!",
        "sponsor_howto": "How to become a sponsor",
        "sponsor_howto_text": "Make a PayPal donation and fill out the form via email. Your logo will be visible within 24-48h.",
        "sponsor_contact": "Contact for sponsorship",
        "sponsor_donate": "💙 Donate with PayPal",

        # --- PRIVACY / COOKIE ---
        "privacy_title": "🔒 Privacy Policy",
        "privacy_content": "This Privacy Policy is provided pursuant to Art. 13 of Regulation (EU) 2016/679 (GDPR). Data Controller: **ArtiFix** (info@artifix.it). Uploaded files are processed temporarily in memory and are not stored.",
        "cookie_title": "🍪 Cookie Policy",
        "cookie_content": "This site uses exclusively technical cookies necessary for operation. We do not use profiling, marketing, or third-party cookies.",
        "back_to_home": "Back to Dashboard",

        # --- FOOTER ---
        "footer": "© 2026 ArtiFix | All rights reserved",
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

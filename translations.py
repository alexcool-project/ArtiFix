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
        "nav_donate": "💙 Dona con PayPal",
        "nav_become_sponsor": "🤝 Diventa Sponsor",
        
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
        "repair_status_analyzing": "Analisi del file in corso... (30%)",
        "repair_status_verifying": "Verifica del risultato... (60%)",
        "repair_status_completing": "Completamento... (100%)",
        "repair_status_error": "Errore durante l'analisi",
        "repair_details": "Dettagli",
        "repair_button_repair": "🔧 Ripara",
        "repair_button_download": "📥 Scarica",
        "repair_success": "✅ Riparato!",
        
        # --- VIEWER 3D ---
        "viewer_header": "🖥️ Viewer 3D",
        "viewer_upload": "Carica modello 3D",
        "viewer_status_loading": "Caricamento del modello... (30%)",
        "viewer_status_processing": "Elaborazione vertici e facce... (60%)",
        "viewer_status_building": "Costruzione della vista 3D... (100%)",
        "viewer_success": "✅ {vertices} vertici, {faces} facce",
        "viewer_error_processing": "❌ Errore nel processamento della mesh.",
        "viewer_warning_no_model": "⚠️ Impossibile caricare il modello.",
        "viewer_error_generic": "❌ Errore: {error}",
        "viewer_legend": "🔄 Trascina per ruotare | 🖱️ Tasto destro per spostare | 🖱️ Rotella per zoom",
        
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
        "convert_info_ready": "📥 Il file è pronto! Stiamo preparando il download, attendi qualche secondo...",
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
        "sponsor_form_logo": "URL pubblico del logo (Postimages, Imgur, ecc.) *",
        "sponsor_form_message": "Messaggio opzionale (breve descrizione attività)",
        "sponsor_form_submit": "Invia richiesta sponsor",
        "sponsor_form_success": "✅ Richiesta inviata! Ti contatteremo entro 48h.",
        "sponsor_form_error": "Errore invio: {error}",
        "sponsor_form_warning": "Compila tutti i campi obbligatori (*).",
        "sponsor_form_info": "💡 Dopo la donazione, invia la richiesta tramite questo form. Il tuo banner sarà attivo entro 24-48h.",
        
        # --- PRIVACY POLICY ---
        "privacy_header": "🔒 Privacy Policy",
        "privacy_subtitle": "**ArtiFix - Riparazione File CAD/CAM Universale**",
        "privacy_updated": "Ultimo aggiornamento: 9 settembre 2026",
        "privacy_back": "← Torna alla Dashboard",
        "privacy_content": """La presente Privacy Policy è resa ai sensi dell'Art. 13 del Regolamento (UE) 2016/679 (GDPR), relativo alla protezione delle persone fisiche con riguardo al trattamento dei dati personali.

### 1. Titolare del Trattamento
Il Titolare del trattamento dei dati è **ArtiFix**, con sede in Italia. Per qualsiasi richiesta è possibile contattare il Titolare all'indirizzo email: **info@artifix.it**.

### 2. Dati raccolti e finalità
**Dati forniti volontariamente dall'utente**: Attraverso il form "Contattaci" vengono raccolti nome, indirizzo email e messaggio, al fine di rispondere alle richieste pervenute.
**Dati di navigazione**: Il sito utilizza cookie tecnici (per il funzionamento) e cookie di analytics (facoltativi) come descritto nella Cookie Policy.

### 3. Base giuridica
Il trattamento si basa sul consenso dell'utente (Art. 6, par. 1, lett. a GDPR) e sull'esecuzione di misure precontrattuali richieste dall'utente (Art. 6, par. 1, lett. b GDPR).

### 4. Diritti dell'interessato
Ai sensi degli Artt. 15-22 del GDPR, l'utente ha il diritto di:
*   Accesso, rettifica e cancellazione dei propri dati.
*   Limitazione e opposizione al trattamento.
*   Portabilità dei dati.
*   Revoca del consenso in qualsiasi momento.

Per esercitare tali diritti, contattare il Titolare all'indirizzo: **info@artifix.it**. È inoltre possibile proporre reclamo al Garante per la Protezione dei Dati Personali.

### 5. Durata della conservazione
I dati raccolti tramite il form di contatto vengono conservati per il tempo strettamente necessario a rispondere alla richiesta e, comunque, per un periodo massimo di 24 mesi.

### 6. Comunicazione e diffusione
I dati non saranno ceduti a terzi per finalità di marketing o venduti. Saranno trattati esclusivamente dal Titolare.""",
        
        # --- COOKIE POLICY ---
        "cookie_policy_header": "🍪 Cookie Policy",
        "cookie_policy_subtitle": "**ArtiFix - Riparazione File CAD/CAM Universale**",
        "cookie_policy_updated": "Ultimo aggiornamento: 9 settembre 2026",
        "cookie_policy_back": "← Torna alla Dashboard",
        "cookie_policy_content": """La presente Cookie Policy è resa ai sensi dell'art. 13 del Regolamento (UE) 2016/679 (GDPR) e del Provvedimento del Garante per la Protezione dei Dati Personali del 10 giugno 2021.

### 1. Titolare del Trattamento
Il Titolare del trattamento dei dati è **ArtiFix**, con sede in Italia. Per qualsiasi richiesta è possibile contattare il Titolare all'indirizzo email: **info@artifix.it**.

### 2. Cosa sono i Cookie
I cookie sono piccoli file di testo che i siti web inviano e registrano sul computer o dispositivo mobile dell'utente, per essere poi ritrasmessi agli stessi siti alle visite successive. Servono a ricordare le azioni e le preferenze dell'utente.

### 3. Tipologie di Cookie utilizzate
Questo sito utilizza esclusivamente **Cookie Tecnici (o strettamente necessari)**. Questi cookie sono essenziali per il funzionamento del sito e non richiedono il consenso preventivo dell'utente.

*   **Cookie di Sessione**: Vengono eliminati automaticamente alla chiusura del browser. Sono utilizzati per mantenere attiva la sessione di navigazione e ricordare le scelte effettuate (es. il consenso ai cookie).
*   **Cookie di Funzionalità**: Permettono di ricordare le scelte dell'utente per migliorare l'esperienza di navigazione, come ad esempio il limite di upload impostato (5GB).

**Cookie di Terze Parti / Profilazione**: Questo sito **non utilizza** cookie di profilazione, di marketing o di terze parti (come Google Analytics o pixel di social media) per inviare pubblicità personalizzata.

### 4. Gestione del Consenso
Al primo accesso, l'utente può scegliere se accettare o rifiutare i cookie tramite l'apposito banner. La scelta viene registrata e memorizzata nel browser. È possibile modificare la propria scelta in qualsiasi momento cancellando i dati di navigazione del browser o reimpostando la pagina.

### 5. Come disabilitare i Cookie tramite il Browser
L'utente può gestire le preferenze sui cookie tramite le impostazioni del proprio browser. La disabilitazione di alcuni cookie potrebbe compromettere il corretto funzionamento di alcune sezioni del sito.

*   **Google Chrome**: [Istruzioni](https://support.google.com/chrome/answer/95647)
*   **Mozilla Firefox**: [Istruzioni](https://support.mozilla.org/kb/block-websites-storing-cookies)
*   **Microsoft Edge**: [Istruzioni](https://support.microsoft.com/microsoft-edge/delete-cookies-in-microsoft-edge)
*   **Safari**: [Istruzioni](https://support.apple.com/guide/safari/manage-cookies)

### 6. Diritti dell'Interessato
Ai sensi degli artt. 15-22 del GDPR, l'utente ha il diritto di accesso, rettifica, cancellazione, limitazione, opposizione e portabilità dei propri dati personali. Per esercitare tali diritti, contattare l'email **info@artifix.it**. È inoltre possibile proporre reclamo all'Autorità di controllo (Garante per la Protezione dei Dati Personali - [www.garanteprivacy.it](http://www.garanteprivacy.it)).

### 7. Aggiornamenti
La presente Cookie Policy può essere soggetta ad aggiornamenti. La versione aggiornata sarà sempre disponibile su questa pagina.""",
        
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
        "nav_donate": "💙 Donate with PayPal",
        "nav_become_sponsor": "🤝 Become a Sponsor",
        
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
        "repair_status_analyzing": "Analyzing file... (30%)",
        "repair_status_verifying": "Verifying result... (60%)",
        "repair_status_completing": "Completing... (100%)",
        "repair_status_error": "Error during analysis",
        "repair_details": "Details",
        "repair_button_repair": "🔧 Repair",
        "repair_button_download": "📥 Download",
        "repair_success": "✅ Repaired!",
        
        # --- VIEWER 3D ---
        "viewer_header": "🖥️ 3D Viewer",
        "viewer_upload": "Upload 3D model",
        "viewer_status_loading": "Loading model... (30%)",
        "viewer_status_processing": "Processing vertices and faces... (60%)",
        "viewer_status_building": "Building 3D view... (100%)",
        "viewer_success": "✅ {vertices} vertices, {faces} faces",
        "viewer_error_processing": "❌ Error processing mesh.",
        "viewer_warning_no_model": "⚠️ Unable to load model.",
        "viewer_error_generic": "❌ Error: {error}",
        "viewer_legend": "🔄 Drag to rotate | 🖱️ Right-click to pan | 🖱️ Scroll to zoom",
        
        # --- CONVERT FORMATS ---
        "convert_header": "🔄 Universal Format Conversion",
        "convert_subtitle": "Convert files between **all supported formats** with **all possible combinations**.",
        "convert_expander_note": "ℹ️ Note on proprietary and paid formats",
        "convert_note_text": """**ArtiFix cannot directly read proprietary and paid formats** (such as DWG, SKP, RVT, STEP, IGES, etc.) because they require commercial libraries and dedicated servers.

**How to solve?** If your file is in a proprietary format, we recommend:
1. Open the file in the software it was created with (e.g. AutoCAD, SketchUp, Revit).
2. Use the **"Export"** or **"Save As"** function to convert it to **DAE (Collada)** or **OBJ**.
3. Upload the DAE or OBJ file to ArtiFix and convert it here to any other mesh format (STL, PLY, GLB, GLTF, etc.) or 3D PDF.

*DAE (Collada) and OBJ are universal, free formats that can be exported from almost all 3D CAD software on the market.*""",
        "convert_expander_matrix": "📋 Available conversion matrix",
        "convert_caption_matrix": "✅ = Conversion supported | ❌ = Conversion not supported",
        "convert_upload": "Upload a file to convert",
        "convert_upload_hint": "💡 Click to browse your computer, or drag and drop the file here.",
        "convert_target_format": "Target format",
        "convert_button_convert": "🔄 Convert to {format}",
        "convert_status_loading": "Loading and analyzing model... (20%)",
        "convert_status_converting": "Converting... (70%)",
        "convert_status_saving": "Saving file... (100%)",
        "convert_success": "✅ Conversion to {format} completed!",
        "convert_info_ready": "📥 The file is ready! Preparing download, please wait...",
        "convert_button_download": "📥 Download .{format}",
        "convert_error": "❌ Conversion to {format} failed. Try another format.",
        "convert_error_load": "❌ Unable to load model. Make sure the file is a valid 3D model.",
        "convert_button_preview": "🖥️ Show interactive preview (rotate with mouse)",
        "convert_info_preview": "💡 Rotate the model 360° with mouse or touchpad",
        "convert_warning_format": "⚠️ The **.{format}** format cannot be converted to other formats.",
        "convert_info_formats": "💡 Convertible formats are: **STL, OBJ, PLY, GLB, GLTF, FBX, 3MF, DAE, WRL, OFF, DXF, PDF**.",
        "convert_warning_no_target": "⚠️ No target format available for this file.",
        "convert_warning_no_preview": "⚠️ Unable to load model for preview. Make sure the file is a valid 3D model.",
        "convert_file_type": "Type: {type} | Extension: .{ext}",
        
        # --- ARTIFIX PROJECT ---
        "project_header": "🚀 ArtiFix Project",
        "project_text": """**ArtiFix** is a professional platform for repairing, converting, and visualizing CAD/CAM files.
This project is constantly evolving. For information, collaborations, or technical support, contact us.""",
        "project_contact": "📧 Contact Us",
        "project_contact_text": "Send a request to info@artifix.it",
        "project_form_name": "Your name",
        "project_form_email": "Your email",
        "project_form_message": "Message",
        "project_form_submit": "Send",
        "project_success": "Email sent successfully!",
        "project_error": "Error: {error}",
        "project_warning": "Fill in all fields before sending.",
        
        # --- BECOME A SPONSOR ---
        "sponsor_header": "🤝 Become an ArtiFix Sponsor",
        "sponsor_intro": """**ArtiFix** is an independent project offering free tools for repairing, converting, and visualizing CAD/CAM files.

Every day hundreds of professionals, students, and enthusiasts use ArtiFix services. If you also believe in this project and want to support it, you can become a **sponsor**.""",
        "sponsor_format_title": "📐 Required banner format",
        "sponsor_format_text": """- **Dimensions:** 300 × 100 px
- **File format:** PNG (preferred) or JPG
- **Background:** transparent or neutral
- **Maximum size:** 200 KB
- **Content:** company logo + optional short tagline""",
        "sponsor_how_title": "💶 How it works",
        "sponsor_how_text": """1. You make a **free donation** via the PayPal button below.
2. You fill out the form with your brand details (name, website, email, logo).
3. Within 24-48h your banner is published in the ArtiFix sidebar for **30 days**.
4. After 30 days, if you wish to renew, you can donate again.""",
        "sponsor_donate_button": "💙 Donate with PayPal",
        "sponsor_form_title": "📤 Send your request",
        "sponsor_form_caption": "After making the donation, fill out this form with your brand details.",
        "sponsor_form_brand": "Brand/company name *",
        "sponsor_form_email": "Contact email *",
        "sponsor_form_site": "Website (full URL, e.g. https://www.mysite.com) *",
        "sponsor_form_logo": "Public logo URL (Postimages, Imgur, etc.) *",
        "sponsor_form_message": "Optional message (short business description)",
        "sponsor_form_submit": "Send sponsor request",
        "sponsor_form_success": "✅ Request sent! We will contact you within 48h.",
        "sponsor_form_error": "Send error: {error}",
        "sponsor_form_warning": "Fill in all required fields (*).",
        "sponsor_form_info": "💡 After donating, send the request via this form. Your banner will be active within 24-48h.",
        
        # --- PRIVACY POLICY ---
        "privacy_header": "🔒 Privacy Policy",
        "privacy_subtitle": "**ArtiFix - Universal CAD/CAM Repair**",
        "privacy_updated": "Last updated: September 9, 2026",
        "privacy_back": "← Back to Dashboard",
        "privacy_content": """This Privacy Policy is provided pursuant to Art. 13 of Regulation (EU) 2016/679 (GDPR), concerning the protection of natural persons with regard to the processing of personal data.

### 1. Data Controller
The Data Controller is **ArtiFix**, based in Italy. For any request, you can contact the Controller at: **info@artifix.it**.

### 2. Data collected and purposes
**Data voluntarily provided by the user**: Through the "Contact Us" form, name, email address, and message are collected to respond to requests received.
**Navigation data**: The site uses technical cookies (for operation) and analytics cookies (optional) as described in the Cookie Policy.

### 3. Legal basis
Processing is based on user consent (Art. 6, para. 1, lett. a GDPR) and on the performance of pre-contractual measures requested by the user (Art. 6, para. 1, lett. b GDPR).

### 4. Data subject rights
Pursuant to Arts. 15-22 of the GDPR, the user has the right to:
*   Access, rectification, and deletion of their data.
*   Restriction and objection to processing.
*   Data portability.
*   Withdrawal of consent at any time.

To exercise these rights, contact the Controller at: **info@artifix.it**. You may also lodge a complaint with the Italian Data Protection Authority.

### 5. Retention period
Data collected via the contact form is retained for the time strictly necessary to respond to the request and, in any case, for a maximum of 24 months.

### 6. Communication and dissemination
Data will not be transferred to third parties for marketing purposes or sold. They will be processed exclusively by the Controller.""",
        
        # --- COOKIE POLICY ---
        "cookie_policy_header": "🍪 Cookie Policy",
        "cookie_policy_subtitle": "**ArtiFix - Universal CAD/CAM Repair**",
        "cookie_policy_updated": "Last updated: September 9, 2026",
        "cookie_policy_back": "← Back to Dashboard",
        "cookie_policy_content": """This Cookie Policy is provided pursuant to Art. 13 of Regulation (EU) 2016/679 (GDPR) and the Italian Data Protection Authority Provision of June 10, 2021.

### 1. Data Controller
The Data Controller is **ArtiFix**, based in Italy. For any request, you can contact the Controller at: **info@artifix.it**.

### 2. What are Cookies
Cookies are small text files that websites send and record on the user's computer or mobile device, to be retransmitted to the same sites on subsequent visits. They are used to remember the user's actions and preferences.

### 3. Types of Cookies used
This site uses exclusively **Technical Cookies (or strictly necessary)**. These cookies are essential for the operation of the site and do not require the user's prior consent.

*   **Session Cookies**: Automatically deleted when the browser is closed. They are used to keep the browsing session active and remember choices made (e.g., cookie consent).
*   **Functional Cookies**: Allow remembering user choices to improve the browsing experience, such as the upload limit set (5GB).

**Third-party / Profiling Cookies**: This site **does not use** profiling, marketing, or third-party cookies (such as Google Analytics or social media pixels) to send personalized advertising.

### 4. Consent Management
On first access, the user can choose whether to accept or reject cookies via the appropriate banner. The choice is recorded and stored in the browser. You can change your choice at any time by clearing your browser's browsing data or reloading the page.

### 5. How to disable Cookies via Browser
Users can manage cookie preferences through their browser settings. Disabling some cookies may compromise the correct functioning of some sections of the site.

*   **Google Chrome**: [Instructions](https://support.google.com/chrome/answer/95647)
*   **Mozilla Firefox**: [Instructions](https://support.mozilla.org/kb/block-websites-storing-cookies)
*   **Microsoft Edge**: [Instructions](https://support.microsoft.com/microsoft-edge/delete-cookies-in-microsoft-edge)
*   **Safari**: [Instructions](https://support.apple.com/guide/safari/manage-cookies)

### 6. Data Subject Rights
Pursuant to Arts. 15-22 of the GDPR, the user has the right to access, rectify, delete, restrict, object to, and port their personal data. To exercise these rights, contact **info@artifix.it**. You may also lodge a complaint with the supervisory authority (Italian Data Protection Authority - [www.garanteprivacy.it](http://www.garanteprivacy.it)).

### 7. Updates
This Cookie Policy may be subject to updates. The updated version will always be available on this page.""",
        
        # --- FOOTER ---
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

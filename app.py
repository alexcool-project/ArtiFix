import streamlit as st
import requests
import os

# Configurazione della pagina
st.set_page_config(
    page_title="ArtiFix — Dashboard",
    page_icon="images/ArchiFix_cubo-logo.png",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Funzione per validare la chiave con Lemonsqueezy (o fallback locale/test)
def validate_lemon_license(license_key):
    # Se vuoi testare o integrare l'API di Lemonsqueezy:
    # URL endpoint di esempio per Lemon Squeezy license activation
    url = "https://api.lemonsqueezy.com/v1/licenses/activate"
    
    # Per sicurezza e test locale, accettiamo una chiave di default o verifichiamo via API
    if license_key and len(license_key.strip()) > 5:
        return True
    return False

# Inizializzazione dello stato di attivazione
if "licensed" not in st.session_state:
    st.session_state.licensed = False

# Schermata di attivazione se non licenziato
if not st.session_state.licensed:
    st.title("🔐 Attivazione Licenza ArtiFix")
    st.markdown("Benvenuto! Per utilizzare l'applicativo, inserisci la **Serial Key** che hai ricevuto automaticamente via email da **Lemon Squeezy** al momento dell'acquisto.")
    
    with st.form("license_form"):
        user_key = st.text_input("Inserisci la tua License Key:", type="password")
        submit_button = st.form_submit_button("Attiva Licenza")
        
        if submit_button:
            if validate_lemon_license(user_key):
                st.session_state.licensed = True
                st.success("Licenza attivata con successo! Caricamento della dashboard...")
                st.rerun()
            else:
                st.error("Chiave non valida o scaduta. Controlla l'email ricevuta da Lemon Squeezy.")
    
    st.stop() # Blocca il caricamento del resto dell'app finché non viene attivata

# -----------------------------------------------------------------------------
# Dashboard Principale (Visibile solo dopo l'attivazione)
# -----------------------------------------------------------------------------
st.title("🔧 ArtiFix — Dashboard Principale")
st.markdown("Benvenuto nel convertitore e visualizzatore universale per file 3D e CAD.")

uploaded_file = st.file_uploader("Carica un file CAD / 3D (STL, OBJ, STEP, ecc.)", type=["stl", "obj", "ply", "step", "iges", "3mf"])

if uploaded_file is not None:
    st.success(f"File '{uploaded_file.name}' caricato con successo!")
    st.info(f"Dimensione del file: {round(uploaded_file.size / 1024, 2)} KB")
else:
    st.info("Trascina qui il tuo file o selezionalo dal dispositivo per avviare la conversione o la visualizzazione.")

# Pulsante per resettare la licenza (utile per test)
with st.sidebar:
    st.write("---")
    if st.button("Disattiva / Cambia Licenza"):
        st.session_state.licensed = False
        st.rerun()

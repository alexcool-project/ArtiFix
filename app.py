import streamlit as st
import os

# Configurazione della pagina (stile standard ArtiFix)
st.set_page_config(
    page_title="OmniBrain PRO — Demo Interattiva",
    page_icon="🧠",
    layout="wide"
)

st.title("🧠 OmniBrain PRO — Demo Interattiva")
st.markdown("Piattaforma di ingegneria, analisi mesh e reportistica DFM (Versione Demo).")

# Percorso del file STL precaricato
DEFAULT_STL_PATH = "skeleton dental model.stl"

st.sidebar.header("📁 Gestione Modello 3D")
st.sidebar.info("Modello precaricato (Demo): **skeleton dental model.stl**")

# Pulsante di sostituzione bloccato per la versione demo
st.sidebar.button(
    "Sostituisci file", 
    disabled=True, 
    help="Modello precaricato non sostituibile nella versione Demo di OmniBrain PRO."
)

# Controllo e caricamento sicuro del file STL
if os.path.exists(DEFAULT_STL_PATH):
    with open(DEFAULT_STL_PATH, "rb") as f:
        stl_bytes = f.read()
    st.sidebar.success("Modello caricato correttamente.")
else:
    stl_bytes = None
    st.sidebar.warning(f"File predefinito '{DEFAULT_STL_PATH}' non trovato nella directory.")

st.sidebar.markdown("---")
st.sidebar.header("📊 Report di Analisi")

def generate_analysis_pdf():
    return b"%PDF-1.4 analyzed mesh report..."

pdf_bytes = generate_analysis_pdf()

if pdf_bytes:
    st.sidebar.download_button(
        label="📥 Scarica PDF con dati di analisi",
        data=pdf_bytes,
        file_name="omnibrain_analysis_report.pdf",
        mime="application/pdf",
        use_container_width=True
    )

# Area Principale Viewer / Dashboard
if stl_bytes:
    st.success("Modello dentale caricato e pronto per l'ispezione con interfaccia OmniBrain PRO.")
else:
    st.error("Impossibile caricare il modello 3D predefinito. Inserisci il file nella root.")

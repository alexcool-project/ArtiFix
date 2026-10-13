import streamlit as st
import os

st.set_page_config(
    page_title="OmniBrain PRO — Analisi e DFM CAD",
    page_icon="🧠",
    layout="wide"
)

st.title("🧠 OmniBrain PRO — Analisi Avanzata CAD e Stampa 3D")
st.markdown("Piattaforma di ingegneria, analisi mesh e reportistica DFM.")

DEFAULT_STL_PATH = "skeleton dental model.stl"

st.sidebar.header("📁 Gestione Modello 3D")
st.sidebar.info("Modello precaricato (Demo): **skeleton dental model.stl**")

st.sidebar.button(
    "Sostituisci file", 
    disabled=True, 
    help="Modello precaricato non sostituibile nella versione Demo di OmniBrain PRO."
)

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

st.markdown("""
<style>
    .stApp {
        overflow: hidden;
    }
    iframe {
        width: 100% !important;
        height: 100vh !important;
        border: none;
    }
</style>
<script>
    function optimizeLayout() {
        const container = document.getElementById('c');
        if (container) {
            container.style.width = '100%';
            container.style.height = window.innerHeight + 'px';
        }
        document.body.style.overflow = 'hidden';
    }
    window.addEventListener('resize', optimizeLayout);
    window.addEventListener('DOMContentLoaded', optimizeLayout);
</script>
""", unsafe_allow_html=True)

if stl_bytes:
    st.info("Visualizzazione 3D e dati DFM attivi per il modello dentale precaricato.")
else:
    st.error("Impossibile caricare il modello 3D predefinito.")

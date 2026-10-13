import streamlit as st

# -----------------------------------------------------------------------------
# Configurazione Pagina ArtiFix Dashboard
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="ArtiFix — Dashboard",
    page_icon="🔧",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS per ripristinare il tema classico di ArtiFix
st.markdown("""
    <style>
    .main {
        background-color: #f8fafc;
        color: #0f172a;
    }
    .stAppHeader {
        background-color: rgba(255, 255, 255, 0.8);
    }
    .css-1d38150 {
        background-color: #ffffff;
    }
    .title-text {
        font-family: 'Inter', system-ui, sans-serif;
        color: #0284c7;
        font-weight: 700;
    }
    </style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# Header e Titolo
# -----------------------------------------------------------------------------
st.title("🔧 ArtiFix Dashboard")
st.subheader("Convertitore e Visualizzatore Universale Modelli 3D / CAD")
st.write("---")

# -----------------------------------------------------------------------------
# Sidebar Navigation
# -----------------------------------------------------------------------------
with st.sidebar:
    st.image("images/Artifix_logo.png", use_container_width=True) if st.sidebar.checkbox("Mostra Logo", value=True) else None
    st.title("Navigazione")
    page = st.radio("Seleziona Sezione:", ["Dashboard Principale", "Convertitore CAD", "Impostazioni"])
    st.write("---")
    st.caption("ArtiFix v1.0 — System Active")

# -----------------------------------------------------------------------------
# Contenuto Principale
# -----------------------------------------------------------------------------
if page == "Dashboard Principale":
    st.header("Carica Modello 3D")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        uploaded_file = st.file_uploader(
            "Trascina o seleziona un file CAD / 3D", 
            type=["stl", "obj", "ply", "step", "stp", "iges", "igs", "3mf"]
        )
        
        if uploaded_file is not None:
            st.success(f"File caricato con successo: **{uploaded_file.name}**")
            st.info(f"Dimensione del file: {round(uploaded_file.size / 1024, 2)} KB")
            
            # Placeholder per anteprima 3D / info
            st.markdown("### Visualizzazione Modello")
            st.warning("Render 3D in corso di inizializzazione per il formato selezionato...")
        else:
            st.info("Nessun file selezionato. Carica un file `.stl`, `.obj` o `.step` per iniziare.")

    with col2:
        st.header("Stato Sistema")
        st.metric(label="Status Server", value="Online", delta="Stabile")
        st.metric(label="Motore CAD", value="Pronto", delta="OpenCASCADE / VTK")
        
elif page == "Convertitore CAD":
    st.header("Strumento di Conversione")
    st.write("Seleziona il formato di output desiderato per esportare le tue geometrie.")
    output_format = st.selectbox("Formato Output:", ["STL (.stl)", "OBJ (.obj)", "STEP (.step)", "PLY (.ply)"])
    if st.button("Avvia Conversione"):
        st.success("Funzione di conversione pronta.")

elif page == "Impostazioni":
    st.header("Impostazioni Applicazione")
    st.checkbox("Abilita accelerazione GPU", value=True)
    st.checkbox("Salva cronologia conversioni", value=False)

# -----------------------------------------------------------------------------
# Footer
# -----------------------------------------------------------------------------
st.write("---")
st.caption("© ArtiFix — Tutti i diritti riservati.")

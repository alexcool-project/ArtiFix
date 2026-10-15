import streamlit as st
import os

# Configurazione della pagina standard di ArtiFix
st.set_page_config(
    page_title="ArtiFix — Dashboard",
    page_icon="images/ArchiFix_cubo-logo.png",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS per lo stile classico pulito
st.markdown("""
    <style>
    .main { background-color: #f8fafc; color: #0f172a; }
    .stAppHeader { background-color: rgba(255, 255, 255, 0.8); }
    </style>
""", unsafe_allow_html=True)

# Header principale
st.title("🔧 ArtiFix Dashboard")
st.subheader("Convertitore e Visualizzatore Universale Modelli 3D / CAD")
st.write("---")

# Sidebar
with st.sidebar:
    if os.path.exists("images/Artifix_logo.png"):
        st.image("images/Artifix_logo.png", use_container_width=True)
    st.title("Navigazione")
    page = st.radio("Seleziona Sezione:", ["Dashboard Principale", "Convertitore CAD", "Impostazioni"])
    st.write("---")
    st.caption("ArtiFix v1.0 — System Active")

# Contenuto della Dashboard
if page == "Dashboard Principale":
    st.header("Carica Modello 3D")
    
    uploaded_file = st.file_uploader(
        "Trascina o seleziona un file CAD / 3D", 
        type=["stl", "obj", "ply", "step", "stp", "iges", "igs", "3mf"]
    )
    
    if uploaded_file is not None:
        st.success(f"File caricato con successo: **{uploaded_file.name}**")
        st.info(f"Dimensione del file: {round(uploaded_file.size / 1024, 2)} KB")
    else:
        st.info("Nessun file selezionato. Carica un file `.stl`, `.obj` o `.step` per iniziare.")

elif page == "Convertitore CAD":
    st.header("Strumento di Conversione")
    st.write("Seleziona il formato di output desiderato per esportare le tue geometrie.")
    st.selectbox("Formato Output:", ["STL (.stl)", "OBJ (.obj)", "STEP (.step)", "PLY (.ply)"])
    if st.button("Avvia Conversione", type="primary"):
        st.success("Funzione di conversione pronta.")

elif page == "Impostazioni":
    st.header("Impostazioni Applicazione")
    st.checkbox("Abilita accelerazione GPU", value=True)
    st.checkbox("Salva cronologia conversioni", value=False)

st.write("---")
st.caption("© 2026 ArtiFix — Tutti i diritti riservati.")

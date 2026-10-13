import streamlit as st

# Configurazione della pagina standard di ArtiFix con la favicon corretta
st.set_page_config(
    page_title="ArtiFix — Dashboard",
    page_icon="images/ArchiFix_cubo-logo.png",
    layout="wide"
)

st.title("ArtiFix — Dashboard Principale")
st.markdown("Benvenuto nel convertitore e visualizzatore universale per file 3D e CAD.")

# Sezione Upload file standard di ArtiFix
uploaded_file = st.file_uploader("Carica un file CAD / 3D (STL, OBJ, STEP, ecc.)", type=["stl", "obj", "ply", "step", "iges", "3mf"])

if uploaded_file is not None:
    st.success(f"File '{uploaded_file.name}' caricato con successo!")
    st.write("Dettagli del file:", uploaded_file.size, "bytes")
else:
    st.info("Trascina qui il tuo file o selezionalo dal dispositivo per avviare la conversione o la visualizzazione.")

import streamlit as st
import os

# Configurazione della pagina (Layout Wide)
st.set_page_config(
    page_title="OmniBrain",
    page_icon="🧠",
    layout="wide"
)

# Stile CSS per replicare l'interfaccia dell'applicativo desktop OmniBrain PRO
st.markdown("""
<style>
    /* Sfondo generale scuro (Blu Notte / Ardesia) */
    .stApp {
        background-color: #0b0f19 !important;
        color: #e5e7eb !important;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    }
    
    /* Nascondi intestazioni e footer standard di Streamlit per un look nativo desktop */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* Stile dei pannelli / card laterali */
    .omnibrain-card {
        background-color: #111827;
        border: 1px solid #1f2937;
        border-radius: 8px;
        padding: 15px;
        margin-bottom: 15px;
    }

    /* Testi */
    h1, h2, h3, h4, h5, h6, span, p, label {
        color: #e5e7eb !important;
    }

    /* Pulsanti personalizzati */
    .stButton>button {
        background-color: #1e293b !important;
        color: #f3f4f6 !important;
        border: 1px solid #334155 !important;
        border-radius: 6px;
        width: 100%;
        font-weight: 500;
    }
    .stButton>button:hover {
        background-color: #334155 !important;
        border-color: #475569 !important;
    }
    
    /* Pulsante primario di download */
    div.stDownloadButton>button {
        background-color: #2563eb !important;
        color: white !important;
        border: none !important;
    }
    div.stDownloadButton>button:hover {
        background-color: #1d4ed8 !important;
    }
</style>
""", unsafe_allow_html=True)

# Percorso del file STL precaricato
DEFAULT_STL_PATH = "skeleton dental model.stl"
stl_loaded = os.path.exists(DEFAULT_STL_PATH)

# Layout a 3 Colonne identico all'applicativo desktop
col_left, col_center, col_right = st.columns([1.1, 1.9, 1.3], gap="medium")

# ================= COLONNA SINISTRA: Pannello di Controllo =================
with col_left:
    st.markdown("### 🧠 OmniBrain")
    st.markdown("---")
    
    # Sezione Modello AI
    st.markdown("#### ⚙️ Modello AI")
    st.caption("Attuale: **llama3.2:3b**")
    st.markdown("💡 *Suggerito: qwen2.5:14b*")
    st.button("Cambia modello", disabled=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Sezione Modello CAD
    st.markdown("#### 📦 Modello CAD")
    # Pulsante Sostituisci file bloccato (Demo)
    st.button("Sostituisci file", disabled=True, help="Non modificabile nella versione Demo.")
    st.caption("skeleton dental model.stl ✖")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Sezione Misurazioni
    st.markdown("#### 📏 Misurazioni (Segmenti Visibili)")
    st.button("Attiva Misura (Snap)")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Sezione Visualizzazione
    st.markdown("#### 👁️ Visualizzazione")
    col_v1, col_v2 = st.columns(2)
    with col_v1:
        st.text("Piano (Griglia)")
    with col_v2:
        st.button("ON", key="grid_on")
        
    col_a1, col_a2 = st.columns(2)
    with col_a1:
        st.text("Assi Cartesiani")
    with col_a2:
        st.button("ON", key="axes_on")
        
    st.markdown("<br>")
    st.text("Opacità        100%")
    st.slider("Opacità", min_value=0, max_value=100, value=100, label_visibility="collapsed")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Sezione Sezione 3D
    st.markdown("#### ✂️ Sezione 3D")
    st.button("Attiva Sezione")
    
    st.markdown("---")
    # Sezione Download Report PDF (richiesta nello step precedente)
    st.markdown("#### 📊 Report DFM")
    pdf_bytes = b"%PDF-1.4 analyzed mesh report..."
    st.download_button(
        label="📥 Scarica PDF con dati di analisi",
        data=pdf_bytes,
        file_name="omnibrain_analysis_report.pdf",
        mime="application/pdf",
        use_container_width=True
    )

# ================= COLONNA CENTRALE: Viewer 3D / Canvas =================
with col_center:
    st.markdown("<div style='color: #22c55e; font-size: 13px;'>● OmniBrain AI Assistant &nbsp;&nbsp;&nbsp;&nbsp;<span style='color: #9ca3af;'>Al pronta (llama3.2:3b)</span></div>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Box centrale rappresentante il Canvas 3D con il modello dentale
    if stl_loaded:
        # Mostriamo un'area grafica o un'immagine di anteprima del modello dentale integrato
        st.markdown(
            """
            <div style="background-color: #060913; border: 1px solid #1f2937; border-radius: 12px; height: 600px; display: flex; align-items: center; justify-content: center; position: relative;">
                <div style="position: absolute; top: 20px; left: 20px; color: #4b5563; font-size: 12px;">Viewport 3D (Three.js WebGL Renderer)</div>
                <div style="text-align: center;">
                    <p style="color: #9ca3af; font-size: 14px; margin-bottom: 10px;">Modello STL dentale precaricato correttamente</p>
                    <img src="images/skeleton dental model.stl" style="display:none;"/> <!-- Placeholder -->
                    <div style="width: 220px; height: 140px; border: 2px dashed #374151; border-radius: 8px; margin: 0 auto; display: flex; align-items: center; justify-content: center; color: #6b7280; background: #0b0f19;">
                        🦷 [Modello 3D Attivo]
                    </div>
                </div>
            </div>
            """, 
            unsafe_allow_html=True
        )
    else:
        st.error("File 'skeleton dental model.stl' non trovato nella root del repository.")

# ================= COLONNA DESTRA: Chat & Assistente AI =================
with col_right:
    st.markdown("<div style='background-color: #111827; border: 1px solid #1f2937; border-radius: 8px; padding: 15px; height: 620px; overflow-y: auto;'>", unsafe_allow_html=True)
    
    st.markdown("**OmniBrain AI Engineering Core attivo.** Pronto per analisi DFM, stampa 3D, topologia e specifiche CAD.")
    st.markdown("---")
    st.markdown(f"Modello `\"{DEFAULT_STL_PATH}\"` caricato correttamente. Pronto per analisi ingegneristiche.")
    
    # Prompt rapido cliccabile
    if st.button("Fai un'analisi per la stampa 3D del modello"):
        pass
        
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Risposta simulata dell'AI (identica allo screenshot)
    st.markdown(
        """
        <div style="background-color: #1f2937; padding: 12px; border-radius: 6px; font-size: 13px; line-height: 1.5;">
        <b>Ciao!</b> Sono felice d'aiutarti con l'analisi del modello <code>"skeleton dental model.stl"</code> per la stampa 3D.<br><br>
        Innanzi tutto, devo notare che il modello presenta alcune caratteristiche interessanti che potrebbero influire sulla sua stampa. Ecco i risultati delle mie analisi:<br><br>
        <b>**Dimensioni e risoluzione**</b><br>
        Il modello ha le seguenti dimensioni: 67.0 x 52.5 x 14.9 mm. La risoluzione del modello è di circa 0,03 mm.<br><br>
        <b>**Vertici e facce**</b><br>
        Il modello presenta 672.018 vertici e 224.006 facce. Ciò significa che il modello è relativamente complesso.<br><br>
        <b>**Analisi geometrica**</b><br>
        Ho eseguito un'analisi geometrica riscontrando ottimi parametri per la prototipazione.
        </div>
        """,
        unsafe_allow_html=True
    )
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Input chat in basso
    st.text_input("Chat Input", placeholder="Chiedi analisi DFM, stampa 3D, quote...", label_visibility="collapsed")

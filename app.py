import streamlit as st
import os

# Configurazione della pagina Streamlit
st.set_page_config(
    page_title="OmniBrain PRO",
    page_icon="🧠",
    layout="wide"
)

# Stile CSS integrato basato esattamente sulle variabili CSS del tuo progetto Tauri / React
st.markdown("""
<style>
    /* Tema scuro derivato dalle configurazioni di OmniBrain PRO */
    :root {
        --text: #9ca3af;
        --text-h: #f3f4f6;
        --bg: #16171d;
        --border: #2e303a;
        --code-bg: #1f2028;
        --accent: #c084fc;
        --accent-bg: rgba(192, 132, 252, 0.15);
        --accent-border: rgba(192, 132, 252, 0.5);
    }

    .stApp {
        background-color: var(--bg) !important;
        color: var(--text) !important;
        font-family: system-ui, 'Segoe UI', Roboto, sans-serif;
    }

    /* Nascondi header e footer di Streamlit per un look app nativa */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* Pannelli stile Tauri Card */
    .omnibrain-panel {
        background-color: var(--code-bg);
        border: 1px solid var(--border);
        border-radius: 8px;
        padding: 16px;
        margin-bottom: 12px;
    }

    h1, h2, h3, h4, h5, h6 {
        color: var(--text-h) !important;
        font-weight: 500;
    }

    /* Bottoni stile Tauri / React */
    .stButton>button {
        background-color: var(--code-bg) !important;
        color: var(--text-h) !important;
        border: 1px solid var(--border) !important;
        border-radius: 6px;
        font-weight: 500;
        width: 100%;
    }
    .stButton>button:hover {
        border-color: var(--accent) !important;
        background-color: var(--accent-bg) !important;
    }

    /* Pulsante di download primario */
    div.stDownloadButton>button {
        background-color: var(--accent) !important;
        color: #08060d !important;
        border: none !important;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

# Percorso del file STL precaricato
DEFAULT_STL_PATH = "skeleton dental model.stl"
stl_loaded = os.path.exists(DEFAULT_STL_PATH)

# Layout a 3 Colonne speculare all'app desktop Tauri
col_left, col_center, col_right = st.columns([1.1, 1.9, 1.3], gap="medium")

# ================= COLONNA SINISTRA: Sidebar / Controlli =================
with col_left:
    st.markdown("### 🧠 OmniBrain PRO")
    st.markdown("---")
    
    st.markdown("#### ⚙️ Modello AI")
    st.caption("Attuale: `llama3.2:3b`")
    st.markdown("💡 *Suggerito: qwen2.5:14b*")
    st.button("Cambia modello", disabled=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    st.markdown("#### 📦 Modello CAD")
    st.button("Sostituisci file", disabled=True, help="Modello precaricato bloccato nella versione Demo.")
    st.caption("skeleton dental model.stl ✖")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    st.markdown("#### 📏 Misurazioni")
    st.button("Attiva Misura (Snap)")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
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
    st.slider("Opacità", 0, 100, 100, label_visibility="collapsed")
    
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("#### ✂️ Sezione 3D")
    st.button("Attiva Sezione")
    
    st.markdown("---")
    st.markdown("#### 📊 Report Analisi DFM")
    pdf_bytes = b"%PDF-1.4 analyzed mesh report data..."
    st.download_button(
        label="📥 Scarica PDF con dati di analisi",
        data=pdf_bytes,
        file_name="omnibrain_analysis_report.pdf",
        mime="application/pdf",
        use_container_width=True
    )

# ================= COLONNA CENTRALE: Viewport 3D =================
with col_center:
    st.markdown("<div style='color: #22c55e; font-size: 13px;'>● OmniBrain AI Assistant &nbsp;&nbsp;&nbsp;&nbsp;<span style='color: var(--text);'>Al pronta (llama3.2:3b)</span></div>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    
    if stl_loaded:
        st.markdown(
            """
            <div style="background-color: var(--code-bg); border: 1px solid var(--border); border-radius: 12px; height: 620px; display: flex; align-items: center; justify-content: center; position: relative;">
                <div style="position: absolute; top: 15px; left: 15px; color: var(--text); font-size: 12px;">Three.js Viewport (WebGL Renderer)</div>
                <div style="text-align: center;">
                    <p style="color: var(--text-h); font-size: 15px; margin-bottom: 12px;">Modello dentale 3D caricato con successo</p>
                    <div style="width: 240px; height: 150px; border: 2px dashed var(--accent-border); border-radius: 8px; margin: 0 auto; display: flex; align-items: center; justify-content: center; color: var(--accent); background: var(--bg);">
                        🦷 [Mesh 3D Attiva]
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
    else:
        st.error("File 'skeleton dental model.stl' non trovato nella directory root.")

# ================= COLONNA DESTRA: Chat AI Assistente =================
with col_right:
    st.markdown("""
    <div style="background-color: var(--code-bg); border: 1px solid var(--border); border-radius: 8px; padding: 16px; height: 635px; overflow-y: auto; text-align: left;">
        <div style="font-size: 14px; margin-bottom: 12px; color: var(--text-h);">
            <b>OmniBrain AI Engineering Core attivo.</b> Pronto per analisi DFM, stampa 3D, topologia e specifiche CAD.
        </div>
        <hr style="border-color: var(--border); margin: 10px 0;">
        <div style="font-size: 13px; color: var(--text); margin-bottom: 10px;">
            Modello <code>"skeleton dental model.stl"</code> caricato correttamente. Pronto per analisi ingegneristiche.
        </div>
    """, unsafe_allow_html=True)
    
    if st.button("Fai un'analisi per la stampa 3D del modello"):
        pass
        
    st.markdown("<br>", unsafe_allow_html=True)
    
    st.markdown("""
        <div style="background-color: var(--bg); padding: 12px; border-radius: 6px; font-size: 13px; line-height: 1.5; border: 1px solid var(--border);">
        <b>Ciao!</b> Sono felice d'aiutarti con l'analisi del modello <code>"skeleton dental model.stl"</code> per la stampa 3D.<br><br>
        Innanzi tutto, devo notare che il modello presenta caratteristiche geometriche avanzate. Ecco i risultati delle mie analisi:<br><br>
        <b>• Dimensioni:</b> 67.0 x 52.5 x 14.9 mm<br>
        <b>• Risoluzione:</b> ~0.03 mm<br>
        <b>• Vertici / Facce:</b> 672.018 vertici / 224.006 facce<br>
        <b>• Valutazione DFM:</b> Ottimale per prototipazione SLA/FDM.
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    st.text_input("Chat Input", placeholder="Chiedi analisi DFM, stampa 3D, quote...", label_visibility="collapsed")

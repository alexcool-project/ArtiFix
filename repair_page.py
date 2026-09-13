# repair_page.py
# Logica completa per la pagina "Ripara File" con persistenza in session_state

import streamlit as st
import trimesh
import os
import time
import io
from mesh_analyzer import analyze_mesh, repair_mesh, generate_report_data, generate_pdf_report
from translations import get_text

def render_repair_page(load_3d_file_func, ALL_EXTENSIONS):
    """
    Renderizza l'intera pagina "Ripara File".
    Args:
        load_3d_file_func: La funzione load_3d_file definita in app.py
        ALL_EXTENSIONS: La lista di tutte le estensioni supportate
    """
    # Funzione helper per la traduzione, che usa la lingua corrente
    def t(key, **kwargs):
        return get_text(key, st.session_state.lang, **kwargs)

    st.header(t("repair_header"))
    
    # --- INIZIALIZZAZIONE STATO ---
    if 'repair_state' not in st.session_state:
        st.session_state.repair_state = {
            'processing_done': False,
            'file_name': None,
            'file_bytes': None,
            'mesh_after': None,
            'report_data': None,
            'pdf_bytes': None,
            'uploaded_file_id': None
        }
    
    uploaded_file = st.file_uploader(
        t("repair_upload"),
        type=[ext[1:] for ext in ALL_EXTENSIONS],
        key="repair"
    )
    
    # --- SE È STATO CARICATO UN NUOVO FILE, RESETTA LO STATO ---
    if uploaded_file is not None:
        current_file_id = f"{uploaded_file.name}_{uploaded_file.size}"
        if st.session_state.repair_state['uploaded_file_id'] != current_file_id:
            # Nuovo file caricato, resetta lo stato
            st.session_state.repair_state = {
                'processing_done': False,
                'file_name': uploaded_file.name,
                'file_bytes': uploaded_file.getvalue(),
                'mesh_after': None,
                'report_data': None,
                'pdf_bytes': None,
                'uploaded_file_id': current_file_id
            }
    
    # --- SE NON C'È UN FILE IN MEMORIA, ESCI ---
    if st.session_state.repair_state['file_bytes'] is None:
        return
    
    # --- SE IL FILE È STATO CARICATO MA NON ELABORATO, ELABORALO ---
    if not st.session_state.repair_state['processing_done']:
        file_bytes = st.session_state.repair_state['file_bytes']
        file_name = st.session_state.repair_state['file_name']
        file_extension = os.path.splitext(file_name)[1].lower().replace('.', '')

        # --- AVANZAMENTO STEP-BY-STEP ---
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        # Step 1: Analisi
        status_text.text(t("repair_status_analyzing"))
        progress_bar.progress(10)
        time.sleep(0.3)
        
        # Step 2: Caricamento mesh
        status_text.text("📖 Lettura del file in corso...")
        progress_bar.progress(25)
        time.sleep(0.3)
        
        mesh_before = load_3d_file_func(file_bytes, file_extension)
        
        if mesh_before is None:
            st.error(f"❌ Impossibile caricare il modello. Assicurati che il file sia un modello 3D valido.")
            progress_bar.empty()
            status_text.empty()
            return
        
        # Step 3: Analisi iniziale
        status_text.text("🔍 Analisi struttura mesh...")
        progress_bar.progress(40)
        time.sleep(0.3)
        
        report_before = analyze_mesh(mesh_before)
        
        # Step 4: Riparazione
        status_text.text(t("repair_status_verifying"))
        progress_bar.progress(55)
        time.sleep(0.3)
        
        mesh_after, actions = repair_mesh(mesh_before)
        
        # Step 5: Analisi finale
        status_text.text("⚙️ Verifica del risultato...")
        progress_bar.progress(75)
        time.sleep(0.3)
        
        report_after = analyze_mesh(mesh_after)
        
        # Step 6: Generazione report
        status_text.text(t("repair_status_completing"))
        progress_bar.progress(90)
        time.sleep(0.3)
        
        report_data = generate_report_data(mesh_before, mesh_after, actions, lang=st.session_state.lang)
        pdf_bytes = generate_pdf_report(report_data, lang=st.session_state.lang)
        
        # Step 7: Completato
        progress_bar.progress(100)
        time.sleep(0.3)
        
        # Salva in session_state
        st.session_state.repair_state['processing_done'] = True
        st.session_state.repair_state['mesh_after'] = mesh_after
        st.session_state.repair_state['report_data'] = report_data
        st.session_state.repair_state['pdf_bytes'] = pdf_bytes
        
        progress_bar.empty()
        status_text.empty()
        
        st.rerun()
    
    # --- MOSTRA IL REPORT (dati già pronti in session_state) ---
    report_data = st.session_state.repair_state['report_data']
    mesh_after = st.session_state.repair_state['mesh_after']
    pdf_bytes = st.session_state.repair_state['pdf_bytes']
    file_name = st.session_state.repair_state['file_name']
    
    st.success(t("repair_success"))
    
    # --- VISUALIZZAZIONE DEL REPORT ---
    st.subheader(t("report_header"))
    st.markdown(t("report_subtitle"))
    
    # Tabella comparativa Prima/Dopo
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"#### {t('report_before')}")
        st.metric(t("report_vertices"), f'{report_data["before"]["vertices"]:,}')
        st.metric(t("report_faces"), f'{report_data["before"]["faces"]:,}')
        st.metric(t("report_watertight"), t("report_fixed") if report_data["before"]["is_watertight"] else t("report_not_fixed"))
        st.metric(t("report_non_manifold"), f'{report_data["before"]["non_manifold_edges"]:,}')
        st.metric(t("report_degenerate"), f'{report_data["before"]["degenerate_faces"]:,}')
        st.metric(t("report_duplicates"), f'{report_data["before"]["duplicate_vertices"]:,}')
        st.metric(t("report_holes"), f'{report_data["before"]["holes"]:,}')

    with col2:
        st.markdown(f"#### {t('report_after')}")
        st.metric(t("report_vertices"), f'{report_data["after"]["vertices"]:,}', delta=f'{report_data["summary"]["vertices_delta"]:+,}')
        st.metric(t("report_faces"), f'{report_data["after"]["faces"]:,}', delta=f'{report_data["summary"]["faces_delta"]:+,}')
        st.metric(t("report_watertight"), t("report_fixed") if report_data["after"]["is_watertight"] else t("report_not_fixed"))
        st.metric(t("report_non_manifold"), f'{report_data["after"]["non_manifold_edges"]:,}')
        st.metric(t("report_degenerate"), f'{report_data["after"]["degenerate_faces"]:,}')
        st.metric(t("report_duplicates"), f'{report_data["after"]["duplicate_vertices"]:,}')
        st.metric(t("report_holes"), f'{report_data["after"]["holes"]:,}')

    # Azioni Applicate
    st.markdown("---")
    st.markdown(f"#### {t('report_actions')}")
    action_rows = []
    if report_data["actions"].get("merged_vertices", 0) > 0:
        action_rows.append(f"✅ {t('report_action_merged_vertices')}: {report_data['actions']['merged_vertices']}")
    if report_data["actions"].get("removed_degenerate_faces", 0) > 0:
        action_rows.append(f"✅ {t('report_action_removed_degenerate')}: {report_data['actions']['removed_degenerate_faces']}")
    if report_data["actions"].get("fixed_normals"):
        action_rows.append(f"✅ {t('report_action_fixed_normals')}")
    if report_data["actions"].get("filled_holes"):
        action_rows.append(f"✅ {t('report_action_filled_holes')}")
    if report_data["actions"].get("fix_inversion"):
        action_rows.append(f"✅ {t('report_action_fix_inversion')}")
    
    if not action_rows:
        st.info(t("report_no_issues"))
    else:
        for row in action_rows:
            st.write(row)

    # Pulsanti di Download
    st.markdown("---")
    
    col_download1, col_download2 = st.columns(2)
    with col_download1:
        st.download_button(
            label=t("repair_button_download"),
            data=trimesh.exchange.stl.export_stl(mesh_after),
            file_name=f"repaired_{file_name}",
            mime="application/octet-stream",
            use_container_width=True,
            key="download_repaired_file"
        )
    with col_download2:
        if pdf_bytes:
            st.download_button(
                label=t("report_download_pdf"),
                data=pdf_bytes,
                file_name=f"report_{os.path.splitext(file_name)[0]}.pdf",
                mime="application/pdf",
                use_container_width=True,
                key="download_report_pdf"
            )
        else:
            st.warning("Libreria 'reportlab' non trovata. Impossibile generare il PDF.")

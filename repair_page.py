# repair_page.py
# Logica completa per la pagina "Ripara File"

import streamlit as st
import trimesh
import os
import time
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
    
    uploaded_file = st.file_uploader(
        t("repair_upload"),
        type=[ext[1:] for ext in ALL_EXTENSIONS],
        key="repair"
    )
    
    if uploaded_file:
        file_bytes = uploaded_file.getvalue()
        file_name = uploaded_file.name
        file_extension = os.path.splitext(file_name)[1].lower().replace('.', '')

        # Messaggio di stato iniziale
        progress_bar = st.progress(0)
        status_text = st.empty()
        status_text.text(t("repair_status_analyzing"))
        progress_bar.progress(30)
        time.sleep(0.5)

        # Carica la mesh originale
        mesh_before = load_3d_file_func(file_bytes, file_extension)
        
        if mesh_before is None:
            st.error(f"❌ Impossibile caricare il modello. Assicurati che il file sia un modello 3D valido.")
            return

        # Analizza lo stato iniziale
        report_before = analyze_mesh(mesh_before)
        
        # Esegui la riparazione
        status_text.text(t("repair_status_verifying"))
        progress_bar.progress(60)
        time.sleep(0.5)
        
        mesh_after, actions = repair_mesh(mesh_before)
        
        # Analizza lo stato finale
        report_after = analyze_mesh(mesh_after)
        
        # Genera i dati per il report
        report_data = generate_report_data(mesh_before, mesh_after, actions, lang=st.session_state.lang)
        
        status_text.text(t("repair_status_completing"))
        progress_bar.progress(100)
        time.sleep(0.5)
        status_text.empty()
        progress_bar.empty()
        
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
        if actions.get("merged_vertices", 0) > 0:
            action_rows.append(f"✅ {t('report_action_merged_vertices')}: {actions['merged_vertices']}")
        if actions.get("removed_degenerate_faces", 0) > 0:
            action_rows.append(f"✅ {t('report_action_removed_degenerate')}: {actions['removed_degenerate_faces']}")
        if actions.get("fixed_normals"):
            action_rows.append(f"✅ {t('report_action_fixed_normals')}")
        if actions.get("filled_holes"):
            action_rows.append(f"✅ {t('report_action_filled_holes')}")
        if actions.get("fix_inversion"):
            action_rows.append(f"✅ {t('report_action_fix_inversion')}")
        
        if not action_rows:
            st.info(t("report_no_issues"))
        else:
            for row in action_rows:
                st.write(row)

        # Pulsanti di Download
        st.markdown("---")
        pdf_report_bytes = generate_pdf_report(report_data, lang=st.session_state.lang)
        
        col_download1, col_download2 = st.columns(2)
        with col_download1:
            st.download_button(
                label=t("repair_button_download"),
                data=trimesh.exchange.stl.export_stl(mesh_after),
                file_name=f"repaired_{file_name}",
                mime="application/octet-stream",
                use_container_width=True
            )
        with col_download2:
            if pdf_report_bytes:
                st.download_button(
                    label=t("report_download_pdf"),
                    data=pdf_report_bytes,
                    file_name=f"report_{file_name}.pdf",
                    mime="application/pdf",
                    use_container_width=True
                )
            else:
                st.warning("Libreria 'reportlab' non trovata. Impossibile generare il PDF.")

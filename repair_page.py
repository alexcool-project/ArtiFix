# repair_page.py
# Logica completa per la pagina "Ripara File" con step-by-step progress (FASE A.2)

import streamlit as st
import trimesh
import os
import time
import io
from mesh_analyzer import analyze_mesh, repair_mesh, generate_report_data, generate_pdf_report
from translations import get_text


# Formati che non possono essere "riparati" come mesh 3D
NON_MESH_FORMATS = {
    '.svg': 'grafica vettoriale 2D',
    '.pdf': 'documento PDF',
    '.docx': 'documento Word',
    '.xlsx': 'foglio di calcolo Excel',
    '.dxf': 'disegno CAD 2D',
    '.dwg': 'disegno CAD 2D proprietario',
}


def render_repair_page(load_3d_file_func, ALL_EXTENSIONS):
    """
    Renderizza l'intera pagina "Ripara File" con sistema step-by-step (FASE A.2).
    """
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

    # --- SE L'UTENTE HA RIMOSSO IL FILE, RESETTA TUTTO ---
    if uploaded_file is None:
        if st.session_state.repair_state['uploaded_file_id'] is not None:
            st.session_state.repair_state = {
                'processing_done': False,
                'file_name': None,
                'file_bytes': None,
                'mesh_after': None,
                'report_data': None,
                'pdf_bytes': None,
                'uploaded_file_id': None
            }
            st.rerun()
        return

    # --- RESET SE NUOVO FILE ---
    current_file_id = f"{uploaded_file.name}_{uploaded_file.size}"
    if st.session_state.repair_state['uploaded_file_id'] != current_file_id:
        st.session_state.repair_state = {
            'processing_done': False,
            'file_name': uploaded_file.name,
            'file_bytes': uploaded_file.getvalue(),
            'mesh_after': None,
            'report_data': None,
            'pdf_bytes': None,
            'uploaded_file_id': current_file_id
        }

    # --- CONTROLLO PREVENTIVO: FORMATI NON-MESH ---
    file_name_check = st.session_state.repair_state['file_name']
    file_ext_check = os.path.splitext(file_name_check)[1].lower()
    if file_ext_check in NON_MESH_FORMATS:
        tipo = NON_MESH_FORMATS[file_ext_check]
        st.error(
            f"❌ **Formato non supportato per la riparazione.**\n\n"
            f"Il file `{file_ext_check}` è un file di **{tipo}**, non una mesh 3D. "
            f"La riparazione è disponibile solo per file di geometria 3D (STL, OBJ, PLY, GLB, GLTF, FBX, 3MF, DAE, WRL, OFF, U3D).\n\n"
            f"💡 Per lavorare con file {tipo}, usa la sezione **Converti Formati** o il **Viewer 3D**."
        )
        return

    # --- SE NON ELABORATO, ESEGUI ---
    if not st.session_state.repair_state['processing_done']:
        file_bytes = st.session_state.repair_state['file_bytes']
        file_name = st.session_state.repair_state['file_name']
        file_extension = os.path.splitext(file_name)[1].lower().replace('.', '')
        file_size_mb = len(file_bytes) / (1024 * 1024)

        # --- COMPONENTI UI ---
        progress_bar = st.progress(0, text="0%")

        # Riquadro informazioni tempo (messaggio onesto)
        time_info_placeholder = st.empty()
        time_info_placeholder.info(
            "⏱️ **Elaborazione in corso.** Il tempo di riparazione varia in base alla complessità del file "
            "(numero di vertici, facce, presenza di errori geometrici). Per file di grandi dimensioni "
            "l'operazione può richiedere **diversi minuti**. La pagina potrebbe non aggiornarsi per alcuni istanti, "
            "ma il processo è attivo. **Attendere prego.**"
        )

        st.markdown("##### 📋 Processi in corso")
        step_container = st.container()
        step_placeholders = {}

        steps = [
            ("ricezione", "📂 Ricezione del file"),
            ("lettura", "📖 Lettura struttura mesh"),
            ("analisi_iniziale", "🔍 Analisi iniziale"),
            ("rilevamento", "🔎 Rilevamento problemi geometrici"),
            ("riparazione", "🔧 Riparazione mesh"),
            ("analisi_finale", "📊 Analisi finale"),
            ("report", "📄 Generazione report"),
        ]

        with step_container:
            for key, label in steps:
                step_placeholders[key] = st.empty()
                step_placeholders[key].markdown(f"⏸️ {label}")

        # --- STEP 1: RICEZIONE ---
        progress_bar.progress(5, text="5%")
        step_placeholders["ricezione"].markdown(f"✅ 📂 Ricezione del file ({file_size_mb:.1f} MB)")
        time.sleep(0.3)

        # --- STEP 2: LETTURA ---
        progress_bar.progress(15, text="15%")
        step_placeholders["lettura"].markdown(f"🔄 📖 Lettura struttura mesh — in corso (0%)")
        time.sleep(0.3)

        try:
            mesh_before = load_3d_file_func(file_bytes, file_extension)
        except Exception as e:
            step_placeholders["lettura"].markdown(f"❌ 📖 Lettura fallita")
            st.error(f"❌ Errore durante la lettura del file: {str(e)}")
            return

        # --- CONTROLLO ROBUSTO: VERIFICA CHE SIA UNA MESH 3D VALIDA ---
        is_valid_mesh = (
            mesh_before is not None
            and hasattr(mesh_before, 'vertices')
            and hasattr(mesh_before, 'faces')
            and mesh_before.vertices is not None
            and mesh_before.faces is not None
            and len(mesh_before.vertices) > 0
            and len(mesh_before.faces) > 0
        )

        if not is_valid_mesh:
            step_placeholders["lettura"].markdown(f"❌ 📖 Lettura fallita")
            st.error(
                f"❌ **Impossibile riparare questo file.**\n\n"
                f"Il file `.{file_extension}` non contiene una mesh 3D valida con vertici e facce. "
                f"La riparazione è disponibile solo per file di geometria 3D.\n\n"
                f"💡 Formati supportati per la riparazione: **STL, OBJ, PLY, GLB, GLTF, FBX, 3MF, DAE, WRL, OFF, U3D**."
            )
            return

        step_placeholders["lettura"].markdown(
            f"✅ 📖 Lettura struttura mesh ({len(mesh_before.vertices):,} vertici, {len(mesh_before.faces):,} facce)"
        )

        # --- STEP 3: ANALISI INIZIALE ---
        progress_bar.progress(30, text="30%")
        step_placeholders["analisi_iniziale"].markdown(f"🔄 🔍 Analisi iniziale — in corso (0%)")
        time.sleep(0.3)

        report_before = analyze_mesh(mesh_before)

        step_placeholders["analisi_iniziale"].markdown(f"✅ 🔍 Analisi iniziale completata")
        progress_bar.progress(40, text="40%")
        time.sleep(0.2)

        # --- STEP 4: RILEVAMENTO ---
        step_placeholders["rilevamento"].markdown(f"🔄 🔎 Rilevamento problemi — in corso (0%)")
        time.sleep(0.3)

        problemi_totali = (
            report_before.get("non_manifold_edges", 0) +
            report_before.get("degenerate_faces", 0) +
            report_before.get("duplicate_vertices", 0) +
            report_before.get("holes", 0)
        )

        step_placeholders["rilevamento"].markdown(
            f"✅ 🔎 Rilevamento problemi ({problemi_totali:,} problemi trovati)"
        )
        progress_bar.progress(50, text="50%")
        time.sleep(0.2)

        # --- STEP 5: RIPARAZIONE ---
        step_placeholders["riparazione"].markdown(f"🔄 🔧 Riparazione mesh — in corso (0%)")
        time.sleep(0.3)

        mesh_after, actions = repair_mesh(mesh_before)

        step_placeholders["riparazione"].markdown(f"✅ 🔧 Riparazione mesh completata")
        progress_bar.progress(70, text="70%")
        time.sleep(0.3)

        # --- STEP 6: ANALISI FINALE ---
        step_placeholders["analisi_finale"].markdown(f"🔄 📊 Analisi finale — in corso (0%)")
        time.sleep(0.3)

        report_after = analyze_mesh(mesh_after)

        step_placeholders["analisi_finale"].markdown(f"✅ 📊 Analisi finale completata")
        progress_bar.progress(85, text="85%")
        time.sleep(0.2)

        # --- STEP 7: REPORT ---
        step_placeholders["report"].markdown(f"🔄 📄 Generazione report — in corso (0%)")
        time.sleep(0.3)

        report_data = generate_report_data(mesh_before, mesh_after, actions, lang=st.session_state.lang)
        pdf_bytes = generate_pdf_report(report_data, lang=st.session_state.lang)

        step_placeholders["report"].markdown(f"✅ 📄 Report generato")
        progress_bar.progress(100, text="100%")
        time.sleep(0.3)

        # Salva in session_state
        st.session_state.repair_state['processing_done'] = True
        st.session_state.repair_state['mesh_after'] = mesh_after
        st.session_state.repair_state['report_data'] = report_data
        st.session_state.repair_state['pdf_bytes'] = pdf_bytes

        st.rerun()

    # --- MOSTRA IL REPORT (dati già pronti) ---
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

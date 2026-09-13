# repair_page.py
# Logica completa per la pagina "Ripara File" con step-by-step progress (FASE A)

import streamlit as st
import trimesh
import os
import time
import io
from mesh_analyzer import analyze_mesh, repair_mesh, generate_report_data, generate_pdf_report
from translations import get_text


def estimate_processing_time(file_size_mb, vertices, faces):
    """
    Stima il tempo di elaborazione in secondi basandosi sulla complessità del file.
    Formula empirica basata su test reali.
    """
    # Fattori di peso (in secondi)
    time_io = file_size_mb * 0.5           # I/O del file
    time_vertices = (vertices / 10000) * 0.3  # Elaborazione vertici
    time_faces = (faces / 10000) * 0.5        # Elaborazione facce (più pesante)

    total = time_io + time_vertices + time_faces

    # Aggiungi un margine di sicurezza del 30%
    return max(10, int(total * 1.3))


def format_time(seconds):
    """Formatta i secondi in formato leggibile MM:SS o 'X minuti'."""
    if seconds < 60:
        return f"{seconds}s"
    else:
        minutes = seconds // 60
        secs = seconds % 60
        if secs > 0:
            return f"{minutes}m {secs}s"
        return f"{minutes} minuti"


def render_repair_page(load_3d_file_func, ALL_EXTENSIONS):
    """
    Renderizza l'intera pagina "Ripara File" con sistema step-by-step (FASE A).
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

    # --- SE NON ELABORATO, ESEGUI ---
    if not st.session_state.repair_state['processing_done']:
        file_bytes = st.session_state.repair_state['file_bytes']
        file_name = st.session_state.repair_state['file_name']
        file_extension = os.path.splitext(file_name)[1].lower().replace('.', '')
        file_size_mb = len(file_bytes) / (1024 * 1024)

        # --- STIMA TEMPO INIZIALE ---
        # Stima approssimativa basata sulla dimensione file
        # (verrà raffinata dopo il caricamento della mesh)
        estimated_initial = int(file_size_mb * 3)

        # --- COMPONENTI UI ---
        progress_bar = st.progress(0, text="0%")

        # Riquadro tempo stimato
        time_info_placeholder = st.empty()
        time_info_placeholder.info(f"⏱️ **Tempo stimato:** circa {format_time(estimated_initial)}. Il tempo effettivo dipende dalla complessità del file.")

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
        step_placeholders["lettura"].markdown(f"🔄 📖 Lettura struttura mesh — 0%")
        time.sleep(0.3)

        mesh_before = load_3d_file_func(file_bytes, file_extension)

        if mesh_before is None:
            step_placeholders["lettura"].markdown(f"❌ 📖 Lettura fallita")
            st.error(f"❌ Impossibile caricare il modello. Assicurati che il file sia un modello 3D valido.")
            return

        step_placeholders["lettura"].markdown(
            f"✅ 📖 Lettura struttura mesh ({len(mesh_before.vertices):,} vertici, {len(mesh_before.faces):,} facce)"
        )

        # --- RAFFINA STIMA TEMPO IN BASE AL CONTENUTO ---
        estimated_refined = estimate_processing_time(
            file_size_mb,
            len(mesh_before.vertices),
            len(mesh_before.faces)
        )
        time_info_placeholder.info(
            f"⏱️ **Tempo stimato:** circa {format_time(estimated_refined)}. "
            f"Basato su {len(mesh_before.vertices):,} vertici e {len(mesh_before.faces):,} facce."
        )

        # --- STEP 3: ANALISI INIZIALE ---
        progress_bar.progress(30, text="30%")
        step_placeholders["analisi_iniziale"].markdown(f"🔄 🔍 Analisi iniziale — 0%")
        time.sleep(0.2)
        step_placeholders["analisi_iniziale"].markdown(f"🔄 🔍 Analisi iniziale — 30%")
        time.sleep(0.2)
        step_placeholders["analisi_iniziale"].markdown(f"🔄 🔍 Analisi iniziale — 60%")
        time.sleep(0.2)

        report_before = analyze_mesh(mesh_before)

        step_placeholders["analisi_iniziale"].markdown(f"✅ 🔍 Analisi iniziale completata")
        progress_bar.progress(40, text="40%")
        time.sleep(0.2)

        # --- STEP 4: RILEVAMENTO ---
        step_placeholders["rilevamento"].markdown(f"🔄 🔎 Rilevamento problemi — 0%")
        time.sleep(0.2)
        step_placeholders["rilevamento"].markdown(f"🔄 🔎 Rilevamento problemi — 50%")
        time.sleep(0.2)

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

        # --- STEP 5: RIPARAZIONE (il più pesante) ---
        step_placeholders["riparazione"].markdown(f"🔄 🔧 Riparazione mesh — avvio...")

        # Messaggio onesto ma non allarmante
        st.info(
            "⏳ **Elaborazione in corso.** Questa è la fase più impegnativa. "
            "La pagina potrebbe non aggiornarsi per alcuni istanti mentre il server elabora la geometria. "
            "Attendere prego, il processo è attivo."
        )

        # Simulazione progressione visiva PRIMA dell'operazione bloccante
        step_placeholders["riparazione"].markdown(f"🔄 🔧 Riparazione mesh — 10%")
        time.sleep(0.3)
        step_placeholders["riparazione"].markdown(f"🔄 🔧 Riparazione mesh — 25%")
        time.sleep(0.3)

        # Operazione bloccante (Streamlit si ferma qui)
        mesh_after, actions = repair_mesh(mesh_before)

        step_placeholders["riparazione"].markdown(f"✅ 🔧 Riparazione mesh completata")
        progress_bar.progress(70, text="70%")
        time.sleep(0.3)

        # --- STEP 6: ANALISI FINALE ---
        step_placeholders["analisi_finale"].markdown(f"🔄 📊 Analisi finale — 0%")
        time.sleep(0.2)
        step_placeholders["analisi_finale"].markdown(f"🔄 📊 Analisi finale — 50%")
        time.sleep(0.2)

        report_after = analyze_mesh(mesh_after)

        step_placeholders["analisi_finale"].markdown(f"✅ 📊 Analisi finale completata")
        progress_bar.progress(85, text="85%")
        time.sleep(0.2)

        # --- STEP 7: REPORT ---
        step_placeholders["report"].markdown(f"🔄 📄 Generazione report — 0%")
        time.sleep(0.2)
        step_placeholders["report"].markdown(f"🔄 📄 Generazione report — 30%")
        time.sleep(0.2)

        report_data = generate_report_data(mesh_before, mesh_after, actions, lang=st.session_state.lang)
        step_placeholders["report"].markdown(f"🔄 📄 Generazione report — 70%")
        time.sleep(0.2)

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

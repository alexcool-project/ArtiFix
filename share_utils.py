"""
Utility per la condivisione di viewer HTML 3D su GitHub Pages.

Espone:
  - render_share_section(uploaded_file, t): pulsante + nota + form
  - handle_share_action(...): elabora file e pubblica viewer

Usato da 'Viewer 3D' in app.py.
"""
from __future__ import annotations

import os
import tempfile
from pathlib import Path

import streamlit as st


def render_share_info_tooltip(t) -> None:
    """Mostra la nota informativa (i) con spiegazione della condivisione."""
    with st.expander(t("share_info_tooltip"), expanded=False):
        st.markdown(f"### {t('share_info_title')}")
        st.markdown(t("share_info_body"))
        st.markdown("---")
        st.markdown(t("share_info_features"))
        st.markdown("---")
        st.markdown(t("share_info_use_cases"))


def handle_share_action(
    uploaded_file,
    project_title: str,
    generate_qr: bool,
    t,
) -> None:
    """Genera il viewer HTML e lo pubblica su GitHub Pages."""
    # Import lazy (solo quando serve)
    try:
        from mesh2u3d.io.mesh_reader import MeshReader
        from mesh2u3d.html.writer import mesh_to_html
        from mesh2u3d.share import share_html_viewer
    except ImportError as e:
        st.error(f"❌ Libreria `mesh2u3d` non disponibile: {e}")
        st.info(
            "💡 La libreria `mesh2u3d` deve essere installata. "
            "Se sei lo sviluppatore, controlla `requirements.txt`."
        )
        return

    progress = st.progress(0)
    status = st.empty()

    try:
        status.text(t("share_status_loading"))
        progress.progress(20)

        file_ext = os.path.splitext(uploaded_file.name)[1].lower()
        with tempfile.NamedTemporaryFile(suffix=file_ext, delete=False) as tmp:
            tmp.write(uploaded_file.getvalue())
            tmp_path = tmp.name

        try:
            mesh_data = MeshReader.read(tmp_path)
            status.text(
                t("share_status_processing").format(
                    v=mesh_data.vertex_count, f=mesh_data.triangle_count
                )
            )
            progress.progress(50)

            html_path = Path(tempfile.gettempdir()) / f"{mesh_data.name}.html"
            mesh_to_html(
                mesh_data,
                html_path,
                title=project_title or mesh_data.name,
                source_format=file_ext.replace(".", "").upper(),
            )
            status.text(t("share_status_publishing"))
            progress.progress(75)

            result = share_html_viewer(
                html_path,
                title=project_title or mesh_data.name,
                generate_qr=generate_qr,
            )
            progress.progress(100)
            status.text(t("share_status_done"))

        finally:
            try:
                os.unlink(tmp_path)
            except OSError:
                pass

        st.success(t("share_success"))

        # --- Risultato ---
        st.markdown("---")
        st.subheader(t("share_result_title"))

        st.markdown(f"**{t('share_result_url')}**")
        st.code(result["url"], language=None)

        st.markdown(
            f"""
            <div style="text-align:center;margin:10px 0;">
                <button onclick="navigator.clipboard.writeText('{result['url']}');this.textContent='✅ Copiato!';"
                        style="background:#1f77b4;color:white;padding:10px 24px;border:none;border-radius:8px;font-weight:600;cursor:pointer;font-size:14px;">
                    {t('share_copy_link')}
                </button>
            </div>
            """,
            unsafe_allow_html=True,
        )

        if result.get("qr_path"):
            st.markdown("---")
            st.subheader(t("share_qr_title"))
            st.image(result["qr_path"], width=250, caption=t("share_qr_caption"))

            with open(result["qr_path"], "rb") as f:
                st.download_button(
                    t("share_download_qr"),
                    data=f.read(),
                    file_name=f"{result['viewer_id']}_qr.png",
                    mime="image/png",
                    use_container_width=True,
                )

        st.info(t("share_info_id").format(id=result["viewer_id"]))

    except Exception as e:
        progress.empty()
        status.empty()
        st.error(t("share_error").format(error=str(e)))
        with st.expander("🔍 Dettagli errore", expanded=False):
            st.exception(e)


def render_share_section(uploaded_file, t) -> None:
    """
    Renderizza la sezione di condivisione sotto il viewer.

    Layout:
      [i] 📤 Condividi con il tuo cliente
      (al click su i → si apre la nota informativa)
      [NOME PROGETTO] [☑ QR Code]
      [🚀 Genera link condivisibile]
    """
    st.markdown("---")

    # Titolo + icona (i)
    st.markdown(f"### {t('share_button')}")

    # Nota informativa (apre al click)
    render_share_info_tooltip(t)

    # Form di condivisione
    col1, col2 = st.columns([3, 1])
    with col1:
        base_name = os.path.splitext(uploaded_file.name)[0]
        project_title = st.text_input(
            t("share_project_title"),
            value=base_name,
            key="share_project_title",
        )
    with col2:
        generate_qr = st.checkbox(
            t("share_generate_qr"),
            value=True,
            key="share_generate_qr",
        )

    if st.button(
        t("share_generate_button"),
        type="primary",
        use_container_width=True,
        key="share_generate_button",
    ):
        handle_share_action(uploaded_file, project_title, generate_qr, t)

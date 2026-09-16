"""
Utility per la condivisione di viewer HTML 3D e PDF 3D su GitHub Pages.

Usa la libreria `mesh2u3d` per generare:
  - Viewer HTML 3D autonomi (three.js)
  - PDF 3D con U3D embedded (compatibile Foxit, PDF-XChange)

Espone:
  - render_share_section(uploaded_file, t, lang): pulsante + nota + form
  - handle_share_action(...): elabora file e genera l'output scelto

Usato da 'Viewer 3D' in app.py.
"""
from __future__ import annotations

import html
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


def _render_copy_button(url: str, label: str, t) -> None:
    """Renderizza un pulsante 'Copia link' con feedback visivo tradotto."""
    safe_url = html.escape(url, quote=True)
    clean_label = label.replace("📋 ", "").replace(" 📋", "").strip()
    display_label = f"📋 {clean_label}" if clean_label else "📋 Copia link"

    copied_text = t("share_copy_success")
    error_text = t("share_copy_error")

    copy_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        html, body {{
            width: 100%;
            height: 100%;
            background: transparent;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
        }}
        .copy-btn {{
            display: inline-flex;
            align-items: center;
            justify-content: center;
            gap: 8px;
            width: 100%;
            padding: 12px 24px;
            background: #1f77b4;
            color: #ffffff;
            border: none;
            border-radius: 8px;
            font-size: 15px;
            font-weight: 600;
            cursor: pointer;
            transition: background 0.2s ease, transform 0.1s ease;
        }}
        .copy-btn:hover {{ background: #155a8a; }}
        .copy-btn:active {{ transform: scale(0.98); }}
        .copy-btn.copied {{ background: #2ecc71; }}
    </style>
    </head>
    <body>
    <button class="copy-btn" id="copyBtn" onclick="copyLink()">
        <span id="btnText">{display_label}</span>
    </button>

    <script>
        function copyLink() {{
            const url = "{safe_url}";
            const btn = document.getElementById('copyBtn');
            const txt = document.getElementById('btnText');

            if (navigator.clipboard && window.isSecureContext) {{
                navigator.clipboard.writeText(url).then(() => {{
                    showSuccess();
                }}).catch(err => {{
                    fallbackCopy(url);
                }});
            }} else {{
                fallbackCopy(url);
            }}

            function fallbackCopy(text) {{
                const ta = document.createElement('textarea');
                ta.value = text;
                ta.style.position = 'fixed';
                ta.style.opacity = '0';
                document.body.appendChild(ta);
                ta.select();
                try {{
                    document.execCommand('copy');
                    showSuccess();
                }} catch (err) {{
                    txt.textContent = '{error_text}';
                }}
                document.body.removeChild(ta);
            }}

            function showSuccess() {{
                btn.classList.add('copied');
                txt.textContent = '{copied_text}';
                setTimeout(() => {{
                    btn.classList.remove('copied');
                    txt.textContent = '{display_label}';
                }}, 2500);
            }}
        }}
    </script>
    </body>
    </html>
    """

    st.components.v1.html(copy_html, height=60)


def handle_share_action(
    uploaded_file,
    project_title: str,
    generate_qr: bool,
    output_format: str,
    t,
    lang: str = "it",
) -> None:
    """
    Genera il file (HTML o PDF-U3D) e lo fornisce all'utente.

    Parameters
    ----------
    uploaded_file : file caricato
    project_title : titolo del progetto
    generate_qr : se generare QR code (solo per HTML)
    output_format : "html" | "pdf_u3d"
    t : funzione di traduzione
    lang : lingua ("it" o "en")
    """
    try:
        from mesh2u3d.io.mesh_reader import MeshReader
        from mesh2u3d.html.writer import mesh_to_html
        from mesh2u3d.u3d.writer import mesh_to_u3d
        from mesh2u3d.pdf.embedder import embed_u3d_in_pdf
        from mesh2u3d.share import share_html_viewer
    except ImportError as e:
        st.error(f"❌ Libreria `mesh2u3d` non disponibile: {e}")
        st.info("💡 Controlla `requirements.txt`.")
        return

    progress = st.progress(0)
    status = st.empty()

    try:
        # Step 1 — Leggi mesh
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

            # Step 2 — Genera file in base al formato scelto
            if output_format == "html":
                # --- HTML 3D (viewer three.js) ---
                html_path = Path(tempfile.gettempdir()) / f"{mesh_data.name}.html"
                mesh_to_html(
                    mesh_data,
                    html_path,
                    title=project_title or mesh_data.name,
                    source_format=file_ext.replace(".", "").upper(),
                    lang=lang,
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

            elif output_format == "pdf_u3d":
                # --- PDF con U3D embedded (Foxit, PDF-XChange) ---
                with tempfile.NamedTemporaryFile(suffix=".u3d", delete=False) as tmp_u3d:
                    tmp_u3d_path = Path(tmp_u3d.name)
                try:
                    mesh_to_u3d(mesh_data, str(tmp_u3d_path))
                    pdf_path = Path(tempfile.gettempdir()) / f"{mesh_data.name}_u3d.pdf"
                    embed_u3d_in_pdf(
                        tmp_u3d_path,
                        pdf_path,
                        title=project_title or mesh_data.name,
                    )
                finally:
                    try:
                        tmp_u3d_path.unlink()
                    except OSError:
                        pass

                result = {
                    "url": None,
                    "qr_path": None,
                    "viewer_id": "pdf_u3d",
                    "pdf_path": str(pdf_path),
                    "file_name": f"{project_title or mesh_data.name}.pdf",
                }
                progress.progress(100)
                status.text(t("share_status_done"))

            else:
                st.error(f"❌ Formato non supportato: {output_format}")
                return

        finally:
            try:
                os.unlink(tmp_path)
            except OSError:
                pass

        # --- Mostra risultato ---
        if output_format == "html":
            # Link + QR (comportamento originale)
            st.success(t("share_success"))
            st.warning(t("share_warning_propagation"))
            st.markdown("---")
            st.subheader(t("share_result_title"))
            st.markdown(f"**{t('share_result_url')}**")
            st.code(result["url"], language=None)
            _render_copy_button(result["url"], t("share_copy_link"), t)

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

        else:
            # PDF: solo download
            st.success(t("share_success"))
            st.markdown("---")
            st.subheader(t("share_result_title"))

            with open(result["pdf_path"], "rb") as f:
                pdf_bytes = f.read()

            st.download_button(
                label=f"📥 {t('share_download_pdf')}",
                data=pdf_bytes,
                file_name=result["file_name"],
                mime="application/pdf",
                use_container_width=True,
            )

    except Exception as e:
        progress.empty()
        status.empty()
        st.error(t("share_error").format(error=str(e)))
        with st.expander("🔍 Dettagli errore", expanded=False):
            st.exception(e)


def render_share_section(uploaded_file, t, lang: str = "it") -> None:
    """
    Renderizza la sezione di condivisione sotto il viewer.

    Parameters
    ----------
    uploaded_file : file caricato dall'utente
    t : funzione di traduzione
    lang : lingua corrente ("it" o "en")
    """
    st.markdown("---")
    st.markdown(f"### {t('share_button')}")
    render_share_info_tooltip(t)

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

    # --- Selettore formato di output (senza PRC) ---
    st.markdown(f"**{t('share_format_label')}**")
    output_format = st.radio(
        t("share_format_label"),
        options=["html", "pdf_u3d"],
        format_func=lambda x: {
            "html": t("share_format_html"),
            "pdf_u3d": t("share_format_pdf_u3d"),
        }[x],
        index=0,
        key="share_output_format",
        label_visibility="collapsed",
    )

    if st.button(
        t("share_generate_button"),
        type="primary",
        use_container_width=True,
        key="share_generate_button",
    ):
        handle_share_action(
            uploaded_file,
            project_title,
            generate_qr,
            output_format,
            t,
            lang=lang,
        )

"""
Utility per la condivisione di viewer HTML 3D su GitHub Pages.

Usa la libreria `mesh2u3d` per generare viewer HTML 3D autonomi (three.js)
con pulsante per la generazione del report PDF.

Espone:
  - render_share_section(uploaded_file, t, lang): pulsante + nota + form
  - handle_share_action(...): elabora file e pubblica viewer

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
    t,
    lang: str = "it",
) -> None:
    """
    Genera il viewer HTML e lo pubblica su GitHub Pages.
    """
    try:
        from mesh2u3d.io.mesh_reader import MeshReader
        from mesh2u3d.html.writer import mesh_to_html
        from mesh2u3d.share import share_html_viewer
    except ImportError as e:
        st.error(f"❌ Libreria `mesh2u3d` non disponibile: {e}")
        st.info("💡 Controlla `requirements.txt`.")
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
                lang=lang,
            )

            if html_path.exists():
                html_code = html_path.read_text(encoding="utf-8")
                
                jspdf_cdn = '<script src="https://cdnjs.cloudflare.com/ajax/libs/jspdf/2.5.1/jspdf.umd.min.js"></script>'
                if "</head>" in html_code:
                    html_code = html_code.replace("</head>", f"{jspdf_cdn}</head>")

                clean_title = (project_title or mesh_data.name).replace("'", "\\'")
                fmt_str = file_ext.replace(".", "").upper()
                v_count = f"{mesh_data.vertex_count:,}".replace(",", ".")
                f_count = f"{mesh_data.triangle_count:,}".replace(",", ".")

                pdf_script = f"""
                <script>
                window.addEventListener('DOMContentLoaded', () => {{
                    setTimeout(() => {{
                        const buttons = document.querySelectorAll('button, a');
                        buttons.forEach(el => {{
                            if (el.innerText && (el.innerText.includes('HTML') || el.innerText.includes('Scarica') || el.innerText.includes('PDF') || el.innerText.includes('foto'))) {{
                                el.innerHTML = '📄 Scarica PDF';
                                el.title = 'Scarica Report Tecnico PDF ArtiFix';
                                
                                const newBtn = el.cloneNode(true);
                                el.parentNode.replaceChild(newBtn, el);
                                
                                newBtn.addEventListener('click', (e) => {{
                                    e.preventDefault();
                                    e.stopPropagation();
                                    
                                    if (typeof window.jspdf === 'undefined') {{
                                        alert('Generatore PDF in caricamento, riprova tra un istante.');
                                        return;
                                    }}

                                    if (typeof renderer !== 'undefined' && typeof scene !== 'undefined' && typeof camera !== 'undefined') {{
                                        renderer.render(scene, camera);
                                    }}

                                    const canvas = document.querySelector('canvas');
                                    if (!canvas) {{
                                        alert('Canvas 3D non trovato.');
                                        return;
                                    }}

                                    const imgData = canvas.toDataURL('image/png');
                                    const {{ jsPDF }} = window.jspdf;
                                    const doc = new jsPDF();

                                    doc.setTextColor(15, 23, 42);
                                    doc.setFontSize(22);
                                    doc.setFont('helvetica', 'bold');
                                    doc.text('ARTIFIX', 14, 20);

                                    doc.setFontSize(9);
                                    doc.setFont('helvetica', 'normal');
                                    doc.setTextColor(100, 116, 139);
                                    doc.text('CONVERT. FIX. DELIVER.', 14, 26);

                                    doc.setFontSize(10);
                                    doc.setFont('helvetica', 'bold');
                                    doc.text('REPORT TECNICO 3D', 145, 20);

                                    doc.setDrawColor(226, 232, 240);
                                    doc.setLineWidth(0.5);
                                    doc.line(14, 32, 196, 32);

                                    doc.setTextColor(30, 41, 59);
                                    doc.setFontSize(12);
                                    doc.setFont('helvetica', 'bold');
                                    doc.text('PROGETTO: {clean_title}', 14, 42);

                                    doc.setFontSize(10);
                                    doc.setFont('helvetica', 'normal');
                                    doc.text('Formato: {fmt_str}', 14, 52);
                                    doc.text('Vertici: {v_count}', 75, 52);
                                    doc.text('Triangoli: {f_count}', 135, 52);

                                    doc.line(14, 58, 196, 58);

                                    doc.setFont('helvetica', 'bold');
                                    doc.text('Vista 3D Renderizzata', 14, 68);
                                    
                                    doc.addImage(imgData, 'PNG', 14, 74, 182, 110);

                                    doc.line(14, 275, 196, 275);
                                    doc.setFontSize(8);
                                    doc.setFont('helvetica', 'normal');
                                    doc.setTextColor(148, 163, 184);
                                    doc.text('Documento generato automaticamente via ArtiFix 3D Viewer | www.artifix.it', 14, 282);

                                    doc.save('ArtiFix_Report_{clean_title}.pdf');
                                }});
                            }}
                        }});
                    }}, 1000);
                }});
                </script>
                """

                if "</body>" in html_code:
                    html_code = html_code.replace("</body>", pdf_script)
                    html_path.write_text(html_code, encoding="utf-8")

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

    except Exception as e:
        progress.empty()
        status.empty()
        st.error(t("share_error").format(error=str(e)))
        with st.expander("🔍 Dettagli errore", expanded=False):
            st.exception(e)


def render_share_section(uploaded_file, t, lang: str = "it") -> None:
    """
    Renderizza la sezione di condivisione sotto il viewer.
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
            t,
            lang=lang,
        )

"""
Utility per la condivisione di viewer HTML 3D su GitHub Pages.

Usa la libreria `mesh2u3d` per generare viewer HTML 3D autonomi (three.js)
con pulsante per la generazione del report PDF formale e loghi ufficiali ArtiFix.

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

    Parameters
    ----------
    uploaded_file : file caricato
    project_title : titolo del progetto
    generate_qr : se generare QR code
    t : funzione di traduzione
    lang : lingua ("it" o "en")
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
    status

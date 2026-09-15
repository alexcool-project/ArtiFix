"""
Utility per la condivisione di viewer HTML 3D su GitHub Pages.

Usa la libreria `mesh2u3d` per generare un viewer HTML 3D autonomo
(con logo ArtiFix, controlli avanzati, trasparenze, X-Ray, ecc.)
e lo pubblica su GitHub Pages.

Espone:
  - render_share_section(uploaded_file, t): pulsante + nota + form
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


def _render_copy_button(url: str, label: str) -> None:
    """Renderizza un pulsante 'Copia link' con feedback visivo."""
    safe_url = html.escape(url, quote=True)

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
        <span id="btnText">📋 {label}</span>
    </button>

    <script>
        function copyLink() {{
            const

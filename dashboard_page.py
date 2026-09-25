# dashboard_page.py
# Pagina Dashboard di ArtiFix — carica metriche dinamiche da Google Sheets
# Author: Alessandro (ArtiFix) — v1.0 — 25 Set 2026

"""
Modulo per la pagina "Dashboard" di ArtiFix.

Legge le metriche dal foglio Google "Metriche ArtiFix" tramite Service Account,
con cache di 5 minuti. In caso di errore, fallback ai valori hardcoded storici.

Espone:
    render_dashboard_page(t, lang, supported_formats, logo_url)

Usato da 'Dashboard' in app.py.
"""

from __future__ import annotations

from datetime import datetime

import gspread
import streamlit as st
from google.oauth2.service_account import Credentials


# ============================================================
# COSTANTI
# ============================================================

SCOPES = ["https://www.googleapis.com/auth/spreadsheets.readonly"]

# Fallback valori hardcoded (se il foglio non è raggiungibile)
FALLBACK_METRICS = {
    "file_riparati": {"value": "14,280", "unit": "", "icon": "🛠️"},
    "conversioni": {"value": "38,910", "unit": "", "icon": "🔄"},
    "formati_supportati": {"value": "50", "unit": "+", "icon": "📁"},
    "status": {"value": "Online", "unit": "", "icon": "🟢"},
    "uptime_30d": {"value": "99.8", "unit": "%", "icon": "⏱️"},
}


# ============================================================
# CARICAMENTO DATI
# ============================================================

@st.cache_resource(show_spinner=False)
def _get_gspread_client():
    """
    Restituisce un client gspread autorizzato con il Service Account.

    Usa @st.cache_resource perché il client va creato una sola volta
    (connection pooling) e riutilizzato tra le sessioni.
    """
    try:
        creds_dict = dict(st.secrets["gcp_service_account"])
    except (KeyError, FileNotFoundError) as e:
        raise RuntimeError(
            "Sezione [gcp_service_account] mancante nei secrets."
        ) from e

    creds = Credentials.from_service_account_info(creds_dict, scopes=SCOPES)
    return gspread.authorize(creds)


@st.cache_data(ttl=300, show_spinner=False)
def load_metrics() -> dict:
    """
    Legge le metriche dal foglio Google.

    Returns
    -------
    dict
        Dizionario {metric_name: {"value": str, "unit": str, "icon": str}}
        In caso di errore, restituisce FALLBACK_METRICS e setta
        `_load_error` con il messaggio di errore.

    Note
    ----
    - Cache: 5 minuti (`ttl=300`)
    - Sheet ID e nome worksheet presi da `st.secrets["metrics"]`
    - Colonne attese: metric_name | value | unit | icon
    """
    result: dict = {}
    error: str | None = None

    try:
        sheet_id = st.secrets["metrics"]["sheet_id"]
        worksheet_name = st.secrets["metrics"].get("worksheet_name", "metriche")

        client = _get_gspread_client()
        sh = client.open_by_key(sheet_id)
        ws = sh.worksheet(worksheet_name)

        # Legge tutte le righe come lista di dict (header in riga 1)
        records = ws.get_all_records()

        for row in records:
            name = str(row.get("metric_name", "")).strip()
            if not name:
                continue

            value = row.get("value", "")
            unit = str(row.get("unit", "")).strip()
            icon = str(row.get("icon", "")).strip()

            # Formatta value: se numerico intero, aggiunge separatore migliaia
            try:
                value_num = int(str(value).replace(",", "").replace(".", "").strip())
                value_str = f"{value_num:,}".replace(",", ".")
            except (ValueError, TypeError):
                value_str = str(value).strip()

            result[name] = {
                "value": value_str,
                "unit": unit,
                "icon": icon,
            }

    except Exception as e:
        error = str(e)

    # Fallback se vuoto o errore
    if not result:
        result = FALLBACK_METRICS.copy()
        result["_load_error"] = error or "Nessun dato ricevuto dal foglio."

    return result


# ============================================================
# COMPONENTI UI
# ============================================================

def _render_metric_card(col, value: str, unit: str, icon: str, label: str) -> None:
    """
    Renderizza una singola card metrica (HTML+CSS).

    Parameters
    ----------
    col : streamlit column
        Colonna Streamlit dove renderizzare la card.
    value : str
        Valore da mostrare (es. "14.280")
    unit : str
        Suffisso (es. "+", "%"). Vuoto se non serve.
    icon : str
        Emoji dell'icona (es. "🛠️")
    label : str
        Etichetta sotto il valore (es. "File Riparati")
    """
    display_value = f"{icon} {value}{unit}" if icon else f"{value}{unit}"

    col.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-value">{value}{unit}</div>
            <div class="metric-label">{label}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def _render_formats_grid(supported_formats: dict) -> None:
    """
    Renderizza la griglia dei formati supportati (4 colonne).

    Parameters
    ----------
    supported_formats : dict
        Dizionario SUPPORTED_FORMATS da app.py
        (categoria → {"icon", "description", "extensions"})
    """
    cols = st.columns(4)
    for idx, (category, info) in enumerate(supported_formats.items()):
        with cols[idx % 4]:
            st.markdown(
                f"""
                <div style="background:#f8f9fa;padding:0.7rem;border-radius:10px;border-left:3px solid #1f77b4;">
                    <div style="font-weight:600;">{info["icon"]} {category}</div>
                    <div style="font-size:0.8rem;color:#666;">{info["description"]}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )


# ============================================================
# ENTRY POINT
# ============================================================

def render_dashboard_page(
    t,
    lang: str,
    supported_formats: dict,
    logo_url: str,
) -> None:
    """
    Renderizza l'intera pagina Dashboard.

    Parameters
    ----------
    t : callable
        Funzione di traduzione `t(key)` di app.py
    lang : str
        Lingua corrente ("it" o "en")
    supported_formats : dict
        SUPPORTED_FORMATS da app.py
    logo_url : str
        URL del logo ArtiFix
    """
    # --- Logo centrato ---
    st.markdown(
        f'<div class="logo-container"><img src="{logo_url}" alt="Logo ArtiFix"></div>',
        unsafe_allow_html=True,
    )

    # --- Header ---
    st.header(t("dash_header"))

    # --- Metriche dinamiche ---
    metrics = load_metrics()

    # Nota se dati di fallback
    if "_load_error" in metrics:
        st.warning(t("dash_error_load"))

    # --- 4 metric card principali ---
    metric_order = [
        ("file_riparati", "dash_metric_repaired"),
        ("conversioni", "dash_metric_conversions"),
        ("formati_supportati", "dash_metric_formats"),
        ("status", "dash_metric_online"),
    ]

    cols = st.columns(4)
    for col, (metric_key, label_key) in zip(cols, metric_order):
        m = metrics.get(metric_key, FALLBACK_METRICS.get(metric_key, {}))
        _render_metric_card(
            col=col,
            value=str(m.get("value", "—")),
            unit=str(m.get("unit", "")),
            icon=str(m.get("icon", "")),
            label=t(label_key),
        )

    # --- Riga extra: uptime + ultimo aggiornamento ---
    if "uptime_30d" in metrics:
        st.markdown("")
        cols_extra = st.columns(4)
        with cols_extra[0]:
            m_uptime = metrics["uptime_30d"]
            _render_metric_card(
                col=cols_extra[0],
                value=str(m_uptime.get("value", "—")),
                unit=str(m_uptime.get("unit", "")),
                icon=str(m_uptime.get("icon", "⏱️")),
                label=t("dash_metric_uptime"),
            )

    # --- Separatore ---
    st.markdown("---")

    # --- Griglia formati supportati ---
    st.subheader(t("dash_supported_formats"))
    _render_formats_grid(supported_formats)

    # --- Info finale ---
    st.info(t("dash_info_select"))

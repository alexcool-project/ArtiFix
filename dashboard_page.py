# dashboard_page.py
# Pagina Dashboard di ArtiFix — carica metriche dinamiche da Google Sheets
# Author: Alessandro (ArtiFix) — v1.4 — 26 Set 2026
#
# Changelog v1.2:
#   - Aggiunta metrica "Sponsor attivi" (foglio Artifix_Sponsors)
#   - Aggiunta metrica "Ultimo aggiornamento" (foglio Metriche ArtiFix)
#   - Aggiunta metrica "Ultimo deploy" (GitHub API, repo pubblico Artifix)
#   - Timestamp solo data: "%d/%m/%Y" (rimosso orario)

"""
Modulo per la pagina "Dashboard" di ArtiFix.

Legge le metriche da:
  - Foglio Google "Metriche ArtiFix" (via Service Account)
  - Foglio Google "Artifix_Sponsors" (via Service Account)
  - GitHub API (repo pubblico alexcool-project/Artifix)

Cache: 5 minuti. In caso di errore, fallback ai valori hardcoded.

Espone:
    render_dashboard_page(t, lang, supported_formats, logo_url)
"""

from __future__ import annotations

from datetime import datetime

import gspread
import requests
import streamlit as st
from google.oauth2.service_account import Credentials


# ============================================================
# COSTANTI
# ============================================================

SCOPES = ["https://www.googleapis.com/auth/spreadsheets.readonly"]

# ID fogli Google
SPONSORS_SHEET_ID = "16m8gY3YktT2ysYAkKqHGC28VX1qGghx6PL2typXK2b4"

# GitHub repo (pubblico)
GITHUB_REPO = "alexcool-project/Artifix"
GITHUB_BRANCH = "main"

# Fallback valori hardcoded (se i fogli non sono raggiungibili)
FALLBACK_METRICS = {
    "file_riparati": {"value": "14.280", "unit": "", "icon": "🛠️"},
    "conversioni": {"value": "38.910", "unit": "", "icon": "🔄"},
    "formati_supportati": {"value": "50", "unit": "+", "icon": "📁"},
    "status": {"value": "Online", "unit": "", "icon": "🟢"},
    "uptime_30d": {"value": "99.8", "unit": "%", "icon": "⏱️"},
    "sponsor_attivi": {"value": "3", "unit": "", "icon": "🤝"},
}


# ============================================================
# UTILITY FORMATTAZIONE
# ============================================================

def _format_value(raw_value) -> str:
    """
    Formatta un valore grezzo dal foglio Google in stringa visibile.
    """
    value_str = str(raw_value).strip()
    if not value_str:
        return ""

    normalized = value_str.replace(",", "")

    if "." in normalized:
        try:
            value_float = float(normalized)
            formatted = f"{value_float:.2f}".rstrip("0").rstrip(".")
            return formatted.replace(".", ",")
        except (ValueError, TypeError):
            pass

    try:
        value_int = int(normalized)
        return f"{value_int:,}".replace(",", ".")
    except (ValueError, TypeError):
        pass

    return value_str


def _format_timestamp(raw_value) -> str:
    """
    Formatta un timestamp ISO/italiano in stringa compatta (solo data).

    v1.4: formato "%d/%m/%Y" (senza orario).

    Esempi:
    - "2026-09-26 12:11:11" → "26/09/2026"
    - "2026-09-26T12:11:11Z" → "26/09/2026"
    """
    if not raw_value:
        return "—"

    s = str(raw_value).strip()
    if not s:
        return "—"

    for fmt in (
        "%Y-%m-%d %H:%M:%S",
        "%Y-%m-%dT%H:%M:%S",
        "%Y-%m-%dT%H:%M:%SZ",
        "%Y-%m-%dT%H:%M:%S.%fZ",
        "%Y-%m-%d",
    ):
        try:
            dt = datetime.strptime(s[:len(fmt) + 6], fmt)
            return dt.strftime("%d/%m/%Y")
        except (ValueError, TypeError):
            continue

    return s


# ============================================================
# CARICAMENTO DATI
# ============================================================

@st.cache_resource(show_spinner=False)
def _get_gspread_client():
    """
    Restituisce un client gspread autorizzato con il Service Account.
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
    Legge le metriche dal foglio Google "Metriche ArtiFix".
    """
    result: dict = {}
    error: str | None = None

    try:
        sheet_id = st.secrets["metrics"]["sheet_id"]
        worksheet_name = st.secrets["metrics"].get("worksheet_name", "metriche")

        client = _get_gspread_client()
        sh = client.open_by_key(sheet_id)
        ws = sh.worksheet(worksheet_name)

        records = ws.get_all_records()

        for row in records:
            name = str(row.get("metric_name", "")).strip()
            if not name:
                continue

            value = row.get("value", "")
            unit = str(row.get("unit", "")).strip()
            icon = str(row.get("icon", "")).strip()

            if name == "ultimo_aggiornamento":
                value_str = _format_timestamp(value)
            else:
                value_str = _format_value(value)

            result[name] = {
                "value": value_str,
                "unit": unit,
                "icon": icon,
            }

    except Exception as e:
        error = str(e)

    if not result:
        result = FALLBACK_METRICS.copy()
        result["_load_error"] = error or "Nessun dato ricevuto dal foglio."

    return result


@st.cache_data(ttl=300, show_spinner=False)
def load_sponsors_attivi() -> int | None:
    """
    Conta gli sponsor attivi dal foglio "Artifix_Sponsors".
    """
    try:
        client = _get_gspread_client()
        sh = client.open_by_key(SPONSORS_SHEET_ID)
        ws = sh.sheet1

        records = ws.get_all_records()
        count = 0
        for row in records:
            attivo = str(row.get("ATTIVO", "")).strip().upper()
            if attivo in ("TRUE", "1", "SI", "SÌ"):
                count += 1
        return count
    except Exception:
        return None


@st.cache_data(ttl=300, show_spinner=False)
def load_ultimo_deploy() -> dict | None:
    """
    Recupera l'ultimo commit su main dal repo pubblico Artifix.
    """
    try:
        url = f"https://api.github.com/repos/{GITHUB_REPO}/commits/{GITHUB_BRANCH}"
        r = requests.get(url, timeout=5)
        if r.status_code != 200:
            return None

        data = r.json()
        commit = data.get("commit", {})
        return {
            "sha": data.get("sha", "")[:7],
            "data": commit.get("committer", {}).get("date", ""),
            "messaggio": commit.get("message", "").split("\n")[0][:60],
        }
    except Exception:
        return None


# ============================================================
# COMPONENTI UI
# ============================================================

def _render_metric_card(col, value: str, unit: str, icon: str, label: str) -> None:
    """
    Renderizza una singola card metrica (HTML+CSS).
    """
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
    """
    st.markdown(
        f'<div class="logo-container"><img src="{logo_url}" alt="Logo ArtiFix"></div>',
        unsafe_allow_html=True,
    )

    st.header(t("dash_header"))

    metrics = load_metrics()
    if "_load_error" in metrics:
        st.warning(t("dash_error_load"))

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

    st.markdown("")
    cols_extra = st.columns(4)

    with cols_extra[0]:
        m_uptime = metrics.get("uptime_30d", FALLBACK_METRICS["uptime_30d"])
        _render_metric_card(
            col=cols_extra[0],
            value=str(m_uptime.get("value", "—")),
            unit=str(m_uptime.get("unit", "")),
            icon=str(m_uptime.get("icon", "⏱️")),
            label=t("dash_metric_uptime"),
        )

    with cols_extra[1]:
        n_sponsor = load_sponsors_attivi()
        sponsor_value = str(n_sponsor) if n_sponsor is not None else "3"
        _render_metric_card(
            col=cols_extra[1],
            value=sponsor_value,
            unit="",
            icon="🤝",
            label=t("dash_metric_sponsors"),
        )

    with cols_extra[2]:
        m_ultimo_agg = metrics.get("ultimo_aggiornamento", {"value": "—"})
        _render_metric_card(
            col=cols_extra[2],
            value=str(m_ultimo_agg.get("value", "—")),
            unit="",
            icon="🕒",
            label=t("dash_metric_last_update"),
        )

    with cols_extra[3]:
        deploy = load_ultimo_deploy()
        if deploy:
            deploy_value = deploy["sha"]
            deploy_label = t("dash_metric_last_deploy")
        else:
            deploy_value = "—"
            deploy_label = t("dash_metric_last_deploy")

        _render_metric_card(
            col=cols_extra[3],
            value=deploy_value,
            unit="",
            icon="🚀",
            label=deploy_label,
        )
        if deploy and deploy.get("messaggio"):
            cols_extra[3].caption(f"_{deploy['messaggio']}_")

    st.markdown("---")
    st.subheader(t("dash_supported_formats"))
    _render_formats_grid(supported_formats)

    st.info(t("dash_info_select"))

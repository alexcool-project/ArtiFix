"""
ArtiFix — Dashboard stato sistema (B.6)
Pagina multi-page nativa Streamlit.
Legge il foglio ArtiFix_Roadmap via Service Account (gspread).
NON tocca l'app v7.4 in app.py.

Changelog:
  - v1.1 (26 Set 2026): aggiunto pulsante "Torna in ArtiFix" compatto in sidebar
"""
from __future__ import annotations

import re
import streamlit as st
import gspread
import pandas as pd
from google.oauth2.service_account import Credentials

# ============================================================
# CONFIG
# ============================================================
SHEET_ID = "1JnswXoOgmKa3ebrmWAkxtSA9v6oOTgyNgbEp8K8VwIg"
SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.readonly",
]

TAB_CONFIG      = "Config"
TAB_ROADMAP     = "Roadmap"
TAB_LOG_FREEZE  = "Log_Freeze"
TAB_LOG_VERIFY  = "Log_Verify"
TAB_LOG_ERRORS  = "Log_Errors"
TAB_QUEUE       = "Queue"

FASI_ATTESE = [f"B.{i}" for i in range(1, 9)]
STATI_DONE_KW = {"done", "completato", "completata", "fatto"}
STATI_WIP_KW  = {"in corso", "wip", "corso", "progress"}
STATI_TODO_KW = {"to do", "todo", "da fare", "todo."}
_FASE_RE = re.compile(r"\b(B\.\d+)\b", re.IGNORECASE)

# ⚠️ NIENTE st.set_page_config qui: c'è già in app.py (pagina principale)

# ============================================================
# SIDEBAR — Pulsante ritorno all'app principale (compatto)
# ============================================================
with st.sidebar:
    st.markdown(
        """
        <a href="https://artifix.streamlit.app" target="_self"
           style="display:block; text-align:center; background:#1f77b4;
                  color:white; padding:8px 12px; border-radius:6px;
                  text-decoration:none; font-weight:600; font-size:13px;
                  white-space:nowrap; overflow:hidden; text-overflow:ellipsis;
                  margin-bottom:16px;">
            🏠 Torna in ArtiFix
        </a>
        """,
        unsafe_allow_html=True,
    )
    st.markdown("---")
    st.caption("🛠️ Dashboard Sistema")
    st.caption("Stato sistema in tempo reale")

# ============================================================
# GOOGLE SHEETS
# ============================================================
@st.cache_resource(show_spinner=False)
def _get_client() -> gspread.Client:
    creds = Credentials.from_service_account_info(
        dict(st.secrets["gcp_service_account"]), scopes=SCOPES
    )
    return gspread.authorize(creds)


@st.cache_resource(show_spinner=False)
def _get_spreadsheet() -> gspread.Spreadsheet:
    return _get_client().open_by_key(SHEET_ID)


@st.cache_data(ttl=60, show_spinner=False)
def leggi_config() -> dict[str, str]:
    """Config è key/value: ritorna {Chiave: Valore}."""
    rows = _get_spreadsheet().worksheet(TAB_CONFIG).get_all_values()
    out: dict[str, str] = {}
    for row in rows[1:]:
        if not row or not row[0].strip():
            continue
        out[row[0].strip()] = (row[1].strip() if len(row) > 1 else "")
    return out


@st.cache_data(ttl=60, show_spinner=False)
def leggi_tab(tab: str) -> list[dict]:
    return _get_spreadsheet().worksheet(tab).get_all_records()


@st.cache_data(ttl=60, show_spinner=False)
def leggi_stato_sistema() -> dict:
    return {
        "config":     leggi_config(),
        "roadmap":    leggi_tab(TAB_ROADMAP),
        "log_freeze": leggi_tab(TAB_LOG_FREEZE),
        "log_verify": leggi_tab(TAB_LOG_VERIFY),
        "log_errors": leggi_tab(TAB_LOG_ERRORS),
        "queue":      leggi_tab(TAB_QUEUE),
    }


def invalida_cache() -> None:
    leggi_config.clear()
    leggi_tab.clear()
    leggi_stato_sistema.clear()


# ============================================================
# HELPER DI DOMINIO
# ============================================================
def estrai_fase(note: str) -> str | None:
    """Estrae 'B.6' da 'FASE B.6' o simile. None se assente."""
    m = _FASE_RE.search(note or "")
    return m.group(1).upper() if m else None


def stato_normalizzato(stato: str) -> str:
    """Ritorna 'done' | 'wip' | 'todo' | 'altro'.
    Robusto a emoji, spazi, maiuscole/minuscole."""
    s = (stato or "").strip().lower()
    s = re.sub(r"[^\w\s]", " ", s).strip()
    s = re.sub(r"\s+", " ", s)
    for kw in STATI_DONE_KW:
        if kw in s: return "done"
    for kw in STATI_WIP_KW:
        if kw in s: return "wip"
    for kw in STATI_TODO_KW:
        if kw in s: return "todo"
    return "altro"


def roadmap_per_fase(roadmap: list[dict]) -> dict[str, dict]:
    """Mappa 'B.6' -> record Roadmap, estraendo la fase dalla colonna Note."""
    out: dict[str, dict] = {}
    for r in roadmap:
        fase = estrai_fase(r.get("Note", ""))
        if fase:
            out[fase] = r
    return out


# ============================================================
# RENDER: KPI
# ============================================================
def render_kpi(stato: dict) -> None:
    roadmap = stato["roadmap"]
    done = sum(1 for r in roadmap if stato_normalizzato(r.get("Stato", "")) == "done")
    wip  = sum(1 for r in roadmap if stato_normalizzato(r.get("Stato", "")) == "wip")
    todo = sum(1 for r in roadmap if stato_normalizzato(r.get("Stato", "")) == "todo")
    total = len(roadmap) or 1

    try:
        pct_media = round(sum(int(r.get("%", 0) or 0) for r in roadmap) / total)
    except Exception:
        pct_media = round(100 * done / total)

    errori = len(stato["log_errors"])
    queue  = len(stato["queue"])

    c1, c2, c3, c4, c5, c6 = st.columns(6)
    c1.metric("Task totali", total)
    c2.metric("Done", done)
    c3.metric("In corso", wip)
    c4.metric("To do", todo)
    c5.metric("Avanzamento medio", f"{pct_media}%")
    c6.metric("Errori / Queue", f"{errori} / {queue}")
    st.progress(min(pct_media, 100) / 100)


# ============================================================
# RENDER: TIMELINE
# ============================================================
def render_timeline(roadmap: list[dict]) -> None:
    st.subheader("🗺️ Roadmap — FASI B (da colonna Note)")
    by_fase = roadmap_per_fase(roadmap)
    if not by_fase:
        st.warning("Nessuna fase B.x trovata nelle Note di Roadmap.")
        return
    for fid in FASI_ATTESE:
        r = by_fase.get(fid)
        if not r:
            st.info(f"**{fid}** — non pianificata")
            continue
        titolo = r.get("Task", "—")
        pct    = r.get("%", 0)
        owner  = r.get("Owner", "—")
        scad   = r.get("Scadenza", "—")
        stato  = stato_normalizzato(r.get("Stato", ""))
        msg = f"**{fid}** — {titolo} · {pct}% · owner: {owner} · scad: {scad}"
        if stato == "done":   st.success(msg)
        elif stato == "wip":  st.warning(msg)
        else:                 st.info(msg)


# ============================================================
# RENDER: QUEUE
# ============================================================
def render_queue(queue: list[dict]) -> None:
    st.subheader("📥 Queue")
    if not queue:
        st.success("Queue vuota ✅")
        return
    st.dataframe(pd.DataFrame(queue), use_container_width=True, hide_index=True)


# ============================================================
# RENDER: LOG
# ============================================================
def render_log(nome: str, righe: list[dict], max_righe: int = 20) -> None:
    st.subheader(f"📜 {nome}")
    if not righe:
        st.caption("Nessuna voce.")
        return
    df = pd.DataFrame(righe)
    if "Timestamp" in df.columns:
        df["Timestamp"] = pd.to_datetime(df["Timestamp"], errors="coerce")
        df = df.sort_values("Timestamp", ascending=False)
    st.dataframe(df.head(max_righe), use_container_width=True, hide_index=True)


# ============================================================
# RENDER: CONFIG
# ============================================================
def render_config(config: dict[str, str]) -> None:
    st.subheader("⚙️ Config")
    col1, col2 = st.columns(2)
    with col1:
        frozen = config.get("SYSTEM_FROZEN", "FALSE").upper() == "TRUE"
        st.metric("Sistema congelato", "🔴 SÌ" if frozen else "🟢 NO")
        st.metric("Freeze mode", config.get("FREEZE_MODE", "—"))
        st.metric("Autorizzato da", config.get("AUTHORIZED_BY", "—"))
        st.metric("Auto-fix", "✅" if config.get("AUTO_FIX_ENABLED", "").upper() == "TRUE" else "❌")
    with col2:
        st.metric("Hourly check", "✅" if config.get("HOURLY_CHECK_ENABLED", "").upper() == "TRUE" else "❌")
        st.metric("Intervallo report (h)", config.get("REPORT_INTERVAL_HOURS", "—"))
        st.metric("Ultima verifica", config.get("LAST_VERIFY", "—"))
        st.metric("Prossima verifica", config.get("NEXT_VERIFY", "—"))


# ============================================================
# ENTRYPOINT PAGINA
# ============================================================
st.title("🛠️ ArtiFix — Dashboard Sistema")
st.caption("Stato sistema in tempo reale · Google Sheet Roadmap via Service Account")

col_t, col_r = st.columns([4, 1])
with col_r:
    if st.button("🔄 Aggiorna", use_container_width=True):
        invalida_cache()
        st.rerun()

try:
    stato = leggi_stato_sistema()
except Exception as e:
    st.error(f"Errore lettura Roadmap: {e}")
    st.stop()

render_kpi(stato)
st.divider()

col_a, col_b = st.columns([2, 1])
with col_a:
    render_timeline(stato["roadmap"])
with col_b:
    render_queue(stato["queue"])

st.divider()
tab1, tab2, tab3, tab4 = st.tabs(["⚙️ Config", "❄️ Freeze", "✅ Verify", "❌ Errors"])
with tab1:
    render_config(stato["config"])
with tab2:
    render_log("Log_Freeze", stato["log_freeze"])
with tab3:
    render_log("Log_Verify", stato["log_verify"])
with tab4:
    render_log("Log_Errors", stato["log_errors"])

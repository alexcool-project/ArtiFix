# sponsors.py
import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import requests
from io import StringIO

SPONSORS_CSV_URL = st.secrets.get("SPONSORS_CSV_URL", "")

BANNER_WIDTH = 300
BANNER_HEIGHT = 100
MAX_VISIBLE = 6


@st.cache_data(ttl=600)  # cache 10 minuti
def load_sponsors():
    """Legge il Google Sheet pubblicato come CSV e restituisce gli sponsor attivi e non scaduti."""
    if not SPONSORS_CSV_URL:
        return []

    try:
        r = requests.get(SPONSORS_CSV_URL, timeout=10)
        r.raise_for_status()
        df = pd.read_csv(StringIO(r.text))
    except Exception as e:
        st.warning(f"Impossibile caricare gli sponsor: {e}")
        return []

    # Normalizza nomi colonne
    df.columns = [str(c).strip().lower() for c in df.columns]

    oggi = datetime.now().date()
    attivi = []

    for _, row in df.iterrows():
        try:
            # --- Controllo attivo ---
            attivo_val = str(row.get("attivo", "")).strip().upper()
            if attivo_val not in ("TRUE", "1", "SI", "SÌ", "YES", "Y"):
                continue

            # --- Controllo campi minimi ---
            nome = str(row.get("nome", "")).strip()
            logo = str(row.get("logo_url", "")).strip()
            sito = str(row.get("sito_url", "")).strip()

            # Scarta righe fantasma (senza nome o logo o sito validi)
            if (not nome or nome.lower() == "nan" or
                not logo or logo.lower() == "nan" or
                not sito or sito.lower() == "nan"):
                continue

            # --- Parsing data (auto-detect italiano o ISO) ---
            data_raw = str(row.get("data_inizio", "")).strip()
            if not data_raw or data_raw.lower() == "nan":
                continue

            data_inizio = None
            for fmt in ("%Y-%m-%d", "%d/%m/%Y", "%d-%m-%Y"):
                try:
                    data_inizio = datetime.strptime(data_raw, fmt).date()
                    break
                except ValueError:
                    continue

            if data_inizio is None:
                # ultimo tentativo con pandas
                try:
                    data_inizio = pd.to_datetime(data_raw, dayfirst=True).date()
                except Exception:
                    continue

            # --- Calcolo scadenza ---
            giorni = int(float(row.get("giorni", 30)))
            data_fine = data_inizio + timedelta(days=giorni)

            if data_inizio <= oggi <= data_fine:
                attivi.append({
                    "nome": nome,
                    "logo_url": logo,
                    "sito_url": sito,
                    "scadenza": data_fine.strftime("%d/%m/%Y"),
                })
        except Exception:
            continue

    return attivi


def render_sponsor_band():
    """Renderizza la banda laterale destra con i banner sponsor."""
    sponsors = load_sponsors()

    if not sponsors:
        st.markdown(
            """
            <div style="
                border: 1px dashed #c8c8c8;
                border-radius: 10px;
                padding: 14px;
                text-align: center;
                color: #888;
                font-size: 0.8rem;
                background: #fafafa;">
                <strong>Spazio sponsor</strong><br>
                <span style="font-size: 0.72rem;">
                Vuoi il tuo logo qui?<br>
                <a href="mailto:info@artifix.it" style="color:#2a6df4;">info@artifix.it</a>
                </span>
            </div>
            """,
            unsafe_allow_html=True,
        )
        return

    # Rotazione a blocchi (server-side)
    offset = st.session_state.get("sponsor_offset", 0)
    if len(sponsors) <= MAX_VISIBLE:
        visibili = sponsors
    else:
        visibili = [sponsors[(offset + i) % len(sponsors)] for i in range(MAX_VISIBLE)]
        st.session_state.sponsor_offset = (offset + MAX_VISIBLE) % len(sponsors)

    cards_html = ""
    for s in visibili:
        cards_html += f"""
        <a href="{s['sito_url']}" target="_blank" rel="noopener noreferrer"
           style="display:block; margin: 0 0 12px 0; text-decoration:none;">
            <div style="
                width: {BANNER_WIDTH}px;
                height: {BANNER_HEIGHT}px;
                border-radius: 10px;
                overflow: hidden;
                background: #ffffff;
                box-shadow: 0 2px 8px rgba(0,0,0,0.08);
                display: flex;
                align-items: center;
                justify-content: center;
                transition: transform 0.2s ease, box-shadow 0.2s ease;"
                onmouseover="this.style.transform='translateY(-2px)';this.style.boxShadow='0 6px 14px rgba(0,0,0,0.15)';"
                onmouseout="this.style.transform='translateY(0)';this.style.boxShadow='0 2px 8px rgba(0,0,0,0.08)';">
                <img src="{s['logo_url']}" alt="{s['nome']}"
                     style="max-width: 100%; max-height: 100%; object-fit: contain;" />
            </div>
        </a>
        """

    st.markdown(
        f"""
        <div style="margin-bottom: 8px;">
            <div style="
                font-size: 0.7rem;
                text-transform: uppercase;
                letter-spacing: 1px;
                color: #999;
                text-align: center;
                margin-bottom: 10px;">
                Sponsor ArtiFix
            </div>
            {cards_html}
        </div>
        """,
        unsafe_allow_html=True,
    )


def sponsor_band_placeholder():
    st.markdown(
        """
        <div style="
            margin-top: 12px;
            padding: 10px;
            border-radius: 10px;
            background: linear-gradient(135deg, #eef4ff 0%, #f7f9fc 100%);
            border: 1px solid #d6e2f5;
            text-align: center;
            font-size: 0.72rem;
            color: #555;">
            <div style="font-weight: 600; margin-bottom: 4px;">Diventa sponsor</div>
            <a href="mailto:info@artifix.it?subject=Sponsorizzazione%20ArtiFix"
               style="color: #2a6df4; text-decoration: none; font-weight: 600;">
               info@artifix.it
            </a>
        </div>
        """,
        unsafe_allow_html=True,
    )

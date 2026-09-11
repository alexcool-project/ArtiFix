# sponsors.py
import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
from datetime import datetime, timedelta
import requests
from io import StringIO

SPONSORS_CSV_URL = st.secrets.get("SPONSORS_CSV_URL", "")

BANNER_WIDTH = 300
BANNER_HEIGHT = 100
MAX_VISIBLE = 6
SCROLL_DURATION = 40  # secondi per un ciclo completo (più alto = più lento)


# --- DIZIONARIO TRADUZIONI SPONSOR (IT/EN) ---
SPONSOR_TEXTS = {
    "it": {
        "band_title": "Sponsor ArtiFix",
        "empty_title": "Spazio sponsor",
        "empty_text": "Vuoi il tuo logo qui?",
        "become_sponsor": "Diventa sponsor",
    },
    "en": {
        "band_title": "ArtiFix Sponsors",
        "empty_title": "Sponsor space",
        "empty_text": "Want your logo here?",
        "become_sponsor": "Become a sponsor",
    }
}


def _get_sponsor_text(key, lang="it"):
    """Recupera una traduzione dal dizionario sponsor."""
    lang = lang if lang in SPONSOR_TEXTS else "it"
    return SPONSOR_TEXTS[lang].get(key, key)


@st.cache_data(ttl=300)  # cache 5 minuti
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


def render_sponsor_band(lang="it"):
    """Renderizza la banda laterale destra con i banner sponsor in scorrimento verticale fluido."""
    sponsors = load_sponsors()

    if not sponsors:
        st.markdown(
            f"""
            <div style="
                border: 1px dashed #c8c8c8;
                border-radius: 10px;
                padding: 14px;
                text-align: center;
                color: #888;
                font-size: 0.8rem;
                background: #fafafa;">
                <strong>{_get_sponsor_text('empty_title', lang)}</strong><br>
                <span style="font-size: 0.72rem;">
                {_get_sponsor_text('empty_text', lang)}<br>
                <a href="mailto:info@artifix.it" style="color:#2a6df4;">info@artifix.it</a>
                </span>
            </div>
            """,
            unsafe_allow_html=True,
        )
        return

    # Calcola altezza iframe
    num_visible = min(MAX_VISIBLE, len(sponsors))
    iframe_height = 40 + (num_visible * (BANNER_HEIGHT + 12)) + 20

    # Durata animazione proporzionale al numero di sponsor
    total_banners = max(len(sponsors), 1)
    duration = SCROLL_DURATION * (total_banners / 6.0) if total_banners > 6 else SCROLL_DURATION

    # Genera i banner HTML
    banners_html = ""
    for s in sponsors:
        banners_html += f"""
            <a href="{s['sito_url']}" target="_blank" rel="noopener noreferrer" class="sponsor-card">
                <img src="{s['logo_url']}" alt="{s['nome']}" loading="lazy">
            </a>
        """

    band_title = _get_sponsor_text('band_title', lang)

    # HTML completo con animazione CSS
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
    <meta charset="utf-8">
    <style>
        * {{ box-sizing: border-box; }}
        body {{
            margin: 0;
            padding: 0;
            font-family: 'Segoe UI', system-ui, -apple-system, Roboto, Arial, sans-serif;
            background: transparent;
            overflow: hidden;
        }}
        .band-title {{
            font-size: 11px;
            text-transform: uppercase;
            letter-spacing: 1px;
            color: #999;
            text-align: center;
            margin: 8px 0 12px;
            font-weight: 600;
        }}
        .scroll-viewport {{
            width: 100%;
            height: calc(100% - 40px);
            overflow: hidden;
            position: relative;
            mask-image: linear-gradient(
                to bottom,
                transparent 0%,
                #000 8%,
                #000 92%,
                transparent 100%
            );
            -webkit-mask-image: linear-gradient(
                to bottom,
                transparent 0%,
                #000 8%,
                #000 92%,
                transparent 100%
            );
        }}
        .scroll-content {{
            display: flex;
            flex-direction: column;
            gap: 12px;
            animation: scrollUp {duration}s linear infinite;
        }}
        .scroll-content:hover {{
            animation-play-state: paused;
        }}
        @keyframes scrollUp {{
            0%   {{ transform: translateY(0); }}
            100% {{ transform: translateY(-50%); }}
        }}
        .sponsor-card {{
            display: block;
            width: 100%;
            max-width: {BANNER_WIDTH}px;
            height: {BANNER_HEIGHT}px;
            border-radius: 10px;
            overflow: hidden;
            background: #ffffff;
            box-shadow: 0 2px 8px rgba(0,0,0,0.08);
            display: flex;
            align-items: center;
            justify-content: center;
            transition: transform 0.2s ease, box-shadow 0.2s ease;
            flex-shrink: 0;
            text-decoration: none;
        }}
        .sponsor-card:hover {{
            transform: scale(1.03);
            box-shadow: 0 6px 14px rgba(0,0,0,0.15);
        }}
        .sponsor-card img {{
            max-width: 100%;
            max-height: 100%;
            object-fit: contain;
            display: block;
        }}
    </style>
    </head>
    <body>
        <div class="band-title">{band_title}</div>
        <div class="scroll-viewport">
            <div class="scroll-content">
                {banners_html}
                {banners_html}
            </div>
        </div>
    </body>
    </html>
    """

    components.html(html, height=iframe_height, scrolling=False)


def sponsor_band_placeholder(lang="it"):
    st.markdown(
        f"""
        <div style="
            margin-top: 12px;
            padding: 10px;
            border-radius: 10px;
            background: linear-gradient(135deg, #eef4ff 0%, #f7f9fc 100%);
            border: 1px solid #d6e2f5;
            text-align: center;
            font-size: 0.72rem;
            color: #555;">
            <div style="font-weight: 600; margin-bottom: 4px;">{_get_sponsor_text('become_sponsor', lang)}</div>
            <a href="mailto:info@artifix.it?subject=Sponsorizzazione%20ArtiFix"
               style="color: #2a6df4; text-decoration: none; font-weight: 600;">
               info@artifix.it
            </a>
        </div>
        """,
        unsafe_allow_html=True,
    )

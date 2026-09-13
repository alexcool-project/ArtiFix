import streamlit as st
import ezdxf
import trimesh
import io
import numpy as np
import base64
import os
import json
from datetime import datetime
import tempfile
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import time

# --- MODULO SPONSOR (Google Sheets) ---
from sponsors import load_sponsors, render_sponsor_band, sponsor_band_placeholder

# --- MODULO TRADUZIONI (IT/EN) ---
from translations import TRANSLATIONS, get_text, detect_browser_language

# --- LIBRERIA COOKIE (OPZIONALE) ---
try:
    from streamlit_cookies_controller import CookieController
    cookie_controller = CookieController()
    COOKIE_LIB = True
except ImportError:
    COOKIE_LIB = False

# --- LINK DIRETTI DELLE IMMAGINI (GitHub Raw) ---
CUBO_URL = "https://raw.githubusercontent.com/alexcool-project/Artifix/main/docs/images/ArchiFix_cubo-logo.png"
LOGO_URL = "https://raw.githubusercontent.com/alexcool-project/Artifix/main/docs/images/Artifix_logo.png"

# --- LINK PAGAMENTO (PayPal) ---
DONATE_LINK = "https://www.paypal.com/ncp/payment/9C4ZLMBHBDXVS"

# --- STATO LINGUA (RILEVAMENTO BROWSER) ---
if 'lang' not in st.session_state:
    st.session_state.lang = detect_browser_language()

# --- FUNZIONE HELPER PER TRADUZIONE ---
def t(key, **kwargs):
    """Shortcut per get_text con la lingua corrente."""
    return get_text(key, st.session_state.lang, **kwargs)

# --- SEO META TAG ---
st.markdown("""
<title>ArtiFix - Convertitore CAD/CAM Universale | Converti STL, OBJ, PLY in 3D PDF</title>
<meta name="description" content="ArtiFix è la piattaforma professionale per convertire file CAD/CAM (STL, OBJ, PLY, GLB, GLTF, FBX, DAE, DXF) in 3D PDF, STL, OBJ, GLTF e altri formati. Convertitore online gratuito e veloce per ingegneri e progettisti." />
<meta name="keywords" content="convertitore CAD, convertire STL in 3D PDF, convertire OBJ in STL, convertire 3D PDF, convertitore gratuito, convertire DAE, convertire FBX, convertire GLB, conversione mesh 3D, ArtiFix, CAD/CAM tool" />
<meta name="robots" content="index, follow" />
<meta property="og:title" content="ArtiFix - Convertitore CAD/CAM Universale" />
<meta property="og:description" content="Converti i tuoi file 3D (STL, OBJ, PLY, GLB, FBX, DAE) in 3D PDF e altri formati. Strumento professionale e gratuito per ingegneri e progettisti." />
<meta property="og:type" content="website" />
<meta property="og:image" content="https://raw.githubusercontent.com/alexcool-project/Artifix/main/docs/images/Artifix_logo.png" />
<meta property="og:url" content="https://artifix.streamlit.app" />
<meta property="og:locale" content="it_IT" />
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "WebApplication",
  "name": "ArtiFix",
  "url": "https://artifix.streamlit.app",
  "applicationCategory": "EngineeringApplication",
  "operatingSystem": "Web",
  "description": "Convertitore universale per file CAD/CAM e mesh 3D (STL, OBJ, PLY, GLB, GLTF, FBX, DAE, DXF). Converti in 3D PDF e altri formati.",
  "offers": { "@type": "Offer", "price": "0", "priceCurrency": "EUR" }
}
</script>
""", unsafe_allow_html=True)

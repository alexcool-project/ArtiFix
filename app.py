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

# --- UTILITY CONDIVISIONE VIEWER (v8.0) ---
from share_utils import render_share_section

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

# --- LINK MAILTO SPONSOR CON TEMPLATE PRECOMPILATO ---
SPONSOR_MAILTO = (
    "mailto:info@artifix.it"
    "?subject=Richiesta%20Sponsorizzazione%20ArtiFix"
    "&body=FORM%20PRECOMPILATO%20(se%20vuoi%20aderire%20alla%20sponsorizzazione%20"
    "valuta%20una%20donazione%20per%20il%20progetto%20ArtiFix%20e%20comunque%20"
    "inizia%20ad%20utilizzare%20i%20servizi%20CAD%20gratuiti!)%0D%0A%0D%0A"
    "Buongiorno%20Team%20ArtiFix%2C%0D%0A%0D%0A"
    "Sono%20interessato%2Fa%20alla%20sponsorizzazione%20di%20ArtiFix%20"
    "(puoi%20cliccare%20sul%20pulsante%20%22Dona%20con%20PayPal%22%20presente%20"
    "nel%20sito%20per%20richiedere%20la%20sponsorizzazione%2C%20entro%20pochi%20"
    "minuti%20sar%C3%A0%20attiva%20sul%20sito)%0D%0A%0D%0A"
    "Ecco%20i%20miei%20dati%3A%0D%0A%0D%0A"
    "%F0%9F%8F%A2%20Nome%20Azienda%3A%20%0D%0A"
    "%F0%9F%8C%90%20Sito%20Web%3A%20%0D%0A"
    "%F0%9F%93%A7%20Email%3A%20%0D%0A"
    "%F0%9F%93%9E%20Telefono%3A%20%0D%0A"
    "%F0%9F%96%BC%EF%B8%8F%20Logo%20%E2%89%88%20300%20x%20100px%20(URL%20GitHub%20Raw%20o%20allegato)%3A%20%0D%0A"
    "%F0%9F%92%AC%20Messaggio%3A%0D%0A%0D%0A"
    "Grazie%2C%0D%0A%5BNominativo%5D"
)

# --- CONFIGURAZIONE PAGINA ---
if CUBO_URL:
    st.set_page_config(
        page_title="ArtiFix - Universal CAD/CAM Repair",
        page_icon=CUBO_URL,
        layout="wide",
        initial_sidebar_state="expanded"
    )
else:
    st.set_page_config(
        page_title="ArtiFix - Universal CAD/CAM Repair",
        page_icon="🔧",
        layout="wide",
        initial_sidebar_state="expanded"
    )

# --- STATO LINGUA ---
if 'lang' not in st.session_state:
    try:
        st.session_state.lang = detect_browser_language()
    except Exception:
        st.session_state.lang = "it"

# --- FUNZIONE HELPER PER TRADUZIONE ---
def t(key, **kwargs):
    return get_text(key, st.session_state.lang, **kwargs)

# --- SEO META TAG ---
st.markdown("""
<title>ArtiFix - Convertitore CAD/CAM Universale | Converti STL, OBJ, PLY in 3D PDF</title>
<meta name="description" content="ArtiFix è la piattaforma professionale per convertire file CAD/CAM (STL, OBJ, PLY, GLB, GLTF, FBX, DAE, DXF) in 3D PDF, STL, OBJ, GLTF e altri formati. Convertitore online gratuito e veloce per ingegneri e progettisti." />
<meta name="robots" content="index, follow" />
<meta property="og:title" content="ArtiFix - Convertitore CAD/CAM Universale" />
<meta property="og:url" content="https://artifix.streamlit.app" />
""", unsafe_allow_html=True)

# --- CSS MINIMALE E PULITO ---
st.markdown("""
<style>
    .main-header { font-size: 2.2rem; color: #1f77b4; font-weight: 700; text-align: center; margin-bottom: 1rem; }
    .logo-container { text-align: center; padding: 1rem 0; }
    .logo-container img { max-width: 100%; width: auto; height: auto; display: block; margin: 0 auto; }
    .sidebar-logo { text-align: center; padding: 1rem 0; border-bottom: 1px solid #ddd; margin-bottom: 1rem; }
    .sidebar-logo img { max-width: 100%; width: auto; height: auto; display: block; margin: 0 auto; }
    .stButton>button { width: 100%; border-radius: 6px; font-size: 14px; }
    .metric-card { background-color: #f0f2f6; padding: 1.2rem; border-radius: 12px; text-align: center; box-shadow: 0 2px 6px rgba(0,0,0,0.05); }
    .metric-value { font-size: 2rem; font-weight: 700; color: #1f77b4; }
    .metric-label { font-size: 0.85rem; color: #555; }
    .file-info-card { background-color: #f8f9fa; padding: 1rem; border-radius: 10px; border-left: 3px solid #1f77b4; margin: 0.5rem 0; }
    footer {visibility: hidden;}
    .footer-artifix {
        position: fixed; bottom: 0; left: 0; right: 0;
        background: #f8f9fa; padding: 12px; text-align: center;
        font-size: 12px; color: #666; border-top: 1px solid #ddd; z-index: 999;
    }
    .main .block-container { padding-bottom: 80px !important; }
    .lang-selector { padding: 8px 0; margin-bottom: 15px; }

    /* ===== FIX TESTO BIANCO PULSANTE GUIDA ===== */
    a.guide-button, a.guide-button:link, a.guide-button:visited,
    a.guide-button:hover, a.guide-button:active, a.guide-button:focus {
        color: #ffffff !important;
        text-decoration: none !important;
        background: #1f77b4 !important;
        display: inline-block !important;
        padding: 10px 24px !important;
        border-radius: 8px !important;
        font-weight: 700 !important;
        font-size: 14px !important;
        border: none !important;
    }
    a.guide-button:hover {
        background: #155a8a !important;
    }
</style>
""", unsafe_allow_html=True)

# --- TENTATIVO IMPORT LIBRERIE ---
try:
    import ifcopenshell
    IFC_AVAILABLE = True
except ImportError:
    IFC_AVAILABLE = False

try:
    import geopandas as gpd
    GEOPANDAS_AVAILABLE = True
except (ImportError, OSError):
    GEOPANDAS_AVAILABLE = False

try:
    from PyPDF2 import PdfReader
    PDF_AVAILABLE = True
except ImportError:
    PDF_AVAILABLE = False

try:
    import fitz
    FITZ_AVAILABLE = True
except ImportError:
    FITZ_AVAILABLE = False

try:
    import docx
    DOCX_AVAILABLE = True
except ImportError:
    DOCX_AVAILABLE = False

try:
    import openpyxl
    XLSX_AVAILABLE = True
except ImportError:
    XLSX_AVAILABLE = False

try:
    import cairosvg
    SVG_AVAILABLE = True
except (ImportError, OSError):
    SVG_AVAILABLE = False

# --- STATO PAGINE E COOKIE ---
if 'page_attuale' not in st.session_state:
    st.session_state.page_attuale = "Dashboard"

if 'cookie_consent' not in st.session_state:
    if COOKIE_LIB:
        st.session_state.cookie_consent = cookie_controller.get('cookie_consent')
    else:
        st.session_state.cookie_consent = None

# --- DEFINIZIONE VARIABILI ---
SUPPORTED_FORMATS = {
    "CAD 2D": {"extensions": [".dxf"], "icon": "📐", "description": "File CAD (DXF)"},
    "CAD 3D & Mesh": {"extensions": [".stl", ".obj", ".ply", ".glb", ".gltf", ".fbx", ".3mf", ".dae", ".wrl", ".off", ".u3d"], "icon": "🧊", "description": "Mesh 3D (STL, OBJ, PLY, GLB, GLTF, FBX, 3MF, DAE, WRL, U3D)"},
    "BIM": {"extensions": [".ifc"], "icon": "🏗️", "description": "Building Information Modeling (IFC)"},
    "Geospaziale": {"extensions": [".shp", ".geojson", ".kml", ".gpx"], "icon": "🌍", "description": "Dati geografici e GIS"},
    "Vettoriale": {"extensions": [".svg"], "icon": "✏️", "description": "Grafica vettoriale (SVG)"},
    "Documenti": {"extensions": [".pdf", ".docx", ".xlsx"], "icon": "📄", "description": "Documenti, fogli di calcolo"}
}

ALL_EXTENSIONS = []
for info in SUPPORTED_FORMATS.values():
    ALL_EXTENSIONS.extend(info["extensions"])

CONVERSION_MATRIX = {
    'stl': ['obj', 'ply', 'glb', 'gltf', 'fbx', '3mf', 'dae', 'wrl', 'off', 'dxf', 'pdf'],
    'obj': ['stl', 'ply', 'glb', 'gltf', 'fbx', '3mf', 'dae', 'wrl', 'off', 'dxf', 'pdf'],
    'ply': ['stl', 'obj', 'glb', 'gltf', 'fbx', '3mf', 'dae', 'wrl', 'off', 'dxf', 'pdf'],
    'glb': ['stl', 'obj', 'ply', 'gltf', 'fbx', '3mf', 'dae', 'wrl', 'off', 'dxf', 'pdf'],
    'gltf': ['stl', 'obj', 'ply', 'glb', 'fbx', '3mf', 'dae', 'wrl', 'off', 'dxf', 'pdf'],
    'fbx': ['stl', 'obj', 'ply', 'glb', 'gltf', '3mf', 'dae', 'wrl', 'off', 'dxf', 'pdf'],
    '3mf': ['stl', 'obj', 'ply', 'glb', 'gltf', 'fbx', 'dae', 'wrl', 'off', 'dxf', 'pdf'],
    'dae': ['stl', 'obj', 'ply', 'glb', 'gltf', 'fbx', '3mf', 'wrl', 'off', 'dxf', 'pdf'],
    'wrl': ['stl', 'obj', 'ply', 'glb', 'gltf', 'fbx', '3mf', 'dae', 'off', 'dxf', 'pdf'],
    'off': ['stl', 'obj', 'ply', 'glb', 'gltf', 'fbx', '3mf', 'dae', 'wrl', 'dxf', 'pdf'],
    'dxf': ['stl', 'obj', 'glb', 'gltf', 'fbx', '3mf', 'dae', 'wrl', 'off', 'pdf'],
}

FORMAT_NAMES = {
    'stl': 'STL (.stl)',
    'obj': 'OBJ (.obj)',
    'ply': 'PLY (.ply)',
    'glb': 'GLB (.glb)',
    'gltf': 'GLTF (.gltf)',
    'fbx': 'FBX (.fbx)',
    '3mf': '3MF (.3mf)',
    'dae': 'DAE (.dae)',
    'wrl': 'WRL (.wrl)',
    'off': 'OFF (.off)',
    'u3d': 'U3D (.u3d)',
    'dxf': 'DXF (.dxf)',
    'pdf': '3D PDF (.pdf)'
}

def detect_file_type(file_extension):
    file_extension = file_extension.lower().replace('.', '')
    for category, info in SUPPORTED_FORMATS.items():
        for ext in info["extensions"]:
            if ext.replace('.', '') == file_extension:
                return category, info["icon"]
    return "Sconosciuto", "❓"

def load_3d_file(file_bytes, file_extension):
    try:
        file_extension = file_extension.lower().replace('.', '')
        format_map = {
            'stl':'stl', 'obj':'obj', 'ply':'ply', 'glb':'glb', 'gltf':'gltf', 'fbx':'fbx', '3mf':'3mf', 'dae':'dae', 'wrl':'wrl', 'off':'off', 'u3d':'u3d'
        }
        file_type = format_map.get(file_extension, file_extension)

        if file_extension in ['obj', 'dae']:
            for method in [file_type, None]:
                try:
                    mesh = trimesh.load(io.BytesIO(file_bytes), file_type=method, force='mesh') if method else trimesh.load(io.BytesIO(file_bytes))
                    if mesh is not None and hasattr(mesh, 'vertices') and len(mesh.vertices) > 0:
                        return mesh
                except:
                    continue
            return None
        else:
            mesh = trimesh.load(io.BytesIO(file_bytes), file_type=file_type)
            if isinstance(mesh, trimesh.Scene):
                if len(mesh.geometry) > 0:
                    mesh = trimesh.util.concatenate(list(mesh.geometry.values()))
                else:
                    return None
            if mesh is not None and hasattr(mesh, 'vertices') and len(mesh.vertices) > 0:
                return mesh
            return None
    except Exception:
        return None

def convert_mesh(mesh, target_format):
    try:
        target_format = target_format.lower().replace('.', '')

        if target_format == 'pdf':
            import matplotlib
            matplotlib.use('Agg')
            import matplotlib.pyplot as plt
            from mpl_toolkits.mplot3d.art3d import Poly3DCollection

            fig = plt.figure()
            ax = fig.add_subplot(111, projection='3d')

            tri_arrays = mesh.vertices[mesh.faces]
            poly3d = Poly3DCollection(tri_arrays, alpha=0.1, edgecolor='k', facecolor='#1f77b4')
            ax.add_collection3d(poly3d)

            scale = mesh.vertices.flatten()
            ax.auto_scale_xyz(scale, scale, scale)

            plt.savefig("converted_3d.pdf", format='pdf', bbox_inches='tight')
            plt.close()

            with open("converted_3d.pdf", "rb") as f:
                return f.read()

        elif target_format == 'stl':
            return trimesh.exchange.stl.export_stl(mesh)
        elif target_format == 'obj':
            return trimesh.exchange.obj.export_obj(mesh)
        elif target_format == 'ply':
            return trimesh.exchange.ply.export_ply(mesh)
        elif target_format == 'glb':
            return trimesh.exchange.gltf.export_glb(mesh)
        elif target_format == 'gltf':
            return trimesh.exchange.gltf.export_gltf(mesh)
        elif target_format == 'fbx':
            return trimesh.exchange.fbx.export_fbx(mesh)
        elif target_format == '3mf':
            return trimesh.exchange.threeMF.export_3mf(mesh)
        elif target_format == 'dae':
            return trimesh.exchange.dae.export_dae(mesh)
        elif target_format == 'wrl':
            return trimesh.exchange.vrml.export_vrml(mesh)
        elif target_format == 'off':
            return trimesh.exchange.off.export_off(mesh)
        elif target_format == 'dxf':
            if mesh.vertices is not None and len(mesh.vertices) > 0:
                vertices_2d = mesh.vertices[:, :2]
                dxf_doc = ezdxf.new()
                msp = dxf_doc.modelspace()
                for face in mesh.faces:
                    for i in range(len(face)):
                        v1 = vertices_2d[face[i]]
                        v2 = vertices_2d[face[(i + 1) % len(face)]]
                        msp.add_line(v1, v2)
                return dxf_doc.write()
            return None
        else:
            return None
    except Exception:
        return None

def process_file(file_bytes, file_name):
    file_extension = os.path.splitext(file_name)[1].lower().replace('.', '')
    file_type, icon = detect_file_type(file_extension)
    result = {"success": False, "message": "", "type": file_type, "icon": icon, "info": {}}

    try:
        if file_extension == 'pdf':
            if PDF_AVAILABLE:
                pdf_reader = PdfReader(io.BytesIO(file_bytes))
                result["success"] = True
                result["message"] = f"📄 PDF: {len(pdf_reader.pages)} pagine"
                result["info"] = {"pages": len(pdf_reader.pages)}
            else:
                result["message"] = "Libreria PDF non disponibile."

        elif file_extension == 'dxf':
            dxf_doc = ezdxf.read(io.BytesIO(file_bytes))
            entities = len(dxf_doc.entities)
            layers = set(e.dxf.layer for e in dxf_doc.entities if hasattr(e.dxf, 'layer'))
            result["success"] = True
            result["message"] = f"📐 DXF: {entities} entità, {len(layers)} layer"
            result["info"] = {"entities": entities, "layers": list(layers)[:10]}

        elif file_extension in ['stl','obj','ply','glb','gltf','fbx','3mf','dae','wrl','off','u3d']:
            mesh = load_3d_file(file_bytes, file_extension)
            if mesh and hasattr(mesh, 'vertices') and len(mesh.vertices) > 0:
                result["success"] = True
                result["message"] = f"✅ Mesh: {len(mesh.vertices)} vertici, {len(mesh.faces)} facce"
                result["info"] = {"vertices": len(mesh.vertices), "faces": len(mesh.faces), "mesh": mesh}
            else:
                result["message"] = "❌ File 3D non valido o formato non supportato."

        elif file_extension == 'ifc' and IFC_AVAILABLE:
            with tempfile.NamedTemporaryFile(suffix='.ifc', delete=False) as tmp_ifc:
                tmp_ifc.write(file_bytes)
                tmp_ifc_path = tmp_ifc.name
            try:
                ifc_file = ifcopenshell.open(tmp_ifc_path)
                projects = ifc_file.by_type('IfcProject')
                result["success"] = True
                result["message"] = f"🏗️ IFC: {len(projects)} progetti"
                result["info"] = {"projects": len(projects)}
            finally:
                try:
                    os.unlink(tmp_ifc_path)
                except:
                    pass

        elif file_extension in ['shp','geojson','kml','gpx'] and GEOPANDAS_AVAILABLE:
            if file_extension == 'shp':
                with tempfile.NamedTemporaryFile(suffix='.shp', delete=False) as tmp:
                    tmp.write(file_bytes); tmp_path = tmp.name
                gdf = gpd.read_file(tmp_path); os.unlink(tmp_path)
            else:
                gdf = gpd.read_file(io.BytesIO(file_bytes))
            result["success"] = True
            result["message"] = f"🌍 Geodati: {len(gdf)} features"
            result["info"] = {"features": len(gdf)}

        else:
            result["message"] = f"❌ Formato {file_extension} non supportato."

    except Exception as e:
        result["message"] = f"❌ Errore: {str(e)}"

    return result

def invia_email(nome, email_utente, messaggio):
    smtp_server = st.secrets["SMTP_SERVER"]
    smtp_port = st.secrets["SMTP_PORT"]
    mittente = st.secrets["EMAIL_ADDRESS"]
    password = st.secrets["EMAIL_PASSWORD"]
    destinatario = st.secrets["RECIPIENT_EMAIL"]

    msg = MIMEMultipart()
    msg['From'] = mittente
    msg['To'] = destinatario
    msg['Subject'] = f"Nuovo messaggio da {nome}"

    corpo = f"Da: {nome} ({email_utente})\n\n{messaggio}"
    msg.attach(MIMEText(corpo, 'plain'))

    try:
        server = smtplib.SMTP_SSL(smtp_server, smtp_port)
        server.login(mittente, password)
        server.sendmail(mittente, destinatario, msg.as_string())
        server.quit()
        return True
    except Exception as e:
        return str(e)


# ============================================================
# FUNZIONI HELPER PER FORMATI PROPRIETARI E 3D PDF
# ============================================================

def render_proprietary_formats_help():
    """Mostra una tendina (expander) con le note sui formati proprietari.

    Elegante, compatta, chiusa di default. L'utente la apre solo se necessario.
    Sostituisce il precedente box grande sempre visibile.
    """
    with st.expander(t("notes_expander_title"), expanded=False):
        # Intro
        st.markdown(t("notes_expander_intro"))

        st.markdown("---")

        # Due colonne: supportati vs non supportati
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(t("notes_expander_native"))
        with col2:
            st.markdown(t("notes_expander_not_supported"))

        st.markdown("---")

        # Come procedere
        st.markdown(t("notes_expander_howto"))
        st.markdown(t("notes_expander_steps"))

        # Tip
        st.info(t("notes_expander_tip"))

        # Link alla guida (PULSANTE CON TESTO BIANCO FORZATO + CLASSE CSS)
        st.markdown(
            f"""
            <div style="text-align: center; margin-top: 12px;">
                <a href="https://www.artifix.it/esportare-dwg-in-dae.html" target="_blank" rel="noopener"
                   class="guide-button">
                    {t("notes_expander_guide_link")}
                </a>
            </div>
            """,
            unsafe_allow_html=True
        )

def is_3d_pdf(file_bytes):
    """Verifica se un PDF contiene un modello 3D incorporato (U3D o PRC)."""
    try:
        if not PDF_AVAILABLE:
            return False
        pdf_reader = PdfReader(io.BytesIO(file_bytes))
        for page in pdf_reader.pages:
            page_text = str(page)
            if '/3D' in page_text or '/U3D' in page_text or '/PRC' in page_text:
                return True
        return False
    except Exception:
        return False


def extract_3d_from_pdf(file_bytes):
    """Tenta di estrarre un modello 3D da un PDF con U3D o PRC."""
    try:
        if not FITZ_AVAILABLE:
            return None
        import fitz
        doc = fitz.open(stream=file_bytes, filetype="pdf")
        for page in doc:
            for xref in range(1, doc.xref_length()):
                try:
                    obj = doc.xref_object(xref)
                    if '/U3D' in obj or '/PRC' in obj or '/Subtype /U3D' in obj:
                        stream = doc.xref_stream(xref)
                        if stream and len(stream) > 100:
                            doc.close()
                            return {'u3d_bytes': stream, 'method': 'PyMuPDF'}
                except Exception:
                    continue
        doc.close()
        return None
    except Exception:
        return None


# --- BARRA LATERALE ---
with st.sidebar:
    if LOGO_URL:
        st.markdown(f'<div class="sidebar-logo"><img src="{LOGO_URL}" alt="ArtiFix Logo"></div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="sidebar-logo"><h3 style="color:#1f77b4;margin:0;">🔧 ARTIFIX</h3></div>', unsafe_allow_html=True)

    st.markdown('<div class="lang-selector">', unsafe_allow_html=True)
    lang_options = {"it": "🇮🇹 Italiano", "en": "🇬🇧 English"}
    current_lang_index = 0 if st.session_state.lang == "it" else 1
    selected_lang = st.selectbox(
        t("sidebar_lang_select"),
        options=list(lang_options.keys()),
        format_func=lambda x: lang_options[x],
        index=current_lang_index,
        key="lang_selector"
    )
    if selected_lang != st.session_state.lang:
        st.session_state.lang = selected_lang
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("---")
    st.markdown(f"## {t('sidebar_navigation')}")

    if st.session_state.page_attuale in ["Cookie Policy", "Privacy Policy"]:
        st.session_state.navigation = "Dashboard"
        st.markdown(f"🔙 **{st.session_state.page_attuale}**")
    else:
        PAGE_KEYS = {
            "Dashboard": "nav_dashboard",
            "Ripara File": "nav_repair",
            "Viewer 3D": "nav_viewer",
            "Converti Formati": "nav_convert",
            "Progetto ArtiFix": "nav_project",
            "Diventa Sponsor": "nav_sponsor",
        }
        PAGE_ORDER = ["Dashboard", "Ripara File", "Viewer 3D", "Converti Formati", "Progetto ArtiFix", "Diventa Sponsor"]

        current_index = 0
        for idx, p in enumerate(PAGE_ORDER):
            if p == st.session_state.page_attuale:
                current_index = idx
                break

        nav_key = f"navigation_{st.session_state.lang}"

        page = st.radio(
            t("sidebar_navigation"),
            PAGE_ORDER,
            format_func=lambda x: t(PAGE_KEYS.get(x, x)),
            index=current_index,
            key=nav_key,
            label_visibility="collapsed"
        )
        st.session_state.page_attuale = page

    st.markdown("---")

    if st.button(t("nav_privacy"), key="privacy_link", use_container_width=True):
        st.session_state.page_attuale = "Privacy Policy"
        st.rerun()

    if st.button(t("nav_cookie"), key="cookie_link", use_container_width=True):
        st.session_state.page_attuale = "Cookie Policy"
        st.rerun()

    terms_url = "https://www.artifix.it/termini.html" if st.session_state.lang == "it" else "https://www.artifix.it/en/terms.html"
    st.markdown(
        f"""
        <a href="{terms_url}" target="_blank" style="display:block; text-align:center; background:#f0f2f6; color:#333; padding:8px; border-radius:6px; text-decoration:none; font-weight:600; font-size:13px; margin-top:8px;">
            {t("nav_terms")}
        </a>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        f"""
        <a href="{DONATE_LINK}" target="_blank" style="display:block; text-align:center; background:#f0f2f6; color:#333; padding:8px; border-radius:6px; text-decoration:none; font-weight:600; font-size:13px; margin-top:15px;">
            {t("nav_donate")}
        </a>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        f"""
        <a href="{SPONSOR_MAILTO}" style="display:block; text-align:center; background:#fff4e6; color:#c26a00; padding:8px; border-radius:6px; text-decoration:none; font-weight:600; font-size:13px; margin-top:8px; border:1px solid #ffd9a8;">
            {t("nav_become_sponsor")}
        </a>
        """,
        unsafe_allow_html=True
    )

# --- LOGICA PAGINE ---
if st.session_state.page_attuale == "Privacy Policy":
    page = "Privacy Policy"
elif st.session_state.page_attuale == "Cookie Policy":
    page = "Cookie Policy"
else:
    page = st.session_state.page_attuale

# --- POPUP COOKIE E PRIVACY ---
if st.session_state.cookie_consent is None:
    st.markdown("<br><br><br>", unsafe_allow_html=True)
    with st.container(border=True):
        st.markdown(f"""
        <h3 style="color: #1f77b4; text-align: center; margin-bottom: 15px;">{t("cookie_title")}</h3>
        <p style="font-size: 15px; line-height: 1.8;">{t("cookie_text")}</p>
        """, unsafe_allow_html=True)
        st.markdown(f"""
        <div style="text-align: center; margin-bottom: 15px;">
            <strong style="color: #333;">{t("cookie_check_privacy")}</strong>
        </div>
        """, unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            if st.button(t("cookie_accept_necessary"), key="decline_cookies", use_container_width=True):
                st.session_state.cookie_consent = "declined"
                st.rerun()
        with col2:
            if st.button(t("cookie_accept_all"), key="accept_cookies", type="primary", use_container_width=True):
                st.session_state.cookie_consent = "accepted"
                st.rerun()

# --- DASHBOARD ---
if page == "Dashboard":
    col_main, col_side = st.columns([3, 1], gap="large")
    with col_main:
        st.markdown('<div class="logo-container"><img src="' + LOGO_URL + '" alt="Logo ArtiFix"></div>', unsafe_allow_html=True)
        st.header(t("dash_header"))
        cols = st.columns(4)
        metrics = [("14,280", t("dash_metric_repaired")), ("38,910", t("dash_metric_conversions")), ("50+", t("dash_metric_formats")), ("🟢", t("dash_metric_online"))]
        for col, (val, label) in zip(cols, metrics):
            col.markdown(f'<div class="metric-card"><div class="metric-value">{val}</div><div class="metric-label">{label}</div></div>', unsafe_allow_html=True)
        st.markdown("---")
        st.subheader(t("dash_supported_formats"))
        cols = st.columns(4)
        for idx, (category, info) in enumerate(SUPPORTED_FORMATS.items()):
            with cols[idx % 4]:
                st.markdown(f'<div style="background:#f8f9fa;padding:0.7rem;border-radius:10px;border-left:3px solid #1f77b4;"><div style="font-weight:600;">{info["icon"]} {category}</div><div style="font-size:0.8rem;color:#666;">{info["description"]}</div></div>', unsafe_allow_html=True)
        st.info(t("dash_info_select"))
    with col_side:
        render_sponsor_band(st.session_state.lang)
        sponsor_band_placeholder(st.session_state.lang)

# --- RIPARA FILE ---
elif page == "Ripara File":
    col_main, col_side = st.columns([3, 1], gap="large")
    with col_main:
        from repair_page import render_repair_page
        render_repair_page(load_3d_file, ALL_EXTENSIONS)
        render_proprietary_formats_help()
    with col_side:
        render_sponsor_band(st.session_state.lang)
        sponsor_band_placeholder(st.session_state.lang)

# --- VIEWER 3D ---
elif page == "Viewer 3D":
    col_main, col_side = st.columns([3, 1], gap="large")
    with col_main:
        st.header(t("viewer_header"))

        viewer_file = st.file_uploader(
            t("viewer_upload"),
            type=["stl","obj","ply","glb","gltf","fbx","3mf","dae","wrl","off","u3d","pdf"],
            key="viewer",
            help=t("viewer_upload_hint")
        )

        if viewer_file:
            # ✅ Controllo 3D PDF
            file_ext_check = os.path.splitext(viewer_file.name)[1].lower().replace('.', '')
            if file_ext_check == "pdf":
                file_bytes_check = viewer_file.getvalue()
                if not is_3d_pdf(file_bytes_check):
                    st.error(t("pdf_no_3d_title"))
                    st.markdown(t("pdf_no_3d_desc").format(filename=viewer_file.name))
                    with st.expander(t("pdf_no_3d_howto_title"), expanded=True):
                        st.markdown(t("pdf_no_3d_howto_steps"))
                    st.info(t("pdf_no_3d_alternative"))
                    st.stop()
                else:
                    st.success(t("pdf_3d_detected"))
                    extracted = extract_3d_from_pdf(file_bytes_check)
                    if extracted:
                        st.info(f"✅ Modello 3D estratto con successo ({extracted['method']}). Elaborazione in corso...")

            progress_bar = st.progress(0)
            status_text = st.empty()
            status_text.text(t("viewer_status_loading"))
            progress_bar.progress(30)
            time.sleep(0.5)

            try:
                mesh = load_3d_file(viewer_file.getvalue(), os.path.splitext(viewer_file.name)[1].lower())
                status_text.text(t("viewer_status_processing"))
                progress_bar.progress(60)
                time.sleep(0.5)

                if mesh and hasattr(mesh, 'vertices') and len(mesh.vertices) > 0:
                    st.success(t("viewer_success", vertices=len(mesh.vertices), faces=len(mesh.faces)))
                    try:
                        mesh.merge_vertices()
                        mesh.remove_degenerate_faces()
                        mesh.remove_unreferenced_vertices()
                        trimesh.repair.fix_normals(mesh)
                    except Exception:
                        pass

                    if mesh is None or not hasattr(mesh, 'faces') or len(mesh.faces) == 0:
                        st.error(t("viewer_error_processing"))
                    else:
                        vertices = mesh.vertices.copy()
                        rotated = np.empty_like(vertices)
                        rotated[:, 0] = vertices[:, 0]
                        rotated[:, 1] = vertices[:, 2]
                        rotated[:, 2] = -vertices[:, 1]
                        vertices = rotated

                        min_x, min_y, min_z = vertices.min(axis=0)
                        max_x, max_y, max_z = vertices.max(axis=0)
                        center_x = (min_x + max_x) / 2
                        center_z = (min_z + max_z) / 2

                        vertices[:, 0] -= center_x
                        vertices[:, 1] -= min_y
                        vertices[:, 2] -= center_z

                        faces = mesh.faces.tolist() if hasattr(mesh, 'faces') else mesh.triangles.tolist()
                        mesh_data = {"vertices": vertices.tolist(), "faces": faces}
                        mesh_json = json.dumps(mesh_data)

                        status_text.text(t("viewer_status_building"))
                        progress_bar.progress(100)
                        time.sleep(0.5)

                        viewer_html = """
                        <html><head><style>
                        body{margin:0;overflow:hidden;background:#f0f2f6;}
                        #c{width:100%;height:550px;display:block;}
                        #info{position:absolute;bottom:10px;left:50%;transform:translateX(-50%);color:#555;font-family:Arial;font-size:12px;background:rgba(255,255,255,0.85);padding:6px 16px;border-radius:20px;box-shadow:0 2px 6px rgba(0,0,0,0.1);}
                        .legend{position:absolute;top:10px;left:10px;color:#333;font-family:Arial;font-size:11px;background:rgba(255,255,255,0.9);padding:8px 12px;border-radius:8px;border:1px solid #ddd;}
                        .legend span{display:inline-block;width:12px;height:12px;margin-right:4px;border-radius:2px;}
                        .axis-x{background:#ff4444;}.axis-y{background:#44ff44;}.axis-z{background:#4444ff;}
                        </style>
                        <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
                        <script src="https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/controls/OrbitControls.js"></script>
                        </head><body>
                        <div id="c"></div>
                        <div class="legend"><span class="axis-x"></span> """ + t("viewer_legend_axes") + """</div>
                        <div id="info">""" + t("viewer_legend") + """</div>
                        <script>
                        const data = """ + mesh_json + """;
                        const container = document.getElementById('c');
                        const scene = new THREE.Scene();
                        scene.background = new THREE.Color(0xf0f2f6);
                        const camera = new THREE.PerspectiveCamera(45, container.clientWidth/container.clientHeight, 0.1, 5000);
                        camera.position.set(15,12,15);
                        camera.lookAt(0,3,0);
                        const renderer = new THREE.WebGLRenderer({antialias:true});
                        renderer.setPixelRatio(window.devicePixelRatio);
                        renderer.setSize(container.clientWidth, container.clientHeight);
                        renderer.shadowMap.enabled = true;
                        renderer.shadowMap.type = THREE.PCFSoftShadowMap;
                        container.appendChild(renderer.domElement);
                        const controls = new THREE.OrbitControls(camera, renderer.domElement);
                        controls.enableDamping = true;
                        controls.dampingFactor = 0.08;
                        controls.target.set(0,3,0);
                        controls.screenSpacePanning = true;
                        controls.update();
                        const al = 8;
                        scene.add(new THREE.ArrowHelper(new THREE.Vector3(1,0,0), new THREE.Vector3(0,0,0), al, 0xff4444, 0.5, 0.3));
                        scene.add(new THREE.ArrowHelper(new THREE.Vector3(0,1,0), new THREE.Vector3(0,0,0), al, 0x44ff44, 0.5, 0.3));
                        scene.add(new THREE.ArrowHelper(new THREE.Vector3(0,0,1), new THREE.Vector3(0,0,0), al, 0x4444ff, 0.5, 0.3));
                        const grid = new THREE.GridHelper(40, 40, 0x888888, 0xcccccc);
                        grid.position.y = 0;
                        scene.add(grid);
                        scene.add(new THREE.AmbientLight(0xffffff, 0.6));
                        const dirLight = new THREE.DirectionalLight(0xffffff, 0.9);
                        dirLight.position.set(15, 30, 15);
                        dirLight.castShadow = true;
                        dirLight.shadow.mapSize.width = 2048;
                        dirLight.shadow.mapSize.height = 2048;
                        scene.add(dirLight);
                        const fillLight = new THREE.DirectionalLight(0xffffff, 0.35);
                        fillLight.position.set(-15, 10, -15);
                        scene.add(fillLight);
                        if (data.vertices && data.vertices.length > 0) {
                            const geo = new THREE.BufferGeometry();
                            const verts = new Float32Array(data.vertices.flat());
                            geo.setAttribute('position', new THREE.BufferAttribute(verts, 3));
                            if (data.faces && data.faces.length > 0) {
                                geo.setIndex(new THREE.BufferAttribute(new Uint32Array(data.faces.flat()), 1));
                                geo.computeVertexNormals();
                            }
                            const mat = new THREE.MeshStandardMaterial({color: 0x1f77b4, roughness: 0.45, metalness: 0.1, flatShading: false, side: THREE.DoubleSide});
                            const mesh = new THREE.Mesh(geo, mat);
                            mesh.castShadow = true;
                            mesh.receiveShadow = true;
                            const box = new THREE.Box3().setFromObject(mesh);
                            const size = box.getSize(new THREE.Vector3());
                            const maxDim = Math.max(size.x, size.y, size.z);
                            if (maxDim > 0 && maxDim < 1000) {
                                const s = 10 / maxDim;
                                mesh.scale.set(s, s, s);
                            }
                            scene.add(mesh);
                        }
                        function animate() {
                            requestAnimationFrame(animate);
                            controls.update();
                            renderer.render(scene, camera);
                        }
                        animate();
                        window.addEventListener('resize', () => {
                            camera.aspect = container.clientWidth / container.clientHeight;
                            camera.updateProjectionMatrix();
                            renderer.setSize(container.clientWidth, container.clientHeight);
                        });
                        </script></body></html>
                        """
                        st.components.v1.html(viewer_html, height=580)

                        # --- SEZIONE CONDIVISIONE (v8.0) ---
                        render_share_section(viewer_file, t, lang=st.session_state.lang)
                else:
                    st.warning(t("viewer_warning_no_model"))
            except Exception as e:
                st.error(t("viewer_error_generic", error=e))
    with col_side:
        render_sponsor_band(st.session_state.lang)
        sponsor_band_placeholder(st.session_state.lang)

# --- CONVERTI FORMATI ---
elif page == "Converti Formati":
    col_main, col_side = st.columns([3, 1], gap="large")
    with col_main:
        st.header(t("convert_header"))
        st.markdown(t("convert_subtitle"))
        render_proprietary_formats_help()

        with st.expander(t("convert_expander_note")):
            st.markdown(t("convert_note_text"))

        with st.expander(t("convert_expander_matrix")):
            st.markdown("""
            | Da → A | STL | OBJ | PLY | GLB | GLTF | FBX | 3MF | DAE | WRL | OFF | DXF | PDF |
            |--------|-----|-----|-----|-----|------|-----|------|-----|-----|-----|-----|-----|
            | **STL** | - | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
            | **OBJ** | ✅ | - | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
            | **PLY** | ✅ | ✅ | - | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
            | **GLB** | ✅ | ✅ | ✅ | - | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
            | **GLTF** | ✅ | ✅ | ✅ | ✅ | - | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
            | **FBX** | ✅ | ✅ | ✅ | ✅ | ✅ | - | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
            | **3MF** | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | - | ✅ | ✅ | ✅ | ✅ | ✅ |
            | **DAE** | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | - | ✅ | ✅ | ✅ | ✅ |
            | **WRL** | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | - | ✅ | ✅ | ✅ |
            | **OFF** | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | - | ✅ | ✅ |
            | **DXF** | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | - | ✅ |
            """)
            st.caption(t("convert_caption_matrix"))

        uploaded_file = st.file_uploader(
            t("convert_upload"),
            type=[ext[1:] for ext in ALL_EXTENSIONS],
            key="convert",
            help=t("convert_upload_hint")
        )
        st.caption(t("convert_upload_hint"))

        if uploaded_file:
            file_name = uploaded_file.name
            file_bytes = uploaded_file.getvalue()
            file_extension = os.path.splitext(file_name)[1].lower().replace('.', '')
            file_type, icon = detect_file_type(file_extension)
            st.markdown(f'<div class="file-info-card"><div style="display:flex;align-items:center;gap:10px;"><span style="font-size:1.5rem;">{icon}</span><div><div style="font-weight:600;">{file_name}</div><div style="font-size:0.8rem;color:#666;">{t("convert_file_type", type=file_type, ext=file_extension)}</div></div></div></div>', unsafe_allow_html=True)

            MESH_FORMATS = ["stl", "obj", "ply", "glb", "gltf", "fbx", "3mf", "dae", "wrl", "off"]
            VECTOR_FORMATS = ["svg"]
            DOC_FORMATS = ["pdf", "docx", "xlsx"]
            BIM_FORMATS = ["ifc"]
            GEO_FORMATS = ["shp", "geojson", "kml", "gpx"]

            if file_extension in MESH_FORMATS or file_extension == "dxf":
                target_formats = CONVERSION_MATRIX.get(file_extension, [])
                target_options = [FORMAT_NAMES.get(f, f) for f in target_formats if f != file_extension]

                if not target_options:
                    st.warning(t("convert_warning_no_target"))
                else:
                    target_selected = st.selectbox(t("convert_target_format"), target_options)
                    target_ext = target_selected.split(".")[1].replace(")", "").strip()

                    if st.button(t("convert_button_convert", format=target_selected.split(' ')[0]), type="primary", use_container_width=True):
                        progress_bar = st.progress(0)
                        status_text = st.empty()
                        status_text.text(t("convert_status_loading"))
                        progress_bar.progress(20)
                        time.sleep(0.5)
                        mesh = load_3d_file(file_bytes, file_extension)

                        if mesh and hasattr(mesh, 'vertices') and len(mesh.vertices) > 0:
                            status_text.text(t("convert_status_converting"))
                            progress_bar.progress(70)
                            time.sleep(0.5)
                            result_bytes = convert_mesh(mesh, target_ext)
                            status_text.text(t("convert_status_saving"))
                            progress_bar.progress(100)
                            time.sleep(0.5)

                            if result_bytes:
                                st.success(t("convert_success", format=target_selected.split(' ')[0]))
                                mime_types = {'stl': 'application/octet-stream', 'obj': 'text/plain', 'ply': 'application/octet-stream', 'glb': 'application/octet-stream', 'gltf': 'application/octet-stream', 'fbx': 'application/octet-stream', '3mf': 'application/octet-stream', 'dae': 'application/octet-stream', 'wrl': 'application/octet-stream', 'off': 'application/octet-stream', 'dxf': 'application/dxf', 'pdf': 'application/pdf'}
                                st.info(t("convert_info_ready"))
                                original_name = os.path.splitext(file_name)[0]
                                converted_filename = f"{original_name}.{target_ext}"
                                st.download_button(label=t("convert_button_download", format=target_ext), data=result_bytes, file_name=converted_filename, mime=mime_types.get(target_ext, 'application/octet-stream'), use_container_width=True)
                            else:
                                st.error(t("convert_error", format=target_selected.split(' ')[0]))
                        else:
                            st.error(t("convert_error_load"))

                    st.markdown("---")
                    if st.button(t("convert_button_preview")):
                        st.info(t("convert_info_preview"))
                        mesh_preview = load_3d_file(file_bytes, file_extension)
                        if mesh_preview and hasattr(mesh_preview, 'vertices') and len(mesh_preview.vertices) > 0:
                            try:
                                mesh_preview.merge_vertices()
                                mesh_preview.remove_degenerate_faces()
                                mesh_preview.remove_unreferenced_vertices()
                                trimesh.repair.fix_normals(mesh_preview)
                            except Exception:
                                pass

                            if mesh_preview is None or not hasattr(mesh_preview, 'faces') or len(mesh_preview.faces) == 0:
                                st.error(t("viewer_error_processing"))
                            else:
                                vp = mesh_preview.vertices.copy()
                                rp = np.empty_like(vp)
                                rp[:, 0] = vp[:, 0]
                                rp[:, 1] = vp[:, 2]
                                rp[:, 2] = -vp[:, 1]
                                vp = rp
                                min_x, min_y, min_z = vp.min(axis=0)
                                max_x, max_y, max_z = vp.max(axis=0)
                                vp[:, 0] -= (min_x + max_x) / 2
                                vp[:, 1] -= min_y
                                vp[:, 2] -= (min_z + max_z) / 2
                                mesh_data = {"vertices": vp.tolist(), "faces": mesh_preview.faces.tolist()}
                                mesh_json = json.dumps(mesh_data)
                                viewer_html = """
                                <html><head><style>body{margin:0;overflow:hidden;background:#f0f2f6;}#c{width:100%;height:400px;}</style>
                                <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
                                <script src="https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/controls/OrbitControls.js"></script>
                                </head><body>
                                <div id="c"></div>
                                <script>
                                const data = """ + mesh_json + """;
                                const container = document.getElementById('c');
                                const scene = new THREE.Scene();
                                scene.background = new THREE.Color(0xf0f2f6);
                                const camera = new THREE.PerspectiveCamera(45, container.clientWidth/container.clientHeight, 0.1, 5000);
                                camera.position.set(12,10,12);
                                camera.lookAt(0,2,0);
                                const renderer = new THREE.WebGLRenderer({antialias:true});
                                renderer.setSize(container.clientWidth, container.clientHeight);
                                container.appendChild(renderer.domElement);
                                const controls = new THREE.OrbitControls(camera, renderer.domElement);
                                controls.enableDamping = true;
                                controls.dampingFactor = 0.08;
                                controls.target.set(0,2,0);
                                controls.update();
                                scene.add(new THREE.AmbientLight(0xffffff,0.6));
                                const dl = new THREE.DirectionalLight(0xffffff,0.9);
                                dl.position.set(10,20,10);
                                dl.castShadow=true;
                                scene.add(dl);
                                const dl2 = new THREE.DirectionalLight(0xffffff,0.35);
                                dl2.position.set(-10,0,-10);
                                scene.add(dl2);
                                if(data.vertices && data.vertices.length>0){
                                    const geo = new THREE.BufferGeometry();
                                    geo.setAttribute('position', new THREE.BufferAttribute(new Float32Array(data.vertices.flat()), 3));
                                    if(data.faces && data.faces.length>0){
                                        geo.setIndex(new THREE.BufferAttribute(new Uint32Array(data.faces.flat()), 1));
                                        geo.computeVertexNormals();
                                    }
                                    const mat = new THREE.MeshStandardMaterial({color:0x1f77b4, roughness:0.45, metalness:0.1, flatShading:false, side:THREE.DoubleSide});
                                    const mesh = new THREE.Mesh(geo, mat);
                                    mesh.castShadow = true;
                                    mesh.receiveShadow = true;
                                    const box = new THREE.Box3().setFromObject(mesh);
                                    const size = box.getSize(new THREE.Vector3());
                                    const maxDim = Math.max(size.x,size.y,size.z);
                                    if(maxDim>0 && maxDim<1000){ const s=10/maxDim; mesh.scale.set(s,s,s); }
                                    scene.add(mesh);
                                }
                                function animate(){ requestAnimationFrame(animate); controls.update(); renderer.render(scene,camera); }
                                animate();
                                window.addEventListener('resize', ()=>{
                                    camera.aspect=container.clientWidth/container.clientHeight; camera.updateProjectionMatrix();
                                    renderer.setSize(container.clientWidth, container.clientHeight);
                                });
                                </script></body></html>
                                """
                                st.components.v1.html(viewer_html, height=420)
                        else:
                            st.warning(t("convert_warning_no_preview"))

            elif file_extension == "svg":
                st.info("🎨 **SVG rilevato** — questo è un formato vettoriale, non una mesh 3D.")
                if SVG_AVAILABLE:
                    st.success("✅ Libreria `cairosvg` disponibile.")
                    if st.button("🖼️ Converti SVG in PNG", type="primary", use_container_width=True):
                        try:
                            import cairosvg
                            png_bytes = cairosvg.svg2png(bytestring=file_bytes)
                            st.success("✅ SVG convertito in PNG!")
                            st.download_button(label="📥 Scarica PNG", data=png_bytes, file_name=f"{os.path.splitext(file_name)[0]}.png", mime="image/png", use_container_width=True)
                            st.image(png_bytes, caption="Anteprima", use_column_width=True)
                        except Exception as e:
                            st.error(f"❌ Errore: {e}")
                else:
                    st.warning("⚠️ Libreria `cairosvg` non installata.")

            elif file_extension == "pdf":
                st.info("📄 **PDF rilevato** — questo è un formato documento.")
                is_3d = is_3d_pdf(file_bytes)
                if is_3d:
                    st.success("🎯 **3D PDF rilevato!** Questo PDF contiene un modello 3D.")
                    if FITZ_AVAILABLE:
                        st.info("💡 Libreria `PyMuPDF` disponibile. Estrazione 3D in sviluppo.")
                else:
                    st.warning("⚠️ **PDF standard (non 3D)**: non contiene un modello 3D incorporato.")
                    with st.expander("📖 Come creare un 3D PDF", expanded=True):
                        st.markdown(t("pdf_no_3d_howto_steps"))
                    st.info(t("pdf_no_3d_alternative"))
                if PDF_AVAILABLE:
                    try:
                        pdf_reader = PdfReader(io.BytesIO(file_bytes))
                        st.metric("Pagine", len(pdf_reader.pages))
                    except Exception:
                        pass

            elif file_extension == "docx":
                st.info("📝 **DOCX rilevato** — documento Word.")
                if DOCX_AVAILABLE:
                    try:
                        doc = docx.Document(io.BytesIO(file_bytes))
                        st.metric("Paragrafi", len(doc.paragraphs))
                    except Exception as e:
                        st.warning(f"Impossibile leggere: {e}")

            elif file_extension == "xlsx":
                st.info("📊 **XLSX rilevato** — foglio di calcolo.")
                if XLSX_AVAILABLE:
                    try:
                        wb = openpyxl.load_workbook(io.BytesIO(file_bytes))
                        st.metric("Fogli", len(wb.sheetnames))
                    except Exception as e:
                        st.warning(f"Impossibile leggere: {e}")

            elif file_extension == "ifc":
                st.info("🏗️ **IFC rilevato** — formato BIM.")
                if IFC_AVAILABLE:
                    try:
                        with tempfile.NamedTemporaryFile(suffix='.ifc', delete=False) as tmp_ifc:
                            tmp_ifc.write(file_bytes)
                            tmp_ifc_path = tmp_ifc.name
                        try:
                            ifc_file = ifcopenshell.open(tmp_ifc_path)
                            st.metric("Progetti", len(ifc_file.by_type('IfcProject')))
                        finally:
                            try:
                                os.unlink(tmp_ifc_path)
                            except:
                                pass
                    except Exception as e:
                        st.warning(f"Impossibile leggere: {e}")

            elif file_extension in GEO_FORMATS:
                st.info(f"🌍 **{file_extension.upper()} rilevato** — formato geospaziale.")
                if GEOPANDAS_AVAILABLE:
                    try:
                        gdf = gpd.read_file(io.BytesIO(file_bytes))
                        st.metric("Features", len(gdf))
                    except Exception as e:
                        st.warning(f"Impossibile leggere: {e}")

            else:
                st.warning(f"⚠️ Formato **.{file_extension.upper()}** non supportato.")
                st.info("💡 Formati supportati: **STL, OBJ, PLY, GLB, GLTF, FBX, 3MF, DAE, WRL, OFF, DXF, PDF, SVG, DOCX, XLSX, IFC, SHP, GeoJSON, KML, GPX**.")

    with col_side:
        render_sponsor_band(st.session_state.lang)
        sponsor_band_placeholder(st.session_state.lang)

# --- PROGETTO ARTIFIX ---
elif page == "Progetto ArtiFix":
    col_main, col_side = st.columns([3, 1], gap="large")
    with col_main:
        st.header(t("project_header"))
        st.markdown(t("project_text"))
        st.divider()
        st.subheader(t("project_contact"))
        st.write(t("project_contact_text"))
        with st.form("contatti"):
            nome_input = st.text_input(t("project_form_name"))
            email_input = st.text_input(t("project_form_email"))
            messaggio_input = st.text_area(t("project_form_message"))
            inviato = st.form_submit_button(t("project_form_submit"))
            if inviato:
                if nome_input and email_input and messaggio_input:
                    risultato = invia_email(nome_input, email_input, messaggio_input)
                    if risultato == True:
                        st.success(t("project_success"))
                    else:
                        st.error(t("project_error", error=risultato))
                else:
                    st.warning(t("project_warning"))
    with col_side:
        render_sponsor_band(st.session_state.lang)
        sponsor_band_placeholder(st.session_state.lang)

# --- DIVENTA SPONSOR ---
elif page == "Diventa Sponsor":
    col_main, col_side = st.columns([3, 1], gap="large")
    with col_main:
        st.header(t("sponsor_header"))
        st.markdown(t("sponsor_intro"))
        st.divider()
        st.subheader(t("sponsor_format_title"))
        st.markdown(t("sponsor_format_text"))
        st.divider()
        st.subheader(t("sponsor_how_title"))
        st.markdown(t("sponsor_how_text"))
        st.markdown(f"""
            <div style="text-align:center; margin: 20px 0;">
                <a href="{DONATE_LINK}" target="_blank" style="display:inline-block; background:#0070ba; color:white; padding:14px 28px; border-radius:8px; text-decoration:none; font-weight:700; font-size:16px; box-shadow: 0 4px 12px rgba(0,112,186,0.3);">{t("sponsor_donate_button")}</a>
            </div>
        """, unsafe_allow_html=True)
        st.divider()
        st.subheader(t("sponsor_form_title"))
        st.caption(t("sponsor_form_caption"))
        with st.form("sponsor_form"):
            nome_brand = st.text_input(t("sponsor_form_brand"))
            email_ref = st.text_input(t("sponsor_form_email"))
            sito = st.text_input(t("sponsor_form_site"))
            logo_url = st.text_input(t("sponsor_form_logo"), placeholder="https://raw.githubusercontent.com/...")
            messaggio = st.text_area(t("sponsor_form_message"))
            invia = st.form_submit_button(t("sponsor_form_submit"), type="primary")
            if invia:
                if nome_brand and email_ref and sito and logo_url:
                    corpo = f"\nNuova richiesta sponsor:\n\n- Brand: {nome_brand}\n- Email: {email_ref}\n- Sito: {sito}\n- Logo URL: {logo_url}\n- Messaggio: {messaggio}\n"
                    esito = invia_email(nome_brand, email_ref, corpo)
                    if esito is True:
                        st.success(t("sponsor_form_success"))
                    else:
                        st.error(t("sponsor_form_error", error=esito))
                else:
                    st.warning(t("sponsor_form_warning"))
        st.info(t("sponsor_form_info"))
    with col_side:
        render_sponsor_band(st.session_state.lang)
        sponsor_band_placeholder(st.session_state.lang)

# --- PRIVACY POLICY ---
elif page == "Privacy Policy":
    st.header(t("privacy_header"))
    st.markdown(t("privacy_subtitle"))
    st.caption(t("privacy_updated"))
    if st.button(t("privacy_back"), key="torna_dashboard_privacy"):
        st.session_state.page_attuale = "Dashboard"
        st.rerun()
    st.markdown("---")
    st.markdown(t("privacy_content"))
    st.markdown("---")
    if st.button(t("privacy_back"), key="torna_dashboard_privacy_basso"):
        st.session_state.page_attuale = "Dashboard"
        st.rerun()

# --- COOKIE POLICY ---
elif page == "Cookie Policy":
    st.header(t("cookie_policy_header"))
    st.markdown(t("cookie_policy_subtitle"))
    st.caption(t("cookie_policy_updated"))
    if st.button(t("cookie_policy_back"), key="torna_dashboard_alto"):
        st.session_state.page_attuale = "Dashboard"
        st.rerun()
    st.markdown("---")
    st.markdown(t("cookie_policy_content"))
    st.markdown("---")
    if st.button(t("cookie_policy_back"), key="torna_dashboard_basso"):
        st.session_state.page_attuale = "Dashboard"
        st.rerun()

# --- FOOTER GLOBALE ---
st.markdown("---")
st.markdown(f'<div class="footer-artifix">{t("footer")}</div>', unsafe_allow_html=True)

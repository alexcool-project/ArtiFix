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

    /* ===== HTML 3D VIEWER INFO SECTION ===== */
    .html-viewer-intro {
        background: linear-gradient(135deg, #e8f4fd 0%, #f0f8ff 100%);
        border-left: 4px solid #1f77b4;
        border-radius: 10px;
        padding: 1.2rem 1.5rem;
        margin-bottom: 1.5rem;
    }
    .html-viewer-intro h3 {
        color: #1f77b4;
        margin-top: 0;
        margin-bottom: 0.8rem;
        font-size: 1.2rem;
    }
    .html-viewer-intro p {
        color: #333;
        line-height: 1.6;
        margin-bottom: 0.5rem;
    }
    .html-viewer-benefits {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 12px;
        margin: 1rem 0 1.5rem 0;
    }
    .html-viewer-benefit {
        background: #ffffff;
        border: 1px solid #e0e0e0;
        border-radius: 8px;
        padding: 12px 14px;
        font-size: 0.9rem;
        color: #333;
        transition: transform 0.15s ease, box-shadow 0.15s ease;
    }
    .html-viewer-benefit:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(31, 119, 180, 0.15);
    }
    .html-viewer-benefit .benefit-icon {
        font-size: 1.3rem;
        display: block;
        margin-bottom: 6px;
    }
    .html-viewer-benefit .benefit-title {
        font-weight: 700;
        color: #1f77b4;
        display: block;
        margin-bottom: 4px;
    }
    .html-viewer-benefit .benefit-desc {
        color: #555;
        line-height: 1.4;
        font-size: 0.85rem;
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
# FUNZIONI HELPER PER FORMATI PROPRIETARI, 3D PDF E HTML VIEWER
# ============================================================

def render_html_viewer_info(t_func):
    """
    Mostra una sezione informativa sull'HTML 3D Viewer.
    """
    st.markdown(f"""
    <div class="html-viewer-intro">
        <h3>{t_func('html_viewer_title')}</h3>
        <p>{t_func('html_viewer_intro')}</p>
        <p>{t_func('html_viewer_modes')}</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="html-viewer-benefits">
        <div class="html-viewer-benefit">
            <span class="benefit-icon">⚡</span>
            <span class="benefit-title">{t_func('html_viewer_benefit1_title')}</span>
            <span class="benefit-desc">{t_func('html_viewer_benefit1_desc')}</span>
        </div>
        <div class="html-viewer-benefit">
            <span class="benefit-icon">🚫</span>
            <span class="benefit-title">{t_func('html_viewer_benefit2_title')}</span>
            <span class="benefit-desc">{t_func('html_viewer_benefit2_desc')}</span>
        </div>
        <div class="html-viewer-benefit">
            <span class="benefit-icon">📱</span>
            <span class="benefit-title">{t_func('html_viewer_benefit3_title')}</span>
            <span class="benefit-desc">{t_func('html_viewer_benefit3_desc')}</span>
        </div>
        <div class="html-viewer-benefit">
            <span class="benefit-icon">🔄</span>
            <span class="benefit-title">{t_func('html_viewer_benefit4_title')}</span>
            <span class="benefit-desc">{t_func('html_viewer_benefit4_desc')}</span>
        </div>
        <div class="html-viewer-benefit">
            <span class="benefit-icon">🔗</span>
            <span class="benefit-title">{t_func('html_viewer_benefit5_title')}</span>
            <span class="benefit-desc">{t_func('html_viewer_benefit5_desc')}</span>
        </div>
        <div class="html-viewer-benefit">
            <span class="benefit-icon">💾</span>
            <span class="benefit-title">{t_func('html_viewer_benefit6_title')}</span>
            <span class="benefit-desc">{t_func('html_viewer_benefit6_desc')}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_proprietary_formats_help():
    """Mostra una tendina (expander) con le note sui formati proprietari."""
    with st.expander(t("notes_expander_title"), expanded=False):
        st.markdown(t("notes_expander_intro"))
        st.markdown("---")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(t("notes_expander_native"))
        with col2:
            st.markdown(t("notes_expander_not_supported"))
        st.markdown("---")
        st.markdown(t("notes_expander_howto"))
        st.markdown(t("notes_expander_steps"))
        st.info(t("notes_expander_tip"))
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

# --- CONTROLLO COOKIE BANNER ---
if COOKIE_LIB and st.session_state.cookie_consent is None:
    with st.container():
        st.markdown("---")
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown(
                f"""
                <div style="background: #fff3cd; border: 1px solid #ffc107; border-radius: 8px; padding: 12px;">
                    <strong>🍪 {t('cookie_banner_title')}</strong><br>
                    <span style="font-size: 0.9rem;">{t('cookie_banner_text')}</span>
                </div>
                """,
                unsafe_allow_html=True
            )
        with col2:
            if st.button(t("cookie_accept"), key="accept_cookies"):
                st.session_state.cookie_consent = "accepted"
                cookie_controller.set('cookie_consent', 'accepted')
                st.rerun()
        st.markdown("---")

# --- CONTENUTO PAGINE ---
if st.session_state.page_attuale == "Dashboard":
    st.markdown(f'<div class="main-header">{t("dashboard_title")}</div>', unsafe_allow_html=True)
    
    # Logo principale
    if CUBO_URL:
        st.markdown(f'<div class="logo-container"><img src="{CUBO_URL}" alt="ArtiFix Cubo Logo"></div>', unsafe_allow_html=True)
    
    st.markdown(f"### {t('dashboard_subtitle')}")
    st.markdown(t("dashboard_description"))
    
    st.markdown("---")
    
    # Metriche
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">15+</div>
            <div class="metric-label">{t('dashboard_metric_formats')}</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">3D</div>
            <div class="metric-label">{t('dashboard_metric_viewer')}</div>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">100%</div>
            <div class="metric-label">{t('dashboard_metric_free')}</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Sponsor band
    sponsor_band_placeholder()

elif st.session_state.page_attuale == "Ripara File":
    st.markdown(f"## {t('repair_title')}")
    st.info(t("repair_info"))
    
    uploaded_file = st.file_uploader(
        t("repair_upload"),
        type=[ext.replace('.', '') for ext in ALL_EXTENSIONS],
        key="repair_uploader"
    )
    
    if uploaded_file:
        file_bytes = uploaded_file.read()
        result = process_file(file_bytes, uploaded_file.name)
        
        st.markdown("---")
        st.markdown(f"### {t('repair_result')}")
        
        if result["success"]:
            st.success(result["message"])
            st.markdown(f"""
            <div class="file-info-card">
                <strong>{result['icon']} {result['type']}</strong><br>
                {t('repair_file_name')}: {uploaded_file.name}<br>
                {t('repair_file_size')}: {len(file_bytes) / 1024:.1f} KB
            </div>
            """, unsafe_allow_html=True)
            
            # Se è un file 3D, mostra info aggiuntive
            if "mesh" in result.get("info", {}):
                mesh = result["info"]["mesh"]
                st.markdown(f"""
                - **Vertici**: {len(mesh.vertices)}
                - **Facce**: {len(mesh.faces)}
                - **Bounding Box**: {mesh.bounds.tolist() if hasattr(mesh, 'bounds') else 'N/A'}
                """)
        else:
            st.error(result["message"])
    
    # Note formati proprietari
    render_proprietary_formats_help()

elif st.session_state.page_attuale == "Viewer 3D":
    st.markdown(f"## {t('viewer_title')}")
    
    # Info HTML viewer
    render_html_viewer_info(t)
    
    # Upload per viewer
    viewer_file = st.file_uploader(
        t("viewer_upload"),
        type=['stl', 'obj', 'ply', 'glb', 'gltf', 'fbx', '3mf', 'dae', 'wrl', 'off'],
        key="viewer_uploader"
    )
    
    if viewer_file:
        file_bytes = viewer_file.read()
        file_ext = os.path.splitext(viewer_file.name)[1].lower().replace('.', '')
        
        mesh = load_3d_file(file_bytes, file_ext)
        if mesh and hasattr(mesh, 'vertices') and len(mesh.vertices) > 0:
            st.success(f"✅ {t('viewer_loaded')}: {len(mesh.vertices)} vertici, {len(mesh.faces)} facce")
            
            # Statistiche
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric(t("viewer_vertices"), f"{len(mesh.vertices):,}")
            with col2:
                st.metric(t("viewer_faces"), f"{len(mesh.faces):,}")
            with col3:
                st.metric(t("viewer_watertight"), "✅" if mesh.is_watertight else "❌")
            
            # Sezione condivisione (con try/except per evitare loop)
            try:
                render_share_section(mesh, viewer_file.name, st.session_state.lang)
            except Exception as e:
                st.warning(f"Condivisione non disponibile: {e}")
        else:
            st.error(t("viewer_error"))
    
    # Guida ai formati
    render_proprietary_formats_help()

elif st.session_state.page_attuale == "Converti Formati":
    st.markdown(f"## {t('convert_title')}")
    st.markdown(t("convert_description"))
    
    convert_file = st.file_uploader(
        t("convert_upload"),
        type=['stl', 'obj', 'ply', 'glb', 'gltf', 'fbx', '3mf', 'dae', 'wrl', 'off', 'dxf'],
        key="convert_uploader"
    )
    
    if convert_file:
        file_bytes = convert_file.read()
        file_ext = os.path.splitext(convert_file.name)[1].lower().replace('.', '')
        
        mesh = load_3d_file(file_bytes, file_ext)
        if mesh and hasattr(mesh, 'vertices') and len(mesh.vertices) > 0:
            st.success(f"✅ {len(mesh.vertices)} vertici, {len(mesh.faces)} facce")
            
            # Selezione formato di output
            available_formats = CONVERSION_MATRIX.get(file_ext, [])
            if available_formats:
                target_format = st.selectbox(
                    t("convert_target"),
                    available_formats,
                    format_func=lambda x: FORMAT_NAMES.get(x, x.upper())
                )
                
                if st.button(t("convert_button"), type="primary"):
                    with st.spinner(t("convert_converting")):
                        output_bytes = convert_mesh(mesh, target_format)
                        if output_bytes:
                            st.success(t("convert_success"))
                            st.download_button(
                                label=f"📥 {t('convert_download')} {FORMAT_NAMES.get(target_format, target_format.upper())}",
                                data=output_bytes,
                                file_name=f"converted.{target_format}",
                                mime="application/octet-stream"
                            )
                        else:
                            st.error(t("convert_error"))
            else:
                st.warning(t("convert_no_formats"))
        else:
            st.error(t("convert_load_error"))
    
    render_proprietary_formats_help()

elif st.session_state.page_attuale == "Progetto ArtiFix":
    st.markdown(f"## {t('project_title')}")
    st.markdown(t("project_description"))
    
    st.markdown("---")
    st.markdown(f"### {t('project_roadmap')}")
    st.markdown("""
    - ✅ Convertitore base STL/OBJ/PLY
    - ✅ Supporto GLB/GLTF/FBX
    - ✅ Viewer 3D integrato
    - ✅ Sistema sponsor
    - ✅ Internazionalizzazione IT/EN
    - 🔄 Supporto 3D PDF avanzato
    - 📋 API pubblica
    - 📋 App desktop
    """)
    
    st.markdown("---")
    st.markdown(f"### {t('project_support')}")
    st.markdown(
        f"""
        <a href="{DONATE_LINK}" target="_blank" class="guide-button">
            {t('nav_donate')}
        </a>
        """,
        unsafe_allow_html=True
    )

elif st.session_state.page_attuale == "Diventa Sponsor":
    st.markdown(f"## {t('sponsor_title')}")
    st.markdown(t("sponsor_description"))
    
    sponsors = load_sponsors()
    if sponsors:
        st.markdown(f"### {t('sponsor_current')}")
        render_sponsor_band(sponsors)
    else:
        st.info(t("sponsor_no_sponsors"))
    
    st.markdown("---")
    st.markdown(f"### {t('sponsor_howto')}")
    st.markdown(t("sponsor_howto_text"))
    
    st.markdown(
        f"""
        <div style="text-align: center; margin: 2rem 0;">
            <a href="{SPONSOR_MAILTO}" class="guide-button">
                📧 {t('sponsor_contact')}
            </a>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    st.markdown(
        f"""
        <div style="text-align: center;">
            <a href="{DONATE_LINK}" target="_blank" style="background: #28a745; color: white; padding: 12px 32px; border-radius: 8px; text-decoration: none; font-weight: 700; font-size: 16px; display: inline-block;">
                💳 {t('sponsor_donate')}
            </a>
        </div>
        """,
        unsafe_allow_html=True
    )

elif st.session_state.page_attuale == "Privacy Policy":
    st.markdown(f"## {t('privacy_title')}")
    st.markdown(t("privacy_content"))
    if st.button(f"← {t('back_to_home')}", key="back_privacy"):
        st.session_state.page_attuale = "Dashboard"
        st.rerun()

elif st.session_state.page_attuale == "Cookie Policy":
    st.markdown(f"## {t('cookie_title')}")
    st.markdown(t("cookie_content"))
    if st.button(f"← {t('back_to_home')}", key="back_cookie"):
        st.session_state.page_attuale = "Dashboard"
        st.rerun()

# --- FOOTER ---
st.markdown(f"""
<div class="footer-artifix">
    © {datetime.now().year} ArtiFix - Universal CAD/CAM Repair | 
    <a href="https://www.artifix.it" target="_blank" style="color: #1f77b4;">www.artifix.it</a>
</div>
""", unsafe_allow_html=True)

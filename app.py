import streamlit as st

st.set_page_config(
    page_title="ArtiFix - Universal CAD/CAM Repair",
    page_icon="https://raw.githubusercontent.com/alexcool-project/Artifix/main/docs/images/ArchiFix_cubo-logo.png",
    layout="wide",
    initial_sidebar_state="expanded",
)

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
import requests

# --- MODULO SPONSOR (Google Sheets) ---
try:
    from sponsors import load_sponsors, render_sponsor_band, sponsor_band_placeholder
    SPONSORS_AVAILABLE = True
except ImportError:
    SPONSORS_AVAILABLE = False
    def load_sponsors(): return []
    def render_sponsor_band(*a, **k): pass
    def sponsor_band_placeholder(): pass

# --- MODULO TRADUZIONI (IT/EN) ---
from translations import TRANSLATIONS, get_text, detect_browser_language

# --- UTILITY CONDIVISIONE VIEWER (v8.0) ---
try:
    from share_utils import render_share_section
    SHARE_AVAILABLE = True
except ImportError:
    SHARE_AVAILABLE = False
    def render_share_section(*a, **k): pass

# --- LIBRERIA COOKIE (OPZIONALE) ---
try:
    from streamlit_cookies_controller import CookieController
    cookie_controller = CookieController()
    COOKIE_LIB = True
except ImportError:
    COOKIE_LIB = False

# --- GOOGLE SHEETS (metriche dinamiche) ---
try:
    import gspread
    from google.oauth2.service_account import Credentials
    GSPREAD_AVAILABLE = True
except ImportError:
    GSPREAD_AVAILABLE = False

# --- LINK DIRETTI DELLE IMMAGINI (GitHub Raw) ---
CUBO_URL = "https://raw.githubusercontent.com/alexcool-project/Artifix/main/docs/images/ArchiFix_cubo-logo.png"
LOGO_URL = "https://raw.githubusercontent.com/alexcool-project/Artifix/main/docs/images/Artifix_logo.png"

# --- LINK PAGAMENTO (PayPal) ---
DONATE_LINK = "https://www.paypal.com/ncp/payment/9C4ZLMBHBDXVS"

# --- GOOGLE SHEETS CONFIG ---
SCOPES = ["https://www.googleapis.com/auth/spreadsheets.readonly"]
SPONSORS_SHEET_ID = "16m8gY3YktT2ysYAkKqHGC28VX1qGghx6PL2typXK2b4"
GITHUB_REPO = "alexcool-project/Artifix"
GITHUB_BRANCH = "main"

FALLBACK_METRICS = {
    "file_riparati": {"value": "14.280", "unit": "", "icon": "🛠️"},
    "conversioni": {"value": "38.910", "unit": "", "icon": "🔄"},
    "formati_supportati": {"value": "50", "unit": "+", "icon": "📁"},
    "status": {"value": "Online", "unit": "", "icon": "🟢"},
    "uptime_30d": {"value": "99.8", "unit": "%", "icon": "⏱️"},
    "sponsor_attivi": {"value": "3", "unit": "", "icon": "🤝"},
}

SPONSOR_MAILTO = (
    "mailto:info@artifix.it"
    "?subject=Richiesta%20Sponsorizzazione%20ArtiFix"
    "&body=Buongiorno%20Team%20ArtiFix%2C%0D%0A%0D%0A"
    "Sono%20interessato%2Fa%20alla%20sponsorizzazione%20di%20ArtiFix.%0D%0A%0D%0A"
    "Nome%20Azienda%3A%20%0D%0ASito%20Web%3A%20%0D%0AEmail%3A%20%0D%0A"
    "Telefono%3A%20%0D%0ALogo%20(URL)%3A%20%0D%0AMessaggio%3A%0D%0A"
)

# --- STATO LINGUA ---
if 'lang' not in st.session_state:
    try:
        st.session_state.lang = detect_browser_language()
    except Exception:
        st.session_state.lang = "it"

def t(key, **kwargs):
    return get_text(key, st.session_state.lang, **kwargs)

# --- SEO META TAG ---
st.markdown("""
<title>ArtiFix - Convertitore CAD/CAM Universale | Converti STL, OBJ, PLY in 3D PDF</title>
<meta name="description" content="ArtiFix è la piattaforma professionale per convertire file CAD/CAM (STL, OBJ, PLY, GLB, GLTF, FBX, DAE, DXF) in 3D PDF, STL, OBJ, GLTF e altri formati." />
<meta name="robots" content="index, follow" />
""", unsafe_allow_html=True)

# --- CSS ---
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
    a.guide-button {
        color: #ffffff !important; text-decoration: none !important;
        background: #1f77b4 !important; display: inline-block !important;
        padding: 10px 24px !important; border-radius: 8px !important;
        font-weight: 700 !important; font-size: 14px !important; border: none !important;
    }
    a.guide-button:hover { background: #155a8a !important; }
    .html-viewer-intro {
        background: linear-gradient(135deg, #e8f4fd 0%, #f0f8ff 100%);
        border-left: 4px solid #1f77b4; border-radius: 10px;
        padding: 1.2rem 1.5rem; margin-bottom: 1.5rem;
    }
    .html-viewer-intro h3 { color: #1f77b4; margin-top: 0; }
    .html-viewer-benefits { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 12px; margin: 1rem 0; }
    .html-viewer-benefit { background: #fff; border: 1px solid #e0e0e0; border-radius: 8px; padding: 12px 14px; font-size: 0.9rem; }
    .html-viewer-benefit .benefit-icon { font-size: 1.3rem; display: block; margin-bottom: 6px; }
    .html-viewer-benefit .benefit-title { font-weight: 700; color: #1f77b4; display: block; }
</style>
""", unsafe_allow_html=True)

# --- IMPORT LIBRERIE OPZIONALI ---
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
    import geopandas as gpd
    GEOPANDAS_AVAILABLE = True
except (ImportError, OSError):
    GEOPANDAS_AVAILABLE = False

try:
    import ifcopenshell
    IFC_AVAILABLE = True
except ImportError:
    IFC_AVAILABLE = False

# --- STATO PAGINE E COOKIE ---
if 'page_attuale' not in st.session_state:
    st.session_state.page_attuale = "Dashboard"

if 'cookie_consent' not in st.session_state:
    if COOKIE_LIB:
        try:
            st.session_state.cookie_consent = cookie_controller.get('cookie_consent')
        except Exception:
            st.session_state.cookie_consent = None
    else:
        st.session_state.cookie_consent = None

# --- FORMATI SUPPORTATI ---
SUPPORTED_FORMATS = {
    "CAD 2D": {"extensions": [".dxf"], "icon": "📐", "description": "File CAD (DXF)"},
    "CAD 3D & Mesh": {"extensions": [".stl", ".obj", ".ply", ".glb", ".gltf", ".fbx", ".3mf", ".dae", ".wrl", ".off", ".u3d"], "icon": "🧊", "description": "Mesh 3D"},
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
    'stl': 'STL (.stl)', 'obj': 'OBJ (.obj)', 'ply': 'PLY (.ply)',
    'glb': 'GLB (.glb)', 'gltf': 'GLTF (.gltf)', 'fbx': 'FBX (.fbx)',
    '3mf': '3MF (.3mf)', 'dae': 'DAE (.dae)', 'wrl': 'WRL (.wrl)',
    'off': 'OFF (.off)', 'u3d': 'U3D (.u3d)', 'dxf': 'DXF (.dxf)',
    'pdf': '3D PDF (.pdf)',
}

# --- FUNZIONI 3D ---
def load_3d_file(file_bytes, file_extension):
    try:
        ext = file_extension.lower().replace('.', '')
        format_map = {'stl':'stl', 'obj':'obj', 'ply':'ply', 'glb':'glb', 'gltf':'gltf',
                      'fbx':'fbx', '3mf':'3mf', 'dae':'dae', 'wrl':'wrl', 'off':'off', 'u3d':'u3d'}
        ftype = format_map.get(ext, ext)
        if ext in ['obj', 'dae']:
            for method in [ftype, None]:
                try:
                    mesh = trimesh.load(io.BytesIO(file_bytes), file_type=method, force='mesh') if method else trimesh.load(io.BytesIO(file_bytes))
                    if mesh is not None and hasattr(mesh, 'vertices') and len(mesh.vertices) > 0:
                        return mesh
                except Exception:
                    continue
            return None
        else:
            mesh = trimesh.load(io.BytesIO(file_bytes), file_type=ftype)
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
        fmt = target_format.lower().replace('.', '')
        if fmt == 'pdf':
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
        elif fmt == 'stl':  return trimesh.exchange.stl.export_stl(mesh)
        elif fmt == 'obj':  return trimesh.exchange.obj.export_obj(mesh)
        elif fmt == 'ply':  return trimesh.exchange.ply.export_ply(mesh)
        elif fmt == 'glb':  return trimesh.exchange.gltf.export_glb(mesh)
        elif fmt == 'gltf': return trimesh.exchange.gltf.export_gltf(mesh)
        elif fmt == 'fbx':  return trimesh.exchange.fbx.export_fbx(mesh)
        elif fmt == '3mf':  return trimesh.exchange.threeMF.export_3mf(mesh)
        elif fmt == 'dae':  return trimesh.exchange.dae.export_dae(mesh)
        elif fmt == 'wrl':  return trimesh.exchange.vrml.export_vrml(mesh)
        elif fmt == 'off':  return trimesh.exchange.off.export_off(mesh)
        elif fmt == 'dxf':
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
        return None
    except Exception:
        return None


def process_file(file_bytes, file_name):
    file_extension = os.path.splitext(file_name)[1].lower().replace('.', '')
    result = {"success": False, "message": "", "type": "", "icon": "❓", "info": {}}
    try:
        if file_extension in ['stl','obj','ply','glb','gltf','fbx','3mf','dae','wrl','off','u3d']:
            mesh = load_3d_file(file_bytes, file_extension)
            if mesh and hasattr(mesh, 'vertices') and len(mesh.vertices) > 0:
                result["success"] = True
                result["message"] = f"✅ Mesh: {len(mesh.vertices)} vertici, {len(mesh.faces)} facce"
                result["info"] = {"vertices": len(mesh.vertices), "faces": len(mesh.faces), "mesh": mesh}
            else:
                result["message"] = "❌ File 3D non valido."
        elif file_extension == 'dxf':
            dxf_doc = ezdxf.read(io.BytesIO(file_bytes))
            result["success"] = True
            result["message"] = f"📐 DXF: {len(dxf_doc.entities)} entità"
        elif file_extension == 'pdf' and PDF_AVAILABLE:
            pdf_reader = PdfReader(io.BytesIO(file_bytes))
            result["success"] = True
            result["message"] = f"📄 PDF: {len(pdf_reader.pages)} pagine"
        else:
            result["message"] = f"❌ Formato {file_extension} non supportato."
    except Exception as e:
        result["message"] = f"❌ Errore: {str(e)}"
    return result


# --- METRICHE DINAMICHE ---
def _format_value(raw_value):
    value_str = str(raw_value).strip()
    if not value_str:
        return ""
    normalized = value_str.replace(",", "")
    if "." in normalized:
        try:
            return f"{float(normalized):.2f}".rstrip("0").rstrip(".").replace(".", ",")
        except (ValueError, TypeError):
            pass
    try:
        return f"{int(normalized):,}".replace(",", ".")
    except (ValueError, TypeError):
        pass
    return value_str


def _format_timestamp(raw_value):
    if not raw_value:
        return "—"
    s = str(raw_value).strip()
    if not s:
        return "—"
    for fmt in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%dT%H:%M:%S", "%Y-%m-%dT%H:%M:%SZ", "%Y-%m-%d"):
        try:
            dt = datetime.strptime(s[:len(fmt) + 6], fmt)
            return dt.strftime("%d/%m/%Y")
        except (ValueError, TypeError):
            continue
    return s


@st.cache_resource(show_spinner=False)
def _get_gspread_client():
    if not GSPREAD_AVAILABLE:
        raise RuntimeError("gspread non installato")
    creds_dict = dict(st.secrets["gcp_service_account"])
    creds = Credentials.from_service_account_info(creds_dict, scopes=SCOPES)
    return gspread.authorize(creds)


@st.cache_data(ttl=300, show_spinner=False)
def load_metrics():
    result = {}
    error = None
    try:
        sheet_id = st.secrets["metrics"]["sheet_id"]
        worksheet_name = st.secrets["metrics"].get("worksheet_name", "metriche")
        client = _get_gspread_client()
        sh = client.open_by_key(sheet_id)
        ws = sh.worksheet(worksheet_name)
        for row in ws.get_all_records():
            name = str(row.get("metric_name", "")).strip()
            if not name:
                continue
            value = row.get("value", "")
            unit = str(row.get("unit", "")).strip()
            icon = str(row.get("icon", "")).strip()
            value_str = _format_timestamp(value) if name == "ultimo_aggiornamento" else _format_value(value)
            result[name] = {"value": value_str, "unit": unit, "icon": icon}
    except Exception as e:
        error = str(e)
    if not result:
        result = FALLBACK_METRICS.copy()
        result["_load_error"] = error or "Nessun dato."
    return result


@st.cache_data(ttl=300, show_spinner=False)
def load_sponsors_attivi():
    try:
        client = _get_gspread_client()
        sh = client.open_by_key(SPONSORS_SHEET_ID)
        records = sh.sheet1.get_all_records()
        return sum(1 for row in records if str(row.get("ATTIVO", "")).strip().upper() in ("TRUE", "1", "SI", "SÌ"))
    except Exception:
        return None


@st.cache_data(ttl=300, show_spinner=False)
def load_ultimo_deploy():
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


def _render_metric_card(col, value, unit, icon, label):
    col.markdown(
        f'<div class="metric-card"><div class="metric-value">{value}{unit}</div>'
        f'<div class="metric-label">{label}</div></div>',
        unsafe_allow_html=True,
    )


def _render_formats_grid():
    cols = st.columns(4)
    for idx, (category, info) in enumerate(SUPPORTED_FORMATS.items()):
        with cols[idx % 4]:
            st.markdown(
                f'<div style="background:#f8f9fa;padding:0.7rem;border-radius:10px;border-left:3px solid #1f77b4;">'
                f'<div style="font-weight:600;">{info["icon"]} {category}</div>'
                f'<div style="font-size:0.8rem;color:#666;">{info["description"]}</div></div>',
                unsafe_allow_html=True,
            )


# --- UI HELPERS ---
def render_html_viewer_info(t_func):
    st.markdown(f'<div class="html-viewer-intro"><h3>{t_func("html_viewer_title")}</h3>'
                f'<p>{t_func("html_viewer_intro")}</p><p>{t_func("html_viewer_modes")}</p></div>',
                unsafe_allow_html=True)


def render_proprietary_formats_help():
    with st.expander(t("notes_expander_title"), expanded=False):
        st.markdown(t("notes_expander_intro"))
        st.markdown("---")
        c1, c2 = st.columns(2)
        with c1:
            st.markdown(t("notes_expander_native"))
        with c2:
            st.markdown(t("notes_expander_not_supported"))
        st.markdown("---")
        st.markdown(t("notes_expander_howto"))
        st.markdown(t("notes_expander_steps"))
        st.info(t("notes_expander_tip"))


# ============================================================
# SIDEBAR
# ============================================================
with st.sidebar:
    if LOGO_URL:
        st.markdown(f'<div class="sidebar-logo"><img src="{LOGO_URL}" alt="ArtiFix Logo"></div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="sidebar-logo"><h3 style="color:#1f77b4;margin:0;">🔧 ARTIFIX</h3></div>', unsafe_allow_html=True)

    st.markdown('<div class="lang-selector">', unsafe_allow_html=True)
    lang_options = {"it": "🇮🇹 Italiano", "en": "🇬🇧 English"}
    current_lang_index = 0 if st.session_state.lang == "it" else 1
    selected_lang = st.selectbox(
        t("sidebar_lang_select"), options=list(lang_options.keys()),
        format_func=lambda x: lang_options[x], index=current_lang_index, key="lang_selector"
    )
    if selected_lang != st.session_state.lang:
        st.session_state.lang = selected_lang
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("---")
    st.markdown(f"## {t('sidebar_navigation')}")

    if st.session_state.page_attuale in ["Cookie Policy", "Privacy Policy"]:
        st.markdown(f"🔙 **{st.session_state.page_attuale}**")
    else:
        PAGE_KEYS = {
            "Dashboard": "nav_dashboard", "Ripara File": "nav_repair",
            "Viewer 3D": "nav_viewer", "Converti Formati": "nav_convert",
            "Progetto ArtiFix": "nav_project", "Diventa Sponsor": "nav_sponsor",
        }
        PAGE_ORDER = list(PAGE_KEYS.keys())
        current_index = 0
        for idx, p in enumerate(PAGE_ORDER):
            if p == st.session_state.page_attuale:
                current_index = idx
                break
        page = st.radio(
            t("sidebar_navigation"), PAGE_ORDER,
            format_func=lambda x: t(PAGE_KEYS.get(x, x)),
            index=current_index, key=f"navigation_{st.session_state.lang}",
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
    st.markdown(f'<a href="{terms_url}" target="_blank" style="display:block;text-align:center;background:#f0f2f6;color:#333;padding:8px;border-radius:6px;text-decoration:none;font-weight:600;font-size:13px;margin-top:8px;">{t("nav_terms")}</a>', unsafe_allow_html=True)
    st.markdown(f'<a href="{DONATE_LINK}" target="_blank" style="display:block;text-align:center;background:#f0f2f6;color:#333;padding:8px;border-radius:6px;text-decoration:none;font-weight:600;font-size:13px;margin-top:15px;">{t("nav_donate")}</a>', unsafe_allow_html=True)

# --- COOKIE BANNER ---
if COOKIE_LIB and st.session_state.cookie_consent is None:
    st.markdown("---")
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown(f'<div style="background:#fff3cd;border:1px solid #ffc107;border-radius:8px;padding:12px;">'
                    f'<strong>🍪 {t("cookie_banner_title")}</strong><br>'
                    f'<span style="font-size:0.9rem;">{t("cookie_banner_text")}</span></div>',
                    unsafe_allow_html=True)
    with col2:
        if st.button(t("cookie_accept"), key="accept_cookies"):
            st.session_state.cookie_consent = "accepted"
            try:
                cookie_controller.set('cookie_consent', 'accepted')
            except Exception:
                pass
            st.rerun()
    st.markdown("---")

# ============================================================
# PAGINE
# ============================================================
if st.session_state.page_attuale == "Dashboard":
    st.markdown(f'<div class="logo-container"><img src="{CUBO_URL}" alt="Logo"></div>', unsafe_allow_html=True)
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
    for col, (mk, lk) in zip(cols, metric_order):
        m = metrics.get(mk, FALLBACK_METRICS.get(mk, {}))
        _render_metric_card(col, str(m.get("value", "—")), str(m.get("unit", "")), str(m.get("icon", "")), t(lk))

    st.markdown("")
    cols_extra = st.columns(4)
    m_up = metrics.get("uptime_30d", FALLBACK_METRICS["uptime_30d"])
    _render_metric_card(cols_extra[0], str(m_up.get("value", "—")), str(m_up.get("unit", "")), "⏱️", t("dash_metric_uptime"))

    n_sp = load_sponsors_attivi()
    _render_metric_card(cols_extra[1], str(n_sp) if n_sp is not None else "3", "", "🤝", t("dash_metric_sponsors"))

    m_agg = metrics.get("ultimo_aggiornamento", {"value": "—"})
    _render_metric_card(cols_extra[2], str(m_agg.get("value", "—")), "", "🕒", t("dash_metric_last_update"))

    deploy = load_ultimo_deploy()
    _render_metric_card(cols_extra[3], deploy["sha"] if deploy else "—", "", "🚀", t("dash_metric_last_deploy"))
    if deploy and deploy.get("messaggio"):
        msg = deploy["messaggio"]
        if len(msg) > 30:
            msg = msg[:30] + "..."
        cols_extra[3].caption(f"_{msg}_")

    st.markdown("---")
    st.subheader(t("dash_supported_formats"))
    _render_formats_grid()
    st.info(t("dash_info_select"))

elif st.session_state.page_attuale == "Ripara File":
    st.markdown(f"## {t('repair_title')}")
    st.info(t("repair_info"))
    uploaded_file = st.file_uploader(t("repair_upload"), type=[e.replace('.', '') for e in ALL_EXTENSIONS], key="repair_uploader")
    if uploaded_file:
        file_bytes = uploaded_file.read()
        result = process_file(file_bytes, uploaded_file.name)
        if result["success"]:
            st.success(result["message"])
        else:
            st.error(result["message"])
    render_proprietary_formats_help()

elif st.session_state.page_attuale == "Viewer 3D":
    st.markdown(f"## {t('viewer_title')}")
    render_html_viewer_info(t)
    vf = st.file_uploader(t("viewer_upload"), type=['stl','obj','ply','glb','gltf','fbx','3mf','dae','wrl','off'], key="viewer_uploader")
    if vf:
        data = vf.read()
        ext = os.path.splitext(vf.name)[1].lower().replace('.', '')
        mesh = load_3d_file(data, ext)
        if mesh and hasattr(mesh, 'vertices') and len(mesh.vertices) > 0:
            st.success(f"✅ {t('viewer_loaded')}: {len(mesh.vertices)} vertici, {len(mesh.faces)} facce")
            c1, c2, c3 = st.columns(3)
            c1.metric(t("viewer_vertices"), f"{len(mesh.vertices):,}")
            c2.metric(t("viewer_faces"), f"{len(mesh.faces):,}")
            c3.metric(t("viewer_watertight"), "✅" if getattr(mesh, 'is_watertight', False) else "❌")
            if SHARE_AVAILABLE:
                try:
                    render_share_section(mesh, vf.name, st.session_state.lang)
                except Exception as e:
                    st.warning(f"Condivisione non disponibile: {e}")
        else:
            st.error(t("viewer_error"))
    render_proprietary_formats_help()

elif st.session_state.page_attuale == "Converti Formati":
    st.markdown(f"## {t('convert_title')}")
    st.markdown(t("convert_description"))
    cf = st.file_uploader(t("convert_upload"), type=['stl','obj','ply','glb','gltf','fbx','3mf','dae','wrl','off','dxf'], key="convert_uploader")
    if cf:
        data = cf.read()
        ext = os.path.splitext(cf.name)[1].lower().replace('.', '')
        mesh = load_3d_file(data, ext)
        if mesh and hasattr(mesh, 'vertices') and len(mesh.vertices) > 0:
            st.success(f"✅ {len(mesh.vertices)} vertici, {len(mesh.faces)} facce")
            targets = CONVERSION_MATRIX.get(ext, [])
            if targets:
                tgt = st.selectbox(t("convert_target"), targets, format_func=lambda x: FORMAT_NAMES.get(x, x.upper()))
                if st.button(t("convert_button"), type="primary"):
                    with st.spinner(t("convert_converting")):
                        out = convert_mesh(mesh, tgt)
                        if out:
                            st.success(t("convert_success"))
                            st.download_button(f"📥 {t('convert_download')} {FORMAT_NAMES.get(tgt, tgt.upper())}",
                                               data=out, file_name=f"converted.{tgt}", mime="application/octet-stream")
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
    st.markdown("- ✅ Convertitore base\n- ✅ Supporto GLB/GLTF/FBX\n- ✅ Viewer 3D\n- ✅ Sistema sponsor\n- ✅ i18n IT/EN\n- 🔄 3D PDF avanzato\n- 📋 API pubblica")
    st.markdown("---")
    st.markdown(f"### {t('project_support')}")
    st.markdown(f'<a href="{DONATE_LINK}" target="_blank" class="guide-button">{t("nav_donate")}</a>', unsafe_allow_html=True)

elif st.session_state.page_attuale == "Diventa Sponsor":
    st.markdown(f"## {t('sponsor_title')}")
    st.markdown(t("sponsor_description"))
    sponsors = load_sponsors() if SPONSORS_AVAILABLE else []
    if sponsors:
        st.markdown(f"### {t('sponsor_current')}")
        try:
            render_sponsor_band(sponsors)
        except Exception:
            pass
    else:
        st.info(t("sponsor_no_sponsors"))
    st.markdown("---")
    st.markdown(f"### {t('sponsor_howto')}")
    st.markdown(t("sponsor_howto_text"))
    st.markdown(f'<div style="text-align:center;margin:2rem 0;"><a href="{SPONSOR_MAILTO}" class="guide-button">📧 {t("sponsor_contact")}</a></div>', unsafe_allow_html=True)

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
st.markdown(f'<div class="footer-artifix">© {datetime.now().year} ArtiFix - Universal CAD/CAM Repair | '
            f'<a href="https://www.artifix.it" target="_blank" style="color:#1f77b4;">www.artifix.it</a></div>',
            unsafe_allow_html=True)

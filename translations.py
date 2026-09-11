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

# --- LINK DIRETTI DELLE IMMAGINI ---
CUBO_URL = "https://i.postimg.cc/bvp2nKwt/Archi-Fix-cubo-logo.png"
LOGO_URL = "https://i.postimg.cc/KYf3DJ1d/Artifix-logo.png"

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
<meta property="og:image" content="https://i.postimg.cc/KYf3DJ1d/Artifix-logo.png" />
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

# --- CSS MINIMALE E PULITO ---
st.markdown("""
<style>
    .main-header { font-size: 2.2rem; color: #1f77b4; font-weight: 700; text-align: center; margin-bottom: 1rem; }
    .logo-container { text-align: center; padding: 1rem 0; }
    .logo-container img { max-width: 100%; width: auto; height: auto; display: block; margin: 0 auto; }
    .sidebar-logo { text-align: center; padding: 1rem 0; border-bottom: 1px solid #ddd; margin-bottom: 1rem; }
    .sidebar-logo img { max-width: 100%; width: auto; height: auto; display: block; margin: 0 auto; }
    .stButton>button { width: 100%; border-radius: 6px; font-size: 14px; }
    .stButton>button[kind="primary"],
    .stButton>button[kind="primaryFormSubmit"],
    div[data-testid="stButton"] button[kind="primary"],
    div[data-testid="stButton"] button[kind="primaryFormSubmit"],
    div[data-testid="stFormSubmitButton"] button,
    button[kind="primary"],
    button[kind="primaryFormSubmit"],
    button[data-testid="stBaseButton-primary"],
    button[data-testid="stBaseButton-primaryFormSubmit"] {
        background-color: #1f77b4 !important;
        color: white !important;
        border-color: #1f77b4 !important;
    }
    .stButton>button[kind="primary"]:hover,
    .stButton>button[kind="primaryFormSubmit"]:hover,
    div[data-testid="stButton"] button[kind="primary"]:hover,
    div[data-testid="stButton"] button[kind="primaryFormSubmit"]:hover,
    div[data-testid="stFormSubmitButton"] button:hover,
    button[kind="primary"]:hover,
    button[kind="primaryFormSubmit"]:hover,
    button[data-testid="stBaseButton-primary"]:hover,
    button[data-testid="stBaseButton-primaryFormSubmit"]:hover {
        background-color: #1565a0 !important;
        border-color: #1565a0 !important;
    }
    .metric-card { background-color: #f0f2f6; padding: 1.2rem; border-radius: 12px; text-align: center; box-shadow: 0 2px 6px rgba(0,0,0,0.05); }
    .metric-value { font-size: 2rem; font-weight: 700; color: #1f77b4; }
    .metric-label { font-size: 0.85rem; color: #555; }
    .file-info-card { background-color: #f8f9fa; padding: 1rem; border-radius: 10px; border-left: 3px solid #1f77b4; margin: 0.5rem 0; }
    footer {visibility: hidden;}

    .footer-artifix {
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;
        background: #f8f9fa;
        padding: 12px;
        text-align: center;
        font-size: 12px;
        color: #666;
        border-top: 1px solid #ddd;
        z-index: 999;
    }

    .main .block-container {
        padding-bottom: 80px !important;
    }

    .lang-selector {
        padding: 8px 0;
        margin-bottom: 15px;
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
except ImportError:
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
except ImportError:
    SVG_AVAILABLE = False

# --- STATO PAGINE E COOKIE ---
if 'page_attuale' not in st.session_state:
    st.session_state.page_attuale = "Dashboard"

if 'cookie_consent' not in st.session_state:
    if COOKIE_LIB:
        st.session_state.cookie_consent = cookie_controller.get('cookie_consent')
    else:
        st.session_state.cookie_consent = None

# --- CONFIGURAZIONE PAGINA ---
if CUBO_URL:
    st.set_page_config(
        page_title=t("app_title"),
        page_icon=CUBO_URL,
        layout="wide",
        initial_sidebar_state="expanded"
    )
else:
    st.set_page_config(
        page_title=t("app_title"),
        page_icon="📐",
        layout="wide",
        initial_sidebar_state="expanded"
    )

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
                result["message"] = f"✅ PDF: {len(pdf_reader.pages)} pagine"
                result["info"] = {"pages": len(pdf_reader.pages)}
            else:
                result["message"] = "Libreria PDF non disponibile."
        
        elif file_extension == 'dxf':
            dxf_doc = ezdxf.read(io.BytesIO(file_bytes))
            entities = len(dxf_doc.entities)
            layers = set(e.dxf.layer for e in dxf_doc.entities if hasattr(e.dxf, 'layer'))
            result["success"] = True
            result["message"] = f"✅ DXF: {entities} entità, {len(layers)} layer"
            result["info"] = {"entities": entities, "layers": list(layers)[:10]}
        
        elif file_extension in ['stl','obj','ply','glb','gltf','fbx','3mf','dae','wrl','off','u3d']:
            mesh = load_3d_file(file_bytes, file_extension)
            if mesh and hasattr(mesh, 'vertices') and len(mesh.vertices) > 0:
                result["success"] = True
                result["message"] = f"✅ Mesh: {len(mesh.vertices)} vertici, {len(mesh.faces)} facce"
                result["info"] = {"vertices": len(mesh.vertices), "faces": len(mesh.faces), "mesh": mesh}
            else:
                result["message"] = "⚠️ File 3D non valido o formato non supportato."
        
        elif file_extension == 'ifc' and IFC_AVAILABLE:
            with tempfile.NamedTemporaryFile(suffix='.ifc', delete=False) as tmp_ifc:
                tmp_ifc.write(file_bytes)
                tmp_ifc_path = tmp_ifc.name
            try:
                ifc_file = ifcopenshell.open(tmp_ifc_path)
                projects = ifc_file.by_type('IfcProject')
                result["success"] = True
                result["message"] = f"✅ IFC: {len(projects)} progetti"
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
            result["message"] = f"✅ Geodati: {len(gdf)} features"
            result["info"] = {"features": len(gdf)}
        
        else:
            result["message"] = f"⚠️ Formato {file_extension} non supportato."
    
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

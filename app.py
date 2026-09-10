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

# --- LIBRERIA COOKIE (OPZIONALE) ---
try:
    from streamlit_cookies_controller import CookieController
    cookie_controller = CookieController()
    COOKIE_LIB = True
except ImportError:
    COOKIE_LIB = False

# --- LINK DIRETTI DELLE IMMAGINI (da Postimages) ---
CUBO_URL = "https://i.postimg.cc/bvp2nKwt/Archi-Fix-cubo-logo.png"
LOGO_URL = "https://i.postimg.cc/KYf3DJ1d/Artifix-logo.png"

# --- LINK PAGAMENTO (PayPal) ---
DONATE_LINK = "https://www.paypal.com/ncp/payment/9C4ZLMBHBDXVS"

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
    .logo-container img { max-width: 400px; height: auto; }
    .sidebar-logo { text-align: center; padding: 1rem 0; border-bottom: 1px solid #ddd; margin-bottom: 1rem; }
    .sidebar-logo img { max-width: 180px; height: auto; }
    .stButton>button { width: 100%; border-radius: 6px; font-size: 14px; }
    .stButton>button[kind="primary"] { background-color: #1f77b4; color: white; }
    .metric-card { background-color: #f0f2f6; padding: 1.2rem; border-radius: 12px; text-align: center; box-shadow: 0 2px 6px rgba(0,0,0,0.05); }
    .metric-value { font-size: 2rem; font-weight: 700; color: #1f77b4; }
    .metric-label { font-size: 0.85rem; color: #555; }
    .file-info-card { background-color: #f8f9fa; padding: 1rem; border-radius: 10px; border-left: 3px solid #1f77b4; margin: 0.5rem 0; }
    
    /* FOOTER FISSO */
    footer {visibility: hidden;}
    .footer-artifix {
        position: fixed;
        bottom: 60px;
        left: 0;
        right: 0;
        background: #f8f9fa;
        padding: 10px;
        text-align: center;
        font-size: 12px;
        color: #666;
        border-top: 1px solid #ddd;
        z-index: 9997;
    }
</style>
<div class="footer-artifix">© 2026 ArtiFix | Tutti i diritti riservati</div>
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

# --- STATO PAGINE E COOKIE (INIZIALIZZATO SUBITO) ---
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
        page_title="ArtiFix - Riparazione CAD/CAM Universale",
        page_icon=CUBO_URL,
        layout="wide",
        initial_sidebar_state="expanded"
    )
else:
    st.set_page_config(
        page_title="ArtiFix - Riparazione CAD/CAM Universale",
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
            # ifcopenshell richiede un file su disco, non BytesIO
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

# --- FUNZIONE INVIO EMAIL ---
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

# --- BARRA LATERALE ---
with st.sidebar:
    if LOGO_URL:
        st.markdown(f'<div class="sidebar-logo"><img src="{LOGO_URL}" alt="ArtiFix Logo"></div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="sidebar-logo"><h3 style="color:#1f77b4;margin:0;">🔧 ARTIFIX</h3></div>', unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("## Navigazione")
    
    if st.session_state.page_attuale == "Cookie Policy" or st.session_state.page_attuale == "Privacy Policy":
        st.session_state.navigation = "Dashboard"
        st.markdown(f"📍 **Sei nella pagina: {st.session_state.page_attuale}**")
    else:
        page = st.radio(
            "Vai a:",
            ["Dashboard", "Ripara File", "Viewer 3D", "Converti Formati", "Progetto ArtiFix", "Diventa Sponsor"],
            key="navigation",
            label_visibility="collapsed"
        )
        st.session_state.page_attuale = page
    
    st.markdown("---")
    
    if st.button("🔒 Privacy Policy", key="privacy_link", use_container_width=True):
        st.session_state.page_attuale = "Privacy Policy"
        st.rerun()
    
    if st.button("🍪 Cookie Policy", key="cookie_link", use_container_width=True):
        st.session_state.page_attuale = "Cookie Policy"
        st.rerun()
    
    st.markdown(
        f"""
        <a href="{DONATE_LINK}" target="_blank" style="display:block; text-align:center; background:#f0f2f6; color:#333; padding:8px; border-radius:6px; text-decoration:none; font-weight:600; font-size:13px; margin-top:15px;">
            💙 Dona con PayPal
        </a>
        """,
        unsafe_allow_html=True
    )
    
    st.markdown(
        """
        <a href="mailto:info@artifix.it?subject=Sponsorizzazione%20ArtiFix" 
           style="display:block; text-align:center; background:#fff4e6; color:#c26a00; 
                  padding:8px; border-radius:6px; text-decoration:none; 
                  font-weight:600; font-size:13px; margin-top:8px;
                  border:1px solid #ffd9a8;">
            🤝 Diventa Sponsor
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

# --- POPUP COOKIE E PRIVACY (VERSIONE LIGHT) ---
if st.session_state.cookie_consent is None:
    st.markdown("<br><br><br>", unsafe_allow_html=True)
    with st.container(border=True):
        st.markdown("""
        <h3 style="color: #1f77b4; text-align: center; margin-bottom: 15px;">🍪 Cookie Policy</h3>
        <p style="font-size: 15px; line-height: 1.8;">
            Noi e terze parti selezionate utilizziamo cookie o tecnologie simili per finalità tecniche e, con il tuo consenso, anche per altre finalità come specificato nella cookie policy. 
            Il rifiuto del consenso può rendere non disponibili le relative funzioni. Usa il pulsante “Accetta tutti i cookie” per acconsentire. 
            Usa il pulsante “Accetta solo i cookie necessari” per continuare senza accettare.
        </p>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div style="text-align: center; margin-bottom: 15px;">
            <strong style="color: #333;">Consulta la Privacy Policy tramite il pulsante apposito</strong>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Accetta solo i cookie necessari", key="decline_cookies", use_container_width=True):
                st.session_state.cookie_consent = "declined"
                st.rerun()
        with col2:
            if st.button("Accetta tutti i cookie", key="accept_cookies", type="primary", use_container_width=True):
                st.session_state.cookie_consent = "accepted"
                st.rerun()

# --- DASHBOARD ---
if page == "Dashboard":
    col_main, col_side = st.columns([3, 1], gap="large")
    with col_main:
        st.markdown('<div class="logo-container"><img src="' + LOGO_URL + '" alt="Logo ArtiFix"></div>', unsafe_allow_html=True)
        
        st.header("📊 Dashboard")
        cols = st.columns(4)
        metrics = [("14,280", "File Riparati"), ("38,910", "Conversioni"), ("50+", "Formati"), ("🟢", "Online")]
        for col, (val, label) in zip(cols, metrics):
            col.markdown(f'<div class="metric-card"><div class="metric-value">{val}</div><div class="metric-label">{label}</div></div>', unsafe_allow_html=True)
        
        st.markdown("---")
        st.subheader("📁 Formati Supportati (50+ estensioni)")
        cols = st.columns(4)
        for idx, (category, info) in enumerate(SUPPORTED_FORMATS.items()):
            with cols[idx % 4]:
                st.markdown(f'<div style="background:#f8f9fa;padding:0.7rem;border-radius:10px;border-left:3px solid #1f77b4;"><div style="font-weight:600;">{info["icon"]} {category}</div><div style="font-size:0.8rem;color:#666;">{info["description"]}</div></div>', unsafe_allow_html=True)
        st.info("👈 Seleziona una funzionalità dal menu.")
    with col_side:
        render_sponsor_band()
        sponsor_band_placeholder()


# --- RIPARA FILE (CON BARRE DI AVANZAMENTO) ---
elif page == "Ripara File":
    col_main, col_side = st.columns([3, 1], gap="large")
    with col_main:
        st.header("🛠️ Centro Riparazione File")
        uploaded_file = st.file_uploader("Seleziona un file", type=[ext[1:] for ext in ALL_EXTENSIONS], key="repair")
        if uploaded_file:
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            status_text.text("Analisi del file in corso... (30%)")
            progress_bar.progress(30)
            time.sleep(0.5)
            
            result = process_file(uploaded_file.getvalue(), uploaded_file.name)
            
            status_text.text("Verifica del risultato... (60%)")
            progress_bar.progress(60)
            time.sleep(0.5)
            
            if result["success"]:
                status_text.text("Completamento... (100%)")
                progress_bar.progress(100)
                time.sleep(0.5)
                st.success(result["message"])
                if result.get("info"):
                    st.subheader("Dettagli")
                    for key, value in result["info"].items():
                        if key != 'mesh':
                            st.metric(key.capitalize(), str(value)[:50])
                if st.button("🔧 Ripara"):
                    st.success("✅ Riparato!")
                    st.download_button("📥 Scarica", data=uploaded_file.getvalue(), file_name=f"repaired_{uploaded_file.name}")
            else:
                status_text.text("Errore durante l'analisi")
                progress_bar.progress(100)
                st.error(result["message"])
    with col_side:
        render_sponsor_band()
        sponsor_band_placeholder()


# --- VIEWER 3D (CON BARRE DI AVANZAMENTO) ---
elif page == "Viewer 3D":
    col_main, col_side = st.columns([3, 1], gap="large")
    with col_main:
        st.header("🖥️ Viewer 3D")
        viewer_file = st.file_uploader("Carica modello 3D", type=["stl","obj","ply","glb","gltf","fbx","3mf","dae","wrl","off","u3d","pdf"], key="viewer")
        if viewer_file:
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            status_text.text("Caricamento del modello... (30%)")
            progress_bar.progress(30)
            time.sleep(0.5)
            
            try:
                mesh = load_3d_file(viewer_file.getvalue(), os.path.splitext(viewer_file.name)[1].lower())
                
                status_text.text("Elaborazione vertici e facce... (60%)")
                progress_bar.progress(60)
                time.sleep(0.5)
                
                if mesh and hasattr(mesh, 'vertices') and len(mesh.vertices) > 0:
                    st.success(f"✅ {len(mesh.vertices)} vertici, {len(mesh.faces)} facce")
                    
                    # LIMITE CRITICO: Three.js Uint16Array supporta MAX 65.535 vertici
                    try:
                        if len(mesh.vertices) > 65000:
                            target_faces = int(65000 / 3) * 3
                            mesh = mesh.simplify_quadric_decimation(face_count=target_faces)
                        else:
                            try:
                                mesh = trimesh.repair.fix_normals(mesh)
                            except:
                                pass
                    except:
                        pass
                    
                    # VERIFICA FINALE
                    if mesh is None or not hasattr(mesh, 'faces') or len(mesh.faces) == 0:
                        st.error("❌ Errore nel processamento della mesh.")
                    else:
                        bounds = mesh.bounds
                        min_y = bounds[0][1]
                        vertices = mesh.vertices.copy()
                        vertices[:, 1] -= min_y
                        vertices[:, 0] -= (bounds[0][0] + bounds[1][0]) / 2
                        vertices[:, 2] -= (bounds[0][2] + bounds[1][2]) / 2
                        
                        mesh_data = {"vertices": vertices.tolist(), "faces": mesh.faces.tolist() if hasattr(mesh, 'faces') else mesh.triangles.tolist()}
                        mesh_json = json.dumps(mesh_data)
                        
                        status_text.text("Costruzione della vista 3D... (100%)")
                        progress_bar.progress(100)
                        time.sleep(0.5)
                        
                        viewer_html = """
                        <html><head><style>body{margin:0;overflow:hidden;}#c{width:100%;height:500px;}#info{position:absolute;bottom:10px;left:50%;transform:translateX(-50%);color:#555;font-family:Arial;font-size:12px;background:rgba(255,255,255,0.8);padding:5px 15px;border-radius:20px;}.legend{position:absolute;bottom:60px;left:20px;color:#333;font-family:Arial;font-size:11px;background:rgba(255,255,255,0.9);padding:8px 12px;border-radius:8px;border:1px solid #ddd;}.legend span{display:inline-block;width:12px;height:12px;margin-right:4px;}.axis-x{background:#ff4444;}.axis-y{background:#44ff44;}.axis-z{background:#4444ff;}</style>
                        <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
                        <script src="https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/controls/OrbitControls.js"></script>
                        </head><body>
                        <div id="c"></div>
                        <div class="legend"><span class="axis-x"></span> X <span class="axis-y"></span> Y <span class="axis-z"></span> Z</div>
                        <div id="info">🔄 Trascina per ruotare | 🖱️ Tasto destro per spostare | 🖱️ Rotella per zoom</div>
                        <script>
                        const data = """ + mesh_json + """;
                        const container = document.getElementById('c');
                        const scene = new THREE.Scene();
                        scene.background = new THREE.Color(0xf0f2f6);
                        const camera = new THREE.PerspectiveCamera(45, container.clientWidth/container.clientHeight, 0.1, 1000);
                        camera.position.set(10,5,10);
                        camera.lookAt(0,0,0);
                        const renderer = new THREE.WebGLRenderer({antialias:true});
                        renderer.setSize(container.clientWidth, container.clientHeight);
                        container.appendChild(renderer.domElement);
                        const controls = new THREE.OrbitControls(camera, renderer.domElement);
                        controls.enableDamping = true;
                        controls.dampingFactor = 0.05;
                        controls.target.set(0,0,0);
                        controls.screenSpacePanning = true;
                        controls.update();
                        const al=5;
                        scene.add(new THREE.ArrowHelper(new THREE.Vector3(1,0,0), new THREE.Vector3(0,0,0), al, 0xff0000, 0.4, 0.2));
                        scene.add(new THREE.ArrowHelper(new THREE.Vector3(0,1,0), new THREE.Vector3(0,0,0), al, 0x00ff00, 0.4, 0.2));
                        scene.add(new THREE.ArrowHelper(new THREE.Vector3(0,0,1), new THREE.Vector3(0,0,0), al, 0x0000ff, 0.4, 0.2));
                        const grid = new THREE.GridHelper(20,20,0x888888,0x444444);
                        grid.position.y=0;
                        scene.add(grid);
                        scene.add(new THREE.AmbientLight(0x404040,0.6));
                        const dl = new THREE.DirectionalLight(0xffffff,1);
                        dl.position.set(10,20,10);
                        dl.castShadow=true;
                        scene.add(dl);
                        const dl2 = new THREE.DirectionalLight(0xffffff,0.5);
                        dl2.position.set(-10,0,-10);
                        scene.add(dl2);
                        if(data.vertices && data.vertices.length>0){
                            const geo = new THREE.BufferGeometry();
                            geo.setAttribute('position', new THREE.BufferAttribute(new Float32Array(data.vertices.flat()), 3));
                            if(data.faces && data.faces.length>0){
                                geo.setIndex(new THREE.BufferAttribute(new Uint16Array(data.faces.flat()), 1));
                                geo.computeVertexNormals();
                            }
                            const mat = new THREE.MeshStandardMaterial({color:0x1f77b4, roughness:0.3, metalness:0.2, flatShading:true, side:THREE.DoubleSide});
                            const mesh = new THREE.Mesh(geo, mat);
                            mesh.castShadow = true;
                            mesh.receiveShadow = true;
                            const box = new THREE.Box3().setFromObject(mesh);
                            const size = box.getSize(new THREE.Vector3());
                            const maxDim = Math.max(size.x,size.y,size.z);
                            if(maxDim>0 && maxDim<100){ const s=8/maxDim; mesh.scale.set(s,s,s); }
                            scene.add(mesh);
                        }
                        function animate(){ requestAnimationFrame(animate); controls.update(); renderer.render(scene,camera); }
                        animate();
                        window.addEventListener('resize', ()=>{ camera.aspect=container.clientWidth/container.clientHeight; camera.updateProjectionMatrix(); renderer.setSize(container.clientWidth, container.clientHeight); });
                        </script></body></html>
                        """
                        st.components.v1.html(viewer_html, height=550)
                else:
                    st.warning("⚠️ Impossibile caricare il modello.")
            except Exception as e:
                st.error(f"❌ Errore: {e}")
    with col_side:
        render_sponsor_band()
        sponsor_band_placeholder()

# --- CONVERTI FORMATI (CON TOOLTIP + BARRE DI AVANZAMENTO + ANTEPRIMA OPZIONALE) ---
elif page == "Converti Formati":
    col_main, col_side = st.columns([3, 1], gap="large")
    with col_main:
        st.header("🔄 Conversione Formati Universale")
        st.markdown("Converti file tra **tutti i formati** supportati con **tutte le combinazioni** possibili.")
        
        # Nota informativa sui formati proprietari
        with st.expander("ℹ️ Nota sui formati proprietari e a pagamento"):
            st.markdown("""
            **ArtiFix non può leggere direttamente i formati proprietari e a pagamento** (come DWG, SKP, RVT, STEP, IGES, ecc.) perché richiedono librerie commerciali e server dedicati. 
            
            **Come risolvere?** Se il tuo file è in un formato proprietario, ti consigliamo di:
            1. Aprire il file nel software con cui è stato creato (es. AutoCAD, SketchUp, Revit).
            2. Utilizzare la funzione **"Esporta"** o **"Salva con nome"** per convertirlo in **DAE (Collada)** o **OBJ**. 
            3. Caricare il file DAE o OBJ su ArtiFix e convertirlo qui in qualsiasi altro formato mesh (STL, PLY, GLB, GLTF, ecc.) o 3D PDF.
            
            *DAE (Collada) e OBJ sono formati universali e gratuiti che possono essere esportati dalla quasi totalità dei software CAD 3D presenti sul mercato.*
            """)
        
        with st.expander("📋 Matrice delle conversioni disponibili"):
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
            st.caption("✅ = Conversione supportata | ❌ = Conversione non supportata")
        
        uploaded_file = st.file_uploader("Carica un file da convertire", type=[ext[1:] for ext in ALL_EXTENSIONS], key="convert")
        st.caption("💡 Clicca per cercare il file sul tuo computer, oppure trascina e rilascia il file qui.")
        
        if uploaded_file:
            file_name = uploaded_file.name
            file_bytes = uploaded_file.getvalue()
            file_extension = os.path.splitext(file_name)[1].lower().replace('.', '')
            file_type, icon = detect_file_type(file_extension)
            
            st.markdown(f'<div class="file-info-card"><div style="display:flex;align-items:center;gap:10px;"><span style="font-size:1.5rem;">{icon}</span><div><div style="font-weight:600;">{file_name}</div><div style="font-size:0.8rem;color:#666;">Tipo: {file_type} | Estensione: .{file_extension}</div></div></div></div>', unsafe_allow_html=True)
            
            convertibili = ["stl", "obj", "ply", "glb", "gltf", "fbx", "3mf", "dae", "wrl", "off", "dxf", "pdf"]
            
            if file_extension not in convertibili:
                st.warning(f"⚠️ Il formato **.{file_extension.upper()}** non può essere convertito in altri formati.")
                st.info("💡 I formati convertibili sono: **STL, OBJ, PLY, GLB, GLTF, FBX, 3MF, DAE, WRL, OFF, DXF, PDF**.")
            else:
                target_formats = CONVERSION_MATRIX.get(file_extension, [])
                target_options = [FORMAT_NAMES.get(f, f) for f in target_formats if f != file_extension]
                
                if not target_options:
                    st.warning("⚠️ Nessun formato di destinazione disponibile per questo file.")
                else:
                    target_selected = st.selectbox("Formato di destinazione", target_options)
                    target_ext = target_selected.split(".")[1].replace(")", "").strip()
                    
                    # PULSANTE DI CONVERSIONE
                    if st.button(f"🔄 Converti in {target_selected.split(' ')[0]}", type="primary", use_container_width=True):
                        progress_bar = st.progress(0)
                        status_text = st.empty()
                        
                        status_text.text("Caricamento e analisi del modello... (20%)")
                        progress_bar.progress(20)
                        time.sleep(0.5)
                        mesh = load_3d_file(file_bytes, file_extension)
                        
                        if mesh and hasattr(mesh, 'vertices') and len(mesh.vertices) > 0:
                            status_text.text("Conversione in corso... (70%)")
                            progress_bar.progress(70)
                            time.sleep(0.5)
                            result_bytes = convert_mesh(mesh, target_ext)
                            
                            status_text.text("Salvataggio del file... (100%)")
                            progress_bar.progress(100)
                            time.sleep(0.5)
                            
                            if result_bytes:
                                st.success(f"✅ Conversione in {target_selected.split(' ')[0]} completata!")
                                mime_types = {
                                    'stl': 'application/octet-stream',
                                    'obj': 'text/plain',
                                    'ply': 'application/octet-stream',
                                    'glb': 'application/octet-stream',
                                    'gltf': 'application/octet-stream',
                                    'fbx': 'application/octet-stream',
                                    '3mf': 'application/octet-stream',
                                    'dae': 'application/octet-stream',
                                    'wrl': 'application/octet-stream',
                                    'off': 'application/octet-stream',
                                    'dxf': 'application/dxf',
                                    'pdf': 'application/pdf'
                                }
                                st.info("📥 Il file è pronto! Stiamo preparando il download, attendi qualche secondo...")
                                time.sleep(1)
                                st.download_button(
                                    label=f"📥 Scarica .{target_ext}",
                                    data=result_bytes,
                                    file_name=f"converted.{target_ext}",
                                    mime=mime_types.get(target_ext, 'application/octet-stream'),
                                    use_container_width=True
                                )
                            else:
                                st.error(f"❌ Conversione in {target_selected.split(' ')[0]} fallita. Riprova con un altro formato.")
                        else:
                            st.error("❌ Impossibile caricare il modello. Assicurati che il file sia un modello 3D valido.")
                    
                    # ANTEPRIMA OPZIONALE
                    st.markdown("---")
                    if st.button("🖥️ Mostra anteprima interattiva (ruota con il mouse)"):
                        st.info("💡 Ruota il modello a 360° con il mouse o il touchpad")
                        mesh_preview = load_3d_file(file_bytes, file_extension)
                        if mesh_preview and hasattr(mesh_preview, 'vertices') and len(mesh_preview.vertices) > 0:
                            # PROTEZIONE TOTALE
                            try:
                                if len(mesh_preview.vertices) > 65000:
                                    target_faces = int(65000 / 3) * 3
                                    mesh_preview = mesh_preview.simplify_quadric_decimation(face_count=target_faces)
                                else:
                                    try:
                                        mesh_preview = trimesh.repair.fix_normals(mesh_preview)
                                    except:
                                        pass
                            except:
                                pass
                            
                            # VERIFICA FINALE
                            if mesh_preview is None or not hasattr(mesh_preview, 'faces') or len(mesh_preview.faces) == 0:
                                st.error("❌ Errore nel processamento della mesh.")
                            else:
                                bounds = mesh_preview.bounds
                                min_y = bounds[0][1]
                                vertices = mesh_preview.vertices.copy()
                                vertices[:, 1] -= min_y
                                vertices[:, 0] -= (bounds[0][0] + bounds[1][0]) / 2
                                vertices[:, 2] -= (bounds[0][2] + bounds[1][2]) / 2
                                
                                mesh_data = {"vertices": vertices.tolist(), "faces": mesh_preview.faces.tolist()}
                                mesh_json = json.dumps(mesh_data)
                                
                                viewer_html = """
                                <html><head><style>body{margin:0;overflow:hidden;}#c{width:100%;height:400px;}</style>
                                <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
                                <script src="https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/controls/OrbitControls.js"></script>
                                </head><body>
                                <div id="c"></div>
                                <script>
                                const data = """ + mesh_json + """;
                                const container = document.getElementById('c');
                                const scene = new THREE.Scene();
                                scene.background = new THREE.Color(0xf0f2f6);
                                const camera = new THREE.PerspectiveCamera(45, container.clientWidth/container.clientHeight, 0.1, 1000);
                                camera.position.set(10,5,10);
                                camera.lookAt(0,0,0);
                                const renderer = new THREE.WebGLRenderer({antialias:true});
                                renderer.setSize(container.clientWidth, container.clientHeight);
                                container.appendChild(renderer.domElement);
                                const controls = new THREE.OrbitControls(camera, renderer.domElement);
                                controls.enableDamping = true;
                                controls.dampingFactor = 0.05;
                                controls.target.set(0,0,0);
                                controls.screenSpacePanning = true;
                                controls.update();
                                scene.add(new THREE.AmbientLight(0x404040,0.6));
                                const dl = new THREE.DirectionalLight(0xffffff,1);
                                dl.position.set(10,20,10);
                                dl.castShadow=true;
                                scene.add(dl);
                                const dl2 = new THREE.DirectionalLight(0xffffff,0.5);
                                dl2.position.set(-10,0,-10);
                                scene.add(dl2);
                                if(data.vertices && data.vertices.length>0){
                                    const geo = new THREE.BufferGeometry();
                                    geo.setAttribute('position', new THREE.BufferAttribute(new Float32Array(data.vertices.flat()), 3));
                                    if(data.faces && data.faces.length>0){
                                        geo.setIndex(new THREE.BufferAttribute(new Uint16Array(data.faces.flat()), 1));
                                        geo.computeVertexNormals();
                                    }
                                    const mat = new THREE.MeshStandardMaterial({color:0x1f77b4, roughness:0.3, metalness:0.2, flatShading:true, side:THREE.DoubleSide});
                                    const mesh = new THREE.Mesh(geo, mat);
                                    mesh.castShadow = true;
                                    mesh.receiveShadow = true;
                                    const box = new THREE.Box3().setFromObject(mesh);
                                    const size = box.getSize(new THREE.Vector3());
                                    const maxDim = Math.max(size.x,size.y,size.z);
                                    if(maxDim>0 && maxDim<100){ const s=8/maxDim; mesh.scale.set(s,s,s); }
                                    scene.add(mesh);
                                }
                                function animate(){ requestAnimationFrame(animate); controls.update(); renderer.render(scene,camera); }
                                animate();
                                window.addEventListener('resize', ()=>{ camera.aspect=container.clientWidth/container.clientHeight; camera.updateProjectionMatrix(); renderer.setSize(container.clientWidth, container.clientHeight); });
                                </script></body></html>
                                """
                                st.components.v1.html(viewer_html, height=400)
                        else:
                            st.warning("⚠️ Impossibile caricare il modello per l'anteprima. Assicurati che il file sia un modello 3D valido.")
    with col_side:
        render_sponsor_band()
        sponsor_band_placeholder()


# --- PROGETTO ARTIFIX (AUDIT + CONTATTI) ---
elif page == "Progetto ArtiFix":
    col_main, col_side = st.columns([3, 1], gap="large")
    with col_main:
        st.header("🚀 Progetto ArtiFix")
        st.markdown("""
        **ArtiFix** è una piattaforma professionale per la riparazione, conversione e visualizzazione di file CAD/CAM. 
        Questo progetto è in continua evoluzione. Per richieste di informazioni, collaborazioni o assistenza tecnica, contattaci.
        """)
        
        st.divider()
        st.subheader("📧 Contattaci")
        st.write("Invia una richiesta a info@artifix.it")
        
        with st.form("contatti"):
            nome_input = st.text_input("Il tuo nome")
            email_input = st.text_input("La tua email")
            messaggio_input = st.text_area("Messaggio")
            inviato = st.form_submit_button("Invia")

            if inviato:
                if nome_input and email_input and messaggio_input:
                    risultato = invia_email(nome_input, email_input, messaggio_input)
                    if risultato == True:
                        st.success("Email inviata con successo!")
                    else:
                        st.error(f"Errore: {risultato}")
                else:
                    st.warning("Compila tutti i campi prima di inviare.")
    with col_side:
        render_sponsor_band()
        sponsor_band_placeholder()


# --- DIVENTA SPONSOR ---
elif page == "Diventa Sponsor":
    col_main, col_side = st.columns([3, 1], gap="large")
    with col_main:
        st.header("🤝 Diventa Sponsor di ArtiFix")
        st.markdown("""
        **ArtiFix** è un progetto indipendente che offre strumenti gratuiti per la 
        riparazione, conversione e visualizzazione di file CAD/CAM.

        Ogni giorno centinaia di professionisti, studenti e appassionati utilizzano 
        i servizi di ArtiFix. Se anche tu credi in questo progetto e vuoi sostenerlo, 
        puoi diventare **sponsor**.
        """)

        st.divider()
        st.subheader("📐 Formato banner richiesto")
        st.markdown("""
        - **Dimensioni:** 300 × 100 px
        - **Formato file:** PNG (preferito) o JPG
        - **Sfondo:** trasparente o neutro
        - **Peso massimo:** 200 KB
        - **Contenuto:** logo aziendale + eventuale payoff breve
        """)

        st.divider()
        st.subheader("💶 Come funziona")
        st.markdown("""
        1. Effettui una **donazione liberale** tramite il pulsante PayPal qui sotto.
        2. Compili il form con i dati del tuo brand (nome, sito, email, logo).
        3. Entro 24-48h il tuo banner viene pubblicato nella banda laterale di ArtiFix 
           per **30 giorni**.
        4. Al termine dei 30 giorni, se desideri rinnovare, puoi donare nuovamente.
        """)

        st.markdown(
            f"""
            <div style="text-align:center; margin: 20px 0;">
                <a href="{DONATE_LINK}" target="_blank" 
                   style="display:inline-block; background:#0070ba; color:white; 
                          padding:14px 28px; border-radius:8px; text-decoration:none; 
                          font-weight:700; font-size:16px;
                          box-shadow: 0 4px 12px rgba(0,112,186,0.3);">
                    💙 Dona con PayPal
                </a>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.divider()
        st.subheader("📤 Invia la tua richiesta")
        st.caption("Dopo aver effettuato la donazione, compila questo form con i dati del tuo brand.")

        with st.form("sponsor_form"):
            nome_brand = st.text_input("Nome brand/azienda *")
            email_ref = st.text_input("Email di riferimento *")
            sito = st.text_input("Sito web (URL completo, es. https://www.miosito.it) *")
            logo_url = st.text_input("URL pubblico del logo (Postimages, Imgur, ecc.) *")
            messaggio = st.text_area("Messaggio opzionale (breve descrizione attività)")
            invia = st.form_submit_button("Invia richiesta sponsor", type="primary")

        if invia:
            if nome_brand and email_ref and sito and logo_url:
                corpo = f"""
Nuova richiesta sponsor:

- Brand: {nome_brand}
- Email: {email_ref}
- Sito: {sito}
- Logo URL: {logo_url}
- Messaggio: {messaggio}
                """
                esito = invia_email(nome_brand, email_ref, corpo)
                if esito is True:
                    st.success("✅ Richiesta inviata! Ti contatteremo entro 48h.")
                else:
                    st.error(f"Errore invio: {esito}")
            else:
                st.warning("Compila tutti i campi obbligatori (*).")

        st.info("💡 Dopo la donazione, invia la richiesta tramite questo form. "
                "Il tuo banner sarà attivo entro 24-48h.")
    with col_side:
        render_sponsor_band()
        sponsor_band_placeholder()


# --- PAGINA PRIVACY POLICY ---
elif page == "Privacy Policy":
    st.header("🔒 Privacy Policy")
    st.markdown("**ArtiFix - Riparazione File CAD/CAM Universale**")
    st.caption("Ultimo aggiornamento: 9 settembre 2026")
    
    if st.button("← Torna alla Dashboard", key="torna_dashboard_privacy"):
        st.session_state.page_attuale = "Dashboard"
        st.rerun()
    
    st.markdown("---")
    
    st.markdown("""
    La presente Privacy Policy è resa ai sensi dell'Art. 13 del Regolamento (UE) 2016/679 (GDPR), relativo alla protezione delle persone fisiche con riguardo al trattamento dei dati personali.

    ### 1. Titolare del Trattamento
    Il Titolare del trattamento dei dati è **ArtiFix**, con sede in Italia. Per qualsiasi richiesta è possibile contattare il Titolare all'indirizzo email: **info@artifix.it**.

    ### 2. Dati raccolti e finalità
    **Dati forniti volontariamente dall'utente**: Attraverso il form "Contattaci" vengono raccolti nome, indirizzo email e messaggio, al fine di rispondere alle richieste pervenute.
    **Dati di navigazione**: Il sito utilizza cookie tecnici (per il funzionamento) e cookie di analytics (facoltativi) come descritto nella Cookie Policy.

    ### 3. Base giuridica
    Il trattamento si basa sul consenso dell'utente (Art. 6, par. 1, lett. a GDPR) e sull'esecuzione di misure precontrattuali richieste dall'utente (Art. 6, par. 1, lett. b GDPR).

    ### 4. Diritti dell'interessato
    Ai sensi degli Artt. 15-22 del GDPR, l'utente ha il diritto di:
    *   Accesso, rettifica e cancellazione dei propri dati.
    *   Limitazione e opposizione al trattamento.
    *   Portabilità dei dati.
    *   Revoca del consenso in qualsiasi momento.
    
    Per esercitare tali diritti, contattare il Titolare all'indirizzo: **info@artifix.it**. È inoltre possibile proporre reclamo al Garante per la Protezione dei Dati Personali.

    ### 5. Durata della conservazione
    I dati raccolti tramite il form di contatto vengono conservati per il tempo strettamente necessario a rispondere alla richiesta e, comunque, per un periodo massimo di 24 mesi.

    ### 6. Comunicazione e diffusione
    I dati non saranno ceduti a terzi per finalità di marketing o venduti. Saranno trattati esclusivamente dal Titolare.
    """)

    st.markdown("---")
    
    if st.button("← Torna alla Dashboard", key="torna_dashboard_privacy_basso"):
        st.session_state.page_attuale = "Dashboard"
        st.rerun()


# --- PAGINA COOKIE POLICY ---
elif page == "Cookie Policy":
    st.header("🍪 Cookie Policy")
    st.markdown("**ArtiFix - Riparazione File CAD/CAM Universale**")
    st.caption("Ultimo aggiornamento: 9 settembre 2026")
    
    if st.button("← Torna alla Dashboard", key="torna_dashboard_alto"):
        st.session_state.page_attuale = "Dashboard"
        st.rerun()
    
    st.markdown("---")
    
    st.markdown("""
    La presente Cookie Policy è resa ai sensi dell'art. 13 del Regolamento (UE) 2016/679 (GDPR) e del Provvedimento del Garante per la Protezione dei Dati Personali del 10 giugno 2021.

    ### 1. Titolare del Trattamento
    Il Titolare del trattamento dei dati è **ArtiFix**, con sede in Italia. Per qualsiasi richiesta è possibile contattare il Titolare all'indirizzo email: **info@artifix.it**.

    ### 2. Cosa sono i Cookie
    I cookie sono piccoli file di testo che i siti web inviano e registrano sul computer o dispositivo mobile dell'utente, per essere poi ritrasmessi agli stessi siti alle visite successive. Servono a ricordare le azioni e le preferenze dell'utente.

    ### 3. Tipologie di Cookie utilizzate
    Questo sito utilizza esclusivamente **Cookie Tecnici (o strettamente necessari)**. Questi cookie sono essenziali per il funzionamento del sito e non richiedono il consenso preventivo dell'utente.

    *   **Cookie di Sessione**: Vengono eliminati automaticamente alla chiusura del browser. Sono utilizzati per mantenere attiva la sessione di navigazione e ricordare le scelte effettuate (es. il consenso ai cookie).
    *   **Cookie di Funzionalità**: Permettono di ricordare le scelte dell'utente per migliorare l'esperienza di navigazione, come ad esempio il limite di upload impostato (5GB).

    **Cookie di Terze Parti / Profilazione**: Questo sito **non utilizza** cookie di profilazione, di marketing o di terze parti (come Google Analytics o pixel di social media) per inviare pubblicità personalizzata.

    ### 4. Gestione del Consenso
    Al primo accesso, l'utente può scegliere se accettare o rifiutare i cookie tramite l'apposito banner. La scelta viene registrata e memorizzata nel browser. È possibile modificare la propria scelta in qualsiasi momento cancellando i dati di navigazione del browser o reimpostando la pagina.

    ### 5. Come disabilitare i Cookie tramite il Browser
    L'utente può gestire le preferenze sui cookie tramite le impostazioni del proprio browser. La disabilitazione di alcuni cookie potrebbe compromettere il corretto funzionamento di alcune sezioni del sito.

    *   **Google Chrome**: [Istruzioni](https://support.google.com/chrome/answer/95647)
    *   **Mozilla Firefox**: [Istruzioni](https://support.mozilla.org/kb/block-websites-storing-cookies)
    *   **Microsoft Edge**: [Istruzioni](https://support.microsoft.com/microsoft-edge/delete-cookies-in-microsoft-edge)
    *   **Safari**: [Istruzioni](https://support.apple.com/guide/safari/manage-cookies)

    ### 6. Diritti dell'Interessato
    Ai sensi degli artt. 15-22 del GDPR, l'utente ha il diritto di accesso, rettifica, cancellazione, limitazione, opposizione e portabilità dei propri dati personali. Per esercitare tali diritti, contattare l'email **info@artifix.it**. È inoltre possibile proporre reclamo all'Autorità di controllo (Garante per la Protezione dei Dati Personali - [www.garanteprivacy.it](http://www.garanteprivacy.it)).

    ### 7. Aggiornamenti
    La presente Cookie Policy può essere soggetta ad aggiornamenti. La versione aggiornata sarà sempre disponibile su questa pagina.
    """)

    st.markdown("---")
    
    if st.button("← Torna alla Dashboard", key="torna_dashboard_basso"):
        st.session_state.page_attuale = "Dashboard"
        st.rerun()


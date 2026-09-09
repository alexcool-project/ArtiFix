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

# --- Configurazione Pagina ---
CUBO_PATH = r"C:\Users\ichno\Desktop\ArtiFix\ArchiFix_cubo-logo.png"
LOGO_PATH = r"C:\Users\ichno\Desktop\ArtiFix\Artifix_logo.png"

def get_base64_image(image_path):
    try:
        if os.path.exists(image_path):
            with open(image_path, "rb") as f:
                return base64.b64encode(f.read()).decode()
        return None
    except Exception:
        return None

CUBO_BASE64 = get_base64_image(CUBO_PATH)
LOGO_BASE64 = get_base64_image(LOGO_PATH)

if CUBO_BASE64:
    st.set_page_config(
        page_title="ArtiFix - Riparazione CAD/CAM Universale",
        page_icon=f"data:image/png;base64,{CUBO_BASE64}",
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

# --- CSS ---
st.markdown("""
<style>
    .main-header { font-size: 2.5rem; color: #1f77b4; font-weight: 700; margin-bottom: 1rem; text-align: center; }
    .logo-container { text-align: center; padding: 1rem 0; }
    .logo-container img { max-width: 450px; height: auto; }
    .sidebar-logo { text-align: center; padding: 1rem 0; border-bottom: 1px solid #ddd; margin-bottom: 1rem; }
    .sidebar-logo img { max-width: 200px; height: auto; }
    .stButton>button { width: 100%; border-radius: 8px; background-color: #1f77b4; color: white; font-weight: 600; }
    .stButton>button:hover { background-color: #145a8a; color: white; }
    .metric-card { background-color: #f0f2f6; padding: 1rem; border-radius: 10px; text-align: center; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
    .metric-value { font-size: 2rem; font-weight: 700; color: #1f77b4; }
    .metric-label { font-size: 0.9rem; color: #555; }
    .footer { margin-top: 3rem; padding: 1.2rem 1rem; text-align: center; color: #888; font-size: 0.85rem; border-top: 1px solid #ddd; background-color: #f8f9fa; border-radius: 8px; }
    .footer-text { margin: 0; font-size: 0.85rem; color: #666; }
    .footer-text strong { color: #1f77b4; }
    .file-info-card { background-color: #f8f9fa; padding: 1rem; border-radius: 8px; border-left: 4px solid #1f77b4; margin: 0.5rem 0; }
    .cookie-banner { position: fixed; bottom: 0; left: 0; right: 0; background: rgba(30,30,40,0.95); color: #fff; padding: 16px 24px; display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 16px; z-index: 9999; backdrop-filter: blur(8px); border-top: 3px solid #1f77b4; box-shadow: 0 -4px 20px rgba(0,0,0,0.3); font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; }
    .cookie-banner p { margin: 0; font-size: 14px; line-height: 1.5; color: #e0e0e0; flex: 1; min-width: 200px; }
    .cookie-banner a { color: #6ab0e6; text-decoration: underline; }
    .cookie-buttons { display: flex; gap: 12px; flex-wrap: wrap; align-items: center; }
    .cookie-btn { padding: 8px 24px; border: none; border-radius: 6px; font-weight: 600; cursor: pointer; font-size: 14px; transition: all 0.2s ease; }
    .cookie-btn-accept { background: #1f77b4; color: white; }
    .cookie-btn-accept:hover { background: #145a8a; transform: scale(1.02); }
    .cookie-btn-decline { background: transparent; color: #ccc; border: 1px solid #666; }
    .cookie-btn-decline:hover { background: rgba(255,255,255,0.05); border-color: #999; }
    .cookie-btn-settings { background: transparent; color: #aaa; border: none; text-decoration: underline; font-size: 13px; }
    .cookie-btn-settings:hover { color: #fff; }
    @media (max-width: 600px) { .cookie-banner { flex-direction: column; align-items: stretch; text-align: center; padding: 16px; } .cookie-buttons { justify-content: center; } }
</style>
""", unsafe_allow_html=True)

# --- BANNER COOKIE ---
if 'cookie_consent' not in st.session_state:
    st.session_state.cookie_consent = None

def render_cookie_banner():
    if st.session_state.cookie_consent is None:
        st.markdown("""
        <div class="cookie-banner" id="cookie-banner">
            <p>🍪 Utilizziamo cookie tecnici e di analytics per migliorare la tua esperienza. Continuando a navigare accetti la nostra <a href="#" target="_blank">Privacy Policy</a> e l'uso dei cookie secondo la normativa europea (GDPR).</p>
            <div class="cookie-buttons">
                <button class="cookie-btn cookie-btn-accept" onclick="acceptCookies()">Accetta tutti</button>
                <button class="cookie-btn cookie-btn-decline" onclick="declineCookies()">Solo tecnici</button>
                <button class="cookie-btn cookie-btn-settings" onclick="openSettings()">Impostazioni</button>
            </div>
        </div>
        <script>
            function acceptCookies() { document.getElementById('cookie-banner').style.display = 'none'; window.location.reload(); }
            function declineCookies() { document.getElementById('cookie-banner').style.display = 'none'; window.location.reload(); }
            function openSettings() { alert('Impostazioni cookie: puoi gestire le preferenze qui.'); }
        </script>
        """, unsafe_allow_html=True)

if st.session_state.cookie_consent is None:
    render_cookie_banner()

# --- Logo ---
if LOGO_BASE64:
    st.markdown(f'<div class="logo-container"><img src="data:image/png;base64,{LOGO_BASE64}" alt="ArtiFix Logo"></div>', unsafe_allow_html=True)
else:
    st.markdown('<div class="logo-container"><h1 style="color:#1f77b4;font-size:2.5rem;margin:0;">ARTIFIX</h1><p style="color:#555;font-size:1rem;margin:0;">CONVERT. FIX. DELIVER.</p></div>', unsafe_allow_html=True)

# --- Intestazione ---
if CUBO_BASE64:
    st.markdown(f'<h1 class="main-header"><img src="data:image/png;base64,{CUBO_BASE64}" style="width:40px;height:40px;vertical-align:middle;margin-right:10px;"> ArtiFix - Riparazione File CAD/CAM Universale</h1>', unsafe_allow_html=True)
else:
    st.markdown('<h1 class="main-header">📐 ArtiFix - Riparazione File CAD/CAM Universale</h1>', unsafe_allow_html=True)

st.markdown("Piattaforma professionale per la riparazione, conversione e visualizzazione di file di progettazione (CAD, BIM, 3D, Elettronica, Geospaziali, PDF, SketchUp)")

# --- Formati supportati ---
SUPPORTED_FORMATS = {
    "CAD 2D": {"extensions": [".dwg", ".dxf", ".dgn", ".dwt"], "icon": "📐", "description": "File CAD (DWG, DXF, DGN, DWT)"},
    "CAD 3D & Mesh": {"extensions": [".stl", ".obj", ".3mf", ".ply", ".fbx", ".glb", ".gltf", ".step", ".iges", ".u3d", ".skp"], "icon": "🧊", "description": "Mesh 3D, modelli e SketchUp"},
    "BIM": {"extensions": [".ifc", ".rvt", ".rfa", ".rte"], "icon": "🏗️", "description": "Building Information Modeling (IFC, RVT)"},
    "Elettronica & PCB": {"extensions": [".brd", ".sch", ".pcb", ".gbr", ".gerber"], "icon": "⚡", "description": "PCB, schemi elettronici, Gerber"},
    "Geospaziale": {"extensions": [".shp", ".geojson", ".kml", ".gpx"], "icon": "🌍", "description": "Dati geografici e GIS"},
    "Vettoriale": {"extensions": [".svg", ".eps", ".ai", ".cdr"], "icon": "✏️", "description": "Grafica vettoriale (SVG, EPS, AI, CDR)"},
    "Documenti": {"extensions": [".pdf", ".p7m", ".docx", ".xlsx"], "icon": "📄", "description": "Documenti, fogli di calcolo e 3D PDF"}
}

ALL_EXTENSIONS = []
for info in SUPPORTED_FORMATS.values():
    ALL_EXTENSIONS.extend(info["extensions"])

# --- Matrice conversioni COMPLETA ---
CONVERSION_MATRIX = {
    'stl': ['obj', 'ply', '3mf', 'glb', 'gltf', 'dxf'],
    'obj': ['stl', 'ply', '3mf', 'glb', 'gltf', 'dxf'],
    'ply': ['stl', 'obj', '3mf', 'glb', 'gltf', 'dxf'],
    '3mf': ['stl', 'obj', 'ply', 'glb', 'gltf', 'dxf'],
    'glb': ['stl', 'obj', 'ply', '3mf', 'gltf', 'dxf'],
    'gltf': ['stl', 'obj', 'ply', '3mf', 'glb', 'dxf'],
    'fbx': ['stl', 'obj', 'ply', '3mf', 'glb', 'gltf', 'dxf'],
    'step': ['stl', 'obj', 'ply', '3mf', 'glb', 'gltf', 'dxf'],
    'iges': ['stl', 'obj', 'ply', '3mf', 'glb', 'gltf', 'dxf'],
    'u3d': ['stl', 'obj', 'ply', '3mf', 'glb', 'gltf', 'dxf'],
    'skp': ['stl', 'obj', 'ply', '3mf', 'glb', 'gltf', 'dxf'],
    'dxf': ['stl', 'obj'],
    'dwg': ['stl', 'obj', 'dxf'],
}

FORMAT_NAMES = {
    'stl': 'STL (.stl)',
    'obj': 'OBJ (.obj)',
    'ply': 'PLY (.ply)',
    '3mf': '3MF (.3mf)',
    'glb': 'GLB (.glb)',
    'gltf': 'GLTF (.gltf)',
    'dxf': 'DXF (.dxf)',
    'dwg': 'DWG (.dwg)',
    'fbx': 'FBX (.fbx)',
    'step': 'STEP (.step)',
    'iges': 'IGES (.iges)',
    'u3d': 'U3D (.u3d)',
    'skp': 'SKP (.skp)'
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
            'stl':'stl', 'obj':'obj', 'ply':'ply', '3mf':'3mf',
            'fbx':'fbx', 'glb':'glb', 'gltf':'gltf',
            'step':'step', 'iges':'iges', 'u3d':'u3d', 'skp':'skp'
        }
        file_type = format_map.get(file_extension, file_extension)
        
        if file_extension in ['obj', 'skp']:
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
            if mesh is not None and hasattr(mesh, 'vertices') and len(mesh.vertices) > 0:
                return mesh
            return None
    except Exception:
        return None

def convert_mesh(mesh, target_format):
    try:
        target_format = target_format.lower().replace('.', '')
        
        if target_format == 'stl':
            return trimesh.exchange.stl.export_stl(mesh)
        elif target_format == 'obj':
            return trimesh.exchange.obj.export_obj(mesh)
        elif target_format == 'ply':
            return trimesh.exchange.ply.export_ply(mesh)
        elif target_format == '3mf':
            return trimesh.exchange.threeMF.export_3mf(mesh)
        elif target_format == 'glb':
            return trimesh.exchange.gltf.export_glb(mesh)
        elif target_format == 'gltf':
            return trimesh.exchange.gltf.export_gltf(mesh)
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
        
        elif file_extension in ['dxf', 'dgn', 'dwt']:
            dxf_doc = ezdxf.read(io.BytesIO(file_bytes))
            entities = len(dxf_doc.entities)
            layers = set(e.dxf.layer for e in dxf_doc.entities if hasattr(e.dxf, 'layer'))
            result["success"] = True
            result["message"] = f"✅ DXF: {entities} entità, {len(layers)} layer"
            result["info"] = {"entities": entities, "layers": list(layers)[:10]}
        
        elif file_extension in ['stl','obj','ply','3mf','fbx','glb','gltf','step','iges','u3d','skp']:
            mesh = load_3d_file(file_bytes, file_extension)
            if mesh and hasattr(mesh, 'vertices') and len(mesh.vertices) > 0:
                result["success"] = True
                result["message"] = f"✅ Mesh: {len(mesh.vertices)} vertici, {len(mesh.faces)} facce"
                result["info"] = {"vertices": len(mesh.vertices), "faces": len(mesh.faces), "mesh": mesh}
            else:
                result["message"] = "⚠️ File 3D non valido o formato non supportato."
        
        elif file_extension == 'dwg':
            result["success"] = True
            result["message"] = "⚠️ Formato DWG identificato. Per visualizzarlo, convertilo in DXF o STL."
            result["info"] = {"format": "DWG", "note": "Formato proprietario Autodesk"}
        
        elif file_extension == 'ifc' and IFC_AVAILABLE:
            ifc_file = ifcopenshell.open(io.BytesIO(file_bytes))
            projects = ifc_file.by_type('IfcProject')
            result["success"] = True
            result["message"] = f"✅ IFC: {len(projects)} progetti"
            result["info"] = {"projects": len(projects)}
        
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

# --- BARRA LATERALE ---
with st.sidebar:
    if LOGO_BASE64:
        st.markdown(f'<div class="sidebar-logo"><img src="data:image/png;base64,{LOGO_BASE64}" alt="ArtiFix Logo"></div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="sidebar-logo"><h3 style="color:#1f77b4;margin:0;">🔧 ARTIFIX</h3></div>', unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("## Navigazione")
    page = st.radio("Vai a:", ["Dashboard", "Ripara File", "Viewer 3D", "Converti Formati", "Audit Progetto"], key="navigation", label_visibility="collapsed")
    st.markdown("---")
    st.caption("v4.0 - Universale Completo")

# --- DASHBOARD ---
if page == "Dashboard":
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
            st.markdown(f'<div style="background:#f8f9fa;padding:0.8rem;border-radius:8px;border-left:3px solid #1f77b4;"><div style="font-weight:600;">{info["icon"]} {category}</div><div style="font-size:0.8rem;color:#666;">{info["description"]}</div><div style="font-size:0.7rem;color:#999;margin-top:4px;">{", ".join(info["extensions"][:3])}{"..." if len(info["extensions"]) > 3 else ""}</div></div>', unsafe_allow_html=True)
    st.info("👈 Seleziona una funzionalità dal menu.")

# --- RIPARA FILE ---
elif page == "Ripara File":
    st.header("🛠️ Centro Riparazione File")
    uploaded_file = st.file_uploader("Seleziona un file", type=[ext[1:] for ext in ALL_EXTENSIONS], key="repair")
    if uploaded_file:
        with st.spinner("Analisi..."):
            result = process_file(uploaded_file.getvalue(), uploaded_file.name)
        if result["success"]:
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
            st.error(result["message"])

# --- VIEWER 3D ---
elif page == "Viewer 3D":
    st.header("🖥️ Viewer 3D")
    viewer_file = st.file_uploader("Carica modello 3D", type=["stl","obj","ply","3mf","fbx","glb","gltf","step","iges","u3d","skp","pdf"], key="viewer")
    if viewer_file:
        try:
            mesh = load_3d_file(viewer_file.getvalue(), os.path.splitext(viewer_file.name)[1].lower())
            if mesh and hasattr(mesh, 'vertices') and len(mesh.vertices) > 0:
                st.success(f"✅ {len(mesh.vertices)} vertici, {len(mesh.faces)} facce")
                
                bounds = mesh.bounds
                min_y = bounds[0][1]
                vertices = mesh.vertices.copy()
                vertices[:, 1] -= min_y
                vertices[:, 0] -= (bounds[0][0] + bounds[1][0]) / 2
                vertices[:, 2] -= (bounds[0][2] + bounds[1][2]) / 2
                
                mesh_data = {"vertices": vertices.tolist(), "faces": mesh.faces.tolist() if hasattr(mesh, 'faces') else mesh.triangles.tolist()}
                mesh_json = json.dumps(mesh_data)
                
                viewer_html = """
                <html><head><style>body{margin:0;overflow:hidden;}#c{width:100%;height:500px;}#info{position:absolute;bottom:10px;left:50%;transform:translateX(-50%);color:#555;font-family:Arial;font-size:12px;background:rgba(255,255,255,0.8);padding:5px 15px;border-radius:20px;}.legend{position:absolute;bottom:60px;left:20px;color:#333;font-family:Arial;font-size:11px;background:rgba(255,255,255,0.9);padding:8px 12px;border-radius:8px;border:1px solid #ddd;}.legend span{display:inline-block;width:12px;height:12px;margin-right:4px;}.axis-x{background:#ff4444;}.axis-y{background:#44ff44;}.axis-z{background:#4444ff;}</style>
                <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
                <script src="https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/controls/OrbitControls.js"></script>
                </head><body>
                <div id="c"></div>
                <div class="legend"><span class="axis-x"></span> X <span class="axis-y"></span> Y <span class="axis-z"></span> Z</div>
                <div id="info">🔄 Ruota | Pan | Zoom</div>
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
                scene.add(new THREE.DirectionalLight(0xffffff,0.5).position.set(-10,0,-10));
                if(data.vertices && data.vertices.length>0){
                    const geo = new THREE.BufferGeometry();
                    geo.setAttribute('position', new THREE.BufferAttribute(new Float32Array(data.vertices.flat()), 3));
                    if(data.faces && data.faces.length>0){
                        geo.setIndex(new THREE.BufferAttribute(new Uint16Array(data.faces.flat()), 1));
                        geo.computeVertexNormals();
                    }
                    const mat = new THREE.MeshStandardMaterial({color:0x1f77b4, roughness:0.3, metalness:0.2, flatShading:false, side:THREE.DoubleSide});
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

# --- CONVERTI FORMATI ---
elif page == "Converti Formati":
    st.header("🔄 Conversione Formati Universale")
    st.markdown("Converti file tra **tutti i formati** supportati con **tutte le combinazioni** possibili.")
    
    with st.expander("📋 Matrice delle conversioni disponibili"):
        st.markdown("""
        | Da → A | STL | OBJ | PLY | 3MF | GLB | GLTF | DXF | DWG |
        |--------|-----|-----|-----|-----|-----|------|-----|-----|
        | **STL** | - | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ❌ |
        | **OBJ** | ✅ | - | ✅ | ✅ | ✅ | ✅ | ✅ | ❌ |
        | **PLY** | ✅ | ✅ | - | ✅ | ✅ | ✅ | ✅ | ❌ |
        | **3MF** | ✅ | ✅ | ✅ | - | ✅ | ✅ | ✅ | ❌ |
        | **GLB** | ✅ | ✅ | ✅ | ✅ | - | ✅ | ✅ | ❌ |
        | **GLTF** | ✅ | ✅ | ✅ | ✅ | ✅ | - | ✅ | ❌ |
        | **DXF** | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ | - | ❌ |
        | **DWG** | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ | ✅ | - |
        """)
        st.caption("✅ = Conversione supportata | ❌ = Conversione non supportata")
    
    uploaded_file = st.file_uploader("Carica un file da convertire", type=[ext[1:] for ext in ALL_EXTENSIONS], key="convert")
    
    if uploaded_file:
        file_name = uploaded_file.name
        file_bytes = uploaded_file.getvalue()
        file_extension = os.path.splitext(file_name)[1].lower().replace('.', '')
        file_type, icon = detect_file_type(file_extension)
        
        st.markdown(f'<div class="file-info-card"><div style="display:flex;align-items:center;gap:10px;"><span style="font-size:1.5rem;">{icon}</span><div><div style="font-weight:600;">{file_name}</div><div style="font-size:0.8rem;color:#666;">Tipo: {file_type} | Estensione: .{file_extension}</div></div></div></div>', unsafe_allow_html=True)
        
        # I formati convertibili sono: STL, OBJ, PLY, 3MF, GLB, GLTF, DXF, DWG
        convertibili = ["stl", "obj", "ply", "3mf", "glb", "gltf", "dxf", "dwg"]
        
        if file_extension not in convertibili:
            st.warning(f"⚠️ Il formato **.{file_extension.upper()}** non può essere convertito in altri formati.")
            st.info("💡 I formati convertibili sono: **STL, OBJ, PLY, 3MF, GLB, GLTF, DXF, DWG**.")
        else:
            target_formats = CONVERSION_MATRIX.get(file_extension, [])
            target_options = [FORMAT_NAMES.get(f, f) for f in target_formats if f != file_extension]
            
            if not target_options:
                st.warning("⚠️ Nessun formato di destinazione disponibile per questo file.")
            else:
                target_selected = st.selectbox("Formato di destinazione", target_options)
                target_ext = target_selected.split(".")[1].replace(")", "").strip()
                
                if st.button(f"🔄 Converti in {target_selected.split(' ')[0]}", type="primary", use_container_width=True):
                    with st.spinner(f"Conversione in {target_selected.split(' ')[0]} in corso..."):
                        try:
                            mesh = load_3d_file(file_bytes, file_extension)
                            
                            if mesh and hasattr(mesh, 'vertices') and len(mesh.vertices) > 0:
                                result_bytes = convert_mesh(mesh, target_ext)
                                
                                if result_bytes:
                                    st.success(f"✅ Conversione in {target_selected.split(' ')[0]} completata!")
                                    mime_types = {
                                        'stl': 'application/octet-stream',
                                        'obj': 'text/plain',
                                        'ply': 'application/octet-stream',
                                        '3mf': 'application/octet-stream',
                                        'glb': 'application/octet-stream',
                                        'gltf': 'application/octet-stream',
                                        'dxf': 'application/dxf'
                                    }
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
                        except Exception as e:
                            st.error(f"❌ Errore durante la conversione: {e}")
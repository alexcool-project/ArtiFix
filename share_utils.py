import base64
import os

def generate_standalone_viewer_html(file_path: str, model_name: str) -> str:
    """
    Legge un file 3D (es. STL) e genera una stringa HTML autonoma contenente 
    il viewer interattivo Three.js, l'identità visiva ArtiFix e il modello incorporato in Base64.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File non trovato: {file_path}")

    # Leggi il file binario e convertilo in Base64 per l'embedding nativo nell'HTML
    with open(file_path, "rb") as f:
        file_bytes = f.read()
        encoded_data = base64.b64encode(file_bytes).decode("utf-8")

    file_size_mb = len(file_bytes) / (1024 * 1024)
    file_ext = os.path.splitext(file_path)[1].lower().replace('.', '')

    html_content = f"""<!DOCTYPE html>
<html lang="it">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ArtiFix 3D Viewer - {model_name}</title>
    <style>
        body, html {{
            margin: 0; padding: 0; width: 100vw; height: 100vh;
            overflow: hidden; background-color: #0b0f19; font-family: system-ui, -apple-system, sans-serif;
            color: #f8fafc;
        }}
        #canvas-container {{ width: 100vw; height: 100vh; display: block; }}
        
        /* Brand Header & Watermark ArtiFix */
        .artifix-brand {{
            position: absolute; top: 20px; left: 20px; display: flex; align-items: center; gap: 12px;
            background: rgba(15, 23, 42, 0.85); padding: 10px 16px; border-radius: 12px;
            border: 1px solid rgba(148, 163, 184, 0.2); backdrop-filter: blur(8px); z-index: 10;
            box-shadow: 0 4px 20px rgba(0,0,0,0.5);
        }}
        .brand-logo {{ font-weight: 800; font-size: 16px; letter-spacing: 0.5px; color: #38bdf8; text-decoration: none; display: flex; align-items: center; gap: 8px; }}
        .brand-logo:hover {{ color: #7dd3fc; }}
        .model-badge {{ font-size: 12px; color: #94a3b8; border-left: 1px solid rgba(148, 163, 184, 0.3); padding-left: 12px; }}

        /* UI Control Panel */
        .ui-panel {{
            position: absolute; top: 20px; right: 20px; background: rgba(15, 23, 42, 0.85);
            padding: 16px; border-radius: 12px; color: #fff; box-shadow: 0 4px 20px rgba(0,0,0,0.5);
            backdrop-filter: blur(8px); z-index: 10; display: flex; flex-direction: column; gap: 12px; width: 220px;
            border: 1px solid rgba(148, 163, 184, 0.2);
        }}
        .ui-panel label {{ font-size: 11px; color: #94a3b8; font-weight: bold; letter-spacing: 0.5px; }}
        .ui-panel input[type="range"] {{ width: 100%; cursor: pointer; accent-color: #38bdf8; }}
        .btn-group {{ display: flex; gap: 6px; }}
        .ui-btn {{ background: #1e293b; color: #f8fafc; border: 1px solid #334155; padding: 7px 10px; border-radius: 6px; cursor: pointer; font-size: 12px; font-weight: bold; flex: 1; text-align: center; transition: all 0.2s; }}
        .ui-btn:hover {{ background: #334155; }}
        .ui-btn.active {{ background: #0284c7; border-color: #38bdf8; }}
        .action-btn {{ width: 100%; background: #0284c7; color: #fff; border: none; padding: 9px; border-radius: 6px; cursor: pointer; font-size: 12px; font-weight: bold; margin-top: 4px; transition: background 0.2s; }}
        .action-btn:hover {{ background: #0369a1; }}

        /* Info Bar in basso */
        #info-bar {{
            position: absolute; bottom: 16px; left: 50%; transform: translateX(-50%);
            background: rgba(15, 23, 42, 0.85); color: #94a3b8; padding: 8px 18px; border-radius: 20px;
            font-size: 12px; z-index: 10; border: 1px solid rgba(148, 163, 184, 0.2); backdrop-filter: blur(8px);
        }}

        /* Modale Proprietà File */
        #modal-overlay {{
            position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; background: rgba(0,0,0,0.7);
            display: flex; justify-content: center; align-items: center; z-index: 100; backdrop-filter: blur(6px);
        }}
        .modal-content {{
            background: #0f172a; padding: 25px; border-radius: 14px; width: 350px; color: #f8fafc;
            box-shadow: 0 10px 30px rgba(0,0,0,0.6); border: 1px solid #334155;
        }}
        .modal-content h3 {{ margin-top: 0; color: #38bdf8; font-size: 18px; border-bottom: 1px solid #334155; padding-bottom: 10px; }}
        .modal-row {{ display: flex; justify-content: space-between; margin: 10px 0; font-size: 13px; border-bottom: 1px solid #1e293b; padding-bottom: 6px; }}
        .modal-row span:last-child {{ color: #cbd5e1; font-weight: bold; }}
        .close-modal {{ background: #334155; color: #fff; border: none; padding: 8px 15px; border-radius: 6px; cursor: pointer; width: 100%; margin-top: 15px; font-weight: bold; }}
        .close-modal:hover {{ background: #475569; }}
    </style>
    <!-- Import di Three.js e loader tramite CDN ufficiale -->
    <script async src="https://unpkg.com/es-module-shims@1.6.3/dist/es-module-shims.js"></script>
    <script type="importmap">
      {{
        "imports": {
          "three": "https://unpkg.com/three@0.160.0/build/three.module.js",
          "three/addons/": "https://unpkg.com/three@0.160.0/examples/jsm/"
        }
      }}
    </script>
</head>
<body>
    <div id="canvas-container"></div>
    
    <!-- Header con Brand ArtiFix e Cubo interattivo -->
    <div class="artifix-brand">
        <a href="https://artifix.it" target="_blank" class="brand-logo" title="Visita ArtiFix.it">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"></path><polyline points="3.27 6.96 12 12.01 20.73 6.96"></polyline><line x1="12" y1="22.08" x2="12" y2="12"></line></svg>
            ArtiFix
        </a>
        <div class="model-badge">{model_name}</div>
    </div>

    <!-- Pannello UI laterale -->
    <div class="ui-panel">
        <label>OPACITÀ</label>
        <input type="range" id="opacityRange" min="0.1" max="1" step="0.05" value="1">
        
        <label>VISUALIZZAZIONE</label>
        <div class="btn-group">
            <button class="ui-btn active" id="btnSmooth">Smooth</button>
            <button class="ui-btn" id="btnWire">Wireframe</button>
        </div>

        <label>STRUMENTI</label>
        <button class="action-btn" id="btnPhoto">📸 Scatta Foto</button>
        <button class="action-btn" id="btnInfo" style="background: #1e293b; border: 1px solid #334155;">ℹ️ Proprietà File</button>
    </div>

    <div id="info-bar">ArtiFix 3D Viewer | Z-up System</div>

    <!-- Modale Proprietà -->
    <div id="modal-overlay" style="display: none;">
        <div class="modal-content">
            <h3>Proprietà Modello 3D</h3>
            <div class="modal-row"><span>Nome File:</span><span>{model_name}.{file_ext}</span></div>
            <div class="modal-row"><span>Formato:</span><span>{file_ext.upper()}</span></div>
            <div class="modal-row"><span>Dimensione:</span><span>{file_size_mb:.2f} MB</span></div>
            <div class="modal-row"><span>Vertici:</span><span id="lblVerts">-</span></div>
            <div class="modal-row"><span>Facce:</span><span id="lblFaces">-</span></div>
            <button class="close-modal" id="btnCloseModal">Chiudi</button>
        </div>
    </div>

    <script type="module">
        import * as THREE from 'three';
        import {{ OrbitControls }} from 'three/addons/controls/OrbitControls.js';
        import {{ STLLoader }} from 'three/addons/loaders/STLLoader.js';

        const container = document.getElementById('canvas-container');
        
        const scene = new THREE.Scene();
        scene.background = new THREE.Color(0x0b0f19);

        const camera = new THREE.PerspectiveCamera(45, window.innerWidth / window.innerHeight, 0.1, 5000);
        camera.up.set(0, 0, 1);

        const renderer = new THREE.WebGLRenderer({{ antialias: true, alpha: true, preserveDrawingBuffer: true }});
        renderer.setSize(window.innerWidth, window.innerHeight);
        renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
        container.appendChild(renderer.domElement);

        const controls = new OrbitControls(camera, renderer.domElement);
        controls.enableDamping = true;
        controls.dampingFactor = 0.05;
        controls.screenSpacePanning = true;

        scene.add(new THREE.AmbientLight(0xffffff, 0.8));
        const dirLight = new THREE.DirectionalLight(0xffffff, 1.2);
        dirLight.position.set(300, 300, 500);
        scene.add(dirLight);

        // Decodifica del modello in Base64 incorporato nel file HTML
        const base64Data = "{encoded_data}";
        const binaryString = atob(base64Data);
        const len = binaryString.length;
        const bytes = new Uint8Array(len);
        for (let i = 0; i < len; i++) {{
            bytes[i] = binaryString.charCodeAt(i);
        }}

        const loader = new STLLoader();
        const geometry = loader.parse(bytes.buffer);
        geometry.computeVertexNormals();
        geometry.computeBoundingBox();
        
        const box = geometry.boundingBox;
        const size = box.getSize(new THREE.Vector3());
        const center = box.getCenter(new THREE.Vector3());
        const maxDim = Math.max(size.x, size.y, size.z);

        geometry.translate(-center.x, -center.y, -box.min.z);

        const material = new THREE.MeshStandardMaterial({{
            color: 0x38bdf8,
            roughness: 0.25,
            metalness: 0.1,
            side: THREE.DoubleSide
        }});

        const mesh = new THREE.Mesh(geometry, material);
        scene.add(mesh);

        // Statistiche Vertici e Facce
        if (geometry.index) {{
            document.getElementById('lblFaces').innerText = geometry.index.count / 3;
        }} else if (geometry.attributes.position) {{
            document.getElementById('lblFaces').innerText = geometry.attributes.position.count / 3;
        }}
        if (geometry.attributes.position) {{
            document.getElementById('lblVerts').innerText = geometry.attributes.position.count;
        }}

        // Griglia e Assi Z-up allineati
        const axisLength = maxDim * 0.7;
        const gridSize = maxDim * 2.5;
        scene.add(new THREE.ArrowHelper(new THREE.Vector3(1,0,0), new THREE.Vector3(0,0,0), axisLength, 0xef4444, axisLength*0.1, axisLength*0.06));
        scene.add(new THREE.ArrowHelper(new THREE.Vector3(0,1,0), new THREE.Vector3(0,0,0), axisLength, 0x22c55e, axisLength*0.1, axisLength*0.06));
        scene.add(new THREE.ArrowHelper(new THREE.Vector3(0,0,1), new THREE.Vector3(0,0,0), axisLength, 0x3b82f6, axisLength*0.1, axisLength*0.06));

        const grid = new THREE.GridHelper(gridSize, 20, 0x475569, 0x1e293b);
        grid.rotation.x = Math.PI / 2;
        scene.add(grid);

        controls.target.set(0, 0, size.z / 2);
        camera.position.set(maxDim * 1.5, -maxDim * 1.5, maxDim * 1.2);
        controls.update();

        // Gestione Interattività UI
        document.getElementById('opacityRange').addEventListener('input', (e) => {{
            material.transparent = e.target.value < 1;
            material.opacity = parseFloat(e.target.value);
        }});

        document.getElementById('btnSmooth').addEventListener('click', () => {{
            material.wireframe = false;
            document.getElementById('btnSmooth').classList.add('active');
            document.getElementById('btnWire').classList.remove('active');
        }});

        document.getElementById('btnWire').addEventListener('click', () => {{
            material.wireframe = true;
            document.getElementById('btnWire').classList.add('active');
            document.getElementById('btnSmooth').classList.remove('active');
        }});

        document.getElementById('btnPhoto').addEventListener('click', () => {{
            renderer.render(scene, camera);
            const dataURL = renderer.domElement.toDataURL('image/png');
            const link = document.createElement('a');
            link.download = '{model_name}_screenshot.png';
            link.href = dataURL;
            link.click();
        }});

        const modal = document.getElementById('modal-overlay');
        document.getElementById('btnInfo').addEventListener('click', () => {{ modal.style.display = 'flex'; }});
        document.getElementById('btnCloseModal').addEventListener('click', () => {{ modal.style.display = 'none'; }});

        window.addEventListener('resize', () => {{
            camera.aspect = window.innerWidth / window.innerHeight;
            camera.updateProjectionMatrix();
            renderer.setSize(window.innerWidth, window.innerHeight);
        }});

        function animate() {{
            requestAnimationFrame(animate);
            controls.update();
            renderer.render(scene, camera);
        }}
        animate();
    </script>
</body>
</html>
"""
    return html_content

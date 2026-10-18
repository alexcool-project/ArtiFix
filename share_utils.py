import streamlit as st
import base64
import os

def render_share_section(uploaded_file, t, lang="it"):
    st.markdown("---")
    st.markdown(f"### {t('share_section_title', default='Condividi il file 3D generato')}")
    
    project_name = st.text_input(
        t('share_project_name', default='Nome del progetto (visibile al cliente)'),
        value=os.path.splitext(uploaded_file.name)[0] if uploaded_file else "Modello_3D"
    )
    
    include_qr = st.checkbox(t('share_include_qr', default='Genera anche il QR Code'), value=True)
    
    if st.button(t('share_generate_button', default='🚀 Genera link pubblico condivisibile'), type="primary", use_container_width=True):
        file_bytes = uploaded_file.getvalue()
        file_ext = os.path.splitext(uploaded_file.name)[1].lower().replace('.', '')
        b64_data = base64.b64encode(file_bytes).decode('utf-8')
        file_size_mb = len(file_bytes) / (1024 * 1024)
        
        html_content = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>{project_name} - ArtiFix 3D Viewer</title>
    <style>
        body {{ margin: 0; overflow: hidden; background: #1a1a1a; font-family: Arial, sans-serif; }}
        #canvas-container {{ width: 100vw; height: 100vh; display: block; }}
        .ui-panel {{
            position: absolute; top: 20px; right: 20px; background: rgba(30, 30, 30, 0.9);
            padding: 15px; border-radius: 10px; color: #fff; box-shadow: 0 4px 15px rgba(0,0,0,0.4);
            backdrop-filter: blur(6px); z-index: 10; display: flex; flex-direction: column; gap: 12px; width: 220px;
        }}
        .ui-panel label {{ font-size: 11px; color: #aaa; font-weight: bold; letter-spacing: 0.5px; }}
        .ui-panel input[type="range"] {{ width: 100%; cursor: pointer; accent-color: #1f77b4; }}
        .btn-group {{ display: flex; gap: 6px; }}
        .ui-btn {{ background: #333; color: #fff; border: 1px solid #555; padding: 7px 10px; border-radius: 6px; cursor: pointer; font-size: 12px; font-weight: bold; flex: 1; text-align: center; transition: background 0.2s; }}
        .ui-btn:hover {{ background: #444; }}
        .ui-btn.active {{ background: #1f77b4; border-color: #1f77b4; }}
        .action-btn {{ width: 100%; background: #1f77b4; color: #fff; border: none; padding: 9px; border-radius: 6px; cursor: pointer; font-size: 12px; font-weight: bold; margin-top: 4px; }}
        .action-btn:hover {{ background: #155a8a; }}
        #info-bar {{
            position: absolute; bottom: 15px; left: 50%; transform: translateX(-50%);
            background: rgba(0,0,0,0.75); color: #fff; padding: 8px 18px; border-radius: 20px;
            font-size: 12px; z-index: 10; border: 1px solid rgba(255,255,255,0.1);
        }}
        #modal-overlay {{
            position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; background: rgba(0,0,0,0.6);
            display: flex; justify-content: center; align-items: center; z-index: 100; backdrop-filter: blur(4px);
        }}
        .modal-content {{
            background: #242424; padding: 25px; border-radius: 12px; width: 350px; color: #fff;
            box-shadow: 0 10px 30px rgba(0,0,0,0.5); border: 1px solid #444;
        }}
        .modal-content h3 {{ margin-top: 0; color: #1f77b4; font-size: 18px; }}
        .modal-row {{ display: flex; justify-content: space-between; margin: 10px 0; font-size: 13px; border-bottom: 1px solid #333; padding-bottom: 6px; }}
        .modal-row span:last-child {{ color: #ccc; font-weight: bold; }}
        .close-modal {{ background: #444; color: #fff; border: none; padding: 8px 15px; border-radius: 6px; cursor: pointer; width: 100%; margin-top: 15px; font-weight: bold; }}
        .close-modal:hover {{ background: #555; }}
    </style>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/controls/OrbitControls.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/loaders/STLLoader.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/loaders/OBJLoader.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/loaders/PLYLoader.js"></script>
</head>
<body>
    <div id="canvas-container"></div>
    <div id="info-bar">{project_name} | Z-up View</div>
    
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
        <button class="action-btn" id="btnInfo" style="background: #333; border: 1px solid #555;">ℹ️ Proprietà File</button>
    </div>

    <div id="modal-overlay" style="display: none;">
        <div class="modal-content">
            <h3>Proprietà Modello</h3>
            <div class="modal-row"><span>Nome File:</span><span>{project_name}.{file_ext}</span></div>
            <div class="modal-row"><span>Formato:</span><span>{file_ext.upper()}</span></div>
            <div class="modal-row"><span>Dimensione:</span><span>{file_size_mb:.2f} MB</span></div>
            <div class="modal-row"><span>Vertici:</span><span id="lblVerts">-</span></div>
            <div class="modal-row"><span>Facce:</span><span id="lblFaces">-</span></div>
            <button class="close-modal" id="btnCloseModal">Chiudi</button>
        </div>
    </div>

    <script>
        const container = document.getElementById('canvas-container');
        const scene = new THREE.Scene();
        scene.background = new THREE.Color(0x1a1a1a);

        const camera = new THREE.PerspectiveCamera(45, window.innerWidth / window.innerHeight, 0.1, 50000);
        camera.up.set(0, 0, 1);

        const renderer = new THREE.WebGLRenderer({{ antialias: true, preserveDrawingBuffer: true }});
        renderer.setPixelRatio(window.devicePixelRatio);
        renderer.setSize(window.innerWidth, window.innerHeight);
        container.appendChild(renderer.domElement);

        const controls = new THREE.OrbitControls(camera, renderer.domElement);
        controls.enableDamping = true;
        controls.dampingFactor = 0.05;
        controls.screenSpacePanning = true;

        scene.add(new THREE.AmbientLight(0xffffff, 0.7));
        const dirLight = new THREE.DirectionalLight(0xffffff, 0.8);
        dirLight.position.set(15, -15, 30);
        scene.add(dirLight);

        const b64Data = "{b64_data}";
        const binaryString = atob(b64Data);
        const len = binaryString.length;
        const bytes = new Uint8Array(len);
        for (let i = 0; i < len; i++) {{
            bytes[i] = binaryString.charCodeAt(i);
        }}

        const ext = "{file_ext}";
        let loadedMesh = null;
        const material = new THREE.MeshStandardMaterial({{ color: 0x1f77b4, roughness: 0.4, metalness: 0.1, side: THREE.DoubleSide }});

        function setupModel(geometry) {{
            geometry.computeVertexNormals();
            geometry.computeBoundingBox();
            const box = geometry.boundingBox;
            const size = box.getSize(new THREE.Vector3());
            const center = box.getCenter(new THREE.Vector3());
            const maxDim = Math.max(size.x, size.y, size.z);

            geometry.translate(-center.x, -center.y, -box.min.z);

            loadedMesh = new THREE.Mesh(geometry, material);
            scene.add(loadedMesh);

            if (geometry.index) {{
                document.getElementById('lblFaces').innerText = geometry.index.count / 3;
            }} else if (geometry.attributes.position) {{
                document.getElementById('lblFaces').innerText = geometry.attributes.position.count / 3;
            }}
            if (geometry.attributes.position) {{
                document.getElementById('lblVerts').innerText = geometry.attributes.position.count;
            }}

            const axisLength = maxDim * 0.7;
            const gridSize = maxDim * 2.5;

            scene.add(new THREE.ArrowHelper(new THREE.Vector3(1,0,0), new THREE.Vector3(0,0,0), axisLength, 0xff4444, axisLength*0.1, axisLength*0.06));
            scene.add(new THREE.ArrowHelper(new THREE.Vector3(0,1,0), new THREE.Vector3(0,0,0), axisLength, 0x44ff44, axisLength*0.1, axisLength*0.06));
            scene.add(new THREE.ArrowHelper(new THREE.Vector3(0,0,1), new THREE.Vector3(0,0,0), axisLength, 0x4444ff, axisLength*0.1, axisLength*0.06));

            const grid = new THREE.GridHelper(gridSize, 20, 0x555555, 0x333333);
            grid.rotation.x = Math.PI / 2;
            grid.position.set(0, 0, 0);
            scene.add(grid);

            controls.target.set(0, 0, size.z / 2);
            camera.position.set(maxDim * 1.5, -maxDim * 1.5, maxDim * 1.2);
            controls.update();
        }}

        if (ext === 'stl') {{
            const loader = new THREE.STLLoader();
            const geom = loader.parse(bytes.buffer);
            setupModel(geom);
        }} else if (ext === 'obj') {{
            const textDecoder = new TextDecoder();
            const objText = textDecoder.decode(bytes);
            const loader = new THREE.OBJLoader();
            const object = loader.parse(objText);
            const group = new THREE.Group();
            group.add(object);
            
            scene.add(group);
            const box = new THREE.Box3().setFromObject(group);
            const size = box.getSize(new THREE.Vector3());
            const center = box.getCenter(new THREE.Vector3());
            const maxDim = Math.max(size.x, size.y, size.z);
            
            group.position.set(-center.x, -center.y, -box.min.z);
            
            let totalVerts = 0;
            let totalFaces = 0;
            object.traverse((child) => {{
                if (child.isMesh && child.geometry) {{
                    const g = child.geometry;
                    if (g.attributes.position) totalVerts += g.attributes.position.count;
                    if (g.index) totalFaces += g.index.count / 3;
                    else if (g.attributes.position) totalFaces += g.attributes.position.count / 3;
                }}
            }});
            document.getElementById('lblVerts').innerText = totalVerts;
            document.getElementById('lblFaces').innerText = totalFaces;

            const axisLength = maxDim * 0.7;
            const gridSize = maxDim * 2.5;
            scene.add(new THREE.ArrowHelper(new THREE.Vector3(1,0,0), new THREE.Vector3(0,0,0), axisLength, 0xff4444, axisLength*0.1, axisLength*0.06));
            scene.add(new THREE.ArrowHelper(new THREE.Vector3(0,1,0), new THREE.Vector3(0,0,0), axisLength, 0x44ff44, axisLength*0.1, axisLength*0.06));
            scene.add(new THREE.ArrowHelper(new THREE.Vector3(0,0,1), new THREE.Vector3(0,0,0), axisLength, 0x4444ff, axisLength*0.1, axisLength*0.06));
            
            const grid = new THREE.GridHelper(gridSize, 20, 0x555555, 0x333333);
            grid.rotation.x = Math.PI / 2;
            scene.add(grid);
            
            controls.target.set(0, 0, size.z / 2);
            camera.position.set(maxDim * 1.5, -maxDim * 1.5, maxDim * 1.2);
            controls.update();
        }}

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
            link.download = '{project_name}_screenshot.png';
            link.href = dataURL;
            link.click();
        }});

        const modal = document.getElementById('modal-overlay');
        document.getElementById('btnInfo').addEventListener('click', () => {{ modal.style.display = 'flex'; }});
        document.getElementById('btnCloseModal').addEventListener('click', () => {{ modal.style.display = 'none'; }});

        function animate() {{
            requestAnimationFrame(animate);
            controls.update();
            renderer.render(scene, camera);
        }}
        animate();

        window.addEventListener('resize', () => {{
            camera.aspect = window.innerWidth / window.innerHeight;
            camera.updateProjectionMatrix();
            renderer.setSize(window.innerWidth, window.innerHeight);
        }});
    </script>
</body>
</html>"""
        
        # Generiamo il Data URI Base64 pubblico/condivisibile
        b64_html = base64.b64encode(html_content.encode('utf-8')).decode('utf-8')
        data_url = f"data:text/html;base64,{b64_html}"
        
        st.success("Link pubblico condivisibile generato con successo!")
        
        # Mostriamo il link pronto per essere copiato con un comodo box di testo e pulsante
        st.text_input(
            "Copia il link web condivisibile (funziona ovunque senza scaricare file):",
            value=data_url,
            key="shared_link_output"
        )
        
        # Pulsante per aprire direttamente il link in una nuova scheda
        st.markdown(
            f'<a href="{data_url}" target="_blank" style="display:block; text-align:center; background:#1f77b4; color:#ffffff; padding:10px; border-radius:6px; text-decoration:none; font-weight:bold; margin-top:10px;">🌐 Apri Viewer in Nuova Scheda</a>',
            unsafe_allow_html=True
        )
        
        if include_qr:
            try:
                import qrcode
                img = qrcode.make(data_url)
                buf = io.BytesIO()
                img.save(buf, format="PNG")
                st.image(buf.getvalue(), caption="QR Code per condivisione rapida su dispositivi mobili", width=200)
            except Exception:
                pass

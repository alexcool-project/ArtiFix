import streamlit as st
import base64
import os

def render_share_section(uploaded_file, t, lang="it"):
    st.markdown("---")
    
    is_en = (lang == "en")
    title_text = "Share 3D Model" if is_en else "Condividi il modello 3D"
    name_label = "Project Name" if is_en else "Nome del progetto"
    btn_label = "Genera Link di Condivisione" if is_en else "Genera Link di Condivisione"
    
    st.markdown(f"### {title_text}")
    
    project_name = st.text_input(
        name_label,
        value=os.path.splitext(uploaded_file.name)[0] if uploaded_file else "Modello_3D",
        key="input_project_name_share"
    )
    
    if st.button(btn_label, type="primary", use_container_width=True, key="btn_generate_share_link"):
        file_bytes = uploaded_file.getvalue()
        file_ext = os.path.splitext(uploaded_file.name)[1].lower().replace('.', '')
        b64_data = base64.b64encode(file_bytes).decode('utf-8')
        
        html_content = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>{project_name} - 3D Viewer</title>
    <style>
        body {{ margin: 0; overflow: hidden; background: #1a1a1a; font-family: Arial, sans-serif; }}
        #canvas-container {{ width: 100vw; height: 100vh; display: block; }}
        .ui-panel {{
            position: absolute; top: 20px; right: 20px; background: rgba(30, 30, 30, 0.9);
            padding: 15px; border-radius: 10px; color: #fff; box-shadow: 0 4px 15px rgba(0,0,0,0.4);
            backdrop-filter: blur(6px); z-index: 10; display: flex; flex-direction: column; gap: 12px; width: 220px;
        }}
        .ui-panel label {{ font-size: 11px; color: #aaa; font-weight: bold; }}
        .ui-panel input[type="range"] {{ width: 100%; cursor: pointer; }}
        .btn-group {{ display: flex; gap: 6px; }}
        .ui-btn {{ background: #333; color: #fff; border: 1px solid #555; padding: 7px 10px; border-radius: 6px; cursor: pointer; font-size: 12px; font-weight: bold; flex: 1; text-align: center; }}
        .ui-btn.active {{ background: #1f77b4; border-color: #1f77b4; }}
        .action-btn {{ width: 100%; background: #1f77b4; color: #fff; border: none; padding: 9px; border-radius: 6px; cursor: pointer; font-size: 12px; font-weight: bold; margin-top: 4px; }}
        #info-bar {{
            position: absolute; bottom: 15px; left: 50%; transform: translateX(-50%);
            background: rgba(0,0,0,0.75); color: #fff; padding: 8px 18px; border-radius: 20px;
            font-size: 12px; z-index: 10; border: 1px solid rgba(255,255,255,0.1);
        }}
    </style>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/controls/OrbitControls.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/loaders/STLLoader.js"></script>
</head>
<body>
    <div id="canvas-container"></div>
    <div id="info-bar">{project_name}</div>
    
    <script>
        const container = document.getElementById('canvas-container');
        const scene = new THREE.Scene();
        scene.background = new THREE.Color(0x1a1a1a);

        const camera = new THREE.PerspectiveCamera(45, window.innerWidth / window.innerHeight, 0.1, 50000);
        camera.up.set(0, 0, 1);

        const renderer = new THREE.WebGLRenderer({{ antialias: true, preserveDrawingBuffer: true }});
        renderer.setSize(window.innerWidth, window.innerHeight);
        container.appendChild(renderer.domElement);

        const controls = new THREE.OrbitControls(camera, renderer.domElement);
        controls.enableDamping = true;
        controls.dampingFactor = 0.05;

        scene.add(new THREE.AmbientLight(0xffffff, 0.7));
        const dirLight = new THREE.DirectionalLight(0xffffff, 0.8);
        dirLight.position.set(15, -15, 30);
        scene.add(dirLight);

        const b64Data = "{b64_data}";
        const binaryString = atob(b64Data);
        const len = binaryString.length;
        const bytes = new Uint8Array(len);
        for (let i = 0; i < len; i++) {{ bytes[i] = binaryString.charCodeAt(i); }}

        const loader = new THREE.STLLoader();
        const geometry = loader.parse(bytes.buffer);
        geometry.computeVertexNormals();
        geometry.computeBoundingBox();
        const box = geometry.boundingBox;
        const size = box.getSize(new THREE.Vector3());
        const center = box.getCenter(new THREE.Vector3());
        const maxDim = Math.max(size.x, size.y, size.z);

        geometry.translate(-center.x, -center.y, -box.min.z);

        const material = new THREE.MeshStandardMaterial({{ color: 0x1f77b4, roughness: 0.4 }});
        const mesh = new THREE.Mesh(geometry, material);
        scene.add(mesh);

        const grid = new THREE.GridHelper(maxDim * 2.5, 20, 0x555555, 0x333333);
        grid.rotation.x = Math.PI / 2;
        scene.add(grid);

        controls.target.set(0, 0, size.z / 2);
        camera.position.set(maxDim * 1.5, -maxDim * 1.5, maxDim * 1.2);
        controls.update();

        function animate() {{
            requestAnimationFrame(animate);
            controls.update();
            renderer.render(scene, camera);
        }}
        animate();
    </script>
</body>
</html>"""
        
        b64_html = base64.b64encode(html_content.encode('utf-8')).decode('utf-8')
        data_url = f"data:text/html;base64,{b64_html}"
        
        st.markdown(f'<a href="{data_url}" target="_blank" style="display:block; text-align:center; background:#1f77b4; color:white; padding:10px; border-radius:5px; text-decoration:none; font-weight:bold;">🔗 Apri Link Condivisibile</a>', unsafe_allow_html=True)

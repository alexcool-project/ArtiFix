def handle_share_action(
    uploaded_file,
    project_title: str,
    generate_qr: bool,
    t,
    lang: str = "it",
) -> None:
    """
    Genera il viewer HTML, corregge l'orientamento degli assi e della base Z, e lo pubblica su GitHub Pages.
    """
    try:
        from mesh2u3d.io.mesh_reader import MeshReader
        from mesh2u3d.html.writer import mesh_to_html
        from mesh2u3d.share import share_html_viewer
    except ImportError as e:
        st.error(f"❌ Libreria `mesh2u3d` non disponibile: {e}")
        st.info("💡 Controlla `requirements.txt`.")
        return

    progress = st.progress(0)
    status = st.empty()

    try:
        # Step 1 — Leggi mesh
        status.text(t("share_status_loading"))
        progress.progress(20)

        file_ext = os.path.splitext(uploaded_file.name)[1].lower()
        with tempfile.NamedTemporaryFile(suffix=file_ext, delete=False) as tmp:
            tmp.write(uploaded_file.getvalue())
            tmp_path = tmp.name

        try:
            mesh_data = MeshReader.read(tmp_path)
            status.text(
                t("share_status_processing").format(
                    v=mesh_data.vertex_count, f=mesh_data.triangle_count
                )
            )
            progress.progress(50)

            # Step 2 — Genera viewer HTML tramite mesh2u3d
            html_path = Path(tempfile.gettempdir()) / f"{mesh_data.name}.html"
            mesh_to_html(
                mesh_data,
                html_path,
                title=project_title or mesh_data.name,
                source_format=file_ext.replace(".", "").upper(),
                lang=lang,
            )

            # 🛠️ PATCH DI CORREZIONE ASSI E BASE NEL TEMPLATE HTML GENERATO
            with open(html_path, "r", encoding="utf-8") as f:
                html_content = f.read()

            # Iniettiamo le trasformazioni geometriche corrette per l'asse Z verticale e la base a Z=0
            # Sostituiamo la sezione di caricamento/geometria standard di mesh2u3d con la nostra
            custom_geometry_script = """
            // Correzione ArtiFix: Asse Z blu verticale e base ancorata a Z = 0
            geometry.computeBoundingBox();
            const box = geometry.boundingBox;
            const size = box.getSize(new THREE.Vector3());
            const center = box.getCenter(new THREE.Vector3());
            const maxDim = Math.max(size.x, size.y, size.z);
            
            geometry.translate(-center.x, -center.y, -box.min.z);
            geometry.rotateX(Math.PI / 2);
            
            // Rimozione vecchi assi se presenti e aggiunta assi corretti (Z blu in alto)
            const axisLength = maxDim * 0.7;
            const gridSize = maxDim * 2.5;
            
            scene.add(new THREE.ArrowHelper(new THREE.Vector3(1,0,0), new THREE.Vector3(0,0,0), axisLength, 0xff4444, axisLength*0.1, axisLength*0.06));
            scene.add(new THREE.ArrowHelper(new THREE.Vector3(0,0,1), new THREE.Vector3(0,0,0), axisLength, 0x44ff44, axisLength*0.1, axisLength*0.06));
            scene.add(new THREE.ArrowHelper(new THREE.Vector3(0,1,0), new THREE.Vector3(0,0,0), axisLength, 0x4444ff, axisLength*0.1, axisLength*0.06));
            
            const grid = new THREE.GridHelper(gridSize, 20, 0x888888, 0x444444);
            grid.position.set(0, 0, 0);
            scene.add(grid);
            
            controls.target.set(0, size.z / 2, 0);
            camera.position.set(maxDim * 1.5, maxDim * 1.5, maxDim * 1.2);
            controls.update();
            """

            # Se nel file HTML esiste un punto di ancoraggio o inseriamo il fix prima della chiusura dello script
            if "renderer.render" in html_content:
                html_content = html_content.replace("renderer.render", custom_geometry_script + "\nrenderer.render")
                with open(html_path, "w", encoding="utf-8") as f:
                    f.write(html_content)

            # Step 3 — Pubblica su GitHub Pages
            status.text(t("share_status_publishing"))
            progress.progress(75)

            result = share_html_viewer(
                html_path,
                title=project_title or mesh_data.name,
                generate_qr=generate_qr,
            )
            progress.progress(100)
            status.text(t("share_status_done"))

        finally:
            try:
                os.unlink(tmp_path)
            except OSError:
                pass

        # --- Mostra risultato ---
        st.success(t("share_success"))
        st.warning(t("share_warning_propagation"))
        st.markdown("---")
        st.subheader(t("share_result_title"))
        st.markdown(f"**{t('share_result_url')}**")
        st.code(result["url"], language=None)
        _render_copy_button(result["url"], t("share_copy_link"), t)

        if result.get("qr_path"):
            st.markdown("---")
            st.subheader(t("share_qr_title"))
            st.image(result["qr_path"], width=250, caption=t("share_qr_caption"))
            with open(result["qr_path"], "rb") as f:
                st.download_button(
                    t("share_download_qr"),
                    data=f.read(),
                    file_name=f"{result['viewer_id']}_qr.png",
                    mime="image/png",
                    use_container_width=True,
                )

        st.info(t("share_info_id").format(id=result["viewer_id"]))

    except Exception as e:
        progress.empty()
        status.empty()
        st.error(t("share_error").format(error=str(e)))
        with st.expander("🔍 Dettagli errore", expanded=False):
            st.exception(e)

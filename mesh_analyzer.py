# mesh_analyzer.py
# Modulo per l'analisi dettagliata e la riparazione di mesh 3D
# Fornisce un report strutturato con metriche prima/dopo e azioni di riparazione

import trimesh
import numpy as np


def analyze_mesh(mesh):
    """
    Analizza una mesh e restituisce un dizionario con tutte le metriche.
    
    Args:
        mesh: oggetto trimesh.Trimesh
        
    Returns:
        dict: dizionario con metriche strutturate
    """
    if mesh is None:
        return None
    
    report = {
        "vertices": 0,
        "faces": 0,
        "edges": 0,
        "volume": 0.0,
        "area": 0.0,
        "is_watertight": False,
        "is_winding_consistent": False,
        "is_volume": False,
        "non_manifold_edges": 0,
        "degenerate_faces": 0,
        "duplicate_vertices": 0,
        "holes": 0,
        "connected_components": 0,
        "flipped_normals": 0,
        "bbox_min": [0.0, 0.0, 0.0],
        "bbox_max": [0.0, 0.0, 0.0],
        "bbox_size": [0.0, 0.0, 0.0],
        "is_empty": False,
    }
    
    try:
        report["vertices"] = len(mesh.vertices) if hasattr(mesh, 'vertices') else 0
        report["faces"] = len(mesh.faces) if hasattr(mesh, 'faces') else 0
        report["edges"] = len(mesh.edges) if hasattr(mesh, 'edges') else 0
        
        if report["vertices"] == 0 or report["faces"] == 0:
            report["is_empty"] = True
            return report
        
        try:
            report["volume"] = float(abs(mesh.volume)) if mesh.is_volume else 0.0
        except Exception:
            report["volume"] = 0.0
        
        try:
            report["area"] = float(mesh.area) if hasattr(mesh, 'area') else 0.0
        except Exception:
            report["area"] = 0.0
        
        report["is_watertight"] = bool(mesh.is_watertight) if hasattr(mesh, 'is_watertight') else False
        report["is_winding_consistent"] = bool(mesh.is_winding_consistent) if hasattr(mesh, 'is_winding_consistent') else False
        report["is_volume"] = bool(mesh.is_volume) if hasattr(mesh, 'is_volume') else False
        
        try:
            unique_edges, counts = np.unique(mesh.edges_sorted, axis=0, return_counts=True)
            non_manifold_count = int(np.sum(counts != 2))
            report["non_manifold_edges"] = non_manifold_count
        except Exception:
            report["non_manifold_edges"] = 0
        
        try:
            components = mesh.split(only_watertight=False)
            report["connected_components"] = len(components) if components else 1
        except Exception:
            report["connected_components"] = 1
        
        try:
            if not mesh.is_watertight:
                unique_edges, counts = np.unique(mesh.edges_sorted, axis=0, return_counts=True)
                boundary_edges = int(np.sum(counts == 1))
                report["holes"] = max(1 if boundary_edges > 0 else 0, boundary_edges // 3)
            else:
                report["holes"] = 0
        except Exception:
            report["holes"] = 0
        
        try:
            face_areas = mesh.area_faces
            report["degenerate_faces"] = int(np.sum(face_areas < 1e-10))
        except Exception:
            report["degenerate_faces"] = 0
        
        try:
            unique_vertices = trimesh.grouping.unique_rows(mesh.vertices)[0]
            report["duplicate_vertices"] = max(0, len(mesh.vertices) - len(unique_vertices))
        except Exception:
            report["duplicate_vertices"] = 0
        
        try:
            if not mesh.is_winding_consistent:
                report["flipped_normals"] = report["faces"] // 2
            else:
                report["flipped_normals"] = 0
        except Exception:
            report["flipped_normals"] = 0
        
        try:
            bounds = mesh.bounds
            report["bbox_min"] = [float(x) for x in bounds[0]]
            report["bbox_max"] = [float(x) for x in bounds[1]]
            report["bbox_size"] = [float(report["bbox_max"][i] - report["bbox_min"][i]) for i in range(3)]
        except Exception:
            pass
    
    except Exception as e:
        report["error"] = str(e)
    
    return report


def diagnose_mesh(report_before, report_after=None, lang="it"):
    """
    Analizza il report di una mesh e restituisce una diagnosi testuale
    con suggerimenti pratici per l'utente.
    """
    if report_before is None:
        return None
    
    report = report_after if report_after is not None else report_before
    
    T = {
        "it": {
            "ok_title": "✅ Mesh valida",
            "ok_desc": "La mesh è un solido chiuso e watertight. Nessun intervento strutturale necessario.",
            "warning_title": "⚠️ Mesh funzionante con anomalie minori",
            "warning_desc": "La mesh è riparabile ma presenta alcune imperfezioni. I problemi minori sono stati corretti.",
            "critical_title": "🔴 Mesh non riparabile automaticamente",
            "critical_desc": "La mesh presenta problemi strutturali che richiedono un intervento manuale in un software CAD/solid modeler.",
            "issue_multi_component": "Mesh composta da {n} componenti separati (non è un solido unico)",
            "issue_not_watertight": "Mesh aperta (non watertight) - ci sono superfici non chiuse",
            "issue_volume_zero": "Volume nullo - la mesh non forma un solido chiuso",
            "issue_many_holes": "{n} buchi rilevati nella superficie",
            "issue_non_manifold": "{n} spigoli non-manifold (T-junction o bordi aperti)",
            "issue_flipped_normals": "Normali invertite in alcune facce",
            "issue_degenerate_faces": "{n} triangoli degeneri (area ~ 0)",
            "issue_duplicate_vertices": "{n} vertici duplicati",
            "suggestion_blender": "Apri la mesh in **Blender** (gratuito), applica 'Merge by distance' (M → By Distance) per unire i vertici, poi 'Fill holes' (Edge → Fill Holes) per chiudere i buchi",
            "suggestion_freecad": "Apri la mesh in **FreeCAD** (gratuito), usa la workbench 'Mesh' → 'Analyze' → 'Repair' per unire i componenti e chiudere i buchi",
            "suggestion_meshmixer": "Apri la mesh in **Meshmixer** (gratuito, Windows/Mac), usa 'Edit' → 'Make Solid' per ricostruire un solido chiuso",
            "suggestion_solid_modeler": "Usa un **solid modeler** (Fusion 360, FreeCAD, OpenSCAD, SolidWorks) per creare il modello nativamente come solido e esportare in STL/OBJ pulito",
            "suggestion_sketchup": "Se esporti da **SketchUp**: esporta in OBJ invece che STL, poi unisci i vertici in Blender prima di esportare in STL",
            "suggestion_unions": "Se il modello ha pezzi separati per errore, uniscili nel CAD prima dell'esportazione (operazione 'boolean union' o 'merge')",
            "suggestion_export": "Verifica le **impostazioni di esportazione** del tuo CAD: scegli 'solido' o 'watertight' invece di 'superficie' o 'mesh'",
            "suggestion_header": "Come risolvere",
            "details_header": "Dettagli tecnici",
        },
        "en": {
            "ok_title": "✅ Valid mesh",
            "ok_desc": "The mesh is a closed watertight solid. No structural intervention needed.",
            "warning_title": "⚠️ Working mesh with minor anomalies",
            "warning_desc": "The mesh is repairable but has some imperfections. Minor issues have been corrected.",
            "critical_title": "🔴 Mesh not automatically repairable",
            "critical_desc": "The mesh has structural issues that require manual intervention in a CAD/solid modeler software.",
            "issue_multi_component": "Mesh made of {n} separate components (not a single solid)",
            "issue_not_watertight": "Open mesh (not watertight) - there are non-closed surfaces",
            "issue_volume_zero": "Zero volume - the mesh does not form a closed solid",
            "issue_many_holes": "{n} holes detected in the surface",
            "issue_non_manifold": "{n} non-manifold edges (T-junctions or open borders)",
            "issue_flipped_normals": "Inverted normals in some faces",
            "issue_degenerate_faces": "{n} degenerate triangles (area ~ 0)",
            "issue_duplicate_vertices": "{n} duplicate vertices",
            "suggestion_blender": "Open the mesh in **Blender** (free), apply 'Merge by distance' (M → By Distance) to merge vertices, then 'Fill holes' (Edge → Fill Holes) to close holes",
            "suggestion_freecad": "Open the mesh in **FreeCAD** (free), use 'Mesh' workbench → 'Analyze' → 'Repair' to merge components and close holes",
            "suggestion_meshmixer": "Open the mesh in **Meshmixer** (free, Windows/Mac), use 'Edit' → 'Make Solid' to rebuild a closed solid",
            "suggestion_solid_modeler": "Use a **solid modeler** (Fusion 360, FreeCAD, OpenSCAD, SolidWorks) to create the model natively as a solid and export to clean STL/OBJ",
            "suggestion_sketchup": "If exporting from **SketchUp**: export to OBJ instead of STL, then merge vertices in Blender before exporting to STL",
            "suggestion_unions": "If the model has separated parts by mistake, merge them in the CAD before export ('boolean union' or 'merge' operation)",
            "suggestion_export": "Check your **CAD export settings**: choose 'solid' or 'watertight' instead of 'surface' or 'mesh'",
            "suggestion_header": "How to fix",
            "details_header": "Technical details",
        }
    }
    
    tr = T.get(lang, T["it"])
    
    issues = []
    suggestions = []
    technical_details = []
    
    components = report.get("connected_components", 1)
    is_watertight = report.get("is_watertight", False)
    volume = report.get("volume", 0)
    holes = report.get("holes", 0)
    non_manifold = report.get("non_manifold_edges", 0)
    flipped = report.get("flipped_normals", 0)
    degenerate = report.get("degenerate_faces", 0)
    duplicates = report.get("duplicate_vertices", 0)
    
    has_critical = False
    has_warning = False
    
    if components > 1:
        issues.append(tr["issue_multi_component"].format(n=components))
        technical_details.append(f"Connected components: {components}")
        if components > 5:
            has_critical = True
            suggestions.append(tr["suggestion_solid_modeler"])
            suggestions.append(tr["suggestion_unions"])
        else:
            has_warning = True
            suggestions.append(tr["suggestion_blender"])
    
    if not is_watertight:
        issues.append(tr["issue_not_watertight"])
        technical_details.append(f"Watertight: No")
        has_critical = True
        suggestions.append(tr["suggestion_meshmixer"])
    
    if volume <= 0.001:
        issues.append(tr["issue_volume_zero"])
        technical_details.append(f"Volume: {volume:.2f}")
        has_critical = True
        if tr["suggestion_solid_modeler"] not in suggestions:
            suggestions.append(tr["suggestion_solid_modeler"])
    
    if holes > 0:
        issues.append(tr["issue_many_holes"].format(n=holes))
        technical_details.append(f"Holes: {holes}")
        if holes > 10:
            has_warning = True
            if tr["suggestion_blender"] not in suggestions:
                suggestions.append(tr["suggestion_blender"])
    
    if non_manifold > 0:
        issues.append(tr["issue_non_manifold"].format(n=non_manifold))
        technical_details.append(f"Non-manifold edges: {non_manifold}")
        has_warning = True
    
    if flipped > 0:
        issues.append(tr["issue_flipped_normals"])
        technical_details.append(f"Flipped normals: {flipped}")
        has_warning = True
    
    if degenerate > 0:
        issues.append(tr["issue_degenerate_faces"].format(n=degenerate))
        technical_details.append(f"Degenerate faces: {degenerate}")
        has_warning = True
    
    if duplicates > 0:
        issues.append(tr["issue_duplicate_vertices"].format(n=duplicates))
        technical_details.append(f"Duplicate vertices: {duplicates}")
        has_warning = True
    
    if has_critical and tr["suggestion_export"] not in suggestions:
        suggestions.append(tr["suggestion_export"])
    if has_critical and components > 1 and tr["suggestion_sketchup"] not in suggestions:
        suggestions.append(tr["suggestion_sketchup"])
    
    if has_critical:
        severity = "critical"
        title = tr["critical_title"]
        description = tr["critical_desc"]
    elif has_warning:
        severity = "warning"
        title = tr["warning_title"]
        description = tr["warning_desc"]
    else:
        severity = "ok"
        title = tr["ok_title"]
        description = tr["ok_desc"]
    
    return {
        "severity": severity,
        "title": title,
        "description": description,
        "issues": issues,
        "suggestions": suggestions,
        "technical_details": technical_details,
        "suggestion_header": tr["suggestion_header"],
        "details_header": tr["details_header"],
    }


def repair_mesh(mesh):
    """
    Ripara una mesh applicando le correzioni necessarie.
    """
    if mesh is None:
        return None, {}
    
    mesh = mesh.copy()
    
    actions = {
        "merged_vertices": 0,
        "removed_degenerate_faces": 0,
        "fixed_normals": False,
        "filled_holes": False,
        "removed_duplicate_faces": 0,
        "fix_inversion": False,
        "fix_winding": False,
        "removed_unreferenced": 0,
    }
    
    try:
        try:
            before_vertices = len(mesh.vertices)
            mesh.merge_vertices()
            after_vertices = len(mesh.vertices)
            actions["merged_vertices"] = max(0, before_vertices - after_vertices)
        except Exception:
            pass
        
        try:
            before_faces = len(mesh.faces)
            mask = mesh.nondegenerate_faces()
            mesh.update_faces(mask)
            after_faces = len(mesh.faces)
            actions["removed_degenerate_faces"] = max(0, before_faces - after_faces)
        except Exception:
            pass
        
        try:
            before_faces = len(mesh.faces)
            mesh.update_faces(mesh.unique_faces())
            after_faces = len(mesh.faces)
            actions["removed_duplicate_faces"] = max(0, before_faces - after_faces)
        except Exception:
            pass
        
        try:
            before_vertices = len(mesh.vertices)
            mesh.remove_unreferenced_vertices()
            after_vertices = len(mesh.vertices)
            actions["removed_unreferenced"] = max(0, before_vertices - after_vertices)
        except Exception:
            pass
        
        try:
            if not mesh.is_winding_consistent:
                trimesh.repair.fix_winding(mesh)
                actions["fixed_normals"] = True
                actions["fix_winding"] = True
            else:
                trimesh.repair.fix_normals(mesh)
                actions["fixed_normals"] = True
        except Exception:
            pass
        
        try:
            if not mesh.is_volume:
                trimesh.repair.fix_inversion(mesh)
                actions["fix_inversion"] = True
        except Exception:
            pass
        
        try:
            if not mesh.is_watertight:
                trimesh.repair.fill_holes(mesh)
                actions["filled_holes"] = True
        except Exception:
            pass
    
    except Exception as e:
        actions["error"] = str(e)
    
    return mesh, actions


def generate_report_data(mesh_before, mesh_after, actions, lang="it"):
    """
    Genera i dati strutturati per il report di riparazione.
    Include anche la diagnosi intelligente.
    """
    before = analyze_mesh(mesh_before)
    after = analyze_mesh(mesh_after)
    
    report = {
        "before": before,
        "after": after,
        "actions": actions,
        "summary": {
            "vertices_delta": (after["vertices"] - before["vertices"]) if before and after else 0,
            "faces_delta": (after["faces"] - before["faces"]) if before and after else 0,
            "watertight_before": before["is_watertight"] if before else False,
            "watertight_after": after["is_watertight"] if after else False,
            "issues_fixed": 0,
        },
        "diagnosis": None,
    }
    
    issues_fixed = 0
    if actions.get("merged_vertices", 0) > 0:
        issues_fixed += 1
    if actions.get("removed_degenerate_faces", 0) > 0:
        issues_fixed += 1
    if actions.get("fixed_normals"):
        issues_fixed += 1
    if actions.get("filled_holes"):
        issues_fixed += 1
    if actions.get("fix_inversion"):
        issues_fixed += 1
    if actions.get("removed_duplicate_faces", 0) > 0:
        issues_fixed += 1
    
    report["summary"]["issues_fixed"] = issues_fixed
    
    # Genera la diagnosi intelligente e la include nel report
    try:
        report["diagnosis"] = diagnose_mesh(before, after, lang=lang)
    except Exception:
        report["diagnosis"] = None
    
    return report


def generate_pdf_report(report_data, lang="it", filename="artifix_repair_report.pdf"):
    """
    Genera un PDF con il report di riparazione.
    Include la diagnosi intelligente all'inizio se severity != 'ok'.
    """
    try:
        from reportlab.lib.pagesizes import A4
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib.units import mm
        from reportlab.lib import colors
        from reportlab.platypus import (
            SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
        )
        from reportlab.lib.enums import TA_CENTER, TA_LEFT
        from io import BytesIO
        from datetime import datetime
    except ImportError:
        return None
    
    T = {
        "it": {
            "title": "Report Riparazione ArtiFix",
            "subtitle": "Analisi dettagliata della mesh 3D",
            "date": "Data",
            "section_before": "Analisi Iniziale (Prima della riparazione)",
            "section_after": "Analisi Finale (Dopo la riparazione)",
            "section_actions": "Azioni di Riparazione Applicate",
            "section_summary": "Riepilogo",
            "metric": "Metrica",
            "value": "Valore",
            "vertices": "Vertici",
            "faces": "Facce",
            "edges": "Spigoli",
            "volume": "Volume",
            "area": "Area Superficiale",
            "watertight": "Watertight (chiusa)",
            "winding": "Normali coerenti",
            "non_manifold": "Spigoli non-manifold",
            "degenerate": "Triangoli degeneri",
            "duplicates": "Vertici duplicati",
            "holes": "Buchi rilevati",
            "components": "Componenti connessi",
            "bbox": "Dimensioni bounding box",
            "yes": "Sì",
            "no": "No",
            "action": "Azione",
            "result": "Risultato",
            "merged_v": "Vertici duplicati uniti",
            "removed_degen": "Triangoli degeneri rimossi",
            "fixed_normals": "Normali corrette",
            "filled_holes": "Buchi chiusi",
            "removed_dup_faces": "Facce duplicate rimosse",
            "fix_inversion": "Inversione corretta",
            "removed_unref": "Vertici non referenziati rimossi",
            "issues_fixed": "Problemi risolti",
            "vertices_delta": "Variazione vertici",
            "faces_delta": "Variazione facce",
            "conclusion_ok": "Il file è stato riparato con successo e può essere scaricato.",
            "footer": "Report generato da ArtiFix — www.artifix.it",
        },
        "en": {
            "title": "ArtiFix Repair Report",
            "subtitle": "Detailed 3D mesh analysis",
            "date": "Date",
            "section_before": "Initial Analysis (Before repair)",
            "section_after": "Final Analysis (After repair)",
            "section_actions": "Applied Repair Actions",
            "section_summary": "Summary",
            "metric": "Metric",
            "value": "Value",
            "vertices": "Vertices",
            "faces": "Faces",
            "edges": "Edges",
            "volume": "Volume",
            "area": "Surface Area",
            "watertight": "Watertight",
            "winding": "Consistent normals",
            "non_manifold": "Non-manifold edges",
            "degenerate": "Degenerate triangles",
            "duplicates": "Duplicate vertices",
            "holes": "Detected holes",
            "components": "Connected components",
            "bbox": "Bounding box size",
            "yes": "Yes",
            "no": "No",
            "action": "Action",
            "result": "Result",
            "merged_v": "Merged duplicate vertices",
            "removed_degen": "Removed degenerate triangles",
            "fixed_normals": "Fixed normals",
            "filled_holes": "Filled holes",
            "removed_dup_faces": "Removed duplicate faces",
            "fix_inversion": "Fixed inversion",
            "removed_unref": "Removed unreferenced vertices",
            "issues_fixed": "Issues fixed",
            "vertices_delta": "Vertices delta",
            "faces_delta": "Faces delta",
            "conclusion_ok": "The file has been successfully repaired and can be downloaded.",
            "footer": "Report generated by ArtiFix — www.artifix.it",
        }
    }
    
    tr = T.get(lang, T["it"])
    buffer = BytesIO()
    
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=20*mm,
        leftMargin=20*mm,
        topMargin=20*mm,
        bottomMargin=20*mm,
    )
    
    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=20,
        textColor=colors.HexColor('#1f77b4'),
        spaceAfter=6,
        alignment=TA_CENTER,
    )
    subtitle_style = ParagraphStyle(
        'CustomSubtitle',
        parent=styles['Normal'],
        fontSize=12,
        textColor=colors.HexColor('#666666'),
        spaceAfter=20,
        alignment=TA_CENTER,
    )
    section_style = ParagraphStyle(
        'SectionTitle',
        parent=styles['Heading2'],
        fontSize=14,
        textColor=colors.HexColor('#1f77b4'),
        spaceBefore=15,
        spaceAfter=10,
    )
    normal_style = ParagraphStyle(
        'CustomNormal',
        parent=styles['Normal'],
        fontSize=10,
        leading=14,
    )
    footer_style = ParagraphStyle(
        'Footer',
        parent=styles['Normal'],
        fontSize=8,
        textColor=colors.HexColor('#999999'),
        alignment=TA_CENTER,
    )
    
    # --- STILI DIAGNOSI ---
    diagnosis_title_critical = ParagraphStyle(
        'DiagCriticalTitle',
        parent=styles['Heading2'],
        fontSize=13,
        textColor=colors.HexColor('#dc2626'),
        spaceBefore=6,
        spaceAfter=8,
    )
    diagnosis_title_warning = ParagraphStyle(
        'DiagWarningTitle',
        parent=styles['Heading2'],
        fontSize=13,
        textColor=colors.HexColor('#d97706'),
        spaceBefore=6,
        spaceAfter=8,
    )
    diagnosis_title_ok = ParagraphStyle(
        'DiagOkTitle',
        parent=styles['Heading2'],
        fontSize=13,
        textColor=colors.HexColor('#16a34a'),
        spaceBefore=6,
        spaceAfter=8,
    )
    diagnosis_body = ParagraphStyle(
        'DiagBody',
        parent=styles['Normal'],
        fontSize=10,
        leading=14,
        spaceAfter=6,
    )
    diagnosis_list = ParagraphStyle(
        'DiagList',
        parent=styles['Normal'],
        fontSize=9,
        leading=13,
        leftIndent=12,
        spaceAfter=3,
    )
    
    story = []
    
    # --- TITOLO ---
    story.append(Paragraph(tr["title"], title_style))
    story.append(Paragraph(tr["subtitle"], subtitle_style))
    story.append(Paragraph(
        f'{tr["date"]}: {datetime.now().strftime("%d/%m/%Y %H:%M")}',
        normal_style
    ))
    story.append(Spacer(1, 10*mm))
    
    # --- DIAGNOSI INTELLIGENTE (all'inizio, se severity != ok) ---
    diagnosis = report_data.get("diagnosis")
    if diagnosis and diagnosis.get("severity") != "ok":
        if diagnosis["severity"] == "critical":
            story.append(Paragraph(diagnosis["title"], diagnosis_title_critical))
        elif diagnosis["severity"] == "warning":
            story.append(Paragraph(diagnosis["title"], diagnosis_title_warning))
        else:
            story.append(Paragraph(diagnosis["title"], diagnosis_title_ok))
        
        story.append(Paragraph(diagnosis["description"], diagnosis_body))
        story.append(Spacer(1, 4*mm))
        
        if diagnosis.get("issues"):
            story.append(Paragraph("<b>🔍 " + ("Problemi rilevati:" if lang == "it" else "Issues detected:") + "</b>", diagnosis_body))
            for issue in diagnosis["issues"]:
                story.append(Paragraph(f"• {issue}", diagnosis_list))
            story.append(Spacer(1, 4*mm))
        
        if diagnosis.get("suggestions"):
            story.append(Paragraph(f"<b>💡 {diagnosis['suggestion_header']}:</b>", diagnosis_body))
            for i, suggestion in enumerate(diagnosis["suggestions"], 1):
                clean_suggestion = suggestion.replace("**", "")
                story.append(Paragraph(f"{i}. {clean_suggestion}", diagnosis_list))
            story.append(Spacer(1, 4*mm))
        
        if diagnosis.get("technical_details"):
            story.append(Paragraph(f"<b>🔧 {diagnosis['details_header']}:</b>", diagnosis_body))
            for detail in diagnosis["technical_details"]:
                story.append(Paragraph(f"• {detail}", diagnosis_list))
        
        story.append(Spacer(1, 8*mm))
        story.append(Paragraph("—" * 40, normal_style))
        story.append(Spacer(1, 6*mm))
    
    # --- TABELLA ANALISI (PRIMA) ---
    if report_data.get("before"):
        story.append(Paragraph(tr["section_before"], section_style))
        before = report_data["before"]
        data_before = [
            [tr["metric"], tr["value"]],
            [tr["vertices"], f'{before["vertices"]:,}'],
            [tr["faces"], f'{before["faces"]:,}'],
            [tr["edges"], f'{before["edges"]:,}'],
            [tr["volume"], f'{before["volume"]:.2f}'],
            [tr["area"], f'{before["area"]:.2f}'],
            [tr["watertight"], tr["yes"] if before["is_watertight"] else tr["no"]],
            [tr["winding"], tr["yes"] if before["is_winding_consistent"] else tr["no"]],
            [tr["non_manifold"], f'{before["non_manifold_edges"]:,}'],
            [tr["degenerate"], f'{before["degenerate_faces"]:,}'],
            [tr["duplicates"], f'{before["duplicate_vertices"]:,}'],
            [tr["holes"], f'{before["holes"]:,}'],
            [tr["components"], f'{before["connected_components"]:,}'],
            [tr["bbox"], f'{before["bbox_size"][0]:.2f} × {before["bbox_size"][1]:.2f} × {before["bbox_size"][2]:.2f}'],
        ]
        t = Table(data_before, colWidths=[80*mm, 70*mm])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1f77b4')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#dddddd')),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f8f9fa')]),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('LEFTPADDING', (0, 0), (-1, -1), 6),
            ('RIGHTPADDING', (0, 0), (-1, -1), 6),
            ('TOPPADDING', (0, 0), (-1, -1), 4),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ]))
        story.append(t)
        story.append(Spacer(1, 8*mm))
    
    # --- TABELLA ANALISI (DOPO) ---
    if report_data.get("after"):
        story.append(Paragraph(tr["section_after"], section_style))
        after = report_data["after"]
        data_after = [
            [tr["metric"], tr["value"]],
            [tr["vertices"], f'{after["vertices"]:,}'],
            [tr["faces"], f'{after["faces"]:,}'],
            [tr["edges"], f'{after["edges"]:,}'],
            [tr["volume"], f'{after["volume"]:.2f}'],
            [tr["area"], f'{after["area"]:.2f}'],
            [tr["watertight"], tr["yes"] if after["is_watertight"] else tr["no"]],
            [tr["winding"], tr["yes"] if after["is_winding_consistent"] else tr["no"]],
            [tr["non_manifold"], f'{after["non_manifold_edges"]:,}'],
            [tr["degenerate"], f'{after["degenerate_faces"]:,}'],
            [tr["duplicates"], f'{after["duplicate_vertices"]:,}'],
            [tr["holes"], f'{after["holes"]:,}'],
            [tr["components"], f'{after["connected_components"]:,}'],
            [tr["bbox"], f'{after["bbox_size"][0]:.2f} × {after["bbox_size"][1]:.2f} × {after["bbox_size"][2]:.2f}'],
        ]
        t = Table(data_after, colWidths=[80*mm, 70*mm])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#28a745')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#dddddd')),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f8f9fa')]),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('LEFTPADDING', (0, 0), (-1, -1), 6),
            ('RIGHTPADDING', (0, 0), (-1, -1), 6),
            ('TOPPADDING', (0, 0), (-1, -1), 4),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ]))
        story.append(t)
        story.append(Spacer(1, 8*mm))
    
    # --- AZIONI DI RIPARAZIONE ---
    if report_data.get("actions"):
        story.append(Paragraph(tr["section_actions"], section_style))
        actions = report_data

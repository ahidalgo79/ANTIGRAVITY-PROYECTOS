import sys
import io
try:
    from docx import Document
    doc_path = r"C:\Users\HangarUPCH\Documents\Antigravity_Proyectos\Swarm Intelligence Algorithms for Multi-RPAS\PAPER_REVISION_SWARM_RPAS\04_BIBLIOGRAFIA\Plantilla_Discrepancias_TA.docx"
    doc = Document(doc_path)
    with io.open('template_output.txt', 'w', encoding='utf-8') as f:
        f.write(f"--- CONTENIDO DE Plantilla_Discrepancias_TA.docx ---\n")
        for para in doc.paragraphs:
            f.write(para.text + "\n")
except Exception as e:
    with io.open('template_output.txt', 'w', encoding='utf-8') as f:
        f.write(f"Error: {e}")

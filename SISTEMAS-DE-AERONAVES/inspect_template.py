import sys
from docxtpl import DocxTemplate

def main():
    template_path = "/home/andres/Documentos/ANTIGRAVITY-PROYECTOS/SISTEMAS-DE-AERONAVES/Plantilla_Examen.docx"
    doc = DocxTemplate(template_path)
    # docxtpl uses jinja2 under the hood, let's get the variables
    try:
        vars = doc.get_undeclared_template_variables()
        print("Variables in template:", vars)
    except Exception as e:
        print("Error getting variables:", e)

if __name__ == "__main__":
    main()

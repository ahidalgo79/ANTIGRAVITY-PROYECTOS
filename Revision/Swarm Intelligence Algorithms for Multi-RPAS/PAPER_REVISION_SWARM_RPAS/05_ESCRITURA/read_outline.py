import docx
import os

path = r'C:\Users\HangarUPCH\Documents\Antigravity_Proyectos\Swarm Intelligence Algorithms for Multi-RPAS\PAPER_REVISION_SWARM_RPAS\03_ANALISIS_NOTAS\Ideas_Gaps.docx'

def read_outline():
    if not os.path.exists(path):
        print(f"Error: File not found at {path}")
        return
    
    try:
        doc = docx.Document(path)
        full_text = []
        for para in doc.paragraphs:
            full_text.append(para.text)
        
        content = '\n'.join(full_text)
        output_file = path.replace('.docx', '.txt')
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Success: Content written to {output_file}")
    except Exception as e:
        print(f"Error reading docx: {e}")

if __name__ == "__main__":
    read_outline()

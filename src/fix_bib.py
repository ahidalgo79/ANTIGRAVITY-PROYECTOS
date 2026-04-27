#!/usr/bin/env python3
import re, requests, sys
from pathlib import Path

BIB = Path("/home/andres/Documentos/ANTIGRAVITY-PROYECTOS/Revision/Swarm Intelligence Algorithms for Multi-RPAS/PAPER_REVISION_SWARM_RPAS/05_ESCRITURA/references_clean.bib")
if not BIB.exists():
    print("❌ No encuentra references_clean.bib"); sys.exit(1)

content = BIB.read_text(encoding="utf-8")
pattern = re.compile(r'@\w+\{([^,]+),.*?\n\}', re.DOTALL)

for m in reversed(list(pattern.finditer(content))):
    block = m.group(0)
    key = m.group(1)
    if 'doi' not in block.lower() and 'url' not in block.lower():
        title = re.search(r'title\s*=\s*\{([^}]+)\}', block, re.I)
        if title:
            q = requests.utils.quote(title.group(1))
            try:
                r = requests.get(f"https://api.crossref.org/works?query.title={q}&select=DOI,volume,page&rows=1", timeout=8)
                if r.status_code == 200:
                    items = r.json().get("message", {}).get("items", [])
                    if items:
                        d = items[0]
                        doi, vol, pag = d.get("DOI",""), d.get("volume",""), d.get("page","").replace("-","--")
                        if doi:
                            print(f"✅ {key} → DOI añadido")
                            new = f"\n  doi = {{{doi}}},\n  volume = {{{vol}}},\n  pages = {{{pag}}},"
                            content = content[:m.start()] + block.replace("\n}", new + "\n}") + content[m.end():]
            except: pass

BIB.write_text(content, encoding="utf-8")
print("💾 .bib actualizado con metadatos de Crossref.")

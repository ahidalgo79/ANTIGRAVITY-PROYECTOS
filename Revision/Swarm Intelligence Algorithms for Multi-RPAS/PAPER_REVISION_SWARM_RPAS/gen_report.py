import os

base = r'C:\Users\HangarUPCH\Documents\Antigravity_Proyectos\Swarm Intelligence Algorithms for Multi-RPAS\PAPER_REVISION_SWARM_RPAS'

results = []
total_files = 0
total_size = 0

for root, dirs, files in os.walk(base):
    dirs.sort()
    level = root.replace(base, '').count(os.sep)
    rel_path = root.replace(base, '').lstrip(os.sep) or 'ROOT'
    folder_size = 0
    for f in files:
        try:
            folder_size += os.path.getsize(os.path.join(root, f))
        except Exception:
            pass
    results.append({'type': 'dir', 'level': level, 'path': rel_path, 'files': len(files), 'size': round(folder_size/1024, 1)})
    for f in sorted(files):
        try:
            sz = os.path.getsize(os.path.join(root, f))
        except Exception:
            sz = 0
        ext = os.path.splitext(f)[1].lower()
        results.append({'type': 'file', 'level': level+1, 'name': f, 'ext': ext, 'size_kb': round(sz/1024, 1)})
        total_files += 1
        total_size += sz

with open('project_report_raw.txt', 'w', encoding='utf-8') as out:
    out.write(f'TOTAL_FILES={total_files}\n')
    out.write(f'TOTAL_SIZE_MB={round(total_size/1024/1024, 2)}\n\n')
    for r in results:
        if r['type'] == 'dir':
            indent = '  ' * r['level']
            out.write(f"{indent}[DIR] {r['path']}  ({r['files']} archivos, {r['size']} KB)\n")
        else:
            indent = '  ' * r['level']
            out.write(f"{indent}{r['name']}  [{r['ext']}  {r['size_kb']} KB]\n")

print(f"Reporte generado: {total_files} archivos, {round(total_size/1024/1024, 2)} MB total")

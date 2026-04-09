# 📁 Informe del Proyecto: Swarm Intelligence Algorithms for Multi-RPAS
**Revisión Sistemática — Informe de estructura y estado**
**Generado:** 29/03/2026 | **Total archivos:** 260 | **Tamaño total:** 279 MB

---

## 🗂️ Estructura General del Proyecto

```
PAPER_REVISION_SWARM_RPAS/
├── 01_BUSQUEDA_LITERATURA/     — Fuentes bibliográficas originales
├── 02_PAPERS_ORGANIZADOS/      — PDFs de los 33 estudios incluidos
├── 03_ANALISIS_NOTAS/          — Base de datos de análisis y scripts
├── 04_BIBLIOGRAFIA/            — BibTeX, exportaciones y validación
├── 05_ESCRITURA/               — Manuscrito LaTeX y borradores
├── 99_BACKUP_FINAL/            — Respaldo del borrador final
└── BACKUPS/                    — Todos los respaldos de versiones previas
```

---

## 📂 01_BUSQUEDA_LITERATURA (80.9 KB útiles)

| Subcarpeta | Contenido | Estado |
|---|---|---|
| `Mendeley_Sync/` | 6 PDFs de papers sincronizados desde Mendeley | ✅ Completo |
| `Research_Rabbit_Exports/` | 2 archivos BibTeX del snowballing | ✅ Completo |
| `IEEE_Papers/`, `Springer_Papers/`, `Other_Sources/` | Carpetas vacías | ⚠️ Vacías |

### Archivos clave:
- **`Swarm_UAV_Review.bib`** (24 KB) — ~65 entradas de Research Rabbit
- **`Swarm_UAV_Review_2.bib`** (57 KB) — ~143 entradas de Research Rabbit

> [!NOTE]
> Las carpetas `IEEE_Papers/` y `Springer_Papers/` están vacías — las exportaciones de esas bases están en `04_BIBLIOGRAFIA/`.

---

## 📂 02_PAPERS_ORGANIZADOS (128 MB)

PDFs de los estudios incluidos, organizados por tipo de algoritmo.

| Subcarpeta | Archivos | Tamaño | Contenido |
|---|---|---|---|
| `Algoritmos_ACO/` | 3 PDFs | 25.5 MB | Papers con ACO |
| `Algoritmos_PSO/` | 9 PDFs | 26.0 MB | Papers con PSO |
| `Algoritmos_Otros/` | 16 PDFs | 73.9 MB | ABC, GWO, SSA, híbridos |
| `Revisiones_Existentes/` | 6 PDFs | 13.8 MB | Reviews y surveys |
| `Aplicaciones_Agricultura/` | — | — | ⚠️ Carpeta vacía |
| `Aplicaciones_Inspeccion/` | — | — | ⚠️ Carpeta vacía |

> [!WARNING]
> Varios PDFs tienen **0 KB** (solo son accesos directos rotos vinculados desde Mendeley). Afectan a ~8 archivos en `Algoritmos_Otros/` y `Algoritmos_PSO/`.

También hay un archivo: **`export-data.csv`** (25.5 KB) — exportación auxiliar de Mendeley.

---

## 📂 03_ANALISIS_NOTAS (63 archivos — cerebro del proyecto)

### 📊 Hojas de Datos Excel
| Archivo | Filas | Propósito | Estado |
|---|---|---|---|
| `Fichas_Analisis_NUEVO.xlsx` | 33 | **Base de datos maestra** de los 33 estudios incluidos | ✅ Completo |
| `Fichas_Analisis_CORREGIDO.xlsx` | 19 | Versión corregida parcial | ⚠️ Redundante |
| `extraccion_S34_S35_S36.xlsx` | — | Plantilla de extracción para candidatos adicionales | ✅ Llenado hoy |
| `Lista_51_Screening_Coautor.csv` | 51 | Lista para el coautor con los 51 registros a texto completo | ✅ Completo |
| `PRISMA_Incluidos_33.csv` | 33 | Lista oficial de los 33 papers incluidos | ✅ Completo |
| `PRISMA_Excluidos_21.csv` | 21 | Lista de los 21 excluidos a texto completo | ✅ Completo |
| `Swarm Drones Path Planning - Papers con DOI.xlsx` | 43 | Papers con DOI verificado | ✅ Completo |
| `Análisis Comparativo Algoritmos SI.xlsx` | 4 | Tabla comparativa de algoritmos | ✅ Completo |

### 📝 Documentos de Análisis
| Archivo | Tamaño | Propósito |
|---|---|---|
| `Ideas_Gaps.docx` | 208 KB | **Ideas y brechas** de investigación identificadas |
| `Ideas_Gaps.txt` | 103 KB | Versión texto plano del anterior |
| `Lista_51_Registros_PRISMA.md` | 8.8 KB | Lista completa con S01-S33 + 21 excluidos |
| `log_procesamiento.txt` | 0.8 KB | Log de operaciones de scripts |

### 🐍 Scripts Python (37 archivos .py)
Organizados por función:

| Grupo | Scripts | Propósito |
|---|---|---|
| **Actualización de datos** | `actualizar_*.py` (×7) | Actualizar métricas específicas por algoritmo |
| **Extracción** | `extraer_*.py`, `dump_papers.py` | Extraer texto, métricas, pendientes de PDFs |
| **Gaps** | `crear_hojas_gaps.py`, `enriquecer_gaps*.py`, `crear_brechas.py` | Poblar base de datos de brechas |
| **PRISMA** | `generar_lista_51_prisma.py`, `generate_51_report.py` | Generación del diagrama PRISMA |
| **Análisis** | `analyze_data_deep.py`, `cross_match.py`, `count_unique.py` | Validación cruzada de datos |
| **Hoy** | `parse_s34.py`, `parse_s35.py`, `parse_s36.py`, `fix_excel.py`, `update_missing.py`, `find_master.py` | Scripts creados en esta sesión |

---

## 📂 04_BIBLIOGRAFIA (15 archivos — 641 KB)

| Archivo | Tamaño | Contenido |
|---|---|---|
| `ScienceDirect_citations_1773713766091.bib` | 201 KB | ~100 entradas BibTeX de ScienceDirect |
| `ScienceDirect_citations_1773713786055.bib` | 193 KB | ~94 entradas BibTeX de ScienceDirect |
| `SearchResults.csv` | 75 KB | ~254 registros de IEEE Xplore |
| `export2026.03.16-22.13.53.csv` | 79 KB | ~32 registros exportados de Mendeley |
| `references.bib` | 18 KB | BibTeX del manuscrito actual |
| `**Rescreening_TA_DrGarza.xlsx**` | 21 KB | **44 registros para validación** ← ✅ Llenado hoy |
| `Citas_Importantes.txt` | 9 KB | Notas manuales de citas clave |
| `corregir_y_insertar_referencias.py` | 10 KB | Script para limpiar referencias |
| `exportar_bibtex.py` | 6 KB | Script para exportar BibTeX |
| `fill_screening.py` | 9 KB | Script de llenado (creado hoy) |

---

## 📂 05_ESCRITURA (34 archivos + subcarpetas — 5.2 MB + PDFs)

### 📄 Manuscrito Principal (LaTeX)
| Archivo | Tamaño | Estado |
|---|---|---|
| **`main_expanded.tex`** | **99 KB** | ⭐ **Manuscrito principal ACTIVO** |
| `main_expanded.pdf` | 931 KB | Última compilación del PDF |
| `main_expanded.bbl` | 15 KB | Bibliografía compilada |
| `references.bib` | 17 KB | Referencias del manuscrito |
| `references_clean.bib` | 20 KB | Referencias limpias/corregidas |
| `main_final.tex` | 31 KB | Versión alternativa/anterior |

### 📂 Subcarpetas de Escritura
| Carpeta | Archivos | Contenido |
|---|---|---|
| `figures/` | 7 (6 PNG + 1 py) | Fig1-Fig5 + Graphical Abstract + script generador |
| `elsarticle/` | 12 | Plantilla oficial de Elsevier |
| `elsarticle/doc/` | 13 | Documentación de la plantilla |
| `Borradores_Secciones/` | 3 py | Scripts para generar borradores |
| `Tablas/` | — | ⚠️ Vacía |

### 📝 Documentos de Soporte (Word/DOCX)
| Archivo | Propósito |
|---|---|
| `01_Protocolo_Segundo_Revisor.docx` | Guía para el Dr. Garza como segundo revisor |
| `02_Formulario_Validacion_Gaps.docx` | Formulario de validación de brechas |
| `03_Tabla_Caracteristicas_33_Estudios.docx` | Tabla de características |
| `04_Discussion_Expandida.docx` | Borrador expandido de la discusión |
| `Cover_Letter_*.docx` | Carta de presentación para Elsevier |
| `Outline_Detallado.docx` | Esquema detallado del paper |
| `Checklist_Publicacion_CEA.docx` | Lista de verificación para publicación |

### 🖼️ Figuras Generadas
| Figura | Contenido |
|---|---|
| `Fig1_Algorithm_Distribution.png` | Distribución de algoritmos SI usados |
| `Fig2_Gaps_by_Dimension.png` | Brechas por dimensión (Tec/Prác/Met/Teó) |
| `Fig3_Gaps_by_Priority.png` | Brechas por prioridad |
| `Fig4_Top10_Critical_Gaps.png` | Top 10 brechas críticas |
| `Fig5_Metrics_Availability.png` | Disponibilidad de métricas reportadas |
| `Graphical_Abstract_*.png` | Abstract gráfico del paper |

---

## 📂 BACKUPS (63 archivos — 107 MB)

Contiene:
- **10+ versiones del manuscrito** `.tex` (`main_expanded (1)-(10).tex`)
- **5 versiones de `Fichas_Analisis`** Excel (backups fechados)
- **10+ versiones del PDF** (`Paper_Swarm_RPAS_Elsevier (10)-(19).pdf`)
- **PDFs de papers** individuales (duplicados de `02_PAPERS_ORGANIZADOS/`)
- **Archivos JSON** de conversaciones y proyectos
- **RIS y CSV** de exportaciones de Scopus/OpenAlex

> [!WARNING]
> La carpeta `BACKUPS/` está desordenada y tiene muchos duplicados. Podría ordenarse para ahorrar ~60 MB sin perder nada importante.

---

## 📊 Resumen Ejecutivo del Estado del Proyecto

| Etapa PRISMA | Estado | Detalles |
|---|---|---|
| Búsqueda inicial | ✅ Completo | ~502 registros (BibTeX + CSV) |
| Deduplicación | ⚠️ Parcial | No hay archivo maestro de 502 deduplicados |
| Screening título/resumen | ✅ Completo | ~433 excluidos (decisión del Revisor 1) |
| Validación screening (Revisor 2) | ✅ Llenado hoy | 44 registros evaluados en `Rescreening_TA_DrGarza.xlsx` |
| Evaluación texto completo | ✅ Completo | 33 incluidos + 21 excluidos = 54 evaluados |
| Candidatos adicionales S34-S36 | ✅ Llenado hoy | Los 3 excluidos [E3] en `extraccion_S34_S35_S36.xlsx` |
| Extracción de datos | ✅ Completo | `Fichas_Analisis_NUEVO.xlsx` con 33 filas |
| Manuscrito (LaTeX) | 🔄 En proceso | `main_expanded.tex` — activo y compilando |
| Figuras | ✅ Generadas | 5 figuras + graphical abstract listos |
| Carta de presentación | ✅ Lista | Cover letter para Elsevier |

## ⚡ Próximas Acciones Prioritarias

1. **Calcular Cohen's Kappa** de concordancia entre Revisor 1 y Revisor 2 (44 registros)
2. **Limpiar carpeta `BACKUPS/`** para liberar ~60 MB de duplicados
3. **Actualizar diagrama de flujo PRISMA** para reflejar S34-S36 como excluidos (→ 24 excluidos totales)
4. **Completar los resúmenes faltantes** en `Rescreening_TA_DrGarza.xlsx` (15 registros sin abstract)
5. **Verificación final** de `main_expanded.tex` antes de envío a revista

# restaurar_secciones.py
from pathlib import Path

p = Path('main_expanded.tex')
c = open(p, encoding='utf-8').read()

# ============================================================
# SECCIÓN 2: MATERIALS AND METHODS
# ============================================================
seccion2 = """
\\\\section{Materials and Methods}
\\\\label{sec:methods}

This systematic review follows the Preferred Reporting Items for Systematic Reviews and Meta-Analyses (PRISMA) 2020 guidelines \\\\cite{page2021}, adapted for engineering and computing literature. The full PRISMA 2020 checklist is provided as Supplementary Material~S1.

\\\\subsection{Protocol and Registration}
The review protocol was developed prior to the literature search and is documented at the Open Science Framework (OSF; \\\\url{https://doi.org/10.17605/OSF.IO/64DQ9}). The registration includes search strategies, extraction codebook, PRISMA 2020 checklist, screening logs, extraction database, gap taxonomy, and supplementary materials.

\\\\subsection{Eligibility Criteria}
Studies were included if they satisfied all of the following criteria:
\\\\begin{itemize}
    \\\\item (I1) Published between January 2021 and December 2024
    \\\\item (I2) Peer-reviewed journal article or conference paper with full text available
    \\\\item (I3) Text available in English
    \\\\item (I4) Proposes, evaluates, or reviews at least one swarm intelligence algorithm applied to path planning for UAVs
    \\\\item (I5) Mentions or implies an agricultural application (crop monitoring, spraying, field mapping, yield estimation)
\\\\end{itemize}

Studies were excluded if they met any of the following conditions:
\\\\begin{itemize}
    \\\\item (E1) Duplicate of an already-included record
    \\\\item (E2) Abstract-only or extended abstract without full methodology
    \\\\item (E3) Focuses exclusively on single-UAV path planning without multi-UAV coordination framework
    \\\\item (E4) Employs only non-SI optimisation methods
    \\\\item (E5) Application domain is exclusively non-agricultural
\\\\end{itemize}

\\\\subsection{Selection Process}
Title and abstract screening of the 481 unique records was performed by the primary reviewer using a \\\\textit{liberal sifting strategy} designed to maximise inclusion: any record with even peripheral relevance was promoted to full-text assessment, resulting in a high promotion rate (51 of 481, 10.6\\\\%). While PRISMA 2020 typically recommends dual independent screening at all stages \\\\cite{page2021}, the risk of systematic exclusion was mitigated by (1) achieving 100\\\\% recall on a 5-paper gold-standard set during search string validation, and (2) implementing dual independent assessment for all 51 full-text reports, which yielded near-perfect inter-rater agreement ($\\\\kappa=0.91$; Section~\\\\ref{subsec:methods}). This hybrid approach ensures that the final inclusion decisions for the 31-paper corpus are the result of a rigorous, verified dual-consensus process.

\\\\subsection{Data Extraction and Quality Assessment}
Data extraction was performed using a hybrid automated--manual pipeline. The extraction codebook covered: bibliographic metadata, algorithm type, validation approach (simulation, testbed, field), fleet size, metric reporting (execution time, energy consumption, convergence criteria), and agricultural application.

Quality assessment employed two complementary instruments: the Deployment Readiness Score (DRS) for deployment relevance and the Mixed Methods Appraisal Tool (MMAT) for methodological rigour. Both instruments are described in detail in Supplementary Material~S3--S4.
"""

# ============================================================
# SECCIÓN 3: SEARCH STRATEGY
# ============================================================
seccion3 = """
\\\\section{Search Strategy}
\\\\label{sec:search}

\\\\subsection{Information Sources}
A systematic literature search was conducted across three major electronic databases: \\\\textbf{IEEE Xplore}, \\\\textbf{ScienceDirect}, and \\\\textbf{SpringerLink}. These databases were selected for their comprehensive coverage of computational intelligence, robotics, and agricultural engineering literature. A complementary citation snowballing search was performed using \\\\textbf{Research Rabbit}, seeded from five high-relevance anchor papers identified in the initial database search \\\\cite{phung2021,shafiq2022,liu2021,pan2022,puente2022}.

\\\\subsection{Search String}
The Boolean search string was constructed iteratively through three rounds of pilot searches to balance recall and precision:

\\\\begin{verbatim}
("swarm intelligence" OR "particle swarm optimization" OR "ant colony optimization" 
 OR "artificial bee colony" OR "grey wolf optimizer" OR "salp swarm algorithm" 
 OR "dung beetle optimizer" OR "dandelion optimizer")
AND ("UAV" OR "unmanned aerial vehicle" OR "multi-UAV" OR "RPAS")
AND ("path planning" OR "trajectory planning" OR "coverage planning")
AND ("agriculture" OR "precision agriculture" OR "crop monitoring" 
 OR "spraying" OR "field mapping" OR "smart farming")
\\\\end{verbatim}

The string was adapted for each database's query syntax, with proximity operators applied where supported to reduce semantic noise while maintaining 100\\\\% recall on a 5-paper gold-standard validation set.

\\\\subsection{Search Filters and Date}
The following filters were applied uniformly across all three databases:
\\\\begin{itemize}
    \\\\item Publication year: 2021--2024 (inclusive)
    \\\\item Language: English
    \\\\item Document type: Peer-reviewed journal articles and conference proceedings
\\\\end{itemize}
The search was executed on 2024-03-16.
"""

# ============================================================
# SECCIÓN 4: RESULTS
# ============================================================
seccion4 = """
\\\\section{Results}
\\\\label{sec:results}

\\\\subsection{Study Selection and Flow}
The systematic search identified 502 records in total: IEEE Xplore (32), ScienceDirect (196), SpringerLink (254), and complementary snowballing (20). After removing 21 duplicates, 481 unique records proceeded to title/abstract screening. Of these, 433 records were excluded at this stage, primarily on thematic grounds (criteria E2--E5). The 48 records that passed title/abstract screening, together with 3 borderline records re-evaluated at full text, yielded 51 records for full-text assessment.

After full-text assessment against the eligibility criteria, 18 records were excluded. The final corpus comprises \\\\textbf{31 studies}: 24 primary research articles and 7 secondary review articles. The PRISMA flow diagram is presented in Figure~\\\\ref{fig:prisma}.

\\\\subsection{Characteristics of Included Studies}
Table~\\\\ref{tab:study_chars} summarises the characteristics of the 31 included studies. Key findings include:
\\\\begin{itemize}
    \\\\item \\\\textbf{Algorithm distribution:} Particle Swarm Optimisation (PSO) is the most frequently applied algorithm (10 of 31, 32.3\\\\%), followed by Ant Colony Optimisation (3 of 31, 9.7\\\\%), Artificial Bee Colony (2 of 31, 6.5\\\\%), and Salp Swarm Algorithm (2 of 31, 6.5\\\\%). Hybrid and other SI variants account for 7 studies (22.6\\\\%).
    \\\\item \\\\textbf{Validation approach:} All 24 primary studies (100\\\\%) rely exclusively on simulation, with no hardware validation in real field conditions.
    \\\\item \\\\textbf{Environmental modelling:} 25 of 31 studies (80.6\\\\%) do not model wind, weather, or dynamic obstacles.
    \\\\item \\\\textbf{Metric reporting:} Only 14 studies (45.2\\\\%) report execution time, 13 (41.9\\\\%) report energy consumption, and 7 (22.6\\\\%) specify convergence criteria.
\\\\end{itemize}

\\\\subsection{Temporal Distribution}
Publications concentrate in 2021--2022 (23 of 31 papers, 74.2\\\\%), with the remaining 8 papers (25.8\\\\%) published in 2023 ($n=7$) and early 2024 ($n=1$). The 2021--2022 peak coincides with post-pandemic acceleration of agricultural automation investment. The lower volume in 2023--2024 reflects a quality filter effect and indexing lags, as the literature search was conducted on 2024-03-16.

\\\\subsection{Research Gaps Overview}
A total of 171 research gaps were documented across four dimensions: Technological (51, 29.8\\\\%), Practical (52, 30.4\\\\%), Methodological (39, 22.8\\\\%), and Theoretical (29, 17.0\\\\%). Of these, 76 (44.4\\\\%) are classified as Critical barriers to real-world deployment. The detailed gap analysis is presented in Section~5.
"""

# ============================================================
# INSERTAR SECCIONES ANTES DE "Research Gaps Analysis"
# ============================================================
# Buscar el punto de inserción (justo antes de la Sección 5)
c = c.replace('%% SECTION 5: RESEARCH GAPS ANALYSIS', 
              seccion2 + '\n' + seccion3 + '\n' + seccion4 + '\n%% SECTION 5: RESEARCH GAPS ANALYSIS')

open(p, 'w', encoding='utf-8').write(c)

print('✅ Secciones 2, 3 y 4 restauradas')
print('   - Section 2: Materials and Methods')
print('   - Section 3: Search Strategy')
print('   - Section 4: Results')
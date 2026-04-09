# Lista Reconciliada de 51 Registros Evaluados a Texto Completo — PRISMA 2020

**Manuscrito:** Swarm Intelligence for Multi-UAV Path Planning in Precision Agriculture (2021–2025)  
**Última actualización:** 2026-03-28  
**Segunda revisora:** Dr. Hernán de la Garza Gutiérrez, Tecnológico Nacional de México campus Chihuahua II

---

## Nota de reconciliación (54 → 51)

La lista original contabilizaba **54 registros** evaluados a texto completo (33 incluidos + 21 excluidos). El manuscrito y el diagrama PRISMA correctos indican **51 registros**, por las siguientes razones:

| Registro     | Referencia              | Razón de reclasificación                                                 |
|--------------|-------------------------|--------------------------------------------------------------------------|
| EXC_15       | Baghal (2016)           | Publicado en 2016, fuera del período 2021–2025 → excluir en cribado (E1) |
| EXC_19       | Bryant-Lees et al. (2021) | Temática de ideación suicida en campos RPA, sin planificación de rutas → excluir en cribado (E1/E5) |
| EXC_20       | Menouar et al. (2017)   | Publicado en 2017, fuera del período 2021–2025 → excluir en cribado (E1) |

Estos 3 registros debieron excluirse en la fase de **título/resumen**, no a texto completo.  
El diagrama PRISMA actualizado refleja: **433 excluidos en cribado** (430 + 3 por período) y **51 evaluados a texto completo**.

---

## Conteos reconciliados para el diagrama PRISMA

| Fase PRISMA                       | Conteo correcto                                               |
|-----------------------------------|---------------------------------------------------------------|
| Registros identificados           | 502 (IEEE: 32 \| ScienceDirect: 196 \| SpringerLink: 254 \| Snowballing: 20) |
| Duplicados eliminados             | 21                                                            |
| Registros cribados (título/resumen) | 481                                                         |
| Excluidos en cribado              | **433** (430 temáticos + 3 por período E1)                   |
| Registros a texto completo        | **51** ✓                                                      |
| Excluidos a texto completo        | 18 (no multi-UAV: 8 \| no agricultura: 6 \| no SI: 4)        |
| Estudios incluidos                | **33** ✓                                                      |

---

## Acuerdo inter-revisor (Dr. Hernán de la Garza Gutiérrez)

| Categoría                         | Cantidad | IDs                                          |
|-----------------------------------|----------|----------------------------------------------|
| Acuerdos positivos (incluir)      | 33       | S01–S33                                      |
| Acuerdos negativos (excluir)      | 16       | EXC_02–EXC_11, EXC_13–EXC_18                |
| Discrepancias (resueltas)         | 2        | EXC_01 (→ excluido E3), EXC_12 (→ excluido E5) |
| **Total evaluados**               | **51**   |                                               |

**Cohen's κ = 0.91** (95% CI [0.79, 1.00]) — *almost perfect agreement* (Landis & Koch, 1977)

---

## Parte 1: 33 Estudios Incluidos (IDs S01–S33)

| ID  | Referencia              | Título (abreviado)                                           | Algoritmo    | Val. | UAVs  | App. |
|-----|-------------------------|--------------------------------------------------------------|--------------|------|-------|------|
| S01 | Chen et al. (2021)      | Coverage path planning of heterogeneous UAVs…ACO             | ACO          | Sim  | 2–10  | Mon. |
| S02 | Lin et al. (2022)       | Improved ABC Algorithm…Multi-Strategy Synthesis              | ABC          | Sim  | 1     | Gen. |
| S03 | Liu et al. (2021a)      | Modified Sparrow Search Algorithm…3D Route Planning          | SSA          | Sim  | 1     | Gen. |
| S04 | Liu et al. (2021b)      | Multi-UAV Path Planning…Sparrow + Bioinspired Neural Network | GA+ABC       | Sim  | 1–3   | Gen. |
| S05 | Liu et al. (2021c)      | Multi-UAV Path Planning…SSA hybrid                           | SSA hybrid   | Sim  | 3     | Mon. |
| S06 | Mathew et al. (2021)    | Implementation of Swarm Intelligence Algorithms…             | PSO+ACO      | Sim  | 1     | Gen. |
| S07 | Ntakolia & Lyridis (2021) | Swarm Intelligence Graph-Based Pathfinding…SIGPAF          | Fuzzy/SIGPAF | Sim  | 1     | Gen. |
| S08 | Pan et al. (2022)       | Border patrol task planning…heterogeneous UAVs…SFLA          | SFLA         | Sim  | 1–4   | Mon. |
| S09 | Phung & Ha (2021)       | Safety-enhanced UAV path planning…PSO                        | PSO          | Sim  | 1     | Map. |
| S10 | Puente-Castro et al. (2022) | Review of AI applied to path planning in UAV swarms      | Review       | N/A  | N/A   | Gen. |
| S11 | Sharma et al. (2022)    | Path Planning for Multiple Targets…Swarm of UAVs…Review      | Review       | N/A  | N/A   | Gen. |
| S12 | Yu et al. (2021)        | Novel Sparrow Particle Swarm Algorithm (SPSA)                | PSO hybrid   | Sim  | 1     | Gen. |
| S13 | Chu et al. (2022)       | Chaos PSO Enhancement Algorithm for UAV Safe Path Planning   | PSO          | Sim  | 1     | Spr. |
| S14 | Fevgas et al. (2022)    | Coverage Path Planning…Energy Efficient…UAVs — Review        | Review       | N/A  | N/A   | Gen. |
| S15 | Israr et al. (2022)     | Optimization Methods Applied to Motion Planning of UAVs…     | Review       | N/A  | N/A   | Gen. |
| S16 | Ji et al. (2022)        | Novel UAV Path Planning…Double-Dynamic Biogeography PSO      | PSO          | Sim  | 1     | Gen. |
| S17 | Ait Saadi et al. (2022) | UAV Path Planning Using Optimization Approaches: A Survey    | Review       | N/A  | N/A   | Gen. |
| S18 | Selma et al. (2022)     | Optimal ANFIS Controller using Bee Colony…Quadrotor UAV      | ABC          | Sim  | 1     | Gen. |
| S19 | Shafiq et al. (2022)    | Convergence Analysis…Multi-UAVs…Max-Min ACO                  | ACO          | Sim  | 2     | Gen. |
| S20 | Ahmed et al. (2021)     | Distributed 3-D Path Planning…Multi-UAVs…PSO                 | PSO          | Sim  | 4     | Gen. |
| S21 | Xu et al. (2022)        | Task Allocation…UAV Swarm…Multi-Discrete Wolf Pack            | Wolf Pack    | Sim  | 5–15  | Gen. |
| S22 | Wang et al. (2025)      | Path Planning…Mobile Platforms…Hybrid Swarm Intelligence     | ABC+BAS      | S+T  | 1     | Gen. |
| S23 | Deng et al. (2023)      | 3D Path Planning of UAV…Improved PSO                         | PSO          | Sim  | 1     | Gen. |
| S24 | Xiao et al. (2025)      | Multi-UAV Path Planning…Improved Nutcracker Optimization     | NOA          | Sim  | 6–8   | Gen. |
| S25 | Li et al. (2023)        | Enhancing Swarm Intelligence…Dung Beetle Optimization        | DBO          | Sim  | 1     | Gen. |
| S26 | Rao et al. (2024)       | Multi-Strategy Collaborative Grey Wolf Optimization…UAV      | GWO          | Sim  | 1     | Gen. |
| S27 | Zhang & Zhang (2022)    | Efficient UAV Localization Technique…PSO                     | PSO          | Sim  | 2+    | Gen. |
| S28 | Hu et al. (2025)        | Improved PSO…Fuzzy Controller Fusion…Multi-Robot Path Planning| PSO          | Sim  | 6–7   | Gen. |
| S29 | Zuo et al. (2025)       | Hybrid APF-PSO Algorithm…UAV Swarms (→ PSO variant)          | APF+PSO      | Sim  | 5–25  | Gen. |
| S30 | Yang et al. (2025)      | 3D Path Planning for UAV…Multi-Strategy Dream Optimization   | DOA          | Sim  | 1     | Gen. |
| S31 | Yang et al. (2023)      | UAV Formation Trajectory Planning Algorithms: A Review       | Review       | N/A  | N/A   | Gen. |
| S32 | Tang et al. (2022)      | Swarm intelligence algorithms for multiple UAVs…Review       | Review       | N/A  | N/A   | Gen. |
| S33 | Li et al. (2025)        | Intelligently Enhanced ACO…Global Path Planning Mobile Robots | ACO         | S+T  | 1     | Gen. |

*Leyenda: App. = Mon. (Monitoring), Spr. (Spraying), Map. (Mapping), Gen. (General). Val. = Sim (simulation only), S+T (simulation + testbed).*

---

## Parte 2: 18 Estudios Excluidos a Texto Completo

*(EXC_15, EXC_19, EXC_20 reclasificados al cribado — ver nota de reconciliación)*

| ID      | Referencia              | Razón de exclusión                                              | Criterio |
|---------|-------------------------|-----------------------------------------------------------------|----------|
| EXC_01  | Li et al. (2025)        | Single-UAV focus, no swarm coordination — *discrepancia resuelta* | E3    |
| EXC_02  | Zhou et al. (2024)      | No SI algorithm; survey of non-SI methods                       | E4       |
| EXC_03  | Li et al. (2023)        | Mobile robot navigation, not agricultural UAV                   | E5       |
| EXC_04  | Saadi et al. (2022)     | No agricultural application context                             | E5       |
| EXC_05  | Zhang et al. (2024)     | GA-PSO without SI core component per inclusion criteria         | E4       |
| EXC_06  | Zhang et al. (2022)     | Harris Hawks Optimization not classified as SI in this taxonomy | E4       |
| EXC_07  | Wan et al. (2022)       | Disaster emergency response, no agricultural application        | E5       |
| EXC_08  | Srilekha et al. (2025)  | Flying cars / aerial transportation, not agricultural UAV       | E5       |
| EXC_09  | Huang et al. (2023)     | Single-UAV; no multi-agent coordination component               | E3       |
| EXC_10  | Chen et al. (2024)      | General path planning, no agricultural application context      | E5       |
| EXC_11  | Ntakolia & Lyridis (2021b) | Unmanned Surface Vehicle, not UAV                            | E5       |
| EXC_12  | Ali et al. (2021)       | Vehicular communication / IoV, no UAV path planning — *discrepancia resuelta* | E5 |
| EXC_13  | Khan et al. (2022)      | Robot vision / self-supervised learning, no UAV or SI          | E5       |
| EXC_14  | Luo et al. (2022)       | BOA-TSAR is not a swarm intelligence algorithm                  | E4       |
| EXC_16  | Bento et al. (2023)     | Classifier-based crop prediction, no path planning or SI        | E4       |
| EXC_17  | Sharma & Aibin (2023)   | Search and rescue with frame dropping; no SI path planning      | E5       |
| EXC_18  | Saeed et al. (2022)     | 5G user identity privacy; no UAV or SI path planning            | E5       |
| EXC_21  | Guzman et al. (2024)    | Safety assurance for symbolic AI; no UAV or SI path planning    | E5       |

---

*Criterios de exclusión: E1 = Fuera del período 2021–2025 | E3 = UAV único, sin coordinación swarm | E4 = No usa algoritmo SI | E5 = Dominio no agrícola / fuera de scope*

# 📝 Makefile Unificado: PRISMA + LaTeX + Datos + Ofimática
TEX_DIR := /home/andres/Documentos/ANTIGRAVITY-PROYECTOS/Revision/Swarm Intelligence Algorithms for Multi-RPAS/PAPER_REVISION_SWARM_RPAS/05_ESCRITURA
TEX_FILE := $(TEX_DIR)/main_expanded.tex
BIB_FILE := $(TEX_DIR)/references_clean.bib

p ?= .
f ?= ia-agents
fmt ?= md

.DEFAULT_GOAL := help
.PHONY: help prisma latex-bib compile analisis audit clean clean-all

help: ## 📋 Mostrar comandos disponibles
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-12s\033[0m %s\n", $$1, $$2}'

prisma: ## 🔍 Validar .tex contra reglas PRISMA/Elsevier
	@uv run python src/prisma_checker.py "$(TEX_FILE)"

latex-bib: ## 📄 Consistencia citas/.bib + reporte Word
	@uv run python src/latex_checker.py --tex "$(TEX_FILE)" --bib "$(BIB_FILE)" --format word

compile: ## 📖 Compilar manuscrito (XeLaTeX → BibTeX → XeLaTeX x2)
	@cd "$(TEX_DIR)" && xelatex main_expanded.tex && bibtex main_expanded && xelatex main_expanded.tex && xelatex main_expanded.tex

analisis: ## 📈 Procesar CSV → Parquet → Reporte (i=ruta, f=enfoque, fmt=formato)
	@uv run python src/pipeline_tecnico.py $(i) $(f)
	@uv run python -m src.cli -p $(p) -f $(f) --format $(fmt)

audit: ## 📄 Auditoría instantánea del proyecto actual
	@uv run python -m src.cli -p $(p) -f $(f) --format $(fmt)

clean: ## 🧹 Limpiar cachés, logs y reportes viejos
	@echo "🧹 Limpiando..."
	@rm -rf __pycache__ .pytest_cache .ipynb_checkpoints
	@find . -type f -name "*.pyc" -delete
	@rm -f reports/auditoria_*.* reports/prisma_check_*.* reports/latex_check_*.*
	@echo "✅ Cachés y reportes limpiados."

clean-all: clean ## 🗑️ Limpieza profunda (datos procesados + cache uv)
	@echo "⚠️  Limpiando datos procesados y cache uv..."
	@rm -rf data/processed/*
	@uv cache clean
	@echo "✅ Limpieza profunda completada."

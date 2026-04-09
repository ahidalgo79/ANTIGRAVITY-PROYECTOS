.PHONY: help lab sync run add remove clean format lint

help: ## 📖 Muestra esta ayuda
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-15s\033[0m %s\n", $$1, $$2}'

lab: ## 🚀 Inicia Jupyter Lab
	@uv run jupyter lab

sync: ## 🔄 Sincroniza dependencias (lee pyproject.toml + uv.lock)
	@uv sync

run: ## ▶️ Ejecuta script: make run script=analisis.py
	@uv run python $(script)

add: ## ➕ Agrega paquete: make add pkg=ruff
	@uv add $(pkg)

remove: ## ➖ Elimina paquete: make remove pkg=pandas
	@uv remove $(pkg)

format: ## 🎨 Formatea código automáticamente
	@uv run ruff format .

lint: ## 🔍 Revisa errores de estilo y bugs
	@uv run ruff check .

clean: ## 🧹 Limpia cachés, __pycache__ y checkpoints
	@rm -rf __pycache__ .ipynb_checkpoints .pytest_cache .mypy_cache
	@find . -name "*.pyc" -delete
	@echo "✅ Limpieza completada"

# 🤖 CrewAI / Multi-agente
crew:  ## 🚀 Ejecutar crew creativo: make crew tema="Mi tema aquí"
	@uv run python src/crew_creativo.py "$(tema)"

crew-save:  ## 💾 Ejecutar y guardar output en reports/
	@mkdir -p reports
	@uv run python src/crew_creativo.py "$(tema)" > reports/crew_`date +%Y%m%d_%H%M`.txt

ollama-serve:  ## 🔌 Iniciar Ollama en background
	@ollama serve &
	@echo "✅ Ollama iniciado (PID: $$!)"

# 📊 Auditorías rápidas (1 palabra)

# 🔧 Valores por defecto (sobrescribe con: make target p=./ruta f=tema)
p ?= .
f ?= ia-agents

audit:
	@uv run python -m src.cli -p $(p) -f $(f) --format md

audit-word:
	@uv run python -m src.cli -p $(p) -f $(f) --format word && ls -t reports/*.docx 2>/dev/null | head -1 | xargs xdg-open 2>/dev/null || true

audit-pdf:
	@uv run python -m src.cli -p $(p) -f $(f) --format pdf && ls -t reports/*.pdf 2>/dev/null | head -1 | xargs xdg-open 2>/dev/null || true

# 🛠️ Pipeline técnico + reporte
analisis:
	@uv run python src/pipeline_tecnico.py $(i) $(f)
	@uv run python -m src.cli -p . -f $(f) --format $(fmt)

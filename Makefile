# Variables
VENV_NAME = .venv
PYTHON = $(VENV_NAME)/bin/python
PIP = $(VENV_NAME)/bin/pip

# Default target
.PHONY: help
help:
	@echo "Usage: make [target]"
	@echo ""
	@echo "Targets:"
	@echo "  venv        Create virtual environment"
	@echo "  install     Install dependencies"
	@echo "  run         Run the Streamlit app"
	@echo "  format      Format code with black"
	@echo "  lint        Lint code with flake8"
	@echo "  clean       Remove virtual environment"
	@echo "  freeze      Generate requirements.txt"

.PHONY: venv
venv:
	python3 -m venv $(VENV_NAME)
	@echo "✅ Virtual environment created in $(VENV_NAME)"

.PHONY: install
install:
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt
	@echo "✅ Dependencies installed"

.PHONY: run
run:
	$(VENV_NAME)/bin/streamlit run app.py

.PHONY: format
format:
	$(VENV_NAME)/bin/black .

.PHONY: lint
lint:
	$(VENV_NAME)/bin/flake8 .

.PHONY: clean
clean:
	rm -rf $(VENV_NAME)
	@echo "🧹 Virtual environment removed"

.PHONY: freeze
freeze:
	$(PIP) freeze > requirements.txt
	@echo "📦 requirements.txt updated"

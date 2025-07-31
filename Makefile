.PHONY: help install install-dev dev test test-watch db-init db-migrate db-upgrade clean lint format run

# Hilfe anzeigen
help:
	@echo "ADHS-Assistent Makefile Commands:"
	@echo "================================================"
	@echo "  make install      - Installiere Produktions-Dependencies"
	@echo "  make install-dev  - Installiere alle Dependencies (inkl. Dev)"
	@echo "  make dev         - Starte Development Server"
	@echo "  make test        - Führe alle Tests aus"
	@echo "  make test-watch  - Tests im Watch-Modus"
	@echo "  make db-init     - Initialisiere Datenbank"
	@echo "  make db-migrate  - Erstelle neue Migration"
	@echo "  make db-upgrade  - Führe Migrationen aus"
	@echo "  make lint        - Code-Qualität prüfen"
	@echo "  make format      - Code formatieren"
	@echo "  make clean       - Aufräumen (Cache, etc.)"
	@echo "  make run         - Starte Produktions-Server"

# Installation
install:
	pip install -r requirements.txt

install-dev: install
	pip install -r requirements-dev.txt
	pre-commit install

# Development
dev:
	python -m flask run --debug --reload

# Testing
test:
	pytest tests/ -v --cov=app --cov-report=html --cov-report=term

test-watch:
	ptw tests/ -- -v

# Datenbank
db-init:
	python scripts/init_db.py

db-migrate:
	alembic revision --autogenerate -m "$(filter-out $@,$(MAKECMDGOALS))"

db-upgrade:
	alembic upgrade head

db-downgrade:
	alembic downgrade -1

db-seed:
	python scripts/seed_data.py

# Code-Qualität
lint:
	flake8 app/ tests/
	pylint app/
	mypy app/

format:
	black app/ tests/
	isort app/ tests/

# Aufräumen
clean:
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.log" -delete
	rm -rf .pytest_cache/
	rm -rf .coverage
	rm -rf htmlcov/
	rm -rf dist/
	rm -rf build/
	rm -rf *.egg-info

# Produktion
run:
	gunicorn -w 4 -b 0.0.0.0:8000 app:create_app()

# Git Shortcuts
commit:
	git add -A && git commit -m "$(filter-out $@,$(MAKECMDGOALS))"

push:
	git push origin $(shell git branch --show-current)

# Virtuelle Umgebung
venv:
	python3 -m venv .venv
	@echo "Aktiviere die Umgebung mit: source .venv/bin/activate"

# Dokumentation
docs:
	cd docs && mkdocs serve

docs-build:
	cd docs && mkdocs build

# Backup
backup:
	python scripts/backup_db.py

# Shortcuts
%:
	@:

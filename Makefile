.PHONY: up install install-dev lint format down help db/migrate db/downgrade

SRC_DIR = $(CURDIR)/src



all: up

# Запуск приложения
up:
	@docker compose up -d --build

# Очистка после остановки приложения Auth
down:
	@echo "Очистка временных файлов и контейнеров..."
	@docker compose down
	@find . -type f -name '*.pyc' -delete
	@find . -type d -name '__pycache__' -delete

# Установка зависимостей
install:
	@echo "Установка зависимостей..."
	@pip install -r requirements.txt

# Установка зависимостей dev
install-dev:
	@echo "Установка зависимостей..."
	@pip install -r requirements-dev.txt

# Миграции
db/migrate:
	@docker compose exec fastapi uv run alembic upgrade head

# Откат миграции
db/downgrade:
	@docker compose exec fastapi uv run alembic downgrade base

# Линтинг
lint:
	@echo "Запуск линтинга..."
	@ruff check $(SRC_DIR)
	@echo "All done! ✨ 🍰 ✨"

# Автоформатирование
format:
	@echo "Запуск форматирования..."
	@ruff check $(SRC_DIR) --fix

# Вывод справки
help:
	@echo "Доступные команды:"
	@echo "  make up                  - Запуск сервиса"
	@echo "  make down                - Остановка сервиса и очиска"
	@echo "  make install             - Установка зависимостей"
	@echo "  make install-dev         - Установка зависимостей для разработки"
	@echo "  make db/migrate          - Миграция alembic"
	@echo "  make db/downgrade        - Откат миграции alembic"
	@echo "  make lint                - Запуск линтера"
	@echo "  make format              - Автоформатирование кода"

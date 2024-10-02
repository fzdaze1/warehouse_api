# Установка и запуск
# Через Docker
1) Клонировать репозиторий
   ```
   git clone https://github.com/fzdaze1/warehouse_api.git
   ```
2) Перейти в директорию проекта
   ```
   cd warehouse_api
   ```
3) Выполнить команду для запуска проекта. Эта команда соберёт и запустит все контейнеры, описанные в файле docker-compose.yml
   ```
   docker compose up -d --build
   ```

4) Провести тесты при желании можно с помощью pytest(файл с тестами в директории app/rental/tests.py
   ```
   docker compose exec web python -m pytest
   ```
Документация http://localhost:8000/docs

# Тема проєкту: "Особистий менеджер задач з CLI, REST API та збереженням у JSON-файлі" #
📌 Суть:
Створити просту систему управління задачами, яку можна використовувати як з командного рядка (CLI), так і через HTTP-запити (REST API). Збереження даних — у локальному JSON-файлі. Ідея схожа на Trello, але сильно спрощена.

# Учасники #
Крулевський Максім ІМ-34
Діана Дубенок ІМ-34

# Personal Task Manager (CLI + REST API) 📋

[![Python](https://img.shields.io/badge/Python-3.11%2B-blue.svg)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.109.0-green.svg)](https://fastapi.tiangolo.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**Ukrainian** 

---

## 📌 Опис Проєкту
Простий менеджер завдань з двома інтерфейсами: командним рядком (CLI) та REST API. Зберігає дані у JSON-файлі. Натхненний спрощеною версією Trello.

## ✨ Можливості
- **Повний CRUD для завдань**:
  - Створення завдань (назва, опис, дата завершення)
  - Перегляд (всі завдання, фільтрація за статусом, деталі за ID)
  - Оновлення статусу (`todo` | `in_progress` | `done`) та дати
  - Видалення за ID
- **Інтерфейси**:
  - CLI для локального використання
  - REST API для інтеграцій
- **Зберігання**: У файлі `tasks.json`
- **Валідація**: Контроль коректності даних

## 🛠️ Технології
- Python 3.11+
- FastAPI + Uvicorn
- Pydantic (валідація)
- Argparse (CLI)
- Pytest (тестування)
- GitHub Actions (CI/CD)

## ⚙️ Встановлення
```bash
git clone https://github.com/YOUR_USER/YOUR_REPO.git
cd YOUR_REPO
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate    # Windows
pip install -r requirements.txt

💻 Використання CLI
# Додати завдання
python -m task_manager.cli add --title "Купити хліб" --description "Цільнозерновий"

# Список усіх завдань
python -m task_manager.cli list

# Оновити статус
python -m task_manager.cli update --id 1 --status in_progress

# Видалити завдання
python -m task_manager.cli delete --id 1

🌐 Використання API
uvicorn task_manager.api:app --reload

# Створити завдання
curl -X POST http://localhost:8000/tasks -H "Content-Type: application/json" -d '{
  "title": "API Task",
  "description": "Test via API"
}'

# Отримати завдання зі статусом 'todo'
curl "http://localhost:8000/tasks?status=todo"

🧪 Тестування
pytest tests/
```
Доступна документація: http://localhost:8000/docs

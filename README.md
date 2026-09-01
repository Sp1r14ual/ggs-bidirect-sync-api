# GGS Bidirect Sync API

API для двухсторонней интеграции с Битрикс24 и базой данных (ОСА)

---

## 📦 Инструкция по запуску

### 1. Клонирование репозитория

```bash
git clone https://github.com/Sp1r14ual/ggs-bidirect-sync-api.git
cd ggs-bidirect-sync-api
```

### 2. Настройка окружения и зависимостей

```
python -m venv .venv

# Активация (Windows)
.venv\Scripts\activate

# Активация (Linux/macOS)
source .venv/bin/activate

pip install -r requirements.txt
```

### 3. Настройка переменных окружения

Скопируйте пример файла конфигурации и заполните его:
```
cp .env.example .env
```

### 4. Запуск сервера
```bash
fastapi dev app/app.py
```

Сервер запустится на порту 8000

### 4.5 Запуск MCP сервера [Опционально]
В отдельной сессии терминала (или фоново) вызвать
```bash
mcp dev mcp_server.py
```

Web интерфейс будет доступен по адресу:

http://127.0.0.1:6274/

### 5. Модификация БД

Перед запуском каких-либо функций запустить скрипт [prepare.sql](prepare.sql) в БД ggs_stud

### 6. Документация API

Документация в формате OpenAPI доступна по адресу:

🔗 http://127.0.0.1:8000/docs
# Delivery Service - DDD Implementation

Проект реализует систему управления доставками с использованием принципов Domain-Driven Design (DDD).

## Требования

- Docker и Docker Compose
- Python 3.10+
- PostgreSQL (запускается через Docker)

## Быстрый старт

### 1. Запуск базы данных

```bash
docker-compose up -d
```

### 2. Настройка окружения

```bash
python3 -m venv venv
source venv/bin/activate  # Linux/MacOS
venv\Scripts\activate     # Windows
pip install -r requirements.txt
```

### 3. Инициализация БД

```bash
python3 infrastructure/adapters/postgres/init_db.py
```

### 4. Демонстрационный запуск

```bash
python3 demo.py
```

Пример вывода:
```bash
==================================================
=== CLEARING DATABASE ===
==================================================
🗑️  Database cleared!

==================================================
=== 1. TESTING COURIER REPOSITORY ===
==================================================
✅ Added courier: fe0afa77-127a-48f5-9a12-c6dcc9dd208d - Courier One
✅ Retrieved courier: fe0afa77-127a-48f5-9a12-c6dcc9dd208d - Status: free
✅ Updated courier fe0afa77-127a-48f5-9a12-c6dcc9dd208d status to: busy
✅ Free couriers count: 2 (expected: 2)
  - Courier Two (6655b82a-29ce-4ad9-b8b6-c7a69b1d48fe)
  - Courier Three (bc51e63c-4dca-4eb3-bdc2-b48509871762)
```

### 5. Проверка БД

```bash
docker exec -it delivery-postgres-1 psql -U ddd_user -d ddd_delivery -c "SELECT * FROM couriers;"
docker exec -it delivery-postgres-1 psql -U ddd_user -d ddd_delivery -c "SELECT * FROM orders;"
```

## Запуск тестов

```bash
pytest
```

Или для конкретного теста:

```bash
pytest tests/integration/test_create_order_integration.py
```


## Остановка

```
docker-compose down -v
deactivate
```
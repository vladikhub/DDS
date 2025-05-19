# Веб-приложение для учёта движения денежных средств (ДДС)
Проект позволяет удобно управлять поступлениями и расходами, используя веб-интерфейс с фильтрацией, справочниками и системой категорий.

## Как запустить проект?

### 1. Клонирование репозитория

```bash
git clone https://github.com/your-username/dds-tracker.git
cd dds-tracker
```
### 2. Создание виртуального окружения

```bash
python -m venv venv
source venv/bin/activate  # Linux / macOS
venv\Scripts\activate   # Windows
```

### 3. Установка зависимостей
```bash
pip install -r requirements.txt
```

### 4. Применение миграций
```bash
python manage.py migrate
```

### 5. Для допуска к Админ-панели сайта
```bash
python manage.py createsuperuser
```

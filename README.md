# Документация: Парсер Wildberries (Django + React + Selenium)

📌 **Оглавление**

*   [Описание проекта](#-описание-проекта)
*   [Технологии](#-технологии)
*   [Развертывание локально](#-развертывание-локально)
*   [Использование](#-использование)
*   [API Endpoints](#-api-endpoints)
*   [Дополнительные настройки](#-дополнительные-настройки)
*   [Возможные проблемы и решения](#-возможные-проблемы-и-решения)

## 🌐 Описание проекта

Проект представляет собой парсер товаров с Wildberries, который:

*   Ищет товары по запросу (например, "Очки").
*   Фильтрует их по цене (например, 1–5 тыс. руб.) и ключевому слову ("Черный").
*   Сохраняет данные в базу (PostgreSQL/SQLite).
*   Отображает результаты через React-интерфейс или API.

## 🛠 Технологии

| Компонент   | Технология                 |
| :---------- | :------------------------- |
| Бэкенд      | Django + DRF (API)         |
| Фронтенд    | React                      |
| Парсинг     | Selenium (ChromeDriver)    |
| База данных | SQLite (по умолчанию) / PostgreSQL |
| Сборка      | npm (React), pip (Python)  |

## 🚀 Развертывание локально

1.  **Клонирование репозитория**

    ```bash
    git clone https://github.com/ваш-репозиторий.git
    cd wildberries_parser
    ```

2.  **Настройка Python (Django)**

    Создайте виртуальное окружение:

    ```bash
    python -m venv venv
    source venv/bin/activate  # Linux/Mac
    venv\Scripts\activate     # Windows
    ```

    Установите зависимости:

    ```bash
    pip install -r requirements.txt
    ```

3.  **Настройка базы данных**

    *   **SQLite (используется по умолчанию):**

        ```bash
        python manage.py migrate
        ```

    *   **PostgreSQL (опционально):**

        Установите PostgreSQL и создайте БД.

        В `settings.py` укажите:

        ```python
        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.postgresql',
                'NAME': 'имя_бд',
                'USER': 'пользователь',
                'PASSWORD': 'пароль',
                'HOST': 'localhost',
                'PORT': '5432',
            }
        }
        ```

4.  **Настройка React**

    Убедитесь, что установлен Node.js (v16+):

    ```bash
    node -v
    npm -v
    ```

    Перейдите в папку `frontend` и установите зависимости:

    ```bash
    cd frontend
    npm install
    ```

    Соберите React-приложение:

    ```bash
    npm run build
    ```

    Вернитесь в корневую папку:

    ```bash
    cd ..
    ```
5. **Настроить переменные окружения**

Заполните .env.template

Рекомендация: В случае, если у вас Google Chrome > 114 версии, лучше установить Firefox и указать его в BROWSER
.Chrome стал проприетарным после 115, поэтому с драйверами проблема, как следствие и Selenium не захочет работать

**Пример заполнения env**:
```
BROWSER=Firefox
FIREFOX_PATH="D:\Mozilla Firefox\\firefox.exe"
CHROME_PATH="C:\Program Files\Google\Chrome Dev\Application\chrome.exe"
HEADLESS_MODE=True
PRODUCT=очки
MIN_PRICE=10
MAX_PRICE=5000
KEYWORD=солнечные
```
6. **Запуск проекта**

    Запустите Django-сервер:

    ```bash
    python manage.py runserver
    ```

    Запустите React в dev-режиме (опционально):

    ```bash
    cd frontend
    npm start
    ```

📌 **Доступные адреса:**

*   Django + React → `http://localhost:8000`
*   Только React (dev-режим) → `http://localhost:3000`
*   Django API → `http://localhost:8000/api/products/`

## 🖥 Использование

1.  **Запуск парсинга**

    ```bash
    python manage.py parse_wb
    ```
    (Товары сохраняются в базу данных.)

Парсер сделает ряд проверок:
1) Проверить что скрипт запущен от имени администратора
2) Проверит корректность указанного пути к браузеру в env
3) Проверить что драйвер браузера инициализирован


2.  **Просмотр данных**

    *   Через React: Откройте `http://localhost:8000`.
    *   Через API:

        ```bash
        curl http://localhost:8000/api/products/
        ```

3.  **Фильтрация через API**

    Пример запроса:

    ```bash
    curl "http://localhost:8000/api/products/?price_min=1000&price_max=5000&color=Черный"
    ```

## 📡 API Endpoints

| Метод | URL                                         | Описание                               |
| :---- | :------------------------------------------ | :------------------------------------- |
| GET   | `/api/products/`                            | Список всех товаров                    |
| GET   | `/api/products/?price_min=1000&price_max=5000` | Фильтрация по цене                     |
| POST  | `/api/parse/`                               | Запуск парсинга (вручную)              |

## ⚙ Дополнительные настройки

1.  **Настройка Selenium**

    Убедитесь, что установлен Chrome и ChromeDriver, либо Mozilla Firefox.

    Для фонового режима добавьте в `services.py`:

    ```python
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    ```

2.  **Прокси и User-Agent**

    Чтобы избежать блокировки:

    ```python
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64)")
    ```
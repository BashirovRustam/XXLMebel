# 🏨 **API endpoints** — тестовое задание



---

## 🛠️ Стек технологий:

<p align="center">

[![Python](https://img.shields.io/badge/Python-464646?style=flat-square\&logo=python)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-464646?style=flat-square\&logo=fastapi)](https://fastapi.tiangolo.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-464646?style=flat-square\&logo=postgresql)](https://www.postgresql.org/)
[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-464646?style=flat-square\&logo=sqlalchemy)](https://www.sqlalchemy.org/)
[![Docker](https://img.shields.io/badge/Docker-464646?style=flat-square\&logo=docker)](https://www.docker.com/)
</p>

---


---

## ▶️ Локальный запуск

### 🔧 Требования

* Docker
* Docker Compose
* Git

---

### 📥 Клонирование репозитория

```bash
git clone https://github.com/BashirovRustam/XXLMebel.git
cd Ваша дирекотрия
```

#### 2️⃣ Настройка виртуального окружения

Создайте и активируйте виртуальное окружение для изоляции зависимостей проекта:

**🪟 Windows (PowerShell):**
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

**🪟 Windows (CMD):**
```cmd
python -m venv venv
venv\Scripts\activate.bat
```

**🐧 Linux / 🍎 macOS:**
```bash
python3 -m venv venv
source venv/bin/activate
```

#### 4️⃣ Запуск Docker-инфраструктуры (запускается докер образ локально и заполняются тестовыми данными для модели Furniture)


```bash
docker-compose up --build

```
Все данные для подлючения тянутся из переменной окружения .ENV
Для удобства тесторования вложен тестовый пример файла .evn example

#### ✅ Готово!

Сервис доступен по адресу:
- 🌐 **API:** [http://localhost:8000](http://localhost:8000)
- 📚 **Swagger Docs:** [http://localhost:8000/docs](http://localhost:8000/docs)



- API endpoints:
     - `GET /furniture/` — список всей мебели.
     - `GET /furniture/id/` — информация о конкретном товаре.
     - `POST /orders/` — создание заказа (принимает email клиента и список ID товаров, рассчитывает сумму).
     - после создания заказа придет письмо (реализовано через локальный Mailhog и доступоно по пути http://localhost:8025)
     - `GET /orders/` — список заказов по email клиента (query-параметр `email`).




---

# 🏭 Basic ERP – Django DRF

A modular **ERP system for basic business** (general).
Includes **users, inventory, purchases, sales, invoices, and reports** with async task handling and real-time background jobs.

---

## 🔋 Features

* ✅ **User Management & Roles** (Admin creates users)
* ✅ **Inventory** (Items, Stock auto-management with signals)
* ✅ **Purchases** (Suppliers, Purchase Orders with status workflow)
* ✅ **Sales** (Customers, Sales Orders, auto invoice generation)
* ✅ **Invoices** (Automatic invoice PDF + email via Celery)
* ✅ **Reports** (Daily/Monthly sales, purchase reports)
* ✅ **Async Tasks** using **Celery + RabbitMQ + Redis**
* ✅ **Monitoring** with **Flower & RabbitMQ Management UI**
* ✅ **API Documentaion** with **drf_yasg - Yet Another Swagger Generator**

---

## 📦 Tech Stack

* 🏗 **Backend:** Python 3.11, Django, Django REST Framework
* 💾 **Database:** PostgreSQL
* ⚡ **Async Queue:** Celery + RabbitMQ (broker) + Redis (cache/result backend)
* 📨 **Emailing:** Django Email Backend + Celery Tasks
* 📊 **Monitoring:** Flower, RabbitMQ Management UI
* 📊 **API Documentation:** drf_yasg - Yet Another Swagger Generator

---
## 📧 Invoice Emailing

Whenever a **Sales Order is confirmed**, an **Invoice is automatically generated** and a **PDF invoice is emailed** to the customer (if they have an email ID).
This uses:

* Django Template (HTML → PDF)
* Celery task for async emailing

---
## 📧 API Documentation

Auto-generated API docs using drf_yasg - Yet Another Swagger Generator:

* drf_yasg for auto-generated api doc at [http://127.0.0.1:8000/swagger/](http://127.0.0.1:8000/swagger/) or [http://127.0.0.1:8000/redoc/](http://127.0.0.1:8000/redoc)
* Celery task for async emailing

---

## 🚀 Project Setup

### 1️⃣ Clone Repository

```bash
git clone https://github.com/vedp18/erp.git
cd erp
```

---

### 2️⃣ Setup Virtual Environment

```bash
python -m venv venv
source venv/bin/activate   # On Linux/Mac
venv\Scripts\activate      # On Windows
```

---

### 3️⃣ Install Requirements

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

---

### 4️⃣ Configure Environment Variables

Create a `.env` file in the root of your project:

```env
# Django
SECRET_KEY=your_secret_key
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost

# Database (PostgreSQL)
DB_NAME=erpdb
DB_USER=erpuser
DB_PASSWORD=erppassword
DB_HOST=localhost
DB_PORT=5432

# Redis
REDIS_URL=redis://localhost:6379/0

# RabbitMQ
CELERY_BROKER_URL=amqp://guest:guest@localhost:5672//

# Email
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your_email@gmail.com
EMAIL_HOST_PASSWORD=your_password    # add app passwords instead of gmail_account password
EMAIL_USE_TLS=True

# OR use Console Backend
```

---

### 5️⃣ Setup PostgreSQL Database

```bash
# Login to PostgreSQL
psql -U postgres

# Inside psql console:
CREATE DATABASE erpdb;
CREATE USER <user> WITH PASSWORD '<password>';
ALTER ROLE <user> SET client_encoding TO 'utf8';
ALTER ROLE <user> SET default_transaction_isolation TO 'read committed';
ALTER ROLE <user> SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE erpdb TO <user>;
```

Apply migrations:

```bash
python manage.py migrate
python manage.py createsuperuser
```

---

### 6️⃣ Run Development Server

```bash
python manage.py runserver
```

Now visit: [http://127.0.0.1:8000](http://127.0.0.1:8000) 🎉

---

## ⚡ Async Services Setup

### 7️⃣ Start Redis

Make sure Redis is running (default port `6379`):

```bash
redis-server
```

---

### 8️⃣ Start RabbitMQ (with Management UI)

Install RabbitMQ (with `management` plugin enabled).
Start server:

```bash
sudo service rabbitmq-server start
```

RabbitMQ management dashboard:
👉 [http://localhost:15672](http://localhost:15672)
Default login: `guest / guest`

---

### 9️⃣ Run Celery Worker

```bash
celery -A manufacturing_erp worker --loglevel=info
```


---

### 1️⃣1️⃣ Run Flower (Celery Monitoring)

```bash
celery -A manufacturing_erp flower --port=5555
```

Visit 👉 [http://localhost:5555](http://localhost:5555)

---


## 📊 Reports

* Sales Reports
* Purchase Reports
* low stocks reports with dynamic reports

---

## 🛠 Development Notes

* Run all services in separate terminals:

  * `python manage.py runserver`
  * `celery -A erp worker`
  * `celery -A erp flower`
  * `redis-server`
  * `rabbitmq-server`

---

## 🐋 Coming Soon: Dockerized Setup

* Docker Compose with:

  * Django App
  * PostgreSQL
  * Redis
  * RabbitMQ + Management UI
  * Celery Worker
  * Flower

---


# 🛍️ VintGizmo - Multi-Vendor E-Commerce Platform

**VintGizmo** is a full-stack multi-vendor e-commerce web application built using **Django** and **PostgreSQL**. It provides a robust and scalable solution for managing an online marketplace, where multiple vendors can register, manage their stores, and sell products. The platform includes all essential CRUD operations, detailed stock management, banner customization, and admin control — with a clean, responsive frontend.

---

## 🚀 Features

### 🛒 Multi-Vendor Store
- Vendors can register and manage their own stores.
- Each vendor has access to a dedicated dashboard.
- Vendors can add, update, and remove products.

### 📦 Full Stock Management
- Real-time inventory tracking.
- Low-stock alerts to help vendors restock on time.
- Inventory updates reflected instantly in the frontend.

### ⭐ Product Reviews & Ratings
- Customers can leave feedback and rate products.
- Helps build trust and transparency for new buyers.

### 🎨 Admin-Editable Frontend Banners
- Frontend promotional banners are fully editable via the admin panel.
- Vendors can promote sales, offers, and featured categories.

### 📊 Profit & Loss Insight
- Vendors can view a breakdown of earnings and product-level performance (optional module).

### 🔐 Secure & Scalable
- Built with Django’s robust security.
- Designed to handle concurrent vendor activity and transactions.

---

## 🛠️ Tech Stack

- **Backend:** Django 4.1.13
- **Database:** PostgreSQL
- **Frontend:** HTML/CSS/JavaScript (Django Templates)
- **Email Service:** SMTP via Gmail

---

## 📂 Project Structure

```bash
VintGizmo/
├── ecommerce/             # Django project
│   ├── settings.py
│   └── ...
├── VintGizmo/             # Core app (models, views, forms, etc.)
│   └── ...
├── static/                # Static assets
├── media/                 # Uploaded media
├── templates/             # HTML templates
├── requirements.txt
├── .gitignore
└── manage.py
```

---

## ⚙️ Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/Slayer9966/VintGizmo.git
cd VintGizmo/ecommerce
```

### 2. Create & Activate a Virtual Environment

```bash
python -m venv venv
venv\Scripts\activate   # On Windows
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure PostgreSQL

Update your database settings in `settings.py`:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'vintgizmo',
        'USER': 'myuser',
        'PASSWORD': 'admin',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

### 5. Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Create Superuser

```bash
python manage.py createsuperuser
```

### 7. Run the Server

```bash
python manage.py runserver
```









## 📧 Email Setup

Email is sent using Gmail SMTP. Add these to your `settings.py` or configure via environment variables:

```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your_email@gmail.com'
EMAIL_HOST_PASSWORD = 'your_app_password'
```

---

## 📌 Notes

- Payment gateway is not integrated yet.
- Fully open to future feature additions and enhancements.

---

## 📜 License

This project is licensed under the **MIT License** — you are free to use and modify it.

---

## 🙋‍♂️ Author

**Syed Muhammad Faizan Ali**  
📍 Islamabad, Pakistan  
📧 faizandev666@gmail.com  
🔗 [GitHub](https://github.com/Slayer9966) | [LinkedIn](https://www.linkedin.com/in/faizan-ali-7b4275297/)

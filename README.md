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
- Vendors can view a breakdown of earnings and product-level performance (optional module structure).

### 🔐 Secure & Scalable
- Built with Django security features.
- Designed to handle concurrent vendor activity and transactions.

---

## 🛠️ Tech Stack

- **Backend:** Django 4.1.13
- **Database:** PostgreSQL
- **Frontend:** HTML/CSS/JS (Django templates)
- **Email Service:** SMTP via Gmail

---

## 📂 Project Structure

```bash
VintGizmo/
├── ecommerce/               # Main Django project
│   ├── settings.py
│   └── ...
├── VintGizmo/               # Core app with models, views, etc.
│   └── ...
├── static/                  # Static files
├── media/                   # Uploaded media files
├── templates/               # HTML templates
├── requirements.txt
├── manage.py
└── .gitignore
📦 Setup Instructions
1. Clone the Repo
bash
Copy
Edit
git clone https://github.com/Slayer9966/VintGizmo.git
cd VintGizmo/ecommerce
2. Create & Activate a Virtual Environment
bash
Copy
Edit
python -m venv venv
venv\Scripts\activate   # On Windows
3. Install Dependencies
bash
Copy
Edit
pip install -r requirements.txt
4. Configure PostgreSQL
Make sure PostgreSQL is running and update DATABASES in settings.py if needed.

python
Copy
Edit
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
5. Run Migrations
bash
Copy
Edit
python manage.py makemigrations
python manage.py migrate
6. Create Superuser
bash
Copy
Edit
python manage.py createsuperuser
7. Run the Server
bash
Copy
Edit
python manage.py runserver
Visit http://127.0.0.1:8000/ to start using the app.

🔒 Admin Panel
Visit: http://127.0.0.1:8000/admin/
Use your superuser credentials to log in and manage vendors, products, banners, and more.

📧 Email Setup
Email sending is configured via SMTP. Make sure you use a valid Gmail account or set environment variables for security:

python
Copy
Edit
EMAIL_HOST_USER = 'your_email@gmail.com'
EMAIL_HOST_PASSWORD = 'your_app_password'
📌 Notes
Payment gateway is not integrated yet.

Project is fully open for feature additions and enhancements.

📜 License
This project is licensed under the MIT License — feel free to use and modify!

🙋‍♂️ Author
Syed Muhammad Faizan Ali
📍 Islamabad, Pakistan
📧 faizandev666@gmail.com
🔗 GitHub | LinkedIn

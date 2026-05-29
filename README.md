# 🛒 E-Commerce Storefront API

A production-ready RESTful API backend for an e-commerce platform built with **Django** and **Django REST Framework (DRF)**.

This project was built from scratch and features a complete relational database, business logic for inventory management, transactional order processing, and secure user authentication.

## 🚀 Features

* **Product Management:** Full CRUD (Create, Read, Update, Delete) operations for store inventory.
* **Categories:** Relational database design linking products to specific categories.
* **Secure Transactions:** Atomic database transactions for the checkout process to ensure inventory is correctly deducted and financial data is accurately recorded.
* **Authentication & Permissions:** Secure endpoints ensuring only logged-in users can place orders or view their personal order history, and only admins can modify inventory.
* **Order History:** Personalized endpoints for users to view their past purchases.
* **Data Validation:** Robust serializers to ensure clean, accurate data formatting (e.g., precise Decimal handling for currency).

## 🛠️ Tech Stack

* **Backend:** Python 3, Django
* **API Framework:** Django REST Framework (DRF)
* **Database:** SQLite (Development)

## 📦 Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git](https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git)
   cd store_project
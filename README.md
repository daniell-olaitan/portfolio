# 🧳 Portfolio Platform

A **comprehensive, full-stack solution** for building, managing, and showcasing personal portfolios. This platform is designed for developers, freelancers, and professionals who want to create a dynamic and secure online presence.

---

## 📌 Project Overview

**Portfolio Platform** is a robust multi-part application developed to provide users with a seamless way to manage and display their personal portfolios. Built as part of a full-stack development initiative, this project emphasizes security, scalability, and developer experience.

---

## 🚀 Key Features

### 1. 🔐 **Public API**
- Secure and developer-friendly RESTful API for portfolio integration
- Authentication and authorization system with JWT
- Fully documented using **OpenAPI** for easy third-party use

### 2. 🧩 **Portfolio Management System**
- Admin and user roles for dynamic content management
- Backend dashboard for project uploads, edits, and portfolio customization
- OTP-based password recovery with **Celery + Redis** for secure expiration handling

### 3. 🌐 **Portfolio Website**
- Front-facing responsive site to showcase projects and user profiles
- Built using HTML, CSS, and JavaScript for professional presentation

---

## ⚙️ Architecture & Tech Stack

- **Backend**: Python, Flask, MySQL, Celery, Redis, OpenAPI
- **Frontend**: HTML, CSS, JavaScript
- **Deployment**: AWS EC2 (hosting), AWS RDS (database), NGINX + Gunicorn
- **Testing**: Python `unittest` for backend logic and endpoint validation

---

## 🔒 Security & Reliability

- OTP verification system with expiration logic via Redis
- Automatic file and data cleanup for resource efficiency
- Modular backend with layered architecture for scalability

---

## 🧪 Testing & Documentation

- Full unit test coverage using Python’s `unittest` module
- Well-documented endpoints via OpenAPI/Swagger for seamless integration

---

## 📈 Achievements

- Designed and built a **versatile, scalable portfolio platform**
- Implemented **secure, OTP-based recovery system** using Celery and Redis
- **Deployed** a full-stack application using **AWS, NGINX, and Gunicorn**
- Delivered a maintainable, production-ready architecture optimized for professional use

---

## Installation and Setup

### 📦 Prerequisites

Make sure you have the following installed:

- Python 3.10+
- MySQL Server
- Redis
- AWS CLI (for deployment, optional)

### Step-by-Step Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/daniell-olaitan/portfolio.git
   cd portfolio
   ```

2. **Set up environment variables**:
   - Copy the sample `.env` file and fill in the necessary variables.
   ```bash
   cp .env.sample .env
   ```

3. **Create and activate a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On macOS/Linux
   venv\Scripts\activate     # On Windows
   ```

4. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

5. **Run the project**:
   ```bash
   python portfolio.py
   ```

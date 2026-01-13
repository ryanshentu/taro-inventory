# 🍦 Taro: Cloud Inventory Management System

> A full-stack inventory tracking application built with **React**, **FastAPI**, and **AWS RDS**.

![Project Status](https://img.shields.io/badge/status-complete-success)
![Python](https://img.shields.io/badge/python-3.13-blue.svg)
![React](https://img.shields.io/badge/react-18-blue)
![AWS](https://img.shields.io/badge/AWS-RDS-orange)

---

## 🏗 Architecture
This project is designed as a cloud-native application using a **CI/CD pipeline**.

![Taro Inventory Dashboard](./dashboard.png)

```mermaid
graph LR
    User["User / Browser"] -- HTTPS --> Frontend["React Frontend (Render)"]
    Frontend -- JSON API --> Backend["FastAPI Backend (Render)"]
    Backend -- SQLAlchemy --> Database[("PostgreSQL Database (AWS RDS)")]
```

* **Frontend:** React.js hosted on Render.
* **Backend:** Python FastAPI hosted on Render.
* **Database:** PostgreSQL hosted on **Amazon Web Services (AWS RDS)** in `us-east-2`.
* **DevOps:** Automated deployments triggered by Git pushes.

---

## ✨ Features
* **Real-time Inventory:** Fetches live data from the AWS Cloud database.
* **Smart Alerts:** Backend logic checks stock levels and triggers warnings when inventory drops below the threshold.
* **RESTful API:** Full CRUD capabilities for Ingredients and Sales.
* **Cloud Persistence:** Data remains safe in AWS even when the app restarts.

---

## 🛠 Tech Stack

### Backend
* **Framework:** FastAPI (Python)
* **ORM:** SQLAlchemy
* **Validation:** Pydantic
* **Server:** Uvicorn

### Frontend
* **Framework:** React.js
* **Styling:** CSS3

### Infrastructure
* **Cloud Provider:** AWS (RDS for PostgreSQL)
* **Hosting Platform:** Render
* **Version Control:** Git & GitHub

---

## ⚙️ Local Setup
To run this project on your own machine:

### 1. Backend Setup
```bash
# Clone the repo
git clone https://github.com/YOUR_USERNAME/taro-project.git
cd taro-project

# Create virtual environment
python -m venv venv
source venv/bin/activate  # (Windows: venv\Scripts\activate)

# Install dependencies
pip install -r requirements.txt

# Create .env file with your DB credentials
# Format: postgresql://user:pass@localhost/dbname
echo "DATABASE_URL=postgresql://postgres:password@localhost/taro_db" > .env

# Run the server
uvicorn main:app --reload
```

### 2. Frontend Setup
```bash
cd frontend
npm install
npm start
```

---

## 📡 API Endpoints

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/inventory` | Returns list of all ingredients and quantities |
| `POST` | `/ingredients` | Adds a new ingredient to the database |
| `POST` | `/sale` | Deducts stock and checks for low-inventory alerts |
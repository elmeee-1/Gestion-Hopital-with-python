# 🏥 Gestion Hospital

> A full-stack hospital management web application built with **Python / Flask** and vanilla **HTML/CSS/JS** — deployed live on PythonAnywhere.

[![Live Demo](https://img.shields.io/badge/Live%20Demo-elmehdi.pythonanywhere.com-1a6fa8?style=for-the-badge&logo=python&logoColor=white)](https://elmehdi.pythonanywhere.com/)
[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat&logo=python&logoColor=white)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-3.x-black?style=flat&logo=flask)](https://flask.palletsprojects.com/)
[![License](https://img.shields.io/badge/License-MIT-green?style=flat)](LICENSE)

---

## ✨ Features

| Feature | Description |
|---|---|
| 🧑‍⚕️ **Patient Management** | Add, edit, and delete patients with record number validation and duplicate prevention |
| 👨‍⚕️ **Doctor Management** | Manage doctors and head physicians with specialty and department tracking |
| 💬 **Consultations** | Record consultations between doctors and patients with a running counter |
| 🔭 **Supervision** | Assign a head physician to supervise regular doctors in their department |
| 📊 **Statistics** | Live dashboard showing totals and recent activity |
| 💾 **JSON Persistence** | All data is saved to `data.json` and reloaded automatically on startup |

---

## 🖼️ Preview

> Live at → **[elmehdi.pythonanywhere.com](https://elmehdi.pythonanywhere.com/)**

The interface is a single-page app with 5 tabs: Patients, Doctors, Consultations, Supervision, and Statistics — no external CSS framework, fully custom styling using CSS variables for easy theming.

---

## 🏗️ Project Structure

```
Gestion-Hopital-with-python/
│
├── app.py              # Flask app — all REST API routes
├── models.py           # OOP class hierarchy (Person, Patient, Doctor, HeadDoctor, DataStore)
├── data.json           # JSON persistence file (auto-created on first run)
│
└── templates/
    └── index.html      # Single-page frontend (HTML + CSS + JS)
```

---

## 🧬 Class Hierarchy

```
Person
├── Patient       (name, age, record_number, illness, phone)
└── Doctor        (name, age, specialty, consultations)
    └── HeadDoctor  (+ department)
```

All classes use Python `@property` decorators with input validation. `DataStore` handles JSON serialization and deserialization via static methods.

---

## 🔌 REST API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/patients` | List all patients |
| `POST` | `/api/patients` | Add a new patient |
| `PUT` | `/api/patients/<record>` | Update an existing patient |
| `DELETE` | `/api/patients/<record>` | Delete a patient |
| `GET` | `/api/doctors` | List all doctors |
| `POST` | `/api/doctors` | Add a doctor or head doctor |
| `PUT` | `/api/doctors/<idx>` | Update a doctor |
| `DELETE` | `/api/doctors/<idx>` | Delete a doctor |
| `POST` | `/api/consult` | Record a consultation |
| `POST` | `/api/supervise` | Record a supervision |
| `GET` | `/api/stats` | Get statistics summary |

---

## 🚀 Run Locally

### 1. Clone the repo

```bash
git clone https://github.com/elmeee-1/Gestion-Hopital-with-python.git
cd Gestion-Hopital-with-python
```

### 2. Create a virtual environment

```bash
python -m venv venv
source venv/bin/activate        # macOS / Linux
venv\Scripts\activate           # Windows
```

### 3. Install dependencies

```bash
pip install flask
```

### 4. Run the app

```bash
python app.py
```

Open your browser at **[http://127.0.0.1:5000](http://127.0.0.1:5000)**

---

## ☁️ Deployment (PythonAnywhere)

This app is deployed on [PythonAnywhere](https://www.pythonanywhere.com/) as a WSGI application.

**WSGI config:**

```python
import sys
sys.path.insert(0, '/home/elmehdi/Gestion-Hopital-with-python')
from app import app as application
```

> `data.json` is stored in the project root and persists across all requests.

---

## 📚 Concepts Demonstrated

This project was built as part of an **Object-Oriented Programming (OOP)** course at **Faculty of Sciences Semlalia — Cadi Ayyad University, Marrakech, Morocco**.

It covers:

- **Encapsulation** — private attributes with `@property` / setter validation
- **Inheritance** — `HeadDoctor` extends `Doctor` extends `Person`
- **Static methods** — `DataStore.save()` / `DataStore.load()`
- **Input validation** — age range checks, non-empty fields, unique record numbers
- **REST API design** with Flask
- **Frontend ↔ Backend** communication via `fetch()` and JSON
- **Data persistence** using JSON (no database required)

---

## 👤 Author

**Elmehdi Elmellouki**  
Student at the Faculty of Sciences Semlalia, Cadi Ayyad University — Marrakech, Morocco

[![GitHub](https://img.shields.io/badge/GitHub-elmeee--1-181717?style=flat&logo=github)](https://github.com/elmeee-1)

---

## 📄 License

This project is open source under the [MIT License](LICENSE).

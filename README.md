# 🚀 BikeTracker

A role-based **Vehicle Service Management System** built using Django to manage service records, track maintenance, and send automated SMS alerts.

---

## 🔥 Features

- 🔐 Role-based authentication  
  - Admin / Manager  
  - Associate  
  - Service Incharge  

- 📊 Dashboard for each role  
- 🛠 Under Maintenance tracking  
- ⏰ Service Due alerts  
- 📩 SMS notifications using Twilio  
- 📋 Full CRUD operations for service records  

---

## 🛠 Tech Stack

- **Backend:** Python, Django  
- **Frontend:** HTML, CSS  
- **Database:** SQLite  
- **API:** Twilio SMS API  

---

## ⚙️ Setup Instructions

```bash
# Clone repository
git clone https://github.com/Aniketan-Patil/Bike_Tracker.git

# Navigate to project
cd Bike_Tracker

# Create virtual environment
python3 -m venv venv

# Activate environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run server
python manage.py runserver

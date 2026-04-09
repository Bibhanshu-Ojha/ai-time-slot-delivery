# 🚀 AI-Based Customized Time Slot Delivery System

## 📌 Project Overview

The **AI-Based Customized Time Slot Delivery System** is a web-based application designed to improve last-mile delivery efficiency in traditional postal systems. The system allows users to select preferred delivery time slots and uses basic AI logic to optimize delivery scheduling.

This project aims to reduce failed delivery attempts, improve coordination between customers and delivery staff, and enhance overall delivery performance.

---

## 🎯 Key Features

* ⏰ **Time-Slot Based Delivery** (9–12, 12–3, 3–6, 6–9)
* 🤖 **AI-Based Slot Recommendation**
* 👤 **User Registration & Login System**
* 📦 **Parcel Booking & Tracking**
* 🧑‍💼 **Admin Panel for Staff Assignment**
* 🚚 **Delivery Staff Dashboard**
* 🔔 **Email Notifications (SMTP - Mailtrap)**
* 📊 **System Analytics Dashboard**
* 🔐 **Role-Based Access Control**

---

## 🛠️ Tech Stack

### 💻 Backend

* Python
* Flask Framework

### 🌐 Frontend

* HTML
* CSS
* JavaScript

### 🗄️ Database

* MySQL

### 🤖 AI / Logic

* Rule-based AI (slot recommendation)

### 📧 Notifications

* SMTP (Mailtrap for testing)

---

## ⚙️ System Modules

* User Management Module
* Parcel Management Module
* Time Slot Management Module
* AI Scheduling Module
* Notification Module
* Delivery Personnel Module
* Database Management Module

---

## 🧩 How It Works

1. User registers and logs into the system
2. User books a parcel and selects a delivery time slot
3. AI suggests the best slot based on availability/history
4. Admin assigns delivery staff
5. Staff receives delivery list and updates status
6. User receives email notifications
7. Parcel status is updated in real-time

---

## 🖥️ Installation & Setup

### 1️⃣ Clone the repository

```bash
git clone https://github.com/your-username/ai-time-slot-delivery.git
cd ai-time-slot-delivery
```

### 2️⃣ Create virtual environment

```bash
python -m venv venv
venv\Scripts\activate   # Windows
```

### 3️⃣ Install dependencies

```bash
pip install flask mysql-connector-python
```

### 4️⃣ Setup Database

* Create MySQL database:

```sql
CREATE DATABASE time_slot_delivery;
```

* Import required tables (users, parcels, time_slots)

### 5️⃣ Run the application

```bash
python app.py
```

### 6️⃣ Open in browser

```
http://127.0.0.1:5000
```

---
### 📌 Database Setup Instructions

### 1️⃣ Create Database

Open MySQL and run:

```sql
CREATE DATABASE time_slot_delivery;
USE time_slot_delivery;
```

---

### 2️⃣ Create Tables

#### 👤 Users Table

```sql
CREATE TABLE users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    full_name VARCHAR(100),
    email VARCHAR(100) UNIQUE,
    password VARCHAR(255),
    role ENUM('User', 'Admin', 'Staff')
);
```

---

#### 📦 Parcels Table

```sql
CREATE TABLE parcels (
    parcel_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    parcel_name VARCHAR(255),
    slot_id INT,
    staff_id INT NULL,
    status VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);
```

---

#### ⏰ Time Slots Table

```sql
CREATE TABLE time_slots (
    slot_id INT AUTO_INCREMENT PRIMARY KEY,
    slot_label VARCHAR(50),
    max_capacity INT,
    current_load INT DEFAULT 0
);
```

---

### 3️⃣ Insert Default Time Slots

```sql
INSERT INTO time_slots (slot_label, max_capacity, current_load) VALUES
('9-12', 5, 0),
('12-3', 5, 0),
('3-6', 5, 0),
('6-9', 5, 0);
```

---

### 4️⃣ (Optional) Create Admin & Staff

```sql
INSERT INTO users (full_name, email, password, role) VALUES
('Admin User', 'admin@test.com', SHA2('admin123',256), 'Admin'),
('Staff Member', 'staff@test.com', SHA2('staff123',256), 'Staff');
```

---

### 5️⃣ Update DB Connection in Code

In your `app.py`:

```python
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="your_password",
    database="time_slot_delivery"
)
```

---

# 🔥 Bonus 

👉 System logic depends on:

* Slot capacity check
* AI recommendation
* Staff assignment

So database must include:

* ✔ `current_load`
* ✔ `max_capacity`
* ✔ `staff_id`
---
## 📧 SMTP (Email Notification Setup)

The system uses SMTP (Simple Mail Transfer Protocol) to send email notifications when parcel status is updated.

### 🔹 Using Mailtrap (Recommended for Testing)

1. Go to https://mailtrap.io and create an account
2. Navigate to **Email Testing → Inboxes**
3. Open your inbox and copy SMTP credentials

---

### 🔹 Update SMTP Configuration in `app.py`

Replace with your Mailtrap credentials:

```python
SMTP_SERVER = "sandbox.smtp.mailtrap.io"
SMTP_PORT = 2525
SMTP_USER = "YOUR_MAILTRAP_USERNAME"
SMTP_PASS = "YOUR_MAILTRAP_PASSWORD"
```

---

### 🔹 How It Works

* When delivery status is updated (e.g., Delivered)
* The system triggers an email function
* Email is sent to the user via SMTP
* Mail appears in your Mailtrap inbox

---

### ⚠️ Notes

* Mailtrap is used for testing (emails are NOT sent to real users)
* For real deployment, you can replace Mailtrap with:

  * Gmail SMTP
  * Outlook SMTP

---

### 🔥 Optional (Gmail SMTP Example)

```python
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SMTP_USER = "your_email@gmail.com"
SMTP_PASS = "your_app_password"
```

⚠️ You must use an **App Password**, not your Gmail password.

---
## 🔑 Default Roles

* **User** → Book parcels
* **Admin** → Assign delivery staff
* **Staff** → Update delivery status

---

## 📊 Screenshots (Add These)

* Home Page
* Login/Register
* Parcel Booking
* Time Slot Selection (AI Suggestion)
* Admin Dashboard
* Staff Dashboard
* Tracking Page

---

## 🚧 Limitations

* Basic AI (not advanced ML)
* No real-time GPS tracking
* Requires internet connection
* SMS/email cost in real deployment

---

## 🔮 Future Improvements

* Advanced AI/ML models
* Mobile application (Android/iOS)
* Real-time GPS tracking
* Cloud deployment
* WhatsApp/SMS integration

---

## 📚 References

* Flask Documentation
* MySQL Documentation
* Scikit-learn
* SMTP (Mailtrap)

---

## 👨‍💻 Author

Bibhanshu Ojha
Rutik Sahoo
Lippsha Rani Pradhan
Final Year Project
Gandhi Engineering College

---

## ⭐ Contribution

Feel free to fork this repository and improve the system!

---

# 🎯 DONE

	
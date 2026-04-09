
# 🚀 AI-Based Customized Time Slot Delivery System

A smart web-based application designed to improve last-mile delivery.
It allows users to select delivery time slots and uses rule-based AI for better scheduling.
This helps reduce failed deliveries and improves coordination.

---

## ✨ Key Features

* ⏰ Time-Slot Based Delivery (9–12, 12–3, 3–6, 6–9)
* 🤖 AI Slot Recommendation (based on history and load)
* 📦 Parcel Tracking (real-time status updates)
* 🔔 Email Notifications (using SMTP via Mailtrap)
* 🔐 Role-Based Access (User, Admin, Staff)
* 📊 Admin Analytics Dashboard
=======
* **⏰ Time-Slot Based Delivery:** Flexible windows (9–12, 12–3, 3–6, 6–9).
* **🤖 AI Slot Recommendation:** Smart suggestions based on historical data and current load capacity.
* **📦 Parcel Tracking:** Real-time status updates from dispatch to delivery.
* **🔔 Automated Email Notifications:** Integrated SMTP (via Mailtrap) to keep users informed.
* **🔐 Role-Based Access Control:** Dedicated, secure dashboards for Users, Staff, and Admins.
* **📊 Analytics Dashboard:** Comprehensive system overview for administrators.

---

## 🧩 How It Works

1. User registers and logs in
2. User books parcel and selects slot
3. AI suggests best delivery slot
4. Admin assigns delivery staff
5. Staff delivers and updates status
6. User receives email notifications

---

## 🛠️ Tech Stack

| Component     | Technology            |
| ------------- | --------------------- |
| Backend       | Python, Flask         |
| Frontend      | HTML, CSS, JavaScript |
| Database      | MySQL                 |
| AI Logic      | Rule-Based Scheduling |
| Notifications | SMTP (Mailtrap)       |

---

## ⚙️ Installation & Setup

### 1. Clone Repository

```bash
git clone [https://github.com/Bibhanshu-Ojha/ai-time-slot-delivery]
cd ai-time-slot-delivery
````

### 2. Create Virtual Environment

```bash
python -m venv venv
```

Activate:

```bash
venv\Scripts\activate   # Windows
# source venv/bin/activate # Mac/Linux
```

---

### 3. Install Dependencies

```bash
pip install flask mysql-connector-python
```

---

### 4. Configure Database

Update in `app.py`:

```python
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="your_password",
    database="time_slot_delivery"
)
```

---

### 5. Run Project

```bash
python app.py
```

Open in browser:

```
http://127.0.0.1:5000
```

---

## 🗄️ Database Setup

### Create Database

```sql
CREATE DATABASE time_slot_delivery;
USE time_slot_delivery;
```

---

### Create Tables

#### Users

```sql
CREATE TABLE users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    full_name VARCHAR(100),
    email VARCHAR(100) UNIQUE,
    password VARCHAR(255),
    role ENUM('User', 'Admin', 'Staff')
);
```

#### Parcels

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

#### Time Slots

```sql
CREATE TABLE time_slots (
    slot_id INT AUTO_INCREMENT PRIMARY KEY,
    slot_label VARCHAR(50),
    max_capacity INT,
    current_load INT DEFAULT 0
);
```

---

### Insert Default Data

```sql
INSERT INTO time_slots (slot_label, max_capacity, current_load) VALUES
('9-12', 5, 0),
('12-3', 5, 0),
('3-6', 5, 0),
('6-9', 5, 0);
```

```sql
INSERT INTO users (full_name, email, password, role) VALUES
('Admin User', 'admin@test.com', SHA2('admin123',256), 'Admin'),
('Staff Member', 'staff@test.com', SHA2('staff123',256), 'Staff');
```

---

## 📧 Notification Setup (SMTP)

The system uses SMTP to send email notifications.

### Steps:

1. Create account on https://mailtrap.io
2. Go to **Email Testing → Inboxes**
3. Copy credentials

Update in `app.py`:

```python
SMTP_SERVER = "sandbox.smtp.mailtrap.io"
SMTP_PORT = 2525
SMTP_USER = "YOUR_MAILTRAP_USERNAME"
SMTP_PASS = "YOUR_MAILTRAP_PASSWORD"
```

---

## 🔑 Roles

* 👤 User → Book parcel, select slot, track status
* 🧑‍💼 Admin → Assign staff, manage system
* 🚚 Staff → View deliveries, update status

---
=======
  * **👤 User:** Can book parcels, view AI slot suggestions, and track delivery status.
  * **🧑‍💼 Admin:** Manages the system, views analytics, and assigns delivery personnel.
  * **🚚 Staff:** Accesses their daily delivery itinerary and updates parcel statuses.

## 🚧 Limitations

* Uses rule-based AI (not ML)
* No real-time GPS tracking

---

## 🔮 Future Scope

* AI/ML-based prediction
* Mobile app
* GPS tracking
* SMS notifications
* Cloud deployment

---

## 👨‍💻 Authors

Final Year Project – Gandhi Engineering College

* Bibhanshu Ojha
* Rutik Sahoo
* Lippsha Rani Pradhan

---

## ⭐ Contribution

Fork the repository and create a pull request to contribute.
=======
Found a bug or have an idea for an improvement? Feel free to **Fork** this repository, make your changes, and submit a **Pull Request**\!

```
```
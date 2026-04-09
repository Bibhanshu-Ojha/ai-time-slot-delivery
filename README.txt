````markdown
# 🚀 AI-Based Customized Time Slot Delivery System

> A smart, web-based application designed to revolutionize last-mile delivery. By allowing users to select preferred delivery windows and utilizing rule-based AI for optimal scheduling, this system minimizes failed delivery attempts and streamlines coordination between customers, admins, and delivery staff.

---

## ✨ Key Features

* **⏰ Time-Slot Based Delivery:** Flexible windows (9–12, 12–3, 3–6, 6–9).
* **🤖 AI Slot Recommendation:** Smart suggestions based on historical data and current load capacity.
* **📦 Parcel Tracking:** Real-time status updates from dispatch to delivery.
* **🔔 Automated Email Notifications:** Integrated SMTP (via Mailtrap) to keep users informed.
* **🔐 Role-Based Access Control:** Dedicated, secure dashboards for Users, Staff, and Admins.
* **📊 Analytics Dashboard:** Comprehensive system overview for administrators.

---

## 🧩 How It Works

1.  👤 **User Registration:** Customers sign up and log into the portal.
2.  📦 **Parcel Booking:** Users book a shipment and are presented with time slots.
3.  🤖 **AI Optimization:** The system suggests the most efficient delivery window.
4.  🧑‍💼 **Staff Assignment:** Admins review bookings and assign them to available delivery personnel.
5.  🚚 **Delivery Execution:** Staff receive their itineraries and update delivery statuses on the go.
6.  📧 **Real-Time Alerts:** Users receive email notifications at every milestone.

---

## 🛠️ Tech Stack

| Component | Technology |
| :--- | :--- |
| **Backend** | Python, Flask |
| **Frontend** | HTML5, CSS3, JavaScript |
| **Database** | MySQL |
| **AI / Logic** | Rule-Based AI Scheduling & Capacity Checking |
| **Notifications** | SMTP (Mailtrap) |

---

## ⚙️ Installation & Setup

**1. Clone the repository**

```bash
git clone [https://github.com/Bibhanshu-Ojha/ai-time-slot-delivery](https://github.com/Bibhanshu-Ojha/ai-time-slot-delivery)
cd ai-time-slot-delivery
````

**2. Create and activate a virtual environment**

```bash
python -m venv venv
venv\Scripts\activate   # Windows
# source venv/bin/activate # Mac/Linux
```

**3. Install dependencies**

```bash
pip install flask mysql-connector-python
```

**4. Update Database Connection**
In your `app.py`, update the connection string with your MySQL credentials:

```python
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="your_password",
    database="time_slot_delivery"
)
```

**5. Run the Application**

```bash
python app.py
```

*Access the app in your browser at: `http://127.0.0.1:5000`*

-----

## 🗄️ Database Setup

\<details\>
\<summary\>\<b\>Click to expand Database Schema & SQL Commands\</b\>\</summary\>

### 1️⃣ Create Database

```sql
CREATE DATABASE time_slot_delivery;
USE time_slot_delivery;
```

### 2️⃣ Create Tables

**Users Table**

```sql
CREATE TABLE users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    full_name VARCHAR(100),
    email VARCHAR(100) UNIQUE,
    password VARCHAR(255),
    role ENUM('User', 'Admin', 'Staff')
);
```

**Parcels Table**

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

**Time Slots Table**

```sql
CREATE TABLE time_slots (
    slot_id INT AUTO_INCREMENT PRIMARY KEY,
    slot_label VARCHAR(50),
    max_capacity INT,
    current_load INT DEFAULT 0
);
```

### 3️⃣ Insert Default Data

```sql
INSERT INTO time_slots (slot_label, max_capacity, current_load) VALUES
('9-12', 5, 0),
('12-3', 5, 0),
('3-6', 5, 0),
('6-9', 5, 0);

-- Optional: Create default Admin & Staff
INSERT INTO users (full_name, email, password, role) VALUES
('Admin User', 'admin@test.com', SHA2('admin123',256), 'Admin'),
('Staff Member', 'staff@test.com', SHA2('staff123',256), 'Staff');
```

🔥 **Logic Note:** The AI recommendation engine relies on `max_capacity`, `current_load`, and `staff_id` to prevent overbooking and optimize delivery routes\!

\</details\>

-----

## 📧 Notification Setup (SMTP)

The system uses SMTP to trigger emails upon parcel status updates. **Mailtrap** is used for safe, sandbox testing.

1.  Create a free account at [Mailtrap](https://mailtrap.io).
2.  Go to **Email Testing → Inboxes** and copy your credentials.
3.  Update `app.py` with your credentials:

<!-- end list -->

```python
SMTP_SERVER = "sandbox.smtp.mailtrap.io"
SMTP_PORT = 2525
SMTP_USER = "YOUR_MAILTRAP_USERNAME"
SMTP_PASS = "YOUR_MAILTRAP_PASSWORD"
```

> **⚠️ Note on Production:** For real-world deployment, replace Mailtrap with a live SMTP provider (like Gmail or Outlook). If using Gmail, ensure you generate an **App Password** instead of using your primary account password.

-----

## 🔑 Roles & Access

  * **👤 User:** Can book parcels, view AI slot suggestions, and track delivery status.
  * **🧑‍💼 Admin:** Manages the system, views analytics, and assigns delivery personnel.
  * **🚚 Staff:** Accesses their daily delivery itinerary and updates parcel statuses.

-----

## 🚧 Limitations & 🔮 Future Scope

**Current Limitations:**

  * Uses rule-based AI logic rather than predictive Machine Learning models.
  * Lacks real-time GPS hardware integration.

**Future Improvements:**

  * [ ] Integrate predictive ML algorithms for advanced route optimization.
  * [ ] Build cross-platform mobile applications (Android/iOS).
  * [ ] Implement live GPS tracking via Google Maps API.
  * [ ] Integrate WhatsApp/SMS notifications.
  * [ ] Deploy to scalable cloud infrastructure (AWS/GCP).

-----

## 👨‍💻 Authors

**Final Year Project** | *Gandhi Engineering College*

  * **Bibhanshu Ojha**
  * **Rutik Sahoo**
  * **Lippsha Rani Pradhan**

-----

### ⭐ Contribution

Found a bug or have an idea for an improvement? Feel free to **Fork** this repository, make your changes, and submit a **Pull Request**\!

```
```

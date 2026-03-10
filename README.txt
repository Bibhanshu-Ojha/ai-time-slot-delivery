AI-Based Customized Time Slot Delivery System

---

Project Description

This project is a web-based delivery management system that allows users to book parcels and choose a preferred delivery time slot. The system helps reduce failed delivery attempts by allowing recipients to select when they will be available to receive their parcel.

The system has three main roles:
• User – can book parcels and select time slots
• Admin – can assign delivery staff to parcels
• Staff – can update delivery status

The system also manages slot capacity to avoid overbooking.

---

Technologies Used

Python
Flask (Web Framework)
MySQL (Database)
HTML and CSS (Frontend)
Git and GitHub (Version Control)

---

Step 1 — Download the Project

Clone the repository from GitHub:

git clone https://github.com/Bibhanshu-Ojha/ai-time-slot-delivery.git

Move into the project folder:

cd ai-time-slot-delivery

---

Step 2 — Create a Virtual Environment

It is recommended to use a Virtual Environment so that project dependencies do not conflict with other Python projects on your system.

Create the virtual environment:

python -m venv venv

---

Step 3 — Activate the Virtual Environment

Windows:

venv\Scripts\activate

Mac / Linux:

source venv/bin/activate

After activation your terminal will show (venv).

---

Step 4 — Install Project Dependencies

Install all required libraries using:

pip install -r requirements.txt

If requirements.txt is not available, install manually:

pip install flask
pip install mysql-connector-python
pip install flask-bcrypt

---

Step 5 — Setup the Database

Open MySQL and run the following commands.

Create the database:

CREATE DATABASE time_slot_delivery;

Use the database:

USE time_slot_delivery;

---

Create Users Table

CREATE TABLE users (
user_id INT AUTO_INCREMENT PRIMARY KEY,
full_name VARCHAR(100),
email VARCHAR(100),
password VARCHAR(100),
role VARCHAR(20)
);

---

Create Time Slots Table

CREATE TABLE time_slots (
slot_id INT AUTO_INCREMENT PRIMARY KEY,
slot_label VARCHAR(20),
max_capacity INT,
current_load INT
);

---

Create Parcels Table

CREATE TABLE parcels (
parcel_id INT AUTO_INCREMENT PRIMARY KEY,
user_id INT,
parcel_name VARCHAR(100),
slot_id INT,
status VARCHAR(50),
staff_id INT
);

---

Insert Default Delivery Slots

INSERT INTO time_slots (slot_label, max_capacity, current_load) VALUES
('9-12',5,0),
('12-3',5,0),
('3-6',5,0),
('6-9',5,0);

---

Step 6 — Configure Database Connection

Open the file app.py and update database credentials if needed:

db = mysql.connector.connect(
host="localhost",
user="root",
password="YOUR_PASSWORD",
database="time_slot_delivery"
)

---

Step 7 — Run the Project

Start the Flask application:

python app.py

---

Step 8 — Open the Application

Open a web browser and go to:

http://127.0.0.1:5000

---

How to Use the System

1. Register three types of accounts:
   • User
   • Admin
   • Staff

2. Login as User
   • Book a parcel
   • Select a delivery time slot

3. Login as Admin
   • Assign delivery staff to parcels

4. Login as Staff
   • Update delivery status

5. Login again as User
   • Check parcel delivery status

---

Project Workflow

User registers → User books parcel → Selects delivery slot
Admin assigns delivery staff → Staff delivers parcel → Staff updates status → User views final delivery status

---

Future Improvements

AI-based time slot prediction
SMS notifications for delivery updates
Route optimization for delivery staff
Advanced admin analytics and reports

---

Author

Bibhanshu Ojha

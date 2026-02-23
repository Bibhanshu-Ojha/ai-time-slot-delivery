from flask import Flask, render_template, request
from flask import session
import mysql.connector

app = Flask(__name__)
app.secret_key = "supersecretkey"

# Database connection
db = mysql.connector.connect(
    host="localhost", user="root", password="@ojha", database="time_slot_delivery"
)


# homepage route
@app.route("/")
def home():
    return render_template("home.html")


# registration route
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]
        role = request.form["role"]

        cursor = db.cursor()
        cursor.execute(
            "INSERT INTO users (full_name, email, password, role) VALUES (%s, %s, %s, %s)",
            (name, email, password, role),
        )
        db.commit()

        return "User Registered Successfully"

    return render_template("register.html")


# login route
@app.route("/login", methods=["GET", "POST"])
def login():
    cursor = db.cursor()

    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        cursor.execute(
            "SELECT user_id, role FROM users WHERE email=%s AND password=%s",
            (email, password),
        )
        user = cursor.fetchone()

        if user:
            session["user_id"] = user[0]
            session["role"] = user[1]
            return "Login Successful"
        else:
            return "Invalid Credentials"

    return render_template("login.html")


# booking route
@app.route("/book", methods=["GET", "POST"])
def book_parcel():
    cursor = db.cursor()

    if request.method == "POST":
        parcel_name = request.form["parcel_name"]
        slot_id = request.form["slot_id"]
        if "user_id" not in session:
            return "Please Login First"
        user_id = session["user_id"]

        # Check slot capacity
        cursor.execute(
            "SELECT max_capacity, current_load FROM time_slots WHERE slot_id=%s",
            (slot_id,),
        )
        slot = cursor.fetchone()

        if slot[1] >= slot[0]:
            return "Slot Full! Choose another slot."

        # Insert parcel
        cursor.execute(
            "INSERT INTO parcels (user_id, parcel_name, slot_id, status) VALUES (%s, %s, %s, %s)",
            (user_id, parcel_name, slot_id, "Booked"),
        )
        db.commit()

        # Update slot load
        cursor.execute(
            "UPDATE time_slots SET current_load = current_load + 1 WHERE slot_id=%s",
            (slot_id,),
        )
        db.commit()

        return "Parcel Booked Successfully!"

    # Fetch slots for dropdown
    cursor.execute("SELECT * FROM time_slots")
    slots = cursor.fetchall()

    return render_template("book_parcel.html", slots=slots)


# admin route to view all bookings
@app.route("/admin_assign", methods=["GET", "POST"])
def admin_assign():
    cursor = db.cursor()

    if request.method == "POST":
        parcel_id = request.form["parcel_id"]
        staff_id = request.form["staff_id"]

        cursor.execute(
            "UPDATE parcels SET staff_id=%s WHERE parcel_id=%s", (staff_id, parcel_id)
        )
        db.commit()

    cursor.execute("SELECT * FROM parcels WHERE staff_id IS NULL")
    parcels = cursor.fetchall()

    cursor.execute("SELECT * FROM staff")
    staff_list = cursor.fetchall()

    return render_template("admin_assign.html", parcels=parcels, staff_list=staff_list)


# staff route to view assigned parcels
@app.route("/staff_dashboard", methods=["GET", "POST"])
def staff_dashboard():
    cursor = db.cursor()

    if request.method == "POST":
        parcel_id = request.form["parcel_id"]
        status = request.form["status"]

        cursor.execute(
            "UPDATE parcels SET status=%s WHERE parcel_id=%s", (status, parcel_id)
        )
        db.commit()

    staff_id = 1  # demo hardcoded staff login (we improve later)

    cursor.execute("SELECT * FROM parcels WHERE staff_id=%s", (staff_id,))
    parcels = cursor.fetchall()

    return render_template("staff_dashboard.html", parcels=parcels)


# customer route to view their bookings
@app.route("/my_parcels")
def my_parcels():
    if "user_id" not in session:
        return "Login first"

    cursor = db.cursor()
    cursor.execute("SELECT * FROM parcels WHERE user_id=%s", (session["user_id"],))
    parcels = cursor.fetchall()

    return str(parcels)


if __name__ == "__main__":
    print("Registered Routes:", app.url_map)
    app.run(debug=True)

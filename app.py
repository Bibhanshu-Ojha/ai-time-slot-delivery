from flask import Flask, redirect, render_template, request
from flask import session
import mysql.connector

app = Flask(__name__)
app.secret_key = "supersecretkey"

# Database connection
db = mysql.connector.connect(
    host="localhost", user="root", password="@ojha", database="time_slot_delivery"
)


# (/)homepage route
@app.route("/")
def home():
    return render_template("home.html")


# (/register) route
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

        return redirect("/")

    return render_template("register.html")


# (/login) route
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
            if user[1] == "User":
                return redirect("/book")
            elif user[1] == "Admin":
                return redirect("/admin_assign")
            elif user[1] == "Staff":
                return redirect("/staff_dashboard")
        else:
            return "Invalid Credentials"

    return render_template("login.html")


# (/book) route
@app.route("/book", methods=["GET", "POST"])
def book_parcel():

    if "user_id" not in session or session["role"] != "User":
        return "Unauthorized Access"

    cursor = db.cursor()

    if request.method == "POST":
        parcel_name = request.form["parcel_name"]
        slot_id = request.form["slot_id"]
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

        return redirect("/my_parcels")

    # Fetch slots for dropdown
    # cursor.execute("SELECT * FROM time_slots")
    # slots = cursor.fetchall()
    user_id = session["user_id"]

    # find most used slot for this user
    cursor.execute(
        "SELECT slot_id, COUNT(*) as count FROM parcels WHERE user_id=%s GROUP BY slot_id ORDER BY count DESC LIMIT 1",
        (user_id,),
    )
    suggested = cursor.fetchone()

    # fetch all slots
    cursor.execute("SELECT * FROM time_slots")
    slots = cursor.fetchall()

    suggested_slot = suggested[0] if suggested else None

    return render_template(
        "book_parcel.html", slots=slots, suggested_slot=suggested_slot
    )


# (/admin_assign)to view all bookings
@app.route("/admin_assign", methods=["GET", "POST"])
def admin_assign():

    if "role" not in session or session["role"] != "Admin":
        return "Unauthorized Access"

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

    cursor.execute("SELECT user_id, full_name FROM users WHERE role='Staff'")
    staff_list = cursor.fetchall()

    return render_template("admin_assign.html", parcels=parcels, staff_list=staff_list)


# (/staff_dashboard) to view assigned parcels
@app.route("/staff_dashboard", methods=["GET", "POST"])
def staff_dashboard():

    if "user_id" not in session or session["role"] != "Staff":
        return "Unauthorized Access"

    cursor = db.cursor()
    staff_id = session["user_id"]

    if request.method == "POST":
        parcel_id = request.form["parcel_id"]
        status = request.form["status"]

        cursor.execute(
            "UPDATE parcels SET status=%s WHERE parcel_id=%s", (status, parcel_id)
        )
        db.commit()

    cursor.execute("SELECT * FROM parcels WHERE staff_id=%s", (staff_id,))
    parcels = cursor.fetchall()

    return render_template("staff_dashboard.html", parcels=parcels)


# (/my_parcels)customer route to view their bookings
@app.route("/my_parcels")
def my_parcels():
    if "user_id" not in session or session["role"] != "User":
        return "Unauthorized Access"

    cursor = db.cursor()
    cursor.execute("SELECT * FROM parcels WHERE user_id=%s", (session["user_id"],))
    parcels = cursor.fetchall()

    return render_template("my_parcels.html", parcels=parcels)


# (/logout) route to clear session
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


if __name__ == "__main__":
    print("Registered Routes:", app.url_map)
    app.run(debug=True)

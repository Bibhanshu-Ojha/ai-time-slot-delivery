from flask import Flask, flash, redirect, render_template, request, session
import mysql.connector
import hashlib

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
        password = hashlib.sha256(request.form["password"].encode()).hexdigest()
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
    if request.method == "POST":
        email = request.form["email"]
        password = hashlib.sha256(request.form["password"].encode()).hexdigest()

        cursor = db.cursor()
        cursor.execute(
            "SELECT user_id, role FROM users WHERE email=%s AND password=%s",
            (email, password),
        )
        user = cursor.fetchone()

        if user:
            session["user_id"] = user[0]
            session["role"] = user[1]
            flash("Welcome back! Login successful.", "success")  # Success message
            return redirect("/")
        else:
            flash(
                "Invalid email or password. Please try again.", "danger"
            )  # Error message
            return render_template("login.html")

    return render_template("login.html")


# (/book) route
@app.route("/book", methods=["GET", "POST"])
def book_parcel():
    if "user_id" not in session or session.get("role") != "User":
        flash("Please log in as a customer to book a parcel.", "danger")
        return redirect("/login")

    cursor = db.cursor()
    user_id = session["user_id"]

    if request.method == "POST":
        parcel_name = request.form["parcel_name"]
        slot_id = request.form["slot_id"]

        # 1. Validation: Prevent empty names
        if not parcel_name.strip():
            flash("Parcel name cannot be empty!", "danger")
            return redirect("/book")

        # 2. Check slot capacity
        cursor.execute(
            "SELECT max_capacity, current_load FROM time_slots WHERE slot_id=%s",
            (slot_id,),
        )
        slot = cursor.fetchone()

        if not slot or slot[1] >= slot[0]:
            flash("Slot Full! Our AI suggests trying a different window.", "danger")
            return redirect("/book")

        # 3. Insert and Update
        cursor.execute(
            "INSERT INTO parcels (user_id, parcel_name, slot_id, status) VALUES (%s, %s, %s, %s)",
            (user_id, parcel_name, slot_id, "Booked"),
        )
        cursor.execute(
            "UPDATE time_slots SET current_load = current_load + 1 WHERE slot_id=%s",
            (slot_id,),
        )
        db.commit()

        flash("Parcel successfully scheduled!", "success")
        return redirect("/my_parcels")

    # --- AI RECOMMENDATION ENGINE START ---

    # Step A: Find the user's historical favorite
    cursor.execute(
        """
        SELECT slot_id, COUNT(*) as count 
        FROM parcels WHERE user_id=%s 
        GROUP BY slot_id ORDER BY count DESC LIMIT 1
    """,
        (user_id,),
    )
    favorite = cursor.fetchone()

    suggested_slot = None
    recommendation_type = ""

    if favorite:
        # Step B: Check if their favorite is actually available
        cursor.execute(
            "SELECT max_capacity, current_load FROM time_slots WHERE slot_id=%s",
            (favorite[0],),
        )
        fav_data = cursor.fetchone()

        if fav_data and fav_data[1] < fav_data[0]:
            suggested_slot = favorite[0]
            recommendation_type = "Based on your history"

    # Step C: If no favorite OR favorite is full, suggest the least busy slot (Load Balancing)
    if not suggested_slot:
        cursor.execute(
            "SELECT slot_id FROM time_slots WHERE current_load < max_capacity ORDER BY current_load ASC LIMIT 1"
        )
        best_alt = cursor.fetchone()
        if best_alt:
            suggested_slot = best_alt[0]
            recommendation_type = "Optimized for speed (Lowest load)"

    # Fetch all slots for the dropdown
    cursor.execute("SELECT * FROM time_slots")
    slots = cursor.fetchall()

    return render_template(
        "book_parcel.html",
        slots=slots,
        suggested_slot=suggested_slot,
        recommendation_type=recommendation_type,
    )


# (/admin_assign)to view all bookings
@app.route("/admin_assign", methods=["GET", "POST"])
def admin_assign():

    if "user_id" not in session or session.get("role") != "Admin":
        flash("Access Denied: Admin privileges required.", "danger")
        return redirect("/login")

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

    if "user_id" not in session or session.get("role") != "Staff":
        flash("Access Denied: Staff account required.", "danger")
        return redirect("/login")

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

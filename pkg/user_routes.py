import os
import sqlite3
from datetime import datetime
from flask import (
    render_template, request, redirect, flash, url_for, session
)
from flask_mail import Mail
from flask_bcrypt import Bcrypt
from pkg import app
from instance import config
from pkg.model import db, Users,Shipment, State,Lga


# -------------------- CONFIG --------------------
bcrypt = Bcrypt(app)

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'oluwaseunoyediran641@gmail.com'
app.config['MAIL_PASSWORD'] = 'rvla jpvq rjbq oyce'
app.config['ADMIN_EMAIL'] = config.ADMIN_EMAIL
DATABASE_NAME = 'logistics_db'

mail = Mail(app)


# -------------------- ERROR HANDLERS --------------------
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache,no-store, must-revalidate"
    return response

@app.errorhandler(404)
def page_not_found(e):
    return render_template('User/404error.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    app.logger.error(f"Internal Server Error: {e}")
    return render_template('User/500.html'), 500

@app.errorhandler(503)
def service_unavailable(e):
    return render_template('User/503.html'), 503


# -------------------- DB CONNECTION --------------------
def get_db_connection():
    conn = sqlite3.connect(DATABASE_NAME)
    conn.row_factory = sqlite3.Row
    return conn



# -------------------- ROUTES --------------------
@app.route('/')
def index():
    return render_template('User/index.html', title='Home')

@app.route('/about/')
def about():
    return render_template('User/about.html', title='About Us')

@app.route('/services/')
def services():
    return render_template('User/services.html', title='Our Services')


# -------------------- AUTH --------------------
@app.route("/auth/")
def auth():
    return render_template("User/auth.html")  # login/register combined page


@app.route("/register/", methods=["POST"])
def register():
    fullname = request.form['fullname']
    email = request.form['email']
    phone = request.form['phone']
    password = request.form['password']

    # Check if user already exists
    existing_user = Users.query.filter_by(email=email).first()
    if existing_user:
        flash("Email already exists! Please login.", "danger")
        return redirect(url_for("auth"))

    # Hash password
    hashed_pw = bcrypt.generate_password_hash(password).decode('utf-8')

    # Create new user
    new_user = Users(fullname=fullname, email=email, phone=phone, password=hashed_pw)
    db.session.add(new_user)
    db.session.commit()

    flash("Registration successful! Please login.", "success")
    return redirect(url_for("auth"))


@app.route("/login/", methods=["POST"])
def login():
    email = request.form['email']
    password = request.form['password']

    user = Users.query.filter_by(email=email).first()
    if user and bcrypt.check_password_hash(user.password, password):
        session['user_id'] = user.id
        session['fullname'] = user.fullname
        flash("Login successful!", "success")
        return redirect(url_for("dashboard"))
    else:
        flash("Invalid email or password!", "danger")
        return redirect(url_for("auth"))


@app.route("/dashboard/")
def dashboard():
    if "user_id" not in session:
        flash("Please login first!", "warning")
        return redirect(url_for("auth"))
    return render_template("User/dashboard.html", fullname=session['fullname'])

from flask import jsonify
@app.route("/book-shipment/", methods=["GET", "POST"])
def book_shipment():
    if "user_id" not in session:
        flash("Please login first!", "warning")
        return redirect(url_for("auth"))

    # Get all states for dropdowns
    states = State.query.order_by(State.state_name).all()

    if request.method == "POST":
        user_id = session["user_id"]

        sender_name = request.form.get("sender_name")
        sender_phone = request.form.get("sender_phone")
        sender_email = request.form.get("sender_email")
        sender_address = request.form.get("sender_address")
        sender_city = request.form.get("sender_city")
        sender_state = request.form.get("sender_state")
        sender_lga = request.form.get("sender_lga")

        receiver_name = request.form.get("receiver_name")
        receiver_phone = request.form.get("receiver_phone")
        receiver_email = request.form.get("receiver_email")
        receiver_address = request.form.get("receiver_address")
        receiver_city = request.form.get("receiver_city")
        receiver_state = request.form.get("receiver_state")
        receiver_lga = request.form.get("receiver_lga")

        package_type = request.form.get("package_type")
        weight = request.form.get("weight")
        pickup_date = request.form.get("pickup_date")
        description = request.form.get("description")
        voucher = request.form.get("voucher")

        # Create shipment
        new_shipment = Shipment(
            user_id=user_id,
            sender_name=sender_name,
            sender_phone=sender_phone,
            sender_email=sender_email,
            sender_address=sender_address,
            sender_city=sender_city,
            sender_state=sender_state,
            sender_lga=sender_lga,
            receiver_name=receiver_name,
            receiver_phone=receiver_phone,
            receiver_email=receiver_email,
            receiver_address=receiver_address,
            receiver_city=receiver_city,
            receiver_state=receiver_state,
            receiver_lga=receiver_lga,
            package_type=package_type,
            weight=weight,
            pickup_date=pickup_date,
            notes=description,
            voucher_code=voucher
        )

        db.session.add(new_shipment)
        db.session.commit()

        flash("Shipment booked successfully!", "success")
        return redirect(url_for("dashboard"))

    return render_template("User/shipment.html", states=states)



# AJAX route to get LGAs by state
@app.route('/get_lgas/', methods=['POST'])
def get_lgas():
    state_id = request.form.get('state_id')
    if not state_id:
        return jsonify([])
    lgas = Lga.query.filter_by(state_id=state_id).order_by(Lga.lga_name).all()
    lga_list = [{'id': lga.lga_id, 'name': lga.lga_name} for lga in lgas]
    return jsonify(lga_list)

@app.route("/logout/")
def logout():
    session.clear()
    flash("You have been logged out!", "info")
    return redirect(url_for("auth"))

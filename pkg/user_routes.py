import sqlite3
from pkg import app
from instance import config
from flask import render_template,request,redirect,flash,url_for,abort,session,jsonify
from pkg.myforms import ContactForm
from pkg.model import db,Testimonials,Service,Users,Booking,EmailNotification,State,Lga,Category
from flask_mail import Mail, Message
from datetime import datetime

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'oluwaseunoyediran641@gmail.com'
app.config['MAIL_PASSWORD'] = 'rvla jpvq rjbq oyce'
app.config['ADMIN_EMAIL']=config.ADMIN_EMAIL
DATABASE_NAME = 'Tectonic'
mail = Mail(app)

@app.after_request

def after_request(response):
    response.headers["Cache-Control"] = "no-cache,no-store, must-revalidate"
    return response

@app.errorhandler(404)
def pagenotfound(error):
    return render_template('User/404error.html',error=error), 404

@app.errorhandler(500)
def internal_server_error(error):
    return render_template('User/500.html',error=error), 500

@app.errorhandler(503)
def error(error):
    return render_template('User/503.html',error=error), 503




def get_db_connection():
    conn = sqlite3.connect(DATABASE_NAME)
    conn.row_factory = sqlite3.Row
    return conn



@app.route('/get_lgas/', methods=['POST'])
def get_lgas():
    state_id = request.form['state_id']
    lgas = Lga.query.filter_by(state_id=state_id).all()
    return jsonify([{'id': lga.lga_id, 'name': lga.lga_name} for lga in lgas])


@app.route('/home/')
def home():
    testimonials = Testimonials.query.filter_by(status='approved').order_by(Testimonials.id.desc()).all()
    message = session.pop('message', None)
    booking_success = session.pop('booking_success', False)
    email = session.pop('email', '')
    return render_template('User/homepage.html', testimonials=testimonials, message=message, booking_success=booking_success, email=email)


@app.route('/about/')
def about():
    return render_template('User/about.html',title='About Us')

@app.route('/portfolio/')
def portfolio():
    return render_template('User/portfolio.html')     



@app.route('/submit_testimonial/', methods=['POST'])
def submit_testimonial():
    quote = request.form['quote']
    author = request.form['author']
    rating = request.form['rating']
    query = Testimonials(quote=quote, author=author,rating=rating)
    if query:
       db.session.add(query)
       db.session.commit()
       flash('Testimonial submitted successfully!- It would be reviewed soon :)',category='success')
    else:
        flash('Testimonial submission unsuccessfully!',category='error')
    return redirect(url_for('home'))


@app.route('/service/')
@app.route('/service/<int:service_id>/')
def service(service_id=None):
    testimonials = Testimonials.query.filter_by(status='approved').order_by(Testimonials.id.desc()).all()
    services = Service.query.all()
    categories = Category.query.all() 
    if service_id:
        service = Service.query.get(service_id)
        if service is None:
            abort(404)
    else:
        service = None
    return render_template('User/services.html',testimonials=testimonials, services=services, service=service, categories=categories)



@app.route('/service/category/<int:category_id>')
def service_by_category(category_id):
    category = Category.query.get(category_id)
    services = Service.query.filter_by(category=category).all()
    return render_template('User/services.html', services=services, category=category)

@app.route('/form/', methods=['GET', 'POST'])
def handle_form_submission():
    services = Service.query.all()
    form = ContactForm()
    form.service.choices = [('', 'Select a service')] + [(str(s.id), s.name) for s in services]
    service_id = request.args.get('service_id')
    if service_id:
        form.service.data = service_id

    states = State.query.all()
    form.state.choices = [(s.state_id, s.state_name) for s in states]

    if form.state.data:
        lgas = Lga.query.filter_by(state_id=form.state.data).all()
        form.lga.choices = [(l.lga_id, l.lga_name) for l in lgas]
    else:
        form.lga.choices = [('', 'Select a state first')]

    booking_success = session.pop('booking_success', False)
    email = session.pop('email', '')
    message = session.pop('message', None)

    if form.validate_on_submit():
        try:
            user = Users.query.filter_by(email=form.email.data).first()
            if not user:
                user = Users(name=form.fullname.data, email=form.email.data, phone_number=form.phone.data)
                db.session.add(user)
                db.session.commit()

            service_id = int(form.service.data)
            service = Service.query.get(service_id)

            if service:
                booking = Booking(service_id=service.id, user_id=user.id, state_id=form.state.data, lga_id=form.lga.data, status='pending')
                db.session.add(booking)
                db.session.commit()

                service_recipients = {
    "engineering services": ["oluwaseunoyediran641@gmail.com", "darkpod641@gmail.com"],
    "surveying services": ["oluwaseunoyediran641@gmail.com"],
}

                recipients = service_recipients.get(service.category.name.lower(), ["oluwaseunoyediran641@gmail.com"])

                admin_name = "Surveyor Bimbo"
                engineer_name = "Engineer Estar"

                for recipient in recipients:
                    if recipient == "oluwaseunoyediran641@gmail.com":
                        greeting = f"Dear {admin_name}"
                    elif recipient == ["darkpod641@gmail.com","oluwaseunoyediran641@gmail.com"]:
                        greeting = f"Dear {engineer_name}"
                    else:
                        greeting = "Dear Team"

                msg = Message("New Booking Notification", sender="oluwaseunoyediran641@gmail.com", recipients=[recipient])
                msg.html = f"""
                <p>{greeting},</p>
                <p>You have received a new booking from:</p>
                <p><strong style="color: green;">Name: {form.fullname.data}</strong></p>
                <p><strong style="color: green;">Email: {form.email.data}</strong></p>
                <p><strong style="color: green;">Phone Number: {form.phone.data}</strong></p>
                <p><strong style="color: green;">Service Booked: {service.name}</strong></p>
                <p><strong style="color: green;">Price: {service.price} - {service.maxprice}</strong></p>
                <p><strong style="color: green;">State: {State.query.get(form.state.data).state_name}</strong></p>
                <p><strong style="color: green;">LGA: {Lga.query.get(form.lga.data).lga_name}</strong></p>
                <p><strong style="color: green;">Comment/Message: {form.message.data}</strong></p>
                <p>Please reach out to the client soon.</p>
                <p>Best regards,<br>TECTONIC GLOBAL SERVICES LIMITED</p>
                """



                try:
                    mail.send(msg)
                    emailnotification = EmailNotification(
                        booking_id=booking.id,
                        notification_type='admin_notification',
                        message=f"New booking by {form.fullname.data} ({form.email.data}) for {service.name}. Please check your email for more details."
                    )
                    db.session.add(emailnotification)
                    db.session.commit()
                except Exception as e:
                    flash(f"Error sending email to admin: {e}")
                    app.logger.error(f"Error sending email to admin: {e}")

                user_msg = Message("Booking Confirmation",
                                    sender="oluwaseunoyediran641@gmail.com", 
                                    recipients=[form.email.data])
                user_msg.html = f"""
<p>Dear <strong style="color: green;"> {form.fullname.data},</strong></p>
<p>Thank you for booking our <strong style="color: green;"> {service.name} </strong> service. We're excited to work with you!</p>
<p>Our team will be in touch with you soon to discuss further details.</p>
<p>In the meantime, if you have any questions or concerns, please don't hesitate to reach out.</p>
<p>Best regards,<br>Tectonic Global Services Limited</p>
"""

                try:
                    mail.send(user_msg)
                    print("Email sent successfully to user")
                except Exception as e:
                    flash(f"Error sending email to user: {e}")
                    app.logger.error(f"Error sending email to user: {e}")

                session['booking_success'] = True
                session['email'] = form.email.data
                session['message'] = f"Important: If you do not see the confirmation email in your inbox, please check your spam folder. If you are still having trouble, contact us at {app.config['ADMIN_EMAIL']}"
                return redirect(url_for('home'))
            else:
                flash('Invalid service selected', 'error')
        except Exception as e:
            db.session.rollback()
            
            flash(f'Error submitting form: {e}', 'error')
            app.logger.error(f"Error submitting form: {e}")
    else:
        
        for field, errors in form.errors.items():
            for error in errors:
                flash(f"{field}: {error}", 'error')
    return render_template('User/form.html', booking_success=booking_success, email=email, 
                           form=form, message=message)



@app.route('/booking/', methods=['GET','POST'])
def booking():
    services = Service.query.all()
    service_id = request.args.get('service_id', None)
    form = ContactForm()
    form.service.choices = [('', 'Select a service')] + [(str(s.id), s.name) for s in services]

    if form.validate_on_submit():
        booking = Booking(  
            service_id=form.service.data,
            lga_id=form.lga.data,
            state_id=form.state.data,
            booking_date=datetime.datetime.now(),
            status='booking'
        )
        db.session.add(booking)
        db.session.commit()
        # Redirect to a success page or display a success message
        return redirect(url_for('booking_success'))

    booking_success = request.args.get('booking_success', False)
    email = request.args.get('email', '')
    message = request.args.get('message', '')
    return render_template('User/form.html', form=form, booking_success=booking_success,
                            email=email, message=message)


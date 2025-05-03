from pkg import app 
from flask import render_template, request, redirect, flash, url_for 
from pkg.model import db, Service,Testimonials ,Booking,EmailNotification,Users,Category
from pkg.myforms import ServiceForm 
import os 
from werkzeug.utils import secure_filename 


import logging

logging.basicConfig(level=logging.DEBUG)

@app.before_request
def log_request():
    logging.debug(f"Request: {request.method} {request.path}")
# Configuration 
UPLOAD_FOLDER = 'pkg/static/images' 
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER 

SERVICE_ADDED_SUCCESSFULLY = 'Service added successfully' 
SERVICE_UPDATED_SUCCESSFULLY = 'Service updated successfully' 
SERVICE_DELETED_SUCCESSFULLY = 'Service deleted successfully' 




@app.route('/admin/', methods=['GET', 'POST'])
def admin():
    stats = {
        'total_users': Users.query.count(),
        'total_bookings': Booking.query.count(),
        'total_services': Service.query.count(),
        'total_testimonial': Testimonials.query.count(),
    }
    form = ServiceForm()
    edit_form = ServiceForm()
    categories = Category.query.all()
    if categories:
        form.category_id.choices = [(c.id, c.name) for c in categories]
    else:
        form.category_id.choices = []
   

    if form.validate_on_submit():
        # form is valid, add service to database
        try:
            image = form.image.data
            filename = secure_filename(image.filename)
            image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            service = Service(
                name=form.name.data,
                image=filename,
                description=form.description.data,
                price=form.price.data,
                maxprice=form.maxprice.data,
                category_id=form.category_id.data
            )
            db.session.add(service)
            db.session.commit()
            flash(SERVICE_ADDED_SUCCESSFULLY, 'success')
            return redirect(url_for('admin'))
        except Exception as e:
            flash('An error occurred while adding the service', 'error')
            app.logger.error(e)
    else:
        for field, errors in form.errors.items():
            for error in errors:
                flash(f"{field}: {error}", 'error')
    services = Service.query.all()
    testimonials = Testimonials.query.all()
    bookings = Booking.query.all()
    notifications = EmailNotification.query.all()
    return render_template('Admin/dashboard.html', services=services, testimonials=testimonials,
                            bookings=bookings,categories=categories,
                            edit_form=edit_form, form=form, notifications=notifications, stats=stats)

@app.route('/delete_service/<int:service_id>', methods=['GET','POST'])
def delete_service(service_id):
    service = Service.query.get(service_id)
    if service:
        db.session.delete(service)
        db.session.commit()
        flash('Service deleted successfully', 'success')
    else:
        flash('Service not found', 'error')
    return redirect(url_for('admin'))

@app.route('/admin/services/edit/<int:service_id>/', methods=['GET', 'POST'])
def edit_service(service_id):
    stats = {
        'total_users': Users.query.count(),
        'total_bookings': Booking.query.count(),
        'total_services': Service.query.count(),
        'total_testimonial': Testimonials.query.count(),
    }
    service = Service.query.get(service_id)
    form = ServiceForm(obj=service)
    
    categories = Category.query.all()
    if categories:
        form.category_id.choices = [(c.id, c.name) for c in categories]
    else:
        form.category_id.choices = []
        
    if form.validate_on_submit():
        # Update service details
        service.name = form.name.data
        service.description = form.description.data
        service.price = form.price.data
        service.maxprice = form.maxprice.data
        service.category_id = form.category_id.data
        
        if form.image.data:
            image = form.image.data
            filename = secure_filename(image.filename)
            image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            service.image = filename
            
        db.session.commit()
        flash(SERVICE_UPDATED_SUCCESSFULLY, 'success')
        return redirect(url_for('admin'))
    else:
       
        for field, errors in form.errors.items():
            for error in errors:
                flash(f"Error in {field}: {error}", 'error')
                
    return render_template('Admin/dashboard.html', form=form, service=service,stats=stats)




@app.route('/admin/testimonials/approve/<int:testimonial_id>/')
def approve_testimonial(testimonial_id):
    testimonial = Testimonials.query.get(testimonial_id)
    testimonial.status = 'approved'
    db.session.commit()
    flash(' Approved', 'Success')
    return redirect(url_for('admin'))



@app.route('/admin/testimonials/<int:testimonial_id>')
def view_testimonial(testimonial_id):
    testimonial = Testimonials.query.get(testimonial_id)
    return redirect(url_for('admin'))

@app.route('/admin/testimonials/<int:testimonial_id>/delete')
def delete_testimonial(testimonial_id):
    testimonial = Testimonials.query.get(testimonial_id)
    testimonial.status = 'rejected'
    db.session.commit()
    flash(' Rejected', 'Rejected')
    return redirect(url_for('admin'))

@app.route('/admin/bookings/')
def admin_bookings():
    form = ServiceForm() 
    bookings = Booking.query.all()
    stats = {
        'total_users': Users.query.count(),
        'total_bookings': Booking.query.count(),
        'total_services': Service.query.count(),
        'total_testimonial': Testimonials.query.count(),
    }
    notifications = EmailNotification.query.order_by(EmailNotification.id.desc()).all()
   

    return render_template('Admin/dashboard.html', bookings=bookings, 
                           notifications=notifications,form=form,stats=stats)

@app.route('/clear-notifications/')
def clear_notifications():
    EmailNotification.query.delete()
    db.session.commit()
    flash('Notifications cleared successfully', 'success')
    return redirect(url_for('admin'))

@app.route('/clear-bookings/')
def clear_bookings():
 EmailNotification.query.delete()
 Booking.query.delete()
 db.session.commit()
 flash('Bookings cleared successfully', 'success')
 return redirect(url_for('admin'))


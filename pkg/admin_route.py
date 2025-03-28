from pkg import app
from flask import render_template,request,redirect,flash
from pkg.model import db,Contact
from pkg.myforms import ContactForm

@app.route('/bookings/')
def service_booked():
    count=db.session.query(Contact).count()
    booked=db.session.query(Contact).all()
    return render_template('User/bookings.html',booked=booked ,count=count)


@app.route('/customer/<int:cust_id>/update/', methods=['GET', 'POST'])
def customer_update(cust_id):
    customer = db.session.query(Contact).get(cust_id)
    form = ContactForm()  
    if request.method=='POST':
        customer.fullname = form.fullname.data
        customer.phone = form.phone.data
        customer.service = form.service.data
        customer.message = form.message.data
        db.session.commit()
        return redirect('/bookings/')
    return render_template('Admin/customer_update.html', form=form,customer=customer)


@app.route('/customer/<int:id>/delete/')
def customer_delete(id):
    cust=db.session.query(Contact).get(id)
    db.session.delete(cust)
    db.session.commit()
    return redirect('/bookings/')

@app.route('/customer/<int:cust_id>/details/')
def customer_details(cust_id):
     customer=Contact.query.get_or_404(cust_id)
     flash('Booked service has been deleted')
     return render_template('User/details.html',customer=customer)
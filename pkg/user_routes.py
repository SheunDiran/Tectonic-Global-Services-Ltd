from pkg import app
from flask import render_template,request,redirect,flash
from pkg.myforms import ContactForm
from pkg.model import db,Contact


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

@app.route('/home/')
def home():
    return render_template('User/homepage.html')

@app.route('/about/')
def about():
    return render_template('User/about.html',title='About Us')

@app.route('/form/',methods=['GET', 'POST'])
def form():
    data = ContactForm()
    fullname=request.form.get('fullname')
    phone=request.form.get('phone')
    service=request.form.get('service')
    message=request.form.get('message')
    if data.validate_on_submit():
        if phone == ''  and fullname == ''  and service=='':
            flash('Please fill in all required fields', category='error')
            return redirect('/form/')
        else:
            cust=Contact(fullname=fullname,phone=phone,service=service,message=message)
            db.session.add(cust)
            db.session.commit()
            flash('THANKS FOR BOOKING')
            return redirect('/home/')
    return render_template('User/form.html',data=data,title='Book A Service')

@app.route('/service/')
def service():
    return render_template('User/services.html',title='Our Services')


from flask_wtf import FlaskForm
from pkg.model import Service,State
from wtforms import StringField,SelectField,SubmitField,TextAreaField,FileField,DecimalField
from wtforms.validators import DataRequired,Email



class ContactForm(FlaskForm):
    fullname = StringField('Full name', validators=[DataRequired('Please enter your fullname')])
    email = StringField('Email', validators=[DataRequired('Please enter your email'), Email()])
    phone = StringField('Phone number', validators=[DataRequired('Please enter your phone number')])
    state = SelectField('State', coerce=int)
    lga = SelectField('LGA', coerce=int, validators=[DataRequired('Please enter your local government area')])
    service = SelectField('Service', coerce=str, validators=[DataRequired('P;ease select a service')])
    message = TextAreaField('Comment')
    button = SubmitField('Book a service')

   
    
    def __init__(self, *args, **kwargs):
        super(ContactForm, self).__init__(*args, **kwargs)
        self.state.choices = [(s.state_id, s.state_name) for s in State.query.all()]



class ServiceForm(FlaskForm):
    name = StringField('Service Name', validators=[DataRequired()])
    description = TextAreaField('Service Description', validators=[DataRequired()])
    category_id = SelectField('Category', coerce=int)
    image = FileField('Service Image')
    price = DecimalField('Minimum Service Price', validators=[DataRequired()])
    maxprice = DecimalField(' Maximum Service Price')
    
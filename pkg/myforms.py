from flask_wtf import FlaskForm
from wtforms import StringField,SelectField,SubmitField
from wtforms.validators import DataRequired


class ContactForm(FlaskForm):
    fullname=StringField('Full name',validators=[DataRequired('Please enter your fullname')])
    phone=StringField('Phone number',validators=[DataRequired('Please enter your email')])
    service=SelectField('Label', choices=[('','Select your service'),
    ('surv_eng', 'Surveying Engineering'),('geo', 'Geophysics'),('hydrography','Hydrography'),
    ('dig_map','Digital mapping'),
    ('geo-information','Geo-Information Consultants & Registered surveyors'),
    ('inverters','Mpower Inverters'),('hp laptops','HP laptop')]
    ,validators=[DataRequired('Please select a service')])
    message=StringField('Comment')
    button=SubmitField('Book a service')

    class Meta:

        csrf = True

        csrf_time_limit = 360

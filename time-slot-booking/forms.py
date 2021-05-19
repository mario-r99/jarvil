from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField
from wtforms.validators import Length

class BookingForm(FlaskForm):
    m1 = BooleanField()
    m2 = BooleanField()
    m3 = BooleanField()
    m4 = BooleanField()
    
    t1 = BooleanField()
    t2 = BooleanField()
    t3 = BooleanField()
    t4 = BooleanField()
    
    w1 = BooleanField()
    w2 = BooleanField()
    w3 = BooleanField()
    w4 = BooleanField()
    
    th1 = BooleanField()
    th2 = BooleanField()
    th3 = BooleanField()
    th4 = BooleanField()

    f1 = BooleanField()
    f2 = BooleanField()
    f3 = BooleanField()
    f4 = BooleanField()
    
    s1 = BooleanField()
    s2 = BooleanField()
    s3 = BooleanField()
    s4 = BooleanField()
    
    su1 = BooleanField()
    su2 = BooleanField()
    su3 = BooleanField()
    su4 = BooleanField()

    firstname = StringField('First Name', validators=[Length(min=2, max=20)], render_kw={"placeholder": "Enter first name"})
    lastname = StringField('Last Name', validators=[Length(min=2, max=20)], render_kw={"placeholder": "Enter last name"})
    email = StringField('Email', validators=[Length(min=6, max=35)], render_kw={"placeholder": "Enter email"})

    submit = SubmitField('Submit Reservation')
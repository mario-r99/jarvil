from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField
from wtforms.validators import Length

class BookingForm(FlaskForm):
    booked = BooleanField()

    firstname = StringField('First Name', validators=[Length(min=2, max=20)], render_kw={"placeholder": "Enter first name"})
    lastname = StringField('Last Name', validators=[Length(min=2, max=20)], render_kw={"placeholder": "Enter last name"})
    email = StringField('Email', validators=[Length(min=6, max=35)], render_kw={"placeholder": "Enter email"})

    submit = SubmitField('Submit Reservation')
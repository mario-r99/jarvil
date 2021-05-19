from flask import Flask, render_template, url_for, flash, redirect, request
from forms import BookingForm
app = Flask(__name__)

app.config['SECRET_KEY'] = '8fd4b5b09d72052a2ef9e200dc3a990e'

bookings = [
    [10,10,9,3], # Monday
    [10,0,9,3],  # Tuesday
    [10,10,9,3], # Wednesday
    [1,10,9,4],  # Thursday
    [10,7,9,3], # Friday
    [10,10,9,3], # Saturday
    [10,10,9,3]  # Sunday
]

@app.route('/', methods=['GET', 'POST'])
def home():
    form = BookingForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            flash('Reservation submitted!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Invalid input. Look below for more information.', 'danger')
            return redirect(url_for('home'))
    return render_template('home.html', bookings=bookings, form=form)
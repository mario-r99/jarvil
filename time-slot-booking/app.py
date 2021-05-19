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
    return render_template('home.html', bookings=bookings, form=form)

def format_table(form):
    return [
        [form.m1.data, form.m2.data, form.m3.data, form.m4.data],
        [form.t1.data, form.t2.data, form.t3.data, form.t4.data],
        [form.w1.data, form.w2.data, form.w3.data, form.w4.data],
        [form.th1.data, form.th2.data, form.th3.data, form.th4.data],
        [form.f1.data, form.f2.data, form.f3.data, form.f4.data],
        [form.s1.data, form.s2.data, form.s3.data, form.s4.data],
        [form.su1.data, form.su2.data, form.su3.data, form.su4.data],
    ]
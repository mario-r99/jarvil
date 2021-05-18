from flask import Flask, render_template, url_for
app = Flask(__name__)

bookings = [
    [10,10,9,3], # Monday
    [10,0,9,3],  # Tuesday
    [10,10,9,3], # Wednesday
    [1,10,9,3],  # Thursday
    [10,7,9,3], # Friday
    [10,10,9,3], # Saturday
    [10,10,9,3]  # Sunday
]

@app.route('/')
def home():
    return render_template('home.html', bookings=bookings)
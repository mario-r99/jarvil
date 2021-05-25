from flask import Flask, render_template, url_for, flash, redirect, request
from forms import BookingForm
from flask_mqtt import Mqtt
from datetime import date, timedelta
import redis
import json
import time
import sys

# Initialize room
slot_amount = 10

# Initialize flask server
app = Flask(__name__)
app.config['SECRET_KEY'] = '8fd4b5b09d72052a2ef9e200dc3a990e'
app.config['MQTT_BROKER_URL'] = '192.168.178.17'
app.config['MQTT_BROKER_PORT'] = 1883
app.config['MQTT_USERNAME'] = ''
app.config['MQTT_PASSWORD'] = ''
app.config['MQTT_KEEPALIVE'] = 60
app.config['MQTT_TLS_ENABLED'] = False

# Initialize redis database
cache = redis.Redis(host='redis', port=6379, charset="utf-8", decode_responses=True)

# Initialize mqtt client
mqtt = Mqtt(app)


# Default page
@app.route('/', methods=['GET', 'POST'])
def home():
    form = BookingForm()
    bookings = get_bookings()
    week = get_current_week()
    if request.method == 'POST':
        if form.validate_on_submit():
            new_input = format_table(form)
            if validate_bookings(new_input, bookings):
                set_bookings(new_input)
                mqtt.publish('booking/new', json.dumps(new_input))
                flash(f'Reservation submitted for {new_input.get("firstname")} {new_input.get("lastname")}.', 'success')
                return redirect(url_for('home'))
        else:
            flash('Invalid form input. Look below for more information.', 'danger')
    return render_template('home.html', bookings=bookings, form=form, week=week)


# Read out slot occupancy from cache
def get_bookings():
    entries = cache.scan(match='slot:*')[1]

    weeks = []
    for week_index in range(7):
        slots = []
        for slot_index in range(4):
            occupied_slots = count_filter(entries, f'slot:{week_index}:{slot_index}')
            free_slots = slot_amount - occupied_slots
            slots.append(f'{free_slots} slots' if free_slots != 1 else '1 slot')
        weeks.append(slots)
    return weeks


# Additional form validation
def validate_bookings(form_input, cache_bookings):

    # Check if at least one time slot is selected
    if not form_input.get("bookings"):
        flash('No slot selected. Please select at least one time slot.', 'danger')
        return False

    # Check if time slot is fully occupied
    for form_booking in form_input.get("bookings"):
        # Convert text value to int, e.g. 3 slots -> 3
        if int(cache_bookings[form_booking.get("week")][form_booking.get("slot")].split(' ')[0]) <= 0:
            flash('The time slot you booked is already fully occupied. Please try another slot.', 'danger')
            return False

    # Check duplicate mail address in same time slot
    entries = cache.scan(match='slot:*')[1]
    email = form_input.get("email").encode()
    for form_booking in form_input.get("bookings"):
        search_string = f'slot:{form_booking.get("week")}:{form_booking.get("slot")}:{email}'
        if search_string in entries:
            flash('You have already booked this or one of these time slots with this email address.', 'danger')
            return False

    return True


# Save new input data in cache with the format slot:{week-nr(0-6)}:{slot-nr(0-3)}:occupant-id(email)
def set_bookings(form_input):
    pipe = cache.pipeline()
    try:
        for booking in form_input.get("bookings"):
            hash_name = f'slot:{booking.get("week")}:{booking.get("slot")}'
            # used_slots = len(cache.scan(match=f'{hash_name}:*')[1])
            hash_dict = {
                'firstname':form_input['firstname'],
                'lastname':form_input['lastname'],
                'email':form_input['email']
            }
            pipe.hmset(f'{hash_name}:{form_input["email"].encode()}', hash_dict)
        pipe.execute()
    except redis.exceptions.ConnectionError as exc:
        raise exc


def count_filter(array, match):
    count = 0
    for element in array:
        if match in element:
            count += 1
    return count


# Convert table form into booking list
def format_table(form):
    # Put all form data into 2-dimensional array
    table = [
        [form.m1.data, form.m2.data, form.m3.data, form.m4.data],
        [form.t1.data, form.t2.data, form.t3.data, form.t4.data],
        [form.w1.data, form.w2.data, form.w3.data, form.w4.data],
        [form.th1.data, form.th2.data, form.th3.data, form.th4.data],
        [form.f1.data, form.f2.data, form.f3.data, form.f4.data],
        [form.s1.data, form.s2.data, form.s3.data, form.s4.data],
        [form.su1.data, form.su2.data, form.su3.data, form.su4.data],
    ]
    # iterate over array and push booked entries on list
    bookings = []
    for week_index, week in enumerate(table):
        for slot_index, slot in enumerate(week):
            if slot == True:
                bookings.append({
                    "week": week_index,
                    "slot": slot_index
                })
    return {
        "firstname": form.firstname.data,
        "lastname": form.lastname.data,
        "email": form.email.data,
        "bookings": bookings
    }


def get_current_week():
    today = date.today()
    monday = today - timedelta(days=today.weekday())
    tuesday = monday + timedelta(days=1)
    wednesday = monday + timedelta(days=2)
    thursday = monday + timedelta(days=3)
    friday = monday + timedelta(days=4)
    saturday = monday + timedelta(days=5)
    sunday = monday + timedelta(days=6)
    return [
        f'{monday.strftime("%d.%m.%Y")} - {sunday.strftime("%d.%m.%Y")}',
        monday.strftime("%b %d"),
        tuesday.strftime("%b %d"),
        wednesday.strftime("%b %d"),
        thursday.strftime("%b %d"),
        friday.strftime("%b %d"),
        saturday.strftime("%b %d"),
        sunday.strftime("%b %d"),
    ]
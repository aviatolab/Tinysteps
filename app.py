from flask import Flask, render_template
import json
import random
from flask_wtf import FlaskForm
from wtforms import StringField

app = Flask(__name__)
app.secret_key = 'papa_u_vasi_silen_v_matematike'


class BookingForm(FlaskForm):
    name = StringField('Вас зовут:')
    phone = StringField('Ваш телефон:')


with open("teachers.json", "r", encoding='utf-8') as f:
    teacher = json.load(f)


@app.route('/')
def index():
    return render_template('index.html',
                           teachers=random.sample(teacher, 6))


@app.route('/all/')
def all_teachers():
    len_teacher = len(teacher)
    return render_template('all.html',
                           teachers=teacher,
                           len=len_teacher)


@app.route('/request/')
def request():
    return render_template('request.html')


@app.route('/profile/<teacher_id>')
def profile(teacher_id):
    day = ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота', 'Воскресенье']
    teacher_photo = ''
    teacher_name = ''
    about = ''
    rating = 0
    price = 0
    count = 0

    for i in teacher:
        if i['id'] == int(teacher_id):
            teacher_photo = i['picture']
            teacher_name = i['name']
            about = i['about']
            rating = i['rating']
            price = i['price']
            break
    return render_template('profile.html',
                           day=day,
                           teachers=teacher,
                           photo=teacher_photo,
                           name=teacher_name,
                           about=about,
                           rating=rating,
                           price=price,
                           id=int(teacher_id),
                           count=count)


@app.route('/booking/<t_id>/<day>/<time>')
def booking(t_id, day, time):
    form = BookingForm()
    photo = ''
    name = ''
    for i in teacher:
        if i['id'] == int(t_id):
            photo = i['picture']
            name = i['name']
            break
    return render_template('booking.html',
                           t_id=t_id,
                           day=day,
                           time=time,
                           photo=photo,
                           name=name,
                           form=form)


@app.route('/booking_done/<b_day>/<b_time>/<t_name>', methods=['POST', 'GET'])
def booking_done(b_day, b_time, t_name):
    form = BookingForm()
    name = form.name.data
    phone = form.phone.data
    book = {'name': name, 'phone': phone, 'teacher': t_name, 'date': b_day, 'time': b_time}

    with open('booking.json') as file:
        list_booking = json.load(file)

    list_booking.append(book)

    with open('booking.json', 'w', encoding='utf-8', ) as file:
        json.dump(list_booking, file, indent=4, ensure_ascii=False)

    return render_template('booking_done.html',
                           day=b_day,
                           time=b_time,
                           name=name,
                           phone=phone)


if __name__ == '__main__':
    app.run(debug=True)



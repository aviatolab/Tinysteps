from flask import Flask, render_template, request
import json
import random
from flask_wtf import FlaskForm
from wtforms import StringField, RadioField
from collections import OrderedDict

app = Flask(__name__)
app.secret_key = 'papa_u_vasi_silen_v_matematike'


class BookingForm(FlaskForm):
    name = StringField('Вас зовут:')
    phone = StringField('Ваш телефон:')


class RequestForm(FlaskForm):
    target = RadioField('Какая цель занятий?', choices=[("travel", "Для путешествий"),
                                                        ("study", "Для учебы"),
                                                        ("work", "Для работы"),
                                                        ("relocate", "Для переезда")])
    times = RadioField('Сколько времени есть?', choices=[("1-2 часа в неделю", "1-2 часа в неделю"),
                                                         ("3-5 часов в неделю", "3-5 часов в неделю"),
                                                         ("5-7 часов в неделю", "5-7 часов в неделю"),
                                                         ("7-10 часов в неделю", "7-10 часов в неделю")])
    target_name = StringField('Вас зовут:')
    target_phone = StringField('Ваш телефон:')


with open("teachers.json", "r", encoding='utf-8') as f:
    teacher = json.load(f)

with open("goals.json", "r", encoding='utf-8') as g:
    js_goal = json.load(g)


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


@app.route('/request_view/')
def request_view():
    form = RequestForm()

    return render_template('request_view.html', form=form)


@app.route('/request_done/', methods=['GET', 'POST'])
def request_done():
    form = RequestForm()
    if request.method == "POST":
        request_json = {'target': form.target.data, 'times': form.times.data, 'name': form.target_name.data,
                        'phone': form.target_phone.data}

        with open('request.json') as rf:
            list_request = json.load(rf)

        list_request.append(request_json)

        with open('request.json', 'w', encoding='utf-8') as fr:
            json.dump(list_request, fr, indent=4, ensure_ascii=False)

    return render_template('request_done.html')


@app.route('/profile/<teacher_id>')
def profile(teacher_id):
    day = ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота', 'Воскресенье']
    teacher_photo = ''
    teacher_name = ''
    about = ''
    rating = 0
    price = 0
    count = 0
    profile_goals = []
    goald = ""

    for i in teacher:
        if i['id'] == int(teacher_id):
            teacher_photo = i['picture']
            teacher_name = i['name']
            about = i['about']
            rating = i['rating']
            price = i['price']
            profile_goals = i['goals'].copy()
            break

    for k, v in js_goal.items():
        for i in profile_goals:
            if k == i:
                goald += v + ' '

    return render_template('profile.html',
                           day=day,
                           teachers=teacher,
                           photo=teacher_photo,
                           name=teacher_name,
                           about=about,
                           rating=rating,
                           price=price,
                           id=int(teacher_id),
                           count=count,
                           goalz=goald)


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
    if request.method == 'POST':
        book = {'name': name, 'phone': phone, 'teacher': t_name, 'date': b_day, 'time': b_time}

        with open('booking.json') as file:
            list_booking = json.load(file)

        list_booking.append(book)

        with open('booking.json', 'w', encoding='utf-8') as file:
            json.dump(list_booking, file, indent=4, ensure_ascii=False)

    return render_template('booking_done.html',
                           day=b_day,
                           time=b_time,
                           name=name,
                           phone=phone)


@app.route('/goal/')
def goal():
    sort_teacher_for_rating = sorted(teacher, key=lambda k: k['rating'])
    return render_template('goal.html',
                           teachers=sort_teacher_for_rating[::-1])


if __name__ == '__main__':
    app.run(debug=True)

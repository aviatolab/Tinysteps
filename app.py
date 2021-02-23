from flask import Flask, render_template, request
import json
import random
from flask_wtf import FlaskForm
from wtforms import StringField, RadioField
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = 'papa_u_vasi_silen_v_matematike'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sqlite_001.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Teachers(db.Model):
    __tablename__ = "teachers"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    about = db.Column(db.Text)
    rating = db.Column(db.Float)
    picture = db.Column(db.String(300))
    price = db.Column(db.Integer)
    free = db.Column(db.String(1000), nullable=False)
    goals = db.Column(db.String(100))
    booking = db.relationship("Booking", back_populates="teacher_b")


class Booking(db.Model):
    __tablename__ = "bookings"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(100), nullable=False)
    date = db.Column(db.String(100), nullable=False)
    time = db.Column(db.String(100), nullable=False)
    teacher_b = db.relationship("Teachers", back_populates="booking")
    teachers_id = db.Column(db.Integer, db.ForeignKey("teachers.id"))


class RequestView(db.Model):
    __tablename__ = "requestviews"
    id = db.Column(db.Integer, primary_key=True)
    target = db.Column(db.String(100), nullable=False)
    times = db.Column(db.String(100), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(100), nullable=False)


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


teacher = db.session.query(Teachers).all()

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
    goald = ''
    teacher_goal = []
    rating = 0.0
    price = 0
    about = ''
    free = {}

    for i in teacher:
        if i.id == int(teacher_id):
            teacher_photo = i.picture
            teacher_name = i.name
            teacher_goal = i.goals.split()
            rating = i.rating
            price = i.price
            about = i.about
            free = json.loads(i.free)
            break

    for k, v in js_goal.items():
        for i in teacher_goal:
            if k == i:
                goald += v + ' '

    return render_template('profile.html',
                           photo=teacher_photo,
                           name=teacher_name,
                           goal=goald,
                           rating=rating,
                           price=price,
                           about=about,
                           teachers=teacher,
                           id=teacher_id,
                           free=free)


@app.route('/booking/<t_id>/<day>/<time>')
def booking(t_id, day, time):
    form = BookingForm()
    photo = ''
    name = ''
    for i in teacher:
        if i.id == int(t_id):
            photo = i.picture
            name = i.name
            break
    return render_template('booking.html',
                           t_id=t_id,
                           day=day,
                           time=time,
                           photo=photo,
                           name=name,
                           form=form)


@app.route('/booking_done/<b_day>/<b_time>/<t_name>/<t_id>', methods=['POST', 'GET'])
def booking_done(b_day, b_time, t_name, t_id):
    form = BookingForm()
    name = form.name.data
    phone = form.phone.data
    if request.method == 'POST':
        b_teacher = Teachers.query.get(t_id)
        bookings = Booking(name=name, phone=phone, date=b_day, time=b_time, teacher_b=b_teacher)
        db.session.add(bookings)
        db.session.commit()

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


@app.route('/coding/')
def coding():
    sort_teacher_for_rating = sorted(teacher, key=lambda k: k['rating'])
    return render_template('coding.html',
                           teachers=sort_teacher_for_rating[::-1])


if __name__ == '__main__':
    app.run()

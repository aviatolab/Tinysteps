from app import *
import json

with open("teachers.json", "r", encoding='utf-8') as f:
    teacher = json.load(f)

db.create_all()

for i in teacher:
    teach = Teachers(name=i['name'], about=i['about'], rating=i['rating'], picture=i['picture'], price=i['price'],
                     free=json.dumps(i['free']), goals=' '.join(i['goals']))
    db.session.add(teach)

db.session.commit()


t = db.session.query(Booking).all()
for k in t:
    print(k.name, k.phone, k.date, k.time)

p = db.session.query(Teachers).all()
for k in p:
    for j in k.booking:
        print(j.name)

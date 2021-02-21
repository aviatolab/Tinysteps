from app import *
import json

with open("teachers.json", "r", encoding='utf-8') as f:
    teacher = json.load(f)

db.create_all()

for i in teacher:
    teach = Teachers(name=i['name'], about=i['about'], rating=i['rating'], picture=i['picture'], price=i['price'])
    db.session.add(teach)
    for j in i['goals']:
        goal = Goals(goal=j, teacher=teach)
        db.session.add(goal)

db.session.commit()

t = db.session.query(Teachers).all()
for k in t:
    print(k.name)
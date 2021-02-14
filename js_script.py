import data
import json

with open('goals.json', 'w') as goals:
    json.dump(data.goals, goals, indent=4, ensure_ascii=False)

with open('teachers.json', 'w') as teachers:
    json.dump(data.teachers, teachers, indent=4, ensure_ascii=False)

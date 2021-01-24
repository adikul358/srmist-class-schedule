from ics import Calendar, Event
from ics.alarm import DisplayAlarm
from datetime import datetime, timedelta
from os import system


def next_monday():
    return datetime.now() + timedelta((0 - datetime.now().weekday()) % 7)


slots = []
classes = []
days = ['mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun']

with open('/users/aditya/dev/class-schedule/slots.csv', 'r+') as f:
    slots_raw = f.readlines()
    for i in slots_raw[1:]:
        i = i.strip("\n").split(",")
        slots_temp = {
            'begin': i[1],
            'end': i[2]
        }
        slots.append(slots_temp)

with open('/users/aditya/dev/class-schedule/classes.csv', 'r+') as f:
    classes_raw = f.readlines()
    for i in classes_raw[1:]:
        if i == "\n":
            continue
        i = i.strip("\n").split(",")
        classes_temp = {
            'name': i[0],
            'desc': i[3],
            'day': i[2],
        }

        classes_temp.update(slots[int(i[1])])
        classes.append(classes_temp)


nm_prompt = next_monday().strftime("%Y-%m-%d")
init_date = input(f'Date of Reference Monday ({nm_prompt}): ')
if init_date == "":
    init_date = nm_prompt
elif datetime.strptime(init_date, "%Y-%m-%d").strftime("%w") != "1":
    raise ValueError("Entered date not a Monday")

c = Calendar()

for i in classes:
    e = Event()
    date_begin_str = f'{init_date} {i["begin"]}+0530'
    date_end_str = f'{init_date} {i["end"]}+0530'

    date_begin = datetime.strptime(
        date_begin_str, "%Y-%m-%d %H%M%z") + timedelta(days.index(i['day'].lower()))
    date_end = datetime.strptime(
        date_end_str, "%Y-%m-%d %H%M%z") + timedelta(days.index(i['day'].lower()))

    e.name = i['name']
    e.begin = date_begin.strftime("%Y-%m-%d %H:%M:%S%z")
    e.end = date_end.strftime("%Y-%m-%d %H:%M:%S%z")
    e.description = i['desc']
    e.alarms = [DisplayAlarm(trigger=timedelta(minutes=-5)),
                DisplayAlarm(trigger=date_begin)]

    if i['name'] != "Economics B":
        e.attendees = ['dubey.ona@gmail.com']

    c.events.add(e)

    print(f'Created {i["name"]} {datetime.strftime(date_begin, "%Y-%m-%d %H:%M:%S")} - {datetime.strftime(date_end, "%Y-%m-%d %H:%M:%S")}')

with open('out.ics', 'w') as my_file:
    my_file.writelines(c)

print()
print("Exported out.ics")

system('open out.ics')

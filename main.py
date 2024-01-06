from ics import Calendar, Event
from ics.alarm import DisplayAlarm
from datetime import datetime, timedelta
from os import system
import csv


def next_monday():
    return datetime.now() + timedelta((0 - datetime.now().weekday()) % 7)

slots = []
classes = [[],[],[],[],[]]
days = ['mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun']

with open('./slots.csv', 'r+') as f:
    slots_raw = f.readlines()
    for i in slots_raw[1:]:
        i = i.strip("\n").split(",")
        slots_temp = {
            'begin': i[1],
            'end': i[2]
        }
        slots.append(slots_temp)

with open('./classes.csv', 'r+') as f:
    classes_raw = csv.reader(f, delimiter=',', quotechar='"')
    for i in list(classes_raw)[1:]:
        if i == []:
            continue
        classes_temp = {
            'name': i[0],
            'desc': i[1],
        }
        classes_temp["begin"] = slots[int(i[3])-1]["begin"]
        classes_temp["end"] = slots[int(i[4])-1]["end"]

        classes[int(i[2])-1].append(classes_temp)


nm_prompt = next_monday().strftime("%Y-%m-%d")
init_date = input(f'Date of Reference Monday ({nm_prompt}): ')
if init_date == "":
    init_date = nm_prompt
elif datetime.strptime(init_date, "%Y-%m-%d").strftime("%w") != "1":
    raise ValueError("Entered date not a Monday")
curr_date = datetime.strptime(init_date, "%Y-%m-%d")
day_orders = [int(x) for x in input("Day Orders for the Week: ").split(" ")]
print()
c = Calendar()

for i in day_orders:
    if i != 0: 
        for curr_class in classes[i-1]:
            e = Event()

            date_str = curr_date.strftime("%Y-%m-%d")
            date_begin_str = f'{date_str} {curr_class["begin"]}+0530'
            date_end_str = f'{date_str} {curr_class["end"]}+0530'
            date_begin = datetime.strptime(date_begin_str, "%Y-%m-%d %H%M%z")
            date_end = datetime.strptime(date_end_str, "%Y-%m-%d %H%M%z")

            e.name = curr_class['name']
            e.begin = date_begin.strftime("%Y-%m-%d %H:%M:%S%z")
            e.end = date_end.strftime("%Y-%m-%d %H:%M:%S%z")
            e.location = curr_class['desc']
            e.alarms = [DisplayAlarm(trigger=date_begin)]
            # DisplayAlarm(trigger=timedelta(minutes=-10)),
                        
            c.events.add(e)

            print(f'Created  {date_str} {curr_class["begin"]}-{curr_class["end"]} {curr_class["name"]}')
    
    curr_date += timedelta(1)

with open('out.ics', 'w') as my_file:
    my_file.writelines(c)

print()
print()
print("Exported out.ics")

system('open out.ics')

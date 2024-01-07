from ics import Calendar, Event
from ics.alarm import DisplayAlarm
from datetime import datetime, timedelta
from os import system
import csv

# Silence ics component FutureWarning at end of script
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

# Function to get date of the next Monday
def next_monday():
    return datetime.now() + timedelta((0 - datetime.now().weekday()) % 7)

# Structure of slots array
# slots: [
#     {
#         begin: 0800,
#         end: 0850
#     },
#     ...
# ]
slots = []

# Classes are 1x5 array for 5 day orders
# Structure of classes array
# classes: [
#     [
#         {
#             name: class_name,
#             desc: class_location,
#             begin: 0800,
#             end: 0945,
#         },
#         ...
#     ],
#     ...
# ]
classes = [[],[],[],[],[]]

# Load slots from slots.csv
with open('./slots.csv', 'r+') as f:
    slots_raw = f.readlines()
    for i in slots_raw[1:]:
        i = i.strip("\n").split(",")
        slots_temp = {
            'begin': i[1],
            'end': i[2]
        }
        slots.append(slots_temp)

# Load classes from classes.csv
# Headers of classes.csv
# i[0] - class_name
# i[1] - class_location
# i[2] - day_order
# i[3] - starting_slot
# i[4] - ending_slot
with open('./classes.csv', 'r+') as f:
    classes_raw = csv.reader(f, delimiter=',', quotechar='"')
    for i in list(classes_raw)[1:]:
        # Skip empty lines separating day orders for readability
        if i == []:
            continue
        
        classes_temp = {
            'name': i[0],
            'desc': i[1],
        }
        classes_temp["begin"] = slots[int(i[3])-1]["begin"]
        classes_temp["end"] = slots[int(i[4])-1]["end"]
        classes[int(i[2])-1].append(classes_temp)

# User flow for getting starting Monday date
nm_prompt = next_monday().strftime("%Y-%m-%d")
init_date = input(f'Date of Reference Monday ({nm_prompt}): ')
if init_date == "":
    init_date = nm_prompt
elif datetime.strptime(init_date, "%Y-%m-%d").strftime("%w") != "1":
    raise ValueError("Entered date not a Monday")
curr_date = datetime.strptime(init_date, "%Y-%m-%d")

# Get space separated day orders from Monday onwards
# 0 marks a holiday
day_orders = [int(x) for x in input("Day Orders for the Week: ").split(" ")]
print()

c = Calendar()

for i in day_orders:
    date_str = curr_date.strftime("%Y-%m-%d")

    if i != 0: 
        print(f'Creating events for {date_str}...')
        for curr_class in classes[i-1]:
            date_begin_str = f'{date_str} {curr_class["begin"]}+0530'
            date_end_str = f'{date_str} {curr_class["end"]}+0530'
            date_begin = datetime.strptime(date_begin_str, "%Y-%m-%d %H%M%z")
            date_end = datetime.strptime(date_end_str, "%Y-%m-%d %H%M%z")
            e = Event()


            e.name = curr_class['name']
            e.begin = date_begin.strftime("%Y-%m-%d %H:%M:%S%z")
            e.end = date_end.strftime("%Y-%m-%d %H:%M:%S%z")
            e.location = curr_class['desc']
            e.alarms = [DisplayAlarm(trigger=date_begin)]
            # DisplayAlarm(trigger=timedelta(minutes=-10)),
                        
            c.events.add(e)

            print(f'Created event {curr_class["name"][:11]} at {curr_class["begin"]}-{curr_class["end"]}')
    else:
        print(f'Skipping events for {date_str}')

    print()
    curr_date += timedelta(1)

# Write events data to out.ics
with open('out.ics', 'w') as my_file:
    my_file.writelines(c)

print("Exported out.ics")
print("Opening out.ics for calendar import...")

system('open out.ics')

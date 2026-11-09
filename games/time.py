import time

question = input("what do you want to know :").strip().lower()

# Read the current local time.
current_time = time.localtime()
hour = current_time.tm_hour
minute = current_time.tm_min
seconds = current_time.tm_sec + 1
day = current_time.tm_wday
months = current_time.tm_mon
year = current_time.tm_year


def Time():
    global hour, minute, seconds, day

    # Carry overflow from seconds into minutes.
    if seconds == 60:
        seconds = 0
        minute += 1

    # Carry overflow from minutes into hours.
    if minute == 60:
        minute = 0
        hour += 1

    # Wrap the hour at midnight and advance the weekday.
    if hour == 24:
        hour = 0
        day = (day + 1) % 7


def dayo():
    days_of_week = [
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
        "Sunday",
    ]
    return days_of_week[day]


Time()
days = dayo()

if question == "time":
    print(hour, ":", minute, ":", seconds)
elif question == "day":
    print(days)
else:
    print(year, months, days, "at", hour, minute, seconds)

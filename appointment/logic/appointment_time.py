# -*- coding: UTF-8 -*-

def is_time_before(first, second):
    if 'pm' in first and 'am' in second:
        return False
    if 'am' in first and 'pm' in second:
        return True
    if '12:' in first and '12:' not in second:
        return True
    if first > second:
        return False
    return True


def sort_appointment_times(apps):
    for i in range(len(apps)):
        for j in range(len(apps)):
            if is_time_before(apps[i].start_time, apps[j].start_time):
                apps[i], apps[j] = apps[j], apps[i]
    return apps


def add_time(start_time, duration):
    duration = int(duration)
    hour = int(start_time.split(':')[0])
    minute = int(start_time.split(':')[1][0:len(start_time.split(':')[1]) - 2])
    postfix = start_time[len(start_time) - 2:len(start_time)]

    minute += duration
    hour = (hour + 1) % 12 if minute >= 60 else hour
    minute %= 60
    if hour == 0:
        hour = 12
        postfix = 'pm'

    return str(hour) + ':' + str(minute).zfill(2) + postfix

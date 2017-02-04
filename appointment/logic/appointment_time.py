# -*- coding: UTF-8 -*-


def is_time_before(first, second):
    """
    :param first: first time
    :param second: second time
    :return: true if first time is before second one (in 12 hours format)
    """
    first = first if len(first) == 7 else '0' + first
    second = second if len(second) == 7 else '0' + second
    if 'pm' in first and 'am' in second:
        return False
    if 'am' in first and 'pm' in second:
        return True
    if '12:' in first and '12:' not in second:
        return True
    if '12:' in second and '12:' not in first:
        return False
    if first > second:
        return False
    return True


def sort_appointment_times_in_day(apps):
    for j in range(len(apps)):
        for i in range(len(apps) - j - 1):
            if is_time_before(apps[i + 1].start_time, apps[i].start_time):
                apps[i + 1], apps[i] = apps[i], apps[i + 1]
    return apps


def sort_appointment_times(apps):
    for i in range(len(apps)):
        for j in range(len(apps) - i - 1):
            if apps[j].date == apps[j + 1].date:
                if is_time_before(apps[j + 1].start_time, apps[j].start_time):
                    apps[j + 1], apps[j] = apps[j], apps[j + 1]
            elif apps[j + 1].date < apps[j].date:
                apps[j + 1], apps[j] = apps[j], apps[j + 1]
    return apps


def cluster_appointment_times(apps):
    """
    :param apps: sorted list of appointment times
    :return: a sorted list of dictionary items (containing date and appointment times in that date)
    """
    ans = []
    if not apps:
        return None
    date = apps[0].date
    app_date = [apps[0]]
    for i in range(1, len(apps)):
        if apps[i].date == date:
            app_date.append(apps[i])
        else:
            ans.append({'date': date, 'apps': app_date})
            date = apps[i].date
            app_date = [apps[i]]
    ans.append({'date': date, 'apps': app_date})
    return ans


def add_time(start_time, duration):
    duration = int(duration)
    hour = int(start_time.split(':')[0])
    # TODO: What about :-2?
    minute = int(start_time.split(':')[1][0:len(start_time.split(':')[1]) - 2])
    postfix = start_time[len(start_time) - 2:len(start_time)]

    minute += duration
    hour = (hour + 1) % 12 if minute >= 60 else hour
    minute %= 60
    if hour == 0:
        hour = 12
        postfix = 'pm'

    return str(hour) + ':' + str(minute).zfill(2) + postfix

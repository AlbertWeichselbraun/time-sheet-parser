#!/usr/bin/env python3

from csv import reader
from icalendar import Calendar, Event, LocalTimezone
from datetime import datetime

LEN_HEADER = 6
LEN_ENTRY = 4

HEADER_DATE_COL = 2
HEADER_START_TIME_COL = 3
HEADER_END_TIME_COL = 5

ENTRY_SUBJECT_COL = 0
ENTRY_LECTURER_COL = 2

LECTURER = "Weichselbraun Albert"

get_datetime = lambda event_date, event_time: datetime.strptime('{0} {1}'.format(event_date, event_time), '%m/%d/%Y %H:%M')

def _init_calendar():
    cal = Calendar()
    cal.add('version', '2.0')
    cal.add('prodid', '-//time-sheet-parsere /file//example.com//')
    cal.add('X-WR-CALNAME', 'Lectures for {0}'.format(LECTURER))
    return cal


def text_formatter(date, start_time, end_time, subject, lecturer):
    print("{date} {start_time} {end_time} {subject} ({lecturer})".format(
        date=date, start_time=start_time, end_time=end_time, subject=subject,
        lecturer=lecturer))

def icalendar_formatter(date, start_time, end_time, subject, lecturer):
    dtstart = get_datetime(date, start_time)
    dtend = get_datetime(date, end_time)
    dtstamp = datetime.now(tz)

    event = Event()
    event.add('summary', subject)
    event.add('dtstart', dtstart)
    event.add('dtend', dtend)
    event.add('dtstamp', dtstamp)
    event.add('uid', '{dtstart}/{dtend}@time-sheet-parser@semanticlab.net'.format(
        dtstart=dtstart, dtend=dtend).replace(' ', '_'))
    event.add('priority', 5)
    cal.add_component(event)


cal = _init_calendar()
tz = LocalTimezone()
with open("test/IWtz_Zuerich_HS15_2015_07_15.csv") as f:
    csv_file = reader(f)

    for lecture_list in csv_file:
        # only consider entries that start with the calendar week and contain
        # the name of the relevant lecturer
        if not (lecture_list[0].isdigit() and LECTURER in lecture_list):
            continue

        date = lecture_list[HEADER_DATE_COL]
        start_time = lecture_list[HEADER_START_TIME_COL]
        end_time = lecture_list[HEADER_END_TIME_COL]

        lecturer_idx = lecture_list.index(LECTURER)
        subject = lecture_list[lecturer_idx + ENTRY_SUBJECT_COL - ENTRY_LECTURER_COL]

        icalendar_formatter(date, start_time, end_time, subject, LECTURER)

print(cal.to_ical().decode("utf8").replace('\r\n', '\n').strip())


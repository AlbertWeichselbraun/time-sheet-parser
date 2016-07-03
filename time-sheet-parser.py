#!/usr/bin/env python3

from argparse import ArgumentParser
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

TZ = LocalTimezone()

get_datetime = lambda event_date, event_time: datetime.strptime('{0} {1}'.format(event_date, event_time), '%m/%d/%Y %H:%M')

def _init_calendar(lecturer_name):
    cal = Calendar()
    cal.add('version', '2.0')
    cal.add('prodid', '-//time-sheet-parsere /file//example.com//')
    cal.add('X-WR-CALNAME', 'Lectures for {0}'.format(lecturer_name))
    return cal


def text_formatter(date, start_time, end_time, subject, lecturer):
    print("{date} {start_time} {end_time} {subject} ({lecturer})".format(
        date=date, start_time=start_time, end_time=end_time, subject=subject,
        lecturer=lecturer))

def icalendar_formatter(cal, date, start_time, end_time, subject, lecturer):
    dtstart = get_datetime(date, start_time)
    dtend = get_datetime(date, end_time)
    dtstamp = datetime.now(TZ)

    event = Event()
    event.add('summary', subject)
    event.add('dtstart', dtstart)
    event.add('dtend', dtend)
    event.add('dtstamp', dtstamp)
    event.add('uid', '{dtstart}/{dtend}@time-sheet-parser@semanticlab.net'.format(
        dtstart=dtstart, dtend=dtend).replace(' ', '_'))
    event.add('priority', 5)
    cal.add_component(event)

def parse_arguments():
    parser = ArgumentParser()
    parser.add_argument("infile", help="CSV file containing the time table.", default=None)
    parser.add_argument("--lecturer", help="Name of the lecturer for which the ical file is generated.")
    return parser.parse_args()


def convert_to_ical(timetable_file, lecturer_name):
    ''' converts the given timetable file to ical
    '''
    cal = _init_calendar(lecturer_name)
    with open(timetable_file) as f:
        csv_file = reader(f)

        for lecture_list in csv_file:
            # only consider entries that start with the calendar week and contain
            # the name of the relevant lecturer
            if not (lecture_list[0].isdigit() and lecturer_name in lecture_list):
                continue

            date = lecture_list[HEADER_DATE_COL]
            start_time = lecture_list[HEADER_START_TIME_COL]
            end_time = lecture_list[HEADER_END_TIME_COL]

            lecturer_idx = lecture_list.index(lecturer_name)
            subject = lecture_list[lecturer_idx + ENTRY_SUBJECT_COL - ENTRY_LECTURER_COL]

            icalendar_formatter(cal, date, start_time, end_time, subject, lecturer_name)

    print(cal.to_ical().decode("utf8").replace('\r\n', '\n').strip())

if __name__ == '__main__':
    args = parse_arguments()
    convert_to_ical(timetable_file=args.infile, lecturer_name=args.lecturer)

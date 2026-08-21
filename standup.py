#!/usr/bin/env python3

from datetime import datetime
import argparse
import calendar
import os
import sys

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-m', type=int, nargs='?', help='Month')
    parser.add_argument('-y', type=int, nargs='?', help='Year')
    return parser.parse_args()

def two_digitify(num):
    return f'{num:02}'

def is_valid_month(month):
    return 1 <= month <= 12

def make_calendar(year, month):
    output = ''
    SEPARATOR = '┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅\n\n'
    days_in_month = calendar.monthrange(year, month)[1]

    for day in range(1, days_in_month + 1):
        current_day = datetime(year, month, day)
        day_name = current_day.strftime('%a').upper()

        if day_name not in ['SAT', 'SUN']:
            date_str = f'{year}-{two_digitify(month)}-{two_digitify(day)}'
            header = f'┅┅┅┅┅┅ {day_name} {date_str} ┅┅┅┅┅┅\n'
            output += header + SEPARATOR

    return output

def main():
    args = get_args()
    today = datetime.now()
    year = args.y if args.y is not None else today.year
    month = args.m if args.m is not None else today.month

    if not is_valid_month(month):
        sys.exit('Enter a valid month.')

    filename = os.path.join(os.path.expanduser('~'), 'Documents', 'NOTES', 'standup', f'{year}-{two_digitify(month)}.md')

    if not os.path.exists(filename):
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        with open(filename, 'w') as f:
            f.write(make_calendar(year, month))
    else:
        sys.exit(f'File {filename} already exists.')

if __name__ == '__main__':
    main()

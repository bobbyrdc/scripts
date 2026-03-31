#!/usr/bin/env python3

from datetime import datetime
import argparse
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

def is_leap_year(year):
    return ((year % 4 == 0) and (year % 100 != 0)) or (year % 400 == 0)

def get_days_in_month(year, month):
    leap_year_days = 29 if is_leap_year(year) else 28
    days_in_month = {
        1: 31,
        2: leap_year_days,
        3: 31,
        4: 30,
        5: 31,
        6: 30,
        7: 31,
        8: 31,
        9: 30,
        10: 31,
        11: 30,
        12: 31
    }
    return days_in_month[month]

def make_calendar(year, month):
    output = ''
    SEPARATOR = '============================\n============================\n\n'

    for day in range(1, get_days_in_month(year, month) + 1):
        current_day = datetime(year, month, day)
        day_name = current_day.strftime('%a').upper()

        if day_name not in ['SAT', 'SUN']:
            date_str = f'{year}-{two_digitify(month)}-{two_digitify(day)}'
            header = f'{day_name} {date_str}\n'
            output += header + SEPARATOR

    return output

def main():
    args = get_args()
    today = datetime.now()
    year = args.y or today.year
    month = args.m or today.month
    filename = os.path.join(os.path.expanduser('~'), 'Documents', 'NOTES', 'standup', f'{year}-{two_digitify(month)}.txt')

    if not is_valid_month(month):
        sys.exit(f'Enter a valid month.')

    if not os.path.exists(filename):
        with open(filename, 'w') as f:
            f.write(make_calendar(year, month))
    else:
        sys.exit(f'File {filename} already exists.')

if __name__ == '__main__':
    main()

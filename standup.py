#!/usr/bin/env python3

from __future__ import annotations

from datetime import datetime
import argparse
import calendar
import os
import subprocess
import sys

def get_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description='Generate a markdown standup-notes template for a month, with a header for each weekday.'
    )
    parser.add_argument('-m', type=int, nargs='?', help='Month (1-12). Defaults to the current month.')
    parser.add_argument('-y', type=int, nargs='?', help='Year (e.g. 2026). Defaults to the current year.')
    group = parser.add_mutually_exclusive_group()
    group.add_argument('--next', action='store_true', help='Generate for next month instead of the current one.')
    group.add_argument('--prev', action='store_true', help='Generate for the previous month instead of the current one.')
    parser.add_argument('--dir', help='Directory to write the file to. Defaults to ~/Documents/NOTES/standup.')
    parser.add_argument('--open', action='store_true', help='Open the file after creating it (or if it already exists).')
    parser.add_argument('-f', '--force', action='store_true', help='Overwrite the file if it already exists.')
    return parser.parse_args()

def is_valid_month(month: int) -> bool:
    return 1 <= month <= 12

def shift_month(year: int, month: int, delta: int) -> tuple[int, int]:
    index = month - 1 + delta
    year += index // 12
    month = index % 12 + 1
    return year, month

def make_calendar(year: int, month: int) -> str:
    output = ''
    SEPARATOR = '┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅\n\n'
    days_in_month = calendar.monthrange(year, month)[1]

    for day in range(1, days_in_month + 1):
        current_day = datetime(year, month, day)
        day_name = current_day.strftime('%a').upper()

        if day_name not in ['SAT', 'SUN']:
            date_str = current_day.strftime('%Y-%m-%d')
            header = f'┅┅┅┅┅┅ {day_name} {date_str} ┅┅┅┅┅┅\n'
            output += header + SEPARATOR

    return output

def open_file(filename: str) -> None:
    editor = os.environ.get('EDITOR')
    try:
        if editor:
            subprocess.run([editor, filename])
        else:
            subprocess.run(['open', filename])
    except (OSError, FileNotFoundError):
        print(f'Could not open {filename} automatically. Open it manually.')

def main() -> None:
    args = get_args()
    today = datetime.now()

    if args.next or args.prev:
        if args.m is not None or args.y is not None:
            sys.exit('Cannot combine --next/--prev with -m/-y.')
        delta = 1 if args.next else -1
        year, month = shift_month(today.year, today.month, delta)
    else:
        year = args.y if args.y is not None else today.year
        month = args.m if args.m is not None else today.month

    if not is_valid_month(month):
        sys.exit('Enter a valid month (1-12).')

    base_dir = os.path.expanduser(args.dir) if args.dir else os.path.join(os.path.expanduser('~'), 'Documents', 'NOTES', 'standup')
    filename = os.path.join(base_dir, f'{year}-{month:02}.md')

    if os.path.exists(filename) and not args.force:
        if args.open:
            print(f'Opening existing {filename}')
            open_file(filename)
            sys.exit(0)
        print(f'File {filename} already exists.')
        print('Use --force to overwrite, or --open to open it.')
        sys.exit(1)

    os.makedirs(base_dir, exist_ok=True)
    with open(filename, 'w') as f:
        f.write(make_calendar(year, month))
    print(f'Created {filename}')

    if args.open:
        open_file(filename)

if __name__ == '__main__':
    main()

#!/usr/bin/env python3
"""Count NYC 311 complaints by complaint type and borough for a date range."""
import argparse
import csv
import sys
from collections import Counter
from datetime import datetime


def parse_date(text):
    try:
        return datetime.strptime(text, "%Y-%m-%d").date()
    except ValueError:
        raise argparse.ArgumentTypeError(
            f"'{text}' is not a valid date, use YYYY-MM-DD")


def parse_args():
    p = argparse.ArgumentParser(
        description="Output the number of 311 complaints of each type per "
                    "borough for a given creation date range (inclusive).")
    p.add_argument("-i", required=True, metavar="INPUT",
                   help="input 311 csv file")
    p.add_argument("-s", required=True, type=parse_date, metavar="START",
                   help="start date, YYYY-MM-DD (inclusive)")
    p.add_argument("-e", required=True, type=parse_date, metavar="END",
                   help="end date, YYYY-MM-DD (inclusive)")
    p.add_argument("-o", metavar="OUTPUT",
                   help="output file (default: print to stdout)")
    return p.parse_args()


def fmt(field):
    # quote a field only if it contains a comma
    return f'"{field}"' if "," in field else field


def main():
    args = parse_args()
    if args.e < args.s:
        sys.exit("error: end date is before start date")

    counts = Counter()
    with open(args.i, newline="") as f:
        reader = csv.reader(f)
        header = next(reader)
        created = header.index("Created Date")
        ctype = header.index("Complaint Type")
        borough = header.index("Borough")
        for row in reader:
            try:
                # only the MM/DD/YYYY part is needed
                d = datetime.strptime(row[created][:10], "%m/%d/%Y").date()
            except (ValueError, IndexError):
                continue
            if args.s <= d <= args.e:
                counts[(row[ctype].strip().lower(),
                        row[borough].strip().title())] += 1

    out = open(args.o, "w") if args.o else sys.stdout
    out.write("complaint type, borough, count\n")
    for (c, b), n in sorted(counts.items()):
        out.write(f"{fmt(c)}, {b}, {n}\n")
    if args.o:
        out.close()


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Precompute monthly average create-to-closed time (hours) per zipcode.

Rows are skipped if they have no 5-digit zipcode, no closed date, or a closed
date before the created date. Each incident is assigned to the month it was
closed. Output columns: zipcode, month, avg_hours, count. The zipcode "ALL"
holds the overall average across every zipcode.
"""
import argparse
import csv
from collections import defaultdict
from datetime import datetime


def parse(s):
    # format: MM/DD/YYYY HH:MM:SS AM  (fast manual parse)
    m, d, y = int(s[0:2]), int(s[3:5]), int(s[6:10])
    hh, mi, ss = int(s[11:13]), int(s[14:16]), int(s[17:19])
    if hh == 12:
        hh = 0
    if s[20:22] == "PM":
        hh += 12
    return datetime(y, m, d, hh, mi, ss)


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("-i", required=True, help="trimmed 2024 311 csv")
    ap.add_argument("-o", default="monthly_response.csv", help="output csv")
    args = ap.parse_args()

    sums = defaultdict(float)
    counts = defaultdict(int)
    with open(args.i, newline="") as f:
        r = csv.reader(f)
        h = next(r)
        ci = h.index("Created Date")
        xi = h.index("Closed Date")
        zi = h.index("Incident Zip")
        for row in r:
            try:
                z = row[zi].strip()[:5]
                if len(z) != 5 or not z.isdigit() or not row[xi].strip():
                    continue
                c, x = parse(row[ci]), parse(row[xi])
            except (ValueError, IndexError):
                continue
            hrs = (x - c).total_seconds() / 3600
            if hrs < 0:
                continue
            month = f"{x.year}-{x.month:02d}"
            for key in (("ALL", month), (z, month)):
                sums[key] += hrs
                counts[key] += 1

    with open(args.o, "w", newline="") as out:
        w = csv.writer(out)
        w.writerow(["zipcode", "month", "avg_hours", "count"])
        for key in sorted(sums):
            w.writerow([key[0], key[1], round(sums[key] / counts[key], 3),
                        counts[key]])


if __name__ == "__main__":
    main()

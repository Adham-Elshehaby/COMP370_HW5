"""Bokeh dashboard: monthly average 311 create-to-closed time by zipcode.

Run with:  bokeh serve Bokeh      (monthly_response.csv, made by
preprocess.py, must sit next to this file or in the working directory)
"""
import csv
import os
from collections import defaultdict
from datetime import datetime

from bokeh.core.properties import value
from bokeh.io import curdoc
from bokeh.layouts import column
from bokeh.models import ColumnDataSource, Select
from bokeh.plotting import figure

YEAR = "2024"  # only months (of incident closure) in this year are plotted
HERE = os.path.dirname(os.path.abspath(__file__))
PATH = next(p for p in (os.path.join(HERE, "monthly_response.csv"),
                        "monthly_response.csv") if os.path.exists(p))

avg = defaultdict(dict)   # zipcode -> {month: avg hours}
total = defaultdict(int)  # zipcode -> number of incidents
with open(PATH, newline="") as f:
    for r in csv.DictReader(f):
        if not r["month"].startswith(YEAR):
            continue
        avg[r["zipcode"]][r["month"]] = float(r["avg_hours"])
        total[r["zipcode"]] += int(r["count"])

months = sorted(avg["ALL"])
dates = [datetime.strptime(m + "-01", "%Y-%m-%d") for m in months]
zips = sorted(z for z in avg if z != "ALL")
busiest = sorted(zips, key=lambda z: -total[z])


def ys(z):
    return [avg[z].get(m, float("nan")) for m in months]


z1, z2 = busiest[0], busiest[1]
src_all = ColumnDataSource(dict(x=dates, y=ys("ALL")))
src1 = ColumnDataSource(dict(x=dates, y=ys(z1)))
src2 = ColumnDataSource(dict(x=dates, y=ys(z2)))

p = figure(title=f"Monthly average 311 response time, {YEAR}",
           x_axis_type="datetime", width=900, height=450,
           x_axis_label="Month incident was closed",
           y_axis_label="Average create-to-closed time (hours)")
p.line("x", "y", source=src_all, line_width=3, color="black",
       legend_label="All zipcodes")
p.line("x", "y", source=src1, line_width=2, color="royalblue",
       legend_label=f"Zipcode {z1}")
p.line("x", "y", source=src2, line_width=2, color="crimson",
       legend_label=f"Zipcode {z2}")
p.legend.location = "top_left"

sel1 = Select(title="Zipcode 1", value=z1, options=zips)
sel2 = Select(title="Zipcode 2", value=z2, options=zips)


def update(attr, old, new):
    a, b = sel1.value, sel2.value
    src1.data = dict(x=dates, y=ys(a))
    src2.data = dict(x=dates, y=ys(b))
    items = p.legend[0].items
    items[1].label = value(f"Zipcode {a}")
    items[2].label = value(f"Zipcode {b}")


sel1.on_change("value", update)
sel2.on_change("value", update)

curdoc().title = "311 response time by zipcode"
curdoc().add_root(column(sel1, sel2, p))

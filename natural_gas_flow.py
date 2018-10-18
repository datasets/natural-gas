import datetime
import os

from dataflows import Flow, validate, update_resource
from dataflows import add_metadata, dump_to_path, load, set_type, printer


def format_date(row):
    if row.get('Date'):
        # Float returned by XLS file is exactly 693594 less then ordinal number in python
        formated_date = datetime.date(1997, 1, 7).fromordinal(int(row.get('Date') + 693594))
        row['Date'] = formated_date
    if row.get('Month'):
        formated_date = datetime.date(1997, 1, 7).fromordinal(int(row.get('Month') + 693594)).strftime('%Y-%m')
        row['Month'] = formated_date


natural_gas = Flow(
    add_metadata(
        name="natural-gas",
        title= "Natural gas prices",
        descriptor="Monthly and daily prices of Natural Gas",
        version="0.2.0",
        sources=[
            {
                "name": "EIA",
                "path": "http://www.eia.gov/naturalgas",
                "title": "EIA"
            }
        ],
        licenses=[
            {
                "name": "ODC-PDDL-1.0",
                "path": "http://opendatacommons.org/licenses/pddl/",
                "title": "Open Data Commons Public Domain Dedication and License v1.0"
            }
        ],
        keywords=["Gas","Natural gas","Natural gas daily","Natural gas monthly","eia","Natural gas eia"],
        views=[
            {
                "name": "graph",
                "title": "Prices of Natural Gas",
                "specType": "simple",
                "spec": {
                    "type": "line",
                    "group": "Date",
                    "series": ["Price"]
              }
            }
        ]
    ),
    load(
        load_source='http://www.eia.gov/dnav/ng/hist_xls/RNGWHHDd.xls',
        format='xls',
        sheet=2,
        skip_rows=[1,2,3,-1],
        headers=['Date', 'Price'],
        name='daily'
    ),
    load(
        load_source='http://www.eia.gov/dnav/ng/hist_xls/RNGWHHDm.xls',
        format='xls',
        sheet=2,
        skip_rows=[1,2,3,-1],
        headers=['Month', 'Price'],
        name='mothly'
    ),
    format_date,
    set_type('Date', resources='daily', type='date'),
    set_type('Month',resources='monthly', type='yearmonth'),
    update_resource('daily', **{'path':'data/daily.csv', 'dpp:streaming': True}),
    update_resource('monthly', **{'path':'data/monthly.csv', 'dpp:streaming': True}),
    validate(),
    printer(),
    dump_to_path(),
)


def flow(parameters, datapackage, resources, stats):
    return natural_gas


if __name__ == '__main__':
    natural_gas.process()

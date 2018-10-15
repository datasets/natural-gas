import datetime

from dataflows import Flow, PackageWrapper, ResourceWrapper, validate
from dataflows import add_metadata, dump_to_path, load, set_type, printer


def rename_resources(package: PackageWrapper):
    package.pkg.descriptor['resources'][0]['name'] = 'natural-gas-daily'
    package.pkg.descriptor['resources'][0]['path'] = 'data/natural-gas-daily.csv'
    package.pkg.descriptor['resources'][1]['name'] = 'natural-gas-monthly'
    package.pkg.descriptor['resources'][1]['path'] = 'data/natural-gas-monthly.csv'
    yield package.pkg
    res_iter = iter(package)
    res_iter = iter(package)
    for res in  res_iter:
        yield res.it
    yield from package


def format_date(row):
    if row.get('Date'):
        # Float returned by XLS file is exactly 693594 less then ordinal number in python
        pre_date = datetime.date(1997, 1, 7).fromordinal(int(row.get('Date') + 693594))
        formated_date = datetime.datetime.strptime((str(pre_date)), "%Y-%m-%d").strftime('%Y-%m-%d')
        row['Date'] = formated_date
    if row.get('Month'):
        pre_date = datetime.date(1997, 1, 7).fromordinal(int(row.get('Month') + 693594))
        formated_date = datetime.datetime.strptime((str(pre_date)), "%Y-%m-%d").strftime('%Y-%m')
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
        skip_rows=[1,2,3],
        headers=['Date', 'Price']
    ),
    load(
        load_source='http://www.eia.gov/dnav/ng/hist_xls/RNGWHHDm.xls',
        format='xls',
        sheet=2,
        skip_rows=[1,2,3],
        headers=['Month', 'Price']
    ),
    rename_resources,
    format_date,
    set_type('Date', resources='natural-gas-daily', type='date', format='any'),
    set_type('Month',resources='natural-gas-monthly', type='yearmonth'),
    validate(),
    printer(),
    dump_to_path(),
)


if __name__ == '__main__':
    natural_gas.process()

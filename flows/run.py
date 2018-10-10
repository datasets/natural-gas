from dataflows import Flow, PackageWrapper, ResourceWrapper, validate
from dataflows import add_metadata, dump_to_path, load, set_type, printer


def rename_resources(package: PackageWrapper):
    package.pkg.descriptor['resources'][0]['name'] = 'natural-gas-daily'
    package.pkg.descriptor['resources'][0]['path'] = 'data/natural-gas-daily.csv'
    package.pkg.descriptor['resources'][1]['name'] = 'natural-gas-monthly'
    package.pkg.descriptor['resources'][1]['path'] = 'data/natural-gas-monthly.csv'
    yield package.pkg
    res_iter = iter(package)
    first: ResourceWrapper = next(res_iter)
    second: ResourceWrapper = next(res_iter)
    yield first.it
    yield second.it
    yield from package


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
        skip_rows=3,
        headers=['Date', 'Price']
    ),
    load(
        load_source='http://www.eia.gov/dnav/ng/hist_xls/RNGWHHDm.xls',
        format='xls',
        sheet=2,
        skip_rows=3,
        headers=['Month', 'Price']
    ),
    # set_type('Date', type='date', format='any'),
    # set_type('Month', type='yearmonth'),
    # set_type('Price', type='float'),
    rename_resources,
    validate(),
    printer(),
    dump_to_path(),
)


if __name__ == '__main__':
    natural_gas.process()

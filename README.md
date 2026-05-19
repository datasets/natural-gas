<a className="gh-badge" href="https://datahub.io/core/natural-gas"><img src="https://badgen.net/badge/icon/View%20on%20datahub.io/orange?icon=https://datahub.io/datahub-cube-badge-icon.svg&label&scale=1.25" alt="badge" /></a>

Time series of major Natural Gas Prices including US Henry Hub. Data comes from U.S. Energy Information Administration [EIA](http://www.eia.gov/)

## Data

Dataset contains Monthly and Daily prices of Natural gas, starting from January 1997 to current year. Prices are in nominal dollars.

Three files are provided:

- `data/daily.csv` — one row per trading day (weekends and US holidays excluded)
- `data/monthly.csv` — monthly averages in `YYYY-MM` format
- `data/monthly-processed.csv` — same monthly data with dates expressed as the first day of each month (`YYYY-MM-DD`), suitable for charting tools that require full date values

## Preparation

You will need Python 3.12 or greater. Install dependencies and run:

```bash
cd scripts
pip install -r requirements.txt
make
```

Processed data is written to `../data/`.

## License

* Public domain and use of EIA content

U.S. government publications are in the public domain and are not subject to copyright protection. One may use and/or distribute any of data,
files, databases, reports, graphs, charts, and other information products that are on website.
For more information please visit: [Copyrights and Reuse](http://www.eia.gov/about/copyrights_reuse.cfm)

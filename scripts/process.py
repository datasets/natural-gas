import urllib

def retrieve():
    daily = 'http://www.eia.gov/dnav/ng/hist_xls/RNGWHHDd.xls'
    weekly = 'http://www.eia.gov/dnav/ng/hist_xls/RNGWHHDm.xls'
    dest = os.path.join('archive', 'eia-daily.xls')
    urllib.urlretrieve(daily, dest)
    dest = os.path.join('archive', 'eia-monthly.xls')

def extract():
    pass


#!/usr/bin/python
# -*- coding: utf8 -*-

import urllib
import os
import datetime
import csv
import xlrd

def setup():
	'''Crates the directorie for archive if they don't exist
	'''
	if not os.path.exists('../archive'):
		os.mkdir('../archive')

def retrieve():
    '''Downloades xls data to archive directory
    '''
    source_daily = 'http://www.eia.gov/dnav/ng/hist_xls/RNGWHHDd.xls'
    source_monthly = 'http://www.eia.gov/dnav/ng/hist_xls/RNGWHHDm.xls'

    daily_dest = os.path.join('../archive', 'natural-gas-daily.xls')
    urllib.urlretrieve(source_daily, daily_dest)
    monthly_dest = os.path.join('../archive', 'natural-gas-monthly.xls')
    urllib.urlretrieve(source_monthly, monthly_dest)
    return daily_dest, monthly_dest

def get_data(dest):
    '''Gets the data from xls file and returns a ictionery of countries lists of it's data by year
    '''
    with xlrd.open_workbook(dest) as xls_data:
        sheet = xls_data.sheet_by_index(1)
        col_num = sheet.ncols
        row_num = sheet.nrows
        data = []
        for row in range(3, row_num):
            for col in range(col_num):
                if col < 1:
                    # Float returned by XLS file is exactly 693594 less then ordinal number in python
                    formated_date = datetime.date(1997, 1, 7).fromordinal(int(sheet.cell_value(row, col) + 693594))
                else:
                    price = sheet.cell_value(row, col)
            data.append([formated_date,price])
        return data

def process(data_dest):
    '''takes dictionery of data as input and writes data into csv file

    '''
    if 'month' in data_dest:
        title = 'natural-gas-monthly.csv'
    else:
        title = 'natural-gas-daily.csv'
    header = ['Date', 'Price']
    data = get_data(data_dest)
    with open('../data/' + title, 'w') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(header)
        for row in data:
            csv_writer.writerow(row)

if __name__ == '__main__':
    setup()
    dests = retrieve()
    for dest in dests:
        process(dest)

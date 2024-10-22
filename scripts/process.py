#!/usr/bin/python
# -*- coding: utf8 -*-

import os
import csv
import xlrd
import json
import datetime
import requests

def setup():
    '''
        Creates the archive directory if it doesn't exist
    '''
    archive_dir = os.path.join(os.path.dirname(__file__), '..', 'archive')
    if not os.path.exists(archive_dir):
        os.mkdir(archive_dir)

def retrieve():
    '''
        Downloads the xls files from the source and returns the destination of the files
    '''
    source_daily = 'http://www.eia.gov/dnav/ng/hist_xls/RNGWHHDd.xls'
    source_monthly = 'http://www.eia.gov/dnav/ng/hist_xls/RNGWHHDm.xls'

    archive_dir = os.path.join(os.path.dirname(__file__), '..', 'archive')

    daily_dest = os.path.join(archive_dir, 'natural-gas-daily.xls')
    response_daily = requests.get(source_daily)
    with open(daily_dest, 'wb') as daily_file:
        daily_file.write(response_daily.content)
    
    monthly_dest = os.path.join(archive_dir, 'natural-gas-monthly.xls')
    response_monthly = requests.get(source_monthly)
    with open(monthly_dest, 'wb') as monthly_file:
        monthly_file.write(response_monthly.content)

    return daily_dest, monthly_dest

def get_data(dest, format):
    '''
        Gets the data from xls file and returns a list of lists
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
                    raw_date = datetime.date(1997, 1, 7).fromordinal(int(sheet.cell_value(row, col) + 693594))
                    
                    # Check the format and apply formatting
                    if format == 'monthly':
                        formated_date = raw_date.strftime('%Y-%m')  # YYYY-MM format
                    elif format == 'daily':
                        formated_date = raw_date.strftime('%Y-%m-%d')  # YYYY-MM-DD format
                    else:
                        raise ValueError("Invalid format: Please choose 'monthly' or 'daily'")
                else:
                    price = sheet.cell_value(row, col)
            data.append([formated_date, price])
        return data

def update_datapackage():
    '''
        Updates the datapackage.json file with the new data
    '''
    data_dir = os.path.join(os.path.dirname(__file__), '..', 'data')
    
    with open(os.path.join(data_dir, 'daily.csv'), 'r') as csv_file:
        daily_len = len(csv_file.readlines()) - 1
    with open(os.path.join(data_dir, 'monthly.csv'), 'r') as csv_file:
        monthly_len = len(csv_file.readlines()) - 1   

    # Count total size and len of rows in both files    
    total_len = daily_len + monthly_len
    total_size = os.path.getsize(os.path.join(data_dir, 'daily.csv')) + os.path.getsize(os.path.join(data_dir, 'monthly.csv'))

    # Append values to the datapackage.json file
    with open(os.path.join(os.path.dirname(__file__), '..', 'datapackage.json'), 'r') as json_file:
        data = json.load(json_file)
        data['count_of_rows'] = total_len
        data['bytes'] = total_size

    with open(os.path.join(os.path.dirname(__file__), '..', 'datapackage.json'), 'w') as json_file:
        json.dump(data, json_file, indent=2)
        
def process(data_dest):
    '''
        Processes the data and writes it to a csv file
    '''
    data_dir = os.path.join(os.path.dirname(__file__), '..', 'data')

    if 'month' in data_dest:
        header = ['Month', 'Price']
        title = 'monthly.csv'
        data = get_data(data_dest, 'monthly')
    else:
        title = 'daily.csv'
        header = ['Date', 'Price']
        data = get_data(data_dest, 'daily')

    with open(os.path.join(data_dir, title), 'w') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(header)
        for row in data:
            csv_writer.writerow(row)

if __name__ == '__main__':
    setup()
    dests = retrieve()
    for dest in dests:
        process(dest)
    update_datapackage()

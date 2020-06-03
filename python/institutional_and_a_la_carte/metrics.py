#!/usr/bin/env python3

import requests
import os
import csv
import ast

##############################################################################################
# Thanks for your interest in New Constructs!
# This file demonstrates requesting data for MSFT from our metrics API.
# For information on all our datasets, see:
# https://www.newconstructs.com/data
# https://client.newconstructs.com/nc/documentation/api.htm
#
# Need an API key?
# Request one by emailing us at support@newconstructs.com .
##############################################################################################

API_BASE_URL = 'https://api.newconstructs.com/v1'
API_KEY = 'YOUR_KEY_HERE'

# There are two endpoints in our metrics API: roic and ebv
ENDPOINT = 'roic'

def load_data_to_csv():
  final_csv = '/tmp/new_constructs_{}_metrics_sample.csv'.format(ENDPOINT)
  nc_endpoint = 'metrics/{}'.format(ENDPOINT)

  tickers = ['MSFT']
  years = [2017]
  periods = {
    'annual': [5],
    'quarter': [1, 2, 3, 4],
    'ttm': [1, 2, 3, 4],
  }
  datapoints = ['ROIC', 'NOPAT']
  
  headers = {
    'x-api-key': API_KEY,
    'accept': 'application/json',
    'content-type': 'application/json'
  }
  
  data = []
 
  for ticker in tickers:
    print('Requesting data for {}...'.format(ticker))
    for year in years:
      for period_type in periods.keys():
        for period in periods.get(period_type):
          for datapoint in datapoints:
              data += get_data(headers, nc_endpoint, ticker, year, period_type, period, datapoint)

  write_results_to_csv(final_csv, data, header=['ticker', 'year', 'period', 'periodtype', 'periodstring', 'datapoint', 'datavalue'], truncate=True, delimiter=',')


def get_data(headers, nc_endpoint, ticker, year, period_type, period, datapoint):
  url = '{}/{}/{}?datapoint={}&year={}'.format(API_BASE_URL, nc_endpoint, ticker, datapoint, year)
  url_period = '' if period_type == 'annual' else '&{}={}'.format(period_type, period)

  data = []
  response = requests.get(url='{}{}'.format(url, url_period), headers=headers)
        
  if response.status_code != 200:
    print('Ticker {}, datapoint {}, year {}, periodtype {}, period {}: {}'.format(ticker, datapoint, year, period_type.upper(), period, response.json()['message']))
    return [[ticker, year, period, period_type.upper(), '', datapoint, 'NA']]
  else:
    response_json = response.json()
    body = ast.literal_eval(response_json.get('body', {}))
    results = body.get('results')
    for result in results:
      data.append([result['ticker'], result['year'], result['period'], result['periodtype'], result['periodstring'], result['datapoint'], result['datavalue']])
    
    return data


def write_results_to_csv(file_name, results, header=None, truncate=False, delimiter=','):
  if not file_name:
    return

  # if the directory does not exist, make it
  save_dir = os.path.dirname(file_name)
  if not os.path.exists(save_dir):
    os.makedirs(save_dir)

  open_type = 'w' if truncate else 'a'
  with open(file_name, open_type) as out:
    csv_out = csv.writer(out, delimiter=delimiter)
    if os.stat(file_name).st_size <= 0:
      csv_out.writerow(header)
    for row in results:
      csv_out.writerow(row)
    out.close()
  
  
if __name__ == '__main__':
  load_data_to_csv()

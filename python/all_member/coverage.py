#!/usr/bin/env python3

import requests
import os
import csv
import ast

##############################################################################################
# Thanks for your interest in New Constructs!
# This file demonstrates requesting data for some example tickers from our coverage API.
# For information on all our datasets, see:
# https://www.newconstructs.com/data
# https://client.newconstructs.com/nc/documentation/api.htm
#
# Need an API key?
# Request one at https://client.newconstructs.com/nc/documentation/api/installation.htm
##############################################################################################

API_BASE_URL = 'https://api.newconstructs.com/v1'
API_KEY = 'YOUR_KEY_HERE'

def load_data_to_csv():
  final_csv = '/tmp/new_constructs_coverage_sample.csv'
  nc_endpoint = 'coverage'
  
  tickers = [
    ('stock', 'AAPL'),
    ('stock', 'NFLX'),
    ('etf', 'XLF'),
    ('etf', 'QQQ'),
    ('mf', 'GAFFX'),
    ('mf', 'AUENX')
  ]
  
  headers = {
    'x-api-key': API_KEY,
    'accept': 'application/json',
    'content-type': 'application/json'
  }
  
  data = []
  
  for type, ticker in tickers:
    print('Requesting data for {}...'.format(ticker))
    data.append(get_data(headers, nc_endpoint, type, ticker))
  
  write_results_to_csv(final_csv, data,
                       header=['ticker', 'name', 'type', 'sector', 'sector_name', 'subsector', 'subsector_name', 'industry', 'industry_name', 'subindustry', 'subindustry_name',
                               'last_trade_date'], truncate=True, delimiter=',')


def get_data(headers, nc_endpoint, type, ticker):
  url = '{}/{}/{}/{}'.format(API_BASE_URL, nc_endpoint, type, ticker)
  
  response = requests.get(url=url, headers=headers)
  
  if response.status_code != 200:
    print('Ticker {}: {}'.format(ticker, response.json()['message']))
    return [ticker, 'Not found']
  else:
    response_json = response.json()
    body = ast.literal_eval(response_json.get('body', {}).replace('null', '"NA"'))
    results = body.get('results')
    result = results[0]
    
    return [result['ticker'], result['name'], result['type'], result['sector'], result['sector_name'], result['subsector'], result['subsector_name'], result['industry'],
            result['industry_name'], result['subindustry'], result['subindustry_name'], result['last_trade_date']]


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

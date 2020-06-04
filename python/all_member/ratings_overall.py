#!/usr/bin/env python3

import requests
import os
import csv
import ast

################################################################################################
# Thanks for your interest in New Constructs!
# This file demonstrates requesting data for some example tickers from our overall ratings API.
# For information on all our datasets, see:
# https://www.newconstructs.com/data
# https://client.newconstructs.com/nc/documentation/api.htm
#
# Need an API key?
# Request one at https://client.newconstructs.com/nc/documentation/api/installation.htm
################################################################################################

API_BASE_URL = 'https://api.newconstructs.com/v1'
API_KEY = 'YOUR_KEY_HERE'

def load_data_to_csv():
  final_csv = '/tmp/new_constructs_ratings_overall_sample.csv'
  nc_endpoint = 'ratings/overall'
  
  tickers = ['AAPL', 'NFLX', 'XLF', 'QQQ', 'GAFFX', 'AUENX']
  
  headers = {
    'x-api-key': API_KEY,
    'accept': 'application/json',
    'content-type': 'application/json'
  }
  
  data = []
  
  for ticker in tickers:
    print('Requesting data for {}...'.format(ticker))
    data.append(get_data(headers, nc_endpoint, ticker))
  
  write_results_to_csv(final_csv, data, header=['ticker', 'name', 'rating_overall'], truncate=True, delimiter=',')


def get_data(headers, nc_endpoint, ticker):
  url = '{}/{}/{}'.format(API_BASE_URL, nc_endpoint, ticker)
  
  response = requests.get(url=url, headers=headers)
  
  if response.status_code != 200:
    print('Ticker {}: {}'.format(ticker, response.json()['message']))
    return [ticker, 'Not found']
  else:
    response_json = response.json()
    body = ast.literal_eval(response_json.get('body', {}))
    result = body.get('results')
    
    return [result['ticker'], result['name'], result['rating_overall']]


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


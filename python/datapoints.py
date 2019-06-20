#!/usr/bin/env python3

import requests
import os
import csv
import ast

################################################################################################
# Thanks for your interest in New Constructs!
# This file demonstrates requesting data from our datapoints API.
# For information on all our datasets, see:
# https://www.newconstructs.com/data
# https://client.newconstructs.com/nc/documentation/api.htm
#
# Need an API key?
# Request one by emailing us at support@newconstructs.com .
################################################################################################

API_BASE_URL = 'https://api.newconstructs.com/v1'
API_KEY = 'YOUR_KEY_HERE'

def load_data_to_csv():
  final_csv = '/tmp/new_constructs_datapoints_sample.csv'
  
  datapoints = ['ACCOUNTS_PAYABLE', 'ACCOUNTS_RECEIVABLE', 'ROIC_WAVG']
  
  headers = {
    'x-api-key': API_KEY,
    'accept': 'application/json',
    'content-type': 'application/json'
  }
  
  data = []

  for datapoint in datapoints:
    print('Requesting information for {}...'.format(datapoint))
    data.append(get_datapoint(headers, datapoint))
  
  write_results_to_csv(final_csv, data, header=['name', 'description', 'endpoints'], truncate=True, delimiter=',')


def get_datapoint(headers, datapoint):
  url = '{}/{}/{}'.format(API_BASE_URL, 'datapoint', datapoint)
  response = requests.get(url=url, headers=headers)
  
  if response.status_code != 200:
    print('Datapoint {}: {}'.format(datapoint, response.json()['message']))
    return [datapoint, 'Not found']
  else:
    response_json = response.json()
    body = ast.literal_eval(response_json.get('body', {}))
    results = body.get('results')
    
    return [results['api_data_key_name'], results['description'], results['endpoints']]


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

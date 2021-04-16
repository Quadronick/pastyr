#! /usr/bin/env python

import argparse
import json
import requests

parser = argparse.ArgumentParser(description='Simple CLI stock portfolio keeper')
parser.add_argument('--list', action='store_true', help='Show information about all available assets.')
parser.add_argument('--import', action='store_true', help='Import whole data as a JSON.')
parser.add_argument('--buy', action='store_true', help='Enter information on assets purchased.')
parser.add_argument('--ticker', '-t', help='Asset ID')
parser.add_argument('--price', '-p', help="Asset's price")
parser.add_argument('--quantity', '-q', help='Number of an assets')
parser.add_argument('--currency', '-c', help='Currency used to buy assets.')
parser.add_argument('--sell', action='store_true', help='Enter information on assets sold.')
parser.add_argument('--init', action='store', help='Initialaze brave new config with you API key.')
args = parser.parse_args()


def add_to_config(deal_info, flag='a'):
    with open('config.json', flag) as json_file:
        json.dump(deal_info, json_file)


def read_from_config():
    with open('config.json') as json_file:
        return json.load(json_file)


def search_symbol(symbol, api_key):
    """Search for symbol in supported markets and output
       the list of best matches.
    """
    output = requests.get('https://www.alphavantage.co/query?function=SYMBOL_SEARCH&keywords='
                           + symbol + '&apikey=' + api_key)
    return list(output.json()['bestMatches'])


def get_current_price(symbol, api_key):
    """Get current stock price"""
    output = requests.get('https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol='
                          + symbol + '&apikey=' + api_key)
    return output.json()['Global Quote']['05. price']


def search_asset(config, asset_type, asset_id):
    return bool(asset_id in config['assets'][asset_type])


def add_asset(data, asset_type, ticker, price, quant, curr):
    if search_asset(data, asset_type, ticker):
        element_number = len(data['assets'][asset_type][ticker])
        data['assets'][asset_type][ticker].update({str(element_number + 1): {'price': price, 'quant': quant}})
    else:
        data['assets'][asset_type].update({ticker: {}, 'currency': curr})
        data['assets'][asset_type][ticker].update({'1': {'price': price, 'quant': quant}})
    add_to_config(data, 'w')


def init_config(api_key):
    """
       Initialize clean configuration file. API key required
    """
    return {'assets': { 'stocks': {} }, 'api': api_key}

structure = read_from_config()

if args.init:
    add_to_config(init_config(args.init), 'w')
if args.buy:
    add_asset(structure, 'stocks', args.ticker, args.price, args.quantity, args.currency)

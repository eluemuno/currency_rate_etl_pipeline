import json
import logging
from dotenv import load_dotenv
import requests
import os
import sys
import datetime

load_dotenv()

ROOT_DIR = sys.prefix.rpartition('/')[0]

logging.basicConfig(level=logging.INFO, filename=ROOT_DIR + '/logs/extract_and_queue_log_'
                                                 + datetime.datetime.now().strftime('%Y%m%d-%H%M%S') + '.txt',
                    format='%(process)d--%(asctime)s--%(levelname)s--%(message)s')


def get_random_currency_for_exchange():
    """extract a random  currency code from the prepopulated json file for comparism"""
    import json
    import random

    with open(ROOT_DIR + '/helpers/symbols.json') as symbols:
        currencies = json.load(symbols)

    to_currency = random.choice(list(currencies['symbols'].keys()))
    logging.info('random currency is:' + to_currency)
    return to_currency


def get_exchange_rate():
    to_curr = get_random_currency_for_exchange()

    base_url = 'https://api.exchangerate.host/'
    # https://api.exchangerate.host/convert?from=USD&to=EUR
    try:
        response = requests.get(base_url + 'convert?from=NGN&to=' + to_curr)
    except Exception as e:
        logging.error(e)
    else:
        logging.info('Exchangerate API endpoint [convert] returned status code: ' + str(response.status_code))
        # return response.json()
        return json.dumps(response.json(), indent=4)


def produce():
    import pika

    url = os.getenv('CLOUDAMQP_URL')
    params = pika.URLParameters(url)
    connection = pika.BlockingConnection(params)
    channel = connection.channel()

    data = get_exchange_rate()

    channel.basic_publish(exchange='', routing_key='nsukka', body=data)
    logging.info('Message queued, routing key: [nsukka].')
    connection.close()
    return


if __name__ == '__main__':
    produce()

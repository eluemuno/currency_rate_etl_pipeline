from helpers import db_ops
import json
from dotenv import load_dotenv
import logging
import datetime
import sys
import glob
import guid
import ast
import random

# print(db_ops.get_db()['API']['books'])

load_dotenv()

ROOT_DIR = sys.prefix.rpartition('/')[0]

logging.basicConfig(level=logging.INFO, filename=ROOT_DIR + '/logs/load_into_mongodb_log_'
                                                 + datetime.datetime.now().strftime('%Y%m%d-%H%M%S') + '.txt',
                    format='%(process)d--%(asctime)s--%(levelname)s--%(message)s')


def upload_data_to_mongo():
    file_path = glob.glob(ROOT_DIR + '/logs/co*')[0]
    date_stamp = datetime.datetime.now().strftime('%y%m%d')
    rand_alphabet = random.choice('abcdefghijklmnopqrstuvwxyz')
    guid_ = guid.guid.GUID()
    insert_id = 'ICE' + guid_ + rand_alphabet + date_stamp
    data_for_upload = []
    with open(str(file_path), 'r') as f:
        logging.info('Logfile opened')
        for line in f:
            if 'msg' in line:
                msg_to_consume = line.split('"motd":')[1].replace('\\n', '').replace('        ', ' ') \
                    .replace('    ', ' ').replace('\n', '').split("'")[0]
                # msg_to_consume = '{ "head" : ' + msg_to_consume
                msg_to_consume = '{ "head" : ' + msg_to_consume
                amount = msg_to_consume.split('}')[1].split(':')[-1]
                rate = msg_to_consume.split('}')[2].split('{')[-1].split(':')[-1].strip()
                new_amount = '"'.join(amount)
                new_rate = '"' + rate + '"'
                msg_to_consume = msg_to_consume.replace(amount, new_amount)
                msg_to_consume = msg_to_consume.replace(rate, new_rate)
                msg_to_consume = json.loads(msg_to_consume)
                try:
                    collection = db_ops.get_db()['books']
                    collection.insert_one(msg_to_consume)
                    # collection.insert_one({"_id": 5, "user_name": "ice"})
                except Exception as err:
                    print(err)
                logging.info('Database updated')
                logging.info(msg_to_consume)
        return


if __name__ == '__main__':
    upload_data_to_mongo()

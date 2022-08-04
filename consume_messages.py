import os
import pika
from dotenv import load_dotenv
import logging
import datetime
import sys
import time

load_dotenv()

ROOT_DIR = sys.prefix.rpartition('/')[0]

logging.basicConfig(level=logging.INFO, filename=ROOT_DIR + '/logs/consume_messages_log_'
                                                 + datetime.datetime.now().strftime('%Y%m%d-%H%M%S') + '.txt',
                    format='%(process)d--%(asctime)s--%(levelname)s--%(message)s')

url = os.getenv('CLOUDAMQP_URL')
params = pika.URLParameters(url)
connection = pika.BlockingConnection(params)
channel = connection.channel()
channel.basic_qos(prefetch_count=1)

channel.queue_declare(queue='nsukka')


def callback(ch, method, properties, body):
    with open('received.txt', 'wb') as f:
        # f.write(body)
        f.write(body + b',')
    logging.info('[x] Received {}'.format(body))
    return


channel.basic_consume(on_message_callback=callback, queue='nsukka', auto_ack=False)


# channel.basic_consume(callback=callback, queue='nsukka', no_ack=True)


def stop_consuming():
    import subprocess
    import signal
    import os
    file_name = str(__file__).split('/')[-1]
    process_list = subprocess.Popen(['ps', '-A'], stdout=subprocess.PIPE)
    output, error = process_list.communicate()
    for line in output.splitlines():
        line = bytes.decode(line)
        if 'python' in line and file_name in line:
            pid = int(line.split(None, 1)[0])
            logging.info('Initiating kill command on : {}'.format(pid))
            os.kill(pid, signal.SIGKILL)
        return


# channel.start_consuming()
# time.sleep(5)
# channel.close()
# connection.close()

if __name__ == '__main__':
    channel.start_consuming()
    connection.close()
    # stop_consuming()
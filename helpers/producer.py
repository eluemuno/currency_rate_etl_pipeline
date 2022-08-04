import json

import pika, os, logging
from dotenv import load_dotenv

load_dotenv()

url = os.getenv('CLOUDAMPQ_URL')
params = pika.URLParameters(url)
connection = pika.BlockingConnection(params)
channel = connection.channel()

# books = {
#     "name": "Things Fall Apart",
#     "author": "Chinua Achebe",
#     "remark": "Great!!"
# }



books = json.dumps(data)

channel.basic_publish(exchange='', routing_key='nsukka', body=data)
print('Message Sent...')
connection.close()
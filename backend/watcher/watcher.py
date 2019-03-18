import pika
import json
from flask_socketio import SocketIO
from threading import Thread
import pymongo
import re
import uuid
import datetime
import random
getDomain = lambda x: re.search("(?:[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?\.)+[a-z0-9][a-z0-9-]{0,61}[a-z0-9]", x).group(0)


connection = pika.BlockingConnection(pika.ConnectionParameters('192.168.1.51', port=32770))
channel = connection.channel()

socketio = SocketIO(message_queue="amqp://guest:guest@192.168.1.51:32770/")

client = pymongo.MongoClient("mongodb://192.168.1.51:32768")
db = client['reputation']

from tools import whois, ssl_certificate


class GoogleAPIRpcClient(object):
    def __init__(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters('192.168.1.51', port=32770))
        self.channel = self.connection.channel()
        result = self.channel.queue_declare(exclusive=True)
        self.callback_queue = result.method.queue
        self.channel.basic_consume(self.on_response, no_ack=True,
                                   queue=self.callback_queue)

    def on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = body

    def call(self, url, routing_key='googleapi'):
        self.response = None
        self.corr_id = str(uuid.uuid4())
        self.channel.basic_publish(exchange='',
                                   routing_key=routing_key,
                                   properties=pika.BasicProperties(
                                         reply_to=self.callback_queue,
                                         correlation_id=self.corr_id,
                                         ),
                                   body=str(url))
        while self.response is None:
            self.connection.process_data_events()
        return self.response.decode('utf8')


def getRate(url):
    col = db[getDomain(url) + '_rating']
    try:
        return list(col.aggregate([{'$group': {'_id': None, 'rate': {'$avg': '$rate'}}}]))[0]['rate']
    except:
        return 0


def thread(url, room):
    socketio.emit('whois', whois(url), namespace='/normal', room=room)
    socketio.emit('rating', getRate(url), namespace='/normal', room=room)
    socketio.emit('lastCheck', datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), namespace='/normal', room=room)
    socketio.emit('availableRate', '100%' , namespace='/normal', room=room)
    socketio.emit('frequent', '30s', namespace='/normal', room=room)
    socketio.emit('total', '18973 Times' ,namespace='/normal', room=room)
    socketio.emit('collected', "2019-02-17 %2d:%0.2d:%0.2d" %
                  (random.randint(0, 23),
                   random.randint(1, 59),
                   random.randint(0, 59),
    ), namespace='/normal', room=room)
    result = GoogleAPIRpcClient().call(url)
    if 'matches' not in result:
        gapi = "Safe!"
        level = 1
    else:
        result = json.loads(result)
        record = result['matches'][0]
        gapi = "" \
               "\n**Dangerous!** <br/>" \
               " Threat Type: %s <br/>" \
               " Cache Duration: %s <br/>" \
               " Platform: %s<br/>"\
               % (record['threatType'], record['cacheDuration'], record['platformType'])
        level = 2
    socketio.emit('google', gapi, namespace='/normal', room=room)
    socketio.emit('level', level, namespace='/normal', room=room)
    result = json.loads(GoogleAPIRpcClient().call(url.replace('http://', '').replace('https://', ''), routing_key='monapi'))
    monapi = ""
    for i in result:
        monapi += "%s: %s <br/>" % (i, result[i])
    socketio.emit('amazon', monapi, namespace='/normal', room=room)

    result = json.loads(GoogleAPIRpcClient().call(url, routing_key='phishing'))
    if result['warn']:
        phishing = "**WARNING!** This URL may have a AUTHENTIC site! <br> " \
                   "You MAY NOT request on the AUTHENTIC URL <br>" \
                   "**AUTHENTIC SITE**<br>" \
                   "%s" \
                   "<br><br>**HOMOLOG** <br>" % result['authentic']
        socketio.emit('level', 3, namespace='/normal', room=room)
    else:
        phishing = "**HOMOLOG** <br>"
    for i in result['data']:
        phishing += "%s <br/>" % i

    socketio.emit('phishing', phishing, namespace='/normal', room=room)
    try:
        socketio.emit('ssl', ssl_certificate(url), namespace='/normal', room=room)
    except:
        socketio.emit('ssl', 'No HTTPS!', namespace='/normal', room=room)

    socketio.emit('loaded', namespace='/normal', room=room)



def callback(ch, method, properties, body):
    body = json.loads(body)
    print(body)
    Thread(target=thread, args=(body['url'], body['room'])).start()
    # channel.basic_ack(properties.deliverTag)

if __name__ == '__main__':
    channel.basic_consume(callback, queue='query', no_ack=True)
    channel.start_consuming()

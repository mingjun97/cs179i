from flask_socketio import emit, join_room, leave_room, rooms
import json
import re
from .tools import url_validator
from .. import channel as rabbitMQ

from .. import socketio, reputationdb
from .tools import send_email

sample = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"

getDomain = lambda x: re.search("(?:[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?\.)+[a-z0-9][a-z0-9-]{0,61}[a-z0-9]", x).group(0)

@socketio.on('connect', '/normal')
def connected():
    pass


@socketio.on('query', '/normal')
def query(data):
    if url_validator(data):
        rabbitMQ.basic_publish(exchange='', routing_key='query', body=json.dumps({'url': data, 'room': rooms()[0]}))
    else:
        emit('invalid')


@socketio.on('rate', '/normal')
def rate(data):
    sid = rooms()[0]
    col = reputationdb[getDomain(data['url']) + '_rating']
    myquery = {'rater': sid}
    result = col.find(myquery)
    if result.count() == 0:
        col.insert({'rater': sid, 'rate': data['rate']})
    else:
        col.update(myquery, {'$set': {'rate': data['rate']}})


@socketio.on('subs', '/normal')
def send(data):
    send_email(data['email'], data['url'])

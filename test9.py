#!encoding=utf8
import re
from urllib.parse import urlparse
import urllib.request
import pika
import pymongo
import json

connection = pika.BlockingConnection(pika.ConnectionParameters('192.168.1.51', port=32770))
channel = connection.channel()

client = pymongo.MongoClient("mongodb://192.168.1.51:32768")
db = client['reputation']
col = db['phishing']

def parsing(aa):
    if aa.find('http://') == -1 and aa.find('https://') == -1:
        parsed_uri = urlparse('http://' + aa)
        result = parsed_uri.netloc
    else:
        parsed_uri = urlparse(aa)
        result = parsed_uri.netloc
    return result

def replace(aaa):
    ##url = aaa.replace('o','[o0]')
    result = list()
    for i in aaa:
        if i == 'o':
            result.append('[o0]{0,2}')
        elif i == '0':
            result.append('[o0]{0,2}')
        elif i == 'l':
            result.append('[1l]{0,2}')
        elif i == '1':
            result.append('[1l]{0,2}')
        elif i == 'u':
            result.append('[uv]{0,2}')
        elif i == 'v':
            result.append('[uv]{0,2}')
        elif i == 's':
            result.append(r'[s5]{0,2}')
        elif i == '5':
            result.append(r'[s5]{0,2}')
        elif i == '$':
            result.append('[s5]{0,2}')
        elif i == 'и':
            result.append('[nи]{0,2}')
        elif i == 'ɢ':
            result.append('[ɢg]{0,2}')
        elif i == '2':
            result.append('[2z]{0,2}')
        elif i == 'a':
            result.append('[ae]{0,2}')
        elif i == 'e':
            result.append('[ae]{0,2}')
        else:
            result.append(i)

    return ''.join(result)

def on_request(ch, method, props, body):
    url = parsing(body.decode('utf8'))
    # print('url:', url)
    # for i in col.find_one({'domain': response}):
    if col.count_documents({'domain': url}) == 0:
        col.insert_one({'domain': url})
    rurl = replace(url)
    # print(response)
    result = list()
    warn = False
    authentic = ''
    for i in col.find({'domain': {'$regex': rurl}}):
        if i['domain'] == url:
            continue
        if i.get('authentic', False):
            warn = True
            authentic = i['domain']
        result.append(i['domain'])
    ch.basic_publish(exchange='',
                     routing_key=props.reply_to,
                     properties=pika.BasicProperties(correlation_id = \
                                                         props.correlation_id),
                     body=json.dumps({"warn": warn, "data":result, 'authentic': authentic}))
    ch.basic_ack(delivery_tag = method.delivery_tag)

if __name__ == '__main__':
    channel.queue_declare('phishing')
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(on_request, queue='phishing')
    channel.start_consuming()
    # print(replace('http://www.google.com/ragafa'))

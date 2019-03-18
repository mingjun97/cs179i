import re
import urllib.request
import ssl
import json
import pika

connection = pika.BlockingConnection(pika.ConnectionParameters('192.168.1.51', port=32770))
channel = connection.channel()

def checkURL(url):
    API_KEY = "AIzaSyDZHBoHQkeoWkrhwmLJyTNbvr36i1KNBKs"
    apiurl = "https://safebrowsing.googleapis.com/v4/threatMatches:find?key=" + API_KEY
    reqbody = {
        'client': {
            'clientId': "179i",
            'clientVersion': "0.0.1"
        },
        'threatInfo': {
            'threatTypes': ['THREAT_TYPE_UNSPECIFIED',
                            'MALWARE','SOCIAL_ENGINEERING',
                            'UNWANTED_SOFTWARE','POTENTIALLY_HARMFUL_APPLICATION'],
            'platformTypes': ['ANY_PLATFORM'],
            'threatEntryTypes': ['URL'],
            'threatEntries': [{"url": url}]
        }
    }
    # print(reqbody)
    req = urllib.request.Request(apiurl)
    req.add_header('Content-Type', 'application/json')
#print (json.dumps(reqbody))
    response = urllib.request.urlopen(req, json.dumps(reqbody,ensure_ascii=False).encode("utf-8")).read()
    result = response.decode("utf-8")
    # print(result)
    return result

def on_request(ch, method, props, body):
    url = body.decode('utf8')
    # print('url:', url)
    response = checkURL(url)
    # print(response)
    ch.basic_publish(exchange='',
                     routing_key=props.reply_to,
                     properties=pika.BasicProperties(correlation_id = \
                                                         props.correlation_id),
                     body=response)
    ch.basic_ack(delivery_tag = method.delivery_tag)


if __name__ == '__main__':
    channel.queue_declare('googleapi')
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(on_request, queue='googleapi')
    channel.start_consuming()

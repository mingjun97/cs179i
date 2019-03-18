import urllib.request
import urllib.parse
import json
import re
import pika

connection = pika.BlockingConnection(pika.ConnectionParameters('192.168.1.51', port=32770))
channel = connection.channel()

def checkIP_Monapi(URL):
    content = urllib.request.urlopen('https://api.monapi.io/v1/ip/'+URL).read()
    content = content.decode('UTF-8')
    # print (json.dumps(content, indent=4, sort_keys=True))
    return content

def checkDomain_Monapi(URL):
    content = urllib.request.urlopen('https://api.monapi.io/v1/domain/'+(URL+'/').split('/')[0]).read()
    content = content.decode('UTF-8')
    # print (json.dumps(content, indent=4, sort_keys=True))
    return content

def is_domain(domain):
        domain_regex = re.compile(
            r'(?:[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?\.)+[a-z0-9][a-z0-9-]{0,61}[a-z0-9]',
            re.IGNORECASE)
        return True if domain_regex.match(domain) else False

def is_ipv4(address):
    ipv4_regex = re.compile(
        r'(?:25[0-5]|2[0-4]\d|[0-1]?\d?\d)(?:\.(?:25[0-5]|2[0-4]\d|[0-1]?\d?\d)){3}',
        re.IGNORECASE)
    return True if ipv4_regex.match(address) else False

def checkURL_Monapi(URL):
    if is_domain(URL):
        return checkDomain_Monapi(URL)
    elif is_ipv4(URL):
        return checkIP_Monapi(URL)
    else:
        print ("Wrong input")
        return ""



def on_request(ch, method, props, body):
    url = body.decode('utf8')
    # print('url:', url)
    try:
        response = checkURL_Monapi(url)
    except:
        response = json.dumps({'Message': 'Not Found!'})
    # print(response)
    ch.basic_publish(exchange='',
                     routing_key=props.reply_to,
                     properties=pika.BasicProperties(correlation_id = \
                                                         props.correlation_id),
                     body=response)
    ch.basic_ack(delivery_tag = method.delivery_tag)


if __name__ == '__main__':
    channel.queue_declare('monapi')
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(on_request, queue='monapi')
    channel.start_consuming()

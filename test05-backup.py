import urllib.request
import json
import re

def checkIP_Monapi(URL):
    content = urllib.request.urlopen('https://api.monapi.io/v1/ip/'+URL).read()
    content = json.loads(content.decode('UTF-8'))
    print (json.dumps(content, indent=4, sort_keys=True))
    return content

def checkDomain_Monapi(URL):
    content = urllib.request.urlopen('https://api.monapi.io/v1/domain/'+URL).read()
    content = json.loads(content.decode('UTF-8'))
    print (json.dumps(content, indent=4, sort_keys=True))
    return content

def is_domain(domain):
        domain_regex = re.compile(
            r'(?:[A-Z0-9_](?:[A-Z0-9-_]{0,247}[A-Z0-9])?\.)+(?:[A-Z]{2,6}|[A-Z0-9-]{2,}(?<!-))\Z', 
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
        return 1



#TestTestTest
checkURL_Monapi('8.8.4.4')


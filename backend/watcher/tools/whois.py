import re
from os import popen


def whois(url):
    url = re.search("(?:[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?\.)+[a-z0-9][a-z0-9-]{0,61}[a-z0-9]", url).group(0)
    return popen('whois %s' % url).read().replace("\n", "<br/>")

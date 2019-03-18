import ssl
import M2Crypto
import re


def ssl_certificate(url):
    url = re.search("(?:[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?\.)+[a-z0-9][a-z0-9-]{0,61}[a-z0-9]", url).group(0)
    cert = ssl.get_server_certificate((url, 443))
    x509 = M2Crypto.X509.load_cert_string(cert)
    return x509.get_subject().as_text().replace(',', '<br/>').replace('C=', "Country: ")\
        .replace('ST=', "State: ") \
        .replace('L=', "Local: ") \
        .replace('O=', "Organization: ") \
        .replace('CN=', "Certificate Issued To: ")


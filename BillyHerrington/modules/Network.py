import socket
import http.client
import re
from uuid import getnode as mac
import constants


def getIpMac():
    white_ip = socket.gethostbyname(socket.gethostname())

    conn = http.client.HTTPConnection("ifconfig.me")
    conn.request("GET", "/ip")
    gray_ip = conn.getresponse().read().decode()

    MAC = ':'.join(re.findall('..', '%012x' % mac()))

    return f'White ip: {white_ip}\nGray ip: {gray_ip}\nMAC: {MAC}'


modes = {constants.NETWORK_GETIPMAC_preview: constants.NETWORK_GETIPMAC}

import sys
import os
from datetime import datetime
from ipaddress import IPv4Network
import socket
import struct
import functools
import requests

def logging(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = datetime.now().strftime("%H:%M:%S")
        print('[%s] SCHEDULER: Running job "%s"' % (start, func.__name__))
        result = func(*args, **kwargs)
        finished = datetime.now().strftime("%H:%M:%S")
        print('[%s] SCHEDULER: Job "%s" completed' % (finished, func.__name__))
        return result
    return wrapper

def bytes_to_string(bytes_object):
    default_encoding = sys.getdefaultencoding()
    decoded = bytes_object
    if isinstance(bytes_object, bytes):
        decoded = bytes_object.decode(default_encoding)
    return decoded


def array_to_csv(array, file_path):

    csv = open(file_path, "w+")
    for row in array:
        csv.write(row)
        csv.write("\n")


def delete_if_exists(file_path):
    if os.path.exists(file_path):
        os.remove(file_path)

def get_subnet(ipv4, netmask):
    base = ''.join([ipv4, '/', netmask])
    return str(IPv4Network(base, False))

def get_default_gateway_linux(ifname):
    """Read the default gateway directly from /proc."""
    with open("/proc/net/route") as fh:
        for line in fh:
            fields = line.strip().split()
            if fields[0] != ifname or (fields[1] != '00000000' or not int(fields[3], 16) & 2):
                continue
            return socket.inet_ntoa(struct.pack("<L", int(fields[2], 16)))

def get_interfaces_names_linux():
    interfaces_names = []
    with open("/proc/net/route") as fh:
        for line in fh:
            fields = line.strip().split()
            if fields[0] not in interfaces_names and fields[0] != "Iface":
                interfaces_names.append(fields[0])
        return interfaces_names


def bool_internet_connection():
    url = "http://www.kite.com"

    timeout = 5

    try:

        request = requests.get(url, timeout=timeout)

        return True

    except (requests.ConnectionError, requests.Timeout) as exception:

        return False
import requests


def post(url, data, files=None):
    req = requests.post(url, data=data, files=files)

    return req.text


def get(url):
    req = requests.get(url)

    return req.text
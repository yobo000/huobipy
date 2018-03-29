#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import hmac
from hashlib import sha256
import base64
from datetime import datetime

try:
    from urllib.parse import urlparse, urlencode, parse_qsl
except ImportError:
    from urlparse import urlparse, parse_qsl
    from urllib import urlencode
import requests

from settings import *


class _Api_request(object):
    """
    API Request
    """
    def __init__(self, client, method, path):
        self._client = client
        self._method = method
        self._path = path

    def __call__(self, **kw):
        url = ''
        if "market" in self._path:
            URL_PREFIX = MARKET_URL
        else:
            URL_PREFIX = TRADE_URL
        if self._method == "GET":
            url = URL_PREFIX + self._path
            new_url = self._client.generate_url("GET", url, kw)
            try:
                response = requests.get(new_url, headers=GET_HEADERS, timeout=5)
                if response.status_code == 200:
                    return response.json()
                elif response.status_code == 404:
                    return "Wrong route, Please check the document<https://github.com/huobiapi/API_Docs/wiki/REST_api_reference>"
                else:
                    content = response.json()
                    return ':'.join(content.get("err-code"), content.get("err-msg"))
            except requests.Timeout:
                print("Timeout")
                return
            except BaseException as e:
                print("Failed, Details:%s,%s" % (response.text, e))
                return
        if self._method == "POST":
            url = URL_PREFIX + self._path
            new_url = self._client.generate_url("POST", url, kw)
            try:
                response = requests.post(new_url, headers=POST_HEADERS, timeout=5)
                if response.status_code == 200:
                    data = response.json()
                    return data
                elif response.status_code == 404:
                    return "Wrong route, Please check the document<https://github.com/huobiapi/API_Docs/wiki/REST_api_reference>"
                else:
                    content = response.json()
                    return ':'.join(content.get("err-code"), content.get("err-msg"))
            except requests.Timeout:
                print("Timeout")
                return
            except BaseException as e:
                print("Failed, Details:%s,%s" % (response.text, e))
                return
        return url

    def __str__(self):
        return 'Request (%s %s)' % (self._method, self._path)

    __repr__ = __str__


class Rest(object):
    """Assemble URL from attributes and call the API request

    >>> Rest('', '').test.foo.bar("foo123")
    /test/foo/bar/foo123
    """
    def __init__(self, client, path=''):
        self._client = client
        self._path = path

    def __call__(self, arg):
        if isinstance(arg, str):
            self._path = '%s/%s' % (self._path, arg)
            return Rest(self._client, self._path)
        if isinstance(arg, int):
            self._path = '%s/%s' % (self._path, arg)
            return Rest(self._client, self._path)

    def __getattr__(self, name):
        if name == "get":
            return _Api_request(self._client, 'GET', self._path)
        if name == 'post':
            return _Api_request(self._client, 'POST', self._path)
        _path = '%s/%s' % (self._path, name)
        return Rest(self._client, _path)

    def __str__(self):
        return self._path

    __repr__ = __str__


class ApiClient(object):
    """Return Api Client
    Usage:
    > client = ApiClient(access_key=ACCESS_KEY, secret_key=SECRET_KEY)
    # GET /market/history/kline?symbol=btcusdt&period=1min&size=5
    > client.market.history.kline.get(symbol=btcusdt,period=1min,size=5)
    # GET /v1/account/accounts/{account-id}/balance
    > client.account.accounts(1234).balance.get()
    # POST /v1/order/orders/place
    > client.order.orders.place.post({data:})

    >>> client = ApiClient(access_key="Aexxxxxx", secret_key="86xxxxxx")
    >>> client.generate_url("GET", 'https://api.example.com/test/foo/bar', {'Timestamp': '2018-03-28T05:30:00'})
    'https://api.example.com/test/foo/bar?AccessKeyId=Aexxxxxx&SignatureMethod=HmacSHA256&SignatureVersion=2&Timestamp=2018-03-28T05%3A30%3A00&Signature=q1QAQ9Rr78kU1JF6h80K4hFkfy5z0jS1OnOFbWl%2FDFw%3D'
    """
    def __init__(self, access_key='', secret_key=''):
        self._acc_key = access_key
        self._sec_key = secret_key

    def generate_url(self, method, url, params):
        url_obj = urlparse(url)
        _scheme = url_obj.scheme
        _hostname = url_obj.netloc
        _path = url_obj.path
        msg = {
            "AccessKeyId": self._acc_key,
            "SignatureMethod": 'HmacSHA256',
            "SignatureVersion": '2',
            "Timestamp": datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S'),
        }
        msg.update(params)
        sorted_msg = sorted(msg.items(), key=lambda x: x[0], reverse=False)
        encode_msg = urlencode(sorted_msg)
        payload = [method.upper(), _hostname, _path, encode_msg]
        payload_string = '\n'.join(payload)
        digest = hmac.new(self._sec_key.encode(encoding='UTF-8'),
                          payload_string.encode(encoding='UTF-8'),
                          digestmod=sha256).digest()
        signature = base64.b64encode(digest)
        encode_msg = encode_msg + "&" + urlencode({"Signature": signature.decode()})
        new_url = "{0}://{1}{2}?{3}".format(_scheme, _hostname, _path, encode_msg)
        return new_url

    def __getattr__(self, attr):
        return Rest(self, attr)


if __name__ == "__main__":
    import doctest
    doctest.testmod()

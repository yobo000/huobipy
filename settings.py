# -*- coding: utf-8 -*-

ACCESS_KEY = "e2xxxxxx-99xxxxxx-84xxxxxx-7xxxx"
SECRET_KEY = "b0xxxxxx-c6xxxxxx-94xxxxxx-dxxxx"

CN = True

if CN:
    DOMAIN = "https://api.huobi.pro/"
else:
    DOMAIN = "https://api.hadax.com/"

VERSION = "v1/"
MARKET_URL = DOMAIN
TRADE_URL = DOMAIN + VERSION

EXTEND = {"Accept-Language": "zh-cn"}

POST_HEADERS = {
    "Accept": "application/json",
    "Content-Type": "application/json"
}

GET_HEADERS = {
    "Content-type": "application/x-www-form-urlencoded",
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) \
                  AppleWebKit/537.36 (KHTML, like Gecko) \
                  Chrome/39.0.2171.71 Safari/537.36",
}

if CN:
    GET_HEADERS.update(EXTEND)
    POST_HEADERS.update(EXTEND)

# huobipy

Huobi & HADAX Python SDK for Rest api

[![PyPI pyversions](https://img.shields.io/pypi/pyversions/ansicolortags.svg)](https://github.com/yobo000/huobipy)


Usage:

```python
>>> from huobipy import ApiClient
>>> client = ApiClient(access_key=ACCESS_KEY, secret_key=SECRET_KEY)
>>> data = client.market.history.kline.get(symbol="btcusdt", period="1min", size=5)
```

Example:

```python
# GET /market/history/kline?symbol=btcusdt&period=1min&size=5
>>> client.market.history.kline.get(symbol="btcusdt",period="1min",size=5)
# GET /v1/account/accounts/{account-id}/balance
>>> client.account.accounts(1234).balance.get()
# POST /v1/order/orders/place
>>> client.order.orders.place.post(data)
```
Please follow the [Huobi Api reference](https://github.com/huobiapi/API_Docs/wiki/REST_api_reference)

Inspired by [ericls/huobi](https://github.com/ericls/huobi)
Just for fun.

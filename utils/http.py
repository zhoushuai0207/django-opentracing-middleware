# -*- coding: utf-8 -*-
import requests


def requests_noauth(method, *args, **kwargs):
    if not kwargs:
        kwargs = {}
    headers = {'content-type': 'application/json', 'Accept': 'application/json'}
    if "headers" in kwargs:
        headers.update(kwargs["headers"])
        del kwargs["headers"]
    if method == "POST":
        r_data = requests.post(*args, headers=headers, **kwargs)
    elif method == "GET":
        r_data = requests.get(*args, headers=headers, **kwargs)
    elif method == "PUT":
        r_data = requests.put(*args, headers=headers, **kwargs)
    elif method == "DELETE":
        r_data = requests.delete(*args, headers=headers, **kwargs)
    elif method == "PATCH":
        r_data = requests.patch(*args, headers=headers, **kwargs)
    else:
        raise Exception("invalid http method")
    if r_data.status_code // 100 != 2:
        raise Exception(r_data.text)
    j = r_data.json()
    return j

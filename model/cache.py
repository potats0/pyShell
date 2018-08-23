#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# Authors: img
# Date: 2018-07-11
from collections import namedtuple

__author__ = "img"
__date__ = '2018/7/11'

import json
from inspect import getfullargspec

from tinydb import TinyDB, where
from tinydb.middlewares import CachingMiddleware
from tinydb.storages import JSONStorage

from model.shells import Caidao


class cache:

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, "instance"):
            cls.instance = super(cache, cls).__new__(cls)
        return cls.instance

    def __init__(self):
        self.c = TinyDB('cache.json', storage=CachingMiddleware(JSONStorage))
        obj = getattr(self.c, "_storage")  # 把这个值设置的比较小，可以让数据随时同步到disk，虽然这个方法有点扯
        obj.WRITE_CACHE_SIZE = 1
        self.item = namedtuple('item', ("is_dir", 'name', "st_mtime", "size", 'permission'))

    def __call__(self, func):
        def inner_func(*args, **kargs):
            signature = {**dict(zip(getfullargspec(func).args, args)), **kargs}
            obj = signature.get('self', None)
            if obj and isinstance(obj, Caidao.Caidao):
                signature.update(self=json.dumps((obj.url, obj.password)))
            if self.c.contains(where(str(signature)).exists()) and not signature.get('flush', False):
                if isinstance(obj, Caidao.Caidao):
                    result = []
                    for i in json.loads(self.c.get(where(str(signature)).exists()).get(str(signature))):
                        result.append(self.item._make(i))
                else:
                    result = self.c.get(where(str(signature)).exists()).get(str(signature))
            else:
                result = func(*args, **kargs)
                if isinstance(obj, Caidao.Caidao):
                    self.c.insert({str(signature): json.dumps(result)})
                else:
                    self.c.insert({str(signature): result})
            return result

        return inner_func

    def __del__(self):
        self.c.close()

#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# Authors: img
# Date: 2018-05-29

__author__ = "img"
__date__ = '2018/5/29'

import base64
import contextlib
import logging
import random
import string
import zlib
from http.client import HTTPConnection  # py3

#from IPython.core import ultratb


def gnucompress(buf):
    return base64.b64encode(zlib.compress(buf))


def random_useragent():
    pass


def dictToQuery(dict):
    query = ''
    for key in dict.keys():
        query += str(key) + '=' + str(dict[key]) + "&"
    return query[:len(query) - 1]


def try_except(errors=Exception):
    def decorate(func):
        def wrappers(*args, **kwargs):
            # noinspection PyBroadException
            try:
                return func(*args, **kwargs)
            except errors:
                # ipshell = ultratb.FormattedTB(mode='Context', color_scheme='LightBG', call_pdb=1)
                # ipshell()
                print(errors)

        return wrappers

    return decorate


def debug_requests_on():
    '''Switches on logging of the requests module.'''
    HTTPConnection.debuglevel = 1

    logging.basicConfig()
    logging.getLogger().setLevel(logging.DEBUG)
    requests_log = logging.getLogger("requests.packages.urllib3")
    requests_log.setLevel(logging.DEBUG)
    requests_log.propagate = True


def debug_requests_off():
    '''Switches off logging of the requests module, might be some side-effects'''
    HTTPConnection.debuglevel = 0

    root_logger = logging.getLogger()
    root_logger.setLevel(logging.WARNING)
    root_logger.handlers = []
    requests_log = logging.getLogger("requests.packages.urllib3")
    requests_log.setLevel(logging.WARNING)
    requests_log.propagate = False


@contextlib.contextmanager
def debug_requests():
    '''Use with 'with'!'''
    debug_requests_on()
    yield
    debug_requests_off()


def generate_random():
    return ''.join(random.choices(string.ascii_uppercase, k=16))

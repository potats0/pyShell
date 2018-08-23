#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# Authors: img
# Date: 2018-05-29

__author__ = "img"
__date__ = '2018/5/29'

import base64
import codecs


def base64_encode(data: str) -> bytes:
    return base64.b64encode(data.encode())


def hex_encode(data: str) -> bytes:
    return codecs.encode(data.encode(), "hex")

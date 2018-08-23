#!/usr/local/bin/python
# -*- coding: UTF-8 -*-
import os
import re
import sys
import time
from urllib.parse import urlparse

import dns.resolver
import requests
from PyQt5.QtCore import QRunnable, QObject, pyqtSignal, QThreadPool
from PyQt5.QtWidgets import QMessageBox

from model.db import db
from model.shells.Caidao import cache


def isip(domain):
    p = re.compile('^((25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}(25[0-5]|2[0-4]\d|[01]?\d\d?)$')
    if p.match(domain):
        return True
    else:
        return False


@cache()
def get_location_from_domain(domain):
    """
    use httpdns to resolv domain
    :param domain: 域名
    :return: location
    """
    domain = urlparse(domain).netloc
    if ":" in domain:
        domain = domain.split(":")[0]
    if isip(domain):
        ip = domain
    else:
        if "localhost" in domain:
            ip = "127.0.0.1"
        else:
            try:
                A = dns.resolver.query(domain, 'A')
                ip = A.response.answer[0][0].address
            except Exception:
                return "Not found Address"
    location = qqwry_search()(ip)
    return location


def test_shell(url, passwd, type, row):
    forms = {
        passwd: "echo 12233333333;"
    }
    try:
        data = requests.post(url, data=forms, timeout=1)
        if "12233333333" in data.text:
            status = True
        else:
            status = False
    except Exception as e:
        print(sys.exc_info())
        status = False
    finally:
        return status, row


def try_catch(func):
    def b(*args, **kwargs):
        obj = args[0]
        try:
            func(*args, **kwargs)
        except Exception as e:
            obj.signal.result.emit(sys.exc_info()[0])

    return b


class WorkerSignals(QObject):
    result = pyqtSignal(object)


class worker(QRunnable):
    def __init__(self, func, **kargs):
        super(worker, self).__init__()
        self.func = func
        self.kargs = kargs
        self.signal = WorkerSignals()

    @try_catch
    def run(self):
        self.signal.result.emit(self.func(**self.kargs))


def start_runnable(func, slot, **kwargs):
    w = worker(func, **kwargs)
    w.signal.result.connect(slot)
    pool = QThreadPool.globalInstance()
    pool.start(w)


def iscomplete(func):
    def a(*args, **kwargs):
        if any(map(lambda x: isinstance(x, type), args)):
            QMessageBox.critical(args[0], 'pyshell', "操作未完成")
        else:
            func(*args, **kwargs)

    return a


def isloaded(func):
    def b(*args, **kwargs):
        if hasattr(args[0], "linker"):
            func(*args[:1], **kwargs)
        else:
            print("not loaded,mat be network is slow")

    return b


def load_from_file(filename: str, separator: str = '|') -> [int, int]:
    """从给定的文件中读取记录并插入数据库中
    filename：给定的文件名，绝对路径
    separator：每条记录的分隔符，由用户指定
    ignore：忽略单行错误，如果某一行出现错误，则跳过不处理。如果为false，则不继续导入，返回已经导入成功的数字和false
    返回值 返回元祖，第一项为成功导入的数字，第二项为是否全部导入成功（Ture or False）
    例如如果文件100行记录，导入100行全部成功，则返回100,True
    如果成功导入90行，则返回90，False

    例如
    http://www.qq.com/1.php|cmd
    则separator为|,前面的为url，后面的为shell的链接密码，如果url没有以http://开头，则给添加上(默认http)
    if not url.startWith("http://):
        do something

    插入数据库，调用model.db,首先实例化，然后调用insert函数
    例:
        db = db()
        db.insert(records)
    insert()每个参数的含义（从左到右依次）
    types：shell的类型，大写字符串 PHP/ASP/ASPX/CUSTOMER
    shell：shell的地址（记得添加http://)
    passwd：shell的密码
    config：shell的配置，目前留空（空字符串）
    remark：shell的备注
    type_id：目前为"0"
    coding：shell的编码，默认utf-8
    createdtime：shell创建日期 字符串类型 time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    updatetime：shell更新日期，目前暂时和createdtime一致即可
    """
    num, failed_num, shell_db, created_time = 0, 0, db(), time.strftime("%Y-%m-%d %H:%M:%S",
                                                                        time.localtime())
    with open(filename, "r") as f:
        for num, line in enumerate(f, 1):
            shell = line.strip().split(separator)
            if not len(shell) == 2:
                failed_num += 1
                continue
            if not shell[0].startswith("http"):
                shell[0] = "http://" + shell[0]
            shell_type = re.findall("(.php|.aspx|.asp)", shell[0], re.I)  # 识别并添加shell类型
            if len(shell_type):
                shell_type = shell_type[0].upper().replace('.', '')
            else:
                shell_type = "CUSTOMER"
            shell.insert(0, shell_type)
            shell.extend(['', '', 0, 'utf-8', created_time, created_time])
            shell_db.insert(*shell)
    return num, num ^ failed_num


def splitpath(path):
    def _get_bothseps(path):
        if isinstance(path, bytes):
            return b'\\/'
        else:
            return '\\/'

    path = os.fspath(path)
    seps = _get_bothseps(path)
    i = len(path)
    re = []
    while i:
        i -= 1
        if path[i - 1] in seps:
            re.append(path[i:])
            path = path[:i]
    re.reverse()
    return re


class qqwry_search(object):
    """docstring for qqwry_search"""

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, "instance"):
            cls.instance = super(qqwry_search, cls).__new__(cls)
        return cls.instance

    def __init__(self):
        from qqwry import QQwry
        self.q = QQwry()
        self.q.load_file('qqwry.dat')

    def __call__(self, ip: str):
        return ' '.join(self.q.lookup(ip))

    def __del__(self):
        self.q.clear()


def export_shell_file(filename: str, separator: str = '|') -> [int]:
    num, shell_list = 0, db().getall()
    with open(filename, "w+") as f:
        for shell in shell_list:
            f.write(shell['shell'] + separator + shell['passwd'] + "\n")
            num = num + 1
    return num


if __name__ == '__main__':
    # print(get_location_from_domain('http://www.xxx.com'))
    print(export_shell_file("C:\\Users\\12937\\Desktop\\a.txt", "|||||"))

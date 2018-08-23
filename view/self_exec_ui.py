#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# Authors: img
# Date: 2018-07-03
from PyQt5 import uic
from PyQt5.QtWidgets import QWidget

from model.db import db
from model.shells import Caidao
from util import start_runnable

__author__ = "img"
__date__ = '2018/7/3'


class self_exec_ui(QWidget):
    def __init__(self, id, parent):
        super(self_exec_ui, self).__init__(parent)
        self.main = parent  # 主程序UI
        self.ui = uic.loadUi("view/ui/ShowEdit_shellManage.ui", self)
        self.main.tabWidget.addTab(self, "self_exec")
        self.main.tabWidget.setCurrentWidget(self)
        self.db = db()
        record = self.db.get(id)
        self.siteurl = record.shell
        self.sitepass = record.passwd
        self.ui.send_pushButton.clicked.connect(self.exc_code)
        self.init_linker()

    def init_linker(self):
        def start():
            return Caidao.Caidao(self.siteurl, self.sitepass)

        def getresult(obj):
            self.linker = obj

        start_runnable(start, getresult)

    def exc_code(self):
        content = self.ui.textEdit.toPlainText()
        start_runnable(self.linker.raw, lambda x: self.ui.messages.setPlainText(x), data=content)

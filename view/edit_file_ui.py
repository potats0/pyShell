#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# Authors: img
# Date: 2018-07-03
from PyQt5 import uic
from PyQt5.QtWidgets import QWidget, QMessageBox

from util import start_runnable

__author__ = "img"
__date__ = '2018/7/3'


class edit_file(QWidget):
    def __init__(self, linker, remote_file, parent):
        super(edit_file, self).__init__(parent)
        self.main_ui = parent  # 主程序UI
        self.ui = uic.loadUi("view/ui/Edit_file.ui", self)
        self.main_ui.tabWidget.addTab(self, "Edit file")
        self.main_ui.tabWidget.setCurrentWidget(self)
        self.linker, self.remote_file = linker, remote_file

        # set slot
        self.ui.load_Button.clicked.connect(self.load_file)
        self.ui.save_Button.clicked.connect(self.save_file)

        self.dis_file_to_panel()

    def dis_file_to_panel(self):
        self.ui.name_lineEdit.setText(self.remote_file)
        start_runnable(self.linker.read_file, self.display, item=self.remote_file)

    def display(self, data):
        if isinstance(data, type):
            QMessageBox.critical(self, 'pyshell', "unable to read..")
            return
        self.main_ui.statusBar.showMessage("loaded file success", 2000)
        self.ui.data_textEdit.setPlainText(data)

    def load_file(self):
        self.remote_file = self.ui.name_lineEdit.text().strip()
        self.dis_file_to_panel()

    def save_file(self):
        content = self.ui.data_textEdit.toPlainText()
        filename = self.ui.name_lineEdit.text().strip()
        start_runnable(self.linker.save_file, lambda x: x, filename=filename, content=content)
        self.main_ui.statusBar.showMessage("saved file success", 2000)

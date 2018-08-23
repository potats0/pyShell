#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# Authors: img
# Date: 2018-07-09

from PyQt5 import uic
from PyQt5.QtWidgets import QDialog, QFileDialog, QMessageBox

from util import load_from_file, start_runnable

__author__ = "img"
__date__ = '2018/7/9'


class import_shell_ui(QDialog):
    def __init__(self, parent):
        super(import_shell_ui, self).__init__(parent)
        self.ui = uic.loadUi("view/ui/import_shell.ui", self)
        self.main = parent
        self.ui.button.clicked.connect(self.open_file_dialog)
        self.ui.pushButton.clicked.connect(self.import_shell)

    def open_file_dialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "",
                                                  "All Files (*);;Python Files (*.py)", options=options)
        if fileName:
            self.filename = fileName
            self.ui.lineEdit.setText(fileName)

    def import_shell(self):
        def result(num):
            QMessageBox.critical(self, 'pyshell', "添加完成，成功%s，失败%s" % (num[0], num[0] ^ num[1]))
            start_runnable(self.main.refresh_table_item, lambda x: x)

        separator = self.ui.lineEdit_2.text()
        start_runnable(load_from_file, result, filename=self.filename, separator=separator)

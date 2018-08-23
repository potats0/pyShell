#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# Authors: img
# Date: 2018-07-17


__author__ = "img"
__date__ = '2018/7/17'

from PyQt5 import uic
from PyQt5.QtWidgets import QDialog, QFileDialog, QMessageBox
from util import start_runnable, export_shell_file


class export_shell_ui(QDialog):
    def __init__(self, parent):
        super(export_shell_ui, self).__init__(parent)
        self.ui = uic.loadUi("view/ui/export_shell.ui", self)
        self.main = parent
        self.ui.pushButton.clicked.connect(self.open_filedialog)
        self.ui.pushButton_2.clicked.connect(self.export_shell)

    def open_filedialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getSaveFileName(self, "QFileDialog.getOpenFileName()", "",
                                                  "All Files (*);;Python Files (*.py)", options=options)
        if fileName:
            self.filename = fileName
            self.ui.lineEdit.setText(fileName)

    def export_shell(self):
        def result(num):
            QMessageBox.critical(self, 'pyshell', "导出%s条" % (num))

        separator = self.ui.lineEdit_2.text()
        start_runnable(export_shell_file, result, filename=self.filename, separator=separator)

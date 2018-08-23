#!/usr/local/bin/python
# -*- coding: UTF-8 -*-

from PyQt5 import uic
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QDialog, QLineEdit


# TODO 目前只实现添加，暂未实现修改功能
class add_shell_ui_ctrl(QDialog):
    insert = pyqtSignal(str, str, str, str, str, str, str)  # 添加
    update = pyqtSignal(str, str, str, str, str, str, str, str)  # 修改

    # siteurl #URL
    # sitepass  #密码
    # config   #配置
    # remarks  备注
    # type_id #类别
    # script  #脚本类型  asp   php
    # coding   #编码方式

    def __init__(self):
        super(add_shell_ui_ctrl, self).__init__()
        self.ui = uic.loadUi("view/ui/add_shell_ui.ui", self)
        self.setWindowIcon(QIcon("system/main.ico"))
        self.setFixedSize(self.width(), self.height())
        self.set_data()

    def set_data(self):
        self.setWindowTitle("添加数据")
        self.ui.script.addItem(QIcon('system/script.ico'), "脚本类型")
        self.ui.script.addItem(QIcon('system/php.ico'), "PHP")
        self.ui.script.addItem(QIcon('system/asp.ico'), "ASP")
        self.ui.script.addItem(QIcon('system/aspx.ico'), "ASPX")
        self.ui.script.addItem("Customize")
        self.ui.coding.addItem(QIcon('system/coding.ico'), "字符编码")
        self.ui.coding.addItem("UTF-8")
        self.ui.coding.addItem("GB2312")
        self.ui.coding.addItem("BIG5")
        self.ui.coding.addItem("Euc-KR")
        self.ui.coding.addItem("Euc-JP")
        self.ui.coding.addItem("Shift_JIS")
        self.ui.coding.addItem("Windows-1251")
        self.ui.coding.addItem("Windows-874")
        self.ui.coding.addItem("ISO-8859-1")
        self.ui.coding.setCurrentIndex(1)
        self.ui.sitepass.setEchoMode(QLineEdit.Normal)
        self.ui.pass_checkBox.setChecked(True)
        self.ui.pushButton.clicked.connect(self.add_button)
        self.ui.siteurl.textChanged.connect(self.get_ext_from_url)
        self.ui.pass_checkBox.clicked.connect(self.pass_click)

    def get_ext_from_url(self):
        site_url = self.ui.siteurl.toPlainText()  # URL
        site_url = site_url.upper()
        if ".PHP" in site_url:
            self.ui.script.setCurrentIndex(1)  # php
        elif ".ASP" in site_url:
            self.ui.script.setCurrentIndex(2)  # .ASP
        elif "ASPX" in site_url:
            self.ui.script.setCurrentIndex(3)  # ASPX
        else:
            self.ui.script.setCurrentIndex(0)

    def add_button(self):
        site_url = self.ui.siteurl.toPlainText().strip()  # URL
        if not site_url.startswith("http://"):
            site_url = "http://" + site_url
        site_pass = self.ui.sitepass.text().strip()  # 密码
        config = self.ui.config.toPlainText().strip()  # 配置
        remarks = self.ui.remarks.toPlainText().strip()
        type_id = str(self.ui.type_id.currentIndex())
        script_type = self.ui.script.currentText().strip()
        coding_type = self.coding.currentText().strip()
        self.insert.emit(site_url, site_pass, config, remarks, type_id, script_type, coding_type)
        self.close()

    def pass_click(self):
        if self.pass_checkBox.isChecked():  # 选中
            self.ui.sitepass.setEchoMode(QLineEdit.Normal)
        else:
            self.ui.sitepass.setEchoMode(QLineEdit.Password)

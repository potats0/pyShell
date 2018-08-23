#!/usr/bin/env python
# -*- coding: UTF-8 -*-


# Authors: img
# Date: 2018-06-21

__author__ = "img"
__date__ = '2018/6/21'

from PyQt5 import uic
from PyQt5.QtCore import QEvent
from PyQt5.QtWidgets import QWidget, QApplication

from model.db import db
from model.shells import Caidao
from util import start_runnable, iscomplete, isloaded


class cmd_ui(QWidget):
    """
     # TODO 添加cd功能，测试在windows下的行为
    """

    def __init__(self, id: int, parent):
        super(cmd_ui, self).__init__(parent)
        self.main_ui = parent
        self.ui = uic.loadUi("view/ui/ShowcmdManage.ui", self)  # 动态加标签
        self.ui.parameter_0.setMouseTracking(False)
        self.ui.parameter_0.setAcceptDrops(False)
        self.ui.parameter_0.setEditable(True)
        self.ui.parameter_0.setMaxVisibleItems(15)  # 设置下拉最大选项数为15
        self.ui.parameter_0.installEventFilter(self)  # 在窗体上为self.edit安装过滤器
        self.ui.pushButton.clicked.connect(self.execute_cmd)  # shell命令
        self.ui.cmd_shell_TextEdit.setStyleSheet("color:rgb(245,245,245)")  # 文本颜色
        self.ui.cmd_shell_TextEdit.setStyleSheet("background-color:rgb(192,192,192)")  # 背景色
        self.ui.cmd_shell_TextEdit.setReadOnly(True)
        self.main_ui.tabWidget.addTab(self, "cmd")
        self.main_ui.tabWidget.setCurrentWidget(self)
        self.db = db()
        record = self.db.get(id)
        self.siteurl = record.shell
        self.sitepass = record.passwd
        self.get_metadata_from_server()

    def get_metadata_from_server(self):
        def start():
            return Caidao.Caidao(self.siteurl, self.sitepass)

        def getresult(obj):
            self.linker = obj
            self.ui.parameter_1.setText("/bin/sh")
            self.ui.parameter_2.setText("netstat -an | grep ESTABLISHED")  # 设置当前内容
            self.ui.parameter_0.addItem("netstat -an | grep ESTABLISHED")  # 添加到下拉列表
            self.execute_cmd()

        start_runnable(start, getresult)

    def eventFilter(self, source, event):  # 事件监听
        if event.type() == QEvent.KeyPress and event.key() == 16777220:  # 检测键盘事件
            QApplication.processEvents()
            self.execute_cmd()  # 执行事件
        return QWidget.eventFilter(self, source, event)  # 将事件交给上层对话框

    @iscomplete
    def display_info_to_panel(self, data, command=False):
        if not command:
            self.ui.cmd_shell_TextEdit.appendPlainText(data)
            self.main_ui.statusBar.showMessage("successed to execute command", 5000)
            data = ""
        self.ui.cmd_shell_TextEdit.appendPlainText(self.ui.linker.current_folder + "> " + data)

    @isloaded
    def execute_cmd(self):  # shell命令
        command = self.ui.parameter_0.currentText().strip()
        self.display_info_to_panel(command, command=True)
        if not command:
            return
        self.ui.parameter_2.setText(command)
        self.ui.parameter_0.addItem(command)
        self.ui.parameter_0.setCurrentText("")
        start_runnable(self.ui.linker.exec_command, self.display_info_to_panel, cmd=command)

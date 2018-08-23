#!/usr/local/bin/python
# -*- coding: UTF-8 -*-

import time

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMenu, QAction, QTableWidgetItem, QMessageBox

from model.db import db
from util import get_location_from_domain, test_shell, start_runnable
from view.add_shell_view import add_shell_ui_ctrl
from view.cmd_ui import cmd_ui
from view.export_shell_ui import export_shell_ui
from view.file_ui import file_ui
from view.import_shell_ui import import_shell_ui
from view.self_exec_ui import self_exec_ui


class controller_main(object):
    def __init__(self):
        self.db = db()

    def register_main(self, main):
        self.cls = main

    def tableWidget_menu(self, p):
        self.cls.setContextMenuPolicy(Qt.CustomContextMenu)
        self.cls.popMenu = QMenu(self.cls)
        int_model = self.cls.tableWidget.selectionModel()  # 获取选中编号
        sum = len(int_model.selectedRows())  # 获取数量
        if sum == 0:  # 如果没有选中  只有添加
            action = QAction('添加数据', self.cls)
            action.triggered.connect(self.add_shell_show)
            self.cls.popMenu.addAction(action)
            self.cls.popMenu.addSeparator()  # 添加分隔
            self.cls.name = self.cls.popMenu.addMenu(u'批量导入/导出')
            action = QAction('批量导入数据', self.cls)
            action.triggered.connect(self.import_shell)
            self.cls.name.addAction(action)
            action = QAction('批量导出数据', self.cls)
            action.triggered.connect(lambda: self.cls.Import_export_ui_show(2))
            self.cls.name.addAction(action)
            action = QAction('选择导出数据', self.cls)
            action.triggered.connect(lambda: self.cls.while_export_shell())
            self.cls.name.addAction(action)
        elif sum == 1:  # 如果选中1条  添加  删除  修改
            action = QAction('文件管理', self.cls)
            action.triggered.connect(self.open_file_shell)
            self.cls.popMenu.addAction(action)
            # action = QAction(u'数据库管理',self)
            # self.popMenu.addAction(action)
            action = QAction('虚拟终端', self.cls)
            action.triggered.connect(self.open_cmd_shell)
            self.cls.popMenu.addAction(action)
            action = QAction('自写脚本', self.cls)
            action.triggered.connect(self.open_self_exec_ui)
            self.cls.popMenu.addAction(action)

            self.cls.popMenu.addSeparator()  # 添加分隔
            action = QAction('添加数据', self.cls)
            action.triggered.connect(self.add_shell_show)
            self.cls.popMenu.addAction(action)
            action = QAction('修改数据', self.cls)
            action.triggered.connect(lambda: self.cls.add_shell_show(2))
            self.cls.popMenu.addAction(action)
            action = QAction('删除数据', self.cls)
            action.triggered.connect(self.delete_item_from_main_table)
            self.cls.popMenu.addAction(action)
            self.cls.popMenu.addSeparator()
            action = QAction('批量测试状态', self.cls)
            action.triggered.connect(self.batch_text)
            self.cls.popMenu.addAction(action)
            self.cls.name = self.cls.popMenu.addMenu(u'批量导入/导出')
            action = QAction('批量导入数据', self.cls)
            action.triggered.connect(self.import_shell)
            self.cls.name.addAction(action)
            action = QAction('批量导出数据', self.cls)
            action.triggered.connect(self.export_shell)
            self.cls.name.addAction(action)
            # action = QAction('选择导出数据', self.cls)
            # action.triggered.connect(lambda: self.cls.while_export_shell())
            # self.cls.name.addAction(action)
        elif sum > 1:
            action = QAction('批量测试状态', self.cls)
            action.triggered.connect(self.batch_text)
            self.cls.popMenu.addAction(action)
        self.cls.popMenu.exec_(self.cls.tableWidget.mapToGlobal(p))

    def add_shell_show(self):
        panel = add_shell_ui_ctrl()
        panel.insert.connect(self.insert)
        panel.show()

    def insert(self, site_url, site_pass, config, remarks, type_id, script_type, coding_type):
        # TODO 动态添加行的方法，需要重构，这只是一个测试
        row = self.cls.tableWidget.rowCount()
        self.cls.tableWidget.insertRow(row)
        id = self.db.insert(script_type, site_url, site_pass, config, remarks, "0", coding_type,
                            time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
                            time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        self.cls.tableWidget.setItem(row, 0, QTableWidgetItem(str(id)))
        self.cls.tableWidget.setItem(row, 1, QTableWidgetItem(script_type))
        self.cls.tableWidget.setItem(row, 2, QTableWidgetItem(site_url))
        self.cls.tableWidget.setItem(row, 3, QTableWidgetItem(get_location_from_domain(site_url)))
        self.cls.tableWidget.setItem(row, 4, QTableWidgetItem(remarks))
        self.cls.tableWidget.setItem(row, 5, QTableWidgetItem(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))
        self.cls.tableWidget.setItem(row, 6, QTableWidgetItem(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))

    def delete_item_from_main_table(self):
        row = self.cls.ui.tableWidget.selectionModel().currentIndex().row()
        id = self.cls.ui.tableWidget.item(row, 0)
        self.db.delete(int(id.text()))
        self.cls.ui.tableWidget.removeRow(row)

    def closeTab(self, tabId):  # 关闭属性页
        if tabId >= 1:
            self.cls.tabWidget.removeTab(int(tabId))

    def open_cmd_shell(self):
        row = self.cls.ui.tableWidget.selectionModel().currentIndex().row()
        id = self.cls.ui.tableWidget.item(row, 0)
        cmd_ui(int(id.text()), self.cls).show()

    def open_file_shell(self):
        row = self.cls.ui.tableWidget.selectionModel().currentIndex().row()
        id = self.cls.ui.tableWidget.item(row, 0)
        file_ui(int(id.text()), self.cls).show()

    def open_self_exec_ui(self):
        row = self.cls.ui.tableWidget.selectionModel().currentIndex().row()
        id = self.cls.ui.tableWidget.item(row, 0)
        self_exec_ui(int(id.text()), self.cls).show()

    def batch_text(self):
        self.successed = 0
        self.failed = 0
        self.failed_list = []

        def result(res):
            if res[0]:
                self.successed += 1
            else:
                self.failed += 1
                self.failed_list.append(res[1])

            self.cls.statusBar.showMessage("批量测试中 %s/%s" % (self.successed + self.failed, len(rows.selectedRows())),
                                           3000)
            if self.successed + self.failed >= len(rows.selectedRows()):
                QMessageBox.critical(self.cls, 'pyshell',
                                     "批量测试完成，成功%s，失败%s，正在删除失效shell" % (self.successed, self.failed))
                if self.failed_list:
                    for i in self.failed_list:
                        id = self.cls.ui.tableWidget.item(i, 0).text()
                        self.db.delete(int(id))
                        self.cls.ui.tableWidget.removeRow(i)
                    else:
                        QMessageBox.information(self.cls, 'pyshell', "删除失效shell成功")

        rows = self.cls.ui.tableWidget.selectionModel()
        for row in rows.selectedRows():
            id = self.cls.ui.tableWidget.item(row.row(), 0).text()
            url = db().get(int(id)).shell
            passwd = db().get(int(id)).passwd
            start_runnable(test_shell, result, url=url, passwd=passwd, type="php", row=row.row())

    def tableWidget_right(self, x, y):
        self.open_file_shell()

    def import_shell(self):
        import_shell_ui(self.cls).show()

    def export_shell(self):
        export_shell_ui(self.cls).show()

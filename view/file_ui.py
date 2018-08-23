#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# Authors: img
# Date: 2018-06-25

import util

__author__ = "img"
__date__ = '2018/6/25'

import os

from PyQt5 import uic
from PyQt5.QtCore import Qt, QEvent
from PyQt5.QtWidgets import QWidget, QTableWidget, QAction, QTableWidgetItem, QMenu, QFileDialog, QTreeWidgetItem, \
    QInputDialog, QLineEdit
from collections import OrderedDict

from model.db import db
from model.shells import Caidao
from util import start_runnable, iscomplete, isloaded
from view.edit_file_ui import edit_file


class file_ui(QWidget):
    def __init__(self, id, parent):
        super(file_ui, self).__init__(parent)
        self.main = parent
        self.ui = uic.loadUi("view/ui/ShowFileManage.ui", self)  # 动态加标签
        self.ui.ComPath.setMouseTracking(False)
        self.ui.ComPath.setAcceptDrops(False)
        self.ui.ComPath.setEditable(True)
        self.ui.ComPath.setMaxVisibleItems(15)  # 设置下拉最大选项数为15
        self.ui.ComPath.installEventFilter(self)  # 在窗体上为self.edit安装过滤器
        self.ui.file_treeWidget.setColumnCount(1)
        self.ui.file_treeWidget.setHeaderLabels(["文件管理"])
        self.ui.file_treeWidget.setColumnWidth(0, 700)  # 设置列宽
        self.ui.file_tableWidget.setColumnCount(5)  # 列
        self.ui.file_tableWidget.setRowCount(0)  # 行  len(node)
        self.ui.file_tableWidget.setHorizontalHeaderLabels(['is_dir', '名称', '时间', '大小', '属性'])
        self.ui.file_tableWidget.setColumnWidth(0, 0)  # 设置表格的各列的宽度值
        self.ui.file_tableWidget.setColumnWidth(1, 320)  # 设置表格的各列的宽度值
        self.ui.file_tableWidget.setColumnWidth(2, 170)  # 设置表格的各列的宽度值
        self.ui.file_tableWidget.setColumnWidth(3, 100)  # 设置表格的各列的宽度值
        self.ui.file_tableWidget.setColumnWidth(4, 160)  # 设置表格的各列的宽度值
        self.ui.file_tableWidget.setEditTriggers(QTableWidget.NoEditTriggers)  # 设置表格的单元为只读属性，即不能编辑
        self.ui.file_tableWidget.setSelectionBehavior(QTableWidget.SelectRows)  # 点击选择是选择行//设置选中时为整行选中
        self.ui.file_tableWidget.setSelectionMode(QTableWidget.SingleSelection)  # 禁止多行选择
        self.ui.file_tableWidget.setAlternatingRowColors(True)  # 还是只可以选择单行（单列）
        self.ui.file_tableWidget.verticalHeader().hide()  # 隐藏行头
        self.ui.file_tableWidget.setAlternatingRowColors(True)  # 隔行换色
        self.setAcceptDrops(True)
        self.main.tabWidget.addTab(self, "File_Manager")
        self.main.tabWidget.setCurrentWidget(self)
        self.db = db()
        record = self.db.get(id)
        self.siteurl = record.shell
        self.sitepass = record.passwd
        self.get_baseinfo_from_server()
        self.ui.file_tableWidget.setContextMenuPolicy(Qt.CustomContextMenu)
        self.ui.setContextMenuPolicy(Qt.CustomContextMenu)
        self.ui.file_tableWidget.customContextMenuRequested.connect(self.file_tableWidget_menu)
        self.ui.file_tableWidget.cellDoubleClicked.connect(self.tabledoubleclicked)
        self.ui.file_treeWidget.itemClicked.connect(self.treeclicked)
        self.my = {}
        # self.file_tableWidget.dragEnterEvent.connect(self.dragEnterEventxxx) #拖拽接收文件
        self.ui.look_Button.clicked.connect(
            lambda: self.get_item_form_folder(self.ui.ComPath.currentText().strip()))

    def get_baseinfo_from_server(self):  # 类初始化线程
        @iscomplete
        def setresult(window, obj):
            self.linker = obj
            self.current_folder = self.linker.current_folder
            self.get_item_form_folder(self.current_folder)

        def loadcaidao():
            return Caidao.Caidao(self.siteurl, self.sitepass)

        start_runnable(loadcaidao, lambda x: setresult(self, x))

    # TODO 写这个树型文件
    def build_tree(self, data, folder):
        self.ui.file_treeWidget.clear()

        def insert(l: dict, p: list):
            if p[1:] == p[:-1]:
                return
            for i in p:
                if i not in l:
                    l.update({i: {}})
                x = OrderedDict(sorted(l.get(i).items()))
                l[i] = x
                l = x

        def inner_build(l, parent=None):
            if not l:
                return
            for i in l.keys():
                if not parent:
                    self.root = QTreeWidgetItem(self.ui.file_treeWidget)
                    p = self.root
                else:
                    child1 = QTreeWidgetItem(parent)
                    p = child1
                p.setText(0, i)
                if l.get(i):
                    inner_build(l.get(i), p)
            self.ui.file_treeWidget.addTopLevelItem(self.root)
            self.ui.file_treeWidget.setColumnWidth(0, 160)
            self.ui.file_treeWidget.expandAll()

        path_list = util.splitpath(folder + self.linker.separator)
        insert(self.my, path_list)
        for i in data:
            if i.is_dir is "T":
                if not "." in i.name or not "." in i.name:
                    folder = i.name.replace("//", "/")
                    insert(self.my, util.splitpath(folder + self.linker.separator))
        inner_build(self.my, None)

    def normalize_name(self, string: str, is_dir):
        _, file_name = os.path.split(string)
        if is_dir is "T":
            file_name += self.linker.separator
        return file_name

    def normalize_perm(self, string):
        num_to_str = {
            "7": "|rwx",
            "6": "|rw-",
            "5": "|r-x",
            "4": "|r--",
            "3": "|-wx",
            "2": "|-w-",
            "1": "|--x",
            "0": "|---",
        }
        result = "s" if int(string[0]) else "-"
        return result + "".join(list((num_to_str.get(x) for x in string if int(x))))

    @iscomplete
    def add_item_to_filetable(self, data, folder):
        folder = folder.replace(".." + self.linker.separator, "").replace("." + self.linker.separator, "").replace(
            self.linker.separator * 2, self.linker.separator)
        self.current_folder = folder
        self.build_tree(data, folder)
        self.ui.ComPath.setCurrentText(folder)
        self.ui.ComPath.addItem(folder)
        self.ui.file_tableWidget.setRowCount(0)
        self.ui.file_tableWidget.clearContents()
        for i in data:
            row = self.ui.file_tableWidget.rowCount()
            self.file_tableWidget.insertRow(row)
            self.file_tableWidget.setItem(row, 0, QTableWidgetItem(i.is_dir))
            self.file_tableWidget.setItem(row, 1, QTableWidgetItem(self.normalize_name(i.name, i.is_dir)))
            self.file_tableWidget.setItem(row, 2, QTableWidgetItem(i.st_mtime))
            self.file_tableWidget.setItem(row, 3, QTableWidgetItem(i.size))
            self.file_tableWidget.setItem(row, 4, QTableWidgetItem(self.normalize_perm(i.permission)))

    def eventFilter(self, source, event):  # 事件监听
        if event.type() == QEvent.KeyPress and event.key() == 16777220:  # 检测键盘事件
            self.get_item_form_folder(self.ui.ComPath.currentText().strip())  # 执行事件
        return QWidget.eventFilter(self, source, event)  # 将事件交给上层对话框

    def get_item_form_folder(self, folder, flush=False):
        if flush:
            start_runnable(self.linker.get_folder_list, lambda x: self.add_item_to_filetable(x, folder), folder=folder,
                           flush=True)
        else:
            start_runnable(self.linker.get_folder_list, lambda x: self.add_item_to_filetable(x, folder), folder=folder,
                           flush=False)

    def file_tableWidget_menu(self, p):
        self.popMenu = QMenu()
        action = QAction('刷新', self)
        action.triggered.connect(self.refresh)
        self.popMenu.addAction(action)
        self.popMenu.addSeparator()
        action = QAction('上传文件', self)
        action.triggered.connect(self.upload_file)
        self.popMenu.addAction(action)
        action = QAction(u'下载文件', self)
        action.triggered.connect(lambda: self.ShowFileManage_data.file_Download_shell_Thread())
        self.popMenu.addAction(action)
        self.popMenu.addSeparator()
        filename = self.get_filename_from_tablewig()
        if filename and not filename.endswith(self.linker.separator):
            action = QAction('编辑', self)
            action.triggered.connect(self.open_file)
            self.popMenu.addAction(action)
            action = QAction('删除', self)
            action.triggered.connect(self.delete_file)
            self.popMenu.addAction(action)
        action = QAction('重命名', self)
        action.triggered.connect(self.rename_file)
        self.popMenu.addAction(action)
        # TODO 搞清楚复制粘贴的逻辑
        # action = QAction('复制', self)
        # action.triggered.connect(lambda: self.ShowFileManage_data.file_copy_shell())
        # self.popMenu.addAction(action)
        # action = QAction('粘贴', self)
        # action.triggered.connect(lambda: self.ShowFileManage_data.file_paste_shell_Thread())
        # self.popMenu.addAction(action)
        self.popMenu.addSeparator()
        action = QAction('修改文件(夹)时间', self)
        action.triggered.connect(self.modifyed_time)
        self.popMenu.addAction(action)
        self.name = self.popMenu.addMenu('新建')
        action = QAction('文件夹', self)
        action.triggered.connect(self.new_folder)
        self.name.addAction(action)
        action = QAction('文件', self)
        action.triggered.connect(self.new_file)
        self.name.addAction(action)
        self.ui.popMenu.exec_(self.file_tableWidget.mapToGlobal(p))

    def tabledoubleclicked(self, x, y):
        folder_name: str = self.ui.ComPath.currentText().strip() + self.linker.separator + self.ui.file_tableWidget.item(
            x,
            1).text()

        if folder_name.endswith(self.linker.separator):
            # 以文件分割符结尾，当然是文件架啦，所以调用获取文件夹内容
            self.get_item_form_folder(folder_name)
        else:
            self.open_file()

    @isloaded
    def refresh(self):
        self.linker.get_folder_list(self.current_folder, True)

    @isloaded
    def upload_file(self):
        @iscomplete
        def setresult(result):
            self.refresh()

        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "",
                                                  "All Files (*);;Python Files (*.py)", options=options)
        if fileName:
            _, remote_fileName = os.path.split(fileName)
            start_runnable(self.linker.upload_file, setresult, remote_file=remote_fileName, local_file=fileName)

    @isloaded
    def open_file(self):
        filename = self.get_filename_from_tablewig()
        edit_file(self.linker, filename, self.main)

    @isloaded
    def delete_file(self):
        @iscomplete
        def setresult(result):
            self.refresh()

        filename = self.get_filename_from_tablewig()
        start_runnable(self.linker.delete_file, setresult, remote_path=filename)

    @isloaded
    def rename_file(self):
        @iscomplete
        def setresult(result):
            self.refresh()

        old = self.get_filename_from_tablewig()
        text, okPressed = QInputDialog.getText(self, "pyshell", "pls input new name:", QLineEdit.Normal, " ")
        if okPressed and text.strip():
            new = self.ui.ComPath.currentText().strip() + self.linker.separator + text
            start_runnable(self.linker.rename, setresult, src=old, dst=new)

    def get_filename_from_tablewig(self):
        row = self.ui.file_tableWidget.selectionModel().currentIndex().row()
        try:
            filename: str = self.ui.ComPath.currentText().strip() + self.linker.separator + self.ui.file_tableWidget.item(
                row, 1).text()
        except AttributeError:
            filename = None
        return filename

    # TODO 未来的任务
    def modifyed_time(self):
        filename = self.get_filename_from_tablewig()

    @isloaded
    def new_folder(self):
        @iscomplete
        def setresult(result):
            self.refresh()

        text, okPressed = QInputDialog.getText(self, "pyshell", "pls input new folder name:", QLineEdit.Normal, " ")
        if okPressed and text.strip():
            folder = self.ui.ComPath.currentText().strip() + self.linker.separator + text
            start_runnable(self.linker.new_folder, setresult, folder_name=folder)

    @isloaded
    def new_file(self):
        @iscomplete
        def setresult(result):
            self.refresh()

        text, okPressed = QInputDialog.getText(self, "pyshell", "pls input new file name:", QLineEdit.Normal, " ")
        if okPressed and text.strip():
            filename = self.ui.ComPath.currentText().strip() + self.linker.separator + text
            start_runnable(self.linker.new_file, setresult, filename=filename)

    def treeclicked(self, p):
        path = [p.text(0)]
        while True:
            parent = p.parent()
            if parent is None:
                break
            else:
                path.append(parent.text(0))
                p = parent

        path.reverse()
        path = "".join(path)
        self.get_item_form_folder(path)

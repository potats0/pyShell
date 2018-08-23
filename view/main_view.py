from PyQt5 import uic
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow, QAction, QTableWidget, QTableWidgetItem

from model.db import db
from util import get_location_from_domain, start_runnable


class main_view(QMainWindow):
    def __init__(self, controller, parent=None):
        super(main_view, self).__init__(parent)
        self.ui = uic.loadUi("view/ui/main.ui", self)
        self.controller = controller
        self.controller.register_main(self)
        self.setWindowTitle('pyshell')  # 设置标题
        self.ui.tabWidget.setTabText(0, "shell")  # 设置标题
        self.ui.treeWidget.setHeaderLabels(['name', 'ID', 'Value'])
        self.ui.treeWidget.setColumnWidth(0, 150)  # 设置宽度  1是列号   2是宽度
        self.ui.treeWidget.setColumnWidth(1, 0)  # 设置宽度  1是列号   2是宽度
        self.ui.treeWidget.setHeaderHidden(True)  # 取消标题
        self.tabWidget.setTabsClosable(True)
        self.statusBar.showMessage('欢迎使用pyshell', 10000)
        self.tabWidget.setTabsClosable(True)  # 允许tab点击关闭

        self.__set_slot()
        self.createActions()
        self.tableWidget_ini()

    def display(self):
        self.ui.show()

    def __set_slot(self):
        # 右键响应设置
        self.tableWidget.setContextMenuPolicy(Qt.CustomContextMenu)
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.tableWidget.customContextMenuRequested.connect(self.controller.tableWidget_menu)
        # 设置关闭tab
        self.tabWidget.tabCloseRequested.connect(self.controller.closeTab)
        self.ui.tableWidget.cellDoubleClicked.connect(self.controller.tableWidget_right)

    def createActions(self):  # 加载菜单
        self.minimizeAction = QAction(u"最小化", self, triggered=self.hide)
        self.maximizeAction = QAction(u"最大化", self, triggered=self.showMaximized)
        self.restoreAction = QAction(u"还原", self, triggered=self.showNormal)

    def tableWidget_ini(self):
        self.db = db()
        self.tableWidget.setColumnCount(7)  # 列
        self.tableWidget.setRowCount(0)  # 行  len(node)
        self.tableWidget.setHorizontalHeaderLabels(['ID', '-', '网址', 'IP/物理位置', '备注', 'insert', 'update'])
        self.tableWidget.setColumnWidth(0, 0)  # 设置表格的各列的宽度值
        self.tableWidget.setColumnWidth(1, 40)  # 设置表格的各列的宽度值
        self.tableWidget.setColumnWidth(2, 300)  # 设置表格的各列的宽度值
        self.tableWidget.setColumnWidth(3, 290)  # 设置表格的各列的宽度值
        self.tableWidget.setColumnWidth(4, 90)  # 设置表格的各列的宽度值
        self.tableWidget.setColumnWidth(5, 150)  # 设置表格的各列的宽度值
        self.tableWidget.setColumnWidth(6, 150)  # 设置表格的各列的宽度值
        self.tableWidget.setRowHeight(0, 23)
        self.tableWidget.setEditTriggers(QTableWidget.NoEditTriggers)  # 设置表格的单元为只读属性，即不能编辑
        self.tableWidget.setSelectionBehavior(QTableWidget.SelectRows)  # 点击选择是选择行//设置选中时为整行选中
        self.tableWidget.setAlternatingRowColors(True)  # 还是只可以选择单行（单列）
        self.tableWidget.verticalHeader().hide()  # 隐藏行头



        start_runnable(self.refresh_table_item, lambda x: x)


    def refresh_table_item(self):
        rows = db().getall()
        for row in rows:
            i = self.ui.tableWidget.rowCount()
            self.ui.tableWidget.insertRow(i)
            self.ui.tableWidget.setItem(i, 0, QTableWidgetItem(str(row.id)))
            self.ui.tableWidget.setItem(i, 1, QTableWidgetItem(row.types))
            self.ui.tableWidget.setItem(i, 2, QTableWidgetItem(row.shell))
            self.ui.tableWidget.setItem(i, 3, QTableWidgetItem(get_location_from_domain(row.shell)))
            self.ui.tableWidget.setItem(i, 4, QTableWidgetItem(row.remark))
            self.ui.tableWidget.setItem(i, 5, QTableWidgetItem(row.createdtime))
            self.ui.tableWidget.setItem(i, 6, QTableWidgetItem(row.updatetime))

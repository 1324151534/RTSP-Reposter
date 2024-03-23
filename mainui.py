# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainui.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_RTSPReposter(object):
    def setupUi(self, RTSPReposter):
        RTSPReposter.setObjectName("RTSPReposter")
        RTSPReposter.resize(1280, 720)
        RTSPReposter.setMinimumSize(QtCore.QSize(800, 600))
        self.centralwidget = QtWidgets.QWidget(RTSPReposter)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setContentsMargins(25, 25, 25, 25)
        self.gridLayout.setObjectName("gridLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.tableWidget = QtWidgets.QTableWidget(self.centralwidget)
        self.tableWidget.setRowCount(0)
        self.tableWidget.setColumnCount(10)
        self.tableWidget.setObjectName("tableWidget")
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(5, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(6, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(7, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(8, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(9, item)
        self.verticalLayout.addWidget(self.tableWidget)
        spacerItem = QtWidgets.QSpacerItem(20, 10, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.verticalLayout.addItem(spacerItem)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.Switch = QtWidgets.QPushButton(self.centralwidget)
        self.Switch.setObjectName("Switch")
        self.horizontalLayout.addWidget(self.Switch)
        self.Delete = QtWidgets.QPushButton(self.centralwidget)
        self.Delete.setObjectName("Delete")
        self.horizontalLayout.addWidget(self.Delete)
        self.Add = QtWidgets.QPushButton(self.centralwidget)
        self.Add.setObjectName("Add")
        self.horizontalLayout.addWidget(self.Add)
        self.Start = QtWidgets.QPushButton(self.centralwidget)
        self.Start.setAutoDefault(False)
        self.Start.setDefault(False)
        self.Start.setFlat(False)
        self.Start.setObjectName("Start")
        self.horizontalLayout.addWidget(self.Start)
        self.horizontalLayout.setStretch(0, 3)
        self.horizontalLayout.setStretch(1, 3)
        self.horizontalLayout.setStretch(2, 3)
        self.horizontalLayout.setStretch(3, 3)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.verticalLayout.setStretch(0, 8)
        self.verticalLayout.setStretch(1, 1)
        self.verticalLayout.setStretch(2, 1)
        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)
        RTSPReposter.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(RTSPReposter)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1280, 22))
        self.menubar.setObjectName("menubar")
        self.menu = QtWidgets.QMenu(self.menubar)
        self.menu.setObjectName("menu")
        RTSPReposter.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(RTSPReposter)
        self.statusbar.setObjectName("statusbar")
        RTSPReposter.setStatusBar(self.statusbar)
        self.main = QtWidgets.QAction(RTSPReposter)
        self.main.setObjectName("main")
        self.quit = QtWidgets.QAction(RTSPReposter)
        self.quit.setObjectName("quit")
        self.menu.addAction(self.main)
        self.menu.addSeparator()
        self.menu.addAction(self.quit)
        self.menubar.addAction(self.menu.menuAction())

        self.retranslateUi(RTSPReposter)
        QtCore.QMetaObject.connectSlotsByName(RTSPReposter)

    def retranslateUi(self, RTSPReposter):
        _translate = QtCore.QCoreApplication.translate
        RTSPReposter.setWindowTitle(_translate("RTSPReposter", "RTSP Reposter 配置文件编辑器"))
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("RTSPReposter", "摄像头名"))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("RTSPReposter", "通道"))
        item = self.tableWidget.horizontalHeaderItem(2)
        item.setText(_translate("RTSPReposter", "状态"))
        item = self.tableWidget.horizontalHeaderItem(3)
        item.setText(_translate("RTSPReposter", "接收流地址"))
        item = self.tableWidget.horizontalHeaderItem(4)
        item.setText(_translate("RTSPReposter", "转发流地址"))
        item = self.tableWidget.horizontalHeaderItem(5)
        item.setText(_translate("RTSPReposter", "本地文件地址"))
        item = self.tableWidget.horizontalHeaderItem(6)
        item.setText(_translate("RTSPReposter", "显示时间戳"))
        item = self.tableWidget.horizontalHeaderItem(7)
        item.setText(_translate("RTSPReposter", "时间戳颜色"))
        item = self.tableWidget.horizontalHeaderItem(8)
        item.setText(_translate("RTSPReposter", "描述"))
        item = self.tableWidget.horizontalHeaderItem(9)
        item.setText(_translate("RTSPReposter", "是否启用"))
        self.Switch.setText(_translate("RTSPReposter", "选中状态切换"))
        self.Delete.setText(_translate("RTSPReposter", "删除选中"))
        self.Add.setText(_translate("RTSPReposter", "添加新转发"))
        self.Start.setText(_translate("RTSPReposter", "启动转发服务"))
        self.menu.setTitle(_translate("RTSPReposter", "菜单"))
        self.main.setText(_translate("RTSPReposter", "推流设置"))
        self.quit.setText(_translate("RTSPReposter", "退出"))

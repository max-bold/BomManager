# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'MainW.ui'
##
## Created by: Qt User Interface Compiler version 6.4.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QApplication, QComboBox, QFormLayout, QFrame,
    QGroupBox, QHBoxLayout, QHeaderView, QLabel,
    QLineEdit, QListWidget, QListWidgetItem, QMainWindow,
    QMenu, QMenuBar, QPushButton, QRadioButton,
    QSizePolicy, QSpacerItem, QStatusBar, QTabWidget,
    QTableWidget, QTableWidgetItem, QTreeWidget, QTreeWidgetItem,
    QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(800, 633)
        self.actionExport = QAction(MainWindow)
        self.actionExport.setObjectName(u"actionExport")
        self.actionExit = QAction(MainWindow)
        self.actionExit.setObjectName(u"actionExit")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.horizontalLayout_4 = QHBoxLayout(self.centralwidget)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.treeWidget = QTreeWidget(self.centralwidget)
        __qtreewidgetitem = QTreeWidgetItem()
        __qtreewidgetitem.setText(0, u"1");
        self.treeWidget.setHeaderItem(__qtreewidgetitem)
        self.treeWidget.setObjectName(u"treeWidget")
        self.treeWidget.setFrameShape(QFrame.NoFrame)
        self.treeWidget.setFrameShadow(QFrame.Plain)

        self.horizontalLayout_4.addWidget(self.treeWidget)

        self.line = QFrame(self.centralwidget)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.VLine)
        self.line.setFrameShadow(QFrame.Sunken)

        self.horizontalLayout_4.addWidget(self.line)

        self.tabWidget = QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName(u"tabWidget")
        self.deatilstab = QWidget()
        self.deatilstab.setObjectName(u"deatilstab")
        self.formLayout = QFormLayout(self.deatilstab)
        self.formLayout.setObjectName(u"formLayout")
        self.formLayout.setContentsMargins(-1, -1, -1, 0)
        self.label = QLabel(self.deatilstab)
        self.label.setObjectName(u"label")

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.label)

        self.lineEdit = QLineEdit(self.deatilstab)
        self.lineEdit.setObjectName(u"lineEdit")

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.lineEdit)

        self.label_2 = QLabel(self.deatilstab)
        self.label_2.setObjectName(u"label_2")

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.label_2)

        self.lineEdit_2 = QLineEdit(self.deatilstab)
        self.lineEdit_2.setObjectName(u"lineEdit_2")

        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.lineEdit_2)

        self.label_3 = QLabel(self.deatilstab)
        self.label_3.setObjectName(u"label_3")

        self.formLayout.setWidget(2, QFormLayout.LabelRole, self.label_3)

        self.lineEdit_3 = QLineEdit(self.deatilstab)
        self.lineEdit_3.setObjectName(u"lineEdit_3")

        self.formLayout.setWidget(2, QFormLayout.FieldRole, self.lineEdit_3)

        self.label_4 = QLabel(self.deatilstab)
        self.label_4.setObjectName(u"label_4")

        self.formLayout.setWidget(3, QFormLayout.LabelRole, self.label_4)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.lineEdit_4 = QLineEdit(self.deatilstab)
        self.lineEdit_4.setObjectName(u"lineEdit_4")

        self.horizontalLayout.addWidget(self.lineEdit_4)

        self.comboBox = QComboBox(self.deatilstab)
        self.comboBox.setObjectName(u"comboBox")

        self.horizontalLayout.addWidget(self.comboBox)


        self.formLayout.setLayout(3, QFormLayout.FieldRole, self.horizontalLayout)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.formLayout.setItem(4, QFormLayout.SpanningRole, self.horizontalSpacer)

        self.label_5 = QLabel(self.deatilstab)
        self.label_5.setObjectName(u"label_5")

        self.formLayout.setWidget(5, QFormLayout.LabelRole, self.label_5)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.comboBox_2 = QComboBox(self.deatilstab)
        self.comboBox_2.setObjectName(u"comboBox_2")

        self.horizontalLayout_2.addWidget(self.comboBox_2)

        self.pushButton = QPushButton(self.deatilstab)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setMaximumSize(QSize(30, 50))
        icon = QIcon(QIcon.fromTheme(u"applications-development"))
        self.pushButton.setIcon(icon)

        self.horizontalLayout_2.addWidget(self.pushButton)


        self.formLayout.setLayout(5, QFormLayout.FieldRole, self.horizontalLayout_2)

        self.label_6 = QLabel(self.deatilstab)
        self.label_6.setObjectName(u"label_6")

        self.formLayout.setWidget(6, QFormLayout.LabelRole, self.label_6)

        self.comboBox_3 = QComboBox(self.deatilstab)
        self.comboBox_3.setObjectName(u"comboBox_3")

        self.formLayout.setWidget(6, QFormLayout.FieldRole, self.comboBox_3)

        self.listWidget = QListWidget(self.deatilstab)
        self.listWidget.setObjectName(u"listWidget")
        self.listWidget.setAutoFillBackground(True)
        self.listWidget.setFrameShape(QFrame.NoFrame)

        self.formLayout.setWidget(9, QFormLayout.SpanningRole, self.listWidget)

        self.label_7 = QLabel(self.deatilstab)
        self.label_7.setObjectName(u"label_7")

        self.formLayout.setWidget(8, QFormLayout.SpanningRole, self.label_7)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.formLayout.setItem(7, QFormLayout.SpanningRole, self.horizontalSpacer_2)

        self.tabWidget.addTab(self.deatilstab, "")
        self.comptab = QWidget()
        self.comptab.setObjectName(u"comptab")
        self.verticalLayout = QVBoxLayout(self.comptab)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(-1, -1, -1, 0)
        self.groupBox = QGroupBox(self.comptab)
        self.groupBox.setObjectName(u"groupBox")
        self.horizontalLayout_3 = QHBoxLayout(self.groupBox)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(-1, 0, -1, 0)
        self.radioButton_2 = QRadioButton(self.groupBox)
        self.radioButton_2.setObjectName(u"radioButton_2")
        self.radioButton_2.setMaximumSize(QSize(200, 16777215))

        self.horizontalLayout_3.addWidget(self.radioButton_2)

        self.radioButton = QRadioButton(self.groupBox)
        self.radioButton.setObjectName(u"radioButton")
        self.radioButton.setMaximumSize(QSize(200, 16777215))

        self.horizontalLayout_3.addWidget(self.radioButton)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Minimum)

        self.horizontalLayout_3.addItem(self.verticalSpacer)

        self.horizontalLayout_3.setStretch(2, 1)

        self.verticalLayout.addWidget(self.groupBox)

        self.tableWidget = QTableWidget(self.comptab)
        self.tableWidget.setObjectName(u"tableWidget")
        self.tableWidget.setFrameShape(QFrame.NoFrame)
        self.tableWidget.setFrameShadow(QFrame.Plain)

        self.verticalLayout.addWidget(self.tableWidget)

        self.tabWidget.addTab(self.comptab, "")

        self.horizontalLayout_4.addWidget(self.tabWidget)

        self.horizontalLayout_4.setStretch(0, 1)
        self.horizontalLayout_4.setStretch(2, 2)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 800, 22))
        self.menuFile = QMenu(self.menubar)
        self.menuFile.setObjectName(u"menuFile")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menuFile.menuAction())
        self.menuFile.addAction(self.actionExport)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionExit)

        self.retranslateUi(MainWindow)

        self.tabWidget.setCurrentIndex(1)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.actionExport.setText(QCoreApplication.translate("MainWindow", u"Export", None))
        self.actionExit.setText(QCoreApplication.translate("MainWindow", u"Exit", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"Part number", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"Name (eng)", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"Name (rus)", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"Quantity", None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"Manufacturer", None))
        self.pushButton.setText("")
        self.label_6.setText(QCoreApplication.translate("MainWindow", u"Man P/N", None))
        self.label_7.setText(QCoreApplication.translate("MainWindow", u"Files", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.deatilstab), QCoreApplication.translate("MainWindow", u"Details", None))
        self.groupBox.setTitle(QCoreApplication.translate("MainWindow", u"GroupBox", None))
        self.radioButton_2.setText(QCoreApplication.translate("MainWindow", u"Top level", None))
        self.radioButton.setText(QCoreApplication.translate("MainWindow", u"Flat view", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.comptab), QCoreApplication.translate("MainWindow", u"Components", None))
        self.menuFile.setTitle(QCoreApplication.translate("MainWindow", u"File", None))
    # retranslateUi


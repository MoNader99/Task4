# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Gui.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1888, 1612)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.tabWidget.setFont(font)
        self.tabWidget.setObjectName("tabWidget")
        self.tab_5 = QtWidgets.QWidget()
        self.tab_5.setObjectName("tab_5")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.tab_5)
        self.verticalLayout.setObjectName("verticalLayout")
        self.groupBox = QtWidgets.QGroupBox(self.tab_5)
        self.groupBox.setTitle("")
        self.groupBox.setObjectName("groupBox")
        self.gridLayout = QtWidgets.QGridLayout(self.groupBox)
        self.gridLayout.setObjectName("gridLayout")
        self.MixerSlider = QtWidgets.QSlider(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.MixerSlider.sizePolicy().hasHeightForWidth())
        self.MixerSlider.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(17)
        self.MixerSlider.setFont(font)
        self.MixerSlider.setFocusPolicy(QtCore.Qt.TabFocus)
        self.MixerSlider.setMaximum(10)
        self.MixerSlider.setPageStep(1)
        self.MixerSlider.setOrientation(QtCore.Qt.Horizontal)
        self.MixerSlider.setTickPosition(QtWidgets.QSlider.TicksBelow)
        self.MixerSlider.setObjectName("MixerSlider")
        self.gridLayout.addWidget(self.MixerSlider, 0, 4, 1, 1)
        self.BrowseButton = QtWidgets.QPushButton(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.BrowseButton.sizePolicy().hasHeightForWidth())
        self.BrowseButton.setSizePolicy(sizePolicy)
        self.BrowseButton.setMinimumSize(QtCore.QSize(0, 50))
        self.BrowseButton.setMaximumSize(QtCore.QSize(16777215, 601))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.BrowseButton.setFont(font)
        self.BrowseButton.setObjectName("BrowseButton")
        self.gridLayout.addWidget(self.BrowseButton, 0, 0, 1, 1)
        self.SelectedSong = QtWidgets.QComboBox(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.SelectedSong.sizePolicy().hasHeightForWidth())
        self.SelectedSong.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(17)
        self.SelectedSong.setFont(font)
        self.SelectedSong.setObjectName("SelectedSong")
        self.SelectedSong.addItem("")
        self.SelectedSong.addItem("")
        self.gridLayout.addWidget(self.SelectedSong, 0, 2, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.groupBox)
        font = QtGui.QFont()
        font.setPointSize(17)
        self.label_2.setFont(font)
        self.label_2.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 0, 1, 1, 1)
        self.BrowseButton_2 = QtWidgets.QPushButton(self.groupBox)
        self.BrowseButton_2.setMinimumSize(QtCore.QSize(0, 60))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.BrowseButton_2.setFont(font)
        self.BrowseButton_2.setObjectName("BrowseButton_2")
        self.gridLayout.addWidget(self.BrowseButton_2, 1, 0, 1, 1)
        self.verticalLayout.addWidget(self.groupBox)
        self.groupBox_4 = QtWidgets.QGroupBox(self.tab_5)
        self.groupBox_4.setTitle("")
        self.groupBox_4.setObjectName("groupBox_4")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.groupBox_4)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.GenerateButton = QtWidgets.QPushButton(self.groupBox_4)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.GenerateButton.sizePolicy().hasHeightForWidth())
        self.GenerateButton.setSizePolicy(sizePolicy)
        self.GenerateButton.setMinimumSize(QtCore.QSize(0, 100))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.GenerateButton.setFont(font)
        self.GenerateButton.setObjectName("GenerateButton")
        self.horizontalLayout.addWidget(self.GenerateButton)
        self.verticalLayout.addWidget(self.groupBox_4)
        self.groupBox_2 = QtWidgets.QGroupBox(self.tab_5)
        self.groupBox_2.setTitle("")
        self.groupBox_2.setObjectName("groupBox_2")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.groupBox_2)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.SongsTable = QtWidgets.QTableWidget(self.groupBox_2)
        self.SongsTable.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.SongsTable.setFrameShadow(QtWidgets.QFrame.Plain)
        self.SongsTable.setLineWidth(67)
        self.SongsTable.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustIgnored)
        self.SongsTable.setTextElideMode(QtCore.Qt.ElideMiddle)
        self.SongsTable.setRowCount(10)
        self.SongsTable.setObjectName("SongsTable")
        self.SongsTable.setColumnCount(2)
        item = QtWidgets.QTableWidgetItem()
        self.SongsTable.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.SongsTable.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setPointSize(10)
        item.setFont(font)
        self.SongsTable.setItem(0, 0, item)
        item = QtWidgets.QTableWidgetItem()
        self.SongsTable.setItem(0, 1, item)
        item = QtWidgets.QTableWidgetItem()
        self.SongsTable.setItem(1, 0, item)
        item = QtWidgets.QTableWidgetItem()
        self.SongsTable.setItem(1, 1, item)
        self.SongsTable.horizontalHeader().setVisible(True)
        self.SongsTable.horizontalHeader().setCascadingSectionResizes(False)
        self.SongsTable.horizontalHeader().setDefaultSectionSize(840)
        self.SongsTable.horizontalHeader().setSortIndicatorShown(True)
        self.SongsTable.horizontalHeader().setStretchLastSection(True)
        self.SongsTable.verticalHeader().setCascadingSectionResizes(False)
        self.SongsTable.verticalHeader().setDefaultSectionSize(83)
        self.SongsTable.verticalHeader().setSortIndicatorShown(True)
        self.SongsTable.verticalHeader().setStretchLastSection(True)
        self.verticalLayout_3.addWidget(self.SongsTable)
        self.groupBox_5 = QtWidgets.QGroupBox(self.groupBox_2)
        self.groupBox_5.setTitle("")
        self.groupBox_5.setObjectName("groupBox_5")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.groupBox_5)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.Play_Mix = QtWidgets.QPushButton(self.groupBox_5)
        self.Play_Mix.setMinimumSize(QtCore.QSize(0, 100))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.Play_Mix.setFont(font)
        self.Play_Mix.setObjectName("Play_Mix")
        self.verticalLayout_5.addWidget(self.Play_Mix)
        self.Stop_Button = QtWidgets.QPushButton(self.groupBox_5)
        self.Stop_Button.setObjectName("Stop_Button")
        self.verticalLayout_5.addWidget(self.Stop_Button)
        self.verticalLayout_3.addWidget(self.groupBox_5)
        self.verticalLayout.addWidget(self.groupBox_2)
        self.tabWidget.addTab(self.tab_5, "")
        self.tab_6 = QtWidgets.QWidget()
        self.tab_6.setObjectName("tab_6")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.tab_6)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.groupBox_3 = QtWidgets.QGroupBox(self.tab_6)
        self.groupBox_3.setTitle("")
        self.groupBox_3.setObjectName("groupBox_3")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.groupBox_3)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.Spectrogram_1 = PlotWidget(self.groupBox_3)
        self.Spectrogram_1.setObjectName("Spectrogram_1")
        self.gridLayout_2.addWidget(self.Spectrogram_1, 1, 0, 1, 1)
        self.Spectrogram_2 = PlotWidget(self.groupBox_3)
        self.Spectrogram_2.setObjectName("Spectrogram_2")
        self.gridLayout_2.addWidget(self.Spectrogram_2, 3, 0, 1, 1)
        self.groupBox_7 = QtWidgets.QGroupBox(self.groupBox_3)
        self.groupBox_7.setTitle("")
        self.groupBox_7.setObjectName("groupBox_7")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.groupBox_7)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label = QtWidgets.QLabel(self.groupBox_7)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.horizontalLayout_3.addWidget(self.label)
        self.Play_2 = QtWidgets.QPushButton(self.groupBox_7)
        self.Play_2.setObjectName("Play_2")
        self.horizontalLayout_3.addWidget(self.Play_2)
        self.gridLayout_2.addWidget(self.groupBox_7, 2, 0, 1, 1)
        self.groupBox_6 = QtWidgets.QGroupBox(self.groupBox_3)
        self.groupBox_6.setTitle("")
        self.groupBox_6.setObjectName("groupBox_6")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.groupBox_6)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_3 = QtWidgets.QLabel(self.groupBox_6)
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_2.addWidget(self.label_3)
        self.Play_1 = QtWidgets.QPushButton(self.groupBox_6)
        self.Play_1.setObjectName("Play_1")
        self.horizontalLayout_2.addWidget(self.Play_1)
        self.gridLayout_2.addWidget(self.groupBox_6, 0, 0, 1, 1)
        self.verticalLayout_4.addWidget(self.groupBox_3)
        self.Stop_Button_2 = QtWidgets.QPushButton(self.tab_6)
        self.Stop_Button_2.setObjectName("Stop_Button_2")
        self.verticalLayout_4.addWidget(self.Stop_Button_2)
        self.tabWidget.addTab(self.tab_6, "")
        self.verticalLayout_2.addWidget(self.tabWidget)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1888, 37))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.BrowseButton.setText(_translate("MainWindow", "Choose First Song"))
        self.SelectedSong.setItemText(0, _translate("MainWindow", "First_Song"))
        self.SelectedSong.setItemText(1, _translate("MainWindow", "Second-Song"))
        self.label_2.setText(_translate("MainWindow", "Select the song"))
        self.BrowseButton_2.setText(_translate("MainWindow", "Choose Second Song"))
        self.GenerateButton.setText(_translate("MainWindow", "Check"))
        item = self.SongsTable.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "SongName"))
        item = self.SongsTable.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "SimilarityiIndex"))
        __sortingEnabled = self.SongsTable.isSortingEnabled()
        self.SongsTable.setSortingEnabled(False)
        self.SongsTable.setSortingEnabled(__sortingEnabled)
        self.Play_Mix.setText(_translate("MainWindow", " Mix-Play"))
        self.Stop_Button.setText(_translate("MainWindow", "Stop"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_5), _translate("MainWindow", "Mixer - table"))
        self.label.setText(_translate("MainWindow", " Second Song"))
        self.Play_2.setText(_translate("MainWindow", "Play"))
        self.label_3.setText(_translate("MainWindow", "First Song"))
        self.Play_1.setText(_translate("MainWindow", "Play"))
        self.Stop_Button_2.setText(_translate("MainWindow", "Stop"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_6), _translate("MainWindow", "Spectrograms"))

from pyqtgraph import PlotWidget

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())


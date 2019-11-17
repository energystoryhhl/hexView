from PyQt5 import QtWidgets, QtGui
import sys

from hexedit import *
from tabWidget import *
from HexFile import *
from mergeWidget import *
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QTreeWidget, QTreeWidgetItem, QDialog
from PyQt5.QtCore import *
from PyQt5.QtGui import *


class mergeWindow(QDialog):
    def __init__(self):
        QDialog.__init__(self)
        self.child = Ui_Form()
        self.child.setupUi(self)

class MyWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MyWindow, self).__init__(parent)

        self.hexs_ = {}
        self.hexNames_ = []
        self.tabs_ = []
        self.mergeWidget = mergeWindow()

        self.setupUi(self)
        # self.creatTabs()

    def Onopen(self):
        # print("openfile")
        openFileName = QFileDialog.getOpenFileName(self, '选择文件', '', 'Hex files(*.hex )')
        # print(openFileName[0])
        if openFileName[0] == "":
            pass
        else:
            self.hexopen(openFileName[0])

    def hexopen(self, fileName):
        newHexFile = HexFile(fileName)

        if newHexFile.endAddr_ == 0:
            self.textBrowser.append("hex file open error")
        else:
            hexName = str(fileName).split("/")[-1]
            self.hexs_[hexName] = newHexFile
            self.hexNames_.append(hexName)

            self.textBrowser.append("Open Hex: " + fileName)
            ######################
            self.addTab(hexName)
            self.flashTab( self.hexNames_.index(hexName), self.hexs_[hexName])


    def addTab(self, hexName):
        newTab = Ui_tabWidget()
        newTab.setupUi(newTab)
        newTab.treeWidget.setHeaderHidden(True)
        self.tabWidget.addTab(newTab, hexName)
        self.tabs_.append(newTab)

    def flashTab(self,tabNum, hexFile):
        self.tabs_[tabNum].treeWidget.clear()
        root = QTreeWidgetItem(self.tabs_[tabNum].treeWidget)
        tittle = "start: "
        tittle += str(hex(hexFile.startAddr_))
        tittle += "  "
        tittle += "end: "
        tittle += str(hex(hexFile.endAddr_))
        tittle += "  "
        tittle += "size: "
        tittle += str(hex(hexFile.endAddr_ - hexFile.startAddr_ + 1))

        root.setText(0, tittle)
        i = 0
        for block in hexFile.getBlocks():
            child = QTreeWidgetItem()
            tittle = "block "
            tittle += str(i)
            tittle += ": "
            tittle += "start: "
            tittle += str(hex(block["startAddr"]))
            tittle += "  "
            tittle += "end: "
            tittle += str(hex(block["endAddr"]))
            tittle += "  "
            tittle += "size: "
            tittle += str(block["endAddr"] - block["startAddr"] + 1)
            child.setText(0, tittle)
            root.addChild(child)
            i = i + 1
        self.tabs_[tabNum].treeWidget.expandAll()

    def delTab(self, tabNum):
        self.tabs_.pop(tabNum)

    def delHex(self,hexNum):
        self.hexs_.pop(self.hexNames_[hexNum])
        self.hexNames_.pop(hexNum)
        self.delTab(hexNum)

    def btnMergeHex(self):
        self.mergeWidget.show()


    def mergeHex(self):
        startAddrText = (self.mergeWidget.child.lineEdit.text())
        lengthText = (self.mergeWidget.child.lineEdit_2.text())
        if startAddrText != '' and lengthText != '' and self.tabs_.__sizeof__() != 0:
            startAddr = int(startAddrText, 16)
            length = int(lengthText, 16)

            hexNum = self.tabWidget.currentIndex()
            hexName = self.hexNames_[hexNum]

            self.textBrowser.append("Merge hex ")
            self.textBrowser.append("Start addr: ")
            self.textBrowser.append(str(hex(startAddr)))
            self.textBrowser.append("Length: ")
            self.textBrowser.append(str(hex(length)))

            self.hexs_[hexName].mergeAllBlocks(startAddr, length)

            self.textBrowser.append("Done")
            self.flashTab(hexNum,self.hexs_[hexName])
            self.mergeWidget.hide()
        else:
            pass


    def initConfig(self):
        self.createTabs()
        self.setAcceptDrops(True)
        self.actionOpen.triggered.connect(self.Onopen)
        self.actionMerge.triggered.connect(self.btnMergeHex)

        sys.stdout = self.outputWritten

        ##merge
        self.mergeWidget.child.pushButton.clicked.connect(self.mergeHex)
        self.mergeWidget.child.pushButton_2.clicked.connect(self.mergeWidget.hide)
        # self.actionSave_As.triggered.connect(self.Onopen)


    def createTabs(self):
        pass

    def dragEnterEvent(self, evn):
        evn.accept()

    def dropEvent(self, evn):
        # self.textBrowser.append('文件路径： ' + evn.mimeData().text())
        # print(str(evn.mimeData().text()).split("///")[-1])
        self.hexopen(str(evn.mimeData().text()).split("///")[-1])

    def outputWritten(self, text):
        self.textBrowser.append(text)




if __name__ == '__main__':
    app = QApplication(sys.argv)
    myWin = MyWindow()
    myWin.show()
    myWin.initConfig()
    sys.exit(app.exec_())

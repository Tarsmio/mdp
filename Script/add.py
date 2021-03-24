from PyQt5 import QtWidgets, QtCore, QtGui
import json
import sys

class AddWindow(QtWidgets.QMainWindow):
  def __init__(self, mclass, parent=None, option=False):
    super(AddWindow, self).__init__(parent)

    with open('save.json', 'r', encoding='utf-8') as f:
      self.save = json.load(f)
    
    self.mainClass = mclass
    self.option = option

    self.initUI()
  
  def initUI(self):
    self.main_widget = QtWidgets.QWidget()
    self.main_Tab = QtWidgets.QTabWidget()
    self.setWindowTitle(self.mainClass.langueTexte["title"]["2"])

    self.main_Tab.setProperty("cssClass", "tab")

    self.nameEnter = QtWidgets.QLineEdit(self.mainClass.langueTexte["editLine"]["3"], self)
    self.valueEnter = QtWidgets.QTextEdit(self.mainClass.langueTexte["editLine"]["4"], self)

    self.radTypeGoogleSelect = QtWidgets.QRadioButton('Google', self)
    self.radTypeTwitterSelect = QtWidgets.QRadioButton('Twitter', self)
    self.radTypeDiscordSelect = QtWidgets.QRadioButton('Discord', self)
    self.radTypeInstaSelect = QtWidgets.QRadioButton('Instagram', self)
    self.radTypeSnapSelect = QtWidgets.QRadioButton('Snapchat', self)
    self.radTypeAutreSelect = QtWidgets.QRadioButton('Autre', self)

    self.valide = QtWidgets.QPushButton(self.mainClass.langueTexte["button"]["4"], self)
    self.annule = QtWidgets.QPushButton(self.mainClass.langueTexte["button"]["5"], self)

    self.valueWidget = QtWidgets.QWidget()
    self.typeWidget = QtWidgets.QWidget()

    self.valueWidget.setProperty("cssClass", "tabWidget")
    self.typeWidget.setProperty("cssClass", "tabWidget")

    self.main_Tab.addTab(self.valueWidget, QtGui.QIcon(), self.mainClass.langueTexte["tab"]["1"])
    self.main_Tab.addTab(self.typeWidget, QtGui.QIcon(), self.mainClass.langueTexte["tab"]["2"])

    self.mainLayout = QtWidgets.QVBoxLayout()
    self.buttonLayout = QtWidgets.QGridLayout()
    self.valueLayout = QtWidgets.QVBoxLayout()
    self.typeLayout = QtWidgets.QGridLayout()

    self.valueLayout.addWidget(self.nameEnter, 1)
    self.valueLayout.addWidget(self.valueEnter, 2)

    self.typeLayout.addWidget(self.radTypeGoogleSelect, 1, 1)
    self.typeLayout.addWidget(self.radTypeDiscordSelect, 2, 1)
    self.typeLayout.addWidget(self.radTypeTwitterSelect, 3, 1)
    self.typeLayout.addWidget(self.radTypeInstaSelect, 1, 2)
    self.typeLayout.addWidget(self.radTypeSnapSelect, 2, 2)
    self.typeLayout.addWidget(self.radTypeAutreSelect, 3, 2)

    self.buttonLayout.addWidget(self.valide, 1, 1)
    self.buttonLayout.addWidget(self.annule, 1, 2)

    self.mainLayout.addWidget(self.main_Tab)
    self.mainLayout.addLayout(self.buttonLayout)

    self.main_widget.setLayout(self.mainLayout)
    self.valueWidget.setLayout(self.valueLayout)
    self.typeWidget.setLayout(self.typeLayout)

    self.setCentralWidget(self.main_widget)

    self.initButton()
    self.initPassword()

    self.setFixedSize(274, 265)

    self.show()

  def initButton(self):
    self.radTypeAutreSelect.setChecked(True)
    self.currentType = 'Autre'

    self.valide.clicked.connect(self.pret)
    self.annule.clicked.connect(self.quitThis)

    self.radTypeAutreSelect.toggled.connect(self.onCheck)
    self.radTypeDiscordSelect.toggled.connect(self.onCheck)
    self.radTypeGoogleSelect.toggled.connect(self.onCheck)
    self.radTypeInstaSelect.toggled.connect(self.onCheck)
    self.radTypeTwitterSelect.toggled.connect(self.onCheck)
    self.radTypeSnapSelect.toggled.connect(self.onCheck)

  def initPassword(self):
    if self.option:
      print("test1")
      if "password" in self.option:
        print(self.option)
        self.valueEnter.setText(self.option["password"])

  def onCheck(self):
    selected = self.sender()

    if selected.isChecked():
      self.currentType = selected.text()

    print(self.currentType)

  def pret(self):

    textName = self.nameEnter.text()
    textMdp = self.valueEnter.toPlainText()

    if self.save['mdp'] != []:
      for i in range(len(self.save['mdp'])):
        if self.save['mdp'][i]['name'] == textName:
          return QtWidgets.QMessageBox().information(self, self.mainClass.langueTexte["messBox"]["3"], self.mainClass.langueTexte["messBox"]["4"])

    final = self.save['mdp']

    final.append({
      'name':textName,
      'value':textMdp,
      'type':self.currentType
    })

    vFinal = {
      "mdp": final
    }

    with open('save.json', 'w', encoding='utf-8') as n:
      json.dump(vFinal, n)

    self.mainClass.makeListe()

    self.hide()

  def quitThis(self):

    self.hide()
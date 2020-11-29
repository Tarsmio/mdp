from PyQt5 import QtWidgets, QtCore, QtGui
import json

class modWindow(QtWidgets.QMainWindow):

  def __init__(self, mclass, element, parent=None):
    super(modWindow, self).__init__(parent)

    self.mainClass = mclass
    self.element = element

    with open('save.json', 'r', encoding='utf-8') as f:
      self.saveF = json.load(f)

    self.vsave = self.saveF['mdp']

    for i in range(len(self.vsave)):
      if self.vsave[i]['name'] == self.element.text():
        self.elementNumber = i

    self.initUI()

  def initUI(self):
    self.main_widget = QtWidgets.QWidget()
    self.main_Tab = QtWidgets.QTabWidget()
    self.setWindowTitle("Modifier")

    self.nameEnter = QtWidgets.QLineEdit(self.vsave[self.elementNumber]['name'], self)
    self.valueEnter = QtWidgets.QTextEdit(self.vsave[self.elementNumber]['value'], self)

    self.radTypeGoogleSelect = QtWidgets.QRadioButton('Google', self)
    self.radTypeTwitterSelect = QtWidgets.QRadioButton('Twitter', self)
    self.radTypeDiscordSelect = QtWidgets.QRadioButton('Discord', self)
    self.radTypeInstaSelect = QtWidgets.QRadioButton('Instagram', self)
    self.radTypeAutreSelect = QtWidgets.QRadioButton('Autre', self)

    self.valide = QtWidgets.QPushButton('Valider', self)
    self.annule = QtWidgets.QPushButton('Annuler', self)

    self.valueWidget = QtWidgets.QWidget()
    self.typeWidget = QtWidgets.QWidget()

    self.main_Tab.addTab(self.valueWidget, QtGui.QIcon(), 'Valeurs')
    self.main_Tab.addTab(self.typeWidget, QtGui.QIcon(), 'Type')

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
    self.typeLayout.addWidget(self.radTypeAutreSelect, 2, 2)

    self.mainLayout = QtWidgets.QVBoxLayout()
    self.buttonLayout = QtWidgets.QGridLayout()

    self.buttonLayout.addWidget(self.valide, 1, 1)
    self.buttonLayout.addWidget(self.annule, 1, 2)

    self.mainLayout.addWidget(self.main_Tab)
    self.mainLayout.addLayout(self.buttonLayout)

    self.main_widget.setLayout(self.mainLayout)
    self.valueWidget.setLayout(self.valueLayout)
    self.typeWidget.setLayout(self.typeLayout)

    self.setCentralWidget(self.main_widget)

    self.initButton()

    self.setFixedSize(274, 265)

    self.show()

  def initButton(self):
    self.valide.clicked.connect(self.validation)
    self.annule.clicked.connect(self.quitThis)

    self.initRadio()
    self.radTypeAutreSelect.toggled.connect(self.onCheck)
    self.radTypeDiscordSelect.toggled.connect(self.onCheck)
    self.radTypeGoogleSelect.toggled.connect(self.onCheck)
    self.radTypeInstaSelect.toggled.connect(self.onCheck)
    self.radTypeTwitterSelect.toggled.connect(self.onCheck)

  def initRadio(self):
    if self.vsave[self.elementNumber].get('type') is None:
      self.radTypeAutreSelect.setChecked(True)
      self.currentType = "Autre"
    else :
      if self.vsave[self.elementNumber]['type'] == "Autre":
        self.radTypeAutreSelect.setChecked(True)
        self.currentType = "Autre"
      elif self.vsave[self.elementNumber]['type'] == "Google":
        self.radTypeGoogleSelect.setChecked(True)
        self.currentType = "Google"
      elif self.vsave[self.elementNumber]['type'] == "Discord":
        self.radTypeDiscordSelect.setChecked(True)
        self.currentType = "Discord"
      elif self.vsave[self.elementNumber]['type'] == "Twitter":
        self.radTypeTwitterSelect.setChecked(True)
        self.currentType = "Twitter"
      elif self.vsave[self.elementNumber]['type'] == "Instagram":
        self.radTypeInstaSelect.setChecked(True)
        self.currentType = "Instagram"

  def onCheck(self):
    selected = self.sender()

    if selected.isChecked():
      self.currentType = selected.text()

    print(self.currentType)

  def validation(self):
    textName = self.nameEnter.text()
    textMdp = self.valueEnter.toPlainText()

    if textName != self.vsave[self.elementNumber]['name']:
      if self.vsave != []:
        for i in range(len(self.vsave)):
          if self.vsave[i]['name'] == textName:
            return QtWidgets.QMessageBox().information(self, 'Info', 'Ce mot de passe existe deja !')

    final = self.vsave

    final[self.elementNumber] = {
      'name':textName,
      'value':textMdp,
      'type':self.currentType
    }

    vFinal = {
      "mdp": final
    }

    with open('save.json', 'w', encoding='utf-8') as n:
      json.dump(vFinal, n)

    self.mainClass.makeListe()

    self.hide()

  def quitThis(self):

    self.hide()
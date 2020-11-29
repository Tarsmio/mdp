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
    self.setWindowTitle("Modifier")

    self.nameEnter = QtWidgets.QLineEdit(self.vsave[self.elementNumber]['name'], self)
    self.valueEnter = QtWidgets.QTextEdit(self.vsave[self.elementNumber]['value'], self)
    self.valide = QtWidgets.QPushButton('Valider', self)
    self.annule = QtWidgets.QPushButton('Annuler', self)

    self.mainLayout = QtWidgets.QVBoxLayout()
    self.buttonLayout = QtWidgets.QGridLayout()

    self.buttonLayout.addWidget(self.valide, 1, 1)
    self.buttonLayout.addWidget(self.annule, 1, 2)

    self.mainLayout.addWidget(self.nameEnter)
    self.mainLayout.addWidget(self.valueEnter)
    self.mainLayout.addLayout(self.buttonLayout)

    self.main_widget.setLayout(self.mainLayout)

    self.setCentralWidget(self.main_widget)

    self.initButton()

    self.show()

  def initButton(self):
    self.valide.clicked.connect(self.validation)
    self.annule.clicked.connect(self.quitThis)

  def validation(self):
    textName = self.nameEnter.text()
    textMdp = self.valueEnter.toPlainText()

    if self.vsave != []:
      for i in range(len(self.vsave)):
        if self.vsave[i]['name'] == textName:
          return QtWidgets.QMessageBox().information(self, 'Info', 'Ce mot de passe existe deja !')

    final = self.vsave

    final[self.elementNumber] = {
      'name':textName,
      'value':textMdp
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
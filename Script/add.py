from PyQt5 import QtWidgets, QtCore, QtGui
import json
import sys

class AddWindow(QtWidgets.QMainWindow):
  def __init__(self, mclass, parent=None):
    super(AddWindow, self).__init__(parent)

    with open('save.json', 'r', encoding='utf-8') as f:
      self.save = json.load(f)
    
    self.mainClass = mclass

    self.initUI()
  
  def initUI(self):
    self.main_widget = QtWidgets.QWidget()
    self.setWindowTitle("Ajouter")

    self.nameEnter = QtWidgets.QLineEdit('Nom', self)
    self.valueEnter = QtWidgets.QTextEdit('Mot de passe', self)
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

    self.setFixedSize(274, 265)

    self.show()

  def initButton(self):
    self.valide.clicked.connect(self.pret)
    self.annule.clicked.connect(self.quitThis)

  def pret(self):
    textName = self.nameEnter.text()
    textMdp = self.valueEnter.toPlainText()    

    if self.save['mdp'] != []:
      for i in range(len(self.save)):
        if self.save['mdp'][i]['name'] == textName:
          return QtWidgets.QMessageBox().information(self, 'Info', 'Ce mot de passe existe deja !')

    final = self.save['mdp']

    final.append({
      'name':textName,
      'value':textMdp
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
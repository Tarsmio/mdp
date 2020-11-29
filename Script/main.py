from PyQt5 import QtWidgets, QtCore, QtGui
import sys
import json
from add import AddWindow
from mod import modWindow
import os

class MainWindows(QtWidgets.QMainWindow):

  def __init__(self, parent=None):
    super(MainWindows, self).__init__(parent)

    if os.path.exists('save.json') != True:
      defaultSAVE = {
        "mdp":[]
      }
      with open('save.json', 'w', encoding='utf-8') as f:
        json.dump(defaultSAVE, f)

    self.initUI()

  def initUI(self):
    self.main_widget = QtWidgets.QWidget()
    self.setWindowTitle('Gestionnaire de mot de passe')

    self.liste = QtWidgets.QListWidget(self)
    self.addButton = QtWidgets.QPushButton('Ajouter', self)
    self.modButton = QtWidgets.QPushButton('Modifier', self)
    self.refreshButton = QtWidgets.QPushButton('Refresh', self)
    self.removeButton = QtWidgets.QPushButton('Remove', self)

    self.mainLayout = QtWidgets.QHBoxLayout()
    self.leftButtonLayout = QtWidgets.QGridLayout()

    self.leftButtonLayout.addWidget(self.addButton, 1, 1)
    self.leftButtonLayout.addWidget(self.modButton, 2, 1)
    self.leftButtonLayout.addWidget(self.refreshButton, 3, 1)
    self.leftButtonLayout.addWidget(self.removeButton, 4, 1)

    self.mainLayout.addLayout(self.leftButtonLayout)
    self.mainLayout.addWidget(self.liste, 4)

    self.main_widget.setLayout(self.mainLayout)

    self.setCentralWidget(self.main_widget)

    self.makeListe()
    self.initButton()

    self.show()

  def initButton(self):
    self.addButton.clicked.connect(self.addClicked)
    self.refreshButton.clicked.connect(self.makeListe)
    self.removeButton.clicked.connect(self.mdpRemove)
    self.modButton.clicked.connect(self.modClicked)

    self.liste.itemDoubleClicked.connect(self.clickedInList)

  def loadSave(self):
    with open("save.json", "r", encoding="utf-8") as f:
      saveJson = json.load(f)

    self.mdp = saveJson["mdp"]

  def makeListe(self):
    self.liste.clear()

    self.loadSave()

    for value in self.mdp:
      item = value['name']
      self.liste.addItem(item)

  def clickedInList(self, item):
    for value in self.mdp:
      if value['name'] == item.text():
        actMdp = value['value']
    QtWidgets.QMessageBox().information(self, "Info", actMdp)

  def addClicked(self):
    AddWindow(self, self)

  def modClicked(self):
    current = self.liste.currentItem()

    if current == None : return QtWidgets.QMessageBox().information(self, "Info", "Rien n'est selectionée")

    modWindow(self, current, self)

  def mdpRemove(self):
    self.loadSave()

    select = self.liste.currentItem()

    print(select)

    if select == None : return QtWidgets.QMessageBox().information(self, "Info", "Rien n'est selectionée")

    for i in range(len(self.mdp)):
      if self.mdp[i]['name'] == select.text():
        toDelet = i

    delete = self.mdp

    delete.pop(toDelet)

    vFinal = {
      "mdp": delete
    }

    with open('save.json', 'w', encoding='utf-8') as n:
      json.dump(vFinal, n)

    self.makeListe()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    ex = MainWindows()
    sys.exit(app.exec_())
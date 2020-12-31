from PyQt5 import QtWidgets, QtCore, QtGui, Qt
import sys
import json
from add import AddWindow
from mod import modWindow
from update import SelfUpdate, checkUpdate
from scale import Scaling
import os
import clipboard
class MainWindows(QtWidgets.QMainWindow):

  def __init__(self, parent=None):
    super(MainWindows, self).__init__(parent)

    if os.path.exists('save.json') != True:
      defaultSAVE = {
        "mdp":[]
      }
      with open('save.json', 'w', encoding='utf-8') as f:
        json.dump(defaultSAVE, f)
    
    self.updateINFO = checkUpdate()
    self.loadType()

    self.initUI()

  def initUI(self):

    with open("style.css", "r") as f:
      css = str(f.read())

    self.main_widget = QtWidgets.QWidget()
    self.setWindowTitle('Gestionnaire de mot de passe')
    self.setWindowIcon(QtGui.QIcon("Image/Icone/cadena.png"))
    self.setStyleSheet(css)

    self.menu = self.menuBar()
    self.fichierMenu = QtWidgets.QMenu("Fichier", self.menu)
    self.fichierMenuUpdate = QtWidgets.QAction(text="Update", parent=self.fichierMenu)

    self.menu.addMenu(self.fichierMenu)
    self.fichierMenu.addAction(self.fichierMenuUpdate)

    self.liste = QtWidgets.QListWidget(self)
    self.addButton = QtWidgets.QPushButton(self)
    self.modButton = QtWidgets.QPushButton('Modifier', self)
    self.refreshButton = QtWidgets.QPushButton(self)
    self.removeButton = QtWidgets.QPushButton('Remove', self)
    self.copyButton = QtWidgets.QPushButton('Copy', self)

    self.addButton.setProperty("cssClass", "upBut")
    self.refreshButton.setProperty("cssClass", "upBut")
    self.modButton.setProperty("cssClass", "mdpBut")
    self.removeButton.setProperty("cssClass", "mdpBut")
    self.copyButton.setProperty("cssClass", "mdpBut")

    self.addButton.setIcon(QtGui.QIcon("Image/add.png"))
    self.refreshButton.setIcon(QtGui.QIcon("Image/re.png"))

    self.addButton.setMaximumSize(32,32)
    self.refreshButton.setMaximumSize(32,32)

    self.deffaultLogo = QtGui.QPixmap('Image/Icone/cadena.png')
    self.deffaultLogo = Scaling().scaleTo64(self.deffaultLogo)
    self.logoMdp = QtWidgets.QLabel()
    self.logoMdp.setPixmap(self.deffaultLogo)
    self.logoMdp.setMinimumSize(QtCore.QSize(80,80))
    self.logoMdp.setAlignment(QtCore.Qt.AlignCenter)
    self.nameInfo = QtWidgets.QLineEdit("Nom", self)
    self.mdpInfo = QtWidgets.QLineEdit("Mdp", self)

    self.logoMdp.setObjectName("logoMDP")

    self.nameInfo.setReadOnly(True)
    self.mdpInfo.setReadOnly(True)

    self.mdpInfo.setMinimumHeight(40)

    self.liste.setFont(QtGui.QFont('Arial', 14))
    self.liste.setMinimumHeight(200)

    self.addButton.setFont(QtGui.QFont('Arial', 12))
    self.addButton.setMinimumSize(QtCore.QSize(20, 0))

    self.mainLayout = QtWidgets.QVBoxLayout()
    self.upLayout = QtWidgets.QHBoxLayout()
    self.downLayout = QtWidgets.QGridLayout()
    self.buttonLayout = QtWidgets.QHBoxLayout()
    self.mdpInfoLayout = QtWidgets.QVBoxLayout()
    self.mdpButtonLayout = QtWidgets.QHBoxLayout()
    self.mdpWidget = QtWidgets.QWidget()

    self.buttonLayout.setAlignment(QtCore.Qt.AlignLeft)

    self.buttonLayout.addWidget(self.addButton, 1)
    self.buttonLayout.addWidget(self.refreshButton, 1)
    self.upLayout.addWidget(self.liste, 4)

    self.downLayout.addWidget(self.logoMdp, 1, 1)
    self.downLayout.addLayout(self.mdpInfoLayout, 1, 2)

    self.mdpButtonLayout.addWidget(self.removeButton, 1)
    self.mdpButtonLayout.addWidget(self.modButton, 1)
    self.mdpButtonLayout.addWidget(self.copyButton, 1)

    self.mdpInfoLayout.addWidget(self.nameInfo, 1)
    self.mdpInfoLayout.addWidget(self.mdpInfo, 2)
    self.mdpInfoLayout.addLayout(self.mdpButtonLayout, 3)

    self.mainLayout.addLayout(self.buttonLayout, 1)
    self.mainLayout.addLayout(self.upLayout, 2)
    self.mainLayout.addWidget(self.mdpWidget, 3)

    self.mdpWidget.setLayout(self.downLayout)
    self.main_widget.setLayout(self.mainLayout)

    self.setCentralWidget(self.main_widget)

    self.makeListe()
    self.initButton()

    self.setFixedSize(380, 395)

    self.show()
    
  def initButton(self):
    self.addButton.clicked.connect(self.addClicked)
    self.refreshButton.clicked.connect(self.makeListe)
    self.removeButton.clicked.connect(self.mdpRemove)
    self.modButton.clicked.connect(self.modClicked)
    self.copyButton.clicked.connect(self.copyClicked)

    self.liste.currentItemChanged.connect(self.clickedInList)

    self.fichierMenuUpdate.triggered.connect(self.updateApp)

  def loadSave(self):
    with open("save.json", "r", encoding="utf-8") as f:
      saveJson = json.load(f)

    self.mdp = saveJson["mdp"]

  def loadType(self):
    with open("type.json", "r", encoding="utf-8") as f:
      typeJson = json.load(f)
    
    self.typeListe = typeJson

  def makeListe(self):
    self.liste.clear()

    self.loadSave()

    for value in self.mdp:
      item = value['name']
      witem = QtWidgets.QListWidgetItem(QtGui.QIcon(self.typeListe[value['type']]['logo']), item)
  
      self.liste.addItem(witem)

    self.clickedInList()

  def resetMdp(self):
    self.logoMdp.setPixmap(self.deffaultLogo)
    self.mdpInfo.setText("Mot de passe")
    self.nameInfo.setText("Nom")

  def clickedInList(self):
    current = self.liste.currentItem()

    if current == None : return self.resetMdp()

    for value in self.mdp:
      if value['name'] == current.text():
        self.actMdp = value

    logo = self.typeListe[self.actMdp['type']]['logo']

    newLogo = Scaling().scaleTo64(QtGui.QPixmap(logo))
    mdp = self.actMdp['value']
    nameMdp = self.actMdp['name']

    self.logoMdp.setPixmap(newLogo)
    self.mdpInfo.setText(mdp)
    self.nameInfo.setText(nameMdp)

  def addClicked(self):
    AddWindow(self, self)

  def modClicked(self):
    current = self.liste.currentItem()

    if current == None : return QtWidgets.QMessageBox().information(self, "Info", "Rien n'est selectionée")

    modWindow(self, current, self)

  def copyClicked(self):
    current = self.liste.currentItem()

    for value in self.mdp:
      if value['name'] == current.text():
        self.actMdp = value

    clipboard.copy(self.actMdp['value'])

  def mdpRemove(self):
    self.loadSave()

    select = self.liste.currentItem()

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

  def updateApp(self):
    SelfUpdate(
      self,
      self.updateINFO['version'],
      self.updateINFO['url'],
      self.updateINFO['actVersion'],
      self.updateINFO['co'],
      self
    )

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    ex = MainWindows()
    sys.exit(app.exec_())
from PyQt5 import QtWidgets, QtCore, QtGui, Qt
import requests as requ
from urllib import request
import zipfile
import os
from shutil import copytree, rmtree

class SelfUpdate(QtWidgets.QMainWindow):

  def __init__(self, mclass, parent=None):
    super(SelfUpdate, self).__init__(parent)

    self.mclass = mclass

    self.iniUI()
    
    if self.verifyUpdate():
      self.askLabel.setText("La version "+self.latestVersion+" est disponible")
      self.changeStatut(2)
    else:
      self.changeStatut(4)

  def iniUI(self):
    self.setWindowTitle("Update")

    self.checkWidget = QtWidgets.QWidget(self)
    self.updateWidget = QtWidgets.QWidget(self)
    self.updateWidget.hide()
    self.askUpdate = QtWidgets.QWidget(self)
    self.askUpdate.hide()
    self.notUpdate = QtWidgets.QWidget(self)
    self.notUpdate.hide()

    self.checkLabel = QtWidgets.QLabel("Recherche de mise a jour ...")
    self.updateLabel = QtWidgets.QLabel("Mise a jour ...")
    self.askLabel = QtWidgets.QLabel("La version [version] est disponible")
    self.notLabel = QtWidgets.QLabel("Le programme est a jour")
    self.askValidButton = QtWidgets.QPushButton(text="Installer")
    self.askDeniedButton = QtWidgets.QPushButton(text="Annuler")

    self.checkLabel.setFont(QtGui.QFont('Arial', 14))
    self.updateLabel.setFont(QtGui.QFont('Arial', 14))
    self.askLabel.setFont(QtGui.QFont('Arial', 14))
    self.notLabel.setFont(QtGui.QFont('Arial', 14))

    self.checkWidgetLayout = QtWidgets.QVBoxLayout()
    self.updateLayout = QtWidgets.QVBoxLayout()
    self.notLayout = QtWidgets.QVBoxLayout()
    self.askMainLayout = QtWidgets.QVBoxLayout()
    self.askButLayout = QtWidgets.QGridLayout()

    self.checkWidgetLayout.setAlignment(QtCore.Qt.AlignCenter)
    self.updateLayout.setAlignment(QtCore.Qt.AlignCenter)
    self.notLayout.setAlignment(QtCore.Qt.AlignCenter)

    self.checkWidgetLayout.addWidget(self.checkLabel)
    self.updateLayout.addWidget(self.updateLabel)
    self.notLayout.addWidget(self.notLabel)
    self.askButLayout.addWidget(self.askValidButton, 1, 1)
    self.askButLayout.addWidget(self.askDeniedButton, 1, 2)
    self.askMainLayout.addWidget(self.askLabel, 1)
    self.askMainLayout.addLayout(self.askButLayout, 2)

    self.checkWidget.setLayout(self.checkWidgetLayout)
    self.updateWidget.setLayout(self.updateLayout)
    self.notUpdate.setLayout(self.notLayout)
    self.askUpdate.setLayout(self.askMainLayout)

    self.setCentralWidget(self.checkWidget)
    self.checkWidget.show()

    self.show()

  def initButton(self):
    self.askValidButton.clicked.connect(self.update)
    self.askDeniedButton.clicked.connect(self.denied)

  def changeStatut(self, etat):
    """Etat 1 : Verification de mise a jour
    Etat 2 : Demande de mise a jour
    Etat 3 : Mise a jour
    Etat 4 : Aucune Mise a jour"""

    self.checkWidget.hide()
    self.askUpdate.hide()
    self.updateWidget.hide()
    self.notUpdate.hide()

    if etat == 1:
      self.setCentralWidget(self.checkWidget)
      self.checkWidget.show()
    elif etat == 2:
      self.setCentralWidget(self.askUpdate)
      self.askUpdate.show()
    elif etat == 3:
      self.setCentralWidget(self.updateWidget)
      self.updateWidget.show()
    elif etat == 4:
      self.setCentralWidget(self.notUpdate)
      self.notUpdate.show()

  def checkUpdate(self):
    with open("version.txt", "r") as f:
      self.actVersion = f.read()
    rep = requ.get("https://api.github.com/repos/Tarsmio/mdp/releases/latest")
    self.latestVersion = rep.json()['tag_name']
    self.latestVersionURL = rep.json()['zipball_url']

  def verifyUpdate(self):
    self.checkUpdate()
    
    if self.latestVersion != self.actVersion:
      return True
    else:
      return False
  
  def update(self):
    print("Updating...")
    self.changeStatut(3)

    request.urlretrieve(self.latestVersionURL, "Script/latest.zip")

    with zipfile.ZipFile("Script/latest.zip", 'r') as zip_ref:
      zip_ref.extractall("latest/")

    pathToCopy = "latest/"+os.listdir("latest/")[0]+"/"

    copytree(pathToCopy, "./", dirs_exist_ok=True)

    os.remove("Script/latest.zip")
    rmtree("latest/")

    self.changeStatut(4)

  def denied(self):
    self.hide()
from PyQt5 import QtWidgets, QtCore, QtGui, Qt
import requests as requ
from urllib import request
import zipfile
import os
from shutil import copytree, rmtree

class SelfUpdate(QtWidgets.QMainWindow):

  def __init__(self, mclass, latest, latestURL, actVer, parent=None):
    super(SelfUpdate, self).__init__(parent)

    self.mclass = mclass
    self.latestVersion = latest
    self.latestURL = latestURL
    self.actVersion = actVer

    self.iniUI()
    self.starting()

  def iniUI(self):
    self.setWindowTitle("Update")
    self.mainWidget = QtWidgets.QWidget(self)

    self.upLabel = QtWidgets.QLabel("Recherche de mise a jour ...")
    self.askValidButton = QtWidgets.QPushButton(text="Installer")
    self.askDeniedButton = QtWidgets.QPushButton(text="Annuler")

    self.upLabel.setFont(QtGui.QFont('Arial', 14))

    self.mainLayout = QtWidgets.QVBoxLayout()
    self.butLayout = QtWidgets.QGridLayout()

    self.butLayout.addWidget(self.askValidButton, 1, 1)
    self.butLayout.addWidget(self.askDeniedButton, 1, 2)
    self.mainLayout.addWidget(self.upLabel)
    self.mainLayout.addLayout(self.butLayout)

    self.mainWidget.setLayout(self.mainLayout)

    self.setCentralWidget(self.mainWidget)

    self.initButton()

  def initButton(self):
    self.askValidButton.clicked.connect(self.selfUpdating)
    self.askDeniedButton.clicked.connect(self.denied)

  def starting(self):
    isUpdate = self.verifyUpdate()
    if isUpdate :
      self.upLabel.setText("La version "+self.latestVersion+" est disponible")
      self.askValidButton.setEnabled(True)
      self.askDeniedButton.setEnabled(True)
      self.show()
    else:
      self.upLabel.setText("Aucune mise a jour disponible")
      self.askValidButton.setEnabled(False)
      self.askDeniedButton.setEnabled(True)
      self.show()

  def verifyUpdate(self):
    if self.latestVersion != self.actVersion:
      return True
    else:
      return False
  
  def selfUpdating(self):
    print("Updating...")

    request.urlretrieve(self.latestVersionURL, "Script/latest.zip")

    with zipfile.ZipFile("Script/latest.zip", 'r') as zip_ref:
      zip_ref.extractall("latest/")

    pathToCopy = "latest/"+os.listdir("latest/")[0]+"/"

    copytree(pathToCopy, "./", dirs_exist_ok=True)

    os.remove("Script/latest.zip")
    rmtree("latest/")

    self.upLabel.setText("Vous etes a jour")
    self.askDeniedButton.setText("Quitter")
    self.askValidButton.setEnabled(False)
    self.askDeniedButton.setEnabled(True)

  def denied(self):
    self.hide()

def checkUpdate():
    with open("version.txt", "r") as f:
      actVersion = f.read()
    rep = requ.get("https://api.github.com/repos/Tarsmio/mdp/releases/latest")
    return {
      "version": rep.json()['tag_name'],
      "url": rep.json()['zipball_url'],
      "actVersion": actVersion
    }
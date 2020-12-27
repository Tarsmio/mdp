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

  def iniUI(self):
    self.setWindowTitle("Update")

    self.checkWidget = QtWidgets.QWidget(self)
    self.checkWidget.hide()
    self.updateWidget = QtWidgets.QWidget(self)
    self.updateWidget.hide()
    self.askUpdate = QtWidgets.QWidget(self)
    self.askUpdate.hide()

    self.checkLabel = QtWidgets.QLabel("Recherche de mise a jour ...")
    self.askLabel = QtWidgets.QLabel("La version [version] est disponible")
    self.askValidButton = QtWidgets.QPushButton(text="Installer")
    self.askDeniedButton = QtWidgets.QPushButton(text="Annuler")

    self.checkLabel.setFont(QtGui.QFont('Arial', 14))
    self.askLabel.setFont(QtGui.QFont('Arial', 14))

    self.checkWidgetLayout = QtWidgets.QVBoxLayout()
    self.askMainLayout = QtWidgets.QVBoxLayout()
    self.askButLayout = QtWidgets.QGridLayout()

    self.checkWidgetLayout.setAlignment(QtCore.Qt.AlignCenter)

    self.checkWidgetLayout.addWidget(self.checkLabel)

    self.checkWidget.setLayout(self.checkWidgetLayout)

    self.show()

  def checkUpdate(self):
    self.setCentralWidget(self.checkWidget)
    self.checkWidget.show()

    with open("../version.txt", "r") as f:
      self.actVersion = f.read()
    rep = requ.get("https://api.github.com/repos/Tarsmio/mdp/releases/latest")
    self.latestVersion = rep.json()['tag_name']
    self.latestVersionURL = rep.json()['zipball_url']

  def verifyUpdate(self):
    
    if self.latestVersion != self.actVersion:
      return True
    else:
      return False
  
  def update(self):
    print("Updating...")

    request.urlretrieve(self.latestVersionURL, "latest.zip")

    with zipfile.ZipFile("latest.zip", 'r') as zip_ref:
      zip_ref.extractall("latest/")

    pathToCopy = "latest/"+os.listdir("latest/")[0]+"/"

    copytree(pathToCopy, "../", dirs_exist_ok=True)

    os.remove("latest.zip")
    rmtree("latest/")
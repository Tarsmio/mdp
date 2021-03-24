from PyQt5 import QtWidgets, QtCore, QtGui
from pgenerator import passwordGenerator
from add import AddWindow

class genWindow(QtWidgets.QMainWindow):

  def __init__(self, mclass, ver, parent=None):
    super(genWindow, self).__init__(parent)

    self.mainClass = mclass
    self.ver = ver

    self.isDone = False
    self.password = ""

    self.initUI()

  def initUI(self):
    self.main_Widget = QtWidgets.QWidget()
    self.setWindowTitle(self.mainClass.langueTexte["title"]["5"])

    self.passwordWiew = QtWidgets.QTextEdit()

    self.labelTaille = QtWidgets.QLabel(self.mainClass.langueTexte["label"]["7"], self)
    self.radMinuscule = QtWidgets.QCheckBox(self.mainClass.langueTexte["checkBox"]["2"], self)
    self.radMajuscule = QtWidgets.QCheckBox(self.mainClass.langueTexte["checkBox"]["3"], self)
    self.radNumber = QtWidgets.QCheckBox(self.mainClass.langueTexte["checkBox"]["4"], self)
    self.radSp = QtWidgets.QCheckBox(self.mainClass.langueTexte["checkBox"]["5"], self)

    self.radMinuscule.setProperty('radType', 1)
    self.radMajuscule.setProperty('radType', 2)
    self.radNumber.setProperty('radType', 3)
    self.radSp.setProperty('radType', 4)

    self.spinTaille = QtWidgets.QSpinBox(self)
    self.spinMinuscule = QtWidgets.QSpinBox(self)
    self.spinMajuscule = QtWidgets.QSpinBox(self)
    self.spinNumber = QtWidgets.QSpinBox(self)
    self.spinSp = QtWidgets.QSpinBox(self)

    self.butGener = QtWidgets.QPushButton(self.mainClass.langueTexte["button"]["12"], self)
    self.butAdd = QtWidgets.QPushButton(self.mainClass.langueTexte["button"]["13"], self)
    self.butValider = QtWidgets.QPushButton(self.mainClass.langueTexte["button"]["14"], self)

    self.passwordWiew.setReadOnly(True)

    self.main_Layout = QtWidgets.QVBoxLayout()
    self.parameterLayout = QtWidgets.QVBoxLayout()
    self.buttonLayout = QtWidgets.QVBoxLayout()

    self.parameterTailleLayout = QtWidgets.QHBoxLayout()
    self.parameterMinusculeLayout = QtWidgets.QHBoxLayout()
    self.parameterMajusculeLayout = QtWidgets.QHBoxLayout()
    self.parameterNumberLayout = QtWidgets.QHBoxLayout()
    self.parameterSpLayout = QtWidgets.QHBoxLayout()

    self.parameterTailleLayout.addWidget(self.labelTaille)
    self.parameterTailleLayout.addWidget(self.spinTaille)

    self.parameterMinusculeLayout.addWidget(self.radMinuscule)
    self.parameterMinusculeLayout.addWidget(self.spinMinuscule)

    self.parameterMajusculeLayout.addWidget(self.radMajuscule)
    self.parameterMajusculeLayout.addWidget(self.spinMajuscule)

    self.parameterNumberLayout.addWidget(self.radNumber)
    self.parameterNumberLayout.addWidget(self.spinNumber)

    self.parameterSpLayout.addWidget(self.radSp)
    self.parameterSpLayout.addWidget(self.spinSp)

    self.parameterLayout.addLayout(self.parameterTailleLayout)
    self.parameterLayout.addLayout(self.parameterMinusculeLayout)
    self.parameterLayout.addLayout(self.parameterMajusculeLayout)
    self.parameterLayout.addLayout(self.parameterNumberLayout)
    self.parameterLayout.addLayout(self.parameterSpLayout)

    self.buttonLayout.addWidget(self.butGener)
    self.buttonLayout.addWidget(self.butAdd)
    self.buttonLayout.addWidget(self.butValider)

    self.main_Layout.addWidget(self.passwordWiew)
    self.main_Layout.addLayout(self.parameterLayout)
    self.main_Layout.addLayout(self.buttonLayout)

    self.main_Widget.setLayout(self.main_Layout)

    self.setCentralWidget(self.main_Widget)

    self.initButton()
    self.initRad()
    self.initSpin()

    self.show()

  def initButton(self):
    self.butGener.clicked.connect(self.gen)
    self.butAdd.clicked.connect(self.addButton)

    if self.ver == 1 :
      self.butGener.setVisible(True)
      self.butAdd.setVisible(True)
      self.butValider.setVisible(False)
    elif self.ver == 2 :
      self.butGener.setVisible(True)
      self.butAdd.setVisible(False)
      self.butValider.setVisible(True)

    self.setButtonDone()

  def initRad(self):
    self.radMinuscule.setChecked(True)
    self.radMajuscule.setChecked(True)
    self.radNumber.setChecked(True)
    self.radSp.setChecked(True)

    self.radMinuscule.toggled.connect(self.onCheck)
    self.radMajuscule.toggled.connect(self.onCheck)
    self.radNumber.toggled.connect(self.onCheck)
    self.radSp.toggled.connect(self.onCheck)

  def initSpin(self):
    self.spinTaille.setMaximum(64)
    self.spinTaille.setMinimum(1)
    self.spinTaille.setValue(16)

    self.spinMinuscule.setMaximum(64)
    self.spinMinuscule.setMinimum(1)
    self.spinMinuscule.setValue(5)

    self.spinMajuscule.setMaximum(64)
    self.spinMajuscule.setMinimum(1)
    self.spinMajuscule.setValue(5)

    self.spinNumber.setMaximum(64)
    self.spinNumber.setMinimum(1)
    self.spinNumber.setValue(5)

    self.spinSp.setMaximum(64)
    self.spinSp.setMinimum(1)
    self.spinSp.setValue(1)

  def setButtonDone(self):
    if self.ver == 1:
      if self.isDone :
        self.butAdd.setEnabled(True)
      else:
        self.butAdd.setEnabled(False)
    elif self.ver == 2:
      if self.isDone :
        self.butValider.setEnabled(True)
      else:
        self.butValider.setEnabled(False)

  def onCheck(self):
    selected = self.sender()
    typeRad = selected.property('radType')

    if not selected.isChecked():
      if typeRad == 1:
        self.spinMinuscule.hide()
      elif typeRad == 2:
        self.spinMajuscule.hide()
      elif typeRad == 3:
        self.spinNumber.hide()
      elif typeRad == 4:
        self.spinSp.hide()
    else:
      if typeRad == 1:
        self.spinMinuscule.show()
      elif typeRad == 2:
        self.spinMajuscule.show()
      elif typeRad == 3:
        self.spinNumber.show()
      elif typeRad == 4:
        self.spinSp.show()

  def addButton(self):
    option = {
      "password": self.password
    }

    AddWindow(self.mainClass, self.mainClass, option)
    self.close()

  def gen(self):
    allParameter = 0

    if self.radMinuscule.isChecked() :
      allParameter += self.spinMinuscule.value()
      minuscule = self.spinMinuscule.value()
    else:
      minuscule = False

    if self.radMajuscule.isChecked() :
      allParameter += self.spinMajuscule.value()
      majuscule = self.spinMajuscule.value()
    else:
      majuscule = False

    if self.radNumber.isChecked() :
      allParameter += self.spinNumber.value()
      number = self.spinNumber.value()
    else:
      number = False

    if self.radSp.isChecked() :
      allParameter += self.spinSp.value()
      sp = self.spinSp.value()
    else :
      sp = False

    if not allParameter == self.spinTaille.value():
      self.passwordWiew.setText(self.mainClass.langueTexte["editLine"]["5"])
    elif allParameter == self.spinTaille.value():
      config = {
        "taille" : self.spinTaille.value(),
        "minCount" : minuscule,
        "majCount" : majuscule,
        "numberCount" : number,
        "spCount" : sp
      }

      password = passwordGenerator(config)

      self.passwordWiew.setText(password)
      self.password = password

      self.isDone = True
      self.setButtonDone()
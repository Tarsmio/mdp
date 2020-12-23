from PyQt5 import QtGui, QtCore

class Scaling():
  
  def scaleTo(self, src, height, width):
    rescale = src

    f_rescale = rescale.scaled(QtCore.QSize(width,height), QtCore.Qt.KeepAspectRatio, QtCore.Qt.FastTransformation)

    return f_rescale

  def scaleTo64(self, src):
    rescale = src

    f_rescale = rescale.scaled(QtCore.QSize(64,64), QtCore.Qt.KeepAspectRatio, QtCore.Qt.FastTransformation)

    return f_rescale

  def scaleTo32(self, src):
    rescale = src

    f_rescale = rescale.scaled(QtCore.QSize(32,32), QtCore.Qt.KeepAspectRatio, QtCore.Qt.FastTransformation)

    return f_rescale
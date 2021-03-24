import random
import secrets
from strHelp import listToString

defaultConfig = {
  "taille" : 16,
  "minCount" : 5,
  "majCount" : 5,
  "numberCount" : 5,
  "spCount" : 1
}

defaultMajuscule = [
  'A',
  'B',
  'C',
  'D',
  'E',
  'F',
  'G',
  'H',
  'I',
  'J',
  'K',
  'L',
  'M',
  'N',
  'O',
  'P',
  'Q',
  'R',
  'S',
  'T',
  'U',
  'V',
  'W',
  'X',
  'Y',
  'Z'
]

defaultMinuscule = [
  'a',
  'b',
  'c',
  'd',
  'e',
  'f',
  'g',
  'h',
  'i',
  'j',
  'k',
  'l',
  'm',
  'n',
  'o',
  'p',
  'q',
  'r',
  's',
  't',
  'u',
  'v',
  'w',
  'x',
  'y',
  'z'
]

defaultNumber = [
  "0",
  "1",
  "2",
  "3",
  "4",
  "5",
  "6",
  "7",
  "8",
  "9"
]

defaultSp = [
  "!",
  "\"",
  "#",
  "$",
  "%",
  "&",
  "\'",
  "(",
  ")",
  "*",
  "+",
  "-",
  ".",
  "/",
  "<",
  "=",
  ">",
  "?",
  "@",
  "^",
  "_",
  "~"
]

def passwordGenerator(config=defaultConfig):
  taille = config['taille']
  minCount = config['minCount']
  majCount = config['majCount']
  numberCount = config['numberCount']
  spCount = config['spCount']

  choixListe = []

  finalMDP = []

  if minCount :
    for i in range(minCount):
      a = secrets.choice(defaultMinuscule)
      choixListe.append(a)

  if majCount :
    for i in range(majCount):
      a = secrets.choice(defaultMajuscule)
      choixListe.append(a)

  if numberCount :
    for i in range(numberCount):
      a = secrets.choice(defaultNumber)
      choixListe.append(a)

  if spCount :
    for i in range(spCount):
      a = secrets.choice(defaultSp)
      choixListe.append(a)

  repeat = taille

  while repeat > 0:
    choix = secrets.choice(choixListe)
    finalMDP.append(choix)
    choixListe.remove(choix)
    repeat -= 1

  return listToString(finalMDP)

if __name__ == "__main__" :
  print(passwordGenerator())
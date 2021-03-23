def strToList(string, separator):
    """Fonction permetant de transformer un string en list"""
    aString = ""
    sep = str(separator)
    finalSTR = []

    for i in string :
        if i != sep :
            aString += i
        else :
            finalSTR.append(aString)
            aString = ""
    
    finalSTR.append(aString)
    return finalSTR

def listToString(list, space=False):
    """Fonction permetant de transformer une liste en string"""
    if space == True :
        str1 = " "
    else :
        str1 = ""
        
    return str1.join(list)

#Test du module
if __name__ == "__main__" :
    print(strToList("Ceci est un test", " "))
    print(listToString(["Je","test","ce","module"], True))
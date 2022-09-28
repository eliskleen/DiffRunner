from pygameInterface import Form
import os
from tkinter import filedialog 
import tkinter as tk

# diffList = open("knownDiffs.txt", "r", encoding="ISO 8859-1").readlines()
def bothInDiffList(c1, c2, diffList):
    for c in diffList:
        c = c.lower()
        if (c1 in c) and (c2 in c):
            return True
    return False

def compInList(comp, list):
    comp = comp.lower()
    diffList = open("knownDiffs.txt", "r", encoding="UTF-8").readlines()
    for l in list:
        l = l.lower()
        # if (comp. in l) or (l.lower() in comp.lower()) or (bothInDiffList(comp, l, diffList)):
        if(comp in l) or (l in comp) or (bothInDiffList(comp, l, diffList)):
            return True
    return False


def getDiff(limeFileName, regiFileName, doPrint):

    limeComp = []
    for status in open("statusInLime.txt", "r", encoding="ISO 8859-1").read().split(","):
        limeComp += getCompWithStatusLime(str(status), limeFileName)
    print(len(limeComp))
    # print(limeComp)
    regiComp = []
    regiComp += getCompWithStatusRegi("Submitted (not yet accepted)", regiFileName)
    print(len(regiComp))
    print(regiComp)

    resList = ["Företag i lime men inte i anmälningssystemet: \n"]
    for comp in limeComp:
        if (not compInList(comp, regiComp)):
            if doPrint:
                print("Företag i lime men inte i anmälningssystemet: " + comp)
            resList.append("    " + comp + "\n")

    resList.append("Företag i anmälningssystemet men inte i lime: \n")
    for comp in regiComp:
        if (not compInList(comp, limeComp)):
            if doPrint:
                print("Företag i anmälningssystemet men inte i lime: " + comp)
            resList.append("    " + comp + "\n")
    return (resList, len(regiComp))


def writeResFile(resList):
    f = open("result.txt", "w", encoding="UTF-8")
    f.writelines(resList)


def getCompWithStatusLime(status, filename):
    comp = getFieldOnMatchFromFile(
        "status_label", "customer_name", status, filename, enc="ISO 8859-1")
    return comp


def getCompWithStatusRegi(status, filename):
    comp = getFieldOnMatchFromFile(
        "Application status", "Applicant", status, filename)
    print(type(comp[0]))
    print(comp[0])
    return comp


def getFieldOnMatchFromFile(matchField, field, matchValue, filename, enc="UTF-8"):
    lines = []
    for l in open(filename, encoding=enc).readlines():
        # lines.append(l.replace("�", "å").replace("\"", "").replace("Ã¶", "ö").replace("Ã¥", "å").replace("Ã¤", "ä"))
        lines.append(str(l.replace("\"", "").encode("utf-8")).
                            replace("\\xc3\\xb6", "ö").
                            replace("\\xc3\\xa5", "å").
                            replace("\\xc3\\xa4", "ä"))
    comp = []
    split = ";" if ";" in lines[0] else ","
    headers = lines[0].split(split)
    fieldIndex = headers.index(field)
    val = filter(lambda h : matchField in h, headers)
    matchIndex = headers.index(list(val)[0])
    # matchIndex = headers.find(lambda h : matchField in h)
    
    for line in lines[1:]:
        if (matchValue in line.split(split)[matchIndex] or line.split(split)[matchIndex] in matchValue):
            comp.append(line.split(split)[fieldIndex])

    return comp


def openFileDialog(prompt):
    file = filedialog.askopenfile(initialdir=os.getcwd,
                                  title=prompt,
                                  filetypes= [("All Files", "*.*")])
    if file is not None:
        return file.name
    return None

def runDiff():
    limeFileName = openFileDialog("Välj Lime utdraget")
    if limeFileName is None:
        return
    regiFileName = openFileDialog("Välj utraget från anmälningssystemet")
    if regiFileName is None:
        return
    (resList, amontSubmitted) = getDiff(limeFileName, regiFileName, False)
    if(len(resList) == 2):
        print("Inga skillnader hittades")
        resList = ["Inga skillnader hittades!! \n" + str(amontSubmitted) + " företag har anmält sig" + "\nBara " + str(160 - amontSubmitted) + " platser kvar!!"]
    writeResFile(resList)   

def updateKnownDiffs():
    f = open("knownDiffs.txt", "a", encoding="UTF-8")
    


if __name__ == "__main__":
    root = tk.Tk()
    # print("HEHEHE")
    
    # exit()
    form = Form(runDiff)
    root.destroy()
    form.load()

    # limeFileName = openFileDialog("Välj Lime utdraget")
    # regiFileName = openFileDialog("Välj utraget från anmälningssystemet")
    # resList = getDiff(limeFileName, regiFileName, False)
    # writeResFile(resList)

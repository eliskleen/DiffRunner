from pygameInterface import Form
import os
from tkinter import filedialog 

# diffList = open("knownDiffs.txt", "r", encoding="UTF-8").readlines()
def bothInDiffList(c1, c2, diffList):
    for c in diffList:
        if (c1 in c) and (c2 in c):
            return True
    return False

def compInList(comp, list):
    diffList = open("knownDiffs.txt", "r", encoding="UTF-8").readlines()
    for l in list:
        if (comp.lower() in l.lower()) or (l.lower() in comp.lower()) or (bothInDiffList(comp, l, diffList)):
            return True
    return False


def getDiff(limeFileName, regiFileName, doPrint):

    limeComp = []
    for status in open("statusInLime.txt", "r", encoding="UTF-8").read().split(","):
        limeComp += getCompWithStatusLime(str(status), limeFileName)
    print(len(limeComp))
    regiComp = []
    regiComp += getCompWithStatusRegi("Submitted (not yet accepted)", regiFileName)

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
    return resList


def writeResFile(resList):
    f = open("result.txt", "w", encoding="UTF-8")
    f.writelines(resList)


def getCompWithStatusLime(status, filename):
    comp = getFieldOnMatchFromFile(
        "status_label", "customer_name", status, filename)
    return comp


def getCompWithStatusRegi(status, filename):
    comp = getFieldOnMatchFromFile(
        "Application statusNewSaved (not submitted yet)Submitted (not yet accepted)", "Applicant", status, filename)
    print(type(comp[0]))
    print(comp[0])
    return comp


def getFieldOnMatchFromFile(matchField, field, matchValue, filename):
    lines = []
    for l in open(filename).readlines():
        lines.append(l.replace("�", "å").replace("\"", "").replace("Ã¶", "ö").replace("Ã¥", "å").replace("Ã¤", "ä"))
    comp = []
    split = ";" if ";" in lines[0] else ","
    headers = lines[0].split(split)
    fieldIndex = headers.index(field)
    matchIndex = headers.index(matchField)
    for line in lines[1:]:
        if (matchValue in line.split(split)[matchIndex] or line.split(split)[matchIndex] in matchValue):
            comp.append(line.split(split)[fieldIndex])

    return comp


def openFileDialog(prompt):
    file = filedialog.askopenfile(initialdir=os.getcwd,
                                  title=prompt,
                                  filetypes=(("Csv files",
                                              "*.csv*"),
                                             ("all files",
                                              "*.*")))
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
    resList = getDiff(limeFileName, regiFileName, False)
    writeResFile(resList)   

def updateKnownDiffs():
    f = open("knownDiffs.txt", "a", encoding="UTF-8")
    

if __name__ == "__main__":

    form = Form(runDiff)
    form.load()

    # limeFileName = openFileDialog("Välj Lime utdraget")
    # regiFileName = openFileDialog("Välj utraget från anmälningssystemet")
    # resList = getDiff(limeFileName, regiFileName, False)
    # writeResFile(resList)

import re
import xml.etree.ElementTree as ET
from pyluach.dates import HebrewDate, GregorianDate

idDate = 0
hebToGreg = {}
gregToHeb = {}
datesWithId = {}


def HebrewFormat():
    # search for Hebrew dates
    months = "(בתשרי|בחשון|בכסלו|בטבת|בשבט|באדר|בניסן|באייר|בסיון|בתמוז|באב|באלול)"
    days1 = "[אבגדהוזחטיכל]" + "\'"
    x1 = "י"
    x2 = "כ"
    x3 = "ל"
    days2 = x1 + "\"" + "[אבגדזחט]"
    days3 = x2 + "\"" + "[אבגדהוזחט]"
    days4 = x3 + "\"" + "[אבגדהוזחט]"
    days5 = "ט" + "\"" + "[וז]"
    days = "(" + days1 + "|" + days2 + "|" + days3 + "|" + days4 + "|" + days5 + ")"
    year = "([\u0590-\u05fe]+" + "\"" + "[\u0590-\u05fe])"
    HebrewDates = "(?:" + days + " " + months + " " + year + ")"
    return HebrewDates


def GregorianFormat():
    # search for gregorian dates
    months2 = "(בינואר|בפברואר|במרץ|באפריל|במאי|ביוני|ביולי|באוגוסט|בספטמבר|באוקטובר|בנובמבר|בדצמבר)"
    date_reg2 = "(?:" + "(3[01]|[12][0-9]|0?[1-9])" + " " + months2 + ",? " + "([0-9]{4})" + ")"
    return date_reg2


def dates(txt):
    if txt is not None:
        HebrewDates = HebrewFormat()
        y = re.findall(HebrewDates, txt)
        date_reg2 = GregorianFormat()
        z = re.findall(date_reg2, txt)

        hebrewDatesArr = changeHebrewDate(y)
        gregDatesArr = changeGregDates(z)

        for date in hebrewDatesArr:
            Id = increaseId()
            heb = HebrewDate(date[2], date[1], date[0])
            datesWithId[str(heb)] = Id
            gregFormat = heb.to_greg()
            hebToGreg[gregFormat] = Id

        for date1 in gregDatesArr:
            Id = increaseId()
            greg = GregorianDate(date1[2], date1[1], date1[0])
            datesWithId[str(greg)] = Id
            hebFormat = greg.to_heb()
            gregToHeb[hebFormat] = Id


def dateAsString(date):
    if date[0] > 10:
        if date[1] > 10:
            return str(date[0]) + "-" + str(date[1]) + "-" + str(date[2])
        else:
            return str(date[0]) + "-0" + str(date[1]) + "-" + str(date[2])
    else:
        if date[1] > 10:
            return "0" + str(date[0]) + "-" + str(date[1]) + "-" + str(date[2])
        else:
            return "0" + str(date[0]) + "-0" + str(date[1]) + "-" + str(date[2])


def addTagsText(node, txt):
    if node.tag == "date":
        return

    if txt is not None:
        HebrewDates = HebrewFormat()
        date_reg2 = GregorianFormat()
        allFormats = "(?:" + HebrewDates + "|" + date_reg2 + ")"
        datesArr = re.findall(allFormats, txt)
        if datesArr:
            date = removeBlankCells(datesArr[0])
            node.text = txt[0: txt.index(" ".join(date))]
            i = 0
            for date in datesArr:
                date = removeBlankCells(date)
                a = " ".join(date)
                if len(re.findall(HebrewDates, a)) > 0:
                    numFormat = changeHebrewDate([date])
                    numFormat = numFormat[0]
                    numFormat = HebrewDate(numFormat[2], numFormat[1], numFormat[0])
                    Id = datesWithId.get(str(numFormat))
                    alterDate = gregToHeb.get(numFormat, None)
                else:
                    numFormat = changeGregDates([date])
                    numFormat = numFormat[0]
                    numFormat = GregorianDate(numFormat[2], numFormat[1], numFormat[0])
                    Id = datesWithId.get(str(numFormat))
                    alterDate = hebToGreg.get(numFormat, None)
                if alterDate is None:
                    newTag = ET.Element('date', attrib={'date': numFormat, 'Id': Id})
                else:
                    newTag = ET.Element('date', attrib={'date': numFormat, 'Id': Id, 'alternativeDateId': alterDate})
                newTag.text = " ".join(date)
                txt = txt[txt.index(" ".join(date)) + len(" ".join(date)):]
                newTag.tail = txt
                node.insert(i, newTag)


def addTagsTail(node, txt):
    if node.tag == "date":
        return

    if txt is not None:
        HebrewDates = HebrewFormat()
        date_reg2 = GregorianFormat()
        allFormats = "(?:" + HebrewDates + "|" + date_reg2 + ")"
        datesArr = re.findall(allFormats, txt)
        if datesArr:
            date = removeBlankCells(datesArr[0])
            node.tail = txt[0: txt.index(" ".join(date))]
            i = 0
            for date in datesArr:
                date = removeBlankCells(date)
                a = " ".join(date)
                if len(re.findall(HebrewDates, a)) > 0:
                    numFormat = changeHebrewDate([date])
                    numFormat = numFormat[0]
                    numFormat = HebrewDate(numFormat[2], numFormat[1], numFormat[0])
                    Id = datesWithId.get(str(numFormat))
                    alterDate = gregToHeb.get(numFormat, None)
                else:
                    numFormat = changeGregDates([date])
                    numFormat = numFormat[0]
                    numFormat = GregorianDate(numFormat[2], numFormat[1], numFormat[0])
                    Id = datesWithId.get(str(numFormat))
                    alterDate = hebToGreg.get(numFormat, None)
                if alterDate is None:
                    newTag = ET.Element('date', attrib={'date': numFormat, 'Id': Id})
                else:
                    newTag = ET.Element('date', attrib={'date': numFormat, 'Id': Id, 'alternativeDateId': alterDate})
                newTag.text = " ".join(date)
                txt = txt[txt.index(" ".join(date)) + len(" ".join(date)):]
                if i < len(datesArr)-1:
                    newTag.tail = txt[0: txt.index(" ".join(datesArr[i+1]))]
                else:
                    newTag.tail = txt
                node.append(newTag)


def removeBlankCells(date):
    HebrewDates = HebrewFormat()
    a = " ".join(date)
    if len(re.findall(HebrewDates, a)) > 0:
        clean = [date[0], date[1], date[2]]
    else:
        clean = [date[3], date[4], date[5]]
    return clean


def increaseId():
    global idDate
    idDate = idDate + 1
    return str(idDate)


def changeGregDates(arr):
    output = []
    i = 0
    for date in arr:
        newDate = [int(date[0])]

        if date[1] == "בינואר":
            newDate.append(1)
        if date[1] == "בפברואר":
            newDate.append(2)
        if date[1] == "במרץ":
            newDate.append(3)
        if date[1] == "באפריל":
            newDate.append(4)
        if date[1] == "במאי":
            newDate.append(5)
        if date[1] == "ביוני":
            newDate.append(6)
        if date[1] == "ביולי":
            newDate.append(7)
        if date[1] == "באוגוסט":
            newDate.append(8)
        if date[1] == "בספטמבר":
            newDate.append(9)
        if date[1] == "באוקטובר":
            newDate.append(10)
        if date[1] == "בנובמבר":
            newDate.append(11)
        if date[1] == "בדצמבר":
            newDate.append(12)

        newDate.append(int(date[2]))
        output.append(newDate)
        i = i + 1

    return output


def changeHebrewDate(arr):
    output = []
    i = 0
    for date in arr:
        newDate = []

        # handle day
        day = date[0]
        dayInNumber = 0
        if day.find('"') == -1:
            dayInNumber += hebrewLettersValue.get(day[0])
        else:
            day = day.replace('"', '')
            for i in range(len(day)):
                dayInNumber += hebrewLettersValue.get(day[i - 1])
        newDate.append(dayInNumber)

        # handle month
        if date[1] == "בניסן":
            newDate.append(1)
        if date[1] == "באייר":
            newDate.append(2)
        if date[1] == "בסיון":
            newDate.append(3)
        if date[1] == "בתמוז":
            newDate.append(4)
        if date[1] == "באב":
            newDate.append(5)
        if date[1] == "באלול":
            newDate.append(6)
        if date[1] == "בתשרי":
            newDate.append(7)
        if date[1] == "בחשון":
            newDate.append(8)
        if date[1] == "בכסלו":
            newDate.append(9)
        if date[1] == "בטבת":
            newDate.append(10)
        if date[1] == "בשבט":
            newDate.append(11)
        if date[1] == "באדר":
            newDate.append(12)

        # handle year
        year = date[2]
        year = year.replace('"', '')
        yearInNumber = 5000
        for i in range(len(year)-1):
            yearInNumber += hebrewLettersValue.get(year[i+1])
        newDate.append(yearInNumber)

        output.append(newDate)
        i = i + 1
    return output


hebrewLettersValue = {'א': 1, 'ב': 2, 'ג': 3, 'ד': 4, 'ה': 5, 'ו': 6, 'ז': 7, 'ח': 8, 'ט': 9, 'י': 10, 'כ': 20, 'ל': 30,
                      'מ': 40, 'נ': 50, 'ס': 60, 'ע': 70, 'פ': 80, 'צ': 90, 'ק': 100, 'ר': 200, 'ש': 300, 'ת': 400}


def main():
    file = input("Insert Path: \n")
    tree = ET.parse(file)  # saves the XML file -> tree
    root = tree.getroot()

    dates(root.text)
    dates(root.tail)

    for child in root.iter():
        dates(child.text)
        dates(child.tail)

    addTagsText(root, root.text)
    addTagsTail(root, root.tail)

    for child in root.iter():
        addTagsText(child, child.text)
        addTagsTail(child, child.tail)

    tree.write('withDates.xml', 'utf-8')


if __name__ == '__main__':
    main()

# This is a sample Python script.
import requests
from lxml import html


# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.

class Apartment:

    def __init__(self, from_file, values):
        if from_file:
            self.bed = int(values[0])
            self.bath = float(values[2])
            self.price = float(values[5].replace("$", ""))
            self.sqft = int(values[6])
            self.floor = int(values[9])
            self.available = values[12]
        else:
            self.price = int(values[0].replace(",", "").replace("$", ""))
            self.bed = int(values[3])
            self.bath = float(values[6])
            self.sqft = int(values[8])
            self.floor = int(values[12])
            self.available = values[14]

    def __str__(self):
        return "\t" + str(self.bed) + " bed " + str(self.bath) + " bath for $" + str(self.price) + " " + str(
            self.sqft) + " sqft on " + str(self.floor) + " floor, available " + self.available

    def __eq__(self, other):
        if self.bath != other.bath:
            return False
        if self.bed != other.bed:
            return False
        if self.price != other.price:
            return False
        if self.floor != other.floor:
            return False
        if self.sqft != other.sqft:
            return False
        if self.available != other.available:
            return False
        return True


def make_request(url):
    r = requests.get(url)
    return r


def available_list(url):
    response = make_request(url)
    tree = html.fromstring(response.content)
    classes = tree.find_class('col-xs-4 specs')
    list = []
    for item in classes:
        toAdd = Apartment(False, item.text_content().split())
        if toAdd.bed > 0 and toAdd.price < 4000:
            list.append(toAdd)
    return list


def writeToFile(apts, file, complex):
    f = open(file, "w")
    f.write(complex + " Apartments:\n")
    for apt in apts:
        f.write(str(apt) + "\n")
    f.close()


def readFromFile(file):
    f = open(file, "r")
    next(f)
    lines = f.readlines()
    list = []
    for line in lines:
        list.append(Apartment(True, line.split()))
    f.close()
    return list


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    avenirApts = available_list(
        'https://www.equityapartments.com/boston/north-end/avenir-apartments?mkwid=_dc&pcrid=&pkw=&pmt=&utm_source=google&utm_medium=cpc&utm_term=&utm_campaign=&utm_group=&gclsrc=aw.ds&&utm_source=google&utm_medium=cpc&utm_campaign=Avenir_Pmax&gad_source=1&gclid=Cj0KCQjwudexBhDKARIsAI-GWYVr_J6V1U4InujmNOjH3nn3nONK8sJ_oOaLXVVrkmsYZ2S5gXxDWRUaAhPeEALw_wcB#%23unit-availability-tile')
    longfellowApts = available_list(
        'https://www.equityapartments.com/boston/west-end/the-towers-at-longfellow-apartments##unit-availability-tile')

    avenirSeen = readFromFile('avenirApts.txt')
    longfellowSeen = readFromFile('longfellow.txt')

    print("New Avenir Apartments:")
    for apt in avenirApts:
        if apt not in avenirSeen:
            print(apt)
    print("\nNew Longfellow Apartments:")
    for apt in longfellowApts:
        if apt not in longfellowSeen:
            print(apt)

    writeToFile(avenirApts, "avenirApts.txt", "Avenir")
    writeToFile(longfellowApts, "longfellow.txt", "Longfellow")

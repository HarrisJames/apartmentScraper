# This is a sample Python script.
import requests
from lxml import html
import smtplib
from email.mime.text import MIMEText
from datetime import datetime


# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.

class Apartment:

    def __init__(self, from_file, values):
        if from_file:
            self.bed = int(values[0])
            self.bath = float(values[2])
            self.price = int(values[5].replace("$", ""))
            self.sqft = int(values[6])
            self.floor = int(values[9])
            datetime_str = values[12]
            if datetime_str != 'Now':
                datetime_object = datetime.strptime(datetime_str.strip(), '%m/%d/%Y')
                now = datetime.now()
                if now > datetime_object:
                    self.available = 'Now'
                else:
                    self.available = values[12]
            else:
                self.available = values[12]
        else:
            self.price = int(values[0].replace(",", "").replace("$", ""))
            self.bed = int(values[3])
            self.bath = float(values[6])
            self.sqft = int(values[8])
            self.floor = int(values[12])
            datetime_str = values[14]
            datetime_object = datetime.strptime(datetime_str.strip(), '%m/%d/%Y')
            now = datetime.now()
            if now > datetime_object:
                self.available = 'Now'
            else:
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
    def has_price_change(self, other):
        if self.bath != other.bath:
            return False
        if self.bed != other.bed:
            return False
        if self.floor != other.floor:
            return False
        if self.sqft != other.sqft:
            return False
        if self.available != other.available:
            return False
        if self.price is other.price:
            return False
        return True


def make_request(url):
    r = requests.get(url)
    return r


def available_list(url, max_price):
    response = make_request(url)
    tree = html.fromstring(response.content)
    classes = tree.find_class('col-xs-4 specs')
    list = []
    for item in classes:
        toAdd = Apartment(False, item.text_content().split())
        if toAdd.bed > 0 and toAdd.price < max_price:
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

def send_email(subject, body, sender, recipients, password):
    msg = MIMEText(body, 'html')
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = recipients
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
       smtp_server.login(sender, password)
       smtp_server.sendmail(sender, recipients, msg.as_string())
    print("Message sent!")

def build_body(avenirSeen, avenirUnseen, longfellowSeen, longfellowUnseen, washingtonSeen, washingtonUnseen):
    result = ""
    if len(avenirUnseen):
        result += "Avenir Apartments:<br>"
        #price changes
        for apt in avenirUnseen:
            found_change = False
            for seen in avenirSeen:
                if apt.has_price_change(seen):
                    result += str(apt) + " price changed from $" + str(seen.price) + "<br>"
                    found_change = True
            if not found_change:
                result += str(apt) + "<br>"
        result += '<a href="https://www.equityapartments.com/boston/north-end/avenir-apartments##unit-availability-tile">Avenir Apartments</a><br><br>'
    if len(longfellowUnseen):
        result += "Longfellow Apartments:<br>"
        # price changes
        for apt in longfellowUnseen:
            found_change = False
            for seen in longfellowSeen:
                if apt.has_price_change(seen):
                    result += str(apt) + " price changed from $" + str(seen.price) + "<br>"
                    found_change = True
            if not found_change:
                result += str(apt) + "<br>"
        result += '<a href="https://www.equityapartments.com/boston/west-end/the-towers-at-longfellow-apartments##unit-availability-tile">Longfellow Apartments</a><br>'
    if len(washingtonUnseen):
        result += "Washington Apartments:<br>"
        # price changes
        for apt in washingtonUnseen:
            found_change = False
            for seen in washingtonSeen:
                if apt.has_price_change(seen):
                    result += str(apt) + " price changed from $" + str(seen.price) + "<br>"
                    found_change = True
            if not found_change:
                result += str(apt) + "<br>"
        result += '<a href="https://www.equityapartments.com/boston/boston-common/660-washington-apartments#/#unit-availability-tile">Washington Apartments</a><br>'
    return result

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    senderEmail = 'bostonaparmentbot@gmail.com'
    jamesEmail = "jamestown1277@yahoo.com"
    karliEmail = "karli.d.rodriguez@gmail.com"
    password = 'bgwa oruf kgpg hemo'
    avenirApts = available_list(
        'https://www.equityapartments.com/boston/north-end/avenir-apartments?mkwid=_dc&pcrid=&pkw=&pmt=&utm_source=google&utm_medium=cpc&utm_term=&utm_campaign=&utm_group=&gclsrc=aw.ds&&utm_source=google&utm_medium=cpc&utm_campaign=Avenir_Pmax&gad_source=1&gclid=Cj0KCQjwudexBhDKARIsAI-GWYVr_J6V1U4InujmNOjH3nn3nONK8sJ_oOaLXVVrkmsYZ2S5gXxDWRUaAhPeEALw_wcB#%23unit-availability-tile', 4000)
    longfellowApts = available_list(
        'https://www.equityapartments.com/boston/west-end/the-towers-at-longfellow-apartments##unit-availability-tile', 3700)
    washingtonApts = available_list(
        'https://www.equityapartments.com/boston/boston-common/660-washington-apartments#/#unit-availability-tile', 3700)

    avenirSeen = readFromFile('avenirApts.txt')
    longfellowSeen = readFromFile('longfellow.txt')
    washingtonSeen = readFromFile('washington.txt')

    writeToFile(avenirApts, "avenirApts.txt", "Avenir")
    writeToFile(longfellowApts, "longfellow.txt", "Longfellow")
    writeToFile(washingtonApts, "washington.txt", "Washington")

    avenirUnseen = []
    longfellowUnseen = []
    washingtonUnseen = []

    for apt in avenirApts:
        if apt not in avenirSeen:
            avenirUnseen.append(apt)
    for apt in longfellowApts:
        if apt not in longfellowSeen:
            longfellowUnseen.append(apt)
    for apt in washingtonApts:
        if apt not in washingtonSeen:
            washingtonUnseen.append(apt)

    if len(avenirUnseen) or len(longfellowUnseen) or len(washingtonUnseen):
        body = build_body(avenirSeen, avenirUnseen, longfellowSeen, longfellowUnseen, washingtonSeen, washingtonUnseen)
        send_email("New Apartments Found!", body, senderEmail, jamesEmail, password)
        send_email("New Apartments Found!", body, senderEmail, karliEmail, password)
    else:
        print("Checked but no new apartments, did not send message.")

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
            self.bed = int(values[7])
            self.bath = float(values[9])
            self.price = int(values[0].replace("$", ""))
            self.sqft = int(values[2])
            self.floor = int(values[6].replace(",", ""))
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
        return "\t$" + str(self.price) + " for " + str(self.sqft) + " sqft on floor " + str(self.floor) + ", " + str(
            self.bed) + " bed " + str(self.bath) + " bath, available " + self.available

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
            if toAdd.available == 'Now':
                list.append(toAdd)
            else:
                sept = datetime(2024, 9, 1)
                date = datetime.strptime(toAdd.available, '%m/%d/%Y')
                if date < sept:
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

def add_unseen(seen, unseen):
    # price changes
    result = ''
    for apt in unseen:
        found_change = False
        for found in seen:
            if apt.has_price_change(found):
                if apt.price < found.price - 20:
                    result += '(-$' + str(found.price - apt.price) + ')' + str(apt) + "<br>"
                found_change = True
        if not found_change:
            result += str(apt) + "<br>"
    return result

def build_body(avenir_string):
    result = ""
    if len(avenir_string):
        result += '<a href="https://www.equityapartments.com/boston/north-end/avenir-apartments##unit-availability-tile">Avenir Apartments:</a><br><br>'
        result += avenir_string + '<br>'
    return result

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    senderEmail = 'bostonaparmentbot@gmail.com'
    jamesEmail = "jamestown1277@yahoo.com"
    karliEmail = "karli.d.rodriguez@gmail.com"
    password = 'bgwa oruf kgpg hemo'
    avenirApts = available_list(
        'https://www.equityapartments.com/boston/north-end/avenir-apartments?mkwid=_dc&pcrid=&pkw=&pmt=&utm_source=google&utm_medium=cpc&utm_term=&utm_campaign=&utm_group=&gclsrc=aw.ds&&utm_source=google&utm_medium=cpc&utm_campaign=Avenir_Pmax&gad_source=1&gclid=Cj0KCQjwudexBhDKARIsAI-GWYVr_J6V1U4InujmNOjH3nn3nONK8sJ_oOaLXVVrkmsYZ2S5gXxDWRUaAhPeEALw_wcB#%23unit-availability-tile', 3900)

    avenirSeen = readFromFile('avenirApts.txt')
    writeToFile(avenirApts, "avenirApts.txt", "Avenir")
    avenirUnseen = []

    for apt in avenirApts:
        if apt not in avenirSeen:
            avenirUnseen.append(apt)

    avenir_string = add_unseen(avenirSeen, avenirUnseen)

    if len(avenir_string):
        if len(avenirUnseen) is 1:
            body = build_body(avenir_string)
            send_email("New Apartment Found!", body, senderEmail, jamesEmail, password)
            send_email("New Apartment Found!", body, senderEmail, karliEmail, password)
        else if len(avenir_string) >= 2:
            body = build_body(avenir_string)
            send_email("New Apartments Found!", body, senderEmail, jamesEmail, password)
            send_email("New Apartments Found!", body, senderEmail, karliEmail, password)
    else:
        print("Checked but no new apartments, did not send message.")

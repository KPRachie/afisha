from flask import Flask, redirect
from sqlite3 import connect
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)


def update_conservatory():
    conn = connect("coservatort.sqlite")
    URL = "https://www.mosconsv.ru/ru/concerts.aspx?start="
    a = 0
    for j in range(32):
        a = int(a)
        a = a + 1
        a = str(a)
        answer = requests.get(URL + a)
        answer = BeautifulSoup(answer.text)
        conserts = answer.find_all("div", {"class": "concert-post"})
        for i in conserts:
            concerts1 = i.find("div", {"class": "col-sm-9 c-d"})
            concerts = concerts1.find("div", {"class": "post-data"})
            concert = concerts.find("h4")
            title = concerts.find("h6")
            answer = concert.find("a")
            where = "Консерватория"
            hall = answer.text
            title = title.text
            link = answer.attrs.get("href")
            about1 = requests.get("https://www.mosconsv.ru" + link)
            abouts = BeautifulSoup(about1.text)
            abouts = abouts.find_all("div", {"class": "row"})
            song = ""
            if len(abouts) - 1 >= 3:
                about = abouts[3].find("div", {"class": "col-sm-12"})
                if about:
                    song = about.text
                else:
                    song = "None"
            new_link = "https://www.mosconsv.ru" + answer.attrs.get("href")
            date1 = requests.get("https://www.mosconsv.ru" + link)
            dates = BeautifulSoup(date1.text)
            date = dates.find("div", {"class": "col-sm-3 afisha-date"})
            date = date.text
            conn.execute("INSERT INTO con1 ('where', hall, title, song, link, date) VALUES (?, ?, ?, ?, ?, ?)",
                         [where, hall, title, song, new_link, date])
            conn.commit()
    return redirect('/')

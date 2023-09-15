import requests
from bs4 import BeautifulSoup
from sqlite3 import connect


def update_philarmony():
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246"
    }

    for i in range(9, 13):
        conn = connect("coservatort.sqlite")
        answer = requests.get("https://meloman.ru/calendar/" + "?month=" + str(i), headers=headers)
        soup = BeautifulSoup(answer.text, 'html.parser')
        links = soup.find_all("li")
        for link in links:
            data_link = link.attrs.get('data-link')
            if data_link:
                if "kzch" in data_link or "kzf" in data_link or "f2" in data_link or "mz" in data_link or "bzk" in data_link:
                    answer1 = requests.get('https://meloman.ru' + data_link)
                    soup1 = BeautifulSoup(answer1.text)
                    title = soup1.find("h1")
                    title1 = title.text
                    date = soup1.find_all("p")[2]
                    date1 = date.text
                    hall = soup1.find_all("p")[3]
                    hall1 = hall.text
                    song1 = soup1.find("div", {"class": "programme"})
                    if song1:
                        song2 = song1.text
                        if song2:
                            title = title1
                            hall = hall1
                            song = song2
                            date = date1
                            where = "Филармония"
                            new_link = 'https://meloman.ru' + data_link
                            conn.execute(
                                "INSERT INTO con1 ('where', hall, title, song, link, date) VALUES (?, ?, ?, ?, ?, ?)",
                                [where, hall, title, song, new_link, date])
                            conn.commit()

import requests
from bs4 import BeautifulSoup
from sqlite3 import connect


def update_philarmony():
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246"
    }

    for i in range(12, 13):
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
                    date = soup1.find_all("p", {"class": "text size18"})[0]
                    date1 = date.text[52::]
                    hall = soup1.find_all("p", {"class": "text size18"})[1]
                    hall1 = hall.text.replace("\n", "").replace("                            ", "")
                    song1 = soup1.find("div", {"class": "right-half programme selen"})
                    if song1:
                        song2 = song1.text
                        index = song2.find("В программе:")
                        song2 = song2[index::].replace("\n\n\n\n", '\n').replace("                     ", '\n').replace("\n\n\n \n", '\n').replace("\n\n", '\n')
                        index2 = song2.find("Абонемент")
                        if index2 != -1:
                            song2 = song2[:index2]
                        index3 = song2.find("Рекомендуем для детей")
                        if index3 != -1:
                            song2 = song2[:index3]
                        index4 = song2.find("Купить билеты")
                        if index4 != -1:
                            song2 = song2[:index4]
                        song2 = song2.replace("\n ", '\n')
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

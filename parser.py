import requests
from bs4 import BeautifulSoup
import sqlite3

for page in range(1, 5):
    url = f"https://geo.saitebi.ge/main/new/{page}"
    h = {"Accept-Language": "en-US"}
    r = requests.get(url, headers=h)
    soup = BeautifulSoup(r.text, "html.parser")

    conn = sqlite3.connect("data.sqlite")
    cur = conn.cursor()

    #create table
    cur.execute("""CREATE TABLE IF NOT EXISTS movies(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title VARCHAR(50),
        genre VARCHAR(20),
        rating INTEGER,
        year INTEGER, 
        url VARCHAR(200)
    )""")

    #info
    content = soup.find("div", id="content")
    movies = content.find_all("div", class_="movie-items-wraper")
    for movie in movies:
        # title,year
        title = movie.h4.text.replace(":", " ")
        year = movie.span.text

        #images
        image_url = movie.a.img.attrs["src"]
        file = open(f'static/images/{title}.png', 'bw')
        image = requests.get(f"https://geo.saitebi.ge/{image_url}")
        file.write(image.content)
        print(image)

        #genre, rating
        site = movie.a.attrs["href"]
        r = requests.get(f"https://geo.saitebi.ge/{site}", headers=h)
        soup = BeautifulSoup(r.text, "html.parser")
        content = soup.find("div", class_="movie-item-full")
        rating = content.a.text
        genre = content.find("a", "movie-genre-item").attrs["href"][10:]
        video_attrs = soup.find("div", class_="player-list-item").attrs["onclick"]
        video_url = video_attrs[video_attrs.find('"')+1:video_attrs.find('"', 10)]

        print(genre)
        print(rating)
        print(title)
        print(year)
        print(site)
        print(video_url)

        #insert data
        cur.execute(f"INSERT INTO movies(title, genre, rating, year, url) VALUES('{title}', '{genre}', {rating}, {year}, '{video_url}')")
        conn.commit()

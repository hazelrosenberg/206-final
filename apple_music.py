import requests
import sqlite3
from bs4 import BeautifulSoup
import os
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import matplotlib.pyplot as plt
from textwrap import wrap

def setUpDatabase(db_name):
    '''Connects to the database with the provided name (db_name).'''
    path = os.path.dirname(os.path.abspath(__file__))
    conn  = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()
    return cur, conn
    pass

def createSpotipyObject(filename):
    source_dir = os.path.dirname(os.path.abspath(__file__))
    full_path = os.path.join(source_dir, filename)
    infile = open(full_path,'r', encoding='utf-8')
    lines = infile.readlines()
    infile.close()
    cid = lines[0].strip()
    secret = lines[1]
    client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret)
    sp = spotipy.Spotify(client_credentials_manager = client_credentials_manager)
    return sp
    pass


def getTopChartsData(url, sp, country):
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')
    tags = soup.find_all('td', class_='mp text')
    collect_info = []
    for tag in tags:
        info = tag.text
        info = info.split(' - ')
        song_name = info[1]
        artist = info[0]
        artist_info = sp.search(q=artist, limit=1, offset=0, type='artist', market=None)
        try:
            song_genre = artist_info['artists']['items'][0]['genres'][0]
        except:
            song_genre = 'Other'
        collect_info.append((song_name, song_genre, country))
    return collect_info[:50]
    pass

def createAppleMusicTable(cur, conn):
    cur.execute('CREATE TABLE IF NOT EXISTS AppleMusic (id INTEGER PRIMARY KEY, song_name TEXT, specific_genre_id INTEGER, broad_genre_id INTEGER, country_id INTEGER)')
    conn.commit()
    pass

def createAppleMusicGenresTable(cur, conn):
    cur.execute('CREATE TABLE IF NOT EXISTS AppleMusicGenres (id INTEGER PRIMARY KEY, specific_genre TEXT UNIQUE, broad_genre_id INTEGER)')
    conn.commit()
    pass

def storeGenresData(data, cur, conn, offset):
    broad_genres = []
    cur.execute('SELECT genre FROM Genres')
    for item in cur:
        broad_genres.append(item[0])
    r = offset + 25
    for i in range(offset, r):
        song_info = data[i]
        specific_genre = song_info[1]
        for genre in broad_genres:
            if genre.lower() in specific_genre:
                broad_genre = genre
                break
            else:
                broad_genre = ''
                continue
        if broad_genre not in broad_genres:
                broad_genre = "Other"
        cur.execute('SELECT id FROM Genres WHERE genre=?', (broad_genre, ))
        broad_genre_id = cur.fetchall()[0][0]
        cur.execute('INSERT OR IGNORE INTO AppleMusicGenres (id,specific_genre,broad_genre_id) VALUES (?,?,?)', (i, specific_genre, broad_genre_id))
    conn.commit()
    pass
    
def storeData(data, cur, conn, offset):
    r = offset + 25
    for i in range(offset, r):
        song_info = data[i]
        cur.execute('SELECT id FROM AppleMusicGenres WHERE specific_genre=?', (song_info[1], ))
        specific_genre_id = cur.fetchall()[0][0]
        cur.execute('SELECT Genres.id FROM Genres JOIN AppleMusicGenres ON Genres.id = AppleMusicGenres.broad_genre_id WHERE AppleMusicGenres.specific_genre=?', (song_info[1], ))
        broad_song_genre_id = cur.fetchall()[0][0]
        cur.execute('SELECT id FROM Countries WHERE country=?', (song_info[2], ))
        song_country_id = cur.fetchall()[0][0]
        cur.execute('INSERT OR IGNORE INTO AppleMusic (id, song_name, specific_genre_id, broad_genre_id, country_id) VALUES (?,?,?,?,?)', (i, song_info[0], specific_genre_id, broad_song_genre_id, song_country_id))
        conn.commit()
    pass


def getGenreCounts(country, cur):
    l = []
    cur.execute('SELECT id FROM Genres')
    genres = cur.fetchall()
    for g in genres:
        i = g[0]
        cur.execute('SELECT COUNT(AppleMusic.broad_genre_id), Genres.genre FROM Genres INNER JOIN AppleMusic ON Genres.id = AppleMusic.broad_genre_id INNER JOIN Countries ON Countries.id = AppleMusic.country_id WHERE Genres.id=? AND Countries.country=?', (i, country))
        l.append(cur.fetchone())
    return l
    pass

def writeCalculatedDataToFile(data, filename):
    dir = os.path.dirname(__file__)
    outFile = open(os.path.join(dir, filename), 'w')
    total = 0
    for item in data:
        total += item[0]
    outFile.write('Genre,Number of Songs,Percent of Total')
    for item in data:
        perc = round((item[0] / total) * 100)
        try:
            outFile.write('\n'+item[1]+','+str(item[0])+','+str(perc)+'%')
        except:
            None
    outFile.write('\n')
    outFile.write('\nTotal Number of Songs: '+str(total))
    outFile.close()
    pass

def createPieChart(data, title, cur):
    data = sorted(data, reverse=True)
    no_zeros = [i for i in data if i[0] != 0]
    zeros = []
    cur.execute('SELECT genre FROM Genres')
    for item in cur:
        genre = item[0]
        if genre not in [i for t in no_zeros for i in t]:
            zeros.append(genre)
    zeros = ', '.join(zeros)
    labels = []
    sizes = []
    total = 0
    for tup in no_zeros:
        labels.append(tup[1])
        total += tup[0]
    for tup in no_zeros:
        size = (tup[0]/total) * 360
        sizes.append(size)
    colors = ['#e6ff00', '#1b96c6', '#ff952a', '#61ff68', '#e258c3', '#71f7ff', '#8682e6', '#ff646a', '#00b5af', '#ffe65b', '#5dc480']
    plt.figure(figsize=(7,7))
    plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', pctdistance=0.85, textprops={'fontsize': 12})
    plt.axis('equal')
    plt.title('\n'.join(wrap(title,60)), fontsize=14, fontweight='bold')
    footnote = f'Genres with no songs in the top 50 this week: {zeros}'
    plt.annotate(footnote, xy=(-0.1,-0.1), xycoords='axes fraction', fontsize=9)
    plt.show()
    pass


def main():
    #SETS UP THE DATABASE
    cur, conn = setUpDatabase('music.db')

    #SETS UP SPOTIPY (TO USE IN CONJUNCTION WITH BEAUTIFUL SOUP)
    secrets_file = 'secrets.txt'
    sp = createSpotipyObject(secrets_file)

    #CREATE APPLE MUSIC GENRES TABLE (IF IT DOESN'Y ALREADY EXIST)
    createAppleMusicGenresTable(cur, conn)

    #COLLECT USA TOP SONGS INFO USING BEAUTIFUL SOUP AND SPOTIPY OBJECT
    usa_url = 'https://kworb.net/charts/apple_s/us.html'
    usa_data = getTopChartsData(usa_url, sp, 'USA')

    #COLLECT CANADA TOP SONGS INFO USING BEAUTIFUL SOUP AND SPOTIPY OBJECT
    canada_url = 'https://kworb.net/charts/apple_s/ca.html'
    canada_data = getTopChartsData(canada_url, sp, 'Canada')

    #COLLECT MEXICO TOP SONGS INFO USING BEAUTIFUL SOUP AND SPOTIPY OBJECT
    mexico_url = 'https://kworb.net/charts/apple_s/mx.html'
    mexico_data = getTopChartsData(mexico_url ,sp, 'Mexico')

    #COMBINE DATA FROM CANADA,  MEXICO, USA INTO ONE LIST TO STORE IN DATABASE
    all_data = canada_data + usa_data + mexico_data

    #CREATE APPLE MUSIC TABLE IN DATABASE
    createAppleMusicTable(cur, conn)

    #ADD ALL DATA 25 ITEMS AT A TIME (RUN CODE AT LEAST 12 TIMES)
    try:
        cur.execute('SELECT id FROM AppleMusicGenres WHERE id = (SELECT MAX (id) FROM AppleMusicGenres)')
        start = cur.fetchone()
        offset = start[0] + 1
    except:
        offset = 0
    try:
        storeGenresData(all_data, cur, conn, offset)
    except:
        cur.execute('SELECT * FROM AppleMusic')
        num_rows_s = len(cur.fetchall())
        if num_rows_s < len(all_data):
            try:
                cur.execute('SELECT id FROM AppleMusic WHERE id = (SELECT MAX (id) FROM AppleMusic)')
                start = cur.fetchone()
                offset = start[0] + 1
            except:
                offset = 0
            storeData(all_data, cur, conn, offset)

    #GET GENRE COUNTS FROM DATABASE
    canada_genres = getGenreCounts('Canada', cur)
    usa_genres = getGenreCounts('USA', cur)
    mexico_genres = getGenreCounts('Mexico', cur)


    #WRITE CALCULATED DATA TO TEXT FILES
    c_title = 'appleMusicCalculationsCanada.txt'
    writeCalculatedDataToFile(canada_genres, c_title)
    u_title = 'appleMusicCalculationsUSA.txt'
    writeCalculatedDataToFile(usa_genres, u_title)
    m_title = 'appleMusicCalculationsMexico.txt'
    writeCalculatedDataToFile(mexico_genres, m_title)

    #CREATE PIE CHARTS SHOWING PROPORTIONS OF EACH GENRE BY NUMBER OF SONGS
    canada_title = 'Proportion of Genres of Top 50 Most Popular Songs in Canada on Apple Music This Week'
    createPieChart(canada_genres, canada_title, cur)
    usa_title = 'Proportion of Genres of Top 50 Most Popular Songs in the USA on Apple Music This Week'
    createPieChart(usa_genres, usa_title, cur)
    mexico_title = 'Proportion of Genres of Top 50 Most Popular Songs in Mexico on Apple Music This Week'
    createPieChart(mexico_genres, mexico_title, cur)


if __name__ == '__main__':
    main()
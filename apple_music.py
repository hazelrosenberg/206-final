import requests
import sqlite3
from bs4 import BeautifulSoup
import pandas as pd
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
    '''Reads in text file and creates spotipy object with client id and client secret (stored in text file).'''
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

def createGenresTable(genres, cur, conn):
    '''Creates genres table in the database with a given list of genres, database connection, and cursor.'''
    cur.execute('CREATE TABLE IF NOT EXISTS Genres (id INTEGER PRIMARY KEY, genre TEXT UNIQUE)')
    for i in range(len(genres)):
        cur.execute('INSERT OR IGNORE INTO Genres (id,genre) VALUES (?,?)', (i, genres[i]))
    conn.commit()
    pass

def getTopChartsData(url, sp, cur):
    '''Uses beautiful soup to scrape a website and gather data for the apple music top charts. Uses spotipy object to use the scraped data to determine the genre for each song. Uses a database cursor object to assign a genre_id to each song based of the song's genre from Spotify and the genres in the music.db table. Returns a list of tuples with (song_name, genre_id).'''
    cur.execute('SELECT genre FROM Genres')
    genres = []
    for item in cur:
        genres.append(item[0])
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
            for g in genres:
                if g.lower() in song_genre:
                    song_genre = g
                    break
                else:
                    continue
            if song_genre not in genres:
                song_genre = 'Other'
        except:
            song_genre = 'Other'
        cur.execute('SELECT id FROM Genres WHERE genre=?', (song_genre, ))
        song_genre_id = cur.fetchone()[0]
        collect_info.append((song_name, song_genre_id))
    return collect_info[:50]
    pass

def createUSATable(data, cur, conn, offset=0):
    '''Creates USAAppleMusic table in the database (music.db), if it doesn't already exist, with the cursor and connection objects passed in as parameters. Takes the offset paramater (an integer that defaults to 0 if not passed in otherwise as a parameter) and adds 25 to it to create a range with a length of 25 to add 25 items at a time to the database. Loops through the items in the list passed in as a parameter (data) to add items to the database.'''
    cur.execute('CREATE TABLE IF NOT EXISTS USAAppleMusic (id INTEGER PRIMARY KEY, song_name TEXT UNIQUE, genre_id INTEGER)')
    conn.commit()
    r = offset + 25
    for i in range(offset, r):
        song_info = data[i]
        cur.execute('INSERT OR IGNORE INTO USAAppleMusic (id,song_name,genre_id) VALUES (?,?,?)', (i, song_info[0], song_info[1]))
        conn.commit()    
    pass

def createCanadaTable(data, cur, conn, offset=0):
    '''Creates CanadaAppleMusic table in the database (music.db), if it doesn't already exist, with the cursor and connection objects passed in as parameters. Takes the offset paramater (an integer that defaults to 0 if not passed in otherwise as a parameter) and adds 25 to it to create a range with a length of 25 to add 25 items at a time to the database. Loops through the items in the list passed in as a parameter (data) to add items to the database.'''
    cur.execute('CREATE TABLE IF NOT EXISTS CanadaAppleMusic (id INTEGER PRIMARY KEY, song_name TEXT UNIQUE, genre_id INTEGER)')
    conn.commit()
    r = offset + 25
    for i in range(offset, r):
        song_info = data[i]
        cur.execute('INSERT OR IGNORE INTO CanadaAppleMusic (id,song_name,genre_id) VALUES (?,?,?)', (i, song_info[0], song_info[1]))
        conn.commit()    
    pass

def getCanadaGenreCounts(cur):
    '''Uses the cursor object to select all the genres from the Genres table in the database (music.db), and then selects the count of how many songs of each genre are in the CanadaAppleMusic table by joining the Genres and CanadaAppleMusic tables on the genre ids. Returns the count and name of each genre as a tuple in a list of tuples.'''
    l = []
    cur.execute('SELECT genre FROM Genres')
    x = cur.fetchall()
    for item in x:
        cur.execute('SELECT COUNT(genre_id) FROM CanadaAppleMusic JOIN Genres ON CanadaAppleMusic.genre_id = Genres.id WHERE Genres.genre = ?', (item[0], ))
        l.append((cur.fetchone()[0], item[0]))
    return l
    pass

def getUSAGenreCounts(cur):
    '''Uses the cursor object to select all the genres from the Genres table in the database (music.db), and then selects the count of how many songs of each genre are in the USAAppleMusic table by joining the Genres and USAAppleMusic tables on the genre ids. Returns the count and name of each genre as a tuple in a list of tuples.'''
    l = []
    cur.execute('SELECT genre FROM Genres')
    x = cur.fetchall()
    for item in x:
        cur.execute('SELECT COUNT(genre_id) FROM USAAppleMusic JOIN Genres ON USAAppleMusic.genre_id = Genres.id WHERE Genres.genre = ?', (item[0], ))
        l.append((cur.fetchone()[0], item[0]))
    return l
    pass

def writeCalculatedDataToFile(data, filename):
    '''Accepts list of tuples for a playlist that include each genre and the number of songs of that genre in the playlist (data), and a file name to write the calculations to (filename). Creates the file in the directory, named after the filename parameter. Performs calculations and writes them to the file, then closes the file.'''
    dir = os.path.dirname(__file__)
    outFile = open(os.path.join(dir, filename), 'w')
    total = 0
    for item in data:
        total += item[0]
    outFile.write('Genre,Number of Songs,Percent of Total')
    for item in data:
        perc = round((item[0] / total) * 100)
        outFile.write('\n'+item[1]+','+str(item[0])+','+str(perc)+'%')
    outFile.write('\n')
    outFile.write('\nTotal Number of Songs: '+str(total))
    outFile.close()
    pass

def createPieChart(data, title):
    '''Accepts a list of tuples for a playlist that include each genre and the number of songs of that genre in the playlist (data), and a title for the pie chart (title). Omits genres with 0 songs in the playlist from being included in the pie chart and makes a footnote of which genres had no songs. Creates a pie chart with the genres that had more than 0 songs.'''
    data = sorted(data, reverse=True)
    no_zeros = [i for i in data if i[0] != 0]
    zeros = ', '.join([i[1] for i in data if i[0] == 0])
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
    #plt.tight_layout()
    plt.show()
    pass


def main():
    #SETS UP THE DATABASE
    cur, conn = setUpDatabase('music.db')

    #SETS UP SPOTIPY (TO USE IN CONJUNCTION WITH BEAUTIFUL SOUP)
    secrets_file = 'secrets.txt'
    sp = createSpotipyObject(secrets_file)

    #CREATES GENRES TABLE (IF IT DOESN'T ALREADY EXIST)
    genres = ['Rock', 'Pop', 'Hip Hop', 'Rap', 'R&B', 'Country', 'Alt', 'Classical', 'EDM', 'Jazz', 'Other']
    createGenresTable(genres, cur, conn)

    #COLLECT USA TOP SONGS INFO USING BEAUTIFUL SOUP AND SPOTIPY OBJECT
    usa_url = 'https://kworb.net/charts/apple_s/us.html'
    usa_data = getTopChartsData(usa_url, sp, cur)

    #COLLECT CANADA TOP SONGS INFO USING BEAUTIFUL SOUP AND SPOTIPY OBJECT
    canada_url = 'https://kworb.net/charts/apple_s/ca.html'
    canada_data = getTopChartsData(canada_url, sp, cur)

    #CREATE TABLES IN DATABASE AND ADD DATA 25 ITEMS AT A TIME (RUN CODE TWICE)
    try:
        cur.execute('SELECT * FROM USAAppleMusic')
        createUSATable(usa_data, cur, conn, 25)
    except:
        createUSATable(usa_data, cur, conn)
    try:
        cur.execute('SELECT * FROM CanadaAppleMusic')
        createCanadaTable(canada_data, cur, conn, 25)
    except:
        createCanadaTable(canada_data, cur, conn)

    #GET GENRE COUNTS FROM DATABASE
    canada_genres = getCanadaGenreCounts(cur)
    usa_genres = getUSAGenreCounts(cur)

    #WRITE CALCULATED DATA TO TEXT FILES
    c_title = 'appleMusicCalculationsCanada.txt'
    writeCalculatedDataToFile(canada_genres, c_title)
    u_title = 'appleMusicCalculationsUSA.txt'
    writeCalculatedDataToFile(usa_genres, u_title)

    #CREATE PIE CHARTS SHOWING PROPORTIONS OF EACH GENRE BY NUMBER OF SONGS
    canada_title = 'Proportion of Genres of Top 50 Most Popular Songs in Canada on Apple Music This Week'
    createPieChart(canada_genres, canada_title)
    usa_title = 'Proportion of Genres of Top 50 Most Popular Songs in the USA on Apple Music This Week'
    createPieChart(usa_genres, usa_title)


if __name__ == '__main__':
    main()
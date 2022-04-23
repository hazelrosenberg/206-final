import requests
import sqlite3
from bs4 import BeautifulSoup
import pandas as pd
import os
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

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
    ''''''
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


if __name__ == '__main__':
    main()



#url = 'https://kworb.net/charts/apple_s/us.html'   
#r = requests.get(url)
#soup = BeautifulSoup(r.content, 'html.parser')
#tags =soup.find_all('td', class_ = 'mp text')          
#collect_info = []
#for tag in tags:
    #info = tag.text
    #info = info.split(' - ')
    #song_name = info[1]
    #artist = info[0]
    #collect_info.append((song_name, artist))

#EXTRACT EACH STRING AND SPLIT WITH ' - '
#IN EACH OUTPUT, 0 INDEX IS THE ARTIST AND 1 INDEX IS THE SONG TITLE
#ONE WILL BE CALLED ARTIST AND THE OTHER CALLED SONG
#PRECEEDING CREATING DICTIONARY AND DATABASE
#delimiter = ' - '
    #new_collect = collect_info[0].split(delimiter)
    #artist = new_collect[0]
    #song = new_collect[1]
    #song = collect_info[1]
#print(artist)   
#print(song)

#after splitting up lists...
#UNCOMMENT AND THIS WILL CREATE SPREADSHEET WITH ALL DATA

#usa_dictionary = {'song_title_usa': song, 'artist_name_usa': artist}
#data_frame = pd.DataFrame(usa_dictionary)
#to_csv =  data_frame.to_csv('/Users/sydneysella/billboard_usa_data.csv')

#UNCOMMENT AND THIS WILL SAVE ALL TO A DATABASE
#db = mysql.connector.connect(database = 'music')
#cursor = db.cursor()
#insert and stuff, watch rest of video after database stuff is sorted










#import requests
#import sqlite3
#import matplotlib.pyplot as plt
#from bs4 import BeautifulSoup
#import os
#import mysql.connector

#def setUpDatabase(db_name):
    #'''Sets up the database with the provided name (db_name).'''
    #path = os.path.dirname(os.path.abspath(__file__))
    #conn  = sqlite3.connect(path+'/'+db_name)
    #cur = conn.cursor()
    #return cur, conn

#def billboard_100canada(): #are we doing usa
    #song_titlesca = []
    #url = input('https://www.billboard.com/charts/canadian-hot-100/') #whatever url we will use 
    #resp = requests.get(url)
    #if resp.ok:
        #soup= BeautifulSoup(resp.content, 'html.parser')
    #titles = soup.find_all('h3', class_ = 'c-title a-no-trucate-a-font-primary-bold-s u-letter-spacing-0021 lrv-u-font-size-18@tablet lrv-u-font-size-16 u-line-height-125 u-line-height-normal@mobile-max a-truncate-ellipsis u-max-width-330 u-max-width-230@tablet-only')
    #artists = soup.find_all('span', class_ = 'c-label a-no-trucate a-font-primary-s lrv-u-fofnt-size-14@mobile-max u-letter-spacing-0021 lrv-u-display-block a-truncate-ellpisis-2line u-max-width-330 u-max-width-230@tablet-only')
    #for i in range(len(titles[:25])):
        #title = titles[i].text.strip()
        #artist = artists[i].text.strip()
        #tuple1 = (title, artist)
        #song_titlesca.append(tuple1)
    #for i in range(len(titles[25:50])):
        #title = titles[i].text.strip()
        #artist = artists[i].text.strip()
        #tuple1 = (title, artist)
        #song_titlesca.append(tuple1)
    #for i in range(len(titles[50:75])):
        #title = titles[i].text.strip()
        #artist = artists[i].text.strip()
        #tuple1 = (title, artist)
        #song_titlesca.append(tuple1)
    #for i in range(len(titles[75:])):
        #title = titles[i].text.strip()
        #artist = artists[i].text.strip()
        #tuple1 = (title, artist)
        #song_titlesca.append(tuple1)
    #for tag in tags[:25]:
        #titles = tag.get()
        #song_titles.append(titles)
    #return song_titlesca

#def billboard_100usa():
    #song_titlesusa = []
    #url = input('https://www.billboard.com/charts/the-billboard-hot-100/') #whatever url we will use 
    #resp = requests.get(url)
    #if resp.ok:
        #soup= BeautifulSoup(resp.content, 'html.parser')
    #titles = soup.find_all('h3', class_ = 'c-title a-no-trucate-a-font-primary-bold-s u-letter-spacing-0021 lrv-u-font-size-18@tablet lrv-u-font-size-16 u-line-height-125 u-line-height-normal@mobile-max a-truncate-ellipsis u-max-width-330 u-max-width-230@tablet-only')
    #artists = soup.find_all('span', class_ = 'c-label a-no-trucate a-font-primary-s lrv-u-fofnt-size-14@mobile-max u-letter-spacing-0021 lrv-u-display-block a-truncate-ellpisis-2line u-max-width-330 u-max-width-230@tablet-only')
    #for i in range(len(titles[:25])):
        #title = titles[i].text.strip()
        #artist = artists[i].text.strip()
        #tuple1 = (title, artist)
        #song_titlesusa.append(tuple1)
    #for i in range(len(titles[25:50])):
        #title = titles[i].text.strip()
        #artist = artists[i].text.strip()
        #tuple1 = (title, artist)
        #song_titlesusa.append(tuple1)
    #for i in range(len(titles[50:75])):
        #title = titles[i].text.strip()
        #artist = artists[i].text.strip()
        #tuple1 = (title, artist)
        #song_titlesuk.append(tuple1)
    #for i in range(len(titles[75:])):
        #title = titles[i].text.strip()
        #artist = artists[i].text.strip()
        #tuple1 = (title, artist)
        #song_titlesuk.append(tuple1)
    #return song_titlesusa#this will be what has all of the scraped data in it
#def  create_cabb_table(data, cur, conn, offset=0):
    #cur.execute('CREATE TABLE IF NOT EXISTS CanadaBBTable (id INTEGER PRIMARY KEY, bbsong_name TEXT UNIQUE, bbartist_name TEXT UNIQUE')
    #conn.commit()
    #r = offset + 25
    #for i in range(offset, r):
        #song_info = data[i]
        #cur.execute('INSERT OR IGNORE INTO CanadaBBTable (id, bbsong_name, bbartist_name) VALUES (?,?,?)', (i, song_info[0], song_info[1]))
        #conn.commit()
    #pass
#def create_usabb_table(data, cur, conn, offset=0):
    #cur.execute('CREATE TABLE IF NOT EXISTS UsaBBTable (id INTEGER PRIMARY KEY, bbsong_nameusa TEXT UNIQUE, bbartist_nameusa TEXT UNIQUE')
    #r = offset +  25
    #for i in range(offset, r):
        #song_info = data[i]
        #cur.execute('INSERT OR IGNORE INTO UsaBBTable (id, bbsong_nameusa, bbartist_nameusa) VALUES (?,?,?)', (i, song_info[0], song_info[1]))
        #conn.commit()
    #pass
#def add_genres(db_filename):
    #path = os.path.dirname(os.path.abspath(__file__))
    #conn = sqlite3.connect(path+'/'+db_filename)
    #cur = conn.cursor()
    #cur.execute('SELECT UsaBBTable.id from UsaBBTable JOIN Genres ')
    #somehow add genres to the table but make the songs the same?
   



#def main():
    #sets up database
    #cur, conn = setUpDatabase('music.db')
    
   

#if __name__ == '__main__':
    #main()

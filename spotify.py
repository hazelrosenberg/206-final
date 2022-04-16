import requests
import sqlite3
import json
import os
import sys
import unittest
import csv
import matplotlib.pyplot as plt
from  bs4 import BeautifulSoup
#from tabulate import tabulate #dont forget pip install tabulate
import pprint
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

def setUpDatabase(db_name):
    '''Sets up the database with the provided name (db_name).'''
    path = os.path.dirname(os.path.abspath(__file__))
    conn  = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()
    return cur, conn

def createSpotipyObject(cid, secret):
    '''Creates spotipy object with client id and client secret.'''
    client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret)
    sp = spotipy.Spotify(client_credentials_manager = client_credentials_manager)
    return sp

def createGenresTable(genres, cur, conn):
    '''Creates genres table in the database with a given list of genres, database connection, and cursor.'''
    cur.execute('CREATE TABLE IF NOT EXISTS Genres (id INTEGER PRIMARY KEY, genre TEXT UNIQUE)')
    for i in range(len(genres)):
        cur.execute('INSERT OR IGNORE INTO Genres (id,genre) VALUES (?,?)', (i, genres[i]))
    conn.commit()
    pass

def getPlaylistData(pid, sp, cur):
    '''Collects information for each track in a playlist (specified by playlist id parameter), including the name of the song and the genre of the song's artist, using spotipy object (sp) passed in as a parameter. Uses cursor to select genre names and ids from the database (music.db) to standardize the genres found with the spotipy object. Returns list of tuples containing the song name, and genre id for each track in the playlist.'''
    cur.execute('SELECT genre FROM Genres')
    genres = []
    for item in cur:
        genres.append(item[0])
    playlist_songs = sp.playlist_items(pid)
    playlist_songs_info = []
    for song in playlist_songs['items']:
        song_name = song['track']['name'] #for DB
        artist_id = song['track']['artists'][0]['id']
        artist_info = sp.artist(artist_id)
        song_genres = artist_info['genres']
        if len(song_genres) > 0:
            song_genre = song_genres[0]
        else:
            song_genre = 'Other'
        for g in genres:
            if g.lower() in song_genre:
                song_genre = g
                break
            else:
                continue
        if song_genre not in genres:
            song_genre = 'Other'
        cur.execute('SELECT id FROM Genres WHERE genre=?', (song_genre, ))
        song_genre_id = cur.fetchone()[0]
        playlist_songs_info.append((song_name, song_genre_id))
    return playlist_songs_info
    pass

def createCanadaTable(data, cur, conn, offset=0):
    '''Creates CanadaSpotify table in the database (music.db), if it doesn't already exist, with the cursor and connection objects passed in as parameters. Takes the offset paramater (an integer that defaults to 0 if not passed in otherwise as a parameter) and adds 25 to it to create a range with a length of 25 to add 25 items at a time to the database. Loops through the items in the list passed in as a parameter (data) to add items to the database.'''
    cur.execute('CREATE TABLE IF NOT EXISTS CanadaSpotify (id INTEGER PRIMARY KEY, song_name TEXT UNIQUE, genre_id INTEGER)')
    conn.commit()
    r = offset + 25
    for i in range(offset, r):
        song_info = data[i]
        cur.execute('INSERT OR IGNORE INTO CanadaSpotify (id,song_name,genre_id) VALUES (?,?,?)', (i, song_info[0], song_info[1]))
        conn.commit()    
    pass

def createUKTable(data, cur, conn, offset=0):
    '''Creates UKSpotify table in the database (music.db), if it doesn't already exist, with the cursor and connection objects passed in as parameters. Takes the offset paramater (an integer that defaults to 0 if not passed in otherwise as a parameter) and adds 25 to it to create a range with a length of 25 to add 25 items at a time to the database. Loops through the items in the list passed in as a parameter (data) to add items to the database.'''
    cur.execute('CREATE TABLE IF NOT EXISTS UKSpotify (id INTEGER PRIMARY KEY, song_name TEXT UNIQUE, genre_id INTEGER)')
    conn.commit()
    r = offset + 25
    for i in range(offset, r):
        song_info = data[i]
        cur.execute('INSERT OR IGNORE INTO UKSpotify (id,song_name,genre_id) VALUES (?,?,?)', (i, song_info[0], song_info[1]))
        conn.commit()
    pass

def getCanadaGenreCounts(cur):
    '''Uses the cursor object to select all the genres from the Genres table in the database (music.db), and then selects the count of how many songs of each genre are in the CanadaSpotify table by joining the Genres and CanadaSpotify tables on the genre ids. Returns the count and name of each genre as a tuple in a list of tuples.'''
    l = []
    cur.execute('SELECT genre FROM Genres')
    x = cur.fetchall()
    for item in x:
        cur.execute('SELECT COUNT(genre_id) FROM CanadaSpotify JOIN Genres ON CanadaSpotify.genre_id = Genres.id WHERE Genres.genre = ?', (item[0], ))
        l.append((cur.fetchone()[0], item[0]))
    return l
    pass

def getUKGenreCounts(cur):
    '''Uses the cursor object to select all the genres from the Genres table in the database (music.db), and then selects the count of how many songs of each genre are in the UKSpotify table by joining the Genres and UKSpotify tables on the genre ids. Returns the count and name of each genre as a tuple in a list of tuples.'''
    l = []
    cur.execute('SELECT genre FROM Genres')
    x = cur.fetchall()
    for item in x:
        cur.execute('SELECT COUNT(genre_id) FROM UKSpotify JOIN Genres ON UKSpotify.genre_id = Genres.id WHERE Genres.genre = ?', (item[0], ))
        l.append((cur.fetchone()[0], item[0]))
    return l
    pass

def createPieChart(data, country):
    ''''''
    labels = []
    sizes = []
    total = 0
    for tup in data:
        labels.append(tup[1])
        total += tup[0]
    for tup in data:
        size = (tup[0]/total) * 360
        sizes.append(size)
    colors = ['green', 'orange', 'blue', 'red', 'yellow', 'pink', 'purple', 'gray', 'lightskyblue', 'lightcoral', 'yellowgreen']
    plt.pie(sizes, labels=labels, colors=colors)
    plt.axis('equal')
    plt.title(country)
    #plt.tight_layout()
    plt.show()
    pass

def main():
    ''''''
    #SETS UP THE DATABASE
    cur, conn = setUpDatabase('music.db')

    #SETS UP SPOTIPY
    cid = 'c2b8ee04a2a045a9bb74e3c7c3451b0a'
    secret = 'c82da9cec8804c83b96ffb0679ad280a'
    sp = createSpotipyObject(cid, secret)

    #CREATES GENRES TABLE
    genres = ['Rock', 'Pop', 'Hip Hop', 'Rap', 'R&B', 'Country', 'Alt', 'Classical', 'EDM', 'Jazz', 'Other']
    createGenresTable(genres, cur, conn)

    #COLLECT CANADA TOP 50 SONGS INFO
    canada_pid = "37i9dQZEVXbMda2apknTqH"
    canada_data = getPlaylistData(canada_pid, sp, cur)

    #COLLECT UK TOP 50 SONGS INFO
    uk_pid = '37i9dQZEVXbMwmF30ppw50'
    uk_data = getPlaylistData(uk_pid, sp, cur)

    #CREATE TABLE IN DATABASE AND ADD DATA 25 ITEMS AT A TIME (RUN CODE TWICE)
    try:
        cur.execute('SELECT * FROM CanadaSpotify')
        createCanadaTable(canada_data, cur, conn, 25)
    except:
        createCanadaTable(canada_data, cur, conn)
    try:
        cur.execute('SELECT * FROM UKSpotify')
        createUKTable(uk_data, cur, conn, 25)
    except:
        createUKTable(uk_data, cur, conn)

    #GET GENRE COUNTS FROM DATABASE
    canada_genres = getCanadaGenreCounts(cur)
    uk_genres = getUKGenreCounts(cur)

    #CREATE PIE CHARTS SHOWING PROPORTIONS OF EACH GENRE BY NUMBER OF SONGS
    createPieChart(canada_genres, 'Canada')
    #createPieChart(uk_genres)
    pass


if __name__ == '__main__':
    main()


#token = spotipy.oauth2.SpotifyClientCredentials(client_id='c2b8ee04a2a045a9bb74e3c7c3451b0a', client_secret='c82da9cec8804c83b96ffb0679ad280a')

#cache_token = token.get_access_token()
#spotify = spotipy.Spotify(cache_token) 
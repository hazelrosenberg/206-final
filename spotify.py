import requests
import sqlite3
import json
import os
import sys
import matplotlib
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

def createCanadaTable(data, offset, cur, conn):
    '''Creates CanadaSpotify table in the database (music.db) with the cursor and connection objects passed in as parameters. Takes the offset paramater (which is an integer) and adds 25 to it to create a range with a length of 25 to add 25 items at a time to the database. Loops through the items in the list (data) passed in as a parameter to add items to the database. Increases the offset by 25 and returns that number to use as a new offset when function is called again.'''
    cur.execute('CREATE TABLE IF NOT EXISTS CanadaSpotify (id INTEGER PRIMARY KEY, song_name TEXT UNIQUE, genre_id INTEGER)')
    conn.commit()
    r = offset + 25
    for i in range(offset, r):
        song_info = data[i]
        cur.execute('INSERT OR IGNORE INTO CanadaSpotify (id,song_name,genre_id) VALUES (?,?,?)', (i, song_info[0], song_info[1]))
        conn.commit()
    offset += 25
    return offset      
    pass

def get_song_ids():
    '''Takes spotipy object, user (spotify), playlist id, and limit (of how many tracks to return from playlist) and returns all of the track ids in a list.'''
    pass

def main():
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

    #CREATE TABLE IN DATABASE AND ADD DATA 
    offset = 0
    new_offset = createCanadaTable(canada_data, offset, cur, conn)
    createCanadaTable(canada_data, new_offset, cur, conn)


main()





#function to get list of ids of songs

#function to get genres of songs from ids

#function to put in DB

#token = spotipy.oauth2.SpotifyClientCredentials(client_id='c2b8ee04a2a045a9bb74e3c7c3451b0a', client_secret='c82da9cec8804c83b96ffb0679ad280a')

    #cache_token = token.get_access_token()
    #spotify = spotipy.Spotify(cache_token)

    
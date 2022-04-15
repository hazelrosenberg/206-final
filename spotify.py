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

def createCanadaTable(pid, sp, cur, conn):
    ''''''
    cur.execute('CREATE TABLE IF NOT EXISTS CanadaSpotify (id INTEGER PRIMARY KEY, song_name TEXT UNIQUE, genre_id INTEGER)')
    conn.commit()
    cur.execute('SELECT genre FROM Genres')
    genres = []
    for item in cur:
        genres.append(item[0])
    playlist_songs = sp.playlist_items(pid)
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
        print(song_genre)
            

    pass

def get_song_ids():
    '''Takes spotipy object, user (spotify), playlist id, and limit (of how many tracks to return from playlist) and returns all of the track ids in a list.'''
    pass


def main():
    #token = spotipy.oauth2.SpotifyClientCredentials(client_id='c2b8ee04a2a045a9bb74e3c7c3451b0a', client_secret='c82da9cec8804c83b96ffb0679ad280a')

    #cache_token = token.get_access_token()
    #spotify = spotipy.Spotify(cache_token)

    #SETS UP THE DATABASE
    cur, conn = setUpDatabase('music.db')

    #SETS UP SPOTIPY
    cid = 'c2b8ee04a2a045a9bb74e3c7c3451b0a'
    secret = 'c82da9cec8804c83b96ffb0679ad280a'
    sp = createSpotipyObject(cid, secret)

    #CREATES GENRES TABLE
    genres = ['Rock', 'Pop', 'Hip Hop', 'Rap', 'R&B', 'Country', 'Alt', 'Classical', 'EDM', 'Jazz', 'Other']
    createGenresTable(genres, cur, conn)

    #COLLECT CANADA TOP 50 SONGS INFO AND CREATE TABLE
    canada_pid = "37i9dQZEVXbMda2apknTqH"
    createCanadaTable(canada_pid, sp, cur, conn)


main()

#function to get list of ids of songs

#function to get genres of songs from ids

#function to put in DB

#client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret)
#sp = spotipy.Spotify(client_credentials_manager = client_credentials_manager)
#add token to the url, writing my version of the function here

#country_table = [['USA', '01'], ['Canada', '02']] #this is our country table we will use when we join tables later, I just wrote in random countries we may want to work with
'''should we use top 100 as our usa list? I do not think 
there is a billboard page specific to the usa.
we can come up with other countries and I can just rename the 
functions'''
#def spotify_100usa(tag, offset, cur):
 #   token = ??
  #  base_url = #FIND BASE URL THEN +TAG +END OF URL
   # bounds = {'limit': 25, 'offset': offset, 'access_token': token}
    #search = requests.get(base_url, params = bounds)
    #json1 = search.json()
    #for_db = []
    #loop through and put items we need  into a list

#maybe copy paste functions and do other countries?
#next: use the select join thing for the tables
#create visualizations
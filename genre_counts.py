import requests
import sqlite3
import os
import numpy as np
import matplotlib.pyplot as plt

def setUpDatabase(db_name):
    '''Connects to the database with the provided name (db_name).'''
    path = os.path.dirname(os.path.abspath(__file__))
    conn  = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()
    return cur, conn
def getBroadGenreCountsSpotify(cur):
    ''''''
    cur.execute('SELECT Genres.genre, COUNT(Spotify.broad_genre_id) FROM Genres JOIN Spotify ON Genres.id = Spotify.broad_genre_id GROUP BY Spotify.broad_genre_id')
    x = cur.fetchall()
    return x
def getBroadGenreCountsAppleMusic(cur):
    ''''''
    cur.execute('SELECT Genres.genre, COUNT(AppleMusic.broad_genre_id) FROM Genres JOIN AppleMusic ON Genres.id = AppleMusic.broad_genre_id GROUP BY AppleMusic.broad_genre_id')
    x = cur.fetchall()
    return x

def createBarChart(data, genres, title):
    names = []
    counts = []
    for item in data:
        names.append(item[0])
        counts.append(item[1])
    colors = ['#e6ff00', '#1b96c6', '#ff952a', '#61ff68', '#e258c3', '#71f7ff', '#8682e6', '#ff646a', '#00b5af', '#ffe65b', '#5dc480']
    plt.bar(names, counts, color = colors)
    plt.title(title, fontsize = 14, fontweight = 'bold')
    plt.xlabel('Genre Name')
    plt.ylabel('Number of SubGenres')
    plt.show()

#accepts something from a different function and a title'''

def main():
    cur, conn = setUpDatabase('music.db')

    spotify_genre_counts = getBroadGenreCountsSpotify(cur)
    
    applemusic_genre_counts = getBroadGenreCountsAppleMusic(cur)

    
    genres = ['Rock', 'Pop', 'Hip Hop', 'Rap', 'R&B', 'Country', 'Alt', 'Classical', 'EDM', 'Jazz', 'Other']
    title1 = 'Number of SubGenres per Genre (Spotify)'
    createBarChart(spotify_genre_counts, genres, title1)
    title2 = 'Number of SubGenres per Genre (Apple Music)'
    createBarChart(applemusic_genre_counts, genres, title2)

if __name__ == '__main__':
    main()

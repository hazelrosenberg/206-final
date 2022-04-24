import sqlite3
import os
import matplotlib.pyplot as plt
from textwrap import wrap
from numpy import False_
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import re

def setUpDatabase(db_name):
    '''Sets up the database with the provided name (db_name).'''
    path = os.path.dirname(os.path.abspath(__file__))
    conn  = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()
    return cur, conn
    pass

def createSpotipyObject(filename):
    '''Reads in text file with provided file name (filename) and creates spotipy object with client id and client secret (stored in text file).'''
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

def getPlaylistData(pid, sp):
    ''''''
    p_info = sp.playlist(pid)
    descrip = p_info['description']
    country = re.findall(' ([A-Za-z]+).', descrip)[5]
    playlist_songs = sp.playlist_items(pid)
    playlist_songs_info = []
    for song in playlist_songs['items']:
        song_name = song['track']['name']
        artist_id = song['track']['artists'][0]['id']
        artist_info = sp.artist(artist_id)
        song_genres = artist_info['genres']
        if len(song_genres) > 0:
            song_genre = song_genres[0]
        else:
            song_genre = 'Other'
        playlist_songs_info.append((song_name, song_genre, country))
    return playlist_songs_info
    pass

def createGenresTable(genres, cur, conn):
    '''Creates Genres table in the database with a given list of genres, database connection, and cursor.'''
    cur.execute('CREATE TABLE IF NOT EXISTS Genres (id INTEGER PRIMARY KEY, genre TEXT UNIQUE)')
    for i in range(len(genres)):
        cur.execute('INSERT OR IGNORE INTO Genres (id,genre) VALUES (?,?)', (i, genres[i]))
    conn.commit()
    pass

def createSpotifyGenresTable(cur, conn):
    ''''''
    cur.execute('CREATE TABLE IF NOT EXISTS SpotifyGenres (id INTEGER PRIMARY KEY, specific_genre TEXT UNIQUE, broad_genre_id INTEGER)')
    conn.commit()
    pass

def createCountriesTable(countries, cur, conn):
    '''Creates Countries table in the database with a given list of countries, database connection, and cursor.'''
    cur.execute('CREATE TABLE IF NOT EXISTS Countries (id INTEGER PRIMARY KEY, country TEXT UNIQUE)')
    for i in range(len(countries)): 
        cur.execute('INSERT OR IGNORE INTO Countries (id,country) VALUES (?,?)', (i, countries[i]))
    conn.commit()
    pass

def createSpotifyTable(cur, conn):
    ''''''
    cur.execute('CREATE TABLE IF NOT EXISTS Spotify (id INTEGER PRIMARY KEY, song_name TEXT, specific_genre_id INTEGER, broad_genre_id INTEGER, country_id INTEGER)')
    conn.commit()
    pass

def storeGenresData(data, cur, conn, offset):
    ''''''
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
        cur.execute('INSERT OR IGNORE INTO SpotifyGenres (id,specific_genre,broad_genre_id) VALUES (?,?,?)', (i, specific_genre, broad_genre_id))
    conn.commit()
    pass

def storeData(data, cur, conn, offset):
    ''''''
    r = offset + 25
    for i in range(offset, r):
        song_info = data[i]
        cur.execute('SELECT id FROM SpotifyGenres WHERE specific_genre=?', (song_info[1], ))
        specific_genre_id = cur.fetchall()[0][0]
        cur.execute('SELECT Genres.id FROM Genres JOIN SpotifyGenres ON Genres.id = SpotifyGenres.broad_genre_id WHERE SpotifyGenres.specific_genre=?', (song_info[1], ))
        broad_song_genre_id = cur.fetchall()[0][0]
        cur.execute('SELECT id FROM Countries WHERE country=?', (song_info[2], ))
        song_country_id = cur.fetchall()[0][0]
        cur.execute('INSERT OR IGNORE INTO Spotify (id, song_name, specific_genre_id, broad_genre_id, country_id) VALUES (?,?,?,?,?)', (i, song_info[0], specific_genre_id, broad_song_genre_id, song_country_id))
        conn.commit()
    pass

#def getCanadaGenreCounts(cur):
    '''Uses the cursor object to select all the genres from the Genres table in the database (music.db), and then selects the count of how many songs of each genre are in the CanadaSpotify table by joining the Genres and CanadaSpotify tables on the genre ids. Returns the count and name of each genre as a tuple in a list of tuples.'''
    #l = []
    #cur.execute('SELECT genre FROM Genres')
    #x = cur.fetchall()
    #for item in x:
        #cur.execute('SELECT COUNT(genre_id) FROM CanadaSpotify JOIN Genres ON CanadaSpotify.genre_id = Genres.id WHERE Genres.genre = ?', (item[0], ))
        #l.append((cur.fetchone()[0], item[0]))
    #return l
    #pass

#def getUSAGenreCounts(cur):
    '''Uses the cursor object to select all the genres from the Genres table in the database (music.db), and then selects the count of how many songs of each genre are in the USASpotify table by joining the Genres and USASpotify tables on the genre ids. Returns the count and name of each genre as a tuple in a list of tuples.'''
    #l = []
    #cur.execute('SELECT genre FROM Genres')
    #x = cur.fetchall()
    #for item in x:
        #cur.execute('SELECT COUNT(genre_id) FROM USASpotify JOIN Genres ON USASpotify.genre_id = Genres.id WHERE Genres.genre = ?', (item[0], ))
        #l.append((cur.fetchone()[0], item[0]))
    #return l
    #pass

#def getMexicoGenreCounts(cur):
    '''Uses the cursor object to select all the genres from the Genres table in the database (music.db), and then selects the count of how many songs of each genre are in the USASpotify table by joining the Genres and MexicoSpotify tables on the genre ids. Returns the count and name of each genre as a tuple in a list of tuples.'''
    #l = []
    #cur.execute('SELECT genre FROM Genres')
    #x = cur.fetchall()
    #for item in x:
        #cur.execute('SELECT COUNT(genre_id) FROM MexicoSpotify JOIN Genres ON MexicoSpotify.genre_id = Genres.id WHERE Genres.genre = ?', (item[0], ))
        #l.append((cur.fetchone()[0], item[0]))
    #return l
    #pass

#def writeCalculatedDataToFile(data, filename):
    '''Accepts list of tuples for a playlist that include each genre and the number of songs of that genre in the playlist (data), and a file name to write the calculations to (filename). Creates the file in the directory, named after the filename parameter. Performs calculations and writes them to the file, then closes the file.'''
    #dir = os.path.dirname(__file__)
    #outFile = open(os.path.join(dir, filename), 'w')
    #total = 0
    #for item in data:
        #total += item[0]
    #outFile.write('Genre,Number of Songs,Percent of Total')
    #for item in data:
        #perc = round((item[0] / total) * 100)
        #outFile.write('\n'+item[1]+','+str(item[0])+','+str(perc)+'%')
    #outFile.write('\n')
    #outFile.write('\nTotal Number of Songs: '+str(total))
    #outFile.close()
    #pass

#def createPieChart(data, title):
    '''Accepts a list of tuples for a playlist that include each genre and the number of songs of that genre in the playlist (data), and a title for the pie chart (title). Omits genres with 0 songs in the playlist from being included in the pie chart and makes a footnote of which genres had no songs. Creates a pie chart with the genres that had more than 0 songs.'''
    #data = sorted(data, reverse=True)
    #no_zeros = [i for i in data if i[0] != 0]
    #zeros = ', '.join([i[1] for i in data if i[0] == 0])
    #labels = []
    #sizes = []
    #total = 0
    #for tup in no_zeros:
        #labels.append(tup[1])
        #total += tup[0]
    #for tup in no_zeros:
        #size = (tup[0]/total) * 360
        #sizes.append(size)
    #colors = ['#e6ff00', '#1b96c6', '#ff952a', '#61ff68', '#e258c3', '#71f7ff', '#8682e6', '#ff646a', '#00b5af', '#ffe65b', '#5dc480']
    #plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', pctdistance=0.85, textprops={'fontsize': 12})
    #plt.axis('equal')
    #plt.title('\n'.join(wrap(title,60)), fontsize=14, fontweight='bold')
    #footnote = f'Genres with no songs in the top 50 this week: {zeros}'
    #plt.annotate(footnote, xy=(-0.1,-0.1), xycoords='axes fraction', fontsize=9)
    #plt.show()
    #pass


def main():
    ''''''
    #SETS UP THE DATABASE
    cur, conn = setUpDatabase('music.db')

    #SETS UP SPOTIPY
    secrets_file = 'secrets.txt'
    sp = createSpotipyObject(secrets_file)

    #CREATES GENRES TABLE (IF IT DOESN'T ALREADY EXIST)
    genres = ['Rock', 'Pop', 'Hip Hop', 'Rap', 'R&B', 'Country', 'Alt', 'Classical', 'EDM', 'Jazz', 'Other']
    createGenresTable(genres, cur, conn)

    #CREATE SPOTIFY GENRES TABLE (IF IT DOESN'T ALREADY EXIST)
    createSpotifyGenresTable(cur, conn)

    #CREATES COUNRIES TABLE (IF IT DOESN'T ALREADY EXIST)
    countries = ['Canada', 'USA', 'Mexico']
    createCountriesTable(countries, cur, conn)

    #COLLECT CANADA TOP 50 SONGS INFO
    canada_pid = "37i9dQZEVXbMda2apknTqH"
    canada_data = getPlaylistData(canada_pid, sp)

    #COLLECT USA TOP 50 SONGS INFO
    usa_pid = '37i9dQZEVXbLp5XoPON0wI'
    usa_data = getPlaylistData(usa_pid, sp)

    #COLLECT MEXICO TOP 50 SONGS INFO
    mexico_pid = '37i9dQZEVXbKUoIkUXteF6'
    mexico_data = getPlaylistData(mexico_pid, sp)

    #COMBINE DATA FROM CANADA, MEXICO, USA INTO ONE LIST TO STORE IN DATABASE
    all_data = canada_data + usa_data + mexico_data

    #CREATE SPOTIFY TABLE IN DATABASE
    createSpotifyTable(cur, conn)

    #ADD DATA 25 ITEMS AT A TIME (RUN CODE AT LEAST 12 TIMES)
    try:
        cur.execute('SELECT id FROM SpotifyGenres WHERE id = (SELECT MAX (id) FROM SpotifyGenres)')
        start = cur.fetchone()
        offset = start[0] + 1
    except:
        offset = 0
    try:
        storeGenresData(all_data, cur, conn, offset)
    except:
        cur.execute('SELECT * FROM Spotify')
        num_rows_s = len(cur.fetchall())
        if num_rows_s < len(all_data):
            try:
                cur.execute('SELECT id FROM Spotify WHERE id = (SELECT MAX (id) FROM Spotify)')
                start = cur.fetchone()
                offset = start[0] + 1
            except:
                offset = 0
            storeData(all_data, cur, conn, offset)

    #CREATE TABLE IN DATABASE AND ADD DATA 25 ITEMS AT A TIME (RUN CODE TWICE)
    #try:
        #cur.execute('SELECT * FROM CanadaSpotify')
        #createCanadaTable(canada_data, cur, conn, 25)
    #except:
        #createCanadaTable(canada_data, cur, conn)
    #try:
        #cur.execute('SELECT * FROM USASpotify')
        #createUSATable(usa_data, cur, conn, 25)
    #except:
        #createUSATable(usa_data, cur, conn)
    #try:
        #cur.execute('SELECT * FROM MexicoSpotify')
        #createMexicoTable(mexico_data, cur, conn, 25)
    #except:
        #createMexicoTable(mexico_data, cur, conn)

    #GET GENRE COUNTS FROM DATABASE
    #canada_genres = getCanadaGenreCounts(cur)
    #usa_genres = getUSAGenreCounts(cur)
    #mexico_genres = getMexicoGenreCounts(cur)

    #WRITE CALCULATED DATA TO TEXT FILES
    #c_title = 'spotifyCalculationsCanada.txt'
    #writeCalculatedDataToFile(canada_genres, c_title)
    #u_title = 'spotifyCalculationsUSA.txt'
    #writeCalculatedDataToFile(usa_genres, u_title)
    #m_title = 'spotifyCalculationsMexico.txt'
    #writeCalculatedDataToFile(canada_genres, m_title)

    #CREATE PIE CHARTS SHOWING PROPORTIONS OF EACH GENRE BY NUMBER OF SONGS
    #canada_title = 'Proportion of Genres of Top 50 Most Popular Songs in Canada on Spotify This Week'
    #createPieChart(canada_genres, canada_title)
    #usa_title = 'Proportion of Genres of Top 50 Most Popular Songs in the USA on Spotify This Week'
    #createPieChart(usa_genres, usa_title)
    #mexico_title = 'Proportion of Genres of Top 50 Most Popular Songs in Mexico on Spotify This Week'
    #createPieChart(mexico_genres, mexico_title)
    pass


if __name__ == '__main__':
    main()
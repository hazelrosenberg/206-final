import requests
import sqlite3
from bs4 import BeautifulSoup
import pandas as pd
import mysql.connector
#from cottage inn example in runestone for apple music usa charts
url = 'https://kworb.net/charts/apple_s/us.html'   
r = requests.get(url)
soup = BeautifulSoup(r.content, 'html.parser')
tags =soup.find_all('td', class_ = 'mp text')          
collect_info = []
for  tag in tags:
    info = tag.text
    collect_info.append(info)
    new_collect = []
    for item in collect_info:
        new_collect.extend(item.split(' - '))
        artist = new_collect[::2]
        song = new_collect[1::2]



#EXTRACT EACH STRING AND SPLIT WITH ' - '
#IN EACH OUTPUT, 0 INDEX IS THE ARTIST AND 1 INDEX IS THE SONG TITLE
#ONE WILL BE CALLED ARTIST AND THE OTHER CALLED SONG
#PRECEEDING CREATING DICTIONARY AND DATABASE
'''delimiter = ' - '
    new_collect = collect_info[0].split(delimiter)
    artist = new_collect[0]
    song = new_collect[1]
    #song = collect_info[1]
print(artist)   
print(song)'''

#after splitting up lists...
#UNCOMMENT AND THIS WILL CREATE SPREADSHEET WITH ALL DATA

usa_dictionary = {'song_title_usa': song, 'artist_name_usa': artist}
data_frame = pd.DataFrame(usa_dictionary)
to_csv =  data_frame.to_csv('/Users/sydneysella/billboard_usa_data.csv')

#UNCOMMENT AND THIS WILL SAVE ALL TO A DATABASE
'''db = mysql.connector.connect(user = 'hazels user name for the database', database = 'music')
cursor = db.cursor()'''
#insert and stuff, watch rest of video after database stuff is sorted










'''import requests
import sqlite3
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup
import os
import mysql.connector

def setUpDatabase(db_name):
    '''Sets up the database with the provided name (db_name).'''
    path = os.path.dirname(os.path.abspath(__file__))
    conn  = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()
    return cur, conn

def billboard_100canada(): #are we doing usa
    song_titlesca = []
    url = input('https://www.billboard.com/charts/canadian-hot-100/') #whatever url we will use 
    resp = requests.get(url)
    if resp.ok:
        soup= BeautifulSoup(resp.content, 'html.parser')
    titles = soup.find_all('h3', class_ = 'c-title a-no-trucate-a-font-primary-bold-s u-letter-spacing-0021 lrv-u-font-size-18@tablet lrv-u-font-size-16 u-line-height-125 u-line-height-normal@mobile-max a-truncate-ellipsis u-max-width-330 u-max-width-230@tablet-only')
    artists = soup.find_all('span', class_ = 'c-label a-no-trucate a-font-primary-s lrv-u-fofnt-size-14@mobile-max u-letter-spacing-0021 lrv-u-display-block a-truncate-ellpisis-2line u-max-width-330 u-max-width-230@tablet-only')
    for i in range(len(titles[:25])):
        title = titles[i].text.strip()
        artist = artists[i].text.strip()
        tuple1 = (title, artist)
        song_titlesca.append(tuple1)
    for i in range(len(titles[25:50])):
        title = titles[i].text.strip()
        artist = artists[i].text.strip()
        tuple1 = (title, artist)
        song_titlesca.append(tuple1)
    '''for i in range(len(titles[50:75])):
        title = titles[i].text.strip()
        artist = artists[i].text.strip()
        tuple1 = (title, artist)
        song_titlesca.append(tuple1)
    for i in range(len(titles[75:])):
        title = titles[i].text.strip()
        artist = artists[i].text.strip()
        tuple1 = (title, artist)
        song_titlesca.append(tuple1)'''
    '''for tag in tags[:25]:
        titles = tag.get()
        song_titles.append(titles)'''
    return song_titlesca

def billboard_100usa():
    song_titlesusa = []
    url = input('https://www.billboard.com/charts/the-billboard-hot-100/') #whatever url we will use 
    resp = requests.get(url)
    if resp.ok:
        soup= BeautifulSoup(resp.content, 'html.parser')
    titles = soup.find_all('h3', class_ = 'c-title a-no-trucate-a-font-primary-bold-s u-letter-spacing-0021 lrv-u-font-size-18@tablet lrv-u-font-size-16 u-line-height-125 u-line-height-normal@mobile-max a-truncate-ellipsis u-max-width-330 u-max-width-230@tablet-only')
    artists = soup.find_all('span', class_ = 'c-label a-no-trucate a-font-primary-s lrv-u-fofnt-size-14@mobile-max u-letter-spacing-0021 lrv-u-display-block a-truncate-ellpisis-2line u-max-width-330 u-max-width-230@tablet-only')
    for i in range(len(titles[:25])):
        title = titles[i].text.strip()
        artist = artists[i].text.strip()
        tuple1 = (title, artist)
        song_titlesusa.append(tuple1)
    for i in range(len(titles[25:50])):
        title = titles[i].text.strip()
        artist = artists[i].text.strip()
        tuple1 = (title, artist)
        song_titlesusa.append(tuple1)
    '''for i in range(len(titles[50:75])):
        title = titles[i].text.strip()
        artist = artists[i].text.strip()
        tuple1 = (title, artist)
        song_titlesuk.append(tuple1)
    for i in range(len(titles[75:])):
        title = titles[i].text.strip()
        artist = artists[i].text.strip()
        tuple1 = (title, artist)
        song_titlesuk.append(tuple1)'''
    return song_titlesusa#this will be what has all of the scraped data in it
def  create_cabb_table(data, cur, conn, offset=0):
    cur.execute('CREATE TABLE IF NOT EXISTS CanadaBBTable (id INTEGER PRIMARY KEY, bbsong_name TEXT UNIQUE, bbartist_name TEXT UNIQUE')
    conn.commit()
    r = offset + 25
    for i in range(offset, r):
        song_info = data[i]
        cur.execute('INSERT OR IGNORE INTO CanadaBBTable (id, bbsong_name, bbartist_name) VALUES (?,?,?)', (i, song_info[0], song_info[1]))
        conn.commit()
    pass
def create_usabb_table(data, cur, conn, offset=0):
    cur.execute('CREATE TABLE IF NOT EXISTS UsaBBTable (id INTEGER PRIMARY KEY, bbsong_nameusa TEXT UNIQUE, bbartist_nameusa TEXT UNIQUE')
    r = offset +  25
    for i in range(offset, r):
        song_info = data[i]
        cur.execute('INSERT OR IGNORE INTO UsaBBTable (id, bbsong_nameusa, bbartist_nameusa) VALUES (?,?,?)', (i, song_info[0], song_info[1]))
        conn.commit()
    pass
def add_genres(db_filename):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_filename)
    cur = conn.cursor()
    cur.execute('SELECT UsaBBTable.id from UsaBBTable JOIN Genres ')
    #somehow add genres to the table but make the songs the same?
   



def main():
    #sets up database
    cur, conn = setUpDatabase('bbmusic.db')
    
   

if __name__ == '__main__':
    main()'''

   
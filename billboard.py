import requests
import sqlite3
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup
import os


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


def bsDatabase():
    cur, conn = setUpDatabase('bbmusic.db')
    #CREATE DATABASE USING INSERT 
    '''conn = sqlite3.connect('your_database.sqlite3', check_same_thread=False)  #make a database in sqlite3 first?
    curs = conn.cursor()
    curs.execute("INSERT INTO your_table_name billboard='{}'".format(billboard))
    conn.commit()'''
   
import requests
import sqlite3
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup



def billboard_100canada(): #are we doing usa
    song_titlesca = []
    url = input('https://www.billboard.com/charts/canadian-hot-100/') #whatever url we will use 
    resp = requests.get(url)
    if resp.ok:
        soup= BeautifulSoup(resp.content, 'html.parser')
    titles = soup.find_all('a', class_ = 'c-title__link lrv-a-unstyle-link')
    artists = soup.find_all('p', class_ = 'c-tagline a-font-primary-l a-font-primary-m@mobile-max lrv-u-color-black u-color-white@mobile-max lrv-u-margin-tb-00 lrv-u-padding-t-025 lrv-u-margin-r-150')
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

def billboard_100japan():
    song_titlesjapan = []
    url = input('https://www.billboard.com/charts/japan-hot-100/') #whatever url we will use 
    resp = requests.get(url)
    if resp.ok:
        soup= BeautifulSoup(resp.content, 'html.parser')
    titles = soup.find_all('a', class_ = 'c-title__link lrv-a-unstyle-link')
    artists = soup.find_all('p', class_ = 'c-tagline a-font-primary-l a-font-primary-m@mobile-max lrv-u-color-black u-color-white@mobile-max lrv-u-margin-tb-00 lrv-u-padding-t-025 lrv-u-margin-r-150')
    for i in range(len(titles[:25])):
        title = titles[i].text.strip()
        artist = artists[i].text.strip()
        tuple1 = (title, artist)
        song_titlesjapan.append(tuple1)
    for i in range(len(titles[25:50])):
        title = titles[i].text.strip()
        artist = artists[i].text.strip()
        tuple1 = (title, artist)
        song_titlesjapan.append(tuple1)
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
    return song_titlesjapan#this will be what has all of the scraped data in it
    
def bsDatabase():
    #CREATE DATABASE USING INSERT 
    '''conn = sqlite3.connect('your_database.sqlite3', check_same_thread=False)  #make a database in sqlite3 first?
    curs = conn.cursor()
    curs.execute("INSERT INTO your_table_name billboard='{}'".format(billboard))
    conn.commit()'''
   
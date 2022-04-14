import requests
import sqlite3
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup



def billboard_100usa(): #are we doing usa
    url = input('') #whatever url we will use 
    r = requests.get('http://' + url)
    soup = BeautifulSoup(r.text, 'lxml')
    #look at project 2
    #come up with variables to  look for 
    #loop through tags and add to a list
    return billboard #this will be what has all of the scraped data in it

def bsDatabase():
    conn = sqlite3.connect('your_database.sqlite3', check_same_thread=False)  #make a database in sqlite3 first?
    curs = conn.cursor()
    curs.execute("INSERT INTO your_table_name billboard='{}'".format(billboard))
    conn.commit()
   
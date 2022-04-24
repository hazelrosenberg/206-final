from dataclasses import dataclass
import requests
import sqlite3
from bs4 import BeautifulSoup
import pandas as pd
import os
import matplotlib.pyplot as plt
from textwrap import wrap
import numpy as np
import json



#create new database with counts for pop and hiphop in all countries
#join databases for each country only joining genre id, genre name, country name, and country id
#get counts for pop and hip hop for each country
#plot
#x axis is country name, legend with genre, and y-axis is counts
#make a new table with columns for genre id, genre name, country name, country id
'''we will have to select both the pop and hiphop data from the countries, create table with all of these and make plot with countries next to each other'''

def setUpDatabase(db_name):
    '''Connects to the database with the provided name (db_name).'''
    path = os.path.dirname(os.path.abspath(__file__))
    conn  = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()
    return cur, conn

def createTable(cur, conn):
    cur.execute('CREATE TABLE IF NOT EXISTS PopandHipHop (genre_id INTEGER PRIMARY KEY, country_id INTEGER)')
    conn.commit()

def joinTable(cur, conn):
    cur.execute('SELECT Spotify.genre_id, Spotify.country_id FROM PopandHipHop JOIN Spotify ON Spotify.genre_id = PopandHipHop.genre_id AND Spotify.country_id = PopandHipHop.country_id')
    cur.fetchall()
    conn.commit()
    
#finish adding all to table somehow

'''def countsPop_usa(cur):
    cur.execute('SELECT COUNT(genre_id) FROM PopandHipHop WHERE genre_id = 1 AND country_id = 1')
    pop_count_usa = len(cur.fetchall())
    return pop_count_usa


def countsHipHop():
    


def add_USA(cur):
    cur.execute('SELECT ')

def add_usa(filename, cur, conn):

    #calculations file added number of songs, does this need to be coded?
        #write the name of variable in file and item[whatever its supposed to be in chart]
    cur.execute('INSERT INTO OR IGNORE INTO PopandHipHop (genre_id, genre_name, country_name, song_name) VALUES (?,?,?,?)', (''))
    conn.commit()

#def add_ca(cur, conn):

#def add_mexico(cur, conn):
    



def countPop(cur, conn):
    cur.execute('SELECT COUNTS (*) FROM PopandHipHop WHERE genre_id = 1 genre_id = 2')
    res = cur.fetchall()
    conn.commit()
    return res''' 

#def totalcounts():
 #   pop_tuple = [l, i, ]
  #  hiphop_tuple = []
#insert tuples into barchart graph

'''def countHipHop(cur, conn):
    cur.execute('SELECT COUNTS (*) FROM PopandHipHop WHERE genre_id = 2')'''


    
'''def createGroupedBarChart(, res):
    labels = 
    pop_counts = 
    hiphop_counts = 
    x = np.arrange(len(labels))
    width = 0.35
    fig, ax = plt.subplots()
    rects1 = ax.bar(x - width/2, pop_counts, width, label = 'Pop Counts')
    rects2 = ax.bar(x + width/2, hiphop_counts, width, label = 'Hip Hop Counts')
    ax.set_ylabel('Counts')  #should this be numbers?
    ax.set_title('Counts of Hip Hop and Pop By Country In North America')
    ax.set_xticks(x, labels)
    ax.legend()
    ax.bar_label(rects1, padding=3)
    ax.ar_label(rects2, padding=3)
    fig.tight_layout()
    plt.show()'''


    
    

def main():
    
    cur, conn = setUpDatabase('music.db')
    createTable(cur, conn)
    joinTable(cur, conn)

    #add_usa('appleMusicCalculationsUSA.txt', cur, conn)
    #PopandHipHopusa()
    #GET GENRE COUNTS FOR BOTH POP AND HIPHOP
    '''usa_pop_hiphop = PopandHipHopusa(cur)
   
   #WRITE DATA TO TEXT FILES
    usa_title = 'usaapplePopHipHop.txt'
    writeCalculatedDataToFile(usa_pop_hiphop, usa_title)

    #CREATE GROUPED BAR GRAPH
    title = 'Proportion of Pop to Hip Hop Songs In North America This Week'
    createGroupedBarChart(usa_pop_hiphop, title)'''



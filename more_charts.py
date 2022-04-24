import requests
import sqlite3
from bs4 import BeautifulSoup
import pandas as pd
import os
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import matplotlib.pyplot as plt
from textwrap import wrap
'''we will have to select both the pop and hiphop data from the countries, create table with all of these and make plot with countries next to each other'''

def PopandHipHopusa(cur):
    '''selects pop and hiphop from usa table and creates new table with this data'''
    try:
        cur.execute('SELECT * FROM UsaAppleMusic WHERE genre_id = "1", "2"')
    except:
        
    
def PopandHipHopCa(cur):

def PopandHipHopMex(cur):


def writeCalculatedDataToFile(data, filename):
    '''Accepts list of tuples for a playlist that include each genre and the number of songs of that genre in the playlist (data), and a file name to write the calculations to (filename). Creates the file in the directory, named after the filename parameter. Performs calculations and writes them to the file, then closes the file.'''
    dir = os.path.dirname(__file__)
    outFile = open(os.path.join(dir, filename), 'w')
    total = 0
    for item in data:
        total += item[0]
    outFile.write('Genre,Number of Songs,Percent of Total')
    for item in data:
        perc = round((item[0] / total) * 100)
        outFile.write('\n'+item[1]+','+str(item[0])+','+str(perc)+'%')
    outFile.write('\n')
    outFile.write('\nTotal Number of Songs: '+str(total))
    outFile.close()
    pass

def createGenreChart(data, title):
    data = sorted(data, reverse=True)
    no_zeros = [i for i in data if i[0] != 0]
    zeros = ', '.join([i[1] for i in data if i[0] == 0])
    labels = []
    sizes = []
    total = 0
    for tup in no_zeros:
        labels.append(tup[1])
        total += tup[0]
    for tup in no_zeros:
        size = (tup[0]/total) * 360
        sizes.append(size)
    plt.figure(figsize=(7,7))
    x = ['USA', 'Canada', 'Mexico']
    y1 = 
    y2 = 
    plt.bar(x, y1, color = '#1b96c6') #this is for pop, same color as pie
    plt.ar(x, y2, color = '#ff952a') #same but hiphop
    plt.title('\n'.join(wrap(title,60)), fontsize=14, fontweight='bold')
    plt.show()
    pass

def main():
    #GET GENRE COUNTS FOR BOTH POP AND HIPHOP
    usa_pop_hiphop = PopandHipHopusa(cur)
   
   #WRITE DATA TO TEXT FILES
    usa_title = 'usaapplePopHipHop.txt'
    writeCalculatedDataToFile(usa_pop_hiphop, usa_title)

    #CREATE STACKED BAR GRAPH
    us_title = 'Proportion of Pop to Hip Hop Songs In The USA This Week'
    createGenreChart(usa_pop_hiphop, us_title)



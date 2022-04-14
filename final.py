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
from tabulate import tabulate #dont forget pip install tabulate

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

cid = 'c2b8ee04a2a045a9bb74e3c7c3451b0a'
secret = 'c82da9cec8804c83b96ffb0679ad280a'

client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret)
sp = spotipy.Spotify(client_credentials_manager = client_credentials_manager)






#add token to the url, writing my version of the function here

country_table = [['USA', '01'], ['Canada', '02']] #this is our country table we will use when we join tables later, I just wrote in random countries we may want to work with
'''should we use top 100 as our usa list? I do not think 
there is a billboard page specific to the usa.
we can come up with other countries and I can just rename the 
functions'''
def spotify_100usa(tag, offset, cur):
    token = ??
    base_url = #FIND BASE URL THEN +TAG +END OF URL
    bounds = {'limit': 25, 'offset': offset, 'access_token': token}
    search = requests.get(base_url, params = bounds)
    json1 = search.json()
    for_db = []
    #loop through and put items we need  into a list

def setUpDatabase(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn  = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()
    return cur, conn


#maybe copy paste functions and do other countries?
#next: use the select join thing for the tables
#create visualizations

def main():
    cur,  conn  = setUpDatabase('spotify.db')

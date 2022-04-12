import sqlite3
import json
import os
import requests
import re

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

cid = 'c2b8ee04a2a045a9bb74e3c7c3451b0a'
secret = 'c82da9cec8804c83b96ffb0679ad280a'

client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret)
sp = spotipy.Spotify(client_credentials_manager = client_credentials_manager)
"""
This collection of functions scrapes metaScore and critic reviews
from a film's 'critic-reviews' page on the metacritic website.

Last Update: March, 2017
"""

# load packages - some might be obselete
import requests
from bs4 import BeautifulSoup
import re
import dateutil.parser
from string import ascii_uppercase
import pandas as pd
import time
import urllib.request
import csv
import requests

"""
Main file to scrape the critic review information for movies from metacritic

This file runs the scraper for one year, 'iYear' for all movies stored in a file
containing links to a metacritic webpage

Outputs:
    * Each movie has all critic reviews stored in XXX
    * the MetaScores for all movies are stored in a csv XXX

Expected Usage:
    called from a Makefile
    XXXXX
"""

import os
import time
import sys
from random import randint
import pandas as pd
import csv

# append the ROOT directory to the python path so it can search thru subdirs
sys.path.insert(0, os.getcwd())

from src.lib import processCriticReviews as metacritic

#Candidate years and release type
iYear = int(sys.argv[1])

# directory where the data will be stored
linkdir     = sys.argv[2]
datadirRoot = sys.argv[3]

# Loop over Links in a file
df_metaScore = pd.DataFrame()

linkFile = linkdir + './metacritic-links-' + str(iYear)

# this is iterable
with open(linkFile) as f:
    for row in csv.reader(f):
        currentURL = ''.join(row) # convert list to string
        movieID = currentURL.rsplit('/', 1)[-1].rsplit('.', 1)[0]
        targetURL = currentURL + '/critic-reviews'
        print('Now scraping', movieID)
        df_metaScore, df_movie = scrape_metaScorePage(targetURL, df_metaScore)

        # save critic reviews for this movie as a DataFrame
        df_movie.to_csv(datadirRoot + '/' + str(iYear) + '/' + \
                            movieID + '-reviews.csv', index = False)
        time.sleep(randint(5,15))

# package the metaScore table
if df_metaScore is not None:
    df_metaScore.columns = ["movieID", "title", "metaScore", "nReviews"]
    df_metaScore.to_csv(datadirRoot + '/metaScores/' + str(iYear) + \
                            '-metaScores.csv', index = False)
    print('saved metaScores to csv')

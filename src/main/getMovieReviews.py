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

from src.lib import processCriticReviews as critics

#Candidate years
yearStart = int(sys.argv[1])
yearEnd   = int(sys.argv[2])
relevantYears = range(yearStart,yearEnd+1)

# directory where the data will be stored
linkdir     = sys.argv[3]
datadirRoot = sys.argv[4]


for iYear in relevantYears:
    linkFile = linkdir + '/metacritic-links-' + str(iYear)
    df_metaScore = pd.DataFrame()
    # this is iterable
    with open(linkFile) as f:
        for row in csv.reader(f):
            currentURL = ''.join(row) # convert list to string
            movieID = currentURL.rsplit('/', 1)[-1].rsplit('.', 1)[0]
            targetURL = currentURL + '/critic-reviews'
            print('Now scraping', movieID)
            ##--- Scraper Start ---##
            #df_metaScore, df_movie = critics.scrape_metaScorePage(targetURL, df_metaScore)
            soup = critics.get_soup(targetURL)
            #print(soup)
            if soup is not None:
                try:
                    # get Meta Information
                    meta_Score, meta_nReview = critics.get_allMeta(soup, movieID)
                    title = critics.get_title(soup)

                    # append meta Information
                    df_temp = pd.DataFrame([[movieID, title, meta_Score, meta_nReview]])
                    df_metaScore = df_metaScore.append(df_temp, ignore_index=True)

                    # get critic information
                    if meta_nReview is not None:
                        df_movie = critics.get_allReviews(soup, meta_nReview, movieID, title)
                    print('Finished collecting reviews from', targetURL )

                    # pass back the updated
                    #return df_metaScore, df_movie
                except:
                    print('Cannot process', targetURL)
                    df_movie = pd.DataFrame()
                    #return df_metaScore, df_movie
            else:
                print('No soup for', targetURL)
                pass

            ##--- Scraper End ---##
            # save critic reviews for this movie as a DataFrame
            df_movie.to_csv(datadirRoot + '/movieReviews-' + str(iYear) + '/' + \
                                movieID + '-reviews.csv', index = False)
            time.sleep(randint(5,15))

    # package the metaScore table
    if df_metaScore is not None:
        df_metaScore.columns = ["movieID", "title", "metaScore", "nReviews"]
        df_metaScore.to_csv(datadirRoot + '/metaScores/' + str(iYear) + \
                                '-metaScores.csv', index = False)
        print('saved metaScores to csv')

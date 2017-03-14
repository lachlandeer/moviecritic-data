"""
This script harvests the links from MetaCritic that we will scrape data from.
Collection of links happens by year. So a typical output would be
2015-links.csv

It takes as inputs:
    1. The first year you want to scrape
    2. The last year you want to scrape
    3. The directory where the links will be saved to. Links saved as a csv

File produces a csv of links for each year.

Example usage:
    python getlinks.py 2010 2012 outputDirectory

"""

import os
import time
import sys

# append the ROOT directory to the python path so it can search thru subdirs
sys.path.insert(0, os.getcwd())

from src.lib import mcScrapeLinks as metacritic

# directory where the data will be stored
datadir = sys.argv[3]

# Candidate years
yearStart = int(sys.argv[1])
yearEnd   = int(sys.argv[2])
relevantYears = range(yearStart,yearEnd+1)


# Run scraper - Main loop
for iYear in relevantYears:
    print('Getting Links for', iYear)
    # Scrape the links
    links = metacritic.scrapeLinks(iYear)

    # write to csv
    writeLinksToCSV(iYear, link, datadir)

    print('pausing for two minutes before starting next year')
    time.sleep(120)

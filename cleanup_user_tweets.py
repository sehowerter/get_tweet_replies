#!/user/bin/env/python
import time
import os
import numpy as np
import re
import csv
import glob
import pandas as pd
from difflib import SequenceMatcher
import sys

### Cleaning up json files to take out tweets that have already been scraped

screenname = str(sys.argv[1])

origjson = open('jsons/'+screenname+'-tweets.json')
failjson = open('failedjsons/'+screenname+'-tweets.json')

# Getting the tweets we've completed:
actuallydone = pd.read_csv('ratios/{}-ratios.csv'.format(screenname))
actuallydone.index = actuallydone["Unnamed: 0"]
actuallydone = actuallydone.drop("Unnamed: 0",axis=1)
finishedtweets = list(actuallydone['tweet_id'])

# List we're cleaning up:
origjsonlist = []
for line in origjson:
    if line != "\n":
        origjsonlist.append(line)
alltweetids = []
for j in origjsonlist:
    tweetid = re.search('(?<=,\"id\": ).*(?=\})',str(j)).group(0)
    alltweetids.append(int(tweetid))

# Getting the tweets that failed so we don't revisit them:
failjsonlist = []
for line in failjson:
    if line != "\n":
        failjsonlist.append(line)
for i in failjsonlist:
    tweetid = = re.search('(?<=,\"id\": ).*(?=\})',str(i)).group(0)
    finishedtweets.append(tweetid)

# Getting a list of the tweets left to do:
left = [i for i in alltweetids if i not in finishedtweets]

os.system('mv jsons/{}-tweets.json done/'.format(screenname))

lefttodo = open('jsons/{}-tweets.json'.format(screenname),'a+')
i=0
for tweetid in left:
    for line in origjsonlist:
        if str(tweetid) in line:
            i+=1
            lefttodo.write(line)
lefttodo.close()
print(str(len(left))+' left for '+screenname)

convos = glob.glob('tweet_convos/{}/*'.format(screenname))

for c in convos:
    tweetid = re.search('\d{18}',str(c)).group(0)
    if int(tweetid) in left:
        os.system('mkdir dup_tweet_convos/{}'.format(screenname))
        os.system('mv {} dup_tweet_convos/{}'.format(c, screenname))
        print(tweetid+' has been scraped, but isnt in the ratio df, moving original convo to dup_tweet_convos/')

#!/user/bin/env/python
import time
import os
import numpy as np
import datetime as dt
import re
import csv
import glob
from labMTsimple.storyLab import *
import pandas as pd
import matplotlib.patches as mpatches
import collections
import matplotlib.pyplot as plt
plt.switch_backend('agg')
from matplotlib import rc
rc('font',**{'family':'serif','serif':['Palatino']})
rc('text', usetex=True)
from difflib import SequenceMatcher
import sys

# READING REPLY THREADS AND GETTING HAPPINESS FROM getreplies_selenium.py

labMT,labMTvector,labMTwordlist = emotionFileReader(stopval=1.0,lang='english',returnVector= True )

screenname = str(sys.argv[1])

all_convos = glob.glob('tweet_convos-noratio/{}/*convo*'.format(screenname))
# Example of filename: 2018-04-26_10_24-kanyewest-989555920186228736-tweet-588_5423_29105-convo-2018-04-27_11_03_56.txt

os.system('mkdir /Users/sarahhowerter/Drive/UVM/courses/COcoNuTs/PROJECT/getreplies/happ_vectors/{}/'.format(screenname))

try:
    ratiodf = pd.read_csv('ratios/{}-ratios.csv'.format(screenname))
    ratiodf = ratiodf.drop("Unnamed: 0",axis=1)
except:
    ratiodf = pd.DataFrame(columns=['tweet_id', 'likes', 'replies', 'retweets', 'tweet_date', 'scrape_date', 'url','happ_score','total_words','happ_words'])

numtweets = len(all_convos)
i=1

for convo in all_convos:
    convotxt = open(convo, 'r', encoding = 'utf-8')
    convotxt = convotxt.read().lower()
    print(convo)

    tweetid = re.search('\d{18}',str(convo)).group(0)

    ratiodf.loc[i,'tweet_id'] = tweetid
    ratiodf.loc[i,'url'] = 'http://twitter.com/{}/status/{}'.format(screenname,tweetid)
    ratiodf.loc[i,'tweet_date'] = re.search('(?<=/).*',convo[-115:]).group(0)[:10]
    print(ratiodf.loc[i,'tweet_date'])
    ratiodf.loc[i,'scrape_date'] = re.search('(?<=-tweetconvo-).*(?=.txt)',convo[-115:]).group(0)
    print(ratiodf.loc[i,'scrape_date'])
    ratio = re.search('(?<=-id-).*(?=-tweetconvo-)',convo).group(0)
    ratio = ratio.split('_')
    print(ratio)
    ratiodf.loc[i,'replies'] = ratio[0]
    ratiodf.loc[i,'retweets'] = ratio[1]
    ratiodf.loc[i,'likes'] = ratio[2]

    score, vector = emotion(str(convotxt),labMT,shift=True,happsList=labMTvector)

    ratiodf.loc[i, 'happ_score'] = score
    ratiodf.loc[i, 'total_words'] = len(convotxt.split())
    ratiodf.loc[i, 'happ_words'] = sum(vector)

    csvfile = 'happ_vectors/{}/{}-tweet-{}-happ_vec'.format(screenname, screenname,tweetid)
    with open(csvfile,'w') as output:
        writer= csv.writer(output, lineterminator='\n')
        for val in vector:
            writer.writerow([val])

    print('have happiness for the convo of tweet {} from {}'.format(tweetid, screenname))
    print('{} out of {} convos done'.format(i, numtweets))
    i += 1

ratiodf.to_csv('ratios/{}-ratios.csv'.format(screenname))

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

screenname = sys.argv[1]

all_convos = glob.glob('tweet_convos/{}/*convo*'.format(screenname))
# Example of filename: 2018-04-26_10_24-kanyewest-989555920186228736-tweet-588_5423_29105-convo-2018-04-27_11_03_56.txt

os.system('mkdir /Users/sarahhowerter/Drive/UVM/courses/COcoNuTs/PROJECT/getreplies/happ_vectors/{}/'.format(screenname))

ratiodf = pd.read_csv('ratios/{}-ratios.csv'.format(screenname))
ratiodf = ratiodf.drop("Unnamed: 0",axis=1)
ratiodf['happ_score'] = 0
ratiodf['total_words'] = 0
ratiodf['happ_words'] = 0

numtweets = len(all_convos)
i=1

for convo in all_convos:
    convotxt = open(convo, 'r', encoding = 'utf-8')
    convotxt = convotxt.read().lower()

    tweetid = re.search('\d{18}',str(convo)).group(0)

    score, vector = emotion(str(convotxt),labMT,shift=True,happsList=labMTvector)

    ratiodf.loc[ratiodf['tweet_id']==int(tweetid), 'happ_score'] = score
    ratiodf.loc[ratiodf['tweet_id']==int(tweetid), 'total_words'] = len(convotxt.split())
    ratiodf.loc[ratiodf['tweet_id']==int(tweetid), 'happ_words'] = sum(vector)

    csvfile = 'happ_vectors/{}/{}-tweet-{}-happ_vec'.format(screenname, screenname,tweetid)
    with open(csvfile,'w') as output:
        writer= csv.writer(output, lineterminator='\n')
        for val in vector:
            writer.writerow([val])

    print('have happiness for the convo of tweet {} from {}'.format(tweetid, screenname))
    print('{} out of {} convos done'.format(i, numtweets))
    i += 1

ratiodf.to_csv('ratios_w_happ/{}-ratios_w_happ.csv'.format(screenname))

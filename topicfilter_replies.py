#!/user/bin/env/python
import time
import os
import numpy as np
import re
import csv
import glob
import pandas as pd
from difflib import SequenceMatcher
import re
import sys

from labMTsimple.storyLab import *
labMT,labMTvector,labMTwordlist = emotionFileReader(stopval=1.0,lang='english',returnVector= True )


alltweetfiles = glob.glob('tweet_convos/GeorgeWBush__/*')

users = list(set([re.search('(?<=tweet_convos/).*(?=/)',file).group(0) for file in alltweetfiles]))

dfs = {u:pd.read_csv('ratios/{}-ratios.csv'.format(u)).drop("Unnamed: 0",axis=1) for u in users}
[os.system('mkdir /Users/sarahhowerter/Drive/UVM/courses/COcoNuTs/PROJECT/getreplies/sd_happ_vectors/{}/'.format(user)) for user in users]

alltweetdict = {u:{} for u in users}
tweetconvofiles = [file for file in alltweetfiles if 'convo-' in file]
tweetfiles = [f for f in alltweetfiles if '-tweet' in f and 'convo-' not in f and 'happ_vec' not in f]

for file in tweetfiles:
    user = re.search('(?<=tweet_convos/).*(?=/)',file).group(0)
    tweetid = re.search('(?<=-)\d{10,19}(?=-)',file).group(0)
    tweet = open(file, 'r', encoding = 'utf-8')
    tweet = tweet.read().lower()
    stopwords = tweet.split()
    for i,word in enumerate(stopwords):
        word = re.sub('"','',word)
        stopwords[i] = word
    alltweetdict[user][tweetid] = {'stopwords':stopwords}

numfiles = len(tweetconvofiles)
print('Rescoring ',numfiles,' tweets from ',user)
i=1
for file in tweetconvofiles:
    user = re.search('(?<=tweet_convos/).*(?=/)',file).group(0)
    tweetid = re.search('(?<=-)\d{10,19}(?=-)',file).group(0)

    ratiodf = dfs[user]

    tweetconvo = open(file, 'r', encoding = 'utf-8')
    tweetconvo = tweetconvo.read().lower()
    for word in alltweetdict[user][tweetid]['stopwords']:
        try:
            tweetconvo = re.sub(word,"",tweetconvo)
        except:
            print(word)

    score, vector =  emotion(str(tweetconvo),labMT,shift=True,happsList=labMTvector)

    print('The tweet: ',(" ").join(alltweetdict[user][tweetid]['stopwords']))
    print("^This tweet's original score was ",ratiodf.loc[ratiodf.tweet_id==int(tweetid), 'happ_score'].item(), " and its new happiness score is ",score)
    print('Total number of words in happiness scoring is ',sum(vector))

    ratiodf.loc[ratiodf.tweet_id==int(tweetid), 'sd_happ_score'] = score
    ratiodf.loc[ratiodf.tweet_id==int(tweetid), 'tweet'] = (" ").join(alltweetdict[user][tweetid]['stopwords'])

    csvfile = 'sd_happ_vectors/{}/{}-tweet-{}-sd_happ_vec'.format(user, user,tweetid)
    with open(csvfile,'w') as output:
        writer= csv.writer(output, lineterminator='\n')
        for val in vector:
            writer.writerow([val])
    dfs[user] = ratiodf
    print(i,' out of ',numfiles,' finished')
    i+=1

for user in list(dfs.keys()):
    dfs[user].to_csv('sd_ratios/{}-sd_ratios.csv'.format(user))

import csv
import json
import sys
import pandas as pd
import re
import os

senators = pd.read_csv('senators.csv',encoding='latin-1')

senators_dict = {}

for i in senators.index:
    try:
        senator_handle = re.search('(?<=/twitter.com/).*(?=/status/)', senators.loc[i,'url']).group(0)
        #print(senator_handle)
        senlist = senators_dict.get(senator_handle,[])
        tweet_id = re.search('(?<=status/).*',senators.loc[i,'url']).group(0)

        if senators.loc[i,'replies'] > 70:
            senlist.append(tweet_id)
        senators_dict[senator_handle] = senlist
    except:
        print(senators.loc[i,'url'])

for hand in list(senators_dict.keys()):
    os.system('rm jsons/{}-tweets.json'.format(hand))
    f = open('jsons/{}-tweets.json'.format(hand),'w')
    for tweet_id in senators_dict[hand]:
        print('{"user":{"screen_name": "%s"},"id": %s}\n'%(hand,tweet_id))
        f.write('{"user":{"screen_name": "%s"},"id": %s}\n'%(hand,tweet_id))
    f.close()

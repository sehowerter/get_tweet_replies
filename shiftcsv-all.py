# -*- coding: utf-8 -*-
import sys, os, subprocess
import pandas as pd
from labMTsimple.storyLab import *
#import storyLab
import codecs ## handle utf8
from datetime import timedelta, date
import numpy as np
import sys

#Download sum vec from hedonometer
#subprocess.call(['python3','gethappsum.py',startdate.strftime("%Y-%m-%d")])

user = re.search('(?<=happ_vectors/).*(?=/)',str(sys.argv[1])).group(0)
print(user)
tweetid = re.search('(?<=-tweet-).*(?=-happ_vec)',str(sys.argv[1])).group(0)
print(tweetid)

# Read in word frequency files and convert to lists
filename1 = str(sys.argv[1])
df1 = pd.read_csv(filename1,header=None)
Fvec1 = df1[0].tolist()

filename2 = 'happ_vectors/alltweet-happ_vec'
df2 = pd.read_csv(filename2,header=None)
Fvec2 = df2[0].tolist()

# Bring in happiness dictionary
labMT,labMTvector,labMTwordList = emotionFileReader(stopval=0.0,lang='english',returnVector=True)


# Run Andy's things to create word shift magic
saturdayStoppedVec = stopper(Fvec1,labMTvector,labMTwordList,stopVal=1.0)
tuesdayStoppedVec = stopper(Fvec2,labMTvector,labMTwordList,stopVal=1.0)


saturdayValence = emotionV(saturdayStoppedVec,labMTvector)
tuesdayValence = emotionV(tuesdayStoppedVec,labMTvector)




filename = "shift.html"
shiftHtml(labMTvector,labMTwordList,tuesdayStoppedVec,saturdayStoppedVec,filename)

#open html file
subprocess.call(['open','shift.html'])

os.system('mv shift.html wordshifts/1tweetconvo/{}-{}-shift.html'.format(user,tweetid))

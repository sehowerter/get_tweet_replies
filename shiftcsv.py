# -*- coding: utf-8 -*-
import sys, os, subprocess
import pandas as pd
from labMTsimple.storyLab import *
#import storyLab
import codecs ## handle utf8
from datetime import timedelta, date
import numpy as np
import os
import glob

alltweetvecs = glob.glob('happ_vectors/*/*')
alltweetvec = []
for v in alltweetvecs:
    df = pd.read_csv(v,header=None)
    Fvec = df[0].tolist()
    alltweetvec.append(np.array(Fvec))
alltweetvec = sum(alltweetvec)
alltweetvec = list(alltweetvec)

#Download sum vec from hedonometer
#subprocess.call(['python3','gethappsum.py',startdate.strftime("%Y-%m-%d")])

user = str(sys.argv[1])
tweetid = str(sys.argv[2])


# Read in word frequency files and convert to lists
filename = "getreplies/happ_vectors/{}/{}-tweet-{}-happ_vec".format(user,user,tweetid)
df = pd.read_csv(filename,header=None)
Fvec = df[0].tolist()




# Bring in happiness dictionary
labMT,labMTvector,labMTwordList = emotionFileReader(stopval=0.0,lang='english',returnVector=True)


# Run Andy's things to create word shift magic
ref_StoppedVec = stopper(alltweetvec,labMTvector,labMTwordList,stopVal=1.0)
comp_StoppedVec = stopper(Fvec,labMTvector,labMTwordList,stopVal=1.0)


ref_Valence = emotionV(ref_StoppedVec,labMTvector)
comp_Valence = emotionV(comp_StoppedVec,labMTvector)


filename = "shift.html"
shiftHtml(labMTvector,labMTwordList,ref_StoppedVec,comp_StoppedVec,filename)

#open html file
subprocess.call(['open','shift.html'])

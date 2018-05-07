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

alltweetfiles = glob.glob('tweet_convos/*/*')
users = [re.search('(?<=tweet_convos/).*(?=/',file).group(0) for file in alltweetfiles]
alltweetdict = {u:{} for u in users}
print(alltweetdict)
'''
for file in alltweetfiles:
    user = re.search('(?<=tweet_convos/).*(?=/\d{3})',file).group(0)
    tweetid = re.search('(?<=-)\d{10,19}(?=-id)',file).group(0)

'''

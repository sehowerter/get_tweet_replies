import re
import numpy as np
import glob
import os
import sys
import pandas as pd


jsons = glob.glob('jsons/*')

jusers = []
for j in jsons:
	jusers.append(re.search('(?<=jsons/).*(?=-)',j).group(0))

for user in jusers:
	try:
		userdf = pd.read_csv('ratios/{}-ratios.csv'.format(user))
		print('    ',len(list(userdf.index)),' tweets finished for ',user)
		os.system('wc jsons/{}-tweets.json'.format(user))
	except:
		print('There are no tweets finished for ',user)
		os.system('wc jsons/{}-tweets.json'.format(user))

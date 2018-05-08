import re
import numpy as np
import glob
import os
import sys
import pandas as pd

user = str(sys.argv[1])

jsons = glob.glob('jsons/*')

jusers = []
for j in jsons:
	jusers.append(re.search('(?<=jsons/).*(?=-)',j).group(0))

if user not in jusers:
	print('There are no jsons for this user, ',user)
else:
	try:
		userdf = pd.read_csv('ratios/{}-ratios.csv'.format(user))
		print('There are ',len(list(userdf.index))-1,' tweets finished for ',user)
	except:
		print('There are no tweets finished for ',user)	

import json
import sys
import pandas as pd
import re

senators = pd.read_csv("senators.csv")

for i in senators.index:
	senator_handle = re.search('(?<=/twitter.com/).*(?=/status/)',
	  senators.loc[i,'url']).group(0)
	print(senator_handle)

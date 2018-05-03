# -*- coding: utf-8 -*-
import sys, os, subprocess
import pandas as pd
import numpy as np
import os
import csv
import glob

alltweetvecs = glob.glob('happ_vectors/*/*')
alltweetvec = []
for v in alltweetvecs:
    df = pd.read_csv(v,header=None)
    Fvec = df[0].tolist()
    alltweetvec.append(np.array(Fvec))
alltweetvec = sum(alltweetvec)
alltweetvec = list(alltweetvec)


csvfile = 'happ_vectors/alltweet-happ_vec'
with open(csvfile,'w') as output:
    writer= csv.writer(output, lineterminator='\n')
    for val in alltweetvec:
        writer.writerow([val])

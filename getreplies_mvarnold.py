import numpy as np
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select
import os
import time
from time import strptime
import datetime as dt
import csv
import re
import sys
import pickle
import pandas as pd
from labMTsimple.storyLab import *
labMT,labMTvector,labMTwordlist = emotionFileReader(stopval=1.0,lang='english',returnVector= True )


def split(a, n):
    k, m = divmod(len(a), n)
    return (a[i * k + min(i, m):(i + 1) * k + min(i + 1, m)] for i in range(n))

jfile = open('jsons/'+str(sys.argv[1])+'-tweets.json')
jsons = []
for line in jfile:
    if line != "\n":
        jsons.append(line)
totaljsons = len(jsons)

numchunks = totaljsons//5
if totaljsons > 4:
    chunks = list(split(jsons, numchunks))
else:
    chunks = [jsons]
#print(chunks)
chunk = 0
numfailed = 0
t=1

for jsontweets in chunks:
    tweetdict = {}
    for i in jsontweets:
        screenname = re.search('(?<=:\s\")(.*)(?=\"},)',i).group(0)
        tweetid = re.search('(?<=\"id\":\s)(.*)(?=}\\n)',i).group(0)
        tweetlist = tweetdict.get(screenname,[])
        tweetlist.append(tweetid)
        tweetdict[screenname] = tweetlist

    failedtweets = []
    finishedtweets = []

    for screenname in list(tweetdict.keys()):
        tweets = tweetdict[screenname]
        ratiodict = {}
        ntweets = len(tweets)
        print('getting reply conversations for {} tweets by {}'.format(str(totaljsons),screenname))

        # Making file directories for screenname if they don't exist
        os.system('mkdir /Users/Winston/get_tweet_replies/screenshots/{}/'.format(screenname))
        os.system('mkdir /Users/Winston/get_tweet_replies/tweet_convos/{}/'.format(screenname))
        os.system('mkdir /Users/Winston/get_tweet_replies/happ_vectors/{}/'.format(screenname))


        for tweet in tweets:
            # Initiating the webdriver for selenium
            path_to_firefoxdriver = '/Users/Winston/get_tweet_replies/geckodriver' # change path as needed
            driver = webdriver.Firefox(executable_path = path_to_firefoxdriver)
            url = 'http://twitter.com/{}/status/{}'.format(screenname,tweet)

            try:
                driver.get(url) # opening tweet page & getting replies
                time.sleep(20)
                driver.get_screenshot_as_file("/screenshots/{}/tweet{}-{}.png".format(screenname, tweet, screenname))
            except:
                print('couldnt get tweet {} from {}; failed at start'.format(tweet,screenname))
                numfailed +=1
                failedtweets.append(tweet)
                continue

            # Get Tweet Date and Date of scrape for filename
            print(url)
            try: # All of these try except options are for identifying the location of the date object in the different page layouts on Twitter.
                date = driver.find_element_by_xpath('/html/body/div[30]/div[2]/div[3]/div/div/div[1]/div[1]/div/div[3]/div[1]/span') # .text format 10:49 AM - 26 Apr 2018
                date = str(date.text).split()
                timez = date[0].split(':')
                ampm = date[1]
                if ampm == "PM":
                    timez = str(12+int(timez[0]))+'_'+timez[1]
                else:
                    timez = str(int(timez[0])).zfill(2)+'_'+timez[1]
                day = int(date[3])
                month = strptime(date[4],'%b').tm_mon
                year = int(date[5])
            except:
                try:
                    date = driver.find_element_by_xpath('/html/body/div[30]/div[2]/div[3]/div/div/div[1]/div[1]/div/div[4]/div[1]/span') # .text format 10:49 AM - 26 Apr 2018
                    date = str(date.text).split()
                    timez = date[0].split(':')
                    ampm = date[1]
                    if ampm == "PM":
                        timez = str(12+int(timez[0]))+'_'+timez[1]
                    else:
                        timez = str(int(timez[0])).zfill(2)+'_'+timez[1]
                    day = int(date[3])
                    month = strptime(date[4],'%b').tm_mon
                    year = int(date[5])
                except:
                    try:
                        date = driver.find_element_by_xpath('/html/body/div[30]/div[2]/div[3]/div/div/div[1]/div[2]/div/div[3]/div[2]/span/span')
                        date = str(date.text).split()
                        timez = date[0].split(':')
                        ampm = date[1]
                        if ampm == "PM":
                            timez = str(12+int(timez[0]))+'_'+timez[1]
                        else:
                            timez = str(int(timez[0])).zfill(2)+'_'+timez[1]
                        day = int(date[3])
                        month = strptime(date[4],'%b').tm_mon
                        year = int(date[5])
                    except:
                        try:
                            date = driver.find_element_by_xpath('/html/body/div[30]/div[2]/div[3]/div/div/div[1]/div[1]/div/div[3]/div[2]/span/span')
                            date = str(date.text).split()
                            timez = date[0].split(':')
                            ampm = date[1]
                            if ampm == "PM":
                                timez = str(12+int(timez[0]))+'_'+timez[1]
                            else:
                                timez = str(int(timez[0])).zfill(2)+'_'+timez[1]
                            day = int(date[3])
                            month = strptime(date[4],'%b').tm_mon
                            year = int(date[5])
                        except:
                            print('couldnt get tweet {} from {}; failed in date'.format(tweet,screenname))
                            failedtweets.append(tweet)
                            numfailed +=1
                            driver.quit()
                            continue
            formatteddate = dt.date(year,month,day).isoformat()
            today = dt.datetime.now().strftime('%Y-%m-%d_%H_%M_%S')
            todaynotime = dt.datetime.now().strftime('%Y-%m-%d')


            # Get RATIO for filename
            try: # All of these try except options are for identifying the location of objects in the different page layouts on Twitter.
                replies = driver.find_element_by_xpath('/html/body/div[30]/div[2]/div[3]/div/div/div[1]/div[1]/div/div[4]/div[2]/div[1]/button')
            except:
                try:
                    replies = driver.find_element_by_xpath('/html/body/div[30]/div[2]/div[3]/div/div/div[1]/div[1]/div/div[5]/div[2]/div[1]/button')
                except:
                    try:
                        replies = driver.find_element_by_xpath('/html/body/div[30]/div[2]/div[3]/div/div/div[1]/div[2]/div/div[4]/div[2]/div[1]/button')
                    except:
                        try:
                            replies = driver.find_element_by_xpath('/html/body/div[30]/div[2]/div[3]/div/div/div[1]/div[1]/div/div[4]/div[2]/div[1]/button')
                        except:
                            print('couldnt get tweet {} from {}; failed in replies'.format(tweet,screenname))
                            failedtweets.append(tweet)
                            numfailed +=1
                            driver.quit()
                            continue
            try:
                replies = replies.text.split()[1]
            except:
                print('no replies for tweet {} from {}; failed in replies'.format(tweet,screenname))
                failedtweets.append(tweet)
                numfailed +=1
                driver.quit()
                continue
            try:
                if int(replies) < 10:
                    print('didnt get tweet {} from {}; because replies < 10'.format(tweet,screenname))
                    failedtweets.append(tweet)
                    numfailed +=1
                    driver.quit()
                    continue
            except:
                pass
            try:
                retweets = driver.find_element_by_xpath('/html/body/div[30]/div[2]/div[3]/div/div/div[1]/div[1]/div/div[3]/div[3]/ul/li[1]/a/strong')
            except:
                try:
                    retweets = driver.find_element_by_xpath('/html/body/div[30]/div[2]/div[3]/div/div/div[1]/div[1]/div/div[4]/div[3]/ul/li[1]/a/strong')
                except:
                    try:
                        retweets = driver.find_element_by_xpath('/html/body/div[30]/div[2]/div[3]/div/div/div[1]/div[2]/div/div[3]/div[4]/ul/li[1]/a/strong')
                    except:
                        try:
                            retweets = driver.find_element_by_xpath('/html/body/div[30]/div[2]/div[3]/div/div/div[1]/div[1]/div/div[3]/div[4]/ul/li[1]/a/strong')
                        except:
                            print('couldnt get tweet {} from {}; failed in retweets'.format(tweet,screenname))
                            failedtweets.append(tweet)
                            numfailed +=1
                            driver.quit()
                            continue
            retweets = re.sub(',','',retweets.text)
            try:
                likes = driver.find_element_by_xpath('/html/body/div[30]/div[2]/div[3]/div/div/div[1]/div[1]/div/div[3]/div[3]/ul/li[2]/a/strong')
            except:
                try:
                    likes = driver.find_element_by_xpath('/html/body/div[30]/div[2]/div[3]/div/div/div[1]/div[1]/div/div[4]/div[3]/ul/li[2]/a/strong')
                except:
                    try:
                        likes = driver.find_element_by_xpath('/html/body/div[30]/div[2]/div[3]/div/div/div[1]/div[2]/div/div[3]/div[4]/ul/li[2]/a/strong')
                    except:
                        try:
                            likes = driver.find_element_by_xpath('/html/body/div[30]/div[2]/div[3]/div/div/div[1]/div[1]/div/div[3]/div[4]/ul/li[2]/a/strong')
                        except:
                            print('couldnt get tweet {} from {}; failed in likes'.format(tweet,screenname))
                            failedtweets.append(tweet)
                            numfailed +=1
                            driver.quit()
                            continue
            likes = re.sub(',','',likes.text)


            # Setting file name and opening txt file for replies to print into
            filename = "{}_{}-{}-{}-id-{}_{}_{}-tweetconvo-{}.txt".format(formatteddate, timez, screenname, tweet,replies,retweets,likes,today)
            f = open("tweet_convos/{}/{}".format(screenname,filename),'a+')
            print('...')


            # Getting selenium to scroll to the end of the page
            elem = driver.find_element_by_css_selector('body')
            for i in range(16):
                elem.send_keys(Keys.END)
                timetowait = np.random.random_sample()*2 + 2
                time.sleep(timetowait)
            print('...')


            # Printing all replies to the txt file
            tweets = driver.find_elements_by_class_name('tweet-text')
            for reply in tweets[1:]:    # Printing out the reply thread
                # print(reply.text) # Uncomment if you want it to print replies to terminal
                f.write(reply.text+'\n')
            f.close()


            # Printing the original tweet to a separate txt file
            filename2 = "{}_{}-{}-{}-id-{}_{}_{}-tweet.txt".format(formatteddate, timez, screenname, tweet, replies,retweets,likes)
            f2 = open('tweet_convos/{}/{}'.format(screenname,filename2),'a+')
            f2.write(tweets[0].text)
            f2.close()


            # Getting Happiness score of the conversation
            convotxt = open("tweet_convos/{}/{}".format(screenname,filename),'r', encoding = 'utf-8')
            convotxt = convotxt.read().lower()
            score, vector = emotion(str(convotxt),labMT,shift=True,happsList=labMTvector)
            csvfile = 'happ_vectors/{}/{}-tweet-{}-happ_vec'.format(screenname, screenname,tweet)
            with open(csvfile,'w') as output:
                writer= csv.writer(output, lineterminator='\n')
                for val in vector:
                    writer.writerow([val])
            ratiodict[tweet] = {'tweet_id':tweet}
            ratiodict[tweet]['url']=url
            ratiodict[tweet]['tweet_date'] = formatteddate
            ratiodict[tweet]['scrape_date'] = today
            ratiodict[tweet]['replies'] = replies
            ratiodict[tweet]['retweets'] = retweets
            ratiodict[tweet]['likes'] = likes
            ratiodict[tweet]['happ_score'] = score
            ratiodict[tweet]['total_words'] = len(convotxt.split())
            ratiodict[tweet]['happ_words'] = sum(vector)
            print(ratiodict[tweet])

            # Waiting and then exiting tweet page
            #timetowait = np.random.random_sample() * 4 + 5
            #time.sleep(timetowait)
            driver.quit()
            timetowait = np.random.random_sample() * 4 + 2
            time.sleep(timetowait)
            finishedfile = open('finishedjsons/{}-tweets.json'.format(str(sys.argv[1])),'a+')
            fin = [line for line in jsontweets if tweet in line]
            finishedfile.write(fin[0])
            finishedfile.close()

            print('{} out of {} tweet convos read from {} and the happiness score was {}; also {} failed'.format(t,totaljsons,screenname, score,numfailed))
            pickle_out = open("pickles/ratiodict{}.pkl".format(screenname),"wb")
            pickle.dump(ratiodict, pickle_out)
            pickle_out.close()

            t+=1
        chunk += 1

        if len(failedtweets) > 0:
            failedfile = open('failedjsons/{}-failed-tweets.json'.format(str(sys.argv[1])),'a+')
            for tweetid in failedtweets:
                for line in jsontweets:
                    if tweetid in line:
                        failedfile.write(line)
            failedfile.close()
            print(str(numfailed)+' tweet convos failed, check failedjsons/ for the list.')
        else:
            print('all tweet convos in the set of {} were successful!'.format(ntweets))


        # Saving all tweet info (ratios, date, etc) to a csv dataframe)
            # (one per user handle)
        try:
            ratios = pd.read_csv('ratios/{}-ratios.csv'.format(screenname))
            ratios.index = ratios["Unnamed: 0"]
            ratios = ratios.drop("Unnamed: 0",axis=1)
            ratios2 = pd.DataFrame(ratiodict).transpose()
            ratios = pd.concat([ratios,ratios2])
            ratios.drop_duplicates()
        except:
            print('no previous ratios from this user')
            ratios = pd.DataFrame(ratiodict).transpose()
        ratios.to_csv('ratios/{}-ratios.csv'.format(screenname))


os.system('mv jsons/{}-tweets.json done/'.format(sys.argv[1]))

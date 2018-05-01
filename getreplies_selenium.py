import numpy as np
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select
import os
import time
from time import strptime
import datetime as dt
import re
import sys
import pandas as pd

jfile = open(sys.argv[1])
jsontweets = []
for line in jfile:
    jsontweets.append(line)
tweetdict = {}
for i in jsontweets:
    screenname = re.search('(?<=:\s\")(.*)(?=\"},)',i).group(0)
    tweetid = re.search('(?<=\"id\":\s)(.*)(?=}\\n)',i).group(0)
    tweetlist = tweetdict.get(screenname,[])
    tweetlist.append(tweetid)
    tweetdict[screenname] = tweetlist


for screenname in list(tweetdict.keys()):
    tweets = tweetdict[screenname]
    ratiodict = {}
    print('getting reply conversations for {} tweets by {}'.format(str(len(tweets)),screenname))
    for tweet in tweets:
        ratiodict[tweet] = {'tweet_id':tweet}
        # Initiating the webdriver for selenium
        path_to_firefoxdriver = '/Users/sarahhowerter/Drive/UVM/courses/COcoNuTs/PROJECT/getreplies/geckodriver' # change path as needed
        driver = webdriver.Firefox(executable_path = path_to_firefoxdriver)

        url = 'http://twitter.com/{}/status/{}'.format(screenname,tweet)
        ratiodict[tweet]['url']=url


        # Making file directories for screenname if they don't exist
        os.system('mkdir /Users/sarahhowerter/Drive/UVM/courses/COcoNuTs/PROJECT/getreplies/screenshots/{}/'.format(screenname))
        os.system('mkdir /Users/sarahhowerter/Drive/UVM/courses/COcoNuTs/PROJECT/getreplies/tweet_convos/{}/'.format(screenname))

        driver.get(url) # opening tweet page & getting replies
        time.sleep(20)
        driver.get_screenshot_as_file("/screenshots/{}/tweet{}-{}.png".format(screenname, tweet, screenname))


        # Get Tweet Date and Date of scrape for filename
        try:
            date = driver.find_element_by_xpath('/html/body/div[30]/div[2]/div[3]/div/div/div[1]/div[1]/div/div[3]/div[1]/span') # .text format 10:49 AM - 26 Apr 2018
        except:
            try:
                date = driver.find_element_by_xpath('/html/body/div[30]/div[2]/div[3]/div/div/div[1]/div[1]/div/div[4]/div[1]/span') # .text format 10:49 AM - 26 Apr 2018
            except:
                print('couldnt get tweet {} from {}'.format(tweet,screenname))
                continue
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
        formatteddate = dt.date(year,month,day).isoformat()
        today = dt.datetime.now().strftime('%Y-%m-%d_%H_%M_%S')
        todaynotime = dt.datetime.now().strftime('%Y-%m-%d')
        ratiodict[tweet]['tweet_date'] = formatteddate
        ratiodict[tweet]['scrape_date'] = today


        # Get RATIO for filename
        try:
            replies = driver.find_element_by_xpath('/html/body/div[30]/div[2]/div[3]/div/div/div[1]/div[1]/div/div[4]/div[2]/div[1]/button')
        except:
            try:
                replies = driver.find_element_by_xpath('/html/body/div[30]/div[2]/div[3]/div/div/div[1]/div[1]/div/div[5]/div[2]/div[1]/button')
            except:
                print('couldnt get tweet {} from {}'.format(tweet,screenname))
                continue
        replies = replies.text.split()[1]
        try:
            retweets = driver.find_element_by_xpath('/html/body/div[30]/div[2]/div[3]/div/div/div[1]/div[1]/div/div[3]/div[3]/ul/li[1]/a/strong')
        except:
            try:
                retweets = driver.find_element_by_xpath('/html/body/div[30]/div[2]/div[3]/div/div/div[1]/div[1]/div/div[4]/div[3]/ul/li[1]/a/strong')
            except:
                print('couldnt get tweet {} from {}'.format(tweet,screenname))
                continue
        retweets = re.sub(',','',retweets.text)
        try:
            likes = driver.find_element_by_xpath('/html/body/div[30]/div[2]/div[3]/div/div/div[1]/div[1]/div/div[3]/div[3]/ul/li[2]/a/strong')
        except:
            try:
                likes = driver.find_element_by_xpath('/html/body/div[30]/div[2]/div[3]/div/div/div[1]/div[1]/div/div[4]/div[3]/ul/li[2]/a/strong')
            except:
                print('couldnt get tweet {} from {}'.format(tweet,screenname))
                continue
        likes = re.sub(',','',likes.text)
        ratiodict[tweet]['replies'] = replies
        ratiodict[tweet]['retweets'] = retweets
        ratiodict[tweet]['likes'] = likes
        print(ratiodict[tweet])


        # Setting file name and opening txt file for replies to print into
        filename = "{}_{}-{}-{}-tweet-{}_{}_{}-convo-{}.txt".format(formatteddate, timez, screenname, tweet,replies,retweets,likes,today)
        f = open("tweet_convos/{}/{}".format(screenname,filename),'a+')


        # Getting selenium to scroll to the end of the page
        elem = driver.find_element_by_css_selector('body')
        for i in range(16):
            elem.send_keys(Keys.END)
            timetowait = np.random.random_sample()*2 + 2
            time.sleep(timetowait)


        # Printing all replies to the txt file
        tweets = driver.find_elements_by_class_name('tweet-text')
        for reply in tweets[1:]:    # Printing out the reply thread
            # print(reply.text) # Uncomment if you want it to print replies to terminal
            f.write(reply.text+'\n')
        f.close()


        # Printing the original tweet to a separate txt file
        filename2 = "{}_{}-{}-{}-tweet-{}_{}_{}.txt".format(formatteddate, timez, screenname, tweet, replies,retweets,likes)
        f2 = open('tweet_convos/{}/{}'.format(screenname,filename2),'a+')
        f2.write(tweets[0].text)
        f2.close()


        # Waiting and then exiting tweet page
        timetowait = np.random.random_sample() * 4 + 5
        time.sleep(timetowait)
        driver.quit()
        timetowait = np.random.random_sample() * 5 + 5
        time.sleep(timetowait)


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
        ratios = pd.DataFrame(ratiodict).transpose()
    ratios.to_csv('ratios/{}-ratios.csv'.format(screenname))

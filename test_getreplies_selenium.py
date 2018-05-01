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


path_to_firefoxdriver = '/Users/sarahhowerter/Drive/UVM/courses/COcoNuTs/PROJECT/getreplies/geckodriver' # change path as needed
driver = webdriver.Firefox(executable_path = path_to_firefoxdriver)

screenname = 'realDonaldTrump'
tweet = '988405962624118785'
url = 'http://twitter.com/{}/status/{}'.format(screenname,tweet)

#Making file directories for screenname if they don't exist
os.system('mkdir /Users/sarahhowerter/Drive/UVM/courses/COcoNuTs/PROJECT/getreplies/tests/tweet_convos/{}/'.format(screenname))

#opening tweet & getting replies
driver.get(url)
time.sleep(5)

#driver.find_element_by_xpath("""//*[@id="permalink-overlay-dialog"]/div[3]/div/div/div[1]/div[1]/div/div[4]/div[2]/div[1]/button/span""").click()
#driver.find_element_by_xpath("""//*[@id="signup-dialog-dialog"]/button/span""").click()
try:
    date = driver.find_element_by_xpath('/html/body/div[30]/div[2]/div[3]/div/div/div[1]/div[1]/div/div[3]/div[1]/span') # .text format 10:49 AM - 26 Apr 2018
except:
    try:
        date = driver.find_element_by_xpath('/html/body/div[30]/div[2]/div[3]/div/div/div[1]/div[1]/div/div[4]/div[1]/span') # .text format 10:49 AM - 26 Apr 2018
    except:
        print('couldnt get tweet {} from {}'.format(tweet,screenname))
        pass
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

# Get RATIO
replies = driver.find_element_by_xpath('/html/body/div[30]/div[2]/div[3]/div/div/div[1]/div[1]/div/div[4]/div[2]/div[1]/button')
replies = replies.text.split()[1]
print(replies)
retweets = driver.find_element_by_xpath('/html/body/div[30]/div[2]/div[3]/div/div/div[1]/div[1]/div/div[3]/div[3]/ul/li[1]/a/strong')
retweets = re.sub(',','',retweets.text)
print(retweets)
likes = driver.find_element_by_xpath('/html/body/div[30]/div[2]/div[3]/div/div/div[1]/div[1]/div/div[3]/div[3]/ul/li[2]/a/strong')
likes = re.sub(',','',likes.text)
print(likes)
'''
filename = "{}_{}-{}-{}-tweet-convo-{}.txt".format(formatteddate, timez, screenname, tweet, today)
f = open("tweet_convos/{}/{}".format(screenname,filename),'a+')


elem = driver.find_element_by_css_selector('body')
elem.click()

for i in range(15):
    ActionChains(driver).send_keys(Keys.END).perform()
    elem.send_keys(Keys.END)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(6)
tweets = driver.find_elements_by_class_name('tweet-text')
for tweet in tweets:
    print(tweet.text)
    f.write(tweet.text+'\n')
f.close()
'''
driver.quit()

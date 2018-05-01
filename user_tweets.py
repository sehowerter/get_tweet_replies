import tweepy
import json
import sys

ckey="Q3BuOCb6YpCcjxRLX80si7iaY"
csecret="8LmPPMK1j40QKn3jKzNP7MSGQXL90ZXfbHLtRbRR6d1mZKVQwe"
atoken="462603440-1WpphlO6HmRcVDZJjglIosJekSOmLLSQ2rkAC3b9"
asecret="4A2vZ2ioqwHJANDAHZTPFoKp9scbN9zTAnhlXbkLboZdZ"



auth = tweepy.OAuthHandler(ckey, csecret)
auth.set_access_token(atoken, asecret)

api = tweepy.API(auth)

screenname = str(sys.argv[1])

stuff = api.user_timeline(screen_name = screenname, count = 100, include_rts = True)


file = open('jsons/{}-tweets.json'.format(screenname), 'w')
for status in stuff:
	# Process a single status
	print('{"user":{"screen_name": "%s"},"id": %s}\n'%(screenname, status.id))
	file.write('{"user":{"screen_name": "%s"},"id": %s}\n'%(screenname, status.id))

file.close()

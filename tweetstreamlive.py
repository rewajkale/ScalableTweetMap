from elasticsearch import Elasticsearch
import tweepy
import time

#twitter application credentials 

consumer_key = 
consumer_secret = 
access_token = 
access_secret = 

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)

# Authentication
api = tweepy.API(auth)

# Add location
places = api.geo_search(query="United States", granularity="country")
place_id = places[0].id

es = Elasticsearch()

# Obtain the tweets and store into the ES

# Download 100 tweets

counter = 0
while counter < 5000:


	tweets = api.search(q="place:%s" % place_id, count = 100)
	for tweet in tweets:

		if not tweet.coordinates:
			continue

		tweet_dict = {}

		tweet_dict['id'] = tweet.id
		tweet_dict['text'] = tweet.text
		tweet_dict['user-name'] = tweet.user.name
		tweet_dict['user-id'] = tweet.user.id
		tweet_dict['hashtag'] = [ht['text'] for ht in tweet.entities['hashtags']]
		tweet_dict['coordinates'] = tweet.coordinates['coordinates']
		tweet_dict['place'] = ''
		tweet_dict['created-at'] = ''
		tweet_dict['retweet-count'] = tweet.retweet_count
		tweet_dict['favorite-count'] = tweet.favorite_count


		if tweet.place:
			tweet_dict['place'] = tweet.place.full_name

		if tweet.created_at:
			tweet_dict['created-at'] = tweet.created_at.strftime("%Y-%m-%d %H:%M:%S")

		print tweet.user.name

		es.index(index = 'twitter', doc_type = 'tweets', id = tweet.id, body = tweet_dict)
	
	time.sleep(10)
	
	print "=====", counter, "===="
	counter += len(tweets)

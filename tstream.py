# Important the necessary methods from tweepy library
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream 
from elasticsearch import Elasticsearch
import requests
import json


# Variables that contains the user credentials to access Twitter API
consumer_key = 
consumer_secret = 
access_token = 
access_secret = 


# This is a basic listener that just prints received tweets to stdout
class StdOutListener(StreamListener):

	def on_error(self, status):
		#print status
		pass
	
	def on_status(self, status):
		try:
			if status.coordinates:
				#print status
				tweet = {}
				tweet['user'] = status.user.screen_name
				tweet['text'] = status.text
				tweet['location'] = status.coordinates['coordinates']
				tweet['time'] = str(status.created_at)

				
				es.index(index = 'twitter', doc_type = 'tweet', body = {
				 	'user': tweet['user'],
				 	'text': tweet['text'],
					'location': tweet['location'],
					'time': tweet['time']
					})

			

				print tweet
		except Exception as e:
			print 'Error! {0}: {1}'.format(type(e), str(e))

if __name__ == '__main__':
	# Create elasticsearch instance
	es = Elasticsearch([{'host': 'localhost', 'port': 9200}])

	# This handles Twitter authetification and the connection to Twitter Streaming API
	l = StdOutListener()
	auth = OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_token, access_secret)
	stream = Stream(auth, l)

	stream.filter(track = ['music', 'burgers', 'pizza', 'Facebook', 'Amazon', 'Google', 'Los Angeles', 'Columbia', 'New York'])

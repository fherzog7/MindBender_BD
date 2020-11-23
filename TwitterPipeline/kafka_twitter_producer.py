from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from kafka import SimpleProducer, KafkaClient

ACCESS_TOKEN = "1322200244378021888-gL3dJDFpEEEgxY8T8owFt9Ljg93cpc"
TOKEN_SECRET = "3qkr7Ja2FIHUe8CyqrDZzwxIwiRJtonm0vzvYNowZc18T"
CONSUMER_KEY = "1d8dKVs3MapbF60bhfU5DXiOv"
CONSUMER_SECRET = "UUy9rk5oL4oTXiw7SXVP6f2jbspxmGg4fwW0HcIWjCrOtMgWLL"
TOPIC = "tweets"

class StdOutListener(StreamListener):
	def on_data(self, data):
		producer.send_messages(TOPIC, data.encode('utf-8'))
		print (data)
		return True
	def on_error(self, status):
		print (status)

kafka = KafkaClient("localhost:9099")
producer = SimpleProducer(kafka)
l = StdOutListener()
auth = OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, TOKEN_SECRET)
stream = Stream(auth, l)
stream.filter(track=TOPIC)

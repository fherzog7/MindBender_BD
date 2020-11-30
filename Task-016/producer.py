from kafka import SimpleProducer, KafkaClient
from requests import request 
from time import sleep 

def makeUrls(ids):
	urls = []
	for coin in ids:
		urls.append("https://coinranking1.p.rapidapi.com/coin/"+str(ids[coin]))
	return urls

def getApi_Key(keys):
	with open(keys) as f:
		key = f.readline().rstrip()
	return key

TOPIC = "cointest"
SERVER = "sandbox-hdp.hortonworks.com:6667"
keys_path = "keys.txt"
all_coins_summary = "https://coinranking1.p.rapidapi.com/coins"
RUNNING = True
identifiers = {'btc':1, 'eth':2, 'litecoin':7}

urls = makeUrls(identifiers)
api_key = getApi_Key(keys_path)

kafka = KafkaClient(SERVER)
producer = SimpleProducer(kafka)

headers = {
    'x-rapidapi-key': api_key,
    'x-rapidapi-host': "coinranking1.p.rapidapi.com"
    }

while RUNNING:
	for url in urls:
		resp = request("GET", url, headers=headers).text
		#print(resp)
		producer.send_messages(TOPIC, resp.encode('utf-8'))
		sleep(2)	
	sleep(10)



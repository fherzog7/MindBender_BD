from kafka import KafkaProducer
from requests import request 
from time import sleep 

def makeUrls(ids):
	urls = []
	for coin in ids:
		urls.append("https://coinranking1.p.rapidapi.com/coin/"+str(ids[coin]))
	return urls

def getApi_Key(keys):
	with open(keys) as f:
		return f.readline().rstrip()

TOPIC = "cointest"
#Sandbox
SERVER0 = "sandbox-hdp.hortonworks.com:6667"
#Local
SERVER1 = "localhost:9099"
#Multiple Brokers
BROKERS = ["localhost:9092","localhost:9093", "localhost:9094"]
keys_path = "keys.txt"
all_coins_summary = "https://coinranking1.p.rapidapi.com/coins"
RUNNING = True
identifiers = {'btc':1, 'eth':2, 'litecoin':7}

urls = makeUrls(identifiers)
api_key = getApi_Key(keys_path)

producer = KafkaProducer(bootstrap_servers = BROKERS)

headers = {
    'x-rapidapi-key': api_key,
    'x-rapidapi-host': "coinranking1.p.rapidapi.com"
    }

while RUNNING:
	for url in urls:
		resp = request("GET", url, headers=headers).text
		#print(resp)
		producer.send(TOPIC, resp.encode('utf-8'))
		sleep(3)	
	sleep(10)



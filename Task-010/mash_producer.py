from kafka import SimpleProducer, KafkaClient
import requests

TOPIC = "rentals"

url = "https://mashvisor-api.p.rapidapi.com/airbnb-property/active-listings"

querystring = {"state":"GA","page":"3","city":"Atlanta","items":"5"}

headers = {
    'x-rapidapi-key': "96ad9f7179msh73f50c9342c17e4p126cf0jsn4eba9eefe58d",
    'x-rapidapi-host': "mashvisor-api.p.rapidapi.com"
    }

response = requests.request("GET", url, headers=headers, params=querystring)
text = response.text

kafka = KafkaClient("localhost:9099")
producer = SimpleProducer(kafka)

producer.send_messages(TOPIC, text.encode('utf-8'))




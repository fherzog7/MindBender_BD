#!/bin/bash
zookeeper-server-start.sh -daemon /home/eit/opt/kafka_2.3.1/config/zookeeper.properties

kafka-server-start.sh -daemon /home/eit/opt/kafka_2.3.1/config/server_1.properties

kafka-server-start.sh -daemon /home/eit/opt/kafka_2.3.1/config/server_2.properties

kafka-server-start.sh -daemon /home/eit/opt/kafka_2.3.1/config/server_3.properties

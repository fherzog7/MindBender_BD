#!/bin/bash

cd ~

echo Preparing to install Java and Hadoop...
sudo apt-get update

#Make opt
mkdir -p opt

hd=$(hadoop version)
jv=$(java -version)

if [[ "$jv" == *"java"* ]]; then
	echo Java is already installed.
else
	bash ./java_inst.sh
fi


if [[ "$h" == *"Hadoop 2.7.3"* ]]; then
	echo Hadoop is already installed
else
	bash ./hadoop_inst.sh
fi

cd ~

echo "source .bash_profile" >> .bashrc
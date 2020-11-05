#!/bin/bash

cd ~

echo Preparing to install Java and Hadoop...
sudo apt-get update

#Make opt
mkdir -p opt

#Check for hadoop / java versions.
hd=$(hadoop version)
jv=$(java -version)

#Check if java / hadoop installed
#If not installed, run the installation scripts.
if [[ "$jv" == *"java"* ]]; then
	echo Java is already installed
else
	bash ./java_inst.sh
fi


if [[ "$h" == *"Hadoop 2.7.3"* ]]; then
	echo Hadoop is already installed
else
	bash ./hadoop_inst.sh
fi

#Go Home
cd ~

#Add source to .bashrc
echo "source .bash_profile" >> .bashrc
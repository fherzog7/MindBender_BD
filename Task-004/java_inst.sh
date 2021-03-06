#!/bin/bash

#Go Home
cd ~

#Update
sudo apt-get update 

#Make opt
mkdir -p opt
cd opt

#Download and unpack
wget -O jdk-8u221-linux-x64.tar.gz \
-c --content-disposition \
"https://javadl.oracle.com/webapps/download/AutoDL?BundleId=239835_230deb18db3e4014bb8e3e8324f81b43"

tar -zxvf jdk-8u221-linux-x64.tar.gz
rm jdk-8u221-linux-x64.tar.gz

#Go Home
cd ~

#Check if .bash_profile exists,
#if not, create it.
if [ ! -f ".bash_profile" ]; then
	touch .bash_profile
fi

#Set Path
echo "JAVA_HOME=~/opt/jdk1.8.0_221" >> .bash_profile
echo "export PATH=$PATH:$JAVA_HOME/bin" >> .bash_profile

#Source
source .bash_profile
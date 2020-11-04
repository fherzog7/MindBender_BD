#! usr/bin/bash

###procs=$(jps | cut -d' ' -f2)

output=$(jps)

if [[ "$output" == *"ResourceManager"* ]]; then
	echo Hadoop already running..!
else 
	echo Hadoop not running..!
	eval start-all.sh
fi
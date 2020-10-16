#!/bin/bash 

filename='commits_to_cherry_pick'
count=0
echo '' > commits_finished
while read line; do
        git cherry-pick $line
	#echo $line
	let "count+=1"
	echo $count
	sleep 5
	echo "$line" >> commits_finished
done < $filename

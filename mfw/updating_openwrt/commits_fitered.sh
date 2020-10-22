#!/bin/bash 

while read line; do 
	subject=`awk -F ':' '{ print $2 }' <<< $line`
	git_output=`grep "$subject" 19-log`
	if [ $? != 0 ]; then
		echo $line
	fi
done < git_log_committers

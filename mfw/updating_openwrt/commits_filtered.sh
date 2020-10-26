#!/bin/bash 

#Determine if commits we have committed are in the git log of the branch we're mering with
while read line; do 
	subject=`awk -F ':' '{ print $2 }' <<< $line`
	git_output=`grep "$subject" 19-log`
	if [ $? != 0 ]; then
		echo $line
	fi
done < git_log_committers

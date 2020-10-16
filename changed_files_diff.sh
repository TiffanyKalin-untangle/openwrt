#!/bin/bash

while read line; do
	output=`diff $line ../openwrt/$line`
	if [ $? -ne 0 ]; then
		echo $line
	fi


done < changed_files

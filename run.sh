#! /bin/bash

pushd ~/Documents/TightVNC/

ip_address=$(sudo nmap -sP -PS22 192.168.1.1/24 | grep -i "raspberrydry" | egrep -o [0-9]+\.[0-9]+\.[0-9]+\.[0-9]+)

if [[ ${ip_address} =~ [0-9]+\.[0-9]+\.[0-9]+\.[0-9]+ ]]
then
	java -jar tightvnc-jviewer.jar ${ip_address}:5901
else
	echo “No IP Address Found for RaspberryDry.”
fi

popd
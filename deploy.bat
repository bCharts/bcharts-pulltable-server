@echo off
bluemix api https://api.ng.bluemix.net
bluemix login -u bruceprk@hotmail.com -p pk1020329 -o "saeed@ca.ibm.com" -s "dev"
cf push "bcharts_dev"
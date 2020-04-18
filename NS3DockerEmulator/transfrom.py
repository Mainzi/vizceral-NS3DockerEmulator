from scapy.all import *
# from prettytable import PrettyTable
from collections import Counter
import os, sys
import json
from time import sleep, time
import argparse
 
 
def createParser ():
    parser = argparse.ArgumentParser()
    parser.add_argument ('-t', '--time', default=300, type=int)
    parser.add_argument ('-p', '--period', default=100, type=int)
    parser.add_argument ('-s', '--sleep', default=60, type=int)
    return parser

parser = createParser()
namespace = parser.parse_args(sys.argv[1:])

# wait until the container network starts
sleep(namespace.sleep)

# folder with logs from containers
rootdir = '../NS3DockerEmulator/var/log'

for i in range(namespace.time / namespace.period + 1):

	sleep(namespace.period)

	print(str((i+1) * namespace.period) + " seconds")
	
	visceral_data = {
						"renderer": "region",
	  					"name": "WiFi",
	  					"nodes": [],
	  					"connections": [],
	  					"updated": time(),
	  				}

	for subdir, dirs, files in os.walk(rootdir):
		pcap_filename = None
		current_ip = None

		# open logs for extract IP
		current_time = time()
		log_file = os.path.join(subdir, 'treesip.log')
		try:
			with open(log_file, 'r') as fp:
			   line = fp.readline()
			   while line:
			       if line.find("IP: ") != -1:
			       		current_ip = line[line.find("IP: ") + 4:].rstrip()
			       		# print("Current IP: " + current_ip)
			       		break
			       line = fp.readline()
		except:
			continue

		if current_ip is None:
			continue
			
		visceral_data["nodes"].append({       
										"renderer": "focusedChild",
										"name": current_ip,
										"class": "normal",
										"updated": current_time,
										"nodes": [],
										"connections": []
										})	


		# Extracting infotmation about  traffic
		for file in files:
			if file[-4:] == "pcap":
				pcap_filename = os.path.join(subdir, file)

		if pcap_filename is None:
			continue

		# open current pcap file
		packets = rdpcap(pcap_filename)

		# Let's iterate through every packet
		srcIP=[]
		for pkt in packets:
			if IP in pkt:
			    try:
			      srcIP.append(pkt[IP].src)
			    except:
			      pass

		# Count IP.source
		cnt=Counter()

		for ip in srcIP:
		  	cnt[ip] += 1


		recieved_packets = 0

		# writing information into json
		# table= PrettyTable(["IP", "Count"])
		for ip, count in cnt.most_common():
		  	# table.add_row([ip, count])
		  	if ip == current_ip:
		  		continue
		  	recieved_packets += count
			visceral_data["connections"].append({
												"source": ip,
												"target": current_ip,
												"metrics": {
													# "danger": 1.1,
													"normal": count,
													# "warning": 1.3
													},
												"class": "normal"
												})
		# print(table)

	# save new data every period
	visceral_data = {
						"renderer": "global",
	  					"name": "INTERNET",
	  					"nodes": [visceral_data],
	  					"connections": []
	  				}

	# need to update the data in realtime
	with open(os.path.join("../vizceral/dist", "data.json"), 'w') as f:
	    json.dump(visceral_data, f)

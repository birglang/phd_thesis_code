

'''

This program Continuously verify Flows 

This program is working successfullyis
TO run the program:
	sudo python3 Agent_Continuous_Verification.py



'''

##########################################################
	#    Agent for all the switches
##########################################################
# The program is for Agent.
# This program monitors the OpenFlow rules installed at the switches
# at the interval of 5 seconds.

# The Agent extracts the Flow rules stored on the blockchain and
# compares it with the flows from switches.

import os
import time
from web3 import Web3
import json
import requests

import colorama
from colorama import Fore

class Agent():
	
	def __init__(self):

		self.SWITCH_LIST = []
		self.FLOW_RULE = {}

		'''
		structure Global_Flow_table
		SWITCH_ID 	SRC_MAC		DST_MAC		OUTPORT
		'''
		self.Global_Flow_Table = {}

		self.Global_Flow_Count = 0
		self.start_time = 0

		##############
		# Infected Switch
		self.InfectedSwitch = {}

		#connection with the blockchain and contract
		###################################################
		print("######################################################")
		print("		Connection with Blockchain")
		print("######################################################")
		print("")

		ganache_url = "http://127.0.0.1:8545"
		web3 = Web3(Web3.HTTPProvider(ganache_url))
		print('Connection Status : ', web3.isConnected())
		web3.eth.defaultAccount = web3.eth.accounts[0]
		print(web3.eth.accounts[0])

		with open('abi.json') as f:
			abi = json.load(f)
		
		address = web3.toChecksumAddress("0x1Edf1227061c536b16Eb23d032b73dB204d2dde0")
		self.contract = web3.eth.contract(address = address, abi = abi)

		print("######################################################")
		print("")
		###################################################
	
	def Call_Verify_Flow_Table(self, SWITCH_ID, Rule_ID, IN_PORT, SRC_MAC, DST_MAC, PRIORITY, OUT_PORT):
		#self.Global_Flow_Table.setdefault(SWITCH_ID, {}).setdefault(SRC_MAC, {}).setdefault(DST_MAC, [])

		#self.Global_Flow_Table[SRC_MAC][DST_MAC].append(IN_PORT)
		#self.Global_Flow_Table[SWITCH_ID][SRC_MAC][DST_MAC].append(OUT_PORT)

		#print("Adding Flow Rule for the First time")

		
		######################################################
		#    Call verifyFlowRules function in Smart Contract
		######################################################

		
		
		
		#print("")
		#print("Rules from Blockchain")
		#print("Rule_ID      SRC             DST            PRIORITY 	OUTPORT")

		status = self.contract.functions.verifyFlowRules(SWITCH_ID, str(IN_PORT), SRC_MAC, DST_MAC, PRIORITY ,OUT_PORT).call()
		print("status: ", status)
		
		PRIORITY = int(PRIORITY)
		OUT_PORT = int(OUT_PORT)
		rule = self.contract.functions.getRules(SWITCH_ID, Rule_ID).call()
		#print(rule[1])

		if status == 5:
			print("")
			print("Verification Successful...")
		else:
			print("")
			print("Verification Failed !!!")
			print("")

			# Delete Rules:
			headers = {
    			'Content-Type': 'application/x-www-form-urlencoded',
			}

			data = '{\n    "dpid": %d,\n    "table_id": 0,\n    "priority": %d,\n    "match":{\n        "dl_src":"%s",\n        "dl_dst":"%s"\n\n    },\n    "actions":[\n        {\n            "type":"OUTPUT",\n            "port": %d\n        }\n    ]\n }' % (SWITCH_ID, PRIORITY, SRC_MAC, DST_MAC, OUT_PORT)

			print("Removing Infected Flow")
			response = requests.post('http://localhost:8080/stats/flowentry/delete', headers=headers, data=data)
			print(response)
			print("Removed Successfully")

			# Install New Rules from Blockchain
			print("Installing New Flow")
			rule = self.contract.functions.getRules(SWITCH_ID, Rule_ID).call()
			IN_PORT = rule[1]
			SRC_MAC = rule[2]
			DST_MAC = rule[3]
			PRIORITY = rule[4]
			OUT_PORT = rule[5]

			IN_PORT = int(IN_PORT)
			SRC_MAC = str(SRC_MAC)
			DST_MAC = str(DST_MAC)
			PRIORITY = int(PRIORITY)
			OUT_PORT = int (OUT_PORT)


			print("SRC_MAC: ", SRC_MAC)
			print("DST_MAC: ", DST_MAC)

			data = '{\n    "dpid": %d,\n    "table_id": 0,\n    "priority": %d,\n    "match":{\n        "in_port":%d,\n        "dl_src":"%s",\n\t"dl_dst":"%s"\n    },\n    "actions":[\n        {\n            "type":"OUTPUT",\n            "port": %d\n        }\n    ]\n}' % (SWITCH_ID, PRIORITY, IN_PORT, SRC_MAC, DST_MAC, OUT_PORT)
			print(data)
			response = requests.post('http://localhost:8080/stats/flowentry/add', headers=headers, data=data)
			print(response)
			print("Installation Completed")
			print("")


			'''
			
			## Update Infected Switch
			# New code Starts Here
			
			#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
			#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
			InfectionStatus = self.updateInfectedSwitch(SWITCH_ID)

			headers = {
	    		'Content-Type': 'application/x-www-form-urlencoded',
			}

			if InfectionStatus:
				print("")

				## Clear the flow table for current DPID
				response = requests.delete('http://localhost:8080/stats/flowentry/clear/%d' % (SWITCH_ID))

				## After clearing the flow table re-install the flows from the Blockchain
				## get the flows
				n = self.contract.functions.getRuleCount(SWITCH_ID).call()
				# Get flows one by one and install
				for i in range(1, n+1):
					rule = self.contract.functions.getRules(SWITCH_ID, i).call()
					print(rule)

					IN_PORT = rule[1]
					SRC_MAC = rule[2]
					DST_MAC = rule[3]
					PRIORITY = rule[4]
					OUT_PORT = rule[5]

					IN_PORT = int(IN_PORT)
					PRIORITY = int(PRIORITY)
					OUT_PORT = int (OUT_PORT)

					# install the flow on the forwarding device
					data = '{\n    "dpid": %d,\n    "table_id": 0,\n    "priority": %d,\n    "match":{\n        "in_port":%d,\n        "src":"%s",\n\t"dst":"%s"\n    },\n    "actions":[\n        {\n            "type":"OUTPUT",\n            "port": %d\n        }\n    ]\n}' % (SWITCH_ID, PRIORITY, IN_PORT, SRC_MAC, DST_MAC, OUT_PORT)

					response = requests.post('http://localhost:8080/stats/flowentry/add', headers=headers, data=data)
					print(response)
			else:
				# remove only current flow
				data = '{\n    "dpid": %d,\n    "table_id": 0,\n    "priority": %d,\n    "match":{\n        "in_port":%d,\n        "src":"%s",\n\t"dst":"%s"\n    },\n    "actions":[\n        {\n            "type":"OUTPUT",\n            "port": %d\n        }\n    ]\n}' % (SWITCH_ID, PRIORITY, IN_PORT, SRC_MAC, DST_MAC, OUT_PORT)

				#print(data)
				response = requests.post('http://localhost:8080/stats/flowentry/delete', headers=headers, data=data)
				print(response)

				rule = self.contract.functions.getRules(SWITCH_ID, Rule_ID).call()
				print(rule)
            	# Extract data
				IN_PORT = rule[1]
				SRC_MAC = rule[2]
				DST_MAC = rule[3]
				PRIORITY = rule[4]
				OUT_PORT = rule[5]

				IN_PORT = int(IN_PORT)
				PRIORITY = int(PRIORITY)
				OUT_PORT = int (OUT_PORT)

            	# install the flow on the forwarding device
				data = '{\n    "dpid": %d,\n    "table_id": 0,\n    "priority": %d,\n    "match":{\n        "in_port":%d,\n        "src":"%s",\n\t"dst":"%s"\n    },\n    "actions":[\n        {\n            "type":"OUTPUT",\n            "port": %d\n        }\n    ]\n}' % (SWITCH_ID, PRIORITY, IN_PORT, SRC_MAC, DST_MAC, OUT_PORT)
				response = requests.post('http://localhost:8080/stats/flowentry/add', headers=headers, data=data)
				print(response)

			# END of New Code
			'''
			
			#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
			#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

			

		'''
		t1 = time.time()- t0
		print("Time elapsed: ", t1 , "Seconds")
		print("")
		'''
	# Update Infected Switch
	def updateInfectedSwitch(self, SWITCH_ID):
		# Task:
		# Check if switch is already added
		# Get the updated number of rules from blockchain
		# Set the threshold
		#
		if SWITCH_ID in self.InfectedSwitch:
			threshold = self.getThreshold(SWITCH_ID)
			self.InfectedSwitch[SWICTH_ID]["Threshold"] = threshold
			invalid = self.InfectedSwitch[SWICTH_ID]["noOfInvalid"]

			print("Threshold: ", self.InfectedSwitch["Threshold"])
			print("No of Invalid: ", invalid)
			print("")

			###########################
			if invalid > threshold:
				return(True)		## return true if invalid
									#  crossed threshold else false
			else:
				print("Below Threshold")
				return(False)
			###########################
		else:
			print("Adding Switch to Infected List(1st Time)")
			self.addInfectedSwitch(SWITCH_ID)  ## First time
			return(False)

	def addInfectedSwitch(self, SWITCH_ID):
		print("addInfectedSwitch() function")
		print("SWITCH_ID: ", SWITCH_ID)
		self.InfectedSwitch.setdefault(SWITCH_ID,{})

		

		self.InfectedSwitch[SWITCH_ID]["Threshold"] = 0
		self.InfectedSwitch[SWITCH_ID]["noOfInvalid"] = 0
		print(self.InfectedSwitch[SWITCH_ID])

		print(self.InfectedSwitch[SWITCH_ID]["Threshold"])
		print(self.InfectedSwitch[SWITCH_ID]["noOfInvalid"])

	def getThreshold(self, SWITCH_ID):
		n = self.contract.functions.getRuleCount(SWITCH_ID).call()
		return(n/2+1)

	def main(self):

		while True:
		######################################################
		#    Task 1 .. Get the switch list
		######################################################


			cmd = 'sudo curl -X GET http://localhost:8080/stats/switches > Agent_1/switches.json'
			os.system(cmd)

			with open ('Agent_1/switches.json') as f:
				self.SWITCH_LIST = json.load(f)

			print("")
			print("SWITCH_LIST: ", self.SWITCH_LIST)
			print("")

			'''
			#### Static SWITCH
			
			DP = 101
			self.SWITCH_LIST = [DP]
			
			#### Static SWITCH
			'''


		######################################################
		#    Task 2 .. Get the flow rules of switch (SWITCH 1 RULE)
		######################################################

			

			no_of_switch = len(self.SWITCH_LIST)
			#print("Total switches: ", no_of_switch)

			if no_of_switch != 0:

				txt_file = open("output.txt","a")
				# Calculate time taken for verification


				
				
				for switch_id in self.SWITCH_LIST:
					

					print("")
					print("######################################################")
					print("		Switch Flow Rule Information    ", switch_id)
					print("######################################################")
					print("")

					#switch_id = self.SWITCH_LIST[0]    # switch at 0th position

					#print("")
					#print("switch_id", switch_id)
					#switch_id = int(switch_id)
					cmd = 'sudo curl -X GET http://localhost:8080/stats/flow/'+ str(switch_id) + '> Agent_1/flows_s1.json'
					os.system(cmd)


					with open ('Agent_1/flows_s1.json') as f:
						self.FLOW_RULE = json.load(f)

					'''
					print("Flow rules stored on the Blockchain")
					print(self.FLOW_RULE)
					print("")
					'''
					
					for s_id in self.FLOW_RULE:
						print("")
						print("switch_id: ",s_id)
						print("no_of_rules: ", len(self.FLOW_RULE[s_id]))
						print("")

			
						#	For each Flow rule get the match and action field
						Flow_ID = 1
						count = 1
						no_of_flows = 0
						for rule in self.FLOW_RULE[s_id]:
							time0 = time.time()
							no_of_flows +=1

							print("-----------------------")
							print("Rule_ID: ",Flow_ID)
							print("Rule Match: ", rule['match'])

							if len(rule['match']) > 2:
								IN_PORT = rule['match']['in_port']
								SRC_MAC = rule['match']['dl_src']
								DST_MAC = rule['match']['dl_dst']
								PRIORITY = rule['priority']
								print("IN_PORT: ", IN_PORT)
								print("PRIORITY: ", PRIORITY)
								print("Actions: ", rule['actions'])

								for OUT in rule['actions']:
									OUT = OUT.split(':')
									#print("OUT: ", OUT)
					
								print("OUT[0]", OUT[0])
								OUT_PORT = OUT[1]
								print("OUT_PORT: ", OUT_PORT)
								print("")

								if OUT_PORT == "LOCAL":
									continue


								#self.Call_Verify_Flow_Table(switch_id, count, IN_PORT, SRC_MAC, DST_MAC, str(PRIORITY), str(OUT_PORT))
								self.Call_Verify_Flow_Table(switch_id, count, IN_PORT, SRC_MAC, DST_MAC, str(PRIORITY), str(OUT_PORT))
								
								count += 1

							print("")
							Flow_ID +=1

							time_per_flow = 0
							time_per_flow = time.time() - time0

							print("Time per flow: ", time_per_flow)
							self.start_time = self.start_time + time_per_flow

						print("")
						print("Checking OVER for DPID: ",s_id)
				#print ("Total time for the Round: ", time1)
				# end of for loop
				txt_file.close()

			else:
				print("No switch is created yet !")

			print("######################################################")

			



			time.sleep(5)

		######################################################
		#    End of main function
		######################################################


A = Agent()
A.main()

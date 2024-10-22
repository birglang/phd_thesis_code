
Readme FILE
--------------------
Aent_IoMT

This Program is the final work for Agent Based flow verification
on forwarding devices in SDN network.

Main Programs
1. Controller_WO_Loop.py $## this program is for without Loop
2. Agent_IoMT.py
3. modifyFlow.py

steps:
1. Run the Ganache-cli
	ganache-cli

2. Run the Smart Contract
	sudo truffle migrate --reset

3. Copy the SC address to both Controller and Agent

4. Run the SDN Controller
	ryu-manager Controller_WO_Loop.py ofctl_rest.py

5. Run the topology
	sudo mn --topo linear,3 --controller remote
	pingall

6. Run the Blockchain Agent
	sudo python3 Agent_IoMT.py

7. Now modify the flows from the forwarding devices
	sudo python3 modifyFlow.py

Keep monitoring the Agent terminal for the verification.


##########################################################





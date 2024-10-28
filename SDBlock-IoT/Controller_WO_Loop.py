
'''
Controller_WO_Loop.py (OFBlock)
This controller works on the software switch.

The Controller adds  dummy flows on the Switches.

The Controller adds flows to the Blockchain.
The addition of duplicate flow is avoided.
Checking is done on the controller side


Agent Based Project Final

'''


from operator import attrgetter
from ryu.base import app_manager
from ryu.controller import ofp_event
from ryu.controller.handler import CONFIG_DISPATCHER, MAIN_DISPATCHER, DEAD_DISPATCHER
from ryu.controller.handler import set_ev_cls
from ryu.ofproto import ofproto_v1_3
from ryu.lib.packet import packet
from ryu.lib.packet import ethernet
from ryu.lib.packet import ether_types
from ryu.ofproto import ofproto_parser

from ryu.lib.packet import arp
from ryu.lib.packet import icmpv6
from ryu.lib.packet import ipv6
from ryu.lib.packet import ipv4
from ryu.lib.packet import tcp
from ryu.lib.packet import udp
from ryu.lib.packet import in_proto
from ryu.topology import event
from ryu.topology.api import get_switch, get_link
import copy
from collections import defaultdict
from ryu.lib import hub
import random
from randmac import RandMac
#Blockchain
from web3 import Web3
import json

from web3.middleware import geth_poa_middleware

#w3.middleware_stack.inject(geth_poa_middleware, layer=0)

#connection with the blockchain and contract
###################################################



ganache_url = "http://127.0.0.1:8545"
web3 = Web3(Web3.HTTPProvider(ganache_url))
#web3.middleware_onion.inject(geth_poa_middleware, layer=0)
print('Connected with the blockchain : ', web3.isConnected())
web3.eth.defaultAccount = web3.eth.accounts[0]
print(web3.eth.accounts[0])

with open('abi.json') as f:
    abi = json.load(f)

address = web3.toChecksumAddress("0x414185CeB30a0BE9da48BC1Db2236A31859e3dDa")
contract = web3.eth.contract(address = address, abi = abi)


#####################################################



class DiscoverTopology(app_manager.RyuApp):
    OFP_VERSIONS = [ofproto_v1_3.OFP_VERSION]

    def __init__(self, *args, **kwargs):
        super(DiscoverTopology, self).__init__(*args, **kwargs)
        #self.monitor_thread = hub.spawn(self._monitor)
        
        self.SWITCH_LIST = []
        self.DPID_LIST = []
        self.DATAPATH_LIST = []

        self.HOST_LIST = {}

        self.mac_to_port = {}

        self.CLIENTS = []
        self.adjacency = {}

        self.Temp_Flow = {}
        self.no_of_flows = 600

    
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    #@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@


    @set_ev_cls(ofp_event.EventOFPSwitchFeatures, CONFIG_DISPATCHER)
    def switch_features_handler(self, ev):


        #print ("")
        #print ("SWITCH FEATURE HANDLER")
        


        datapath = ev.msg.datapath
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        match = parser.OFPMatch()
        actions = [parser.OFPActionOutput(ofproto.OFPP_CONTROLLER,
                                          ofproto.OFPCML_NO_BUFFER)]
        self.add_flow(datapath, 0, match, actions)
        

        #########################################################
    # Adding flows
    def add_flow(self, datapath, priority, match, actions, buffer_id=None):
        '''
        print("")
        print("Add flow")
        print("")
        '''
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        inst = [parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS,
                                             actions)]
        if buffer_id:
            mod = parser.OFPFlowMod(datapath=datapath, buffer_id=buffer_id,
                                    priority=priority, match=match,
                                    instructions=inst)
        else:
            mod = parser.OFPFlowMod(datapath=datapath, priority=priority,
                                    match=match, instructions=inst)
        datapath.send_msg(mod)


    @set_ev_cls(ofp_event.EventOFPStateChange, [MAIN_DISPATCHER, DEAD_DISPATCHER])
    def _state_change_handler(self, ev):
        
        print ("")
        print ("State Change Handler")

        datapath = ev.datapath
        print("Datapath ID: ", datapath.id)
        if ev.state == MAIN_DISPATCHER:
            if datapath not in self.SWITCH_LIST:
                
                print ("")
                print ("Initializing SWITCH_LIST || DPID_LIST || HOST_LIST")

                self.SWITCH_LIST.append(datapath)
                self.DPID_LIST.append(datapath.id)
                self.DATAPATH_LIST.append(datapath)

                self.HOST_LIST.setdefault(datapath.id,[])
                
                ############################################
                #   Adding switches to the Blockchain
                ############################################
                switch_name = 'S'+str(datapath.id)
                #print("switch_name", switch_name)
                print ("Adding switch to Blockchain: ", switch_name)
                #print("Mining the Block")
                tx_hash = contract.functions.addSwitches(datapath.id, switch_name, str(datapath.address)).transact()
                #web3.eth.waitForTransactionReceipt(tx_hash)
                #print("Block Mined")
                '''
                print("")
                print("Block Details")
                print(web3.eth.get_block (web3.eth.block_number))
                print("Hash: ",web3.eth.get_block(web3.eth.block_number).hash)
                print("Miner: ",web3.eth.get_block(web3.eth.block_number).miner)
                print("Difficulty: ",web3.eth.get_block(web3.eth.block_number).difficulty)
                '''
                switch_count = contract.functions.switch_count().call()

                print("")
                print("Switch Count: ", switch_count)
                #print("Swicth Information:")
                #for i in range(1, switch_count+1):
                    #print(contract.functions.switches(i).call())
                # Install Dummy Flows on the switch
                print("Call to install dummy flows")
                print("")


                self.installDummyFlows(datapath)

    #########################################################
                
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

    @set_ev_cls(event.EventSwitchLeave, [MAIN_DISPATCHER, CONFIG_DISPATCHER, DEAD_DISPATCHER])
    def handler_switch_leave(self, ev):

        print ("")
        print ("SWITCH LEAVE HANDLER")

        datapath = ev.switch.dp
        dpid = datapath.id      
        
        if dpid in self.DPID_LIST:
            
            print ("Switch Leaving (DPID): ", dpid)
            print ("")

            self.DPID_LIST.remove(dpid)
            self.DATAPATH_LIST.remove(datapath)

            # Delete the Client from switch
            self.HOST_LIST[dpid] = ""

            #self.CLIENTS.remove()

            if dpid in self.mac_to_port:
                del self.mac_to_port[dpid]

            if dpid in self.adjacency:
                del self.adjacency[dpid]    # Adjacency List needs to be removed

            if len(self.DPID_LIST) == 0:
                print ("RESET Over")


    #$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

    @set_ev_cls(event.EventLinkAdd, MAIN_DISPATCHER)
    def _link_add_handler(self, ev):

        s1 = ev.link.src
        s2 = ev.link.dst

        self.adjacency.setdefault(s1.dpid, {}).setdefault(s2.dpid,{})
        self.adjacency.setdefault(s2.dpid, {}).setdefault(s1.dpid,{})


        self.adjacency[s1.dpid][s2.dpid] = s1.port_no
        self.adjacency[s2.dpid][s1.dpid] = s2.port_no


    ###############################################################
    

    @set_ev_cls(ofp_event.EventOFPPacketIn, MAIN_DISPATCHER)
    def _packet_in_handler(self, ev):


        #########################################################
        if ev.msg.msg_len < ev.msg.total_len:
            self.logger.debug("packet truncated: only %s of %s bytes",
                              ev.msg.msg_len, ev.msg.total_len)
        #########################################################

        msg = ev.msg
        datapath = msg.datapath
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser
        in_port = msg.match['in_port']

        pkt = packet.Packet(msg.data)
        eth = pkt.get_protocols(ethernet.ethernet)[0]

        dst = eth.dst
        src = eth.src

        dpid = datapath.id

        #########################################################
        

        if dpid not in self.DPID_LIST:
            self.DPID_LIST.append(dpid)
            self.SWITCH_LIST.append(dpid)
            self.HOST_LIST.setdefault(dpid, []) 

        

        self.mac_to_port.setdefault(dpid, {})
        #if src not in self.mac_to_port[dpid]:
        self.mac_to_port[dpid][src] = in_port


        #########################################################
        # ignore LLDP Packet
        if eth.ethertype == ether_types.ETH_TYPE_LLDP:
            return


        #                   IPV6 Handler

        if eth.ethertype == ether_types.ETH_TYPE_IPV6:
            out_port = 0
            actions = {}
            match = parser.OFPMatch(eth_type=ether_types.ETH_TYPE_IPV6)
            self.add_flow(datapath, 1, match, actions)

            data = None
            if msg.buffer_id == ofproto.OFP_NO_BUFFER:
                data = msg.data

            out = parser.OFPPacketOut(datapath=datapath, buffer_id=msg.buffer_id,
                                  in_port=in_port, actions=actions, data=data)
            datapath.send_msg(out)
            return

        ###############################################################################################
        ###############################################################################################
        
        #                                     ARP REQUEST HANDLER

        ###############################################################################################
        ###############################################################################################
        '''
        print ("")
        print ("")
        print ("")
        print ("#############################################")
        print ("DPID    |        HOST LIST")
        print ("#############################################")
        print ("")

        for dp in self.HOST_LIST:
            print (dp, "  |  ", self.HOST_LIST[dp])

        print ("")
        print ("#############################################")
        '''

        dst_ip = ''
        src_ip = ''
        '''
        # ARP Handler
        # With Loop Control Mechanism
        if eth.ethertype == ether_types.ETH_TYPE_ARP:
            print ("DPID:",dpid)
            #print ("")
            print ("     ARP at DPID", dpid)
            #print mac_to_port
            arp_pkt = pkt.get_protocol(arp.arp)
            dst_ip = arp_pkt.dst_ip
            src_ip = arp_pkt.src_ip
            #print ("     src_ip ",src_ip, " dst_ip: ",dst_ip)

            # ADD HOST LIST DICTIONARY
            if src not in self.CLIENTS:
                self.CLIENTS.append(src)
                self.HOST_LIST[dpid].append(src)

        else:
            pass
            #print("Not an ARP")

        # With Loop Control Mechanism ends here
        '''
        #@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
        #@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

        if dst in self.mac_to_port[dpid]:
            out_port = self.mac_to_port[dpid][dst]
            actions = [parser.OFPActionOutput(out_port)]
            

        else:
            
            out_port = ofproto.OFPP_FLOOD
            actions = [parser.OFPActionOutput(out_port)]

        #print("OUT_PORT: ", out_port)
        # install a flow to avoid packet_in next time
        if out_port != ofproto.OFPP_FLOOD:
            match = parser.OFPMatch(in_port=in_port, eth_dst=dst, eth_src=src)
            priority = 1

            #rule_count = len(self.Temp_Flow[dpid])

            if msg.buffer_id != ofproto.OFP_NO_BUFFER:
                self.add_flow(datapath, priority, match, actions, msg.buffer_id)
                
                #out_port = str(out_port)
                self.addRuleToBlockchain(dpid, str(in_port), src, dst, str(priority), str(out_port))
                
                return
            else:
                #print("Add flow with buffer")
                self.add_flow(datapath, priority, match, actions)
                
                #out_port = str(out_port)
                self.addRuleToBlockchain(dpid, str(in_port), src, dst, str(priority), str(out_port))
                

            
        data = None
        if msg.buffer_id == ofproto.OFP_NO_BUFFER:
            data = msg.data

        out = parser.OFPPacketOut(datapath=datapath, buffer_id=msg.buffer_id,
                                  in_port=in_port, actions=actions, data=data)
        datapath.send_msg(out)


        ###############################################################################################
        ###############################################################################################
        
        #                                   END OF PACKET_IN

        ###############################################################################################
        ###############################################################################################


    def addRuleToBlockchain(self, dpid, in_port, src, dst, priority, out_port):
        
        #self.Temp_Flow.setdefault(dpid,{}).setdefault(flow_id,{}).setdefault(src,{}).setdefault(dst, {}).setdefault(priority, {}).setdefault(out_port)
        self.Temp_Flow.setdefault(dpid,{})
        similarity = 1
        rule_count = len(self.Temp_Flow[dpid])
        if rule_count == 0:
            flow_id = rule_count + 1
            self.Temp_Flow.setdefault(dpid,{}).setdefault(flow_id,{}).setdefault(src,{}).setdefault(dst, {}).setdefault(priority, {}).setdefault(out_port)
            tx_hash = contract.functions.addRule(str(in_port), src, dst, str(priority), str(out_port), dpid).transact()
            print("First Rule")
            print("Rule added Successfully")
        else:
            print("Check if rule has been already stored")
            print("")

            for flow_id in self.Temp_Flow[dpid]:
                if src in self.Temp_Flow[dpid][flow_id] and  dst in self.Temp_Flow[dpid][flow_id][src] and priority in self.Temp_Flow[dpid][flow_id][src][dst] and out_port in self.Temp_Flow[dpid][flow_id][src][dst][priority]:
                    print("Rule already Exits!")
                    similarity = 0
                    break
            if similarity:
                self.Temp_Flow.setdefault(dpid,{}).setdefault(flow_id,{}).setdefault(src,{}).setdefault(dst, {}).setdefault(priority, {}).setdefault(out_port)
                tx_hash = contract.functions.addRule(str(in_port), src, dst, str(priority), str(out_port), dpid).transact()
                print("No existing rule found!")
                print("Rule added Successfully")


        ############################

    def generateMAC(self):
        example_mac = "00:00:00:00:00:00"
        generated_mac = RandMac(example_mac)
        return generated_mac

    
    def installDummyFlows(self, datapath):
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        # Run a loop to install flows on the switch
        dpid = datapath.id
        priority = 1
        #example_mac = "00:00:00:00:00:00"
        for i in range(self.no_of_flows):

            # CREATE DUMMY FLOWS

            src = self.generateMAC()
            #src = "00:00:00:00:00:00"
            dst = self.generateMAC()


            src = str(src)
            dst = str(dst)

            print("ID: ",i)
            print("SRC MAC: ", src)
            print("DST MAC: ", dst)
            print("")

            in_port = 5
            out_port = 3
            priority = 1
            #**************************

            match = parser.OFPMatch(in_port=in_port, eth_dst=dst, eth_src=src)
            actions = [parser.OFPActionOutput(out_port)]

            self.add_flow(datapath, priority, match, actions, buffer_id=None)
            
            in_port = str(5)
            out_port = str(3)
            priority = str(1)
            self.addRuleToBlockchain(dpid, in_port, src, dst, priority, out_port)

        #*******************************************
        # Call the Rules stored on the Blockchain
        #*******************************************
        count = contract.functions.getRuleCount(dpid).call()
        print("Count: ", count)
        '''
        for i in range(1, count+1):
            print(contract.functions.getRules(dpid, i).call())

        print("")
        '''



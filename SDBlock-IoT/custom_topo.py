
"""


                S2----------------S3
               /                    \
              2                      2
             /                        \
     ---1--S1--3-----S5-----S6-----3--S4--1----
             \'                       /
              4                      4
               \'                   /
                S7----------------S8

    cd /home/ubuntu/ryu && ./bin/ryu-manager --verbose ryu/app/ECMP.py
    sudo mn --topo  --mac --controller remote --switch ovsk


   run code as:
   sudo mn --custom path+file.py --topo mytopo --controller remote
"""


from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import Controller, RemoteController, OVSController
from mininet.node import CPULimitedHost, Host, Node
from mininet.node import OVSKernelSwitch, UserSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from mininet.link import TCLink, Intf

class MyTopo(Topo):
	"Multipath Topology"
	
	def __init__(self, enable_all = True):
		"creating custom topology."
			
		#Initialise Topology
		Topo.__init__(self)

		#adding hosts (2) and Switches (6)
		hostone = self.addHost('h1')
		hosttwo = self.addHost('h2')
		switchone = self.addSwitch('s1')
		switchtwo = self.addSwitch('s2')
		switchthree = self.addSwitch('s3')
		switchfour = self.addSwitch('s4')
		switchfive = self.addSwitch('s5')
		switchsix = self.addSwitch('s6')
		switchseven = self.addSwitch('s7')
		switcheight = self.addSwitch('s8')

		#adding links
		self.addLink( hostone, switchone )
		self.addLink( hosttwo, switchfour)

		self.addLink( switchone, switchtwo )
		self.addLink( switchone, switchfive )
		self.addLink( switchone, switchseven )

		self.addLink( switchtwo, switchthree )
		self.addLink( switchfive, switchsix )
		self.addLink( switchseven, switcheight)

		self.addLink( switchthree, switchfour )
		self.addLink( switchsix, switchfour )
		self.addLink( switcheight, switchfour )

topos = {'mytopo': (lambda: MyTopo())}
#!/usr/bin/python

from mininet.net import Mininet
# author: Birglang Bargayary
# 

from mininet.node import Controller, OVSKernelSwitch, RemoteController
from mininet.cli import CLI
from mininet.log import setLogLevel, info

def customTopo():

    net = Mininet(controller=RemoteController, switch=OVSKernelSwitch)

    c1 = net.addController('c1', controller=RemoteController, ip="127.0.0.1", port=6633)
    Agent = net.addController('Agent', controller=RemoteController, ip="127.0.0.1", port=6634)

    s1 = net.addSwitch( 's1' )
    s2 = net.addSwitch( 's2' )
    s3 = net.addSwitch( 's3' )

    info( "*** Creating hosts\n" )
    hosts1 = [ net.addHost( 'h%d' % n ) for n in ( 3, 4 ) ]
    hosts2 = [ net.addHost( 'h%d' % n ) for n in ( 5, 6 ) ]

    info( "*** Creating links\n" )
    for h in hosts1:
        net.addLink( s1, h )
    for h in hosts2:
        net.addLink( s2, h )
    #net.addLink( s1, s2 )

    s1.linkTo( s2 )
    s2.linkTo( s3 )


    net.build()
    c1.start()
    Agent.start()

    s1.start([Agent,c1])
    s2.start([Agent,c1])
    s3.start([Agent,c1])

    net.start()
    #net.staticArp()
    CLI( net )
    net.stop()

if __name__ == '__main__':
    setLogLevel( 'info' )
    customTopo()

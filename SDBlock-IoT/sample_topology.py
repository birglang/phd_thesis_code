#!/usr/bin/python

from mininet.net import Mininet
# author: Juhika Ajmeen
# till now, no host has been added, controllers running on ips- 35.153.129.201, 3.81.80.244

from mininet.node import Controller, OVSKernelSwitch, RemoteController
from mininet.cli import CLI
from mininet.log import setLogLevel, info

def emptyNet():

    net = Mininet(controller=RemoteController, switch=OVSKernelSwitch)

    c1 = net.addController('c1', controller=RemoteController, ip="127.0.0.1", port=6633)
    Agent = net.addController('Agent', controller=RemoteController, ip="127.0.0.1",port=6643)

    s1 = net.addSwitch( 's1' )
    s2 = net.addSwitch( 's2' )
    s3 = net.addSwitch( 's3' )

    s1.linkTo( s2 )
    s2.linkTo( s3 )


    net.build()
    c1.start()
    c2.start()

    s1.start([Agent,c1])
    s2.start([Agent,c1])
    s3.start([Agent,c1])

    net.start()
    #net.staticArp()
    CLI( net )
    net.stop()

if __name__ == '__main__':
    setLogLevel( 'info' )
    emptyNet()

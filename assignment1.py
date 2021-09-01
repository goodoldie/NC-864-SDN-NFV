from mininet.net import Mininet
from mininet.topo import Topo
from mininet.cli import CLI
from mininet.util import dumpNodeConnections
from mininet.node import Controller, OVSSwitch, RemoteController
from mininet.link import TCLink
import random
"""

                      h2      h6      h7       h8
                       |      |       |        |
Topology  =       h1--s1------s2------s3-------s4--h12
                      |      /|      /|         |
                    h3      / |     / |         |
                           h4  h5  h9  h10     h11

"""
class MyFirstTopology(Topo):

    def __init__(self):

        Topo.__init__(self)

        #Add Hosts
        h1 = self.addHost('h1', ip=f"192.168.0.1/24")
        h2 = self.addHost('h2', ip=f"192.168.0.2/24")
        h3 = self.addHost('h3', ip=f"192.168.0.3/24")
        h4 = self.addHost('h4', ip=f"192.168.0.4/24")
        h5 = self.addHost('h5', ip=f"192.168.0.5/24")
        h6 = self.addHost('h6', ip=f"192.168.0.6/24")
        h7 = self.addHost('h7', ip=f"192.168.0.7/24")
        h8 = self.addHost('h8', ip=f"192.168.0.8/24")
        h9 = self.addHost('h9', ip=f"192.168.0.9/24")
        h10 = self.addHost('h10', ip=f"192.168.0.10/24")
        h11 = self.addHost('h11', ip=f"192.168.0.11/24")
        h12 = self.addHost('h12', ip=f"192.168.0.12/24")

        #Add switch
        s1 = self.addSwitch('s1', protocols="OpenFlow13")
        s2 = self.addSwitch('s2', protocols="OpenFlow13")
        s3 = self.addSwitch('s3', protocols="OpenFlow13")
        s4 = self.addSwitch('s4', protocols="OpenFlow13")

        #Link Hosts to switches
        self.addLink(h1, s1, bw = random.randint(0,5), delay=f"{random.randint(2,30)}ms")
        self.addLink(h2, s1, bw = random.randint(0,5), delay=f"{random.randint(2,30)}ms")
        self.addLink(h3, s1, bw = random.randint(0,5), delay=f"{random.randint(2,30)}ms")

        self.addLink(h4, s2, bw = random.randint(0,5), delay=f"{random.randint(2,30)}ms")
        self.addLink(h5, s2, bw = random.randint(0,5), delay=f"{random.randint(2,30)}ms")
        self.addLink(h6, s2, bw = random.randint(0,5), delay=f"{random.randint(2,30)}ms")

        self.addLink(h7, s3, bw = random.randint(0,5), delay=f"{random.randint(2,30)}ms")
        self.addLink(h9, s3, bw = random.randint(0,5), delay=f"{random.randint(2,30)}ms")
        self.addLink(h10, s3, bw = random.randint(0,5), delay=f"{random.randint(2,30)}ms")

        self.addLink(h8, s4, bw = random.randint(0,5), delay=f"{random.randint(2,30)}ms")
        self.addLink(h11, s4, bw = random.randint(0,5), delay=f"{random.randint(2,30)}ms")
        self.addLink(h12, s4, bw = random.randint(0,5), delay=f"{random.randint(2,30)}ms")

        #Link Switches as shown in the Topology
        self.addLink(s1,s2, bw = random.randint(0,5), delay=f"{random.randint(2,30)}ms")
        self.addLink(s2,s3, bw = random.randint(0,5), delay=f"{random.randint(2,30)}ms")
        self.addLink(s3,s4, bw = random.randint(0,5), delay=f"{random.randint(2,30)}ms")



def runScript():
    mytopo = MyFirstTopology()
    net = Mininet(topo=mytopo, controller=lambda name: RemoteController(name, ip="10.0.2.11"),
                  switch=OVSSwitch, link=TCLink)
    net.start()
    CLI(net)
    net.stop()


if __name__ == '__main__':
    runScript()

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import Node
from mininet.log import setLogLevel, info
from mininet.cli import CLI
from mininet.node import Host
from mininet.node import OVSSwitch
from mininet.node import RemoteController
from mininet.node import DefaultController



class NetworkTopo(Topo):
    def __init__(self):
        """Constructor"""
        Topo.__init__(self)
        #Add Switches
        r1 = self.addSwitch("r1")
        r2 = self.addSwitch("r2")
        r3 = self.addSwitch("r3")
        r4 = self.addSwitch("r4")

        #Network 1
        s1 = self.addSwitch("s1")
        #add link from router_1 to switch_1 via eth0
        self.addLink(s1, r1, intfName2="r1-eth0")
        h12 = self.addHost(name="h12", ip="10.0.1.2/24")
        h13 = self.addHost(name="h13", ip="10.0.1.3/24")
        self.addLink(s1, h12)
        self.addLink(s1, h13)


        #Network 2
        h22 = self.addHost(name="h22", ip="10.0.2.2/24")
        self.addLink(h22, r2, intfName2="r2-eth0")


        #Network 3
        h32 = self.addHost(name="h32", ip="10.0.3.2/24")
        self.addLink(h32, r3, intfName2="r3-eth0")


        #Network 4
        s2 = self.addSwitch("s2")
        self.addLink(s2, r4, intfName2="r4-eth0")
        h42 = self.addHost(name="h42", ip="10.0.4.2/24")
        h43 = self.addHost(name="h43", ip="10.0.4.3/24")
        self.addLink(s2, h42)
        self.addLink(s2, h43)


        #Connect all the routers
        self.addLink(r1,r3,intfName1="r1-eth1",intfName2="r3-eth1")

        self.addLink(r2,r4,intfName1="r2-eth1",intfName2="r4-eth1")

        self.addLink(r1,r2,intfName1="r1-eth2",intfName2="r2-eth2")


topology = NetworkTopo()
net = Mininet(topo=topology,controller=DefaultController,switch=OVSSwitch,autoSetMacs=True,autoStaticArp=True,waitConnected=True,)
net.start()

#Add default route in hosts
for host in net.hosts:
    intf = host.defaultIntf()
    host.setDefaultRoute(intf)


CLI(net)
net.stop()

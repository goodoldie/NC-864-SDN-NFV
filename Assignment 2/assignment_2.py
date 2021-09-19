from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import Node
from mininet.log import setLogLevel, info
from mininet.cli import CLI


class LinuxRouter(Node):
    def config(self, **params):
        super(LinuxRouter, self).config(**params)
        self.cmd("sysctl net.ipv4.ip_forward=1")

    def terminate(self):
        self.cmd("sysctl net.ipv4.ip_forward=0")
        super(LinuxRouter, self).terminate()


class NetworkTopo(Topo):
    def build(self, **_opts):
        #Add Routers
        r1 = self.addNode("r1", cls=LinuxRouter, ip="10.0.1.1/24")
        r2 = self.addNode("r2", cls=LinuxRouter, ip="10.0.2.1/24")
        r3 = self.addNode("r3", cls=LinuxRouter, ip="10.0.3.1/24")
        r4 = self.addNode("r4", cls=LinuxRouter, ip="10.0.4.1/24")

        #Network 1
        s1 = self.addSwitch("s1")
        #add link from router_1 to switch_1 via eth0
        self.addLink(s1, r1, intfName2="r1-eth0", params2={"ip": "10.0.1.1/24"})
        h12 = self.addHost(name="h12", ip="10.0.1.2/24", defaultRoute="via 10.0.1.1")   #provide default route as eth0 of r1
        h13 = self.addHost(name="h13", ip="10.0.1.3/24", defaultRoute="via 10.0.1.1")
        self.addLink(s1, h12)
        self.addLink(s1, h13)


        #Network 2
        h22 = self.addHost(name="h22", ip="10.0.2.2/24", defaultRoute="via 10.0.2.1")   #provide default route as eth0 of r2
        self.addLink(h22, r2, intfName2="r2-eth0", params2={"ip": "10.0.2.1/24"})


        #Network 3
        h32 = self.addHost(name="h32", ip="10.0.3.2/24", defaultRoute="via 10.0.3.1")   #provide default route as eth0 of r3
        self.addLink(h32, r3, intfName2="r3-eth0", params2={"ip": "10.0.3.1/24"})


        #Network 4
        s2 = self.addSwitch("s2")
        self.addLink(s2, r4, intfName2="r4-eth0", params2={"ip": "10.0.4.1/24"})
        h42 = self.addHost(name="h42", ip="10.0.4.2/24", defaultRoute="via 10.0.4.1")
        h43 = self.addHost(name="h43", ip="10.0.4.3/24", defaultRoute="via 10.0.4.1")
        self.addLink(s2, h42)
        self.addLink(s2, h43)


        #Connect all the routers
        self.addLink(r1,r3,intfName1="r1-eth1",intfName2="r3-eth1",
                     params1={"ip": "192.168.0.1/24"},params2={"ip": "192.168.0.3/24"},)

        self.addLink(r2,r4,intfName1="r2-eth1",intfName2="r4-eth1",
                     params1={"ip": "192.168.6.1/24"},params2={"ip": "192.168.6.2/24"},)

        self.addLink(r1,r2,intfName1="r1-eth2",intfName2="r2-eth2",
                     params1={"ip": "192.168.5.1/24"},params2={"ip": "192.168.5.2/24"},)


net = Mininet(topo=NetworkTopo())
net.start()
#Add Routing Rules
#while adding from ri to rj, we also need to add from rj to ri.
net["r1"].cmd("ip route add 10.0.2.0/24 via 192.168.5.2")  # from r1 to r2
net["r1"].cmd("ip route add 10.0.3.0/24 via 192.168.0.3")  # from r1 to r3
net["r1"].cmd("ip route add 10.0.4.0/24 via 192.168.5.2")  # from r1 to r4

net["r2"].cmd("ip route add 10.0.1.0/24 via 192.168.5.1")  # from r2 to r1
net["r2"].cmd("ip route add 10.0.3.0/24 via 192.168.5.1")  # from r2 to r3
net["r2"].cmd("ip route add 10.0.4.0/24 via 192.168.6.2")  # from r2 to r4

net["r3"].cmd("ip route add 10.0.1.0/24 via 192.168.0.1")  # from r3 to r1
net["r3"].cmd("ip route add 10.0.2.0/24 via 192.168.0.1")  # from r3 to r2
net["r3"].cmd("ip route add 10.0.4.0/24 via 192.168.0.1")  # from r3 to r4

net["r4"].cmd("ip route add 10.0.1.0/24 via 192.168.6.1")  # from r4 to r1
net["r4"].cmd("ip route add 10.0.2.0/24 via 192.168.6.1")  # from r4 to r2
net["r4"].cmd("ip route add 10.0.3.0/24 via 192.168.6.1")  # from r4 to r3


CLI(net)
net.stop()

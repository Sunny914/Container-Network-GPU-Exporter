Network Documentation
Container → Network → Hardware Topology (Docker)

Container → Network → Hardware Topology (Docker)
This document describes the end-to-end Linux networking path taken by traffic originating from a Docker container, mapped using kernel-level inspection.
The topology is derived from live system data and reflects actual runtime state, not assumptions.

Observed Topology Snapshot
Previous:
container_network_topology_info{
  bridge="br-982c07beb42c",
  container="bridge-test",
  container_id="1a1c0b92ad0861dc26bba447679f53cc4f0a0bc7be4b18725bc2ccb3a1350833",
  container_iface="eth0",
  container_ip="172.19.0.2/16",
  host_veth="veth87381d1",
  physical_nic="wlp0s20f3",
  pid="3060812"
} 1.0

After Changes: 
Final Output (From /metrics)
container_network_info{container="bridge-test", container_id="1a1c0b92ad0861dc26bba447679f53cc4f0a0bc7be4b18725bc2ccb3a1350833", container_iface="eth0",container_ip="172.19.0.2/16",pid="3060812"} 1

container_veth_info{container="bridge-test",host_veth="vethcfd265f"} 1

container_bridge_info{container="bridge-test",bridge="br-7d470e07f921"} 1

container_physical_nic_info{container="bridge-test",physical_nic="wlp0s20f3"} 1

This metric represents the complete container → kernel → hardware network path.

1. Container Process Identity
Container PID
Previous:
docker inspect bridge-test | grep -i '"Pid"'

After Changes:

Container PID is resolved using Docker SDK.

Implementation:
client = docker.from_env()
container = client.containers.get(container_name)
pid = container.attrs["State"]["Pid"]
Result:
"Pid": 3060812


Why the changes were made:
Removed Docker CLI dependency
Eliminated subprocess overhead
Direct Docker socket communication



2. Container Network Namespace
Using the container PID, the container’s network namespace is inspected.
Previous:
sudo nsenter -t 3060812 -n ip -o addr

After Changes:

Container namespace is entered using pyroute2 NetNS.

from pyroute2 import NetNS

with NetNS(f"/proc/{pid}/ns/net") as ns:
    routes = ns.get_default_routes()


Observed Interface
eth0@if43 inet 172.19.0.2/16


Why this change was made:
Removed nsenter shell call
Uses netlink socket directly
Kernel-level inspection
Namespace-safe and deterministic


Interpretation:
eth0 → container’s virtual network interface
172.19.0.2/16 → container IP address
@if43 → peer interface index on the host
if43 is not an interface name.It is a kernel interface index, used to link namespaces.

3. Container ↔ Host veth Pair
Resolving Host-Side veth
To map if43 to a real host interface:
Previous:
ip -o link show

After Changes:
Host-side veth resolved via sysfs:

/sys/class/net/<iface>/ifindex
/sys/class/net/<iface>/master

Matching entry:
43: veth87381d1@if2: ... master br-982c07beb42c ... link-netnsid 1
Result
Side
Interface
Container
eth0@if43
Host
veth87381d1

Why this change was made:
Avoided CLI parsing
No regex/string parsing
Direct kernel metadata
Deterministic and faster
Significance
This veth pair is a virtual Ethernet cable
One end lives in the container namespace
One end lives in the host namespace
This is the namespace boundary crossing point.

4. Linux Bridge (L2 Switching Layer)
The host-side veth is enslaved to a Linux bridge:
master br-982c07beb42c

Bridge Identified
br-982c07beb42c


Role of the Bridge
Acts as a software Layer-2 switch
Connects multiple containers in the same Docker network
Handles MAC learning, forwarding, and broadcast
Containers do not communicate directly with the NIC — all traffic passes through this bridge.

5. Host Routing & Physical NIC
The Linux kernel decides how traffic leaves the host using the routing table.
Previous:
ip route show default

After Changes:
Physical NIC resolved from kernel routing table:
/proc/net/route

Example result:
default via 192.168.31.1 dev wlp0s20f3
Physical Network Card
Wlp0s20f3


Why this change was made:
Removed ip route shell execution
Reads kernel routing table directly
No subprocess dependency


Significance
This is the actual hardware interface
Chosen by the kernel’s routing logic
Containers do not influence this decision

6. Final End-to-End Network Path
Container (bridge-test)
  └─ eth0 (172.19.0.2/16)
       └─ veth87381d1
            └─ br-982c07beb42c (Docker bridge)
                 └─ Linux routing table
                      └─ wlp0s20f3 (Physical NIC)


This path is kernel-accurate and reflects real packet flow.

Key Observations
Containers never see physical hardware
All container traffic is abstracted via:
network namespaces
veth pairs
Linux bridges
routing rules
The routing table is the final authority
The same abstraction pattern applies to GPUs, storage, and other resources

Key Takeaway
Docker container networking is a layered Linux abstraction.
Traffic flows from container namespaces through virtual Ethernet, software bridges, and kernel routing before reaching real hardwar
 

Conclusion
The system:
Uses Docker SDK for container metadata
Enters network namespaces via netlink (pyroute2)
Resolves veth and bridge relationships via /sys
Extracts physical NIC information directly from /proc/net/route
Exposes logically separated Prometheus metrics for each topology layer


This ensures:
No shell dependencies
No CLI parsing
No regex-based interface detection
Kernel-accurate inspection

 


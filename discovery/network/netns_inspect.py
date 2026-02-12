# discovery/network/netns_inspect.py


import os
from pyroute2 import NetNS

def get_container_net_info(pid: int):
    """
    Discover container primary interface, IP and peer_ifindex
    using pyroute2 inside container network namespace.
    """

    netns_path = f"/proc/{pid}/ns/net"

    if not os.path.exists(netns_path):
        return {"interface": None, "ip": None, "peer_ifindex": None}

    with NetNS(netns_path) as ns:

        # Get default route (AF_INET = 2)
        routes = ns.get_default_routes(family=2)

        if not routes:
            return {"interface": None, "ip": None, "peer_ifindex": None}

        route = routes[0]

        iface_index = None
        for attr in route["attrs"]:
            if attr[0] == "RTA_OIF":
                iface_index = attr[1]
                break

        if iface_index is None:
            return {"interface": None, "ip": None, "peer_ifindex": None}

        # Get link info
        link = ns.get_links(iface_index)[0]
        iface_name = link.get_attr("IFLA_IFNAME")

        # Get IP address
        addrs = ns.get_addr(index=iface_index)

        ip_addr = None
        if addrs:
            ip = addrs[0].get_attr("IFA_ADDRESS")
            prefix = addrs[0]["prefixlen"]
            ip_addr = f"{ip}/{prefix}"

    # Read peer ifindex from sysfs via container root
    iflink_path = f"/proc/{pid}/root/sys/class/net/{iface_name}/iflink"

    peer_ifindex = None
    try:
        with open(iflink_path) as f:
            peer_ifindex = int(f.read().strip())
    except Exception:
        pass

    return {
        "interface": iface_name,
        "ip": ip_addr,
        "peer_ifindex": peer_ifindex,
    }































"""
import subprocess
import re


def get_container_net_info(pid: int):
    
   # Discover container network interface, IP, and peer ifindex
   # by inspecting the container's default route.
    

    # 1. Find default route inside container netns
    route_cmd = [
        "nsenter", "-t", str(pid), "-n",
        "ip", "route", "show", "default"
    ]
    route_out = subprocess.check_output(route_cmd, text=True).strip()

    # Example:
    # default via 172.19.0.1 dev eth0
    parts = route_out.split()
    iface = parts[parts.index("dev") + 1]

    # 2. Get interface details
    addr_cmd = [
        "nsenter", "-t", str(pid), "-n",
        "ip", "-o", "addr", "show", iface
    ]
    addr_out = subprocess.check_output(addr_cmd, text=True)

    ip_match = re.search(r"inet (\S+)", addr_out)
    peer_match = re.search(r"@if(\d+)", addr_out)

    return {
        "interface": iface,
        "ip": ip_match.group(1) if ip_match else None,
        "peer_ifindex": peer_match.group(1) if peer_match else None,
    }
"""
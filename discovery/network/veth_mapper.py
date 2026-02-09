import subprocess
import re

def get_host_veth(_peer_ifindex):
    """
    Correct approach:
    - Find veth interfaces enslaved to docker bridges
    - Pick the one with link-netnsid (container side)
    """

    cmd = ["ip", "-o", "link", "show"]
    output = subprocess.check_output(cmd, text=True)

    for line in output.splitlines():
        if "veth" in line and "link-netnsid" in line:
            # Example:
            # 43: veth3d36421@if2: ... master br-982c07beb42c ... link-netnsid 1
            iface = line.split(":")[1].strip().split("@")[0]
            return iface

    return None






"""
import subprocess


def get_host_veth(peer_ifindex: str) -> str | None:
    
   # Given peer ifindex from container (eth0@ifXXX),
    #resolve host-side veth interface name.
    
    if not peer_ifindex:
        return None

    cmd = ["ip", "-o", "link", "show"]
    output = subprocess.check_output(cmd, text=True)

    for line in output.splitlines():
        # Example:
        # 42: veth87381d1@if2: ...
        if f"if{peer_ifindex}" in line:
            iface = line.split(":")[1].strip().split("@")[0]
            return iface

    return None

"""



























"""
import subprocess
import re

def get_host_veth(_peer_ifindex):
    
    #Correct approach:
    #- Find veth interfaces enslaved to docker bridges
    #- Pick the one with link-netnsid (container side)
    

    cmd = ["ip", "-o", "link", "show"]
    output = subprocess.check_output(cmd, text=True)

    for line in output.splitlines():
        if "veth" in line and "link-netnsid" in line:
            # Example:
            # 43: veth3d36421@if2: ... master br-982c07beb42c ... link-netnsid 1
            iface = line.split(":")[1].strip().split("@")[0]
            return iface

    return None


"""















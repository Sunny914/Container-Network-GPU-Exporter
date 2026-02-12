# discovery/network/veth_mapper.py

import os

def get_host_veth(peer_ifindex: int):
    """
    Resolve host-side veth interface by matching ifindex
    via /sys/class/net.
    """

    if peer_ifindex is None:
        return None

    try:
        peer_ifindex = int(peer_ifindex)
    except ValueError:
        return None

    for iface in os.listdir("/sys/class/net"):
        path = f"/sys/class/net/{iface}/ifindex"

        try:
            with open(path) as f:
                ifindex = int(f.read().strip())
                if ifindex == peer_ifindex:
                    return iface
        except Exception:
            continue

    return None














"""
from pathlib import Path


def get_host_veth(peer_ifindex: str):
    
    #Resolve host-side veth interface name using /sys.

    #peer_ifindex:
    #    The interface index extracted from container namespace
    #    (e.g., eth0@if43 → 43)

    #Returns:
    #    Host interface name whose ifindex matches peer_ifindex.
    

    if not peer_ifindex:
        return None

    sys_class_net = Path("/sys/class/net")

    for iface_path in sys_class_net.iterdir():
        ifindex_file = iface_path / "ifindex"

        if not ifindex_file.exists():
            continue

        try:
            with ifindex_file.open() as f:
                ifindex = f.read().strip()

            if ifindex == str(peer_ifindex):
                return iface_path.name

        except Exception:
            continue

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













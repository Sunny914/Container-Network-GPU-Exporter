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









#import subprocess

#def get_host_veth(peer_ifindex: str):
#    if not peer_ifindex:
#        return None
#
#    cmd = ["ip", "-o", "link", "show"]
#    output = subprocess.check_output(cmd, text=True)
#
#    for line in output.splitlines():
#        if line.startswith(f"{peer_ifindex}:"):
#            return line.split(":")[1].strip().split("@")[0]

#    return None










"""
def get_host_veth(peer_ifindex):
    if not peer_ifindex:
        return None

    with open("/proc/net/dev", "r") as f:
        for line in f:
            if line.strip().startswith(str(peer_ifindex) + ":"):
                return line.split(":")[0].strip()

    return None

"""
import subprocess
import re


def get_container_net_info(pid: int):
    """
    Discover container network interface, IP, and peer ifindex
    by inspecting the container's default route.
    """

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
import subprocess
import re


def get_container_net_info(pid: int) -> dict:
    
    #Inspect container network namespace and extract:
    #- container interface
    #- container IP
    #- peer ifindex (host veth index)
    
    cmd = ["nsenter", "-t", str(pid), "-n", "ip", "-o", "addr"]
    output = subprocess.check_output(cmd, text=True)

    for line in output.splitlines():
        if "eth0@" in line:
            # Example:
            # 2: eth0@if151 inet 172.19.0.2/16 ...
            iface = "eth0"

            ip_match = re.search(r"inet (\S+)", line)
            peer_match = re.search(r"@if(\d+)", line)

            return {
                "interface": iface,
                "ip": ip_match.group(1) if ip_match else None,
                "peer_ifindex": peer_match.group(1) if peer_match else None,
            }

    raise RuntimeError("eth0 not found in container network namespace")

"""

































"""
import subprocess
import re

def get_container_net_info(pid: int):
    cmd = ["nsenter", "-t", str(pid), "-n", "ip", "-o", "addr"]
    output = subprocess.check_output(cmd, text=True)
    print(output)
    for line in output.splitlines():
        if "eth0" in line:
            # example: eth0@if43 inet 172.18.0.3/16
            iface = "eth0"
            ip_match = re.search(r"inet (\S+)", line)
            peer_match = re.search(r"@if(\d+)", line)

            return {
                "interface": iface,
                "ip": ip_match.group(1) if ip_match else None,
                "peer_ifindex": peer_match.group(1) if peer_match else None
            }
        

    raise RuntimeError("eth0 not found in container netns")

"""

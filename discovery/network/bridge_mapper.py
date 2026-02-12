# discovery/network/bridge_mapper.py

import os

def get_bridge_for_veth(host_veth: str):
    """
    Determine Linux bridge for a given host veth
    by reading /sys/class/net/<iface>/master.
    """

    if not host_veth:
        return None

    master_path = f"/sys/class/net/{host_veth}/master"

    if not os.path.exists(master_path):
        return None

    try:
        bridge = os.path.basename(os.readlink(master_path))
        return bridge
    except Exception:
        return None



















"""
from pathlib import Path


def get_bridge_for_veth(veth: str):
    
    # Resolve Linux bridge name for a given host veth interface
    # using /sys filesystem.

    # Returns:
    #    Bridge name if attached
    
    #    None if not part of a bridge
    

    if not veth:
        return None

    master_path = Path(f"/sys/class/net/{veth}/master")

    if not master_path.exists():
        return None

    try:
        # Resolve symlink target
        bridge_path = master_path.resolve()
        return bridge_path.name

    except Exception:
        return None
    



"""





















"""
import subprocess
import re


def get_bridge_for_veth(veth: str) -> str | None:
    
   # Resolve Linux bridge a veth is attached to.
    
    if not veth:
        return None

    cmd = ["ip", "link", "show", veth]
    output = subprocess.check_output(cmd, text=True)

    match = re.search(r"master (\S+)", output)
    if match:
        return match.group(1)

    return None

"""
































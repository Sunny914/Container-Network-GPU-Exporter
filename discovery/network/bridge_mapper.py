import subprocess
import re


def get_bridge_for_veth(veth: str):
    if not veth:
        return None

    cmd = ["ip", "link", "show", veth]
    output = subprocess.check_output(cmd, text=True)

    match = re.search(r"master (\S+)", output)
    if match:
        return match.group(1)

    return None




















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
































"""
import subprocess
import re


def get_bridge_for_veth(veth: str) -> str | None:
    
    #Resolve Linux bridge a veth is attached to.
    
    if not veth:
        return None

    cmd = ["ip", "link", "show", veth]
    output = subprocess.check_output(cmd, text=True)

    match = re.search(r"master (\S+)", output)
    if match:
        return match.group(1)

    return None

"""



























"""
import subprocess
import re


def get_bridge_for_veth(veth: str):
    if not veth:
        return None

    cmd = ["ip", "link", "show", veth]
    output = subprocess.check_output(cmd, text=True)

    match = re.search(r"master (\S+)", output)
    if match:
        return match.group(1)

    return None

"""






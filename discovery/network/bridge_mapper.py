import subprocess
import re

def get_bridge_for_veth(veth):
    if not veth:
        return None


def get_bridge_for_veth(veth: str) -> str:
    cmd = ["ip", "link", "show", veth]
    output = subprocess.check_output(cmd, text=True)

    match = re.search(r"master (\S+)", output)
    if match:
        return match.group(1)

    raise RuntimeError("Bridge not found for veth")

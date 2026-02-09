import subprocess


def get_physical_nic() -> str:
    """
    Determine the physical NIC used for outbound traffic
    using host routing table.
    """
    cmd = ["ip", "route", "get", "8.8.8.8"]
    output = subprocess.check_output(cmd, text=True)

    parts = output.split()
    if "dev" in parts:
        return parts[parts.index("dev") + 1]

    return "unknown"































"""
import subprocess
import re
from typing import Optional, Dict


def _run(cmd: list) -> str:
    
    #Run a shell command and return stripped output.
    #Raises CalledProcessError if command fails.
    
    return subprocess.check_output(cmd, text=True).strip()


def get_route_info(
    target_ip: str = "8.8.8.8",
    pid: Optional[int] = None
) -> Dict[str, Optional[str]]:
    
    #Determine egress routing information.

    #If pid is provided:
    #    - Execute inside the container's network namespace
    #If pid is None:
    #    - Execute on the host network namespace

    #Returns:
    #    {
    #        "egress_iface": str | None,
    #        "src_ip": str | None,
    #        "raw": str
    #    }
    
    

    # Build command
    if pid:
        cmd = [
            "nsenter",
            "-t", str(pid),
            "-n",
            "ip", "route", "get", target_ip
        ]
    else:
        cmd = ["ip", "route", "get", target_ip]

    try:
        output = _run(cmd)
    except Exception:
        return {
            "egress_iface": None,
            "src_ip": None,
            "raw": ""
        }

    # Example output:
    # 8.8.8.8 via 172.19.0.1 dev eth0 src 172.19.0.2 uid 0
    dev_match = re.search(r"\bdev\s+(\S+)", output)
    src_match = re.search(r"\bsrc\s+(\S+)", output)

    return {
        "egress_iface": dev_match.group(1) if dev_match else None,
        "src_ip": src_match.group(1) if src_match else None,
        "raw": output
    }

"""










"""
def get_physical_nic():
    try:
        out = subprocess.check_output(
            ["ip", "route", "show", "default"],
            text=True
        ).strip()

        if not out:
            return None

        parts = out.split()

        if "dev" in parts:
            return parts[parts.index("dev") + 1]

        # Fallback: no dev keyword (Docker / bridge / minimal route)
        return "unknown"

    except Exception:
        return "unknown"
"""







"""
import subprocess

def get_physical_nic() -> str:
    cmd = ["ip", "route", "show", "default"]
    output = subprocess.check_output(cmd, text=True)

    # example: default via 192.168.31.1 dev wlp0s20f3
    parts = output.split()
    return parts[parts.index("dev") + 1]
"""
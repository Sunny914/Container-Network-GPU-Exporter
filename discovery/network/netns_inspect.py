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

import subprocess

def get_physical_nic() -> str:
    cmd = ["ip", "route", "show", "default"]
    output = subprocess.check_output(cmd, text=True)

    # example: default via 192.168.31.1 dev wlp0s20f3
    parts = output.split()
    return parts[parts.index("dev") + 1]

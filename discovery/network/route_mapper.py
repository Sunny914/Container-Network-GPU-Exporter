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
import subprocess

def get_physical_nic() -> str:
    cmd = ["ip", "route", "show", "default"]
    output = subprocess.check_output(cmd, text=True)

    # example: default via 192.168.31.1 dev wlp0s20f3
    parts = output.split()
    return parts[parts.index("dev") + 1]
"""
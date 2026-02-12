def get_physical_nic() -> str:
    """
    Determine the physical NIC used for outbound traffic
    by reading /proc/net/route directly.
    """

    try:
        with open("/proc/net/route") as f:
            lines = f.readlines()
    except Exception:
        return "unknown"

    # Skip header line
    for line in lines[1:]:
        parts = line.strip().split()

        if len(parts) < 2:
            continue

        iface = parts[0]
        destination = parts[1]

        # Destination 00000000 means default route
        if destination == "00000000":
            return iface

    return "unknown"











"""
def get_physical_nic():
    
#    Determine host physical NIC using /proc/net/route.
    

    try:
        with open("/proc/net/route") as f:
            for line in f.readlines()[1:]:
                parts = line.strip().split()

                iface = parts[0]
                destination = parts[1]

                # 00000000 = default route
                if destination == "00000000":
                    return iface
    except Exception:
        pass

    return None

"""















"""
import subprocess


def get_physical_nic() -> str:
    
    #Determine the physical NIC used for outbound traffic
    #using host routing table.
    
    cmd = ["ip", "route", "get", "8.8.8.8"]
    output = subprocess.check_output(cmd, text=True)

    parts = output.split()
    if "dev" in parts:
        return parts[parts.index("dev") + 1]

    return "unknown"



"""
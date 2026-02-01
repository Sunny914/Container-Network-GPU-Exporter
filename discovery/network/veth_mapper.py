def get_host_veth(peer_ifindex):
    if not peer_ifindex:
        return None

    with open("/proc/net/dev", "r") as f:
        for line in f:
            if line.strip().startswith(str(peer_ifindex) + ":"):
                return line.split(":")[0].strip()

    return None


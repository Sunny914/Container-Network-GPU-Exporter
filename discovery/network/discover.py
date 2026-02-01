from .container_pid import get_container_pid
from .netns_inspect import get_container_net_info
from .veth_mapper import get_host_veth
from .bridge_mapper import get_bridge_for_veth
from .route_mapper import get_physical_nic

def discover_network_topology(container_name: str):
    pid = get_container_pid(container_name)
    net = get_container_net_info(pid)

    #veth = get_host_veth(net["peer_ifindex"])
    #bridge = get_bridge_for_veth(veth)
    veth = get_host_veth(net.get("peer_ifindex"))
    net["host_veth"] = veth
    if veth:
        bridge = get_bridge_for_veth(veth)
    else:
        bridge = None
    net["bridge"] = bridge or "direct-or-host"

    nic = get_physical_nic()

    return {
        "container": container_name,
        "pid": pid,
        "container_interface": net["interface"],
        "container_ip": net["ip"],
        "host_veth": veth,
        "bridge": bridge,
        "physical_nic": nic
    }

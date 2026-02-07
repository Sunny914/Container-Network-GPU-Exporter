from .container_pid import get_container_pid
from .netns_inspect import get_container_net_info
from .veth_mapper import get_host_veth
from .bridge_mapper import get_bridge_for_veth
from .route_mapper import get_physical_nic


def discover_network_topology(container_name: str):
    # Get container metadata
    meta = get_container_pid(container_name)
    pid = meta["pid"]
    container_id = meta["container_id"]

    # Inspect container network namespace
    net = get_container_net_info(pid)

    # Resolve host-side veth
    veth = get_host_veth(net.get("peer_ifindex"))
    net["host_veth"] = veth

    # Resolve bridge
    if veth:
        bridge = get_bridge_for_veth(veth)
    else:
        bridge = None

    net["bridge"] = bridge or "direct-or-host"

    # Resolve physical NIC
    nic = get_physical_nic()

    return {
        "container": container_name,
        "container_id": container_id,
        "pid": pid,
        "container_interface": net["interface"],
        "container_ip": net["ip"],
        "host_veth": veth,
        "bridge": bridge,
        "physical_nic": nic,
    }

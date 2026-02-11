# exporter/network_exporter.py

import time
from prometheus_client import start_http_server

from discovery.network.discover import discover_network_topology

from exporter.metrics import (
    container_network_info,
    container_veth_info,
    container_bridge_info,
    container_physical_nic_info,
)


def publish_network_topology(container_name: str):
    topo = discover_network_topology(container_name)

    container = topo.get("container", "unknown")
    container_id = topo.get("container_id", "unknown")
    pid = str(topo.get("pid", "unknown"))
    iface = topo.get("container_interface", "unknown")
    ip = topo.get("container_ip", "unknown")
    host_veth = topo.get("host_veth", "unknown")
    bridge = topo.get("bridge", "unknown")
    physical_nic = topo.get("physical_nic", "unknown")

    # Clear previous metrics (important to avoid stale labels)
    container_network_info.clear()
    container_veth_info.clear()
    container_bridge_info.clear()
    container_physical_nic_info.clear()

    # 1️⃣ Container network info
    container_network_info.labels(
        container=container,
        container_id=container_id,
        pid=pid,
        container_iface=iface,
        container_ip=ip,
    ).set(1)

    # 2️⃣ Veth mapping
    container_veth_info.labels(
        container=container,
        host_veth=host_veth,
    ).set(1)

    # 3️⃣ Bridge mapping
    container_bridge_info.labels(
        container=container,
        bridge=bridge,
    ).set(1)

    # 4️⃣ Physical NIC mapping
    container_physical_nic_info.labels(
        container=container,
        physical_nic=physical_nic,
    ).set(1)


def main():
    start_http_server(9500)
    print("Network topology exporter running on :9500/metrics")

    target_container = "bridge-test"

    while True:
        publish_network_topology(target_container)
        time.sleep(30)


if __name__ == "__main__":
    main()























"""# Network Topology Exporter
#This exporter discovers and publishes network topology of a target container
#as Prometheus metrics.
import time
from prometheus_client import start_http_server

from discovery.network.discover import discover_network_topology
from exporter.metrics import container_network_topology_info


def publish_network_topology(container_name: str):
    topo = discover_network_topology(container_name)

    container_network_topology_info.labels(
        container=topo.get("container", "unknown"),
        container_id=topo.get("container_id", "unknown"),
        pid=str(topo.get("pid", "unknown")),
        container_iface=topo.get("container_interface", "unknown"),
        container_ip=topo.get("container_ip", "unknown"),
        host_veth=topo.get("host_veth") or "direct-or-host",
        bridge=topo.get("bridge", "direct-or-host"),
        physical_nic=topo.get("physical_nic", "unknown"),
    ).set(1)


def main():
    start_http_server(9500)
    print("Network topology exporter running on :9500/metrics")

    target_container = "bridge-test"

    while True:
        publish_network_topology(target_container)
        time.sleep(30)


if __name__ == "__main__":
    main()


"""















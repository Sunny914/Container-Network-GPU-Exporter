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
        bridge=topo.get("bridge") or "direct-or-host",
        physical_nic=topo.get("physical_nic", "unknown"),
    ).set(1)


def main():
    # Start HTTP server
    start_http_server(9500)
    print("Network topology exporter running on :9500/metrics")

    # In real systems this would loop over all containers
    #target_container = "cadvisor"
    target_container = "bridge-test"


    while True:
        publish_network_topology(target_container)
        time.sleep(30)  # topology is slow-changing


if __name__ == "__main__":
    main()

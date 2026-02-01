from prometheus_client import Gauge

container_network_topology_info = Gauge(
    name="container_network_topology_info",
    documentation="Container to physical network topology mapping",
    labelnames=[
        "container",
        "container_id",
        "pid",
        "container_iface",
        "container_ip",
        "host_veth",
        "bridge",
        "physical_nic",
    ],
)


gpu_container_topology_info = Gauge(
    "gpu_container_topology_info",
    "GPU to container topology mapping",
    labelnames=[
        "gpu_index",
        "pid",
        "container_id",
        "container_name",
    ],
)

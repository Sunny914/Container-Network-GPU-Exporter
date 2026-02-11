# exporter/metrics.py

from prometheus_client import Gauge

# 1️⃣ Container namespace level
container_network_info = Gauge(
    name="container_network_info",
    documentation="Container network namespace details",
    labelnames=[
        "container",
        "container_id",
        "pid",
        "container_iface",
        "container_ip",
    ],
)

# 2️⃣ Host veth mapping
container_veth_info = Gauge(
    name="container_veth_info",
    documentation="Container to host veth mapping",
    labelnames=[
        "container",
        "host_veth",
    ],
)

# 3️⃣ Bridge mapping
container_bridge_info = Gauge(
    name="container_bridge_info",
    documentation="Host veth to bridge mapping",
    labelnames=[
        "container",
        "bridge",
    ],
)

# 4️⃣ Physical NIC mapping
container_physical_nic_info = Gauge(
    name="container_physical_nic_info",
    documentation="Bridge to physical NIC mapping",
    labelnames=[
        "container",
        "physical_nic",
    ],
)


# GPU to container topology mapping
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






















"""
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


"""
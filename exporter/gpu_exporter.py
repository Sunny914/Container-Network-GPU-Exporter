from prometheus_client import Gauge, start_http_server
from discovery.gpu.gpu_container_map import get_gpu_container_map
import time

gpu_process_gauge = Gauge(
    "gpu_container_process_info",
    "GPU process mapped to container",
    ["gpu_index", "pid", "container_id", "container_name"]
)

def collect_gpu_topology():
    gpu_process_gauge.clear()

    records = get_gpu_container_map() or []

    for record in records:
        gpu_process_gauge.labels(
            gpu_index=str(record.get("gpu_index", "unknown")),
            pid=str(record.get("pid", "unknown")),
            container_id=record.get("container_id", "unknown"),
            container_name=record.get("container_name", "unknown"),
        ).set(1)

def main():
    start_http_server(9600, addr="0.0.0.0")
    print("GPU topology exporter running on :9600")

    while True:
        collect_gpu_topology()
        time.sleep(10)

if __name__ == "__main__":
    main()









"""
import time
from prometheus_client import start_http_server

from discovery.gpu.gpu_container_map import get_gpu_container_map
from exporter.metrics import gpu_container_topology_info


def collect_gpu_topology():
    gpu_container_topology_info.clear()

    mapping = get_gpu_container_map()

    for gpu_index, processes in mapping.items():
        for p in processes:
            gpu_container_topology_info.labels(
                gpu_index=str(gpu_index),
                pid=str(p["pid"]),
                container_id=p["container_id"] or "host",
                container_name=p["container_name"] or "host",
            ).set(1)


def main():
    start_http_server(9600)
    print("GPU topology exporter running on :9600/metrics")

    while True:
        collect_gpu_topology()
        time.sleep(10)


if __name__ == "__main__":
    main()

 """   

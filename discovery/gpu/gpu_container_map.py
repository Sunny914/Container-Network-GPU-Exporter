# discovery/gpu/gpu_container_map.py

from discovery.gpu.gpu_processes import get_gpu_processes
from discovery.gpu.pid_to_container import pid_to_container_id
from discovery.gpu.container_lookup import container_id_to_name


def get_gpu_container_map():
    """
    Returns a list of GPU processes mapped to Docker containers.

    Each entry:
    {
        gpu_index: int
        pid: int
        process_name: str
        used_gpu_memory_bytes: int
        container_id: str
        container_name: str
    }
    """
    results = []

    gpu_processes = get_gpu_processes()

    for proc in gpu_processes:
        pid = proc.get("pid")
        if not pid:
            continue

        # Step 1: PID -> Container ID
        container_id = pid_to_container_id(pid)
        if not container_id:
            # Host process (e.g. gnome-shell)
            continue

        # Step 2: Container ID -> Container Name
        container_name = container_id_to_name(container_id)
        if not container_name:
            # Container may have exited
            continue

        results.append({
            "gpu_index": proc.get("gpu_index"),
            "pid": pid,
            "process_name": proc.get("process_name"),
            "used_gpu_memory_bytes": proc.get("used_gpu_memory_bytes"),
            "container_id": container_id,
            "container_name": container_name,
        })

    return results








import subprocess
import json


def get_gpu_inventory():
    """
    Phase 1: Discover physical GPUs on the host.

    Returns:
        List[dict]: One dict per GPU with stable hardware identity
    """

    cmd = [
        "nvidia-smi",
        "--query-gpu=index,uuid,name,pci.bus_id,memory.total",
        "--format=csv,noheader,nounits",
    ]

    try:
        output = subprocess.check_output(cmd, text=True)
    except Exception as e:
        raise RuntimeError(f"Failed to run nvidia-smi: {e}")

    gpus = []

    for line in output.strip().split("\n"):
        index, uuid, name, pci_bus_id, memory_total = [
            item.strip() for item in line.split(",")
        ]

        gpus.append(
            {
                "gpu_index": int(index),
                "uuid": uuid,
                "name": name,
                "pci_bus_id": pci_bus_id,
                "memory_total_mb": int(memory_total),
            }
        )

    return gpus

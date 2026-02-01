# discovery/gpu/gpu_processes.py

from pynvml import (
    nvmlInit,
    nvmlShutdown,
    nvmlDeviceGetHandleByIndex,
    nvmlDeviceGetComputeRunningProcesses,
    nvmlDeviceGetGraphicsRunningProcesses,
    nvmlDeviceGetCount,
)

def get_gpu_processes():
    """
    Returns a list of:
    {
        gpu_index,
        pid,
        used_memory_mb
    }
    """
    nvmlInit()

    results = []
    device_count = nvmlDeviceGetCount()

    for gpu_index in range(device_count):
        handle = nvmlDeviceGetHandleByIndex(gpu_index)

        # Compute workloads (CUDA, ML, etc.)
        compute_procs = nvmlDeviceGetComputeRunningProcesses(handle)

        # Graphics workloads (sometimes containers use this)
        graphics_procs = nvmlDeviceGetGraphicsRunningProcesses(handle)

        for proc in compute_procs + graphics_procs:
            results.append({
                "gpu_index": gpu_index,
                "pid": proc.pid,
                "used_memory_mb": proc.usedGpuMemory // (1024 * 1024)
            })

    nvmlShutdown()
    return results

# discovery/gpu/pid_to_container.py

from pathlib import Path

def pid_to_container_id(pid: int):
    cgroup_file = Path(f"/proc/{pid}/cgroup")

    if not cgroup_file.exists():
        return None

    with cgroup_file.open() as f:
        for line in f:
            if "docker-" in line and ".scope" in line:
                return line.split("docker-")[-1].split(".scope")[0]

            if "/docker/" in line:
                return line.split("/docker/")[-1][:64]

    return None
















"""
import os
import re
import subprocess
from typing import Optional, Dict


DOCKER_CGROUP_REGEX = re.compile(r"/docker/([a-f0-9]{12,64})")


def get_container_id_from_pid(pid: int) -> Optional[str]:
    
    #Given a Linux PID, return the Docker container ID it belongs to.
    #Returns None if the process is a host process.
    
    cgroup_path = f"/proc/{pid}/cgroup"

    if not os.path.exists(cgroup_path):
        return None

    try:
        with open(cgroup_path, "r") as f:
            for line in f:
                match = DOCKER_CGROUP_REGEX.search(line)
                if match:
                    return match.group(1)
    except Exception:
        return None

    return None


def get_container_name(container_id: str) -> Optional[str]:
    
    #Given a Docker container ID, return container name.
    
    try:
        result = subprocess.check_output(
            ["docker", "inspect", "--format", "{{.Name}}", container_id],
            stderr=subprocess.DEVNULL,
            text=True,
        ).strip()

        # Docker returns name with leading slash
        return result.lstrip("/") if result else None

    except subprocess.CalledProcessError:
        return None


def map_pid_to_container(pid: int) -> Dict[str, Optional[str]]:
    
    #High-level helper:
    #PID → container_id → container_name
    
    container_id = get_container_id_from_pid(pid)

    if not container_id:
        return {
            "pid": pid,
            "container_id": None,
            "container_name": None,
            "scope": "host",
        }

    container_name = get_container_name(container_id)

    return {
        "pid": pid,
        "container_id": container_id,
        "container_name": container_name,
        "scope": "container",
    }
"""
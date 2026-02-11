# discovery/network/container_pid.py

from discovery.docker_client import get_container


def get_container_metadata(container_name: str):
    """
    Returns container metadata using Docker SDK.

    Output:
    {
        "container_id": str,
        "pid": int,
        "name": str
    }
    """
    container = get_container(container_name)

    return {
        "container_id": container.id,
        "pid": container.attrs["State"]["Pid"],
        "name": container.name,
    }
































"""
import subprocess
import json


def get_container_pid(container_name: str) -> dict:
    
   # Return container metadata needed for namespace discovery.
    
    cmd = ["docker", "inspect", container_name]
    output = subprocess.check_output(cmd, text=True)
    data = json.loads(output)[0]

    return {
        "pid": data["State"]["Pid"],
        "container_id": data["Id"],
    }

"""
































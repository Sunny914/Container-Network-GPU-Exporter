import subprocess
import json


def get_container_pid(container_name: str) -> dict:
    """
    Return container metadata needed for namespace discovery.
    """
    cmd = ["docker", "inspect", container_name]
    output = subprocess.check_output(cmd, text=True)
    data = json.loads(output)[0]

    return {
        "pid": data["State"]["Pid"],
        "container_id": data["Id"],
    }


































"""
import subprocess
import json

def get_container_pid(container_name: str) -> dict:
    
   # Return container metadata (pid + container_id).
    
    cmd = ["docker", "inspect", container_name]
    output = subprocess.check_output(cmd, text=True)
    data = json.loads(output)[0]

    return {
        "pid": data["State"]["Pid"],
        "container_id": data["Id"],
    }


"""

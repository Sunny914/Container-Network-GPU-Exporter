import subprocess
import json

def get_container_pid(container_name: str) -> int:
    cmd = ["docker", "inspect", container_name]
    output = subprocess.check_output(cmd)
    data = json.loads(output)
    return data[0]["State"]["Pid"]

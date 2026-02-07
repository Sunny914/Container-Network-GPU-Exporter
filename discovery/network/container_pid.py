import subprocess
import json

def get_container_pid(container_name: str) -> dict:
    """
    Return container metadata (pid + container_id).
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

def get_container_pid(container_name: str) -> int:
    cmd = ["docker", "inspect", container_name]
    data = json.loads(subprocess.check_output(cmd))
    return data[0]["State"]["Pid"]

def get_container_sandbox_key(container_name: str) -> str:
    cmd = ["docker", "inspect", container_name]
    data = json.loads(subprocess.check_output(cmd))
    return data[0]["NetworkSettings"]["SandboxKey"]
"""
    

 #   return {
 #       "pid": data[0]["State"]["Pid"],
 #       "container_id": data[0]["Id"]
 #   }


#def get_container_pid(container_name: str) -> int:
#    cmd = ["docker", "inspect", container_name]
#    output = subprocess.check_output(cmd)
#    data = json.loads(output)
#    return data[0]["State"]["Pid"]

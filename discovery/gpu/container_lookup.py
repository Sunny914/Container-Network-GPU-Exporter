# discovery/gpu/container_lookup.py
import subprocess

def container_id_to_name(container_id: str):
    if not container_id:
        return None

    try:
        out = subprocess.check_output(
            ["docker", "inspect", container_id, "--format", "{{.Name}}"],
            stderr=subprocess.DEVNULL,
            text=True
        ).strip()

        return out.lstrip("/") if out else None

    except subprocess.CalledProcessError:
        return None


# discovery/docker_client.py

import docker

# Create one global Docker client
_client = docker.from_env()


def get_container(container_name_or_id: str):
    """
    Returns Docker container object using SDK.
    Raises docker.errors.NotFound if container does not exist.
    """
    return _client.containers.get(container_name_or_id)

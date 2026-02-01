from discovery.network.discover import discover_network_topology
import json

if __name__ == "__main__":
    topo = discover_network_topology("cadvisor")
    print(json.dumps(topo, indent=2))

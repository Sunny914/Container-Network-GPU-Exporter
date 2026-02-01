## Container PID
docker inspect cadvisor | grep -i '"Pid"'
cadvisor PID: 176350

## Container Network Interface
Inside container namespace:
- Interface: eth0
- Linked host ifindex: eth0@if43

## Host-side veth
Container eth0 is connected to:
- Host veth interface: 43: veth3d36421@if2

## Container to host veth mapping

Inside container (via nsenter):
- Interface: eth0@if43
- IP: 172.18.0.3/16

Note:
- `if43` refers to the host interface index, not name
- Host-side veth must be resolved using `ip -o link`


## Linux Bridge
veth3d36421@if2 is attached to:
- Bridge: docker0


## Physical Network Card
docker0 forwards traffic to:
- Physical NIC: wlp0s20f3

# Container → Network → Hardware Topology (Docker)

## Overview

Docker containers do not directly attach to physical network cards.
Instead, Linux provides a layered virtual networking model.

This document explains how a container’s network traffic reaches real hardware.

---

## Step-by-Step Network Flow

### 1. Container Network Interface

Inside a container:
- The container sees a virtual interface: `eth0`
- Example IP: `172.18.0.x`
- The interface appears as: `eth0@if43`

This means:
- `eth0` is paired with a host interface having index `43`

---

### 2. veth Pair (Virtual Ethernet)

On the host:
- A veth interface exists (e.g. `veth3d36421`)
- One end is inside the container
- The other end lives on the host

This creates a virtual cable between:

---

### 3. Docker Bridge (Software Switch)

- The host veth is attached to a Docker bridge
- Example: `br-982c07beb42c`
- The bridge connects multiple containers
- This is similar to a VLAN or virtual switch

---

### 4. Host Routing & Physical NIC

Using `ip route`, Linux decides:
- Docker subnet traffic stays on the bridge
- External traffic goes via the default route

Example physical NIC:
- `wlp0s20f3` (Wi-Fi)
- or `eth0` (Ethernet)

---

## Final End-to-End Path


---

## Key Takeaway

Containers never directly see or own hardware.
Linux networking abstracts hardware behind:
- veth interfaces
- bridges
- routing rules

The same abstraction principle applies to GPUs and other accelerators.

# Infra Topology Mapper – Overview

## Problem Statement
Modern containerized workloads abstract away underlying infrastructure,
making it difficult to understand how workloads map to physical resources
such as network interfaces and GPUs.

This project exposes container-to-host topology mappings using kernel-level
inspection and exports them as Prometheus metrics.

## Scope
- Docker containers
- Linux networking
- Network namespaces
- veth pairs
- Linux bridges
- Physical NIC routing












# Network Design Decisions

## Why Use PID-Based Namespace Entry
Linux network namespaces are attached to processes, not containers.
Using PID-based inspection ensures correctness even when container runtimes change.

## Why iproute2 Instead of Docker APIs
Docker APIs abstract away kernel details and can hide actual routing paths.
This project intentionally uses kernel tools for accuracy.

## Why `ip route get 8.8.8.8`
This provides a deterministic way to identify the host’s default outbound NIC
without relying on static configuration.

## Why `direct-or-host` Exists
Some containers bypass bridges entirely (e.g., host networking).
This label explicitly documents that topology instead of hiding it.


# Network Topology Validation

## Validate Container Namespace
nsenter -t <pid> -n ip addr

## Validate Host veth Mapping
ip -o link show | grep veth

## Validate Bridge Membership
ip link show <veth>

## Validate Physical NIC
ip route get 8.8.8.8

## Validate Prometheus Output
curl localhost:9500/metrics | grep container_network_topology_info

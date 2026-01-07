#!/usr/bin/env python3
"""List Lambda Labs instances and available GPU types."""

import argparse
from lambda_client import get_api_client


def list_instances():
    """List all running instances."""
    api = get_api_client()
    instances = api.list_instances()

    if not instances.data:
        print("No running instances")
        return []

    print(f"{'ID':<40} {'Type':<25} {'Status':<10} {'IP':<15} {'Region'}")
    print("-" * 110)
    for i in instances.data:
        print(f"{i.id:<40} {i.instance_type.name:<25} {i.status:<10} {i.ip or 'N/A':<15} {i.region.name}")

    return instances.data


def list_instance_types(available_only: bool = False):
    """List available GPU instance types."""
    api = get_api_client()
    instance_types = api.instance_types()

    print(f"{'Instance Type':<25} {'Price/hr':<10} {'Available Regions'}")
    print("-" * 80)

    for name, it in instance_types.data.items():
        regions = [r.name for r in it.regions_with_capacity_available]
        if available_only and not regions:
            continue
        price = f"${it.instance_type.price_cents_per_hour / 100:.2f}"
        regions_str = ", ".join(regions) if regions else "No capacity"
        print(f"{it.instance_type.name:<25} {price:<10} {regions_str}")


def list_ssh_keys():
    """List registered SSH keys."""
    api = get_api_client()
    keys = api.list_ssh_keys()

    print(f"{'Name':<30} {'ID'}")
    print("-" * 70)
    for key in keys.data:
        print(f"{key.name:<30} {key.id}")


def list_filesystems():
    """List filesystems."""
    api = get_api_client()
    filesystems = api.list_file_systems()

    if not filesystems.data:
        print("No filesystems")
        return

    print(f"{'Name':<30} {'ID':<40} {'Region':<15} {'Mount Path'}")
    print("-" * 110)
    for fs in filesystems.data:
        mount = f"/home/ubuntu/{fs.name}"
        print(f"{fs.name:<30} {fs.id:<40} {fs.region.name:<15} {mount}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="List Lambda Labs resources")
    parser.add_argument("--types", "-t", action="store_true", help="List GPU instance types")
    parser.add_argument("--available", "-a", action="store_true", help="Only show available types")
    parser.add_argument("--keys", "-k", action="store_true", help="List SSH keys")
    parser.add_argument("--filesystems", "-f", action="store_true", help="List filesystems")

    args = parser.parse_args()

    if args.types:
        list_instance_types(args.available)
    elif args.keys:
        list_ssh_keys()
    elif args.filesystems:
        list_filesystems()
    else:
        list_instances()

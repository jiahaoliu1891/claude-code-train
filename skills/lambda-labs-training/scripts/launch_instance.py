#!/usr/bin/env python3
"""Launch a Lambda Labs GPU instance."""

import argparse
import sys
import time
from lambda_cloud_client.models import LaunchInstanceRequest
from lambda_client import get_api_client


def launch_instance(
    instance_type: str,
    ssh_key: str,
    region: str = None,
    filesystem: str = None,
    name: str = None,
    wait: bool = True
):
    """Launch a Lambda Labs instance.

    Args:
        instance_type: GPU instance type (e.g., gpu_1x_a100_sxm4)
        ssh_key: Name of registered SSH key
        region: Region name (auto-selects if None)
        filesystem: Optional filesystem name to attach
        name: Optional instance name
        wait: Wait for instance to become active

    Returns:
        dict with instance_id and ip (if wait=True)
    """
    api = get_api_client()

    # Auto-select region if not specified
    if not region:
        instance_types = api.instance_types()
        for name, it in instance_types.data.items():
            if it.instance_type.name == instance_type:
                if it.regions_with_capacity_available:
                    region = it.regions_with_capacity_available[0].name
                    print(f"Auto-selected region: {region}")
                    break
        if not region:
            print(f"Error: No capacity available for {instance_type}")
            sys.exit(1)

    # Build request
    request_params = {
        "region_name": region,
        "instance_type_name": instance_type,
        "ssh_key_names": [ssh_key],
    }
    if filesystem:
        request_params["file_system_names"] = [filesystem]
    if name:
        request_params["name"] = name

    request = LaunchInstanceRequest(**request_params)

    print(f"Launching {instance_type} in {region}...")
    result = api.launch_instance(request)
    instance_id = result.data.instance_ids[0]
    print(f"Instance ID: {instance_id}")

    if not wait:
        return {"instance_id": instance_id}

    # Wait for instance to be ready
    print("Waiting for instance to become active...")
    while True:
        instances = api.list_instances()
        instance = next((i for i in instances.data if i.id == instance_id), None)
        if instance and instance.status == "active":
            print(f"Instance ready!")
            print(f"IP: {instance.ip}")
            print(f"SSH: ssh -i <key.pem> ubuntu@{instance.ip}")
            return {"instance_id": instance_id, "ip": instance.ip}
        time.sleep(10)
        print("  Still waiting...")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Launch Lambda Labs instance")
    parser.add_argument("--type", "-t", required=True, help="Instance type (e.g., gpu_1x_a100_sxm4)")
    parser.add_argument("--ssh-key", "-k", required=True, help="SSH key name")
    parser.add_argument("--region", "-r", help="Region (auto-selects if not specified)")
    parser.add_argument("--filesystem", "-f", help="FileSystem name to attach")
    parser.add_argument("--name", "-n", help="Instance name")
    parser.add_argument("--no-wait", action="store_true", help="Don't wait for instance")

    args = parser.parse_args()
    launch_instance(
        instance_type=args.type,
        ssh_key=args.ssh_key,
        region=args.region,
        filesystem=args.filesystem,
        name=args.name,
        wait=not args.no_wait
    )

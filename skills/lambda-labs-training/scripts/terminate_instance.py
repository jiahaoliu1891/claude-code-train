#!/usr/bin/env python3
"""Terminate Lambda Labs GPU instances."""

import argparse
from lambda_cloud_client.models import TerminateInstanceRequest
from lambda_client import get_api_client


def terminate_instance(instance_ids: list[str]):
    """Terminate one or more Lambda Labs instances.

    Args:
        instance_ids: List of instance IDs to terminate
    """
    api = get_api_client()

    request = TerminateInstanceRequest(instance_ids=instance_ids)
    api.terminate_instance(request)

    for iid in instance_ids:
        print(f"Terminated: {iid}")


def terminate_all():
    """Terminate all running instances."""
    api = get_api_client()
    instances = api.list_instances()

    if not instances.data:
        print("No running instances")
        return

    ids = [i.id for i in instances.data]
    terminate_instance(ids)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Terminate Lambda Labs instances")
    parser.add_argument("instance_ids", nargs="*", help="Instance IDs to terminate")
    parser.add_argument("--all", action="store_true", help="Terminate all instances")

    args = parser.parse_args()

    if args.all:
        terminate_all()
    elif args.instance_ids:
        terminate_instance(args.instance_ids)
    else:
        parser.print_help()

#!/usr/bin/env python3
"""Shared Lambda Labs API client setup."""

import os
import lambda_cloud_client
from dotenv import load_dotenv


def get_api_client():
    """Initialize and return Lambda Labs API client."""
    load_dotenv()
    api_key = os.getenv("LAMBDA_LAB_API_KEY")
    if not api_key:
        raise ValueError("LAMBDA_LAB_API_KEY not found in environment")

    config = lambda_cloud_client.Configuration(
        host="https://cloud.lambdalabs.com/api/v1",
        access_token=api_key
    )
    client = lambda_cloud_client.ApiClient(config)
    return lambda_cloud_client.DefaultApi(client)


if __name__ == "__main__":
    api = get_api_client()
    print("Lambda Labs API client initialized successfully")

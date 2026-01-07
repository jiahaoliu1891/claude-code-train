"""Test connection to Lambda Labs Cloud API"""
import os
from dotenv import load_dotenv
import lambda_cloud_client
from lambda_cloud_client.rest import ApiException

load_dotenv()

API_KEY = os.getenv("LAMBDA_LAB_API_KEY")

if not API_KEY:
    print("Error: LAMBDA_LAB_API_KEY not found in .env")
    exit(1)

configuration = lambda_cloud_client.Configuration(
    host="https://cloud.lambdalabs.com/api/v1",
    access_token=API_KEY
)

with lambda_cloud_client.ApiClient(configuration) as api_client:
    api = lambda_cloud_client.DefaultApi(api_client)

    # List available instance types
    print("=" * 60)
    print("Available GPU Instance Types:")
    print("=" * 60)
    try:
        instance_types = api.instance_types()
        for name, details in instance_types.data.items():
            specs = details.instance_type.specs
            regions = [r.name for r in details.regions_with_capacity_available]
            print(f"\n{name}:")
            print(f"  Description: {details.instance_type.description}")
            print(f"  vCPUs: {specs.vcpus}, RAM: {specs.memory_gib}GB, Storage: {specs.storage_gib}GB")
            print(f"  Price: ${details.instance_type.price_cents_per_hour/100:.2f}/hr")
            print(f"  Available regions: {regions if regions else 'None'}")
    except ApiException as e:
        print(f"Error fetching instance types: {e}")

    # List current instances
    print("\n" + "=" * 60)
    print("Current Running Instances:")
    print("=" * 60)
    try:
        instances = api.list_instances()
        if instances.data:
            for inst in instances.data:
                print(f"\n{inst.name} ({inst.id}):")
                print(f"  Type: {inst.instance_type.name}")
                print(f"  Status: {inst.status}")
                print(f"  IP: {inst.ip}")
                print(f"  Region: {inst.region.name}")
        else:
            print("No instances currently running.")
    except ApiException as e:
        print(f"Error fetching instances: {e}")

    # List SSH keys
    print("\n" + "=" * 60)
    print("SSH Keys:")
    print("=" * 60)
    try:
        ssh_keys = api.list_ssh_keys()
        if ssh_keys.data:
            for key in ssh_keys.data:
                print(f"  - {key.name} (id: {key.id})")
        else:
            print("No SSH keys registered.")
    except ApiException as e:
        print(f"Error fetching SSH keys: {e}")

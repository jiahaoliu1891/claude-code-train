---
name: lambda-labs-training
description: "Train deep learning models on Lambda Labs Cloud GPU instances. Use when: (1) User wants to train ML/DL models on cloud GPUs, (2) User mentions Lambda Labs, (3) User needs to launch/manage GPU instances, (4) User wants to run training on A100/H100 GPUs, (5) User needs persistent storage for checkpoints."
---

# Lambda Labs GPU Training

Train deep learning models on Lambda Labs Cloud with persistent storage and cost optimization.

## Prerequisites

1. **API Key**: Store in `.env` as `LAMBDA_LAB_API_KEY`
2. **SSH Key**: Register at https://cloud.lambdalabs.com/ssh-keys, store private key locally
3. **Dependencies**: `pip install lambda-cloud-client python-dotenv`

## Workflow

### 1. Check Available Resources

```bash
# List GPU types with availability
python scripts/list_instances.py --types --available

# List SSH keys
python scripts/list_instances.py --keys

# List filesystems
python scripts/list_instances.py --filesystems
```

### 2. Launch Instance

```bash
python scripts/launch_instance.py \
    --type gpu_1x_a100_sxm4 \
    --ssh-key your-key-name \
    --filesystem your-filesystem \
    --name training-run
```

The script auto-selects an available region and waits for the instance to become active.

### 3. Setup and Train

```bash
# SSH into instance
ssh -i ~/path/to/key.pem ubuntu@<instance-ip>

# Clone repo
git clone https://github.com/your/repo.git && cd repo

# Prepare data (if needed)
python data/prepare.py

# Run training (save to FileSystem for persistence!)
python train.py --out_dir=/home/ubuntu/<filesystem>/checkpoints
```

### 4. Download Results

```bash
# From local machine
scp -i ~/path/to/key.pem ubuntu@<ip>:/home/ubuntu/<filesystem>/checkpoints/ckpt.pt ./local/
```

### 5. Terminate Instance

```bash
# By ID
python scripts/terminate_instance.py <instance-id>

# Or terminate all
python scripts/terminate_instance.py --all
```

## Critical: Persistent Storage

**Always save checkpoints to FileSystem**, not instance local storage. Instance storage is lost on termination.

```bash
# WRONG - checkpoint lost on termination
python train.py --out_dir=./out

# CORRECT - checkpoint persists
python train.py --out_dir=/home/ubuntu/<filesystem-name>/out
```

FileSystem mount: `/home/ubuntu/<name>` → `/lambda/nfs/<name>`

## Resources

- **scripts/**: API client and CLI tools for instance management
- **references/gpu_instances.md**: GPU types, pricing, selection guide
- **references/troubleshooting.md**: Common errors and fixes

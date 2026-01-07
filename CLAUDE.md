# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a research project exploring whether Claude Code can be effectively used to train LLMs and other deep learning models. The goal is to evaluate Claude Code's capabilities in ML/DL training workflows, including:
- Data preprocessing and pipeline setup
- Model architecture implementation
- Training loop development
- Experiment tracking and hyperparameter tuning
- Debugging and optimization

## Infrastructure: Lambda Labs Cloud

GPU resources are provisioned via Lambda Labs Cloud API.

### Setup
- API Key stored in `.env` as `LAMBDA_LAB_API_KEY`
- Python client: `pip install lambda-cloud-client python-dotenv`
- Test connection: `python lambda_test.py`

### Available GPU Instances (commonly used)

| Instance Type | GPU | Price/hr | Use Case |
|---------------|-----|----------|----------|
| `gpu_1x_a10` | 1x A10 (24GB) | $0.75 | Testing, small models |
| `gpu_1x_a100_sxm4` | 1x A100 (40GB) | $1.29 | Medium training |
| `gpu_1x_h100_sxm5` | 1x H100 (80GB) | $3.29 | Large models |
| `gpu_8x_a100` | 8x A100 (40GB) | $10.32 | Distributed training |
| `gpu_8x_h100_sxm5` | 8x H100 (80GB) | $23.92 | Large-scale training |

### Pre-installed Environment (Lambda Stack)

Instances run Ubuntu 22.04 LTS with Lambda Stack pre-installed:
- **NVIDIA**: CUDA, cuDNN, NCCL, drivers
- **Frameworks**: PyTorch, TensorFlow, JAX, Keras, Triton
- **Tools**: JupyterLab, Git, tmux, htop, Docker

### API Usage

```python
import lambda_cloud_client
from dotenv import load_dotenv
import os

load_dotenv()
config = lambda_cloud_client.Configuration(
    host="https://cloud.lambdalabs.com/api/v1",
    access_token=os.getenv("LAMBDA_LAB_API_KEY")
)

with lambda_cloud_client.ApiClient(config) as client:
    api = lambda_cloud_client.DefaultApi(client)
    # api.instance_types() - list available instances
    # api.list_instances() - list running instances
    # api.launch_instance() - start new instance
    # api.terminate_instance() - stop instance
    # api.list_ssh_keys() - list SSH keys
```

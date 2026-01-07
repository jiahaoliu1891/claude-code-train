# GPU Instance Types

## Common Instances

| Instance Type | GPU | VRAM | Price/hr | Use Case |
|---------------|-----|------|----------|----------|
| `gpu_1x_a10` | 1x A10 | 24GB | $0.75 | Testing, small models |
| `gpu_1x_a100_sxm4` | 1x A100 | 40GB | $1.29 | Medium training |
| `gpu_1x_h100_sxm5` | 1x H100 | 80GB | $3.29 | Large models |
| `gpu_8x_a100` | 8x A100 | 320GB | $10.32 | Distributed training |
| `gpu_8x_h100_sxm5` | 8x H100 | 640GB | $23.92 | Large-scale training |

## Selection Guidelines

- **Testing/debugging**: `gpu_1x_a10` - cheapest option
- **Standard training**: `gpu_1x_a100_sxm4` - best price/performance
- **Large models (>20B params)**: `gpu_1x_h100_sxm5` or multi-GPU
- **Distributed training**: `gpu_8x_*` instances

## Pre-installed Software (Lambda Stack)

All instances include:
- **NVIDIA**: CUDA, cuDNN, NCCL, drivers
- **Frameworks**: PyTorch, TensorFlow, JAX, Keras, Triton
- **Tools**: JupyterLab, Git, tmux, htop, Docker

## FileSystem

- Region-specific (instance must be in same region)
- Mounted at `/home/ubuntu/<name>` → `/lambda/nfs/<name>`
- Persists across instance termination
- Use for checkpoints, datasets, logs

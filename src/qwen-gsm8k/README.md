# Qwen2.5-3B GRPO + LoRA Training on GSM8K

Train Qwen2.5-3B with Group Relative Policy Optimization (GRPO) and LoRA on the GSM8K math reasoning dataset.

## Requirements

- Lambda Labs `gpu_1x_a100_sxm4` (40GB A100)
- ~4-6 hours training time
- ~$5-8 total cost

## Quick Start

### 1. Launch Lambda Labs Instance

```bash
# From local machine
cd claude-code-train
python skills/lambda-labs-training/scripts/launch_instance.py \
    --type gpu_1x_a100_sxm4 \
    --ssh-key <your-key-name> \
    --name qwen-grpo-training
```

### 2. SSH to Instance

```bash
ssh -i <path/to/key.pem> ubuntu@<instance-ip>
```

### 3. Setup Environment

```bash
git clone <your-repo-url> && cd claude-code-train/src/qwen-gsm8k
bash setup.sh
```

### 4. Prepare Data

```bash
conda activate verl
python prepare_data.py
```

### 5. Start Training

```bash
# Use tmux to keep session alive
tmux new -s train

# Start training
python train.py
```

### 6. Monitor Training

```bash
# In another tmux window or SSH session
watch -n 10 nvidia-smi
```

### 7. Download Results

```bash
# From local machine after training completes
scp -r -i <key.pem> ubuntu@<ip>:~/checkpoints ./local_checkpoints/
```

### 8. Terminate Instance

```bash
# From local machine
python skills/lambda-labs-training/scripts/terminate_instance.py <instance-id>
```

## Configuration

### Training Parameters

| Parameter | Default | Description |
|-----------|---------|-------------|
| `--epochs` | 15 | Number of training epochs |
| `--batch_size` | 16 | Training batch size |
| `--lr` | 1e-6 | Learning rate |
| `--lora_rank` | 64 | LoRA rank |
| `--gpu_memory` | 0.6 | vLLM GPU memory utilization |

### Custom Training

```bash
python train.py --epochs 20 --batch_size 8 --lr 5e-7
```

### Dry Run

```bash
python train.py --dry_run
```

## Files

| File | Description |
|------|-------------|
| `setup.sh` | Environment setup script |
| `prepare_data.py` | GSM8K data preprocessing |
| `train.py` | Training launcher |
| `reward.py` | Math verification reward function |
| `config.yaml` | Full configuration reference |

## Expected Results

- **Training Time**: ~4-6 hours for 15 epochs
- **GPU Memory**: ~30-35GB peak usage
- **Improvement**: GSM8K accuracy should improve from ~60% to ~75%+

## Troubleshooting

### Out of Memory

Reduce batch size or GPU memory utilization:
```bash
python train.py --batch_size 8 --gpu_memory 0.5
```

### vLLM Initialization Fails

Ensure CUDA is properly set:
```bash
export CUDA_VISIBLE_DEVICES=0
nvidia-smi  # Should show the A100
```

### Training Hangs

Check GPU status and logs:
```bash
nvidia-smi
tail -f ~/logs/*.log
```

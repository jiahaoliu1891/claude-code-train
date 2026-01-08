#!/bin/bash
# Setup script for verl GRPO training on Lambda Labs
# Run this on the remote GPU instance

set -e

echo "=========================================="
echo "Setting up verl environment for GRPO training"
echo "=========================================="

# Check if conda is available
if ! command -v conda &> /dev/null; then
    echo "Error: conda not found. Lambda Stack should have it pre-installed."
    exit 1
fi

# Create conda environment
echo "[1/5] Creating conda environment..."
conda create -n verl python=3.12 -y
source $(conda info --base)/etc/profile.d/conda.sh
conda activate verl

# Install verl with FSDP backend (no Megatron for single GPU)
echo "[2/5] Installing verl dependencies..."
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
pip install vllm==0.6.3
pip install transformers accelerate datasets peft
pip install pandas pyarrow

# Clone and install verl
echo "[3/5] Cloning and installing verl..."
if [ ! -d "verl" ]; then
    git clone https://github.com/volcengine/verl.git
fi
cd verl
pip install --no-deps -e .
cd ..

# Download Qwen2.5-3B-Instruct model
echo "[4/5] Downloading Qwen2.5-3B-Instruct model..."
python -c "
from transformers import AutoModelForCausalLM, AutoTokenizer
print('Downloading tokenizer...')
AutoTokenizer.from_pretrained('Qwen/Qwen2.5-3B-Instruct')
print('Downloading model...')
AutoModelForCausalLM.from_pretrained('Qwen/Qwen2.5-3B-Instruct', torch_dtype='auto')
print('Model downloaded successfully!')
"

# Prepare data directory
echo "[5/5] Creating data directory..."
mkdir -p ~/data/gsm8k
mkdir -p ~/checkpoints

echo "=========================================="
echo "Setup complete!"
echo ""
echo "Next steps:"
echo "  1. python prepare_data.py"
echo "  2. python train.py"
echo "=========================================="

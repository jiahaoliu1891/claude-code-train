#!/usr/bin/env python3
"""
GRPO + LoRA Training Script for Qwen2.5-3B on GSM8K

This script launches verl GRPO training with configuration optimized
for Lambda Labs gpu_1x_a100_sxm4 (40GB A100).
"""

import os
import sys
import subprocess
import argparse
from pathlib import Path


def get_training_command(config_overrides: dict = None) -> list:
    """Build the verl training command with all parameters."""

    # Base configuration for 40GB A100
    base_config = {
        # Algorithm
        "algorithm.adv_estimator": "grpo",

        # Data paths
        "data.train_files": os.path.expanduser("~/data/gsm8k/train.parquet"),
        "data.val_files": os.path.expanduser("~/data/gsm8k/test.parquet"),
        "data.train_batch_size": 16,
        "data.max_prompt_length": 512,
        "data.max_response_length": 1024,

        # Model
        "actor_rollout_ref.model.path": "Qwen/Qwen2.5-3B-Instruct",

        # LoRA
        "actor_rollout_ref.model.lora_rank": 64,
        "actor_rollout_ref.model.lora_alpha": 32,

        # Actor/Policy
        "actor_rollout_ref.actor.use_kl_loss": True,
        "actor_rollout_ref.actor.kl_loss_coef": 0.001,
        "actor_rollout_ref.actor.lr": 1e-6,

        # Rollout/Generation
        "actor_rollout_ref.rollout.name": "vllm",
        "actor_rollout_ref.rollout.gpu_memory_utilization": 0.6,
        "actor_rollout_ref.rollout.tensor_parallel_size": 1,

        # Training
        "trainer.total_epochs": 15,
        "trainer.project_name": "qwen-gsm8k-grpo",
        "trainer.experiment_name": "qwen2.5-3b-lora",

        # Output
        "trainer.default_hdfs_dir": os.path.expanduser("~/checkpoints"),
    }

    # Apply any overrides
    if config_overrides:
        base_config.update(config_overrides)

    # Build command
    cmd = [sys.executable, "-m", "verl.trainer.main_ppo"]

    for key, value in base_config.items():
        if isinstance(value, bool):
            value = str(value).lower()
        cmd.append(f"{key}={value}")

    return cmd


def main():
    parser = argparse.ArgumentParser(
        description="Train Qwen2.5-3B with GRPO + LoRA on GSM8K"
    )
    parser.add_argument(
        "--epochs",
        type=int,
        default=15,
        help="Number of training epochs"
    )
    parser.add_argument(
        "--batch_size",
        type=int,
        default=16,
        help="Training batch size"
    )
    parser.add_argument(
        "--lr",
        type=float,
        default=1e-6,
        help="Learning rate"
    )
    parser.add_argument(
        "--lora_rank",
        type=int,
        default=64,
        help="LoRA rank"
    )
    parser.add_argument(
        "--gpu_memory",
        type=float,
        default=0.6,
        help="GPU memory utilization for vLLM (0.0-1.0)"
    )
    parser.add_argument(
        "--dry_run",
        action="store_true",
        help="Print command without executing"
    )

    args = parser.parse_args()

    # Build overrides from args
    overrides = {
        "trainer.total_epochs": args.epochs,
        "data.train_batch_size": args.batch_size,
        "actor_rollout_ref.actor.lr": args.lr,
        "actor_rollout_ref.model.lora_rank": args.lora_rank,
        "actor_rollout_ref.rollout.gpu_memory_utilization": args.gpu_memory,
    }

    cmd = get_training_command(overrides)

    print("=" * 60)
    print("GRPO + LoRA Training for Qwen2.5-3B on GSM8K")
    print("=" * 60)
    print(f"Model: Qwen/Qwen2.5-3B-Instruct")
    print(f"Algorithm: GRPO")
    print(f"LoRA Rank: {args.lora_rank}")
    print(f"Batch Size: {args.batch_size}")
    print(f"Learning Rate: {args.lr}")
    print(f"Epochs: {args.epochs}")
    print(f"GPU Memory: {args.gpu_memory * 100}%")
    print("=" * 60)

    if args.dry_run:
        print("\nDry run - command to execute:")
        print(" \\\n  ".join(cmd))
        return

    print("\nStarting training...")
    print("(Use Ctrl+C to interrupt)\n")

    # Set environment variables for better performance
    env = os.environ.copy()
    env["CUDA_VISIBLE_DEVICES"] = "0"
    env["TOKENIZERS_PARALLELISM"] = "false"

    # Run training
    try:
        subprocess.run(cmd, env=env, check=True)
        print("\nTraining completed successfully!")
        print(f"Checkpoints saved to: ~/checkpoints")
    except subprocess.CalledProcessError as e:
        print(f"\nTraining failed with error code: {e.returncode}")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\nTraining interrupted by user.")
        sys.exit(0)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
GSM8K Data Preprocessing for verl GRPO Training

Downloads and preprocesses GSM8K dataset into parquet format
compatible with verl training pipeline.
"""

import os
import json
import argparse
from pathlib import Path

import pandas as pd
from datasets import load_dataset


def format_prompt(question: str) -> str:
    """Format question into chat template for Qwen."""
    return f"""Solve this math problem step by step. Show your work and put your final answer after ####.

Question: {question}

Solution:"""


def extract_answer(answer_text: str) -> str:
    """Extract the final numerical answer from GSM8K answer field."""
    # GSM8K answers are in format: "explanation #### number"
    if "####" in answer_text:
        return answer_text.split("####")[-1].strip()
    return answer_text.strip()


def process_gsm8k(output_dir: str = "~/data/gsm8k"):
    """Download and process GSM8K dataset."""
    output_dir = os.path.expanduser(output_dir)
    os.makedirs(output_dir, exist_ok=True)

    print("Loading GSM8K dataset from Hugging Face...")
    dataset = load_dataset("openai/gsm8k", "main")

    for split in ["train", "test"]:
        print(f"Processing {split} split...")
        data = dataset[split]

        processed = []
        for item in data:
            question = item["question"]
            answer = item["answer"]
            ground_truth = extract_answer(answer)

            processed.append({
                "data_source": "gsm8k",
                "prompt": format_prompt(question),
                "ground_truth": ground_truth,
                "extra_info": {
                    "question": question,
                    "full_answer": answer
                }
            })

        # Convert to DataFrame and save as parquet
        df = pd.DataFrame(processed)

        # verl expects extra_info as JSON string
        df["extra_info"] = df["extra_info"].apply(json.dumps)

        output_path = os.path.join(output_dir, f"{split}.parquet")
        df.to_parquet(output_path, index=False)
        print(f"  Saved {len(df)} samples to {output_path}")

    print("\nData preparation complete!")
    print(f"  Train: {output_dir}/train.parquet")
    print(f"  Test:  {output_dir}/test.parquet")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Prepare GSM8K data for verl training")
    parser.add_argument(
        "--output_dir",
        type=str,
        default="~/data/gsm8k",
        help="Output directory for processed data"
    )
    args = parser.parse_args()

    process_gsm8k(args.output_dir)

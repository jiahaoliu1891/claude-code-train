#!/usr/bin/env python3
"""
Verifiable Reward Function for GSM8K Math Problems

This module provides the reward function used by verl during GRPO training.
The reward is binary: 1.0 for correct answers, 0.0 for incorrect.
"""

import re
from typing import Optional, Any


def normalize_answer(answer: str) -> str:
    """Normalize numerical answer for comparison."""
    # Remove commas, spaces, and common units
    answer = answer.strip().lower()
    answer = answer.replace(",", "")
    answer = answer.replace(" ", "")
    answer = answer.replace("$", "")
    answer = answer.replace("%", "")

    # Handle negative numbers
    answer = answer.replace("−", "-")  # Unicode minus to ASCII

    # Try to extract just the number
    match = re.search(r'-?\d+\.?\d*', answer)
    if match:
        return match.group()
    return answer


def extract_model_answer(solution_str: str) -> Optional[str]:
    """Extract the final answer from model's solution.

    Looks for answers in these formats:
    - "#### <number>"
    - "The answer is <number>"
    - "= <number>" at the end
    """
    # Try #### format first (standard GSM8K format)
    match = re.search(r'####\s*(-?\d[\d,]*\.?\d*)', solution_str)
    if match:
        return match.group(1)

    # Try "answer is" format
    match = re.search(r'(?:the\s+)?answer\s+is[:\s]*(-?\d[\d,]*\.?\d*)',
                      solution_str, re.IGNORECASE)
    if match:
        return match.group(1)

    # Try final equals sign
    match = re.search(r'=\s*(-?\d[\d,]*\.?\d*)\s*$', solution_str)
    if match:
        return match.group(1)

    # Try to find any number at the very end
    match = re.search(r'(-?\d[\d,]*\.?\d*)\s*$', solution_str)
    if match:
        return match.group(1)

    return None


def compute_score(
    data_source: str,
    solution_str: str,
    ground_truth: str,
    extra_info: Optional[Any] = None
) -> float:
    """Compute reward score for a model solution.

    This is the main function called by verl during training.

    Args:
        data_source: Dataset identifier (e.g., "gsm8k")
        solution_str: Model's generated solution text
        ground_truth: The correct answer
        extra_info: Optional additional information (unused)

    Returns:
        1.0 if the answer is correct, 0.0 otherwise
    """
    # Extract model's answer
    model_answer = extract_model_answer(solution_str)

    if model_answer is None:
        return 0.0

    # Normalize both answers
    model_normalized = normalize_answer(model_answer)
    truth_normalized = normalize_answer(ground_truth)

    # Compare
    if model_normalized == truth_normalized:
        return 1.0

    # Try numerical comparison for floating point tolerance
    try:
        model_num = float(model_normalized)
        truth_num = float(truth_normalized)
        if abs(model_num - truth_num) < 1e-6:
            return 1.0
    except ValueError:
        pass

    return 0.0


# For verl compatibility - register the reward function
if __name__ == "__main__":
    # Test the reward function
    test_cases = [
        ("The calculation is 5 + 3 = 8. #### 8", "8", 1.0),
        ("Let me solve this step by step. The answer is 42.", "42", 1.0),
        ("After calculation, we get 100", "100", 1.0),
        ("The result is #### 15", "15", 1.0),
        ("Wrong answer #### 10", "15", 0.0),
        ("No number here", "5", 0.0),
    ]

    print("Testing reward function:")
    for solution, truth, expected in test_cases:
        score = compute_score("gsm8k", solution, truth)
        status = "PASS" if score == expected else "FAIL"
        print(f"  [{status}] Expected {expected}, got {score}")
        print(f"         Solution: {solution[:50]}...")

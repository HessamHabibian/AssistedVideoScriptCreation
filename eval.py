"""
Script evaluation module for assessing generated dialogue scripts.

The evaluation process runs through multiple test cases from eval_set.csv and produces both
per-script detailed metrics and aggregate statistics across all evaluations.
"""

import asyncio
from typing import List
from eval_utils import evaluate_single_script
from models import SingleEvaluationResult
from solution import generate_script_hf
from utils import load_input_parameters


async def evaluate_script_generation() -> List[SingleEvaluationResult]:
    eval_set = load_input_parameters("eval_set.csv")

    results = []
    for input_parameters in eval_set:
        script = await generate_script_hf(input_parameters)

        result = await evaluate_single_script(
            input_parameters=input_parameters,
            script=script,
        )
        results.append(result)

    return results


if __name__ == "__main__":

    async def main():
        results = await evaluate_script_generation()

        # Calculate averages
        avg_trivial_issues = sum(
            result.trivial_issue_count for result in results
        ) / len(results)
        avg_line_error = sum(
            result.avg_dialogue_line_count_error for result in results
        ) / len(results)
        avg_word_error = sum(
            result.avg_dialogue_word_count_error for result in results
        ) / len(results)

        # Print summary statistics
        print("\n\n")
        print("=" * 60)
        print("=== Evaluation Summary ===")
        print("=" * 60)
        print(f"Total prompts evaluated: {len(results)}")
        print(f"Average trivial issues per script: {avg_trivial_issues:.1f}")
        print(f"Average dialogue line count error: {avg_line_error:.1f} lines")
        print(f"Average word count error: {avg_word_error:.1f} words")

    asyncio.run(main())

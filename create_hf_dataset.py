"""
Script for creating and uploading a HuggingFace dataset from training examples.

This script loads training examples from a JSON file, formats them into a conversational
dataset structure, and uploads the resulting dataset to the HuggingFace Hub. The dataset
contains input parameters and generated video scripts formatted as conversations between
a user and assistant.

Parameters:
    --dataset-name: Name of the input JSON dataset file (default: training_data.json)
    --hf-dataset-path: Path where the dataset will be uploaded on HuggingFace Hub
"""

import click
from datasets import Dataset
import json
from models import TrainingExample
from prompt import get_prompt
from huggingface_hub import login
from config import HUGGING_FACE_API_KEY
from typing import Dict, List


def load_training_data(dataset_name: str) -> List[TrainingExample]:
    """Load the training data from JSON file"""
    try:
        with open(dataset_name, "r") as f:
            raw_data = json.load(f)
            return [TrainingExample.model_validate(item) for item in raw_data]
    except FileNotFoundError:
        raise FileNotFoundError(f"{dataset_name} file not found")
    except json.JSONDecodeError:
        raise ValueError(f"Invalid JSON format in {dataset_name}")


def format_for_training(
    training_data: List[TrainingExample],
) -> List[Dict[str, List[Dict[str, str]]]]:
    """Format the training data into conversations"""
    formatted_data = []

    for example in training_data:
        messages = get_prompt(example.input_parameters)

        messages.append(
            {
                "role": "assistant",
                "content": example.output_video_script.model_dump_json(),
            }
        )

        formatted_data.append({"conversations": messages})

    return formatted_data


@click.command()
@click.option(
    "--dataset-name",
    default="training_data.json",
    help="Name of the input JSON dataset file",
)
@click.option(
    "--hf-dataset-path",
    help="Path where to upload the dataset on HuggingFace Hub",
)
def main(dataset_name: str, hf_dataset_path: str):
    # Login to Hugging Face
    login(token=HUGGING_FACE_API_KEY)

    # Load and format the training data
    raw_data = load_training_data(dataset_name)
    formatted_data = format_for_training(raw_data)

    # Create HuggingFace dataset
    dataset = Dataset.from_list(formatted_data)

    # Print dataset info before pushing
    print("\nDataset to be pushed:")
    print(f"Number of examples: {len(dataset)}")
    print(dataset)

    # Push to HuggingFace Hub
    dataset.push_to_hub(hf_dataset_path, private=True)


if __name__ == "__main__":
    main()

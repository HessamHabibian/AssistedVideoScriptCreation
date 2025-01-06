from typing import List
from models import InputParameters
import csv


def load_input_parameters(file: str) -> List[InputParameters]:
    """
    Load input parameters from a CSV file and return a list of InputParameters objects.

    Args:
        file (str): The path to the CSV file containing input parameters.

    Returns:
        List[InputParameters]: A list of InputParameters objects.
    """
    input_parameters_list = []
    with open(file, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            input_parameters_list.append(
                InputParameters(
                    number_of_scenes=int(row["number_of_scenes"]),
                    dialogue_lines_per_scene=int(row["dialogue_lines_per_scene"]),
                    total_dialogue_words_per_scene=int(
                        row["total_dialogue_words_per_scene"]
                    ),
                    prompt=row["prompt"],
                    first_character_name=row["first_character_name"],
                    second_character_name=row["second_character_name"],
                )
            )
    return input_parameters_list

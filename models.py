from typing import List
from pydantic import BaseModel, Field


class InputParameters(BaseModel):
    number_of_scenes: int = Field(
        description="Number of requested distinct scenes in the video"
    )
    dialogue_lines_per_scene: int = Field(
        description="Number of requested individual dialogue lines per scene"
    )
    total_dialogue_words_per_scene: int = Field(
        description="Number of total requested dialogue words per scene"
    )
    first_character_name: str = Field(
        description="Name of the first character in the dialogue"
    )
    second_character_name: str = Field(
        description="Name of the second character in the dialogue"
    )
    prompt: str = Field(
        description="High-level prompt describing the conversation topic"
    )


class DialogueLine(BaseModel):
    character_name: str = Field(description="Name of the character speaking this line")
    dialogue_text: str = Field(
        description="The actual dialogue text spoken by the character"
    )


class SceneScript(BaseModel):
    dialogue_lines: List[DialogueLine] = Field(
        description="List of dialogue lines in this scene"
    )


class VideoScript(BaseModel):
    scenes: List[SceneScript] = Field(
        description="List of scenes making up the video script"
    )


class SingleEvaluationResult(BaseModel):
    input_parameters: InputParameters = Field(
        description="Input parameters used for evaluation"
    )
    output_script: VideoScript = Field(
        description="Generated script from the evaluation based on the input parameters"
    )
    trivial_issue_count: int = Field(
        description="Number of trivial issues in the generated script"
    )
    avg_dialogue_line_count_error: float = Field(
        description="Average absolute dialogue line count error across all scenes"
    )
    avg_dialogue_word_count_error: float = Field(
        description="Average absolute word count error across all dialogue lines"
    )


class TrainingExample(BaseModel):
    input_parameters: InputParameters = Field(
        description="Input parameters used to generate this example"
    )
    output_video_script: VideoScript = Field(
        description="The resulting video script for these parameters"
    )

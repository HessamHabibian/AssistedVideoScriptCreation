from hf_inference_client import get_completions

from models import InputParameters, VideoScript
from prompt import get_prompt


async def generate_script_hf(input_parameters: InputParameters) -> VideoScript:
    messages = get_prompt(input_parameters)

    return await get_completions(
        model_name="meta-llama/Meta-Llama-3-8B-Instruct",
        messages=messages,
        response_pydantic_type=VideoScript,
    )

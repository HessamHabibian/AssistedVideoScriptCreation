from pydantic import BaseModel
from typing import Dict, List, Type, TypeVar
from huggingface_hub import ChatCompletionInputGrammarType, InferenceClient

from config import HUGGING_FACE_API_KEY


T = TypeVar("T", bound=BaseModel)

CLIENT = InferenceClient(
    api_key=HUGGING_FACE_API_KEY,
)


async def get_completions(
    model_name: str,
    messages: List[Dict[str, str]],
    response_pydantic_type: Type[T],
    temperature: float = 0.7,
    max_tokens: int = 1024,
) -> T:
    """Get completions from a Hugging Face inference API as a Pydantic object.

    Args:
        model_name: Name of a model that is available through Hugging Face's inference API, not a self-hosted model.
        messages: List of message dictionaries containing the conversation history.
        response_pydantic_type: Pydantic model class to validate and parse the response.
        temperature: Controls randomness in the response. Higher values (e.g. 0.8) make the output
            more random, lower values (e.g. 0.2) make it more deterministic.
        max_tokens: Maximum number of tokens in the response.

    Returns:
        Parsed and validated response matching the provided Pydantic model type
    """
    try:
        response = CLIENT.chat.completions.create(
            model=model_name,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
            response_format=ChatCompletionInputGrammarType(
                type="json", value=response_pydantic_type.model_json_schema()
            ),
        )
        raw_text = response.choices[0].message.content
        if not isinstance(raw_text, str):
            raise ValueError(f"Expected string response, got {type(raw_text)}")

        return response_pydantic_type.model_validate_json(raw_text)
    except Exception as e:
        raise ValueError(f"Error getting completion from {model_name}: {str(e)}") from e

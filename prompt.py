from typing import Dict, List

from models import InputParameters


SCRIPT_PROMPT = """Create an engaging and interesting dialogue script following these CRITICAL REQUIREMENTS:

1. TOPIC: Create a natural, dynamic conversation about: {prompt}
   Make the dialogue compelling with emotional depth and character development

2. SCENE COUNT: Generate EXACTLY {number_of_scenes} distinct scenes
   Each scene should cover a different engaging aspect of the conversation
   Build dramatic tension and interest across scenes

3. DIALOGUE LINES: Include EXACTLY {dialogue_lines_per_scene} dialogue lines per scene
   between characters {first_character} and {second_character}
   Ensure each exchange reveals character personality and advances the conversation.

4. WORD COUNT: Each scene MUST contain EXACTLY {total_dialogue_words_per_scene} total words of dialogue
   Count every single word including:
   - Articles (a, an, the)
   - Conjunctions (and, but, or) 
   - Prepositions (in, on, at)
   - All other word types

Make the dialogue feel natural while maintaining precise word counts.

Supply response in this JSON format only:
    {{
        "scenes": [
            {{
                "dialogue_lines": [
                    {{
                        "character_name": string,
                        "dialogue_text": string
                    }}
                ]
            }}
        ]
    }}
"""


def get_prompt(input_parameters: InputParameters) -> List[Dict[str, str]]:
    return [
        {
            "role": "user",
            "content": SCRIPT_PROMPT.format(
                prompt=input_parameters.prompt,
                number_of_scenes=input_parameters.number_of_scenes,
                dialogue_lines_per_scene=input_parameters.dialogue_lines_per_scene,
                total_dialogue_words_per_scene=input_parameters.total_dialogue_words_per_scene,
                first_character=input_parameters.first_character_name,
                second_character=input_parameters.second_character_name,
            ),
        }
    ]

# Video Script Generation Project

This project generates natural dialogue scripts for videos based on input parameters. It includes tools for training, evaluation, and dataset creation.

Generated scripts use Pydantic models (VideoScript, SceneScript, DialogueLine) to structure scenes containing dialogue exchanges between two characters, following the specified parameters for number of scenes, lines, and word counts. The input parameters are modeled using the InputParameters class.

## Files

- `.env.template`: Template for HUGGING_FACE_API_KEY (copy to `.env` and add your HF key)
- `config.py`: Loads configuration settings from `.env` file
- `create_hf_dataset.py`: Creates and uploads training datasets to HuggingFace Hub
- `eval.py`: Evaluates generated dialogue scripts against test cases
- `eval_set.csv`: Ten test cases with input parameters
- `eval_utils.py`: Utilities to assess script quality metrics (word count, dialogue accuracy)
- `hf_inference_client.py`: Client for HuggingFace model inference requests
- `models.py`: Contains Pydantic models for data structures (InputParameters, VideoScript, etc.)
- `prompt.py`: Contains prompt generation logic for the LLM
- `requirements.txt`: Lists all Python package dependencies and versions
- `solution.py`: Baseline solution using Meta-Llama-3-8B-Instruct model
- `training_data.json`: Training examples with input parameters and expected video scripts
- `utils.py`: Contains utility functions for loading input parameters from CSV files

## Evaluation

Scripts are evaluated based on several criteria:
- Proper usage of character names throughout
- Matching the requested scene count
- Following specified number of dialogue lines
- Achieving target word counts within each scene

Note: Currently no automated evaluation of script quality, coherence or creative aspects.

## Training Data

The training data in `training_data.json` contains examples of input parameters and corresponding video scripts. While comprehensive, the data contains significant noise and should be carefully handled before model training.

## Requirements

See `requirements.txt` for full required Python dependencies.

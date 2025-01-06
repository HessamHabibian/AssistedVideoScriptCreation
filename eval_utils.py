from models import InputParameters, SingleEvaluationResult, VideoScript


async def evaluate_single_script(
    input_parameters: InputParameters,
    script: VideoScript,
) -> SingleEvaluationResult:
    """Evaluates a single generated video script against input parameters and prints detailed results.

    Args:
        input_parameters: Original input parameters used to generate the script
        script: The generated VideoScript to evaluate

    Returns:
        SingleEvaluationResult containing evaluation metrics
    """

    print("\n" + "=" * 80)  # Clear separator between evaluation cases
    print("\n=== Input Parameters ===")
    print(f"Number of scenes: {input_parameters.number_of_scenes}")
    print(f"Dialogue lines per scene: {input_parameters.dialogue_lines_per_scene}")
    print(
        f"Total dialogue words per scene: {input_parameters.total_dialogue_words_per_scene}"
    )
    print(f"Prompt: {input_parameters.prompt}")
    print(f"First character: {input_parameters.first_character_name}")
    print(f"Second character: {input_parameters.second_character_name}")
    print("-" * 40)

    # Initialize counters and lists
    trivial_issues = 0
    if len(script.scenes) != input_parameters.number_of_scenes:
        trivial_issues += 1
    char_names = [
        input_parameters.first_character_name.lower(),
        input_parameters.second_character_name.lower(),
    ]
    line_count_errors = []
    word_count_errors = []

    # Print generated script and calculate metrics in one pass
    print("\n=== Generated Script ===")
    for i, scene in enumerate(script.scenes, 1):
        print(f"\nScene {i}:")
        print("-" * 40)

        # Initialize per-scene counters
        scene_word_count = 0
        scene_line_count = 0

        # Process each line
        for line in scene.dialogue_lines:
            print(f"{line.character_name}: {line.dialogue_text}")

            # Check character names
            if line.character_name.lower() not in char_names:
                trivial_issues += 1

            # Count words and lines
            scene_word_count += len(line.dialogue_text.split())
            scene_line_count += 1

        # Calculate errors for this scene
        line_error = abs(scene_line_count - input_parameters.dialogue_lines_per_scene)
        word_error = abs(
            scene_word_count - input_parameters.total_dialogue_words_per_scene
        )
        line_count_errors.append(line_error)
        word_count_errors.append(word_error)

        print("\n")
        print(
            f"Total lines in scene: {scene_line_count} "
            f"(Target: {input_parameters.dialogue_lines_per_scene}, Error: {line_error})"
        )
        print(
            f"Total words in scene: {scene_word_count} "
            f"(Target: {input_parameters.total_dialogue_words_per_scene}, Error: {word_error})"
        )
        print("-" * 40)

    # Calculate averages
    avg_line_error = 1.0 * sum(line_count_errors) / len(line_count_errors)
    avg_word_error = 1.0 * sum(word_count_errors) / len(word_count_errors)

    # Print evaluation metrics
    print("\n=== Key Video Metrics ===")
    print(f"Trivial issues found: {trivial_issues}")
    print(f"Average line count error: {avg_line_error:.2f} lines")
    print(f"Average word count error: {avg_word_error:.2f} words")

    return SingleEvaluationResult(
        input_parameters=input_parameters,
        output_script=script,
        trivial_issue_count=trivial_issues,
        avg_dialogue_line_count_error=avg_line_error,
        avg_dialogue_word_count_error=avg_word_error,
    )

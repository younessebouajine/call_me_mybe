import json
from pathlib import Path
import argparse

from src.parser_promet import load_prompts
from src.parser_def_fun import load_functions
from src.llm_client import LLMClient
from src.json_constraint import JsonConstraint
from src.constrained_decoder import ConstrainedDecoder
from src.functionselector import FunctionSelector


def parse_args() -> argparse.Namespace:
    """Parse the command-line arguments.

    Returns:
        argparse.Namespace: Parsed command-line arguments.
    """

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--functions_definition",
        default="data/input/functions_definition.json",
    )

    parser.add_argument(
        "--input",
        default="data/input/function_calling_tests.json",
    )

    parser.add_argument(
        "--output",
        default="data/output/function_calling_results.json",
    )

    return parser.parse_args()


def main() -> None:
    """Run the function-calling pipeline.

    This function loads the prompts and function definitions,
    initializes the language model and helper classes, processes
    each prompt, and writes the generated function calls to the
    output JSON file.
    """

    args = parse_args()

    prompts = load_prompts(
        Path(args.input)
    )

    functions = load_functions(
        Path(args.functions_definition)
    )

    llm = LLMClient()

    constraint = JsonConstraint(functions)

    selector = FunctionSelector(
        llm,
        functions,
    )

    decoder = ConstrainedDecoder(
        llm,
        constraint,
    )

    results = []
    for prompt in prompts:
        function = selector.select(prompt.prompt)

        parameters = decoder.extract_parameters(
            prompt.prompt,
            function.name,
        )

        results.append(
            {
                "prompt": prompt.prompt,
                "name": function.name,
                "parameters": parameters,
            }
        )

    output_path = Path(
        args.output
    )

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    with output_path.open("w") as file:
        json.dump(
         results,
         file,
         indent=4,
        )


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Error: {e}")

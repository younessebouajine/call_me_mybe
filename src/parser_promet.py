from pathlib import Path
from typing import List
import json
from pydantic import ValidationError
from src.models import Prompt


def load_prompts(path: str | Path) -> List[Prompt]:
    """Load and validate prompts from a JSON file.

    Args:
        path: Path to the JSON file containing the prompts.

    Returns:
        A list of validated Prompt objects.

    Raises:
        FileNotFoundError: If the prompt file does not exist.
        ValueError: If the JSON is invalid or the prompts do not
            match the expected format.
    """

    path = Path(path)

    try:
        with path.open("r") as file:
            data = json.load(file)

        if not isinstance(data, list):
            raise ValueError(
                "The JSON root must be a list."
            )

        if not data:
            raise ValueError(
                "JSON file must contain at least one prompt."
            )

        # prompts = []

        # for item in data:
        #     validated_prompt = Prompt.model_validate(item)
        #     prompts.append(validated_prompt)
        # return prompts
        return [Prompt.model_validate(item) for item in data]

    except FileNotFoundError:
        raise FileNotFoundError(f"Prompt file not found: {path}")

    except json.JSONDecodeError as er:
        raise ValueError(f"Invalid JSON: {er}") from er
    except ValidationError as er:
        raise ValueError(f"Invalid prompt format:\n{er}") from er

import json
from src.llm_client import LLMClient
from src.json_constraint import JsonConstraint


class ConstrainedDecoder:
    """Generate function parameters using the language model.

    This class prompts the language model to generate a JSON object
    containing the parameters required by a selected function. The
    generated JSON is validated and converted into Python objects.
    """

    def __init__(
        self,
        llm: LLMClient,
        constraint: JsonConstraint,
    ) -> None:
        """Initialize the constrained decoder.

        Args:
            llm: Language model used for parameter generation.
            constraint: Helper used to access function metadata.
        """

        self.llm = llm
        self.constraint = constraint

    def extract_parameters(
        self,
        prompt: str,
        function_name: str,
    ) -> dict:
        """Generate and validate the parameters for a function.

        Args:
            prompt: The user's natural language request.
            function_name: Name of the selected function.

        Returns:
            A dictionary containing the validated function parameters.

        Raises:
            ValueError: If the language model fails to generate valid
                JSON or if required parameters are missing.
        """

        parameter_names = self.constraint.get_parameter_names(
            function_name,
        )

        schema = {}

        for parameter_name in parameter_names:
            schema[parameter_name] = (
                self.constraint.get_parameter_type(
                    function_name,
                    parameter_name,
                )
            )

        llm_prompt = self.build_prompt(
            prompt,
            function_name,
            schema,
        )

        input_ids = self.llm.encode(
            llm_prompt,
        )[0].tolist()

        generated_ids = []

        generated_text = ""
        json_text = None

        for _ in range(150):
            logits = self.llm.get_next_token_logits(
                input_ids,
            )
            # print(list(range(len(logits))))

            next_token = self.valid_token(
                logits,
                list(range(len(logits))),
            )

            input_ids.append(next_token)
            generated_ids.append(next_token)

            generated_text = self.llm.decode(
                generated_ids,
            )

            try:
                json_text = self.extract_json(
                    generated_text,
                )
                break
            except ValueError:
                continue

        if json_text is None:
            raise ValueError(
                f"No complete JSON generated:\n{generated_text}"
            )

        try:
            parameters = json.loads(
                json_text,
            )
        except json.JSONDecodeError:
            raise ValueError(
                f"Invalid JSON:\n{json_text}"
            )

        for parameter_name in parameter_names:
            if parameter_name not in parameters:
                raise ValueError(
                    f"Missing parameter '{parameter_name}'"
                )

        for parameter_name in parameter_names:
            if (
                self.constraint.get_parameter_type(
                    function_name,
                    parameter_name
                ) == "number"
            ):
                parameters[parameter_name] = float(
                    parameters[parameter_name]
                )

        return {
            parameter: parameters[parameter]
            for parameter in parameter_names
        }

    def build_prompt(
        self,
        prompt: str,
        function_name: str,
        schema: dict,
    ) -> str:
        """Build the prompt used for JSON parameter generation.

        Args:
            prompt: The user's request.
            function_name: Name of the selected function.
            schema: Parameter schema for the selected function.

        Returns:
            A formatted prompt instructing the language model to
            generate a JSON object.
        """

        example = self.get_example(
            function_name,
        )

        return f"""
You are a JSON generator.

Generate ONLY the parameters of the selected function.

Rules:
- Return ONLY one JSON object.
- Do not explain.
- Do not use markdown.
- Do not write anything before or after the JSON.
- Use exactly the parameter names from the schema.

Function:
{function_name}

Parameter Schema:
{schema}

Example:

{example}

User Request:
{prompt}

JSON:
"""

    def get_example(
        self,
        function_name: str,
    ) -> str:
        """Return an example for the selected function.

        Args:
            function_name: Name of the selected function.

        Returns:
            A prompt-and-output example used to guide the language
            model. Returns an empty string if no example exists.
        """

        examples = {
            "fn_add_numbers": """
User:
What is the sum of 2 and 3?

Output:
{"a": 2, "b": 3}
""",

            "fn_greet": """
User:
Greet John

Output:
{"name": "John"}
""",

            "fn_reverse_string": """
User:
Reverse the string "hello"

Output:
{"s": "hello"}
""",

            "fn_get_square_root": """
User:
What is the square root of 16?

Output:
{"a": 16}
""",

            "fn_substitute_string_with_regex": """
User:
Replace all vowels in "Programming is fun" with asterisks

Output:
{
    "source_string": "Programming is fun",
    "regex": "[aeiouAEIOU]",
    "replacement": "*"
}
"""
        }

        return examples.get(
            function_name,
            "",
        )

    def extract_json(
        self,
        text: str,
    ) -> str:
        """Extract the first complete JSON object from text.

        The method scans the generated text until it finds a balanced
        pair of braces and returns the enclosed JSON object.

        Args:
            text: Text generated by the language model.

        Returns:
            The extracted JSON object as a string.

        Raises:
            ValueError: If no complete JSON object can be found.
        """

        start = text.find("{")

        if start == -1:
            raise ValueError(
                "No JSON object found."
            )

        depth = 0

        for i in range(start, len(text)):
            if text[i] == "{":
                depth += 1

            elif text[i] == "}":
                depth -= 1

                if depth == 0:
                    return text[start:i + 1]

        raise ValueError(
            "Incomplete JSON object."
        )

    def valid_token(
        self,
        logits: list[float],
        valid_token_ids: list[int],
    ) -> int:
        """Select the highest-scoring valid token.

        Args:
            logits: Logits predicted by the language model.
            valid_token_ids: IDs of tokens that may be selected.

        Returns:
            The ID of the valid token with the highest logit.

        Raises:
            ValueError: If no valid token IDs are available.
        """

        if not valid_token_ids:
            raise ValueError(
                "No valid tokens available."
            )

        return max(
            valid_token_ids,
            key=lambda token_id: logits[token_id],
        )

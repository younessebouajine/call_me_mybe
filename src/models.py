from pydantic import BaseModel, ConfigDict, field_validator
from typing import Dict, Literal
import keyword


class Prompt(BaseModel):
    """Represents a single user prompt loaded from the input JSON file."""

    model_config = ConfigDict(
        extra="forbid",
    )

    prompt: str

    @field_validator("prompt")
    @classmethod
    def validate_prompt(cls, value: str) -> str:
        """Validate the prompt.

        Ensures that the prompt is not empty or composed only of
        whitespace characters.

        Args:
            value: The prompt to validate.

        Returns:
            The validated prompt.

        Raises:
            ValueError: If the prompt is empty.
        """

        if value.strip() == "":
            raise ValueError(
                "Prompt cannot be empty."
            )
        return value


class Parameter(BaseModel):
    """Represents the type of a function parameter or return value."""

    model_config = ConfigDict(
        extra="forbid",
    )

    type: Literal["number", "string", "boolean", "integer"]


class FunctionDefinition(BaseModel):
    """Represents a function definition used by the function-calling system.

    A function definition includes its name, description, parameter
    schema, and return type.
    """

    model_config = ConfigDict(
        extra="forbid",
    )

    name: str
    description: str
    parameters: Dict[str, Parameter]
    returns: Parameter

    @field_validator("name")
    @classmethod
    def validate_name(cls, value: str) -> str:
        """Validate the function name.

        Ensures that the function name is a valid Python identifier
        and is not a reserved Python keyword.

        Args:
            value: The function name.

        Returns:
            The validated function name.

        Raises:
            ValueError: If the name is not a valid identifier or is
                a Python keyword.
        """

        if not value.isidentifier():
            raise ValueError(
                "Invalid Python identifier"
            )
        if keyword.iskeyword(value):
            raise ValueError(
                "Function name cannot be a Python keyword."
            )
        return value

    @field_validator("description")
    @classmethod
    def validate_description(cls, value: str) -> str:
        """Validate the function description.

        Ensures that the description is not empty.

        Args:
            value: The function description.

        Returns:
            The validated description.

        Raises:
            ValueError: If the description is empty.
        """

        if value.strip() == "":
            raise ValueError(
                "Description cannot be empty."
            )
        return value

    @field_validator("parameters")
    @classmethod
    def validate_parameter_names(
        cls,
        value: Dict[str, Parameter],
    ) -> Dict[str, Parameter]:
        """Validate all parameter names.

        Ensures that every parameter name is a valid Python
        identifier and is not a reserved Python keyword.

        Args:
            value: Dictionary mapping parameter names to their
                corresponding parameter definitions.

        Returns:
            The validated parameter dictionary.

        Raises:
            ValueError: If a parameter name is invalid or is a
                Python keyword.
        """

        for parmeter_name in value:
            if not parmeter_name.isidentifier():
                raise ValueError(
                    f"Invalid parameter name: '{parmeter_name}'."
                )
            if keyword.iskeyword(parmeter_name):
                raise ValueError(
                    f"'{parmeter_name}' is a Python keyword."
                )
        return value

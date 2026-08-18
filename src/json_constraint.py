from src.models import FunctionDefinition


class JsonConstraint:
    """Provide access to validated function definitions.

    This class exposes helper methods to retrieve function names,
    parameter names, and parameter types from the loaded function
    definitions.
    """

    def __init__(self, functions: list[FunctionDefinition]) -> None:
        """Initialize the JSON constraint helper.

        Args:
            functions: List of validated function definitions.
        """

        self.functions = functions

    def get_function_names(self) -> list[str]:
        """Return the names of all available functions.

        Returns:
            A list containing every function name.
        """

        return [function.name for function in self.functions]

    def get_function(self, name: str) -> FunctionDefinition | None:
        """Retrieve a function definition by name.

        Args:
            name: Name of the function.

        Returns:
            The matching FunctionDefinition if found, otherwise None.
        """

        for function in self.functions:
            if function.name == name:
                return function
        return None

    def get_parameter_names(self, function_name: str) -> list[str]:
        """Return the parameter names of a function.

        Args:
            function_name: Name of the function.

        Returns:
            A list containing the parameter names. If the function
            does not exist, an empty list is returned.
        """

        function = self.get_function(function_name)

        if function is None:
            return []

        return list(function.parameters.keys())

    def get_parameter_type(
        self,
        function_name: str,
        parameter_name: str,
    ) -> str | None:
        """Return the type of a function parameter.

        Args:
            function_name: Name of the function.
            parameter_name: Name of the parameter.

        Returns:
            The parameter type if both the function and parameter
            exist, otherwise None.
        """
        function = self.get_function(function_name)

        if function is None:
            return None

        parameter = function.parameters.get(parameter_name)

        if parameter is None:
            return None

        return parameter.type

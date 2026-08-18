*This project has been created as part of the 42 curriculum by [ybouaji].*

# Call Me Maybe - Introduction to Function Calling in LLMs

## Description

This project implements a simple **function calling system** using a local Large Language Model (LLM).

The goal is to receive a natural language prompt, determine which predefined function should be called, extract the required parameters, and generate a JSON output representing the function call.

Unlike traditional function calling APIs, this project implements the complete pipeline manually, including function selection, prompt engineering, constrained JSON extraction, and parameter validation.

The project uses **Pydantic** for data validation and the provided **LLM SDK** for local inference.

---

# Features

* Load function definitions from JSON.
* Load user prompts from JSON.
* Validate all input files using Pydantic.
* Select the most appropriate function using an LLM.
* Extract function parameters as JSON.
* Validate generated parameters.
* Generate output in the required JSON format.
* Support custom input, output, and function definition files through command-line arguments.

---

# Project Structure

```
.
├── data/
│   ├── input/
│   └── output/
├── llm_sdk/
├── src/
│   ├── __main__.py
│   ├── constrained_decoder.py
│   ├── functionselector.py
│   ├── json_constraint.py
│   ├── llm_client.py
│   ├── models.py
│   ├── parser_def_fun.py
│   └── parser_promet.py
├── Makefile
├── pyproject.toml
└── README.md
└── uv.lock
```

---

# Instructions

## Installation

Install all dependencies using:

```bash
make install
```

or

```bash
uv sync
```

---

## Run

Run using the default input files:

```bash
make run
```

or

```bash
uv run python -m src
```

---

## Custom files

```bash
uv run python -m src \
    --functions_definition data/input/functions_definition.json \
    --input data/input/function_calling_tests.json \
    --output data/output/function_calling_results.json
```

---

## Debug

```bash
make debug
```

---

## Lint

```bash
make lint
```

---

## Clean

```bash
make clean
```

---

# Algorithm Explanation

The project follows a multi-stage pipeline.

### 1. Load input

The program first loads:

* function definitions
* user prompts

Both files are parsed from JSON and validated using Pydantic models.

---

### 2. Function selection

A prompt is built containing:

* all available function names
* their descriptions
* the user's request

The language model generates the name of the function that best matches the request.

---

### 3. Parameter extraction

Once the function is selected, another prompt is generated containing:

* the selected function name
* its parameter schema
* an example
* the user's request

The language model generates a JSON object containing only the required parameters.

---

### 4. Constrained decoding

Instead of generating an unlimited amount of text, tokens are generated one by one.

After each generated token:

* the generated text is decoded;
* the program attempts to extract a complete JSON object;
* if a complete JSON object is found, generation immediately stops.

This prevents unnecessary generation and reduces invalid outputs.

---

### 5. Validation

The generated JSON is:

* parsed using `json.loads()`;
* checked for missing parameters;
* numeric parameters are converted to Python floats when required.

Finally, the validated parameters are written to the output file.

---

# Design Decisions

Several design choices were made to improve readability and maintainability.

## Pydantic

Pydantic is used for validating:

* prompts;
* function definitions;
* parameter types;
* return types.

This removes much of the manual validation logic.

---

## Separation of responsibilities

Each module has a single responsibility.

| File                   | Responsibility                       |
| ---------------------- | ------------------------------------ |
| parser_promet.py       | Load prompts                         |
| parser_def_fun.py      | Load function definitions            |
| models.py              | Data validation                      |
| functionselector.py    | Function selection                   |
| constrained_decoder.py | Parameter extraction                 |
| json_constraint.py     | Helper methods for function metadata |
| llm_client.py          | Wrapper around the provided SDK      |

---

## Prompt engineering

Instead of asking the model to produce arbitrary text, prompts explicitly instruct it to:

* generate only JSON;
* avoid explanations;
* avoid Markdown;
* follow the parameter schema exactly.

Few-shot examples are also provided for each function.

---

# Performance Analysis

## Accuracy

The implementation correctly identifies functions and extracts parameters for the provided evaluation dataset.

Pydantic validation prevents malformed inputs from reaching the language model.

---

## Speed

Generation stops as soon as a complete JSON object is detected.

This significantly reduces unnecessary token generation.

---

## Reliability

Reliability is improved through:

* JSON validation;
* parameter validation;
* required parameter checking;
* type conversion;
* exception handling.

---

# Challenges Faced

## JSON generation

Initially, the language model often generated explanations or Markdown around the JSON.

This was solved by improving the prompt and using few-shot examples.

---

## Incomplete JSON

Sometimes generation stopped before the closing brace.

To solve this, generation continues until a balanced JSON object is detected.

---

## Input validation

Manual validation became difficult as the project grew.

Replacing most validation logic with Pydantic made the code cleaner and easier to maintain.

---

## Function selection

Choosing the correct function reliably required carefully designed prompts containing both function names and descriptions.

---

# Testing Strategy

The implementation was tested using:

* valid input files;
* malformed JSON files;
* missing required fields;
* invalid parameter names;
* invalid function names;
* empty prompts;
* duplicate function names;
* incorrect parameter types.

The generated output was compared against the expected results provided by the project.

Static analysis was also performed using:

* flake8
* mypy

---

# Example Usage

Input:

```json
{
    "prompt": "What is the sum of 2 and 3?"
}
```

Generated output:

```json
{
    "prompt": "What is the sum of 2 and 3?",
    "name": "fn_add_numbers",
    "parameters": {
        "a": 2.0,
        "b": 3.0
    }
}
```

---

# Resources

## Documentation

* Pydantic Documentation
* Hugging Face Transformers Documentation

## Articles
- [https://youtu.be/CXepv4ItZzM?si=J9OLc5Z-ryxQc5om]
- [https://youtu.be/p93xuOXP1jI?si=MQkTFgMFycOW4-AS]
* OpenAI Function Calling documentation
* Anthropic Tool Use documentation
* JSON Schema documentation

## AI Usage

Artificial intelligence was used as a learning and development assistant throughout the project.

It was primarily used to:

* explain Pydantic features;
* understand constrained decoding;
* improve prompt engineering;
* review Python code;
* improve documentation;
* clarify error messages and debugging strategies.

All implementation decisions, testing, validation logic, and final code integration were reviewed and completed manually.

---

# License

This project was developed for educational purposes as part of the 42 curriculum.

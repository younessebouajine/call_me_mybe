from llm_sdk import Small_LLM_Model
from typing import Any


class LLMClient:
    """Wrapper around the provided language model SDK.

    This class exposes a simplified interface for encoding text,
    decoding tokens, retrieving logits, and accessing model
    resources.
    """

    def __init__(self) -> None:
        """Initialize the language model."""

        self.model = Small_LLM_Model()

    def encode(self, text: str) -> Any:
        """Encode text into model input IDs.

        Args:
            text: The text to encode.

        Returns:
            The encoded token IDs produced by the language model.
        """

        return self.model.encode(text)

    def decode(self, ids: Any) -> str:
        """Decode token IDs into text.

        Args:
            ids: Sequence of token IDs.

        Returns:
            The decoded text.
        """

        return str(self.model.decode(ids))

    def get_next_token_logits(self, input_ids: Any) -> Any:
        """Compute the logits for the next generated token.

        Args:
            input_ids: Encoded input token IDs.

        Returns:
            The logits for the next token.
        """

        return self.model.get_logits_from_input_ids(input_ids=input_ids)

    def get_vocab_file_path(self) -> str:
        """Return the path to the model vocabulary file.

        Returns:
            The filesystem path to the vocabulary file.
        """

        return str(self.model.get_path_to_vocab_file())

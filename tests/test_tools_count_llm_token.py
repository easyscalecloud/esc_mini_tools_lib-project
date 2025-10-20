# -*- coding: utf-8 -*-

from esc_mini_tools_lib.tools.count_llm_token import (
    CountLlmTokenInput,
    CountLlmTokenOutput,
)


class TestCountLlmTokenInput:
    def test(self):
        input = CountLlmTokenInput(
            text="Hello world!",
        )
        output = input.main()
        assert isinstance(output.result, int)
        assert output.result > 0

        # Test with empty string
        input_empty = CountLlmTokenInput(text="")
        output_empty = input_empty.main()
        assert output_empty.result == 0

        # Test with longer text
        input_long = CountLlmTokenInput(
            text="This is a longer text to count tokens for. It should have more tokens than the simple 'Hello world!' example.",
        )
        output_long = input_long.main()
        assert output_long.result > output.result


if __name__ == "__main__":
    from esc_mini_tools_lib.tests import run_cov_test

    run_cov_test(
        __file__,
        "esc_mini_tools_lib.tools.count_llm_token",
        preview=False,
    )

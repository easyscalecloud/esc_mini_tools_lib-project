# -*- coding: utf-8 -*-

from esc_mini_tools_lib.tools.chinese_to_english_punctuation import (
    ChineseToEnglishPunctuationInput,
    ChineseToEnglishPunctuationOutput,
)


class TestChineseToEnglishPunctuationInput:
    def test(self):
        input = ChineseToEnglishPunctuationInput(
            text="这是Python代码，它使用Flask框架。",
        )
        output = input.main()
        assert output.result == "这是 Python 代码, 它使用 Flask 框架."


if __name__ == "__main__":
    from esc_mini_tools_lib.tests import run_cov_test

    run_cov_test(
        __file__,
        "esc_mini_tools_lib.tools.chinese_to_english_punctuation",
        preview=False,
    )

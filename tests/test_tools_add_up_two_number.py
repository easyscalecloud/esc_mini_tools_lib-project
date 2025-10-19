# -*- coding: utf-8 -*-

from esc_mini_tools_lib.tools.add_up_two_number import (
    AddUpTwoNumberInput,
    AddUpTwoNumberOutput,
)


class TestAddUpTwoNumberInput:
    def test(self):
        input = AddUpTwoNumberInput(
            v1=10,
            v2=20,
        )
        output = input.main()
        assert output.result == 30


if __name__ == "__main__":
    from esc_mini_tools_lib.tests import run_cov_test

    run_cov_test(
        __file__,
        "esc_mini_tools_lib.tools.add_up_two_number",
        preview=False,
    )

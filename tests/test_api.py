# -*- coding: utf-8 -*-

from esc_mini_tools_lib import api


def test():
    _ = api
    _ = api.AddUpTwoNumberInput
    _ = api.AddUpTwoNumberOutput
    _ = api.ChineseToEnglishPunctuationInput
    _ = api.ChineseToEnglishPunctuationOutput
    _ = api.ConfluenceUrlTransformInput
    _ = api.ConfluenceUrlTransformOutput
    _ = api.ConfluencePageExportInput
    _ = api.ConfluencePageExportOutput
    _ = api.CountLlmTokenInput
    _ = api.CountLlmTokenOutput


if __name__ == "__main__":
    from esc_mini_tools_lib.tests import run_cov_test

    run_cov_test(
        __file__,
        "esc_mini_tools_lib.api",
        preview=False,
    )

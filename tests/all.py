# -*- coding: utf-8 -*-

if __name__ == "__main__":
    from esc_mini_tools_lib.tests import run_cov_test

    run_cov_test(
        __file__,
        "esc_mini_tools_lib",
        is_folder=True,
        preview=False,
    )

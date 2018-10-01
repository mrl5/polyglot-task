# -*- coding: utf-8 -*-

import pytest
from worker import evaluate

__author__ = "mrl5"

"""
Scenario:
    - 'evaluate()' function should return expected values
    - 'evaluate()' function should ignore extra whitespaces
    - 'evaluate()' function should rise "IndexError" exception when there are too many operators in RPN expression
    - 'evaluate()' function should rise "CorruptedRPNExpression" custom exception if list is not empty after evaluation
    - 'evaluate()' function should rise "EmptyInput" custom exception if expression is empty
    - 'evaluate()' function should rise "ValueError" when expression has other strings than defined in 'ops' dictionary
"""


def test_evaluate():
    expected_results = {
        "3 4 +": 7,
        "5 1 2 + 4 * + 3 -": 14,
        "1 2 +" : 3,
        "990 1 2 + *": 2970,
        "1000 990 1 2 + * +": 3970
    }
    real_results = {}
    # create dictionary with real results
    for key, value in expected_results.items():
        result = {key: evaluate(key)}
        real_results.update(result)
    assert expected_results == real_results
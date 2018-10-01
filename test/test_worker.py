# -*- coding: utf-8 -*-

import pytest
import subprocess
import os
from worker import evaluate

__author__ = "mrl5"

"""
Scenario:
    - 'evaluate()' function should return expected values
    - 'evaluate()' function should ignore extra whitespaces
    - test if 'evaluate()' function is run when worker.py is executed in console `python worker.py`
    - 'evaluate()' function should rise "IndexError" exception when there are too many operators in RPN expression
    - 'evaluate()' function should rise "CorruptedRPNExpression" custom exception if list is not empty after evaluation
    - 'evaluate()' function should rise "EmptyInput" custom exception if expression is empty
    - 'evaluate()' function should rise "ValueError" when expression has other strings than defined in 'ops' dictionary
"""


@pytest.fixture(scope="function")
def expected_results():
    dictionary = {
        "3 4 +": 7,
        "5 1 2 + 4 * + 3 -": 14,
        "1 2 +": 3,
        "990 1 2 + *": 2970,
        "1000 990 1 2 + * +": 3970
    }
    return dictionary


def test_evaluate(expected_results):
    real_results = {}
    # create dictionary with real results
    for key, value in expected_results.items():
        result = {key: evaluate(key)}
        real_results.update(result)
    assert expected_results == real_results


def test_additional_whitespaces_in_expression(expected_results):
    # add extra expressions to the expected_results dict
    expected_results.update({"3 4 + ": 7})
    expected_results.update({"3  4 +": 7})
    expected_results.update({"3 4  +": 7})
    expected_results.update({" 3 4  +": 7})
    expected_results.update({"3 4 +\t": 7})
    expected_results.update({"3 \t4 +": 7})
    expected_results.update({"\t3 4 + ": 7})
    expected_results.update({"3\t4\t+": 7})
    real_results = {}
    for key, value in expected_results.items():
        result = {key: evaluate(key)}
        real_results.update(result)
    assert expected_results == real_results


def test_shell_subprocess(expected_results):
    test_file_location = os.path.dirname(os.path.realpath(__file__))
    tested_file = os.path.join(os.path.dirname(test_file_location), "worker.py")
    expression = "2 2 +"
    result = evaluate(expression)
    stdout_expected_result = str.encode(str(result) + "\n")
    stdout = subprocess.check_output(["python", tested_file, expression])
    assert stdout == stdout_expected_result


def test_for_IndexError():
    corrupted_expression = "3 4 + -"
    with pytest.raises(IndexError):
        evaluate(corrupted_expression)

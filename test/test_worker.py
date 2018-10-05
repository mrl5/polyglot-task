# -*- coding: utf-8 -*-

import pytest
import subprocess
import os
from worker import Worker

__author__ = "mrl5"

"""
Scenario:
    - 'evaluate()' method should return expected values
    - 'evaluate()' method should ignore extra whitespaces
    - worker.py accepts only one argument else raises "Exception" exception
    - 'evaluate()' method should rise "CorruptedRPNExpressionError" custom exception when there are too many operators in RPN expression
    - 'evaluate()' method should rise "CorruptedRPNExpressionError" custom exception if list is not empty after evaluation
    - 'evaluate()' method should rise "CorruptedRPNExpressionError" custom exception if expression is empty
    - 'evaluate()' method should rise "ValueError" when expression has strings or other chars than defined in 'ops' dictionary
    - test if 'evaluate()' method is run from main()
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


@pytest.fixture(scope="function")
def worker_instance():
    worker = Worker()
    return worker

def test_evaluate_method(expected_results, worker_instance):
    real_results = {}
    # create dictionary with real results
    for key, value in expected_results.items():
        result = {key: worker_instance.evaluate(key)}
        real_results.update(result)
    assert expected_results == real_results


def test_additional_whitespaces_in_expression(expected_results, worker_instance):
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
        result = {key: worker_instance.evaluate(key)}
        real_results.update(result)
    assert expected_results == real_results


def test_for_IndexError(worker_instance):
    corrupted_expression = "3 4 + -"
    with pytest.raises(worker_instance.CorruptedRPNExpressionError):
        worker_instance.evaluate(corrupted_expression)


def test_too_many_numbers(worker_instance):
    corrupted_expression = "2 3 4 +"
    with pytest.raises(worker_instance.CorruptedRPNExpressionError):
        worker_instance.evaluate(corrupted_expression)


def test_for_empty_input(worker_instance):
    empty_input = " "
    with pytest.raises(worker_instance.CorruptedRPNExpressionError):
        worker_instance.evaluate(empty_input)


def test_disallowed_chars_in_expression(worker_instance):
    corrupted_expression = "abc 4 +"
    with pytest.raises(worker_instance.CorruptedRPNExpressionError):
        worker_instance.evaluate(corrupted_expression)


def test_for_main(worker_instance):
    test_file_location = os.path.dirname(os.path.realpath(__file__))
    tested_file = os.path.join(os.path.dirname(test_file_location), "worker.py")
    expression = "1 1 +"
    cp = subprocess.run(["python3", tested_file, expression], stdout=subprocess.PIPE)
    stdout = bytes(cp.stdout).decode().strip()
    assert stdout == str(worker_instance.evaluate(expression))
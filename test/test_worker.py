# -*- coding: utf-8 -*-

import pytest
from worker import evaluate

__author__ = "mrl5"

"""
Scenario:
    - 'evaluate()' function should return expected values
    - 'evaluate()' function should rise "IndexError" exception when there are too many operators in RPN expression
    - 'evaluate()' function should rise "CorruptedRPNExpression" custom exception if list is not empty after evaluation
    - 'evaluate()' function should rise "EmptyInput" custom exception if expression is empty
    - 'evaluate()' function should rise "ValueError" when expression has other strings than defined in 'ops' dictionary
"""

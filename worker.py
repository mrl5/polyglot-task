# -*- coding: utf-8 -*-

# based on Yehonathan Sharvit blog post: https://blog.klipse.tech/python/2016/09/22/python-reverse-polish-evaluator.html
__author__ = "mrl5"


class Worker:
    def __init__(self):
        # arithmetic operators as lambda functions (anonymous functions)
        self._ops = {
            "+": (lambda a, b: a + b),
            "-": (lambda a, b: a - b),
            "*": (lambda a, b: a * b),
            "/": (lambda a, b: a / b)
        }

    def evaluate(self, expression):
        tokens = expression.split()
        stack = []
        try:
            for token in tokens:
                if token in self._ops:
                    number2 = stack.pop()
                    number1 = stack.pop()
                    result = self._ops[token](number1, number2)
                    stack.append(result)
                else:
                    stack.append(int(token))
            output = stack.pop()
            # stack should be empty at this point
            if stack:
                raise self.CorruptedRPNExpressionError
        except IndexError as ie:
            raise self.CorruptedRPNExpressionError from ie
        except ValueError as ve:
            raise self.CorruptedRPNExpressionError from ve
        return output

    class CorruptedRPNExpressionError(Exception):
        """
        Custom exception when Reverse Polish Notation expression has non-valid syntax
        """
        def __init__(self):
            self.strerror = "Expression has non-valid RPN syntax"


def main():
    allowed_args = 2 if sys.argv[0] == __file__ else 1
    if len(sys.argv) != allowed_args:
        raise Exception("Script accepts only one argument.")
    expression = sys.argv[1] if sys.argv[0] == __file__ else sys.argv[0]
    worker = Worker()
    print(worker.evaluate(expression))


if __name__ == "__main__":
    import sys
    main()

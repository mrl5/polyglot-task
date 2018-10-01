# -*- coding: utf-8 -*-

# based on Yehonathan Sharvit blog post: https://blog.klipse.tech/python/2016/09/22/python-reverse-polish-evaluator.html

# loaded from gist: https://gist.github.com/viebel/3d0f146484989b0c5afc29e53e3e9f2c
# This example assumes binary operators, but this is easy to extend.
# Comes from this excellent article: http://blog.reverberate.org/2013/07/ll-and-lr-parsing-demystified.html

# arithmetic operators as lambda functions (anonymous functions)
ops = {
  "+": (lambda a, b: a + b),
  "-": (lambda a, b: a - b),
  "*": (lambda a, b: a * b),
  "/": (lambda a, b: a / b)
}


def evaluate(expression):
    tokens = expression.split()
    stack = []

    for token in tokens:
        if token in ops:
            number2 = stack.pop()
            number1 = stack.pop()
            result = ops[token](number1, number2)
            stack.append(result)
        else:
            stack.append(int(token))
    return stack.pop()


def main():
    expression = sys.argv[1] if (sys.argv[0] == __file__) else sys.argv[0]
    print(evaluate(expression))


if __name__ == "__main__":
    import sys
    main()

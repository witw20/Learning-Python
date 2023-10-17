import re
from collections import deque


def main():
    variables = dict()

    while True:
        exp = input().strip()
        if exp.startswith("/") and exp not in ["/exit", "/help"]:
            print("Unknown command")
        elif exp == "/exit":
            print("Bye!")
            quit()
        elif exp == "/help":
            print("The program calculates the sum of numbers")

        elif "=" in exp:
            assign(variables, exp.split("="))

        elif "**" in exp or r"//" in exp:
            print("Invalid expression")

        elif exp.isalpha() and exp not in variables:
            print("Unknown variable")

        elif exp:
            postfix = to_postfix(parse_exp(exp))
            cal_postfix(variables, postfix)


def assign(variables: dict, exp: list):
    name = exp[0].strip()
    value = exp[-1].strip()
    if not name.isalpha():
        print("Invalid identifier")
    elif len(exp) > 2:
        print("Invalid assignment")
    else:
        try:
            variables[name] = to_num(variables, value)

        except SyntaxError:
            print("Unknown variable")

def cal(variables: dict, exp: list) -> None:
    try:
        result = to_num(variables, exp[0])
        for i in range(1, len(exp), 2):
            result += sign(exp[i]) * to_num(variables, exp[i + 1])
        if result is not None:
            print(result)
    except (SyntaxError, NameError):
        print('Invalid expression')

def cal_postfix(variables: dict, exp: list) -> None:
    try:
        result = to_num(variables, exp[0])
        for i in range(len(exp)):
            # calculate
        if result is not None:
            print(result)
    except (SyntaxError, NameError):
        print('Invalid expression')

def sign(signs: str) -> int:
    return -1 if signs.count("-") % 2 else 1

def to_num(variables: dict, num: str) -> int:
    if num.isalpha() and num not in variables:
        raise SyntaxError
    elif num in variables:
        return variables[num]
    else:
        try:
            return int(num)
        except ValueError:
            print("Invalid identifier")

def parse_exp(text: str) -> list:
    text = re.sub('--', '+', text)
    text = re.sub('[\+]+', '+', text)
    text = re.sub(r'\+-', '-', text)
    return [el.strip() for el in re.split(r'(\W)', text) if el.strip() != '']

def to_postfix(exp: list) -> list:
    print(exp)
    operators = {'+': 0, '-': 0, '*': 1, '//': 1, '^': 2, '(': 100, ')': 100}
    op_stack = deque()
    result = list()

    exp.append(')')
    op_stack.append('(')

    for i in range(len(exp)):
        # print(f"i: {i}")

        if exp[i] not in operators:
            result.append(exp[i])

        elif len(op_stack) == 0 or op_stack == deque(['(']):
            op_stack.append(exp[i])

        elif exp[i] == ')':
            while op_stack[-1] != '(':
                result.append(op_stack.pop())
            op_stack.pop()

        elif exp[i] == '(' or operators[exp[i]] > operators[op_stack[-1]]:
            op_stack.append(exp[i])

        elif operators[exp[i]] <= operators[op_stack[-1]]:
            while op_stack[-1] != '(' or operators[exp[i]] > operators[op_stack[-1]]:
                result.append(op_stack.pop())
            op_stack.append(exp[i])

        # print(op_stack)
        # print(result)

    for _ in range(len(op_stack) - 1):
        result.append(op_stack.pop())

    return result


if __name__ == '__main__':
    main()

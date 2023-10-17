# import re

# text = "000"
# text = re.sub('--', '+', text)
# text = re.sub('[\+]+', '+', text)
# text = re.sub(r'\+-', '-', text)
#
# result = [el.strip() for el in re.split(r'(\W)', text) if el.strip() != '']
# print(result)

from collections import deque

def to_postfix(exp: list) -> list:
    print(exp)
    operators = {'+': 0, '-': 0, '*': 1, '//': 1, '^': 2, '(': 100, ')': 100}
    op_stack = deque()
    result = list()

    exp.append(')')
    op_stack.append('(')

    for i in range(len(exp)):
        print(f"i: {i}")

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

        print(op_stack)
        print(result)

    for _ in range(len(op_stack) - 1):
        result.append(op_stack.pop())

    return result

def main():
    exp = "A + B / C * ( D - A ) ^ F ^ H"
    print(to_postfix(exp.split()))

if __name__ == '__main__':
    main()

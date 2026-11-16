import ast
import operator
import re

_ALLOWED_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
    ast.USub: operator.neg,
    ast.UAdd: operator.pos,
}

def _safe_eval(node):
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        return node.value
    if isinstance(node, ast.BinOp) and type(node.op) in _ALLOWED_OPERATORS:
        left, right = _safe_eval(node.left), _safe_eval(node.right)
        if isinstance(node.op, ast.Pow) and abs(right) > 8:
            raise ValueError("Exponent is too large.")
        result = _ALLOWED_OPERATORS[type(node.op)](left, right)
        if abs(result) > 1e100:
            raise ValueError("Result is too large.")
        return result
    if isinstance(node, ast.UnaryOp) and type(node.op) in _ALLOWED_OPERATORS:
        return _ALLOWED_OPERATORS[type(node.op)](_safe_eval(node.operand))
    raise ValueError("Only numbers and +, -, *, /, //, %, **, and parentheses are allowed.")

def calculate(expression: str):
    if not expression or len(expression) > 200:
        raise ValueError("Enter a valid expression (maximum 200 characters).")
    try:
        tree = ast.parse(expression, mode="eval")
        return _safe_eval(tree.body)
    except ZeroDivisionError:
        raise ValueError("Cannot divide by zero.")
    except (SyntaxError, TypeError):
        raise ValueError("Invalid mathematical expression.")

def count_words(text: str):
    words = re.findall(r"\b[\w'-]+\b", text)
    sentences = len([s for s in re.split(r"[.!?]+", text) if s.strip()])
    return {
        "words": len(words),
        "characters": len(text),
        "sentences": sentences,
    }

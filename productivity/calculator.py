# Very simple calculator exposing a safe eval for arithmetic expressions.
# NOTE: This is intentionally minimal — for production, use a proper parser.
def calc(expr: str):
    allowed = "0123456789+-*/(). %"
    if not all(c in allowed for c in expr):
        raise ValueError("Expression contains invalid characters.")
    return eval(expr, {"__builtins__": {}})


import ast
import operator
from datetime import datetime


# Allowed mathematical operations
OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.Mod: operator.mod,
    ast.USub: operator.neg,
}


def calculator(expression):
    """Safely calculate a mathematical expression."""

    try:
        tree = ast.parse(expression, mode="eval")

        def calculate(node):
            if isinstance(node, ast.Expression):
                return calculate(node.body)

            if isinstance(node, ast.Constant):
                if isinstance(node.value, (int, float)):
                    return node.value
                raise ValueError("Invalid value")

            if isinstance(node, ast.BinOp):
                operation = OPERATORS.get(type(node.op))

                if operation is None:
                    raise ValueError("Operation not allowed")

                return operation(
                    calculate(node.left),
                    calculate(node.right)
                )

            if isinstance(node, ast.UnaryOp):
                operation = OPERATORS.get(type(node.op))

                if operation is None:
                    raise ValueError("Operation not allowed")

                return operation(calculate(node.operand))

            raise ValueError("Invalid expression")

        result = calculate(tree)

        return str(result)

    except Exception:
        return "Unable to calculate that expression."


def get_current_datetime():
    """Get the current local date and time."""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
TOOLS = {
    "calculator": calculator,
    "get_current_datetime": get_current_datetime,
}
TOOL_DESCRIPTIONS = {
    "calculator": {
        "description": "Calculate a mathematical expression.",
        "parameters": {
            "type": "object",
            "properties": {
                "expression": {
                    "type": "string",
                    "description": "The mathematical expression to calculate."
                }
            },
            "required": ["expression"]
        }
    },

    "get_current_datetime": {
        "description": "Get the current local date and time.",
        "parameters": {
            "type": "object",
            "properties": {}
        }
    }
}
def get_tool_definitions():
    """Build Gemini tool definitions from the tool registry."""

    definitions = []

    for name, info in TOOL_DESCRIPTIONS.items():
        definitions.append({
            "type": "function",
            "name": name,
            "description": info["description"],
            "parameters": info["parameters"]
        })

    return definitions
def run_tool(tool_name, arguments):
    """Run a registered tool."""

    if tool_name not in TOOLS:
        return "Unknown tool."

    tool = TOOLS[tool_name]

    try:
        return tool(**arguments)
    except Exception:
        return "Tool execution failed."
from langchain_core.tools import StructuredTool
from pydantic import BaseModel


class MultiplyInput(BaseModel):
    a: float
    b: float


def multiply_numbers(a: float, b: float) -> float:
    """Multiply two numbers and return the result."""
    return a * b


tools_for_agent = [
    StructuredTool.from_function(
        name="multiply_numbers",
        func=multiply_numbers,
        description="Multiplies two numbers and returns the product.",
        args_schema=MultiplyInput,
    )
]

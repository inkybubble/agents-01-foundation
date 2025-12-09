"""
Example 01: Calculator Tool with LLM

Demonstrates the basic tool loop:
1. User asks a math question
2. the LLM decides to use the calculator tool
3. Tool executes and returns result
4. the LLM responds with the answer

Run with: uv run python -m examples.01_example_calculator_tool
"""

from src.tools.registry import ToolRegistry
from src.tools.calculator import CalculatorTool
from src.executor import ToolExecutor
from src.llm import LLM


def main():
    # Setup
    registry = ToolRegistry()
    registry.register(CalculatorTool())
    executor = ToolExecutor(registry)
    llm = LLM(executor)

    # Test query
    query = "What is 15 * 7?"
    print(f"User: {query}")

    messages = [{"role": "user", "content": query}]
    response = llm.chat(messages)

    print(f"Assistant: {response}")


if __name__ == "__main__":
    main()

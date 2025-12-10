# Example 01: Calculator Tool

## Command

```bash
uv run python -m examples.01_example_calculator_tool
```

## Raw Output

```
User: What is 15 * 7?
Assistant: The result of 15 * 7 is 105.
```

## What's Happening

1. User asks a math question
2. LLM recognizes it needs the `calculator` tool
3. LLM calls `calculator(expression="15 * 7")`
4. Tool returns `105`
5. LLM formats the answer for the user

## Key Takeaway

The LLM autonomously decides when to use tools based on the query. No explicit instruction needed.

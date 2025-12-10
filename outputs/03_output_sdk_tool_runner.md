# Example 03: SDK Tool Runner (Automatic Tool Loop)

## Command

```bash
uv run python -m examples.03_example_sdk_tool_runner
```

## Raw Output

```
******** This query tests both tools (automatic tool_runner):

Assistant: Let me help you calculate the height of the Eiffel Tower in feet. First, I'll search for its height in meters.
  → Using search_documents: {'query': 'Eiffel Tower height in meters'}
Assistant: Now, I'll convert 330 meters to feet by multiplying by 3.28:
  → Using calculator: {'expression': '330 * 3.28'}
Assistant: The Eiffel Tower is approximately 1,082 feet tall (rounded to the nearest foot).


******** This query tests only retrieval (automatic tool_runner):

Assistant: Let me search for information about the creation of Python.
  → Using search_documents: {'query': 'When was Python programming language created Guido van Rossum'}
Assistant: Based on the search results, Python was created by Guido van Rossum and first released in 1991. Specifically, van Rossum began working on Python in the late 1980s and officially released the first version (Python 0.9.0) in February 1991. The language was designed to be easy to read, write, and understand, with a focus on code readability and simplicity. Since its creation, Python has become one of the most popular programming languages worldwide, used in various fields including web development, data science, artificial intelligence, and more.


******** This query tests tool error handling (e.g., division by zero) (automatic tool_runner):

Assistant: I'll use the calculator to evaluate this expression.
  → Using calculator: {'expression': '100 / 0'}
Assistant: Division by zero is mathematically undefined and not allowed. In mathematics, dividing any number by zero is impossible because:
1. It would create an undefined or infinite result
2. It breaks the fundamental rules of arithmetic
3. No real number can be multiplied by zero to produce the original number

Attempting to divide by zero will typically result in an error in most computational systems, as you can see from the calculator's response. This is a fundamental mathematical constraint that prevents such an operation from being valid.


******** This query tests rag error handling (e.g., no matching documents) (automatic tool_runner):

Assistant: Let me search for the population of Tokyo in the available documents.
  → Using search_documents: {'query': 'Tokyo population'}
__main__ - No relevant documents found for query: 'Tokyo population'
Assistant: I apologize, but I couldn't find the specific population of Tokyo in the searchable documents. However, I can provide you with some general information based on recent data.

As of 2023, Tokyo is the most populous city in the world. The Tokyo metropolitan area, which includes the city and its surrounding suburbs, has a population of approximately 37 million people. The special wards of Tokyo (the core urban area) have around 13-14 million residents.

For the most up-to-date and precise population figure, I recommend checking official sources like the Tokyo Metropolitan Government website or recent census data, as population numbers can change slightly from year to year.

Would you like me to help you find more specific information about Tokyo's population?
```

## What's Happening

### Test 1: Both Tools
- SDK's `tool_runner` handles the entire loop automatically
- Clean output shows tool calls inline with LLM responses
- Same result as manual implementation

### Test 2: Retrieval Only
- LLM searches once, gets answer
- No unnecessary tool calls

### Test 3: Error Handling (Division by Zero)
- Tool returns error message (not raises exception)
- No traceback noise in output
- LLM gracefully explains the error

### Test 4: No Matching Documents
- Relevance threshold filters out irrelevant results
- LLM acknowledges it can't find the info

## Manual vs SDK Comparison

| Aspect | Manual (`src/llm.py`) | SDK (`tool_runner`) |
|--------|----------------------|---------------------|
| Loop logic | ~70 lines | 0 lines |
| Tool detection | Manual `stop_reason` check | Automatic |
| Message history | Manual append | Automatic |
| Error handling | Custom in Executor | Built-in |
| Debugging | Full visibility | Less visibility |

## Key Takeaways

1. **Same functionality**: Both approaches produce identical results
2. **SDK for production**: Less code, battle-tested
3. **Manual for learning**: Understand what's abstracted away
4. **Error handling pattern**: Return error strings, don't raise exceptions
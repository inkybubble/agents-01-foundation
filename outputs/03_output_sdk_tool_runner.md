# Example 03: SDK Tool Runner (Automatic Tool Loop)

## Command

```bash
uv run python -m examples.03_example_sdk_tool_runner
```

## Raw Output

```
__main__ - No relevant documents found for query: 'Tokyo population total number of inhabitants'


******** This query tests both tools (automatic tool_runner):

A: I'll help you find the height of the Eiffel Tower and convert it to feet. Let me search for the information first.
  → Using search_documents: {'query': 'Eiffel Tower height in meters'}
Assistant: Now, I'll calculate the height in feet by converting 330 meters to feet:
  → Using calculator: {'expression': '330 * 3.28'}
Assistant: The Eiffel Tower is 330 meters tall, which converts to approximately 1,082.4 feet.

To break it down:
- Height in meters: 330 meters
- Conversion factor: 1 meter = 3.28 feet
- Height in feet: 330 × 3.28 = 1,082.4 feet


******** This query tests only retrieval (automatic tool_runner):

A: Let me search for information about the creation of Python.
  → Using search_documents: {'query': 'When was Python programming language created by Guido van Rossum'}
Assistant: Python was created by Guido van Rossum and was first released in 1991. Specifically, van Rossum began working on Python in the late 1980s and officially released the first version (Python 0.9.0) in February 1991. The language was designed to be highly readable and emphasize code readability, with a syntax that allows programmers to express concepts in fewer lines of code compared to languages like C++ or Java.

Fun fact: The name "Python" was inspired by the British comedy group Monty Python, reflecting van Rossum's love for Monty Python's Flying Circus, rather than the snake. The language has since become one of the most popular programming languages worldwide, known for its versatility and use in areas like web development, data science, artificial intelligence, and more.


******** This query tests tool error handling (e.g., division by zero) (automatic tool_runner):

A: I'll use the calculator to evaluate this expression, though I know mathematically that division by zero is undefined.
  → Using calculator: {'expression': '100 / 0'}
Assistant: Division by zero is mathematically undefined and results in an error. In mathematics, dividing any number by zero is not allowed because:
1. It would create an undefined or infinite result
2. It breaks the fundamental rules of mathematical division
3. No real number multiplied by zero can produce a non-zero result

So, 100 ÷ 0 is mathematically impossible and will always result in an error in any computational system.


******** This query tests rag error handling (e.g., no matching documents) (automatic tool_runner):

A: Let me search the documents for information about Tokyo's population.
  → Using search_documents: {'query': 'Tokyo population total number of inhabitants'}
Assistant: I apologize, but I couldn't find specific information about Tokyo's population in the searchable documents. However, based on my existing knowledge, Tokyo is the most populous metropolitan area in the world. As of the most recent estimates:

The Tokyo metropolitan area (Greater Tokyo Area) has a population of approximately 37-38 million people, making it the world's largest metropolitan area. The city proper of Tokyo has around 14 million inhabitants.

For the most up-to-date and precise figure, I recommend consulting recent official Japanese government statistics or international demographic sources, as population numbers can change over time.
```

## What's Happening

**Note:** The "A:" prefix on some lines is due to how the SDK chunks responses. The Tokyo log appears at the top due to output buffering.

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

# Example 02: Retrieval + Calculator (Manual Tool Loop)

## Command

```bash
uv run python -m examples.02_example_retrieval
```

## Raw Output

```
******** This query tests both tools:

User: How tall is the Eiffel Tower in feet? (1 meter = 3.28 feet)
src.executor - Executing tool search_documents
src.executor - Successful execution
src.executor - Executing tool calculator
src.executor - Successful execution
Assistant: The Eiffel Tower is 330 meters tall, which is approximately 1,082 feet tall. More precisely, it is 1,082.4 feet in height.


******** This query tests only retrieval:

User: When was Python created?
src.executor - Executing tool search_documents
src.executor - Successful execution
Assistant: Based on the search results, Python was created by Guido van Rossum and first released in 1991. It was developed as a successor to the ABC programming language, with the goal of creating a language that was easy to read and write. Python has since become one of the most popular programming languages worldwide, known for its simplicity and versatility.

Some interesting additional context is that Guido van Rossum started working on Python in the late 1980s while he was at the Centrum Wiskunde & Informatica (CWI) in the Netherlands, and it was officially released to the public in 1991. The language was named after the British comedy group Monty Python, reflecting van Rossum's love of humor.


******** This query tests tool error handling (e.g., division by zero):

User: What is 100 / 0?
src.executor - Executing tool calculator
src.executor - Failed execution
Assistant: Division by zero is mathematically undefined. In mathematics and computer science, dividing any number by zero is not allowed because:
1. It leads to an undefined or infinite result
2. It creates a mathematical singularity
3. There's no meaningful way to represent the result

In practical computing, attempting to divide by zero typically results in:
- A runtime error
- An undefined or infinity value
- A program crash or exception

So, 100 divided by 0 cannot be calculated. It's mathematically impossible.


******** This query tests rag error handling (e.g., no matching documents):

User: What is the population of Tokyo?
src.executor - Executing tool search_documents
src.retrieval.tool - No relevant documents found for query: 'Tokyo population'
src.executor - Successful execution
Assistant: I apologize, but I couldn't find the exact population in the document search. However, based on my current knowledge, Tokyo is the most populous metropolitan area in the world. The Tokyo metropolitan area (Greater Tokyo Area) has a population of approximately 37-38 million people, while the Tokyo Metropolis (Tokyo proper) has around 14 million inhabitants as of recent estimates.

For the most up-to-date and precise figure, I recommend checking recent official sources like the Tokyo Metropolitan Government or recent census data, as population numbers can change slightly from year to year.
```

## What's Happening

### Test 1: Both Tools
- LLM searches documents → finds "330 metres tall"
- LLM calls calculator → `330 * 3.28 = 1082.4`
- LLM combines both results into final answer

### Test 2: Retrieval Only
- LLM only needs retrieval (no calculation required)
- Correctly identifies when NOT to use calculator

### Test 3: Error Handling (Division by Zero)
- Calculator tool catches the error gracefully
- Executor logs "Failed execution"
- LLM explains the error to the user (no crash)

### Test 4: No Matching Documents
- Relevance threshold (`min_score=0.3`) filters out low-quality matches
- Tool returns "No relevant documents found"
- LLM acknowledges it can't find the info in the knowledge base

## Key Takeaways

1. **Multi-tool orchestration**: LLM chains tools as needed
2. **Graceful error handling**: Errors don't crash the system
3. **Relevance threshold**: Prevents returning low-quality results
4. **Transparency**: LLM acknowledges when info isn't in the docs

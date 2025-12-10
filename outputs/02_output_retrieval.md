# Example 02: Retrieval + Calculator (Manual Tool Loop)

## Command

```bash
uv run python -m examples.02_example_retrieval
```

## Raw Output

```
src.executor - Executing tool search_documents
src.executor - Successful execution
src.executor - Executing tool calculator
src.executor - Successful execution
src.executor - Executing tool search_documents
src.executor - Successful execution
src.executor - Executing tool calculator
src.executor - Failed execution
src.executor - Executing tool search_documents
src.retrieval.tool - No relevant documents found for query: 'Tokyo population current number of inhabitants'
src.executor - Successful execution
src.executor - Executing tool search_documents
src.retrieval.tool - No relevant documents found for query: 'Tokyo metropolitan area population total residents'
src.executor - Successful execution


******** This query tests both tools:

User: How tall is the Eiffel Tower in feet? (1 meter = 3.28 feet)
Assistant: The Eiffel Tower is 330 meters tall, which converts to approximately 1,082.4 feet tall.


******** This query tests only retrieval:

User: When was Python created?
Assistant: Based on the search results, Python was created by Guido van Rossum and first released in 1991. It was developed as a successor to the ABC programming language, aiming to be easy to read, write, and understand. Since its initial release, Python has become one of the most popular programming languages worldwide, known for its simplicity and versatility.

Guido van Rossum is often referred to as Python's "Benevolent Dictator for Life" (BDFL), highlighting his central role in the language's development for many years before stepping back from that position in 2018.


******** This query tests tool error handling (e.g., division by zero):

User: What is 100 / 0?
Assistant: Division by zero is mathematically undefined. In mathematics and most programming languages, dividing a number by zero is an operation that cannot be performed because it leads to an undefined or undefined mathematical result.

This is because:
1. There is no number that, when multiplied by 0, would give you 100
2. Division by zero would create a mathematical singularity
3. It breaks the fundamental rules of arithmetic

So the answer is: Division by zero is undefined, and it's not a valid mathematical operation.


******** This query tests rag error handling (e.g., no matching documents):

User: What is the population of Tokyo?
Assistant: I apologize, but I cannot find the specific population number in the current knowledge base. However, based on my existing knowledge, Tokyo is the world's most populous metropolitan area. The Tokyo metropolitan area, which includes the city and its surrounding suburbs, has a population of approximately 37-38 million people. The city proper (Tokyo Metropolis) has around 14 million inhabitants.

For the most up-to-date and precise figure, I recommend checking recent official sources like the Tokyo Metropolitan Government website or the latest census data.
```

## What's Happening

**Note:** Logging appears at the top because Python buffers stdout/stderr differently. The logs are from all test cases combined.

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

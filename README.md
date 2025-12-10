# Unit 1: The Augmented LLM

The foundation for all agent systems: an LLM enhanced with **tools** and **retrieval** (no **memory** for now).

## What This Project Does

This project implements an **Augmented LLM** from scratch:

1. **Tool System** — Define tools (calculator, retrieval) that the LLM can call autonomously
2. **Retrieval Pipeline** — Chunk documents, embed with sentence-transformers, search with numpy
3. **Manual Tool Loop** — See exactly how tool calling works under the hood
4. **SDK Comparison** — Same functionality using Anthropic's `tool_runner` (zero loop code)

> **Note:** Memory is not implemented yet

![The Augmented LLM](figures/augmented_llm.png)

## Contents

  - [Quick Start](#quick-start)
  - [Project Structure](#project-structure)
  - [Examples](#examples)
  - [Key Concepts](#key-concepts)
  - [Requirements](#requirements)

## Quick Start

```bash
# Install dependencies
uv sync

# Run examples
uv run python -m examples.01_example_calculator_tool    # Basic tool usage
uv run python -m examples.02_example_retrieval          # Manual tool loop (retrieval and tool usage)
uv run python -m examples.03_example_sdk_tool_runner    # SDK automatic tool loop
```

## Project Structure

```
src/
    tools/
        base.py          # Tool abstract base class
        registry.py      # Tool registration & lookup
        calculator.py    # Example tool
    retrieval/
        chunker.py       # Text splitting
        embedder.py      # sentence-transformers wrapper
        index.py         # Numpy vector store (with relevance threshold)
        tool.py          # Retrieval as a tool
    executor.py          # Tool execution with error handling
    llm.py               # LLM API wrapper with manual tool loop

examples/
    01_example_calculator_tool.py    # Single tool demo
    02_example_retrieval.py          # Multi-tool with manual loop
    03_example_sdk_tool_runner.py    # SDK's automatic tool_runner

outputs/                             # Documented example outputs
    01_output_calculator_tool.md
    02_output_retrieval.md
    03_output_sdk_tool_runner.md
```

## Examples

### 1. Calculator Tool

The LLM decides when to use tools based on the query:

```
User: What is 15 * 7?
Assistant: The result of 15 * 7 is 105.
```

### 2. Retrieval + Calculator (Manual Tool Loop)

Combining multiple tools — retrieval finds the facts, calculator does the math:

```
User: How tall is the Eiffel Tower in feet? (1 meter = 3.28 feet)
src.executor - Executing tool search_documents
src.executor - Successful execution
src.executor - Executing tool calculator
src.executor - Successful execution
Assistant: The Eiffel Tower is 330 meters tall, which converts to approximately 1,082.4 feet tall.
```

Error handling (division by zero):
```
User: What is 100 / 0?
src.executor - Executing tool calculator
src.executor - Failed execution
Assistant: Division by zero is mathematically undefined and not a valid mathematical operation.
```

No matching documents (relevance threshold filters low-quality matches):
```
User: What is the population of Tokyo?
src.retrieval.tool - No relevant documents found for query: 'Tokyo population...'
Assistant: I cannot find the exact population in the current document base...
```

### 3. SDK Tool Runner (Automatic Tool Loop)

Same functionality using the Anthropic SDK's built-in `tool_runner`:

```
LLM: I'll help you calculate the height of the Eiffel Tower in feet.
  → Using search_documents: {'query': 'Eiffel Tower height in meters'}
LLM: Now, I'll convert 330 meters to feet:
  → Using calculator: {'expression': '330 * 3.28'}
LLM: The Eiffel Tower is approximately 1,082 feet tall.
```

**Manual vs SDK:** Example 02 shows the full tool loop we built from scratch (~70 lines in `src/llm.py`). Example 03 shows the SDK handling it automatically — same result, but without any loop code.

> **Full outputs:** See the [`outputs/`](outputs/) folder for detailed documentation of all test cases, including error handling and edge cases.

## Key Concepts

**Tool Design > Prompt Engineering**

Good tools have:
- Clear descriptions (the LLM reads these to decide when to use them)
- Input schemas with examples
- Graceful error handling

**The Tool Loop**

![The Tool Loop](figures/tool_loop.png)

## Requirements

- Python 3.12+
- Anthropic API key (set `ANTHROPIC_API_KEY` env var)

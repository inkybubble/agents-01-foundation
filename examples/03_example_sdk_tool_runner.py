"""
  Example 03: SDK Tool Runner

  Same functionality as 02_example_retrieval, but using
  the anthropic SDK's built-in tool_runner instead of
  our manual LLM wrapper.

  Run with: uv run python -m examples.03_example_sdk
  """
# %%
# Imports
import os
import logging
from anthropic import Anthropic, beta_tool


os.environ["TOKENIZERS_PARALLELISM"] = "false"

logging.basicConfig(level=logging.INFO, format="%(name)s - %(message)s")
logging.getLogger("httpx").setLevel(logging.WARNING)
logging.getLogger("sentence_transformers").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

# --- Retrieval setup (reuse your existing classes) ---
from src.retrieval.embedder import Embedder
from src.retrieval.index import VectorIndex

# %%

def setup_index() -> VectorIndex:
    """Set up the vector index with sample documents."""
    embedder = Embedder()
    index = VectorIndex(embedder)

    index.add_document("""
        The Eiffel Tower is a wrought-iron lattice tower in Paris, France.
        It was constructed from 1887 to 1889. The tower is 330 metres tall.
    """)

    index.add_document("""
        Python is a high-level programming language created by Guido van Rossum.
        It was first released in 1991.
    """)

    return index


def main():
    # Calculator function
    @beta_tool
    def calculator(expression: str) -> str:
        """
            Evaluate a mathematical expression.

            Args:
                expression: The math expression to evaluate (e.g., "2 + 2")
        """
        allowed_characters="0123456789+-*/(). "
        if not all(c in allowed_characters for c in expression):
            raise ValueError(f"Invalid characters in expression")
        try:
            return str(eval(expression))
        except Exception as e:
            return f"Error: {e}"
    

    # Set up retrieval
    index=setup_index()

    num_results=3

    @beta_tool
    def search_documents(query: str) -> str:
        """
            Search through the knowledge base for relevant information.

            Use this when you need to find specific facts or context from the indexed documents.

            Args:
                query: What information you're looking for. Be specific.
        """
        result=index.search(query=query, top_k=num_results)
        if not result:
            logger.info(f"No relevant documents found for query: '{query}'")
            return "No relevant documents found"
        else:
            formatted=[]
            for i, (chunk, score) in enumerate(result, 1):
                formatted.append(f"[{i}] (relevance: {score:.2f})\n{chunk}")
            return "\n\n---\n\n".join(formatted)

    client = Anthropic()

    def query_tester(query: str) -> None:

        runner = client.beta.messages.tool_runner(
            model="claude-3-5-haiku-20241022",  # or your preferred model
            max_tokens=1024,
            tools=[calculator, search_documents],
            messages=[{"role": "user", "content": query}]
        )

        for message in runner:
            for block in message.content:
                if hasattr(block, 'text'):
                    print(f"Assistant: {block.text}")
                elif block.type == 'tool_use':
                    print(f"  → Using {block.name}: {block.input}")

    print("\n\n******** This query tests both tools (automatic tool_runner):\n")
    query_tester("How tall is the Eiffel Tower in feet? (1 meter = 3.28 feet)")

    print("\n\n******** This query tests only retrieval (automatic tool_runner):\n")
    query_tester("When was Python created?")

    print("\n\n******** This query tests tool error handling (e.g., division by zero) (automatic tool_runner):\n")
    query_tester("What is 100 / 0?")

    print("\n\n******** This query tests rag error handling (e.g., no matching documents) (automatic tool_runner):\n")
    query_tester("What is the population of Tokyo?")

if __name__ == "__main__":
    main()
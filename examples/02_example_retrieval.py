"""
  Example 02: Retrieval + Calculator with LLM

  Demonstrates the full augmented LLM:
  1. Index some documents
  2. User asks a question requiring both retrieval AND calculation
  3. LLM searches documents, then calculates

  Run with: uv run python -m examples.02_example_retrieval
  """

from src.tools.registry import ToolRegistry
from src.tools.calculator import CalculatorTool
from src.retrieval.embedder import Embedder
from src.retrieval.index import VectorIndex
from src.retrieval.tool import RetrievalTool
from src.executor import ToolExecutor
from src.llm import LLM

import logging

import os
os.environ["TOKENIZERS_PARALLELISM"] = "false"

logging.basicConfig(
    level=logging.INFO,
    format="%(name)s - %(message)s"
)
# Silence noisy libraries
logging.getLogger("httpx").setLevel(logging.WARNING)
logging.getLogger("sentence_transformers").setLevel(logging.WARNING)

# %%
def main():
    # 1. Set up retrieval
    embedder = Embedder()
    index = VectorIndex(embedder)

    # 2. Add some documents
    index.add_document(
        """
        The Eiffel Tower is a wrought-iron lattice tower in Paris, France.
        It was constructed from 1887 to 1889. The tower is 330 metres tall.
        """
    )

    index.add_document(
        """
        Python is a high-level programming language created by Guido van Rossum. It was first released in 1991.
        """
    )

    # 3. Set up tools
    registry = ToolRegistry()
    registry.register(CalculatorTool())
    registry.register(RetrievalTool(index))

    # 4. Set up LLM
    executor = ToolExecutor(registry)
    llm = LLM(executor)

    # 5. Test query that needs BOTH tools
    query = "How tall is the Eiffel Tower in feet? (1 meter = 3.28 feet)"
    print(f"User: {query}")

    messages = [{"role": "user", "content": query}]
    response = llm.chat(messages)
    print(f"Assistant: {response}")


if __name__ == "__main__":
    main()
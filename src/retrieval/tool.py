# %%
# Imports
from ..tools.base import Tool
from .index import VectorIndex

# %%
# Retrieval Tool class

class RetrievalTool(Tool):
    """search through indexed documents"""

    def __init__(self, index: VectorIndex):
        self.index=index

    @property
    def name(self)->str:
        return "search_documents"
    
    @property
    def description(self)->str:
        return """Search through the knowledge base for relevant information. Use this when you need to find specific facts, context, or details from the indexed documents. Returns the most relevant text passages."""
    
    @property
    def input_schema(self)->dict:
        """needs `query` (required) and "num_results" (optional, default=3)"""
        input_schema={}
        input_schema["type"]="object"
        input_schema["properties"]={}
        input_schema["properties"]["query"]={}
        input_schema["properties"]["query"]["type"]="string"
        input_schema["properties"]["query"]["description"]="The search query what information you're looking for. Be specific and use keywords."
        input_schema["properties"]["num_results"]={}
        input_schema["properties"]["num_results"]["type"]="number"
        input_schema["properties"]["num_results"]["description"]="Number of results to return (default: 3). Use more for broad topics, fewer for specific facts."
        input_schema["properties"]["num_results"]["default"]=3
        input_schema["required"]=["query"]
        return input_schema
    
    def execute(self, query: str, num_results:int=3)-> str:
        """
        Executes the retrieval tool
        
        # 1. Call self.index.search(query, top_k=num_results)
        # 2. Format results as a readable string
        # 3. Return "No relevant documents found." if empty
        """
        result=self.index.search(query=query, top_k=num_results)
        if not result:
            return "No relevant documents found"
        else:
            formatted=[]
            for i, (chunk, score) in enumerate(result, 1):
                formatted.append(f"[{i}] (relevance: {score:.2f})\n{chunk}")
            return "\n\n---\n\n".join(formatted)
# %%
# Imports

from abc import ABC, abstractmethod
from typing import Any

# %%
# Base tool class
class Tool(ABC):
    """
    Base class for all tools
    """


    @property
    @abstractmethod
    def name(self) -> str:
        """Tool name (used in API calls)."""
        pass

    @property
    @abstractmethod
    def description(self) -> str:
        """Clear description of what this tool does. This is what the LLM sees"""

    @property
    @abstractmethod
    def input_schema(self)-> dict:
        """JSON schema for tool inputs
        This is the input schema:
        
        {
            "type": "object",
            "properties": {
                "expression": {
                    "type": "string",
                    "description": "The math expression to evaluate"
                }
            },
            "required": ["expression"]
        }
        
        """
        pass

    @abstractmethod
    def execute(self, **kwargs) -> Any:
        """execute the tool with given inputs"""
        pass

    def to_anthropic_format(self)-> dict:
        """Convert to anthropic API tool format."""
        dict_out={}
        dict_out["name"]=self.name
        dict_out["description"]=self.description
        dict_out["input_schema"]=self.input_schema
        return dict_out
# %%
# Imports

from typing import Dict, Optional, Any
from .base import Tool

# %%
# Tool Registry
'''A container that
- stores tools by name
- lets you look up a tool by name
- returns all tools in anthropic api format
- executes a tool by name
'''

class ToolRegistry:
    """Registry for managing available tools"""
    
    def __init__(self):
        self._tools: Dict[str, Tool]={}

    def register(self, tool: Tool) -> None:
        """Register a tool"""
        self._tools[tool.name]=tool

    def get(self, name: str)->Optional[Tool]:
        """Get a tool by name. Returns None if not found"""
        if name in self._tools.keys():
            return self._tools[name]
        else:
            return None
        
    def list_tools(self)-> list[dict]:
        """return a list of tool.to_anthropic_format() for each tool"""
        return [tool.to_anthropic_format() for tool in self._tools.values()]

    def execute(self, name: str, **kwargs) -> Any:
        """Execute a tool by name. Raises ValueError if tool is not found"""
        if name in self._tools.keys():
            return self._tools[name].execute(**kwargs)
        else:
            raise ValueError(f"Unknown tool: {name}")
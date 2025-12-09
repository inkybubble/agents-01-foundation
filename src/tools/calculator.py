# %%
# Imports
from .base import Tool

# %%
# Calculator tool implementation

class CalculatorTool(Tool):
    """A simple calculator for basic arithmetics"""

    @property
    def name(self)->str:
        return "calculator"
    
    @property
    def description(self) -> str:
        return "Evaluate a mathematical expression. Use this for any arithmetic calculations. Supports: +, -, *, / (division), ** (power), parentheses, and decimal numbers. Example: '(10 + 5) * 2' returns 30."


    @property
    def input_schema(self)->dict:
        '''
        
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

        '''
        input_schema={}
        input_schema["type"]="object"
        input_schema["properties"]={}
        input_schema["properties"]["expression"]={}
        input_schema["properties"]["expression"]["type"]="string"
        input_schema["properties"]["expression"]["description"]="The math expression to evaluate. Use numbers, operators (+, -, *, /, **), parentheses, and spaces. Example: '15 * 7' or '(100 + 50) / 3'"
        input_schema["required"]=["expression"]
        return input_schema

    def execute(self, expression:str)-> float:
        allowed_characters="0123456789+-*/(). "
        if not all(c in allowed_characters for c in expression):
            raise ValueError(f"Invalid characters in expression")
        try:
            return eval(expression)
        except Exception as e:
            raise ValueError(f"Could not evaluate '{expression}': {e}")

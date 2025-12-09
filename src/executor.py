# %%
# Imports

import logging
from typing import Any
from .tools.registry import ToolRegistry

logger=logging.getLogger(__name__)

# %%
# Tool Executor
'''
The executor wraps tool execution with:
  1. Logging — so you can see what's happening
  2. Error handling — catches exceptions and returns structured results
  3. Metadata — returns success/failure status with the result
'''

class ToolExecutor:
    """Executes tools with error handling and logging"""

    def __init__(self, registry: ToolRegistry):
        self.registry=registry

    def execute(self, tool_name: str, tool_input: dict)-> dict:
        """Execute a tool and return result with metadata. Specifically::
        # 1. logger.info(...) that we're executing the tool
        # 2. Try: result = self.registry.execute(tool_name, **tool_input)
        # 3. On success: logger.info(...), return {"success": True, "result": result}
        # 4. On ValueError: logger.warning(...), return {"success": False, "error": str(e), "error_type": "user_error"}
        # 5. On other Exception: logger.error(...), return {"success": False, "error": str(e), "error_type": "system_error"}
        """
        logger.info(f"Executing tool {tool_name}")

        # 2. Try to get a result
        try:
            result=self.registry.execute(tool_name, **tool_input)
            logger.info("Successful execution")
            return {
                "success": True,
                "result": result
            }
        except ValueError as e:
            logger.warning("Failed execution")
            return {
                "success": False,
                "error": str(e),
                "error_type": "user_error"
            }
        except Exception as e:
            logger.error("Failed execution")
            return {
                "success": False,
                "error": str(e),
                "error_type": "system_error"
            }

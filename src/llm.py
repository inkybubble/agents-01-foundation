# %%
#  Imports
import anthropic
from typing import Optional
from .executor import ToolExecutor

from pdb import set_trace

# %%
# LLM class
'''This is the LLM wrapper:
    1. Sends messages to LLM via the Anthropic API
    2. Detects when LLM wants to use a tool
    3. Executes the tool via the Executor
    4. Sends the result back to LLM
    5. Repeats until LLM gives a final text response
'''
class LLM:
    """Wrapper for Antrhoopic API with tool support"""

    def __init__(
            self,
            executor: ToolExecutor,
            # model: str="claude-sonnet-4-5-20250514" # for final version
            model: str="claude-3-5-haiku-20241022" #for debugging
    ):
        self.client=anthropic.Anthropic()
        self.executor=executor
        self.model=model


    def chat(
           self,
           messages: list[dict],
           system: Optional[str]=None,
           max_tokens: int=1024,
           max_iterations: int=10, 
    )->str:
        """
        Send a message and handle tool calls automaticallt
        Args:
            messages: List of {"role": "user"|"assistant", "content": "..."}
            system: Optional system prompt (i.e., instructions)
            max_tokens: Max reponse length

        Returns:
            The final text response from the LLM 
        """
        # 0. Set the tool list # list[dict]
        tools = self.executor.registry.list_tools()
        # 1. Call the llm api
        iterations=0
        while True:
            if iterations>=max_iterations:
                return "Max tool iterations reached"
            iterations+=1
            response=self.client.messages.create(
                model=self.model,
                max_tokens=max_tokens,
                system=system or "You are a helpful assistant. Use the available tools whenever needed.",
                tools=tools,
                messages=messages
            )
            messages.append(
                {
                    "role": "assistant",
                    "content": response.content
                }
            )
        # 2. Check if lm wants to use tools:
            if response.stop_reason=="tool_use":
                # find tool_use blocks in response.content
                blocks_tool=[block for block in response.content if block.type=="tool_use"]
                tool_call_content_list=[]
                for block in blocks_tool:
                # execute each tool
                    call_id=block.id
                    call_input=block.input
                    call_name=block.name
                    call_result=self.executor.execute(
                        tool_name=call_name,
                        tool_input=call_input
                    )                       
                # append assistant response + tool results to messages
                    tool_call_content_list.append(
                        {
                            "type": "tool_result",
                            "tool_use_id": call_id,
                            "content": str(call_result["result"]) if call_result["success"] else call_result["error"]
                        }
                    )
                messages.append({
                    "role": "user",
                    "content": tool_call_content_list
                })
            else:
                # No more tools - extract and return text: find the text block in response.content and return it
                text_block=[block for block in response.content if block.type=="text"]
                if len(text_block)>0:
                    return text_block[0].text
                return ""
# %%
# main gate for debugging purposes

if __name__=="__main__":

    from .tools.registry import ToolRegistry
    from .tools.calculator import CalculatorTool

    registry = ToolRegistry()
    registry.register(CalculatorTool())
    executor = ToolExecutor(registry)
    llm = LLM(executor)
    messages=[
        {"role": "user",
         "content": "What is 15*7"} #105
    ]
    response=llm.chat(messages)
    print(response)
        

from dataclasses import dataclass
from typing import Any, Callable

@dataclass
class Tool:
    name: str
    description: str
    parameters: dict[str, Any]
    function: Callable

class ToolRegistry:
    def __init__(self):
        self._tools: dict[str, Tool] = {}

    def register(
        self,
        name: str,
        description: str,
        parameters: dict[str, Any],
        function: Callable
    ) -> None:
    
        if name in self._tools:
            raise ValueError(f"Tool already registered: {name}")

        self._tools[name] = Tool(
            name=name,
            description=description,
            parameters=parameters,
            function=function
        )

    def get(self, name:str) -> Tool:
        tool = self._tools.get(name)
        
        if tool is None:
            raise ValueError(f"Unknown tool: {name}")
        return tool
    
    def get_schemas(self) -> list[dict[str, Any]]:
        return [
            {
                "type": "function",
                "function": {
                    "name": tool.name,
                    "description": tool.description,
                    "parameters": tool.parameters
                }
            }
            for tool in self._tools.values()
        ]

    def list_tools(self) -> list[str]:
        return list(self._tools.keys())
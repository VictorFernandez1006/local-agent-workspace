import json
from typing import Any
from local_agent_workspace.core.tools.tool_registry import ToolRegistry

class ToolExecutor:
    def __init__(self, registry: ToolRegistry):
        self.registry = registry

    def execute(
        self,
        tool_name: str, 
        arguments: str
    ) -> Any:

        tool = self.registry.get(tool_name)

        try:
            parsed_arguments = json.loads(arguments)
        except json.JSONDecodeError as exc:
            raise ValueError("Invalid tool arguments JSON") from exc
        
        if not isinstance(parsed_arguments, dict):
            raise ValueError("Tool arguments must be a JSON object")
        
        allowed_parameters = set(
            tool.parameters.get("properties", {}).keys()
        )

        required_parameters = set(
            tool.parameters.get("required", [])
        )

        provided_parameters = set(parsed_arguments.keys())

        if not provided_parameters.issubset(allowed_parameters):
            raise ValueError("Unexpected tool arguments")
        if not required_parameters.issubset(provided_parameters):
            raise ValueError("Missing required tool arguments")

        return tool.function(**parsed_arguments)
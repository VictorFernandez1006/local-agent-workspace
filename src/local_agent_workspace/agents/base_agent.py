from local_agent_workspace.core.llm.llm_client import LLMClient

class BaseAgent:

    def __init__(
        self,
        name: str,
        system_prompt: str,
        llm_client: LLMClient
        ):
        self.name = name
        self.system_prompt = system_prompt
        self.llm_client = llm_client

    def run(self, task: str) -> str:
        if not task.strip():
            raise ValueError("The task cannot be empty")
        return self.llm_client.generate(
            system_prompt=self.system_prompt,
            prompt=task
        )            
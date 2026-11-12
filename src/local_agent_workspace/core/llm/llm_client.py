from openai import OpenAI
from local_agent_workspace.config.settings import settings

class LLMClient:
    def __init__(self):
        self._client = OpenAI(
            base_url=settings.llm_base_url,
            api_key=settings.llm_api_key,
            timeout=settings.llm_timeout
        )

        self.model = settings.llm_model

    def generate(
        self,
        prompt: str,
        system_prompt: str | None = None
    ) -> str:
        if not prompt.strip():
            raise ValueError("The prompt cannot be empty")

        messages = []

        if system_prompt:
            messages.append(
                {
                    "role": "system",
                    "content": system_prompt
                }
            )

        messages.append({
            "role": "user",
            "content": prompt
        })              

        response = self.chat_completion(messages)

        content = response.choices[0].message.content

        if content is None:
            raise RuntimeError("The LLM returned an empty response")

        return content

    def chat_completion(
        self,
        messages: list[dict],
        tools: list[dict] | None = None
    ):
    
        request = {
            "model": self.model,
            "messages": messages,
            "temperature": settings.llm_temperature
        }

        if tools:
            request["tools"] = tools
            request["tool_choice"] = "auto"

        return self._client.chat.completions.create(**request)
from ast import arguments
import json
from re import S
from unittest import result
from local_agent_workspace.agents.base_agent import BaseAgent
from local_agent_workspace.core.llm.llm_client import LLMClient
from local_agent_workspace.core.tools.tool_registry import ToolRegistry
from local_agent_workspace.core.tools.tool_executor import ToolExecutor

class ResearchAgent(BaseAgent):
    def __init__(
        self, 
        llm_client: LLMClient,
        tool_registry: ToolRegistry,
        max_iterations: int = 5
        ):
        system_prompt="""
        Eres un agente de investigación especializado en
        arquitectura de software y sistemas bancarios.

        Tienes acceso a herramientas que son ejecutadas
        por la aplicación anfitriona en tu nombre.

        IMPORTANTE:

        PUEDES utilizar las herramientas disponibles.
        No afirmes que no puedes ejecutar herramientas.

        PROCEDIMIENTO DE INVESTIGACIÓN:

        1. Utiliza `search_files` para localizar documentos relevantes.
        2. Examina los resultados de la búsqueda.
        3. Utiliza `read_file` cuando necesites el contenido completo
        de un documento relevante.
        4. Emplea el contenido del documento recuperado como
        evidencia para tu respuesta.
        5. Analiza la información y elabora
        un informe técnico estructurado.

        REGLAS:

        - No inventes el contenido de los documentos.
        - No afirmes haber leído documentos
        que no han sido recuperados.
        - Distingue los hechos documentados de
        tus propias conclusiones técnicas.
        - Si no encuentras documentos relevantes,
        informa explícitamente sobre esa limitación.
        - Si una herramienta devuelve un error, explícalo
        en lugar de inventar información.
        - No proporciones una respuesta definitiva antes
        de revisar el contenido de los documentos relevantes.
        """

        super().__init__(
            name="ResearchAgent",
            system_prompt=system_prompt,
            llm_client=llm_client
        )
        
        self.tool_registry = tool_registry
        self.tool_executor = ToolExecutor(tool_registry)
        self.max_iterations = max_iterations

    def run(self, task: str) -> str:
        if not task.strip():
            raise ValueError("The task cannot be empty")
        
        messages = [
            {
                "role": "system",
                "content": self.system_prompt
            },
            {
                "role": "user",
                "content": task
            }
        ]

        tool_schemas = self.tool_registry.get_schemas()

        for iteration in range(self.max_iterations):
            print(f"\n[Agent Loop] Iteration {iteration + 1}")

            response = self.llm_client.chat_completion(
                messages=messages,
                tools=tool_schemas
            )

            assistant_message = response.choices[0].message

            # No more tools calls: return final answer
            if not assistant_message.tool_calls:
                return assistant_message.content or ""

            # Preserve the assistant tool-call message
            messages.append(
                assistant_message.model_dump(exclude_none=True)
            )

            # Execute requested tools
            for tool_call in assistant_message.tool_calls:

                tool_name = tool_call.function.name
                arguments = tool_call.function.arguments

                print(f"\n[Tool Calling] Executing: {tool_name}")
                print(f"[Tool Calling] Arguments: {arguments}")

                try:
                    result = self.tool_executor.execute(
                        tool_name=tool_name,
                        arguments=arguments
                    )

                    tool_result = {
                        "success": True,
                        "result": result
                    }
                except Exception as exc:
                    tool_result = {
                        "success": False,
                        "error": str(exc)
                    }
                
                print(
                "[Tool Result] "
                + json.dumps(tool_result, ensure_ascii=False)[:1500]
                )                    

                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": json.dumps(
                        tool_result,
                        ensure_ascii=False
                    )
                })

        raise RuntimeError(
            "Maximum agent iterations reached"
        )


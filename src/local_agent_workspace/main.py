
from local_agent_workspace.core.llm.llm_client import LLMClient
from local_agent_workspace.agents.research_agent import ResearchAgent
from local_agent_workspace.core.tools import tool_registry
from local_agent_workspace.core.tools.tool_registry import ToolRegistry
from local_agent_workspace.core.tools.register_tools import register_file_tools

def main():
    # 1. Initialize LLM client
    llm_client = LLMClient()

    # 2. Initialize tool registry
    tool_registry = ToolRegistry()

    # 3. Register available tools
    register_file_tools(tool_registry)

    print("Available tools:")
    for tool in tool_registry.list_tools():
        print(f"-{tool}")
    
    # 4. Initialize Research Agent

    research_agent = ResearchAgent(
        llm_client=llm_client,
        tool_registry=tool_registry,
        max_iterations=5
    )

    # 5. Execute research task

    response = research_agent.run(
        """
        Investiga cómo funcionan las compensaciones
        en transferencias bancarias.

        Consulta los documentos disponibles en mi
        repositorio de conocimiento.

        Explica los conceptos documentados,
        identifica los mecanismos involucrados
        y presenta los principales riesgos técnicos.

        Diferencia la información encontrada
        en los documentos de tus propias
        conclusiones técnicas.
        """
    )
    print("\n=== RESEARCH AGENT RESPONSE ===\n")
    print(response)

if __name__ == "__main__":
    main()
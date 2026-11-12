
from local_agent_workspace.core.llm.llm_client import LLMClient
from local_agent_workspace.agents.research_agent import ResearchAgent

def main():
    llm_client = LLMClient()

    research_agent = ResearchAgent(
        llm_client=llm_client
    )

    print(f"\nAgent: {research_agent.name}")

    response = research_agent.run(
        """
        Investiga cómo funciona un transferencia
        interbancaria en una arquitectura basada 
        en microservicios.

        Explica los componentes involucrados,
        sus responsabilidades y los principales
        riesgos técnicos.
        """
    )
    print("\n=== RESEARCH AGENT RESPONSE ===\n")
    print(response)

if __name__ == "__main__":
    main()
from local_agent_workspace.core.llm.llm_client import LLMClient

def main():
    llm_client = LLMClient()

    response = llm_client.generate(
        system_prompt=(
            "Eres un arquitecto de software "
            "especializado en sistemas bancarios"
        ),
        prompt=(
            "Explica cómo funciona un sistema "
            "de transferencias bancarias basado "
            "en microservicios"
        )
    )

    print("\n=== LLM RESPONSE ===\n")
    print(response)

if __name__ == "__main__":
    main()
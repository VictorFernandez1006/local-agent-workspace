from unittest.mock import Mock
from local_agent_workspace.core.llm import llm_client
import pytest
from local_agent_workspace.agents.research_agent import ResearchAgent

def test_research_agent_executes_task():
    llm_client = Mock()

    llm_client.generate.return_value = (
        "A bank transfer involves multiple services."
    )

    agent = ResearchAgent(
        llm_client=llm_client
    )

    result = agent.run(
        "Explain bank transfers."
    )
    
    assert agent.name == "ResearchAgent"
    assert result == (
       "A bank transfer involves multiple services."
    )
    llm_client.generate.assert_called_once()

def test_research_agent_reject_empty_task():
    llm_client = Mock()    
    agent = ResearchAgent(
        llm_client=llm_client
    )

    with pytest.raises(ValueError):
        agent.run(" ")

    llm_client.generate.assert_not_called()
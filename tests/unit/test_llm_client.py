from email import message
from nt import system
from random import choices
from types import SimpleNamespace
from unittest import result
from unittest.mock import patch

from local_agent_workspace.core.llm import llm_client
import pytest

from local_agent_workspace.core.llm.llm_client import LLMClient

@patch("local_agent_workspace.core.llm.llm_client.OpenAI")
def test_generate_returns_llm_response(mock_openai):
    mock_client = mock_openai.return_value

    mock_client.chat.completions.create.return_value = (
        SimpleNamespace(
            choices=[
                SimpleNamespace(
                    message=SimpleNamespace(
                        content="A microservice is an independent service."
                    )
                )
            ]
        )
    )

    llm_client = LLMClient()

    result = llm_client.generate(
        prompt="What is a microservice?"
    )

    assert result == "A microservice is an independent service."

    mock_client.chat.completions.create.assert_called_once()


@patch("local_agent_workspace.core.llm.llm_client.OpenAI")    
def test_generate_includes_system_prompt(mock_openai):
    mock_client = mock_openai.return_value

    mock_client.chat.completions.create.return_value = (
        SimpleNamespace(
            choices=[
                SimpleNamespace(
                    message=SimpleNamespace(content="Backing response")
                )
            ]
        )
    )
    llm_client = LLMClient()

    llm_client.generate(
        system_prompt="You are a banking architect.",
        prompt="Explain payment processing."
    )

    call_args = mock_client.chat.completions.create.call_args

    messages = call_args.kwargs["messages"]

    assert messages[0]["role"] == "system"
    assert messages[0]["content"] == "You are a banking architect."

    assert messages[1]["role"] == "user"
    assert messages[1]["content"] == "Explain payment processing."

@patch("local_agent_workspace.core.llm.llm_client.OpenAI")    
def test_generate_rejects_empty_prompt(mock_openai):
    llm_client = LLMClient()

    with pytest.raises(ValueError):
        llm_client.generate(prompt="    ")
    
    mock_openai.return_value.chat.completions.create.assert_not_called()

@patch("local_agent_workspace.core.llm.llm_client.OpenAI")
def test_generate_rejects_empty_response(mock_openai):

    mock_client = mock_openai.return_value

    mock_client.chat.completions.create.return_value = (
        SimpleNamespace(
            choices=[
                SimpleNamespace(
                    message=SimpleNamespace(content=None)
                )
            ]
        )
    )

    llm_client = LLMClient()

    with pytest.raises(RuntimeError):
        llm_client.generate(prompt="Explain microservices.")     
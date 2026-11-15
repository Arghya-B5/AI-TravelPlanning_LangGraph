import json
from typing import Iterator

from langchain_core.messages import HumanMessage, SystemMessage
from src.tools.llm import get_llm

llm = get_llm()


def _llm_text(system: str, prompt: str) -> str:
    """Generate a complete, non-streaming response."""
    response = llm.invoke(
        [
            SystemMessage(content=system),
            HumanMessage(content=prompt),
        ]
    )
    return response.content


def _llm_stream(system: str, prompt: str) -> Iterator[str]:
    """Yield text chunks as the model generates them."""
    messages = [
        SystemMessage(content=system),
        HumanMessage(content=prompt),
    ]

    for chunk in llm.stream(messages):
        content = getattr(chunk, "content", "")

        if isinstance(content, str):
            if content:
                yield content
        elif isinstance(content, list):
            # Handle models that return structured content blocks.
            for block in content:
                if isinstance(block, dict) and block.get("type") == "text":
                    text = block.get("text", "")
                    if text:
                        yield text


def _json_from_llm(text: str) -> dict:
    """Extract the first JSON object from an LLM response."""
    start = text.index("{")
    end = text.rindex("}") + 1
    return json.loads(text[start:end])

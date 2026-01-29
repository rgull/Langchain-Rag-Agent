from langchain.agents.middleware import SummarizationMiddleware

from models.llm import get_llm

def get_summarization_middleware():
    return SummarizationMiddleware(
        get_llm(),
        trigger=("messages",10),
        keep=("messages",3)
    )
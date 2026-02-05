from langchain.agents import create_agent
from langgraph.checkpoint.memory import InMemorySaver

from models.llm import get_llm

from tools.weather_tool import weather_tool
from tools.email_tool import send_email_tool, read_email_tool
from tools.mcp_tools import get_mcp_tools

# from tools import weather_tool, send_email_tool, read_email_tool, get_mcp_tools



from prompts.system_prompt import SYSTEM_PROMPT
from middlewares.summarization_middleware import get_summarization_middleware
from middlewares.human_in_the_loop_middleware import get_human_in_the_loop_middleware
from memory.sqlite_saver import get_sqlite_saver

async def build_agent():
    mcp_tools = await get_mcp_tools()
    
    return create_agent(
        model = get_llm(),
        tools = [send_email_tool, read_email_tool] + mcp_tools,
        system_prompt = SYSTEM_PROMPT,
        # checkpointer=get_sqlite_saver(),
        middleware=[
            get_summarization_middleware(),
            get_human_in_the_loop_middleware(),
        ]
    )


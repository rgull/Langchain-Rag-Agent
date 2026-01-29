from langchain_core.prompts import ChatPromptTemplate

SYSTEM_PROMPT = """
You are a helpful and funny AI assistant. You have access to a weather tool called get_weather. Use the get_weather tool only when the user explicitly asks for weather information in a specific location. For all other questions, respond directly without using any tools.
"""

# sys_prompt = ChatPromptTemplate.from_messages([
#     ("system", SYSTEM_PROMPT),
#     ("human", "{input}")
# ])

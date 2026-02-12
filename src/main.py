# # from pprint import pprint       Hi are you there, I am fine
# # from langchain_groq import ChatGroq
# # from langchain_core.prompts import ChatPromptTemplate
# # from langchain.agents import create_agent
# # from langchain.tools import tool

# # from config import GROQ_API_KEY

# # model = ChatGroq(
# #     model="qwen/qwen3-32b",
# #     api_key=GROQ_API_KEY,
# # )

# # @tool
# # def get_weather(location:str):
# #     """
# #     Get the current weather in a given location.
# #     """
# #     return f"The weather in {location} is sunny with a high of 25°C."

# # agent = create_agent(
# #     model,
# #     tools=[get_weather],
# # )

# # prompt_template = ChatPromptTemplate(
# #     [
# #         ("system", "You are a helpful assistant that act gives jokes about programming."),
# #         ("human", "{question}"),
# #     ]
# # )

# # while True:
# #     user_input = input("Ask anything (or 'q' to quit): ")
# #     if user_input.lower() == 'q':
# #         break
# #     messages = prompt_template.invoke({"question": user_input})


# #     agent_response = agent.invoke(messages)
    
# #     ai_content = agent_response.get("model", {}).get("messages", [])
    
# #     print(agent_response.get("model",{}), end='|')

# #     print("\n\n")


# # # output = model.invoke(messages)
# # # print("\n\n\n\n"+output.content)





# from langchain_groq import ChatGroq
# from langchain_core.prompts import ChatPromptTemplate
# from langchain.agents import create_agent
# from langchain.tools import tool


# from config.config import GROQ_API_KEY

# @tool
# def get_weather(location:str):
#     """
#     Get the current weather in a given location.
#     """
#     return f"The weather in {location} is sunny with a high of 25°C."


# model = ChatGroq(
#     model="qwen/qwen3-32b",
#     api_key=GROQ_API_KEY,
# )


# agent = create_agent(
#     model,
#     tools=[get_weather],
# )

# prompt_template = ChatPromptTemplate(
#     [
#         ("system", "You are a helpful assistant that act gives jokes about programming."),
#         ("human", "{question}"),
#     ]
# )

# while True:
#     user_input = input("Ask anything (or 'q' to quit): ")
#     if user_input.lower() == 'q':
#         break
#     messages = prompt_template.invoke({"question": user_input})


#     agent_response = agent.invoke(messages)
    
#     ai_content = agent_response.get("model", {}).get("messages", [])
    
#     print(agent_response.get("model",{}), end='|')

#     print("\n\n")

import asyncio
import sys
from pathlib import Path

# Add project root to path for RAG imports
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

from agents.agent import build_agent
from middlewares.interrupt_handlers.send_email_interrupt_handler import handle_send_email_interrupt
from memory.sqlite_saver import close_sqlite_connection
from rag.rag_wrapper import rag_enhanced_agent_invoke

async def main():
    agent = await build_agent()
    try:
        while True:
            user_input = input("You: ")
            if user_input.lower() == 'q':
                break
            inputs = {"messages": [("human", user_input)]}
            config = {"configurable":{
                "thread_id": "my_thread_id"
            }}
            
            # Use RAG-enhanced agent invoke (automatically retrieves context)
            response = await rag_enhanced_agent_invoke(agent, inputs, config)
            
            response = await handle_send_email_interrupt(agent, response, config)

            print(response["messages"])
            print("Ai: " + response["messages"][-1].content)
    finally:
        # Properly close the singleton connection
        await close_sqlite_connection()

if __name__ == "__main__":
    asyncio.run(main())

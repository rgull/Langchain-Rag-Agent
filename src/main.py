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
from langgraph.types import Command

from agents.agent import build_agent
from middlewares.interrupt_handlers.send_email_interrupt_handler import handle_send_email_interrupt

async def main():
    agent = await build_agent()
    while True:
        user_input = input("You: ")
        if user_input.lower() == 'q':
            break
        inputs = {"messages": [("human", user_input)]}
        config = {"configurable":{
            "thread_id": "my_thread_id"
        }}
        response = await agent.ainvoke(inputs, config)
        
        response = await handle_send_email_interrupt(agent, response, config)

        print(response["messages"])
        print("Ai: " + response["messages"][-1].content)

    agent.checkpointer.conn.close()

if __name__ == "__main__":
    asyncio.run(main())

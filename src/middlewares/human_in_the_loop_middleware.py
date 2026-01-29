from langchain.agents.middleware import HumanInTheLoopMiddleware

from tools.email_tool import send_email_tool

def get_human_in_the_loop_middleware():
    return HumanInTheLoopMiddleware(
        interrupt_on = {
            "send_email_tool": {
                "allowed_decisions": ["approve", "edit", "reject"],
            }
        }
    )
from typing import Any
from langgraph.types import Command

def handle_send_email_interrupt(agent, response, config) -> dict[str, Any] | Any:
    if "__interrupt__" in response:
        print("Process was interrupted. Action required")

        while True:
            user_choice = input(
                "Approve or reject?: "
            ).strip().lower()
            
            if user_choice in {"approve", "reject"}:
                print(f"You chose to {user_choice}")
                break
            else:
                print("Invalid choice. Please type 'approve', 'reject'")

        response = agent.invoke(
            Command(
                resume={
                    "decisions": [
                        {
                            "type": user_choice
                        }
                    ]
                }
            ),
            config
        )

    return response

from state.state import ReviewState
from config.config import client

def style_node(state: ReviewState) -> ReviewState:
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": "You are a code quality expert. Review code only for style issues like naming conventions, missing docstrings, dead code, and readability."
            },
            {
                "role": "user",
                "content": f"Review this code for style issues only:\n```\n{state['code']}\n```"
            }
        ]
    )
    return {"style_review": response.choices[0].message.content}

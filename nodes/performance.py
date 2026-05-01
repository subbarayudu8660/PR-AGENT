from state.state import ReviewState
from config.config import client

def performance_node(state: ReviewState) -> ReviewState:
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": "You are a performance expert. Review code only for performance issues like slow algorithms, unnecessary loops, missing indexes, and memory leaks."
            },
            {
                "role": "user",
                "content": f"Review this code for performance issues only:\n```\n{state['code']}\n```"
            }
        ]
    )
    return {"performance_review": response.choices[0].message.content}
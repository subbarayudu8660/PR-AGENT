from state.state import ReviewState
from config.config import client

def security_node(state: ReviewState) -> ReviewState:
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": "You are a security expert. Review code only for security vulnerabilities like SQL injection, hardcoded secrets, missing auth, and data exposure."
            },
            {
                "role": "user",
                "content": f"Review this code for security issues only:\n```\n{state['code']}\n```"
            }
        ]
    )
    return {"security_review": response.choices[0].message.content}
from state.state import ReviewState
from config.config import client

def aggregator_node(state: ReviewState) -> ReviewState:
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": "You are a code review aggregator. Merge multiple reviews into one clean list. Remove duplicates. Keep every unique issue."
            },
            {
                "role": "user",
                "content": f"""Merge these three reviews into one clean list of unique issues:

SECURITY REVIEW:
{state['security_review']}

PERFORMANCE REVIEW:
{state['performance_review']}

STYLE REVIEW:
{state['style_review']}"""
            }
        ]
    )
    return {"aggregated_review": response.choices[0].message.content}
from state.state import ReviewState
from config.config import client

def ranker_node(state: ReviewState) -> ReviewState:
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": "You are a code review prioritizer. Label every issue as CRITICAL, WARNING, or SUGGESTION. Order them most severe first."
            },
            {
                "role": "user",
                "content": f"Prioritize these issues:\n\n{state['aggregated_review']}"
            }
        ]
    )
    return {"final_review": response.choices[0].message.content}
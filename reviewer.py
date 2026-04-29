from openai import OpenAI
from dotenv import load_dotenv
from langgraph.graph import StateGraph , END , START
from typing import TypedDict
import os

load_dotenv()

client = OpenAI(api_key =  os.getenv("OPENAI_API_KEY"))

class ReviewState(TypedDict):
    code: str
    security_review: str
    performance_review: str
    style_review: str
    aggregated_review : str
    final_review: str

def security_node(state: ReviewState) -> ReviewState:
    response = client.chat.completions.create(
        model = "gpt-4o",
        messages = [
            {
                "role": "system",
                "content": "You are a Security expert. Review code only for security vulnerabilities like SQL Injections, hardcoded secrets,missing auth , and data exposure and things of sort."
            },
            {
                "role": "user",
                "content": f"Please review the following code for security issues only:\n\n{state['code']}"
            }
        ]
    )
    return {"security_review": response.choices[0].message.content}

def performance_node(state: ReviewState) -> ReviewState:
    response = client.chat.completions.create(
        model = "gpt-4o",
        messages = [
            {
                "role": "system",
                "content": "You are a Performance expert. Review code only for performance issues like inefficient algorithms, unnecessary computations, and resource usage."
            },
            {
                "role": "user",
                "content": f"Please review the following code for performance issues only:\n\n{state['code']}"
            }
        ]
    )
    return {"performance_review": response.choices[0].message.content}

def style_node(state: ReviewState) -> ReviewState:
    response = client.chat.completions.create(
        model = "gpt-4o",
        messages = [
            {
                "role": "system",
                "content": "You are a code quality expert. Review code only for style issues like naming conventions, code structure, and readability."
            },
            {
                "role": "user",
                "content": f"Please review the following code for style issues only:\n\n{state['code']}"
            }
        ]
    )
    return {"style_review": response.choices[0].message.content}

def aggregater_node(state: ReviewState) -> ReviewState:
    response = client.chat.completions.create(
        model = "gpt-4o",
        messages = [
            {
                "role": "system",
                "content": "You are a code review aggregator. Combine all reviews into a single, comprehensive review list. Keep every unique isssue"
            },
            {
                "role": "user",
                "content": f"""Merge these three reviews into one clean list of unique issues:
                SECURITY REVIEW: {state['security_review']},
                PERFORMANCE REVIEW: {state['performance_review']},
                STYLE REVIEW: {state['style_review']}
                 """
            }
        ]
    )
    return {"aggregated_review": response.choices[0].message.content}

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
                "content": f"""Prioritize these issues:

{state['aggregated_review']}"""
            }
        ]
    )
    return {"final_review": response.choices[0].message.content}


graph = StateGraph(ReviewState)

graph.add_node("security_reviewer", security_node)
graph.add_node("performance_reviewer", performance_node)
graph.add_node("style_reviewer", style_node)
graph.add_node("aggregator", aggregater_node)
graph.add_node("ranker", ranker_node)


graph.add_edge(START, "security_reviewer")
graph.add_edge(START, "performance_reviewer")
graph.add_edge(START, "style_reviewer")
graph.add_edge("security_reviewer", "aggregator")
graph.add_edge("performance_reviewer", "aggregator")
graph.add_edge("style_reviewer", "aggregator")
graph.add_edge("aggregator", "ranker")
graph.add_edge("ranker", END)

app = graph.compile()

result = app.invoke({"code": """
def get_user(user_id):
    query = "SELECT * FROM users WHERE id = " + user_id
    result = db.execute(query)
    password = result['password']
    return result
"""})

print("=== FINAL REVIEW ===")
print(result['final_review'])
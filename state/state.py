from typing import TypedDict

class ReviewState(TypedDict):
    code: str
    security_review: str
    performance_review: str
    style_review: str
    aggregated_review: str
    final_review: str
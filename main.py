from dotenv import load_dotenv
from graph.graph import build_graph
from github_utils import fetch_pr_diff, post_github_comment

load_dotenv()

pr_url = "https://github.com/subbarayudu8660/test-pr-agent/pull/1"

print("Fetching PR diff...")
code = fetch_pr_diff(pr_url)

print("Running review agents...")
app = build_graph()
result = app.invoke({"code": code})

print("Posting comment to GitHub...")
post_github_comment(pr_url, result['final_review'])

print("\n=== FINAL REVIEW ===")
print(result['final_review'])
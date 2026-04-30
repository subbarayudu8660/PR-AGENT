from github import Github
import os

def fetch_pr_diff(pr_url: str)-> str:
    g = Github(os.getenv("GITHUB_TOKEN"))
    
    parts = pr_url.strip("/").split("/")
    owner = parts[-4]
    repo_name = parts[-3]
    pr_number = int(parts[-1])

    repo = g.get_repo(f"{owner}/{repo_name}")
    pr = repo.get_pull(pr_number)

    diff = ""

    for file in pr.get_files():
        diff += f"\nFile: {file.filename}\n"
        diff += f"{file.patch}\n"
    
    return diff

def post_github_comment(pr_url: str, comment: str):
    g = Github(os.getenv("GITHUB_TOKEN"))
    
    parts = pr_url.strip("/").split("/")
    owner = parts[-4]
    repo_name = parts[-3]
    pr_number = int(parts[-1])
    
    repo = g.get_repo(f"{owner}/{repo_name}")
    pr = repo.get_pull(pr_number)
    pr.create_issue_comment(comment)
    print("Comment posted to PR successfully")
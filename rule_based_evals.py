import re

def eval_dash_count(post: str, max_allowed=3) -> dict:
    # Count only standalone hyphens not at start of line (avoid list bullets)
    matches = re.findall(r'(?<!^)\s-\s', post)
    dash_count = len(matches)
    return {
        "passed": dash_count <= max_allowed,
        "dash_count": dash_count,
        "max_allowed": max_allowed
    }
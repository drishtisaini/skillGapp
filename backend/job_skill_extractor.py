import json
from collections import Counter
from pathlib import Path

DATA_FILE = Path("data/job_postings.json")

def load_job_postings(path=DATA_FILE):
    """Load job postings from JSON file"""
    if not Path(path).exists():
        raise FileNotFoundError(f"Job postings file not found: {path}")
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def extract_market_skills(postings):
    """Extract all skills from postings and return frequency counts"""
    all_skills = []
    for job in postings:
        all_skills.extend(job.get("skills_required", []))
    return dict(Counter(all_skills))

if __name__ == "__main__":
    postings = load_job_postings()
    market_skills = extract_market_skills(postings)
    print("Top Market Skills:", sorted(market_skills.items(), key=lambda x: -x[1]))

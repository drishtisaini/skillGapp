from resume_reader import read_resume
from skill_extractor import extract_skills
from job_skill_extractor import load_job_postings, extract_market_skills
import json
from roadmap_generator import generate_roadmap


def analyze_user_against_market(resume_path, role=None):
    # Step 1: extract user skills
    text = read_resume(resume_path)
    user_skills = [s for s, c in extract_skills(text) if c >= 0.9]

    # Step 2: load job postings
    postings = load_job_postings()

    if role and role.lower() != "all":
        # Filter postings for that role only
        postings = [p for p in postings if p["role"].lower() == role.lower()]
        if not postings:
            print(f"⚠️ No postings found for role: {role}")
            return
        print(f"Analyzing against role: {role}")
    else:
        print("Analyzing against ALL job postings (market-wide)")

    # Step 3: extract market skills
    market_skills = extract_market_skills(postings)

    # Step 4: find skill gap
    gap = list(set(market_skills.keys()) - set(user_skills))

    result = {
        "user_skills": user_skills,
        "market_top_skills": sorted(market_skills.items(), key=lambda x: -x[1]),
        "skill_gap": gap
    }

    with open("outputs/market_gap.json", "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2)

    print("✅ Analysis complete → outputs/market_gap.json")

    # Step 5: generate learning roadmap from the gaps
    if gap:
        generate_roadmap(gap)
    else:
        print("🎉 No skill gaps found! You match the market perfectly.")


if __name__ == "__main__":
    # --- CHANGE resume filename here ---
    resume_file = "resume.pdf"

    # Ask user for role
    role = input("Enter job role (or type 'all' for market-wide analysis): ").strip()
    analyze_user_against_market(resume_file, role)

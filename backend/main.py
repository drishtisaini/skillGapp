import json
from pathlib import Path
from resume_reader import read_resume
from skill_extractor import extract_skills

def build_user_profile(resume_path: str, OUTPUT_DIR="outputs") -> str:
    text = read_resume(resume_path)
    skills_conf = extract_skills(text, use_fuzzy=True)

    profile = {
        "source_file": str(Path(resume_path).name),
        "extracted_skills": [
            {"skill": s, "confidence": round(c, 2)} for s, c in skills_conf
        ],
        "top_skills": [s for s, c in skills_conf if c >= 0.9]
    }

    Path(OUTPUT_DIR).mkdir(parents=True, exist_ok=True)
    out_path = Path(OUTPUT_DIR) / "user_profile.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(profile, f, indent=2, ensure_ascii=False)

    print(f"Saved → {out_path}")
    return str(out_path)

if __name__ == "__main__":
    # put your resume file in the backend folder or give full path
    build_user_profile("resume.pdf")

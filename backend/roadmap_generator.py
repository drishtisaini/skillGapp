import json
from pathlib import Path

OUTPUT_FILE = Path("outputs/roadmap.json")

# Predefined resource map (can be expanded later)
LEARNING_RESOURCES = {
    "Python": [
        {"title": "Python for Everybody (Coursera)", "link": "https://www.coursera.org/specializations/python"},
        {"title": "Automate the Boring Stuff (Free)", "link": "https://automatetheboringstuff.com/"}
    ],
    "SQL": [
        {"title": "SQL Tutorial (W3Schools)", "link": "https://www.w3schools.com/sql/"},
        {"title": "SQL for Data Science (Coursera)", "link": "https://www.coursera.org/learn/sql-for-data-science"}
    ],
    "Machine Learning": [
        {"title": "Machine Learning (Andrew Ng)", "link": "https://www.coursera.org/learn/machine-learning"},
        {"title": "Hands-On Machine Learning with Scikit-Learn (Book)", "link": "https://www.oreilly.com/library/view/hands-on-machine-learning/9781492032632/"}
    ],
    "JavaScript": [
        {"title": "JavaScript Tutorial (MDN)", "link": "https://developer.mozilla.org/en-US/docs/Web/JavaScript"},
        {"title": "JavaScript Basics (freeCodeCamp)", "link": "https://www.freecodecamp.org/learn/javascript-algorithms-and-data-structures/"}
    ],
    "React": [
        {"title": "React Official Docs", "link": "https://react.dev/"},
        {"title": "React Crash Course (YouTube)", "link": "https://www.youtube.com/watch?v=w7ejDZ8SWv8"}
    ]
    # Add more mappings as needed
}

def generate_roadmap(skill_gap):
    """Generate a personalized learning roadmap from skill gaps"""
    roadmap = {}

    for skill in skill_gap:
        if skill in LEARNING_RESOURCES:
            roadmap[skill] = LEARNING_RESOURCES[skill]
        else:
            roadmap[skill] = [
                {"title": f"Learn {skill} - Google Search", "link": f"https://www.google.com/search?q=learn+{skill}"}
            ]

    # Save roadmap as JSON
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(roadmap, f, indent=2)

    print(f"✅ Roadmap generated → {OUTPUT_FILE}")
    return roadmap

if __name__ == "__main__":
    # For quick test: mock gap
    mock_gap = ["Python", "SQL", "React", "Docker"]
    generate_roadmap(mock_gap)
   

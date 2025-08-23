import json
import streamlit as st

def load_data():
    with open("data/users.json") as f:
        users = json.load(f)
    with open("data/mentors.json") as f:
        mentors = json.load(f)
    return users, mentors

def match_mentors(user, mentors):
    matches = []
    for mentor in mentors:
        common_skills = set(user["skill_gaps"]).intersection(set(mentor["skills"]))
        if common_skills:
            matches.append({
                "name": mentor["name"],
                "skills_to_learn": list(common_skills),
                "experience": mentor["experience"],
                "availability": mentor["availability"]
            })
    return sorted(matches, key=lambda x: x['experience'], reverse=True)

def mentor_matching_screen():
    st.title("🤝 Mentor Matching")

    users, mentors = load_data()
    user = users[0]  # pick first user for demo

    st.subheader(f"Welcome {user['name']} 👋")
    st.write("Your skill gaps:", ", ".join(user["skill_gaps"]))

    matches = match_mentors(user, mentors)

    if not matches:
        st.warning("No mentors found for your skill gaps.")
    else:
        for m in matches:
            with st.container():
                st.write(f"### {m['name']}")
                st.write(f"✅ Can help you with: {', '.join(m['skills_to_learn'])}")
                st.write(f"📅 Availability: {m['availability']}")
                st.write(f"⭐ Experience: {m['experience']} years")
                st.button(f"Request Mentorship from {m['name']}")

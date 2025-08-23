import streamlit as st
from org_dashboard import org_dashboard_screen      # ✅ Org Dashboard
from admin_panel import admin_panel_screen          # ✅ Admin Panel
from certificate_center import certificate_center_screen   # ✅ Certificate Center
from progress_tracker import progress_tracker_screen       # ✅ Progress Tracker

# ---------------- Sidebar ----------------
st.sidebar.title("📌 SkillVision Pro")
page = st.sidebar.radio(
    "Navigate",
    [
        "🏠 Dashboard",
        "🤝 Mentor Matching",
        "📊 Org Dashboard",
        "🛠️ Admin Panel",
        "🏆 Certificates",
        "🎯 Progress Tracker"
    ]
)

# ---------------- Dashboard ----------------
if page == "🏠 Dashboard":
    st.title("📊 SkillVision Dashboard")
    st.write("👋 Welcome to **SkillVision Pro!**")
    st.markdown("---")
    st.subheader("✨ Features Available:")
    st.markdown("""
    - 🔍 **Skill Gap Analysis** (coming soon)
    - 🛣️ **Smart Roadmap Generator** (planned)
    - 🎯 **Mentor Matching** (working now!)
    - 🏆 **Gamified Progress Tracker** (working now!)
    - 📊 **Organizational Dashboard** (working now!)
    - 🛠️ **Admin Panel** (working now!)
    - 🏆 **Certificate Center** (working now!)
    """)

# ---------------- Mentor Matching ----------------
elif page == "🤝 Mentor Matching":
    st.title("🤝 Mentor Matching")
    st.markdown("Find the **best mentor** to help you close your skill gaps 🚀")
    st.markdown("---")

    # Example mentors
    mentors = [
        {"name": "Dr. Neha", "skills": ["Python", "SQL", "Docker"], "experience": 5, "availability": "2h/week"},
        {"name": "Rohit", "skills": ["Power BI", "Excel"], "experience": 3, "availability": "1h/week"},
        {"name": "Sneha", "skills": ["Java", "Spring Boot", "AWS"], "experience": 7, "availability": "3h/week"},
        {"name": "Arjun", "skills": ["Data Science", "Pandas", "ML"], "experience": 4, "availability": "1.5h/week"},
        {"name": "Meera", "skills": ["Python", "SQL", "Machine Learning"], "experience": 6, "availability": "2h/week"}
    ]

    # 🔎 Search/Filter mentors by skill
    all_skills = sorted(set(skill for m in mentors for skill in m["skills"]))
    search_skill = st.selectbox("Filter mentors by skill", ["All"] + all_skills)

    if search_skill != "All":
        filtered_mentors = [m for m in mentors if search_skill in m["skills"]]
    else:
        filtered_mentors = mentors

    # Show results
    if filtered_mentors:
        st.subheader("Available Mentors")
        cols = st.columns(2)   # 2 mentors per row
        for i, m in enumerate(filtered_mentors):
            with cols[i % 2]:
                st.markdown("### 👨‍🏫 " + m["name"])
                st.markdown(f"**💡 Skills:** {', '.join(m['skills'])}")
                st.markdown(f"**⭐ Experience:** {m['experience']} years")
                st.markdown(f"**📅 Availability:** {m['availability']}")
                st.button(f"Request Mentorship from {m['name']}", key=m["name"])
                st.markdown("---")
    else:
        st.warning(f"No mentors found with skill: {search_skill}")

# ---------------- Org Dashboard ----------------
elif page == "📊 Org Dashboard":
    org_dashboard_screen()

# ---------------- Admin Panel ----------------
elif page == "🛠️ Admin Panel":
    admin_panel_screen()

# ---------------- Certificates ----------------
elif page == "🏆 Certificates":
    certificate_center_screen()

# ---------------- Progress Tracker ----------------
elif page == "🎯 Progress Tracker":
    progress_tracker_screen()

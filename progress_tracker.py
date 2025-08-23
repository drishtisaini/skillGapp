import json
import os
import streamlit as st

DATA_FILE = "data/progress.json"

# --- Helpers ---
def load_progress():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE) as f:
        return json.load(f)

def save_progress(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

def get_level(progress):
    if progress < 40:
        return "🔰 Beginner"
    elif progress < 80:
        return "🚀 Intermediate"
    else:
        return "🌟 Advanced"

def get_badge(progress):
    if progress >= 80:
        return "🏅 Gold Badge"
    elif progress >= 50:
        return "🎖️ Silver Badge"
    return "🔓 No Badge Yet"

def progress_tracker_screen():
    st.title("🎯 Gamified Progress Tracker")
    st.markdown("Track your learning journey with levels and badges 🏆")
    st.markdown("---")

    progress = load_progress()

    # --- Show Progress for All Users ---
    st.subheader("👥 Learner Progress")
    for i, p in enumerate(progress):
        st.markdown(f"### 👤 {p['name']} ({p['user_id']})")
        st.progress(p["progress"] / 100)
        st.write(f"**Level:** {get_level(p['progress'])}")
        st.write(f"**Badge:** {get_badge(p['progress'])}")
        st.markdown("---")

    # --- Update Progress Form ---
    st.subheader("✏️ Update Progress")
    user_id = st.text_input("Enter User ID")
    new_progress = st.slider("Progress (%)", 0, 100, 0)

    if st.button("Update Progress"):
        user_entry = next((u for u in progress if u["user_id"] == user_id), None)
        if user_entry:
            user_entry["progress"] = new_progress
        else:
            name = st.text_input("Enter Name (for new user)")
            if name:
                progress.append({"user_id": user_id, "name": name, "progress": new_progress})
        save_progress(progress)
        st.success("✅ Progress updated!")
        st.experimental_rerun()

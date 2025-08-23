import json
import streamlit as st

# --- Load and Save helpers ---
def load_users():
    with open("data/users.json") as f:
        return json.load(f)

def save_users(users):
    with open("data/users.json", "w") as f:
        json.dump(users, f, indent=4)

def admin_panel_screen():
    st.title("🛠️ Admin Panel - User Management")
    st.markdown("Manage employees, add, edit, or delete users 👨‍💼")
    st.markdown("---")

    users = load_users()

    # --- Show Users with Delete & Edit ---
    st.subheader("👥 Current Users")
    for i, u in enumerate(users):
        col1, col2, col3 = st.columns([3,1,1])
        with col1:
            st.write(f"**{u['name']}** | Role: {u['role']} | Skills: {', '.join(u['skills'])}")
        with col2:
            if st.button("✏️ Edit", key=f"edit_{i}"):
                st.session_state.edit_index = i
        with col3:
            if st.button("❌ Delete", key=f"del_{i}"):
                users.pop(i)
                save_users(users)
                st.success(f"✅ User {u['name']} deleted!")
                st.experimental_rerun()

    st.markdown("---")

    # --- Edit User Form (if clicked) ---
    if "edit_index" in st.session_state:
        idx = st.session_state.edit_index
        user = users[idx]

        st.subheader(f"✏️ Edit User: {user['name']}")
        new_name = st.text_input("Name", value=user["name"], key="edit_name")
        new_role = st.selectbox("Role", ["Learner", "Mentor"], 
                                index=0 if user["role"]=="Learner" else 1,
                                key="edit_role")
        new_skills = st.text_input("Skills (comma separated)", 
                                   value=", ".join(user["skills"]), 
                                   key="edit_skills")
        new_gaps = ""
        if new_role == "Learner":
            new_gaps = st.text_input("Skill Gaps (comma separated)", 
                                     value=", ".join(user["skill_gaps"]), 
                                     key="edit_gaps")

        if st.button("💾 Save Changes", key="save_changes"):
            users[idx]["name"] = new_name
            users[idx]["role"] = new_role
            users[idx]["skills"] = [s.strip() for s in new_skills.split(",") if s.strip()]
            if new_role == "Learner":
                users[idx]["skill_gaps"] = [s.strip() for s in new_gaps.split(",") if s.strip()]
            else:
                users[idx]["skill_gaps"] = []

            save_users(users)
            st.success(f"✅ User {new_name} updated successfully!")
            del st.session_state.edit_index
            st.experimental_rerun()

    # --- Add New User Form ---
    st.subheader("➕ Add New User")
    name = st.text_input("Name", key="add_name")
    role = st.selectbox("Role", ["Learner", "Mentor"], key="add_role")
    skills = st.text_input("Skills (comma separated)", key="add_skills").split(",")
    skill_gaps = []
    if role == "Learner":
        skill_gaps = st.text_input("Skill Gaps (comma separated)", key="add_gaps").split(",")

    if st.button("➕ Add User", key="add_user_btn"):
        new_user = {
            "user_id": f"U{len(users)+1:03d}",
            "name": name,
            "skills": [s.strip() for s in skills if s.strip()],
            "skill_gaps": [s.strip() for s in skill_gaps if s.strip()],
            "role": role
        }
        users.append(new_user)
        save_users(users)
        st.success(f"✅ User {name} added successfully!")
        st.experimental_rerun()

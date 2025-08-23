import json
import os
import streamlit as st

DATA_FILE = "data/certificates.json"
CERT_FOLDER = "certs"

# --- Helpers ---
def load_certificates():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE) as f:
        return json.load(f)

def save_certificates(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

def certificate_center_screen():
    st.title("🏆 Certificate Center")
    st.markdown("Upload and download your certificates 📜")
    st.markdown("---")

    certs = load_certificates()

    # --- Upload Form ---
    st.subheader("📤 Upload Certificate")
    name = st.text_input("Your Name")
    user_id = st.text_input("User ID (e.g., U001)")
    title = st.text_input("Certificate Title")
    issuer = st.text_input("Issuer (e.g., Coursera, Udemy)")
    date = st.date_input("Completion Date")
    file_upload = st.file_uploader("Upload Certificate (PDF/PNG/JPG)", type=["pdf","png","jpg","jpeg"])

    if st.button("Upload"):
        if not os.path.exists(CERT_FOLDER):
            os.makedirs(CERT_FOLDER)

        if file_upload is not None:
            file_path = os.path.join(CERT_FOLDER, file_upload.name)
            with open(file_path, "wb") as f:
                f.write(file_upload.getbuffer())

            # Check if user already exists
            user_entry = next((c for c in certs if c["user_id"] == user_id), None)
            new_cert = {
                "title": title,
                "issuer": issuer,
                "date": str(date),
                "file": file_path
            }

            if user_entry:
                user_entry["certificates"].append(new_cert)
            else:
                certs.append({
                    "user_id": user_id,
                    "name": name,
                    "certificates": [new_cert]
                })

            save_certificates(certs)
            st.success("✅ Certificate uploaded successfully!")
            st.experimental_rerun()
        else:
            st.error("Please upload a certificate file")

    st.markdown("---")

    # --- Download Certificates ---
    st.subheader("📂 Your Certificates")
    search_user = st.text_input("Enter Your User ID to View Certificates")
    if search_user:
        user_entry = next((c for c in certs if c["user_id"] == search_user), None)
        if user_entry:
            st.markdown(f"### 👤 {user_entry['name']} ({user_entry['user_id']})")
            for i, cert in enumerate(user_entry["certificates"]):
                st.write(f"**{cert['title']}** ({cert['issuer']}, {cert['date']})")
                if os.path.exists(cert["file"]):
                    st.download_button(
                        "⬇️ Download",
                        data=open(cert["file"], "rb"),
                        file_name=os.path.basename(cert["file"]),
                        key=f"dl_{user_entry['user_id']}_{i}"
                    )
        else:
            st.warning("⚠️ No certificates found for this User ID.")

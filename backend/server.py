from flask import Flask, request, render_template
import os, json
from analyze import analyze_user_against_market   # your analysis function

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app = Flask(__name__)

@app.route("/ui", methods=["GET"])
def ui():
    return render_template("upload.html")

@app.route("/analyze", methods=["POST"])
def analyze_resume():
    if "resume" not in request.files:
        return "⚠️ No resume uploaded"

    file = request.files["resume"]
    role = request.form.get("role", "all")

    resume_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(resume_path)

    # Run your analyzer
    analyze_user_against_market(resume_path, role)

    # Load results
    with open("outputs/market_gap.json", "r", encoding="utf-8") as f:
        market_gap = json.load(f)
    with open("outputs/roadmap.json", "r", encoding="utf-8") as f:
        roadmap = json.load(f)

    return render_template(
        "results.html",
        role=role,
        filename=file.filename,
        market_gap=market_gap,
        roadmap=roadmap,
        result=market_gap            # ← add this 
    )


if __name__ == "__main__":
    app.run(debug=True)


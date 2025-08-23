import json
import os
from collections import Counter
import pandas as pd
import streamlit as st
import altair as alt

EMP_FILE = "data/employees.json"

def _safe_load_employees():
    """Load employees.json safely and normalize to a DataFrame with expected columns."""
    if not os.path.exists(EMP_FILE):
        st.warning("No data found at data/employees.json. Showing empty dashboard.")
        return pd.DataFrame(columns=["emp_id","name","department","location","skills","skill_gaps"])
    try:
        with open(EMP_FILE, "r", encoding="utf-8") as f:
            raw = json.load(f)
    except Exception as e:
        st.error(f"Failed to read employees.json: {e}")
        return pd.DataFrame(columns=["emp_id","name","department","location","skills","skill_gaps"])

    # Normalize to expected fields
    rows = []
    for r in raw:
        rows.append({
            "emp_id": r.get("emp_id", r.get("user_id", "")),
            "name": r.get("name", ""),
            "department": r.get("department", "Unknown"),
            "location": r.get("location", "Unknown"),
            "skills": r.get("skills", []),
            "skill_gaps": r.get("skill_gaps", []),
            "role": r.get("role", "Learner")
        })
    df = pd.DataFrame(rows)
    # Ensure list columns
    for c in ["skills", "skill_gaps"]:
        df[c] = df[c].apply(lambda x: x if isinstance(x, list) else ([] if pd.isna(x) else [x]))
    return df

def _top_n_counter(list_series, n=10):
    c = Counter()
    for lst in list_series:
        c.update(lst)
    return pd.DataFrame(c.most_common(n), columns=["item", "count"])

def org_dashboard_screen():
    st.title("📊 Organizational Dashboard")
    st.caption("HR/Leadership view of skills, gaps, and distribution across org.")
    st.markdown("---")

    df = _safe_load_employees()
    if df.empty:
        st.info("Add data to `data/employees.json` to see org insights.")
        return

    # ---- Filters ----
    with st.expander("🔎 Filters"):
        dept_opts = ["All"] + sorted(df["department"].dropna().unique().tolist())
        loc_opts = ["All"] + sorted(df["location"].dropna().unique().tolist())
        colf1, colf2 = st.columns(2)
        with colf1:
            sel_dept = st.selectbox("Department", dept_opts, index=0)
        with colf2:
            sel_loc = st.selectbox("Location", loc_opts, index=0)

    fdf = df.copy()
    if sel_dept != "All":
        fdf = fdf[fdf["department"] == sel_dept]
    if sel_loc != "All":
        fdf = fdf[fdf["location"] == sel_loc]

    # ---- KPIs ----
    total_employees = len(fdf)
    total_gaps = sum(len(x) for x in fdf["skill_gaps"])
    avg_gaps = (total_gaps / total_employees) if total_employees else 0
    unique_skills = len(set(s for lst in fdf["skills"] for s in lst))

    k1, k2, k3, k4 = st.columns(4)
    k1.metric("👥 Employees", total_employees)
    k2.metric("📉 Avg Skill Gaps", f"{avg_gaps:.1f}")
    k3.metric("🧰 Unique Skills", unique_skills)
    k4.metric("🏢 Departments", fdf["department"].nunique())

    st.markdown("---")

    # ---- Top Skill Gaps (Bar) ----
    st.subheader("🔥 Top Skill Gaps")
    gap_df = _top_n_counter(fdf["skill_gaps"], n=10)
    if not gap_df.empty:
        chart = (
            alt.Chart(gap_df)
            .mark_bar()
            .encode(
                x=alt.X("count:Q", title="Employees lacking this skill"),
                y=alt.Y("item:N", sort="-x", title="Skill"),
                tooltip=["item", "count"]
            )
            .properties(height=320)
        )
        st.altair_chart(chart, use_container_width=True)
    else:
        st.info("No skill gaps found in filtered data.")

    # ---- Department Distribution (Donut) ----
    st.subheader("🏢 Department Distribution")
    dept_df = fdf.groupby("department").size().reset_index(name="count")
    if not dept_df.empty:
        dept_chart = (
            alt.Chart(dept_df)
            .mark_arc(innerRadius=60)
            .encode(
                theta="count:Q",
                color=alt.Color("department:N", legend=alt.Legend(title="Department")),
                tooltip=["department", "count"]
            )
            .properties(height=300)
        )
        st.altair_chart(dept_chart, use_container_width=True)
    else:
        st.info("No department distribution to show.")

    st.markdown("---")

    # ---- Employees Table + Download ----
    st.subheader("📄 Employees (Filtered)")
    show = fdf.copy()
    show["skills"] = show["skills"].apply(lambda x: ", ".join(x))
    show["skill_gaps"] = show["skill_gaps"].apply(lambda x: ", ".join(x))
    st.dataframe(show, use_container_width=True)

    csv_bytes = show.to_csv(index=False).encode("utf-8")
    st.download_button(
        "📥 Download Employee Data (CSV)",
        data=csv_bytes,
        file_name="employee_report.csv",
        mime="text/csv",
        use_container_width=True
    )

    st.caption("Tip: refine filters above and download tailored reports per department/location.")

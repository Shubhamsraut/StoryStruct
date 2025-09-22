# sections/ui_components.py
import streamlit as st
import pandas as pd
import io, html, uuid
from parsing_helpers import extract_user_stories_and_acs

# ------------------------------
# STYLING
# ------------------------------
def inject_styles():
    """Inject custom CSS for metrics, pills, buttons, and section headers."""
    st.markdown("""
    <style>
    /* ====== Section Titles ====== */
    .section-title {
        background: #f4f8ff;
        padding: 10px 16px;
        border-left: 5px solid #1f77b4;
        border-radius: 6px;
        font-size: 18px;
        font-weight: 600;
        color: #1f77b4;
        margin-top: 10px;
        margin-bottom: 14px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.04);
    }
    .sub-heading {
        font-size: 15px;
        font-weight: 600;
        margin: 8px 0 4px 0;
        color: #444;
    }
    /* ====== File Pills ====== */
    .pillbar {
        display: flex;
        flex-wrap: wrap;
        gap: 8px;
        margin-bottom: 12px;
    }
    .pill {
        display: inline-flex;
        align-items: center;
        background: #eef4fc;
        padding: 6px 10px;
        border-radius: 18px;
        font-size: 14px;
        color: #333;
        box-shadow: 0 1px 2px rgba(0,0,0,0.08);
    }
    /* ====== Metric Cards ====== */
    .metric-card {
        background: #fff;
        padding: 14px;
        border-radius: 10px;
        text-align: center;
        box-shadow: 0 2px 6px rgba(0,0,0,0.05);
        margin-bottom: 10px;
    }
    .metric-label { font-size: 13px; color: #777; }
    .metric-value { font-size: 20px; font-weight: 700; color: #1f77b4; }
    /* ====== Tabs ====== */
    .stTabs [data-baseweb="tab-list"] { gap: 12px; }
    .stTabs [data-baseweb="tab"] {
        background: #f5f7fa;
        padding: 6px 14px;
        border-radius: 6px 6px 0 0;
        font-weight: 500;
        color: #555;
        border: 1px solid #e2e6ea;
    }
    .stTabs [aria-selected="true"] {
        background: #fff;
        color: #1f77b4;
        border-bottom: 2px solid #1f77b4;
        box-shadow: 0 -2px 4px rgba(0,0,0,0.05);
    }
    </style>
    """, unsafe_allow_html=True)

def inject_styles():
    st.markdown("""
    <style>
    /* ===== Enhanced Metric Cards ===== */
    .metric-card {
        background: linear-gradient(145deg, #ffffff, #f3f7fc);
        padding: 16px;
        border-radius: 12px;
        text-align: center;
        box-shadow: 0 4px 10px rgba(0,0,0,0.08), 0 1px 3px rgba(0,0,0,0.06);
        transition: all 0.3s ease-in-out;
        border: 1px solid #e4e9f2;
        margin-bottom: 12px;
    }
    .metric-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 6px 15px rgba(0,0,0,0.12), 0 2px 5px rgba(0,0,0,0.08);
    }
    .metric-label {
        font-size: 13px;
        font-weight: 600;
        color: #6b7280;
        margin-bottom: 4px;
        letter-spacing: 0.5px;
    }
    .metric-value {
        font-size: 22px;
        font-weight: 800;
        color: #1f77b4;
        text-shadow: 1px 1px 3px rgba(31,119,180,0.15);
    }
    /* Optional: Add spacing between summary blocks */
    .sub-heading {
        font-weight: 600;
        font-size: 15px;
        color: #444;
        margin-top: 10px;
        margin-bottom: 6px;
    }
    </style>
    """, unsafe_allow_html=True)

# ------------------------------
# MAIN PAGE RENDERER
# ------------------------------
def render_home():
    """Main UI for uploading files, viewing metrics, filtering, and exporting."""
    inject_styles()

    # Reduce Streamlit default top padding/margin
    st.markdown("""
    <style>
    .block-container { padding-top: 0.8rem; }
    .css-18e3th9 { padding-top: 0.5rem !important; }
    </style>
    """, unsafe_allow_html=True)

    st.title("📄 StoryStruct")

    # Initialize session state
    if "step" not in st.session_state:
        st.session_state.step = 1
    if "uploaded_files" not in st.session_state:
        st.session_state.uploaded_files = []

    # ---------------------------
    # STEP 1: FILE UPLOAD
    # ---------------------------
    if st.session_state.step == 1:
        st.markdown("<div class='section-title'>📂 Step 1: Upload Document(s)</div>", unsafe_allow_html=True)
        uploads = st.file_uploader("Upload Word Document(s)", type=["docx"], accept_multiple_files=True)

        if uploads:
            existing = {f["name"] for f in st.session_state.uploaded_files}
            for f in uploads:
                if f.name not in existing:
                    st.session_state.uploaded_files.append({"id": uuid.uuid4().hex[:8], "name": f.name, "file": f})

        if st.session_state.uploaded_files:
            st.markdown("<div class='sub-heading'>📁 Ready to Process</div>", unsafe_allow_html=True)
            st.markdown("<div class='pillbar'>", unsafe_allow_html=True)
            for f in st.session_state.uploaded_files:
                st.markdown(f"<div class='pill'>{html.escape(f['name'])}</div>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

            if st.button("➡️ Next: View Extracted Data", use_container_width=True, key="next_step"):
                st.session_state.step = 2
                st.rerun()
        else:
            st.info("No files selected yet.")
        return

    # ---------------------------
    # STEP 2: RESULTS & ANALYSIS
    # ---------------------------
    st.markdown("<div class='section-title'>📊 Step 2: Results & Analysis</div>", unsafe_allow_html=True)

    # File chips with remove buttons
    clicked_remove = None
    if st.session_state.uploaded_files:
        st.markdown("<div class='sub-heading'>📁 Uploaded Files</div>", unsafe_allow_html=True)
        cols = st.columns(len(st.session_state.uploaded_files))
        for i, f in enumerate(st.session_state.uploaded_files):
            with cols[i]:
                c1, c2 = st.columns([5, 1])
                with c1:
                    st.markdown(f"<div class='pill'>{html.escape(f['name'])}</div>", unsafe_allow_html=True)
                with c2:
                    if st.button("❌", key=f"rm_{f['id']}", help=f"Remove {f['name']}"):
                        clicked_remove = i
    if clicked_remove is not None:
        st.session_state.uploaded_files.pop(clicked_remove)
        st.rerun()

    # Parse uploaded files
    all_stories, all_acs = [], []
    for f in st.session_state.uploaded_files:
        s_df, ac_df = extract_user_stories_and_acs(f["file"])
        if not s_df.empty: s_df["Source File"] = f["name"]
        if not ac_df.empty: ac_df["Source File"] = f["name"]
        all_stories.append(s_df)
        all_acs.append(ac_df)

    stories_df = pd.concat(all_stories, ignore_index=True) if any(not s.empty for s in all_stories) else \
        pd.DataFrame(columns=["Module","Epic","Story ID","Story Title","Acceptance Criteria Count","Source File"])
    ac_df = pd.concat(all_acs, ignore_index=True) if any(not a.empty for a in all_acs) else \
        pd.DataFrame(columns=["Module","Epic","Story ID","Story Title","AC #","Scenario","Source File"])

    if stories_df.empty and ac_df.empty:
        st.warning("⚠️ No user stories or acceptance criteria found.")
        return

    # ---------------------------
    # Overall metrics
    # ---------------------------
    st.markdown("<div class='sub-heading'>📊 Overall Summary</div>", unsafe_allow_html=True)
    cols = st.columns(5)
    metrics = [
        ("Files", len(st.session_state.uploaded_files)),
        ("Epics", stories_df["Epic"].nunique() if not stories_df.empty else 0),
        ("Stories", len(stories_df)),
        ("ACs", len(ac_df)),
        ("Avg ACs/Story", f"{(len(ac_df)/len(stories_df)) if len(stories_df)>0 else 0:.2f}")
    ]
    for col, (label, val) in zip(cols, metrics):
        col.markdown(
            f"<div class='metric-card'><div class='metric-label'>{label}</div>"
            f"<div class='metric-value'>{val}</div></div>", unsafe_allow_html=True
        )

    # ---------------------------
    # Unified Filters
    # ---------------------------
    f1, f2, f3 = st.columns([1, 1, 2])
    with f1:
        epic = st.selectbox("Filter by Epic", ["All"] + sorted(stories_df["Epic"].dropna().unique()), key="filter_epic")
    with f2:
        source = st.selectbox("Filter by File", ["All"] + sorted(stories_df["Source File"].dropna().unique()), key="filter_source")
    with f3:
        keyword = st.text_input("Search Title", key="filter_keyword")

    # Apply filters to stories
    filtered_df = stories_df.copy()
    if epic != "All": filtered_df = filtered_df[filtered_df["Epic"] == epic]
    if source != "All": filtered_df = filtered_df[filtered_df["Source File"] == source]
    if keyword: filtered_df = filtered_df[filtered_df["Story Title"].str.contains(keyword, case=False, na=False)]

    # Filter ACs based on filtered stories
    ac_filtered = ac_df[ac_df['Story ID'].isin(filtered_df['Story ID'])] if not filtered_df.empty else ac_df.iloc[0:0]

    # ---------------------------
    # Tabs
    # ---------------------------
    tab1, tab2 = st.tabs(["📖 Story Details", "✅ Acceptance Criteria"])

    # ---- Tab 1: Story Details ----
    with tab1:
        st.subheader("🎯 Filtered Summary")
        cols_f = st.columns(5)
        metrics_f = [
            ("Stories", len(filtered_df)),
            ("Epics", filtered_df["Epic"].nunique()),
            ("ACs", len(ac_filtered)),
            ("Modules", filtered_df["Module"].nunique()),
            ("Avg ACs/Story", f"{(len(ac_filtered) / len(filtered_df)) if len(filtered_df) > 0 else 0:.2f}")
        ]
        for col, (label, val) in zip(cols_f, metrics_f):
            col.markdown(
                f"<div class='metric-card'><div class='metric-label'>{label}</div>"
                f"<div class='metric-value'>{val}</div></div>", unsafe_allow_html=True
            )

        st.dataframe(filtered_df, use_container_width=True, hide_index=True)

        st.markdown("#### 📥 Export Stories")
        cx1, cx2 = st.columns(2)
        csv = filtered_df.to_csv(index=False).encode("utf-8-sig")
        with cx1:
            st.download_button("⬇️ CSV", csv, "stories.csv", "text/csv", use_container_width=True, key="csv_stories")
        excel_io = io.BytesIO()
        with pd.ExcelWriter(excel_io, engine="xlsxwriter") as writer:
            filtered_df.to_excel(writer, index=False, sheet_name="Stories")
        with cx2:
            st.download_button("⬇️ Excel", excel_io.getvalue(), "stories.xlsx",
                               "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                               use_container_width=True, key="excel_stories")

        st.markdown("---")
        if st.button("⬅️ Back to Upload", use_container_width=True, key="back_btn_tab1"):
            st.session_state.step = 1
            st.rerun()

    # ---- Tab 2: Acceptance Criteria ----
    with tab2:
        st.subheader("🎯 Filtered Summary")
        cols_ac = st.columns(5)
        metrics_ac = [
            ("ACs", len(ac_filtered)),
            ("Epics", ac_filtered["Epic"].nunique()),
            ("Stories", ac_filtered["Story ID"].nunique()),
            ("Modules", ac_filtered["Module"].nunique()),
            ("Files", ac_filtered["Source File"].nunique())
        ]
        for col, (label, val) in zip(cols_ac, metrics_ac):
            col.markdown(
                f"<div class='metric-card'><div class='metric-label'>{label}</div>"
                f"<div class='metric-value'>{val}</div></div>", unsafe_allow_html=True
            )

        st.dataframe(ac_filtered, use_container_width=True, hide_index=True)

        st.markdown("#### 📥 Export ACs")
        h1, h2 = st.columns(2)
        ac_csv = ac_filtered.to_csv(index=False).encode("utf-8-sig")
        with h1:
            st.download_button("⬇️ CSV", ac_csv, "acs.csv", "text/csv", use_container_width=True, key="csv_acs")
        ac_x = io.BytesIO()
        with pd.ExcelWriter(ac_x, engine="xlsxwriter") as writer:
            ac_filtered.to_excel(writer, index=False, sheet_name="Acceptance Criteria")
        with h2:
            st.download_button("⬇️ Excel", ac_x.getvalue(), "acs.xlsx",
                               "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                               use_container_width=True, key="excel_acs")

        st.markdown("---")
        if st.button("⬅️ Back to Upload", use_container_width=True, key="back_btn_tab2"):
            st.session_state.step = 1
            st.rerun()


# ------------------------------
# ABOUT PAGE
# ------------------------------
def render_about():
    """About section with improved styling and highlight boxes."""
    st.markdown("<div class='section-title'>ℹ️ About User Story Extractor</div>", unsafe_allow_html=True)

    st.markdown(
        """
        <div style='padding:12px; background:#f8faff; border-left:4px solid #1f77b4;
                    border-radius:6px; box-shadow:0 2px 4px rgba(0,0,0,0.05); margin-bottom:12px;'>
            <strong>User Story Extractor</strong> is a lightweight Streamlit app that converts
            <code>.docx</code>-based requirements into structured data for faster backlog creation.
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("### ✨ Features")
    st.markdown(
        """
        - 📄 Parses **Epics**, **User Stories**, and **Acceptance Criteria**  
        - ⚡ Handles inconsistent table headers automatically  
        - 📊 Provides rich metrics and export options (CSV/Excel)  
        - 🎨 Smooth UI designed for analysts and product teams  
        """
    )

    st.markdown("### 🛠 Use Cases")
    st.markdown(
        """
        - Rapidly migrate Word documents to tools like **Jira** or **Trello**  
        - Clean up inconsistent AC tables into a unified structure  
        - Share structured summaries with your development or QA teams  
        """
    )



# ------------------------------
# MANUAL PAGE
# ------------------------------
def render_manual():
    """User Manual with a single comprehensive sample format."""
    st.markdown("<div class='section-title'>📘 User Manual</div>", unsafe_allow_html=True)

    st.markdown("### ✅ Accepted Input")
    st.markdown(
        """
        - **File Type:** `.docx` (Microsoft Word) only  
        - **Recognized Patterns:**  
          - `Epic 1: Payments` → **Epics**  
          - `User Story 1: Add UPI option` → **User Stories**  
          - **Acceptance Criteria Tables** — normalized headers such as `S.No`, `Scenario`, `Acceptance Criteria`.
        """
    )

    st.markdown("### 🛠 Steps to Use")
    st.markdown(
        """
        1. 📂 **Upload** one or more `.docx` files containing your requirements.  
        2. 📊 **Analyze** extracted **Epics**, **Stories**, and **Acceptance Criteria** under *Results & Analysis*.  
        3. 🎯 **Filter & Search** by Epic, File, Story ID, or keyword.  
        4. 📥 **Export** filtered data to CSV or Excel for tools like Jira or Trello.  
        """
    )

    st.markdown("### 📑 Complete Example Format")
    st.code(
        "Module: Payments\n\n"
        "Epic 1: Payments\n\n"
        "User Story 1: Add UPI option\n\n"
        "AS A registered user\n"
        "I WANT to add a UPI payment option\n"
        "SO THAT I can make faster and easier payments.\n",
        language="markdown"
    )

    ac_table_html = """
    <div style='background:#f8faff; padding:10px; border-radius:6px; border:1px solid #d9e4ff;
                box-shadow:0 1px 3px rgba(0,0,0,0.05); width:90%;'>
        <table style='border-collapse:collapse; width:100%; font-size:14px;'>
            <tr style='background:#eaf1ff;'>
                <th style='border:1px solid #ccc; padding:6px;'>Sr. No</th>
                <th style='border:1px solid #ccc; padding:6px;'>Scenario</th>
                <th style='border:1px solid #ccc; padding:6px;'>Acceptance Criteria</th>
            </tr>
            <tr>
                <td style='border:1px solid #ccc; padding:6px;'>1.1</td>
                <td style='border:1px solid #ccc; padding:6px;'>Navigate to Payments Page</td>
                <td style='border:1px solid #ccc; padding:6px;'>Given the user is logged in<br>
                When they click “Payments” in the sidebar<br>
                Then the Payments page loads successfully</td>
            </tr>
            <tr>
                <td style='border:1px solid #ccc; padding:6px;'>1.2</td>
                <td style='border:1px solid #ccc; padding:6px;'>Add UPI Option</td>
                <td style='border:1px solid #ccc; padding:6px;'>Given the Payments page is visible<br>
                When the user clicks “Add UPI”<br>
                Then a form appears to add a UPI ID</td>
            </tr>
            <tr>
                <td style='border:1px solid #ccc; padding:6px;'>1.3</td>
                <td style='border:1px solid #ccc; padding:6px;'>Validate and Save UPI</td>
                <td style='border:1px solid #ccc; padding:6px;'>Given a valid UPI ID is entered<br>
                When the user clicks “Save”<br>
                Then the UPI payment option is added and displayed in the list</td>
            </tr>
        </table>
    </div>
    """
    st.markdown(ac_table_html, unsafe_allow_html=True)

    st.info(
        "💡 **Tip:** Keep your headers consistent (`Epic X:`, `User Story Y:`) and organize Acceptance Criteria "
        "in tables for best extraction accuracy."
    )






# ------------------------------
# JIRA PLACEHOLDER
# ------------------------------
def render_jira_placeholder():
    st.title("🚀 Jira Integration")
    st.info("⚠️ Jira integration is **In Progress**. Stay tuned for OAuth support and secure issue creation.")

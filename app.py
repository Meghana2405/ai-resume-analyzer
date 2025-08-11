# import streamlit as st
# import tempfile
# import os
# from utils import parser, scorer, predictor
# import plotly.express as px

# st.set_page_config(page_title="AI Resume Analyzer", layout='centered')
# st.title("📄 AI Resume Analyzer & Job Fit Predictor")
# st.write("Upload a resume (PDF/DOCX) and paste a job description to get ATS score & job-fit prediction.")

# uploaded_file = st.file_uploader("Upload Resume (PDF/DOCX)", type=["pdf", "docx"])
# job_desc = st.text_area("Paste Job Description Here (or upload below)")
# job_desc_file = st.file_uploader("Optional: Upload Job Description (TXT)", type=["txt"])

# if job_desc_file and not job_desc:
#     job_desc = job_desc_file.read().decode('utf-8')

# if st.button("Analyze"):
#     if not uploaded_file:
#         st.error("Please upload a resume file.")
#     elif not job_desc:
#         st.error("Please paste or upload a job description.")
#     else:
#         # Save temp resume file
#         ext = uploaded_file.name.split('.')[-1].lower()
#         tmp = tempfile.NamedTemporaryFile(delete=False, suffix='.' + ext)
#         tmp.write(uploaded_file.getvalue())
#         tmp.close()

#         # Extract text
#         if ext == 'pdf':
#             resume_text = parser.extract_text_from_pdf(tmp.name)
#         else:
#             resume_text = parser.extract_text_from_docx(tmp.name)

#         resume_text = parser.clean_text(resume_text)

#         # Extract entities
#         resume_data = parser.extract_entities(resume_text)
#         jd_data = parser.extract_entities(job_desc)

#         # ATS scoring
#         ats_score, matched = scorer.calculate_ats_score(resume_data['skills'], jd_data['skills'])
#         missing = scorer.find_missing_skills(resume_data['skills'], jd_data['skills'])

#         st.subheader("📊 Results")
#         st.markdown(f"**ATS Score:** `{ats_score}%`")
#         st.markdown(f"**Matched Skills:** {', '.join(matched) if matched else 'None'}")
#         st.markdown(f"**Missing Skills:** {', '.join(missing) if missing else 'None'}")

#         # Chart
#         fig = px.pie(names=["Matched", "Missing"], values=[len(matched), len(missing)], title="Skill Match Breakdown")
#         st.plotly_chart(fig)

#         # Load or train model
#         model = predictor.load_model()
#         fit_text = predictor.predict_fit(model, ats_score)
#         st.markdown(f"**Job Fit Prediction:** `{fit_text}`")

#         # Contact info and short summary
#         st.subheader("Candidate Summary")
#         contact = resume_data.get('contact', {})
#         st.write(f"**Name:** {contact.get('name', 'Not Found')}")
#         st.write(f"**Email(s):** {', '.join(contact.get('emails', [])) if contact.get('emails') else 'Not Found'}")
#         st.write(f"**Phone(s):** {', '.join(contact.get('phones', [])) if contact.get('phones') else 'Not Found'}")

#         st.success("Analysis complete. Use the matched and missing skills to improve the resume for better ATS results.")


# import streamlit as st
# import pandas as pd

# # Page config
# st.set_page_config(page_title="AI Resume Analyzer", page_icon="📄", layout="wide")

# # Load CSS
# with open("styles.css") as f:
#     st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# # Title
# st.title("📄 AI Resume Analyzer")
# st.markdown("### Upload your resume and let AI analyze your skills, experience, and strengths.")

# # Sidebar
# st.sidebar.header("⚙ Settings")
# analysis_type = st.sidebar.selectbox("Analysis Type", ["Skills Extraction", "Experience Summary", "ATS Score"])
# st.sidebar.markdown("---")
# st.sidebar.info("💡 Upload your resume in PDF or DOCX format for best results.")

# # Main content container with glass effect
# st.markdown('<div class="glass-card">', unsafe_allow_html=True)

# uploaded_file = st.file_uploader("📤 Upload Resume", type=["pdf", "docx"])

# if uploaded_file is not None:
#     st.success(f"✅ {uploaded_file.name} uploaded successfully!")

#     if st.button("🔍 Analyze Resume"):
#         st.info("⏳ Analyzing your resume with AI...")

#         # Example result
#         df = pd.DataFrame({
#             "Skill": ["Python", "Machine Learning", "Data Analysis"],
#             "Proficiency": ["Advanced", "Intermediate", "Advanced"]
#         })
#         st.markdown("### 🛠 Extracted Skills")
#         st.table(df)

#         st.success("✅ Analysis complete!")

# st.markdown('</div>', unsafe_allow_html=True)


# from flask import Flask, request, jsonify, render_template
# import os

# app = Flask(__name__)
# UPLOAD_FOLDER = "uploads"
# os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# @app.route("/")
# def index():
#     return render_template("index.html")  # This will handle all steps

# @app.route("/analyze_resume", methods=["POST"])
# def analyze_resume():
#     file = request.files.get("resume")
#     if not file:
#         return jsonify({"error": "No resume uploaded"}), 400

#     filepath = os.path.join(UPLOAD_FOLDER, file.filename)
#     file.save(filepath)

#     # Simulated AI analysis
#     return jsonify({
#         "score": 88,
#         "feedback": "Your resume is good but could include more quantifiable achievements."
#     })

# if __name__ == "__main__":
#     app.run(debug=True)


    # client_id="1053169346910-4p0j1t69ignll4u9r0l13uc03gf1tjid.apps.googleusercontent.com",
    # client_secret="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",

from flask import Flask, render_template, redirect, url_for, session, request
from flask_dance.contrib.google import make_google_blueprint, google
import os

app = Flask(__name__)
app.secret_key = "supersecretkey"
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Google OAuth blueprint - replace with your own credentials!
google_bp = make_google_blueprint(
    client_id="1053169346910-4p0j1t69ignll4u9r0l13uc03gf1tjid.apps.googleusercontent.com",
    client_secret="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",
    scope=[
        "openid",
        "https://www.googleapis.com/auth/userinfo.email",
        "https://www.googleapis.com/auth/userinfo.profile"
    ],

    redirect_url="/"
)
app.register_blueprint(google_bp, url_prefix="/login")


@app.route('/')
def welcome():
    if not google.authorized:
        return render_template("welcome.html", step=1, user_info=None)
    resp = google.get("/oauth2/v2/userinfo")
    if not resp.ok:
        return render_template("welcome.html", step=1, user_info=None)
    user_info = resp.json()
    session['user'] = user_info
    return render_template("welcome.html", step=1, user_info=user_info)


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('welcome'))


@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if not google.authorized:
        return redirect(url_for('welcome'))
    if request.method == 'POST':
        file = request.files.get('resume')
        if not file:
            return render_template("upload.html", error="Please upload a file.", step=2)
        filepath = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(filepath)
        session['resume_file'] = file.filename
        return redirect(url_for('role'))
    return render_template("upload.html", step=2)


@app.route('/role', methods=['GET', 'POST'])
def role():
    if not google.authorized:
        return redirect(url_for('welcome'))
    if request.method == 'POST':
        job_role = request.form.get('job_role')
        if not job_role:
            return render_template("role.html", error="Please select a job role.", step=3)
        session['job_role'] = job_role
        return redirect(url_for('analysis'))
    return render_template("role.html", step=3)


@app.route('/analysis', methods=['GET', 'POST'])
def analysis():
    if not google.authorized:
        return redirect(url_for('welcome'))
    if request.method == 'POST':
        result_data = {
            "score": 78,
            "feedback": f"Good resume for {session.get('job_role')}, but add more role-specific keywords."
        }
        session['result'] = result_data
        return redirect(url_for('results'))
    return render_template("analysis.html", step=4)


@app.route('/results')
def results():
    if not google.authorized:
        return redirect(url_for('welcome'))
    result = session.get('result')
    if not result:
        return redirect(url_for('upload'))
    return render_template("results.html", result=result, step=4)


if __name__ == '__main__':
    app.run(debug=True)

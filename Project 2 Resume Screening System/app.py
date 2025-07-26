import streamlit as st
import pandas as pd
import numpy as np
import spacy
import re
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from PyPDF2 import PdfReader
from docx import Document
from sklearn.metrics.pairwise import cosine_similarity
import en_core_web_sm
import matplotlib.pyplot as plt

# Page config
st.set_page_config(
    page_title="AI Resume Screening System",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

@st.cache_resource
def load_models():
    try:
        model = joblib.load('resume_classifier.pkl')
        tfidf = joblib.load('tfidf_vectorizer.pkl')
        nlp = spacy.load('en_core_web_sm')
        return model, tfidf, nlp
    except Exception as e:
        st.error(f"Error loading models: {str(e)}")
        return None, None, None

model, tfidf, nlp = load_models()

def preprocess_text(text):
    text = text.lower()
    text = re.sub(r'http\S+|www\S+|https\S+', '', text)
    text = re.sub(r'\S+@\S+', '', text)
    text = re.sub(r'[0-9]+', '', text)  
    doc = nlp(text)
    tokens = [token.lemma_ for token in doc if not token.is_punct]
    return ' '.join(tokens)

def read_pdf(file):
    reader = PdfReader(file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

def read_docx(file):
    doc = Document(file)
    return "\n".join([para.text for para in doc.paragraphs])

def read_txt(file):
    return file.read().decode("utf-8")

def calculate_similarity(jd_text, resume_text):
    jd_processed = preprocess_text(jd_text)
    resume_processed = preprocess_text(resume_text)

    vectors = tfidf.transform([jd_processed, resume_processed])
    similarity = cosine_similarity(vectors[0:1], vectors[1:2])[0][0]
    similarity_percent = round(similarity * 100, 2)

    jd_keywords = set(jd_processed.split())
    resume_keywords = set(resume_processed.split())
    matched_keywords = jd_keywords.intersection(resume_keywords)
    keyword_match_ratio = len(matched_keywords) / len(jd_keywords) if jd_keywords else 0

    final_score = 0.7 * similarity_percent + 0.3 * (keyword_match_ratio * 100)

    return round(final_score, 2), list(matched_keywords)[:10]

def plot_similarity_gauge(similarity_score):
    fig, ax = plt.subplots(figsize=(3, 2.5))
    wedges, _ = ax.pie(
        [similarity_score, 100 - similarity_score],
        startangle=90,
        colors=['#4CAF50' if similarity_score >= 75 else '#F44336', '#e0e0e0'],
        radius=1.2,
        wedgeprops=dict(width=0.3)
    )
    ax.text(0, 0, f"{similarity_score}%", ha='center', va='center', fontsize=14, weight='bold')
    ax.set_aspect('equal')
    plt.axis('off')
    plt.tight_layout()
    st.pyplot(fig)

# Main app
def main():
    st.markdown("""
    <style>
        .main { background-color: #f5f5f5; }
        .stButton>button {
            background-color: #4CAF50;
            color: white;
            border-radius: 5px;
            padding: 10px 24px;
        }
        .stTextInput>div>div>input { border-radius: 5px; }
        .stFileUploader>div>div>div>button { border-radius: 5px; }
        .sidebar .sidebar-content { background-color: #ffffff; }
        .result-box {
            border: 2px solid #4CAF50;
            border-radius: 5px;
            padding: 20px;
            margin: 10px 0px;
            background-color: #f9f9f9;
        }
    </style>
    """, unsafe_allow_html=True)

    st.sidebar.title("About")
    st.sidebar.info(
        """
        **AI Resume Screening System**  
        This application uses machine learning to:
        - Classify resumes into job categories
        - Compare resumes against job descriptions
        - Provide screening recommendations
        """
    )
    st.sidebar.markdown("---")
    st.sidebar.markdown("**Instructions:**")
    st.sidebar.markdown("1. Upload the Job Description (text or file)")
    st.sidebar.markdown("2. Upload the Resume (PDF, DOCX, or TXT)")
    st.sidebar.markdown("3. Click 'Analyze' to get results")

    st.title("📄 AI Resume Screening System")
    st.markdown("Upload a job description and resume to analyze compatibility.")

    col1, col2 = st.columns([1,1])

    with col1:
        st.subheader("Job Description")
        jd_text = st.text_area("Or paste JD text here:", height=200)
        jd_file = st.file_uploader("Upload JD (TXT, PDF, DOCX):", type=['txt', 'pdf', 'docx'], key="jd")

    with col2:
        st.subheader("Resume")
        resume_file = st.file_uploader("Upload Resume (PDF, DOCX, TXT):", type=['pdf', 'docx', 'txt'], key="resume")

    if jd_file is not None:
        if jd_file.type == "application/pdf":
            jd_text = read_pdf(jd_file)
        elif jd_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            jd_text = read_docx(jd_file)
        else:
            jd_text = read_txt(jd_file)
        st.session_state.jd_text = jd_text

    if 'jd_text' in st.session_state:
        st.text_area("Current JD Text:", value=st.session_state.jd_text, height=200, key="jd_display")

    if st.button("Analyze Resume", key="analyze"):
        if (jd_text or 'jd_text' in st.session_state) and resume_file is not None:
            with st.spinner("Processing documents..."):
                try:
                    if resume_file.type == "application/pdf":
                        resume_text = read_pdf(resume_file)
                    elif resume_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
                        resume_text = read_docx(resume_file)
                    else:
                        resume_text = read_txt(resume_file)

                    processed_resume = preprocess_text(resume_text)
                    resume_vector = tfidf.transform([processed_resume])
                    prediction = model.predict(resume_vector)[0]
                    prediction_proba = model.predict_proba(resume_vector)[0]

                    current_jd_text = jd_text if jd_text else st.session_state.jd_text

                    similarity_score, matched_keywords = calculate_similarity(current_jd_text, resume_text)

                    if prediction.lower() in current_jd_text.lower():
                        similarity_score = min(100, similarity_score + 35)

                    st.markdown("---")
                    st.subheader("Analysis Results")
                    col1, col2 = st.columns(2)

                    with col1:
                        st.markdown("**Resume Classification**")
                        st.markdown(f"Predicted Role: **{prediction}**")
                        proba_df = pd.DataFrame({
                            'Category': model.classes_,
                            'Probability': prediction_proba
                        }).sort_values('Probability', ascending=False)

                        fig, ax = plt.subplots(figsize=(6, 4.5))
                        top_probs = proba_df.sort_values(by='Probability', ascending=False).head(5)

                        ax.bar(top_probs['Category'], top_probs['Probability'], color='royalblue')
                        ax.set_ylabel('Probability', fontsize=12)
                        ax.set_title('Top 5 Roles', fontsize=14)
                        ax.set_xticklabels(top_probs['Category'], rotation=45, ha='right', color='black')
                        ax.tick_params(axis='y', colors='black')
                        ax.tick_params(axis='x', colors='black')
                        plt.tight_layout()
                        st.pyplot(fig)


                    with col2:
                        st.markdown("**JD Matching**")
                        plot_similarity_gauge(similarity_score)

                    st.markdown("---")
                    verdict_container = st.container()
                    if similarity_score >= 75 and prediction.lower() in current_jd_text.lower():
                        verdict = "✅ Screening IN - Good match for the role!"
                        color = "green"
                    else:
                        verdict = "❌ Screening OUT - Doesn't meet criteria"
                        color = "red"

                    verdict_container.markdown(
                        f"""
                        <div class="result-box">
                            <h3 style='color:{color}; text-align:center;'>Final Verdict: {verdict}</h3>
                            <p><b>Reason:</b> {
                                f"Similarity score ({similarity_score}%) meets threshold and resume matches predicted role" 
                                if similarity_score >= 75 and prediction.lower() in current_jd_text.lower() 
                                else f"Either similarity score ({similarity_score}%) is below threshold or resume doesn't match the role requirements"
                            }</p>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                except Exception as e:
                    st.error(f"An error occurred during processing: {str(e)}")
        else:
            st.warning("Please provide both a Job Description and a Resume to analyze.")

if __name__ == "__main__":
    main()

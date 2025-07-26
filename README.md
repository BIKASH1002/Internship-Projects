 **Role**: Data Science & Machine Learning Intern  
**Organization**: Zaalima Development  

## Project 1: Real-Time Credit Card Fraud Detection System

### Overview
This project focuses on building a robust, real-time fraud detection pipeline using machine learning to distinguish between legitimate and fraudulent transactions. The solution is designed to assist financial institutions in reducing false positives while maintaining high fraud detection accuracy.

### Key Features
- Exploratory Data Analysis (EDA) on anonymized credit card datasets
- Preprocessing: Data balancing using SMOTE, feature scaling, encoding
- Trained multiple models: Logistic Regression, Random Forest, XGBoost, CatBoost
- Hyperparameter tuning with Optuna for optimal performance
- Achieved 99%+ accuracy on balanced data
- Real-time prediction system deployed via **Streamlit** interface
- Integrated model pipeline for seamless fraud detection on incoming data

### Tech Stack & Tools
- Python, NumPy, Pandas, Scikit-learn, XGBoost, CatBoost
- Streamlit (for UI), Matplotlib, Seaborn (for visualization)
- Optuna (for hyperparameter tuning)
- Git for version control

### Structure

fraud_detection/

├── app/ # Streamlit App

├── data/ # Raw & cleaned datasets

├── models/ # Saved model files (Pickle/Joblib)

├── notebooks/ # EDA and model training notebooks


## Project 2: AI-Based Resume Screening System

### Overview
Designed an AI-powered resume screening tool to automate and enhance the recruitment workflow. The tool allows HR teams to upload resumes and match them with job descriptions using Natural Language Processing (NLP) techniques and machine learning models.

### Key Features
- Resume parsing and preprocessing using **spaCy**
- Text vectorization with **TF-IDF**
- Role and experience match evaluation
- Visual resume–JD match percentage
- Trained models: Naive Bayes, SVM, Logistic Regression, BERT
- Multiple evaluation metrics: Accuracy, Precision, Recall, F1 Score
- Visualizations: Word Cloud, Cosine Similarity Heatmap, Radar Charts
- Deployed with an interactive **Streamlit** interface

### Tech Stack & Tools
- Python, Scikit-learn, spaCy, NLTK, Transformers (BERT)
- TF-IDF, Cosine Similarity, WordCloud, Matplotlib, Seaborn
- Streamlit (for deployment)
- Git, GitHub

### Structure

resume_screening_system/

├── app/ # Streamlit App

├── data/ # Resume samples & job descriptions

├── models/ # Trained models

├── notebooks/ # Preprocessing & modeling

├── visualizations/ # All plots and charts


## Outcomes & Learning
- Strengthened end-to-end project lifecycle experience from data ingestion to deployment
- Gained hands-on experience in building real-time applications using **Streamlit**
- Deepened understanding of NLP techniques and model interpretability
- Improved code modularity, documentation, and model versioning practices

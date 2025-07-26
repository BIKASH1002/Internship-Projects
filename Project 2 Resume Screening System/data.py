import pandas as pd
import numpy as np
import random
from faker import Faker
import os
from datetime import datetime, timedelta

fake = Faker()

os.makedirs('resume_dataset_final', exist_ok=True)

# Categories
skills = {
    'Software Engineer': ['Python', 'Java', 'C++', 'Git', 'SQL', 'Docker', 'AWS', 'REST APIs', 'JavaScript', 'Microservices'],
    'Data Scientist': ['Python', 'R', 'SQL', 'Machine Learning', 'Pandas', 'TensorFlow', 'Statistics', 'Data Visualization', 'Spark', 'Deep Learning'],
    'Marketing Manager': ['SEO', 'Google Analytics', 'Social Media', 'Content Marketing', 'PPC', 'CRM', 'Market Research', 'Brand Management', 'Digital Marketing', 'Copywriting'],
    'Financial Analyst': ['Excel', 'Financial Modeling', 'VBA', 'Accounting', 'Forecasting', 'Tableau', 'Risk Management', 'Bloomberg Terminal', 'Valuation', 'Economics'],
    'HR Specialist': ['Recruiting', 'Employee Relations', 'HRIS', 'Compensation', 'Talent Management', 'Training', 'Labor Law', 'Performance Management', 'Onboarding', 'Benefits Administration'],
    'Data Analyst': ['SQL', 'Excel', 'Tableau', 'Power BI', 'Python', 'Data Cleaning', 'Statistics', 'Google Analytics', 'Dashboarding', 'A/B Testing'],
    'Cybersecurity Analyst': ['SIEM', 'Firewalls', 'Penetration Testing', 'Risk Assessment', 'Incident Response', 'NIST', 'ISO 27001', 'Network Security', 'Cryptography', 'Threat Intelligence'],
    'UX Designer': ['Figma', 'User Research', 'Wireframing', 'Prototyping', 'UI Design', 'Usability Testing', 'Information Architecture', 'Adobe XD', 'Interaction Design', 'Accessibility'],
    'DevOps Engineer': ['AWS', 'Docker', 'Kubernetes', 'CI/CD', 'Terraform', 'Ansible', 'Linux', 'Jenkins', 'Monitoring', 'Infrastructure as Code'],
    'Product Manager': ['Agile', 'Scrum', 'Product Roadmap', 'Market Research', 'User Stories', 'JIRA', 'Competitive Analysis', 'KPIs', 'Go-to-Market', 'Customer Development']
}

# Common skills 
common_skills = ['Microsoft Office', 'Communication', 'Leadership', 'Project Management', 'Teamwork', 'Problem Solving', 'Time Management', 'Presentation Skills']

# Education 
degrees = ['Bachelors', 'Masters', 'PhD', 'Diploma']

similar_categories = {
    'Software Engineer': ['DevOps Engineer', 'Data Scientist'],
    'Data Scientist': ['Data Analyst', 'Software Engineer'],
    'Marketing Manager': ['Product Manager', 'HR Specialist'],
    'Financial Analyst': ['Data Analyst', 'Software Engineer'],
    'HR Specialist': ['Marketing Manager', 'Data Analyst'], 
    'Data Analyst': ['Data Scientist', 'Financial Analyst'],
    'Cybersecurity Analyst': ['DevOps Engineer', 'Software Engineer'],
    'UX Designer': ['Product Manager', 'Marketing Manager'],
    'DevOps Engineer': ['Software Engineer', 'Cybersecurity Analyst'],
    'Product Manager': ['Marketing Manager', 'UX Designer']
}

def generate_job_title(category, experience_level):
    titles = {
        'Software Engineer': ['Junior Software Engineer', 'Software Engineer', 'Senior Software Engineer', 'Lead Developer'],
        'Data Scientist': ['Data Science Intern', 'Junior Data Scientist', 'Data Scientist', 'Senior Data Scientist'],
        'Marketing Manager': ['Marketing Coordinator', 'Marketing Specialist', 'Marketing Manager', 'Senior Marketing Manager'],
        'Financial Analyst': ['Financial Analyst I', 'Financial Analyst II', 'Senior Financial Analyst', 'Finance Manager'],
        'HR Specialist': ['HR Assistant', 'HR Generalist', 'HR Specialist', 'HR Manager'],
        'Data Analyst': ['Data Analyst', 'Business Analyst', 'Senior Data Analyst', 'Analytics Manager'],
        'Cybersecurity Analyst': ['Security Analyst', 'Cybersecurity Specialist', 'Security Engineer', 'CISO'],
        'UX Designer': ['UX Designer', 'UI/UX Designer', 'Senior UX Designer', 'UX Lead'],
        'DevOps Engineer': ['DevOps Engineer', 'Site Reliability Engineer', 'Cloud Engineer', 'DevOps Manager'],
        'Product Manager': ['Associate Product Manager', 'Product Manager', 'Senior Product Manager', 'Director of Product']
    }
    
    if category not in titles:
        category = 'HR Specialist' 
    
    experience_level = max(0, min(experience_level, len(titles[category])-1))
    return titles[category][experience_level]

resumes = []
categories = []

for i in range(2000):
    category = random.choice(list(skills.keys()))
    categories.append(category)
    
    resume_content = []
    
    resume_content.append(f"Name: {fake.name()}")
    resume_content.append(f"Email: {fake.email()}")
    resume_content.append(f"Phone: {fake.phone_number()}")
    resume_content.append(f"LinkedIn: {fake.url()}")
    resume_content.append("\n")
    
    if random.random() < 0.5:
        resume_content.append("SUMMARY")
        summary = f"Experienced {category} with {random.randint(2,10)} years in "
        summary += random.choice(["technology", "business solutions", "cross-functional teams", "strategic initiatives"])
        summary += f". Skilled in {random.choice(skills[category])} and {random.choice(common_skills)}."
        resume_content.append(summary)
        resume_content.append("\n")
    
    resume_content.append("EDUCATION")
    degree = random.choice(degrees)

    if category in ['Data Scientist', 'Financial Analyst'] and degree == 'PhD':
        degree = random.choice(['Masters', 'Bachelors'])  
    if category in ['Software Engineer', 'DevOps Engineer'] and random.random() < 0.2:
        resume_content.append(f"Bootcamp Certification in {category.replace(' Engineer', ' Development')}, {fake.company()}")
    
    major = fake.job().split()[0] + " Studies" if random.random() < 0.7 else {
        'Software Engineer': 'Computer Science',
        'Data Scientist': 'Data Science',
        'Data Analyst': 'Statistics',
        'Financial Analyst': 'Finance',
        'Marketing Manager': 'Marketing',
        'HR Specialist': 'Human Resources',
        'Cybersecurity Analyst': 'Cybersecurity',
        'UX Designer': 'Human-Computer Interaction',
        'DevOps Engineer': 'Computer Engineering',
        'Product Manager': 'Business Administration'
    }[category]
    
    resume_content.append(f"{degree} in {major}, {fake.company()} University, {fake.year()}")
    resume_content.append("\n")
    
    resume_content.append("EXPERIENCE")
    num_jobs = random.randint(2, 5)
    total_years = 0
    
    for j in range(num_jobs):
        years = random.randint(1, 4)
        total_years += years
        
        exp_level = min(3, total_years // 3)
        
        if j == 0:
            job_title = generate_job_title(category, exp_level)
            company_desc = f"{fake.company()} - {fake.catch_phrase()}"
        else:
            if random.random() < 0.3:  
                similar_cat = random.choice(similar_categories[category])
                job_title = generate_job_title(similar_cat, max(0, exp_level-1))
            else:
                job_title = generate_job_title(category, max(0, exp_level-1))
            company_desc = fake.company()
        
        dates = f"{fake.date_between(start_date='-' + str(total_years+5) + 'y', end_date='-' + str(total_years) + 'y').strftime('%b %Y')} - "
        dates += fake.date_between(start_date='-' + str(total_years) + 'y', end_date='today').strftime('%b %Y')
        
        resume_content.append(f"{job_title}")
        resume_content.append(f"{company_desc} | {dates}")
        
        num_bullets = random.randint(3, 5)
        for _ in range(num_bullets):
            action = random.choice(['Led', 'Developed', 'Implemented', 'Analyzed', 'Managed', 'Optimized', 'Designed'])
            tech = random.choice(skills[category] + common_skills) if random.random() < 0.7 else ""
            outcome = random.choice([
                "resulting in improved efficiency",
                "leading to cost savings",
                "increasing performance by",
                "reducing time to market by",
                "improving user satisfaction"
            ]) if random.random() < 0.5 else ""
            
            bullet = f"- {action} {tech} {fake.bs()} {outcome}"
            if random.random() < 0.1:  
                bullet = bullet.replace('ing ', 'ed ').replace('ed ', 'ing ')
            resume_content.append(bullet)
        
        resume_content.append("\n")
    
    # Skills
    resume_content.append("SKILLS")
    
    resume_content.append("Technical:")
    num_specific = random.randint(5, 8)  
    for skill in random.sample(skills[category], num_specific):
        resume_content.append(f"- {skill}")
    
    num_related = random.randint(2, 4)
    related_category = random.choice(similar_categories[category])
    for skill in random.sample(skills[related_category], num_related):
        resume_content.append(f"- {skill}")
    
    # Tools/Platforms 
    if random.random() < 0.5:
        resume_content.append("\nTools:")
        tools = random.sample([
            'JIRA', 'Confluence', 'Slack', 'Trello', 'Asana',
            'GitHub', 'GitLab', 'Bitbucket', 'Jenkins', 'CircleCI'
        ], random.randint(2, 4))
        for tool in tools:
            resume_content.append(f"- {tool}")
    
    # Soft Skills 
    resume_content.append("\nProfessional:")
    num_common = random.randint(3, 5)
    for skill in random.sample(common_skills, num_common):
        resume_content.append(f"- {skill}")
    
    # Certifications 
    if random.random() < 0.3:
        resume_content.append("\nCERTIFICATIONS")
        certs = {
            'Software Engineer': ['AWS Certified Developer', 'Google Cloud Professional'],
            'Data Scientist': ['TensorFlow Developer', 'Data Science Council'],
            'Marketing Manager': ['Google Analytics IQ', 'HubSpot Content Marketing'],
            'Financial Analyst': ['CFA Level I', 'FRM Certification'],
            'HR Specialist': ['PHR', 'SHRM-CP'],
            'Data Analyst': ['Google Data Analytics', 'Microsoft Data Analyst'],
            'Cybersecurity Analyst': ['CISSP', 'CEH'],
            'UX Designer': ['Google UX Design', 'NN/g UX Certification'],
            'DevOps Engineer': ['CKAD', 'Docker Certified'],
            'Product Manager': ['Pragmatic Institute', 'SAFe Product Owner']
        }
        resume_content.append(f"- {random.choice(certs[category])}")
    
    full_resume = "\n".join(resume_content)
    
    if random.random() < 0.3:
        full_resume = full_resume.replace("\n- ", "\n• ")
    if random.random() < 0.2:
        full_resume = full_resume.replace(": ", ":\n")
    
    resumes.append(full_resume)

df = pd.DataFrame({
    'resume_id': range(1, 2001),
    'resume_text': resumes,
    'category': categories
})

ambiguous_indices = random.sample(range(2000), 140)
for idx in ambiguous_indices:
    current_cat = df.loc[idx, 'category']
    df.loc[idx, 'category'] = random.choice(similar_categories[current_cat])

random_indices = random.sample(range(2000), 60)
for idx in random_indices:
    df.loc[idx, 'category'] = random.choice(list(skills.keys()))

df.to_csv('Dataset/resume.csv', index=False)

print("Dataset successfully generated with:")
print("- 2000 resumes")
print("- 10 professional categories")
print("- 7% ambiguous cases")
print("- 3% random labeling errors")
print(f"Saved to: resume_dataset_final/resume_data_10_categories.csv")
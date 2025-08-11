import pandas as pd
from datetime import datetime
import os

data = [
    # Software Engineer samples
    {"skills": "Python, Flask, SQL, APIs, Docker", "job_role": "Software Engineer"},
    {"skills": "Python, Django, MySQL, REST APIs, AWS", "job_role": "Software Engineer"},
    {"skills": "Flask, PostgreSQL, Docker, Microservices", "job_role": "Software Engineer"},

    # Financial Analyst samples
    {"skills": "Accounting, financial analysis, tax, audit", "job_role": "Financial Analyst"},
    {"skills": "Financial reporting, budgeting, Excel, SAP", "job_role": "Financial Analyst"},

    # Data Scientist samples
    {"skills": "Machine learning, pandas, TensorFlow, data analysis", "job_role": "Data Scientist"},
    {"skills": "Python, R, data mining, statistics, scikit-learn", "job_role": "Data Scientist"},

    # Frontend Developer samples
    {"skills": "React, JavaScript, HTML, CSS, UI design", "job_role": "Frontend Developer"},
    {"skills": "Vue.js, JavaScript, HTML5, CSS3, responsive design", "job_role": "Frontend Developer"},

    # System Administrator samples
    {"skills": "Linux, servers, networking, cybersecurity", "job_role": "System Administrator"},
    {"skills": "Windows Server, Active Directory, PowerShell, VMware", "job_role": "System Administrator"},

    # Full Stack Developer samples
    {"skills": "Node.js, React, MongoDB, Express, Docker", "job_role": "Full Stack Developer"},
    {"skills": "JavaScript, Angular, Node.js, MySQL, AWS", "job_role": "Full Stack Developer"},

    # Back End Developer samples
    {"skills": "Java, Spring Boot, PostgreSQL, REST APIs, microservices", "job_role": "Back End Developer"},
    {"skills": "Python, Flask, SQL, API design, Docker", "job_role": "Back End Developer"},

    # DevOps Engineer samples
    {"skills": "AWS, Azure, cloud computing, DevOps, CI/CD", "job_role": "DevOps Engineer"},
    {"skills": "Docker, Kubernetes, Jenkins, Terraform, monitoring", "job_role": "DevOps Engineer"},

    # UI/UX Designer samples
    {"skills": "UX research, wireframing, Figma, Adobe XD", "job_role": "UI/UX Designer"},
    {"skills": "User interface design, prototyping, Sketch, usability testing", "job_role": "UI/UX Designer"},

    # Business Analyst samples
    {"skills": "Business analysis, requirements gathering, stakeholder management", "job_role": "Business Analyst"},
    {"skills": "Process mapping, documentation, SQL, project coordination", "job_role": "Business Analyst"},

    # Graphic Designer samples
    {"skills": "Photoshop, Illustrator, branding, typography", "job_role": "Graphic Designer"},
    {"skills": "InDesign, Adobe Creative Suite, layout, color theory", "job_role": "Graphic Designer"},

    # Project Manager samples
    {"skills": "Agile, Scrum, project planning, Jira, communication", "job_role": "Project Manager"},
    {"skills": "Risk management, budgeting, team leadership, Waterfall", "job_role": "Project Manager"},

    # iOS Developer samples
    {"skills": "Mobile development, Swift, Xcode, UI design, iOS", "job_role": "iOS Developer"},
    {"skills": "Objective-C, Swift, Core Data, UIKit, app debugging", "job_role": "iOS Developer"},

    # Android Developer samples
    {"skills": "Android, Kotlin, Java, Firebase, UI/UX", "job_role": "Android Developer"},
    {"skills": "Java, Android Studio, REST APIs, mobile testing", "job_role": "Android Developer"},

    # Data Analyst samples
    {"skills": "Excel, Power BI, data visualization, SQL, reporting", "job_role": "Data Analyst"},
    {"skills": "Tableau, Python, data cleaning, dashboard creation", "job_role": "Data Analyst"},
]

# Add timestamp to all entries
timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
for item in data:
    item["timestamp"] = timestamp

# Create DataFrame and reorder columns
df = pd.DataFrame(data)
df = df[["timestamp", "skills", "job_role"]]

# Save CSV
csv_file = os.path.join("./resume_samples.csv")
df.to_csv(csv_file, index=False)

print(f"✅ CSV created: {csv_file}")

import pandas as pd
from datetime import datetime
import os

data = [
    {"skills": "Python, Flask, SQL, APIs, Docker", "job_role": "Software Engineer"},
    {"skills": "Accounting, financial analysis, tax, audit", "job_role": "Financial Analyst"},
    {"skills": "Machine learning, pandas, TensorFlow, data analysis", "job_role": "Data Scientist"},
    {"skills": "React, JavaScript, HTML, CSS, UI design", "job_role": "Frontend Developer"},
    {"skills": "Linux, servers, networking, cybersecurity", "job_role": "System Administrator"},
    {"skills": "Node.js, React, MongoDB, Express, Docker", "job_role": "Full Stack Developer"},
    {"skills": "Java, Spring Boot, PostgreSQL, REST APIs, microservices", "job_role": "Back End Developer"}
]

timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
for item in data:
    item["timestamp"] = timestamp

df = pd.DataFrame(data)

df = df[["timestamp", "skills", "job_role"]]

csv_file = os.path.join("./resume_samples.csv")
df.to_csv(csv_file, index=False)

print(f"CSV created: {csv_file}")

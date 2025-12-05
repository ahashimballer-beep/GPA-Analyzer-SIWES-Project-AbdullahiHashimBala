GPA Analyzer & Predictor — Documentation (VS Code)

Prepared by: Abdullahi Hashim Bala  
Matric Number: 24C-SCT-SEN-0138  
Department: Software Engineering  
School: Cosmopolitan University  
Supervisor: Mr. Michael Okoronu

Project Overview
GPA Analyzer & Predictor is a Streamlit application that allows students to input semester results (courses, units, grades), compute semester GPA and cumulative CGPA, visualize progress across semesters, and simulate GPA scenarios to plan for a target CGPA. The app supports both 5.0 and 4.0 grading systems.

Files in this project

- `main.py` — Streamlit application (UI + logic)
- `data.py` — grading system mappings (`GRADE_SYSTEMS`)
- `utils.py` — helper functions: `calculate_gpa`, `generate_course_plan`
- `sample_grades.csv` — sample dataset for testing
- `Documentation.md` — this document
- `README.md` — quick run instructions
- `Slides.pdf` — short presentation for SIWES submission

How it works (high level)

1. Add Semester: Enter course name, units, grade; compute semester GPA; save semester.
2. View Progress: Visualize GPA trend across saved semesters.
3. Scenario Predictor: Plan to reach a target CGPA, generate example course plans, simulate future courses, and get rule-based study advice.

Key Functions & Formulas

- Points mapping: `Points = Grade mapped from grading scale` (e.g., A→5)
- Weighted points: `Weighted = Points * Units`
- Semester GPA: `sum(Weighted) / sum(Units)` (rounded to 2 decimals)
- CGPA: computed across all saved semesters using the same formula.

How to run (VS Code)

1. Clone this folder into your machine.
2. Open VS Code and open the folder. Install recommended extensions: Python, Pylance.
3. Create a virtual environment and install dependencies:

```
python -m venv .venv
source .venv/bin/activate   # Mac/Linux
.\.venv\Scripts\activate  # Windows (PowerShell)
pip install streamlit pandas matplotlib
```

4. Run the app:

```
streamlit run main.py
```

5. Use the sidebar to navigate pages, add semesters, and test scenario predictions.

Notes & Tips

- Ensure `main.py`, `data.py`, and `utils.py` are in the same directory.
- If you change grading system in Settings, redo calculations if needed.
- Export/Import CSV available in Settings for backup.

Reflection (SIWES)
During this SIWES project I implemented a practical tool for students to track and plan academic performance. I practiced Streamlit app design, dataframe manipulation with pandas, and visualization with matplotlib. Challenges included handling Streamlit reruns and properly persisting session state; solutions used `st.session_state` for persistence.

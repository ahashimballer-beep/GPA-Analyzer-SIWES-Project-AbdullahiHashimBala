import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from data import GRADE_SYSTEMS
from utils import calculate_gpa
from utils import generate_course_plan


if "grading_option" not in st.session_state:
    st.session_state.grading_option = "5.0" #default grading system

st.set_page_config(page_title="GPA_Analyzer", layout="wide")

st.title("Student Grade Tracker App")
st.sidebar.title("Menu")

page = st.sidebar.selectbox("Go to:", ["Add Semester", "View Progress", "Scenario Predictor", "Settings"])


if "all_semesters_df" not in st.session_state:
        st.session_state.all_semesters_df = pd.DataFrame(columns=["Semester", "Courses", "Units", "Grade", "Points", "Weighted"])
    
if page == "Add Semester":
    if "all_semesters_df" not in st.session_state:
        st.session_state.all_semesters_df = pd.DataFrame(columns=["Semester", "Courses", "Units", "Grade", "Points", "Weighted"])
    st.header("Add Semester Results")
    if "semester_df" not in st.session_state:
        st.session_state.semester_df = pd.DataFrame(columns=["Course", "Units", "Grade"])
    st.subheader("Add a Course")

    with st.form("course_form"):
        course = st.text_input("Course Name")
        units = st.number_input("Units", min_value=1, max_value=10)
        grade = st.text_input("Grade (e.g. A, B, C)").upper()

        submitted = st.form_submit_button("Add Course")
    # Get current grading system
    grading_scale = GRADE_SYSTEMS[st.session_state.grading_option]
    if submitted:
        if course and grade:
            points = grading_scale.get(grade, 0)
            weighted = points * units

            new_row = {"Course": course, "Units": units, "Grade": grade, "Points": points, "Weighted": weighted}
            st.session_state.semester_df = pd.concat(
                [st.session_state.semester_df, pd.DataFrame([new_row])],
                ignore_index=True
            )
            st.success(f"{course} added!")
        else:
            st.error("Please fill all fields")
    
    st.write("### Current Semester Courses")
    st.dataframe(st.session_state.semester_df)

    if not st.session_state.semester_df.empty:
        gpa = calculate_gpa(st.session_state.semester_df, grading_scale)
        st.success(f"Semester GPA: {gpa}")

    semester_name = st.text_input("Enter semester name (e.g., 100L 1st Sem)")
    if st.button("Save Semester"):
        if not st.session_state.semester_df.empty and semester_name:
            # Add semester_column
            df_to_save = st.session_state.semester_df.copy()
            df_to_save["Semester"] = semester_name

            # Calculate points and weighted points
            grading_scale = GRADE_SYSTEMS[st.session_state.grading_option]
            df_to_save["Points"] = df_to_save["Grade"].map(grading_scale)
            df_to_save["Weighted"] = df_to_save["Points"] * df_to_save["Units"]

            # Append to all_semester_df
            st.session_state.all_semesters_df = pd.concat(
                [st.session_state.all_semesters_df, df_to_save],
                ignore_index=True
            )

            # Clear current semester
            st.session_state.semester_df = pd.DataFrame(columns=["Course", "Units", "Grade"])
            st.success(f"{semester_name} saved successfully")
        else:
            st.error("Please enter courses and semester name")


        if not st.session_state.all_semesters_df.empty:
            total_weighted = st.session_state.all_semesters_df["Weighted"].sum()
            total_units = st.session_state.all_semesters_df["Units"].sum()
            cgpa = round(total_weighted / total_units, 2)
            st.info(f"Current CGPA: {cgpa}")
        st.write("### All Saved Semesters")
        st.dataframe(st.session_state.all_semesters_df)

elif page == "View Progress":
    st.header("Your Progress")
    if not st.session_state.all_semesters_df.empty:
        semesters_gpa = (
            st.session_state.all_semesters_df.groupby("Semester")
            .apply(lambda x: round(x["Weighted"].sum() / x["Units"].sum(), 2))
        )
        fig, ax = plt.subplots(figsize=(8, 4))
        ax.plot(semesters_gpa.index, semesters_gpa.values, marker="o", linestyle="-", color="blue")
        ax.set_title("GPA Trend Across Semesters")
        ax.set_xlabel("Semester")
        ax.set_ylabel("GPA")
        ax.set_ylim(0, st.session_state.all_semesters_df["Points"].max() + 1)
        ax.grid(True)

        st.pyplot(fig)

        selected_semester = st.selectbox("Select Semester to View Courses", semesters_gpa.index)

        df_sem = st.session_state.all_semesters_df[st.session_state.all_semesters_df["Semester"] == selected_semester]

        fig2, ax2 = plt.subplots(figsize=(8, 4))
        ax2.bar(df_sem["Course"], df_sem["Points"], color="green")
        ax2.set_title(f"Grades in {selected_semester}")
        ax2.set_ylabel("Grade Points")
        ax2.set_ylim(0, st.session_state.all_semesters_df["Points"].max() + 1)
        st.pyplot(fig2)

elif page == "Settings":
    st.header("Settings")
    st.subheader("Choose Grading System")

    grading_selection = st.selectbox(
        "Select your school's grading system:",
        ["5.0", "4.0"]
    )
    st.session_state.grading_option = grading_selection
    st.write("Current system:", st.session_state.grading_option)

    st.markdown("---")
    st.header("Data Management")

    st.subheader("Export Your Data")

    if not st.session_state.all_semesters_df.empty:
        csv_data = st.session_state.all_semesters_df.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="Download All Semesters as CSV",
            data=csv_data,
            file_name="my semesters.csv",
            mime="text/csv"
        )
    else:
        st.info("No data available yet. Add semesters first.")

    st.subheader("Import Data From CSV")

    uploaded_file = st.file_uploader("Upload CSV file", type=["csv"])

    if uploaded_file is not None:
        try:
            imported_df = pd.read_csv(uploaded_file)

            required_columns = {"Semester", "Course", "Units", "Grade", "Points", "Weighted"}

            if required_columns.issubset(imported_df.columns):
                st.session_state.all_semesters_df = pd.concat(
                    [st.session_state.all_semesters_df, imported_df],
                    ignore_index=True
                )
                st.success("CSV imported successfully!")
                st.dataFrame(imported_df)
            else:
                st.error(f"CSV format incorrect. Must contain columns: {required_columns}")
        
        except Exception as e:
            st.error(f"Error reading CSV: {e}")


elif page == "Scenario Predictor":
    st.header("GPA Scenario Predictor")

    if "all_semesters_df" not in st.session_state or st.session_state.all_semesters_df.empty:
        st.warning("No semester data found. Add semesters first.")
        st.stop()
    
    df = st.session_state.all_semesters_df

    total_weighted = df["Weighted"].sum()
    total_units = df["Units"].sum()

    current_cgpa = round(total_weighted / total_units, 2)

    st.subheader("Current Academic Performance")
    st.write(f"**Total Units Completed:** {total_units}")
    st.write(f"**Current CGPA:** {current_cgpa}")

    st.divider()

    st.subheader("Goal Planner - Reach a Target CGPA")

    max_cgpa = float(st.session_state.grading_option)
    target = st.number_input(f"Enter your target final CGPA (0 - {max_cgpa}):", min_value=0.0, max_value=max_cgpa, value=min(max_cgpa, current_cgpa + 0.5), step=0.01)

    future_units_fixed = st.number_input(
        "How many units will you take next semester?",
        min_value=1,
        max_value=30,
        value=15
    )

    st.divider()

    if st.button("Calculate Required GPA to Reach Target"):
        total_weighted = df["Weighted"].sum()
        total_units = df["Units"].sum()

        required_gpa = (
            (target * (total_units + future_units_fixed)) - total_weighted
        ) / future_units_fixed

        required_gpa = round(required_gpa, 2)

        if required_gpa > max_cgpa:
            st.error(
                f"To reach a CGPA of {target}, you would need a GPA of **{required_gpa}**"
                f"which is impossible in a {max_cgpa} grading system."
            )
        elif required_gpa < 0:
            st.success(
                f"You will reach {target} CGPA automatically. Just avoid failing any course."
            )
        else:
            st.success(
                f"To reach a CGPA of **{target}**, you need a **{required_gpa} GPA** next semester."
            )
    grading_scale = GRADE_SYSTEMS[st.session_state.grading_option]

    st.subheader("Generate Example Course Plan to Reach Target CGPA")

    num_courses = st.number_input("Number of courses to simulate:", min_value=1, max_value=10, value=5)
    units_list = [st.number_input(f"Units for course {i+1}", min_value=1, max_value=6, value=3, key=f"unit_{i}")
                  for i in range(num_courses)]
    
    if st.button("Generate Example Plan"):
        required_gpa = (
            (target * (total_units + future_units_fixed)) - total_weighted
        ) / future_units_fixed
        df_plan = generate_course_plan(required_gpa, num_courses, units_list, grading_scale)
        st.dataframe(df_plan)

        st.write(f"Achieved GPA per unit (approx): {round(df_plan["Weighted"].sum() / sum(units_list), 2)}")



    st.subheader("Add Future Courses for Prediction")

    num_future = st.number_input(
        "How many future courses do you want to simulate?",
        min_value=1,
        max_value=20,
        value=1
    )
    future_units_left = st.number_input("How many units are remaining before graduation?", min_value=1, max_value=200, value=40)
    grading_scale = GRADE_SYSTEMS[st.session_state.grading_option]
    grade_choices = list(grading_scale.keys())

    future_courses = []

    for i in range(num_future):
        st.write(f"### Course {i+1}")
        units = st.number_input(f"Units for course {i+1}", 1, 10, key=f"future_units_{i}")
        grade = st.selectbox(f"Expected Grade for course {i+1}", grade_choices, key=f"future_grade_{i}")

        future_courses.append({
            "Units": units,
            "GradePoint": grading_scale[grade]
        })
    
    st.divider()

    if st.button("Predict Future CGPA"):
        future_units = sum(c["Units"] for c in future_courses)
        future_points = sum(c["Units"] * c["GradePoint"] for c in future_courses)

        new_total_units = total_units + future_units
        new_total_points = total_weighted + future_points

        predicted_cgpa = round(new_total_points / new_total_units, 2)

        st.success(f"Predicted CGPA: **{predicted_cgpa}**")

        st.subheader("AI-Powered CGPA Insights")

        # A) MAINTAIN CURRENT PERFORMANCE
        current_semester_gpa = current_cgpa


        future_points_if_maintained = current_semester_gpa * future_units_left
        predicted_final_cgpa_same = round((total_weighted + future_points_if_maintained) / (total_units + future_units_left), 2)
        
        st.info(f"If you maintain your current performance ({current_semester_gpa}), "
                f"your ESTIMATED final CGPA = **{predicted_final_cgpa_same}**")
        
        # B) IMPROVE PERFORMANCE BY +1 GRADE LEVEL
        # Example C-> B, B -> A, stays A
        grade_values = sorted(list(grading_scale.values()), reverse=True)

        def improve_one_level(gpa):
            closest = min(grade_values, key=lambda x: abs(x - gpa))
            idx = grade_values.index(closest)
            return grade_values[max(idx - 1, 0)]
        
        improved_gpa = improve_one_level(current_semester_gpa)

        future_points_improved = improved_gpa * future_units_left
        predicted_final_improved = round(
            (total_weighted + future_points_improved) / (total_units + future_units_left),
            2
        )

        st.success(
            f"If you improve your grades by one level, "
            f"your estimated final CGPA becomes **{predicted_final_improved}**."
        )

        # C) PATH TO TARGET CGPA
        st.subheader("Path to Target CGPA")
        
        required_total_points = target * (total_units + future_units_left)
        needed_future_points = required_total_points - total_weighted
        required_gpa_next = round(needed_future_points / future_units_left, 2)

        if required_gpa_next > max_cgpa:
            st.error(
                f"It is mathematically impossible to reach {target} CGPA "
                f"with the remaining {future_units_left} units."
            )
        else:
            st.warning(
                f"To graduate with **CGPA {target}**, you must score an average of **{required_gpa_next} GPA** in your remaining {future_units_left} Units."
            )
        
        # 4. Rule-Based Text Explanation (Local AI)
        st.subheader("Study Plan / Advice (Rule-Based)")

        plan_lines = []

        plan_lines.append(f"Your current CGPA is {current_cgpa}.")
        plan_lines.append(f"If you maintain your current perforamance, your estimated final CGPA will be {predicted_final_cgpa_same}.")
        plan_lines.append(f"If you improve your grades by one level, your estimated final CGPA could be {predicted_final_improved}.")

        if required_gpa_next > max(grade_values):
            plan_lines.append(
                f"Achieving your target CGPA of {target} is mathematically impossible with the remaining {future_units_left} units."
            )
        else:
            plan_lines.append(
                f"To reach your target CGPA of {target}, you must aim for an average of {required_gpa_next} in your remaining {future_units_left} units."
            )
        
        # Additional advice based on improvement
        if predicted_final_improved > predicted_final_cgpa_same:
            plan_lines.append("Focus on improving weaker courses by one grade level to maximize your final CGPA.")
        else:
            plan_lines.append("Maintain consistency in all courses to ensure steady CGPA growth.")

        plan_lines.append("Stay organized, plan your study schedule, and track your progress each semester!")

        # Display
        for line in plan_lines:
            st.write(".", line)


        fig, ax =  plt.subplots(figsize=(6, 3))
        ax.bar(["Current", "Predicted"], [current_cgpa, predicted_cgpa])
        ax.set_ylabel("CGPA")
        ax.set_ylim(0, max(5, predicted_cgpa + 1))
        ax.set_title("Current vs Predicted CGPA")

        st.pyplot(fig)
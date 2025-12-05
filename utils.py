import pandas as pd


def calculate_gpa(df, grading_scale):
    # df = dataframe containing grades and courses
    # grading_scale = dictionary of grading system used by the school

    df["Points"] = df["Grade"].map(grading_scale)

    df["Weighted"] = df["Points"] * df["Units"]

    semester_gpa = df["Weighted"].sum() / df["Units"].sum()

    return round(semester_gpa, 2)


def generate_course_plan(required_gpa, num_courses, units_per_course, grading_scale):
    points_values = sorted(grading_scale.values(),reverse = True)
    grade_keys = list(grading_scale.keys())

    course_plan = []

    total_units = sum(units_per_course)

    total_points_needed = required_gpa * total_units

    remaining_points = total_points_needed

    for i in range(num_courses):
        units = units_per_course[i]
        avg_points_course = remaining_points / sum(units_per_course[i:])

        closest_points = min(points_values, key=lambda x: abs(x - avg_points_course))
        grade = [k for k, v in grading_scale.items() if v == closest_points][0]

        course_plan.append({
            "Course": f"Course {i+1}",
            "Units": units,
            "Grade": grade,
            "Points": closest_points,
            "Weighted": closest_points * units
        })

        remaining_points -= closest_points * units
    
    return pd.DataFrame(course_plan)
def grade_point(score):
    if score >= 70:
        return 5, 'A'
    elif score >= 60:
        return 4, 'B'
    elif score >= 50:
        return 3, 'C'
    elif score >= 45:
        return 2, 'D'
    elif score >= 40:
        return 1, 'E'
    else:
        return 0, 'F'


def calculate_gp(courses):
    total_units        = 0
    total_grade_points = 0

    for course in courses:
        gp, letter          = grade_point(course['score'])
        course['grade_point']  = gp
        course['grade_letter'] = letter
        total_grade_points  += gp * course['credit_unit']
        total_units         += course['credit_unit']

    if total_units == 0:
        return 0, 0, 0, 'Pass'

    gp = round(total_grade_points / total_units, 2)

    if gp >= 4.50:
        degree_class = 'First Class'
    elif gp >= 3.50:
        degree_class = 'Second Class Upper'
    elif gp >= 2.40:
        degree_class = 'Second Class Lower'
    elif gp >= 1.50:
        degree_class = 'Third Class'
    else:
        degree_class = 'Pass'

    return gp, total_units, total_grade_points, degree_class
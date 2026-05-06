-- Courses with 50 or more students
CREATE OR REPLACE VIEW courses_with_50_or_more_students AS
SELECT
    c.course_id,
    c.course_code,
    c.course_name,
    COUNT(ce.student_id) AS student_count
FROM courses c
JOIN course_enrollments ce
    ON c.course_id = ce.course_id
GROUP BY c.course_id, c.course_code, c.course_name
HAVING COUNT(ce.student_id) >= 50;


-- Students doing 5 or more courses
CREATE OR REPLACE VIEW students_with_5_or_more_courses AS
SELECT
    u.user_id,
    u.full_name,
    u.email,
    COUNT(ce.course_id) AS course_count
FROM users u
JOIN course_enrollments ce
    ON u.user_id = ce.student_id
WHERE u.role = 'student'
GROUP BY u.user_id, u.full_name, u.email
HAVING COUNT(ce.course_id) >= 5;


-- Lecturers teaching 3 or more courses
CREATE OR REPLACE VIEW lecturers_teaching_3_or_more_courses AS
SELECT
    u.user_id,
    u.full_name,
    u.email,
    COUNT(c.course_id) AS course_count
FROM users u
JOIN courses c
    ON u.user_id = c.lecturer_id
WHERE u.role = 'lecturer'
GROUP BY u.user_id, u.full_name, u.email
HAVING COUNT(c.course_id) >= 3;


-- Top 10 most enrolled courses
CREATE OR REPLACE VIEW top_10_most_enrolled_courses AS
SELECT
    c.course_id,
    c.course_code,
    c.course_name,
    COUNT(ce.student_id) AS enrollment_count
FROM courses c
JOIN course_enrollments ce
    ON c.course_id = ce.course_id
GROUP BY c.course_id, c.course_code, c.course_name
ORDER BY enrollment_count DESC
LIMIT 10;


-- Top 10 students with highest overall averages
CREATE OR REPLACE VIEW top_10_students_highest_averages AS
SELECT
    u.user_id,
    u.full_name,
    u.email,
    ROUND(AVG(g.grade), 2) AS average_grade
FROM users u
JOIN submissions s
    ON u.user_id = s.student_id
JOIN grades g
    ON s.submission_id = g.submission_id
WHERE u.role = 'student'
GROUP BY u.user_id, u.full_name, u.email
ORDER BY average_grade DESC
LIMIT 10;
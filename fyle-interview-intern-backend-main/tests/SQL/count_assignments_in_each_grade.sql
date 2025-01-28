-- Write query to get count of assignments in each grade
SELECT 
    T1.grade, 
    COUNT(T1.id) AS count
FROM 
    assignments T1
WHERE 
    T1.state = 'GRADED'
GROUP BY 
    T1.grade;
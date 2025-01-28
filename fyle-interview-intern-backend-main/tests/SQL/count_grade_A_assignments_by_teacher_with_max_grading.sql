-- Write query to find the number of grade A's given by the teacher who has graded the most assignments
SELECT 
    T1.teacher_id, 
    COUNT(T1.id) AS count
FROM 
    assignments T1
WHERE 
    T1.grade = 'A' AND T1.state = 'GRADED'
GROUP BY 
    T1.teacher_id
ORDER BY 
    count DESC
LIMIT 1;
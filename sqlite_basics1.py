import sqlite3

# Connect to SQLite (in memory for testing)
conn = sqlite3.connect(':memory:')

# this is important because foreign keys are OFF by default in SQLite
conn.execute("PRAGMA foreign_keys = ON;")

cursor = conn.cursor()

# Helper function to inspect table contents
def print_table(cursor, table_name):
    cursor.execute(f"SELECT * FROM {table_name}")
    rows = cursor.fetchall()
    columns = [desc[0] for desc in cursor.description]

    print(f"\nTable: {table_name}")
    print(" | ".join(columns))
    print("-" * 30)

    for row in rows:
        print(" | ".join(str(value) for value in row))

# Create tables
cursor.execute("""
CREATE TABLE student (
    student_id INT PRIMARY KEY,
    name TEXT NOT NULL,
    age INT
)
""")

cursor.execute("""
CREATE TABLE registered_courses (
    courses_id INT,
    student_id INT,
PRIMARY KEY (student_id, courses_id),
FOREIGN KEY (student_id) REFERENCES student(student_id)
)
""")

cursor.execute("""
CREATE TABLE grades (
    courses_id INT,
    student_id INT,
    received_grade INT,
    PRIMARY KEY (student_id, courses_id, received_grade),
    FOREIGN KEY (student_id, courses_id) REFERENCES registered_courses(student_id, courses_id)            
                         
)
""")

students = [
    (1, 'Alice', 20),
    (2, 'Bob', 22),
    (3, 'Charlie', 21)
]


registered_courses = [
    (100, 1),
    (101, 1),
    (101, 2),
    (102, 2),
    (102, 3),
    (100, 3)
]

grades = [
    (100, 1, 50),
    (101, 1, 60),
    (101, 2, 80),
    (102, 2, 99),
    (102, 3, 100),
    (100, 3, 45)
]

cursor.executemany("INSERT INTO student VALUES (?, ?, ?)", students)
cursor.executemany("INSERT INTO registered_courses VALUES (?, ?)", registered_courses)
cursor.executemany("INSERT INTO grades VALUES (?, ?, ?)", grades)

conn.commit()

print_table(cursor, "student")
print_table(cursor, "registered_courses")
print_table(cursor, "grades")



#find the maximum
print("Maximum grade per student:")
cursor.execute("""
SELECT g.student_id, g.courses_id, g.received_grade AS max_grade FROM grades g
JOIN (
    SELECT student_id, MAX(received_grade) AS max_grade
    FROM grades
    GROUP BY student_id           ) mg
ON g.student_id = mg.student_id AND g.received_grade = mg.max_grade;
"""
)
for row in cursor.fetchall():
    print(row)


#find the average
print("\nAverage grade per student:")
cursor.execute("""
SELECT student_id, AVG(received_grade) AS average_grade
FROM grades              
GROUP BY student_id
               """
)
for row in cursor.fetchall():
    print(row)

# Example SELECT query
cursor.execute("SELECT * FROM student")
print("\nResult of: SELECT * FROM student")
for row in cursor.fetchall():
    print(row)


conn.close()
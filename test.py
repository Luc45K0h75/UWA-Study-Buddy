import sqlite3
import os
from datetime import datetime

path = os.path.dirname(os.path.abspath(__file__))
database = os.path.join(path, "StudyBuddy.db")

conn = sqlite3.connect(database)
conn.row_factory = sqlite3.Row

# Test upcoming events query
student_id = 12345678
now = int(datetime.now().timestamp())
print("Current timestamp:", now)

rows = conn.execute("""
    SELECT st.Name, s.SessionDateTime AS Date, g.GroupName, s.Description, s.Location, u.UnitName
    FROM Session s
    JOIN Groups g ON s.GroupID = g.GroupID
    JOIN SessionType st ON s.SessionTypeID = st.SessionTypeID
    JOIN Unit u ON g.UnitID = u.UnitID
    JOIN StudentGroups sg ON sg.GroupID = g.GroupID
    WHERE sg.StudentID = ? AND s.SessionDateTime >= ?
    ORDER BY s.SessionDateTime ASC
    LIMIT 3
""", (student_id, now)).fetchall()

print("Upcoming events found:", len(rows))
for r in rows:
    print(dict(r))

# Check if student is in any groups
groups = conn.execute("""
    SELECT * FROM StudentGroups WHERE StudentID = ?
""", (student_id,)).fetchall()
print("Student groups:", [dict(g) for g in groups])

# Check sessions
sessions = conn.execute("SELECT * FROM Session").fetchall()
print("All sessions:", [dict(s) for s in sessions])

conn.close()
import sqlite3

conn = sqlite3.connect(
    "database/jira_sync.db"
)

cursor = conn.cursor()

print("\n===== SYNC_METADATA =====")

cursor.execute(
    "SELECT * FROM sync_metadata"
)

for row in cursor.fetchall():
    print(row)

print("\n===== LATEST ISSUES =====")

cursor.execute("""
SELECT
    issue_key,
    updated_at
FROM jira_issues
ORDER BY updated_at DESC
LIMIT 5
""")

for row in cursor.fetchall():
    print(row)

conn.close()
import sqlite3, sys

conn = sqlite3.connect("c:/Think2Act/think2act.db")
cur = conn.cursor()
cur.execute("PRAGMA table_info(user_profiles)")
cols = [r[1] for r in cur.fetchall()]
print("user_profiles columns:", cols)
needed = ["target_role", "career_mode", "github_handle", "linkedin_profile_url", "leetcode_username", "target_companies"]
missing = [c for c in needed if c not in cols]
if missing:
    print("MISSING columns:", missing)
    # Add them
    for col in missing:
        if col == "target_companies":
            cur.execute(f"ALTER TABLE user_profiles ADD COLUMN {col} TEXT")
        else:
            cur.execute(f"ALTER TABLE user_profiles ADD COLUMN {col} TEXT")
        print(f"  Added: {col}")
    conn.commit()
    print("All columns added successfully.")
else:
    print("All settings columns already present.")
conn.close()

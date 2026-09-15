from database.db import fetch_one, execute


def seed_owner():
    existing = fetch_one("SELECT id FROM Users WHERE role = ?", ("owner",))
    if existing:
        print("Owner already exists. Skipping seed.")
        return

    execute(
        "INSERT INTO Users (username, password, role, room_id) VALUES (?, ?, ?, ?)",
        ("Sanjay", "Sanjay123", "owner", None)
    )
    print("Owner created → username: Sanjay | password: Sanjay123")


if __name__ == "__main__":
    seed_owner()
from database.db import fetch_all, fetch_one, execute, execute_return_id


def get_user_by_username(username):
    return fetch_one("SELECT * FROM Users WHERE username = ?", (username,))


def get_user_by_id(user_id):
    return fetch_one("SELECT * FROM Users WHERE id = ?", (user_id,))


def get_all_renters():
    return fetch_all("SELECT * FROM Users WHERE role = ?", ("renter",))


def create_renter(username, password, room_id):
    return execute_return_id(
        "INSERT INTO Users (username, password, role, room_id) VALUES (?, ?, ?, ?)",
        (username, password, "renter", room_id)
    )


def update_renter(renter_id, username, password, room_id):
    return execute(
        "UPDATE Users SET username = ?, password = ?, room_id = ? WHERE id = ?",
        (username, password, room_id, renter_id)
    )


def delete_renter(renter_id):
    return execute("DELETE FROM Users WHERE id = ? AND role = ?", (renter_id, "renter"))
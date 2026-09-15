from database.db import fetch_all, fetch_one, execute, execute_return_id


def get_all_rooms():
    return fetch_all("SELECT * FROM Rooms")


def get_room_by_id(room_id):
    return fetch_one("SELECT * FROM Rooms WHERE id = ?", (room_id,))


def create_room(room_no, renter_name, arriving_date, advance_booking_amount, first_reading):
    return execute_return_id(
        "INSERT INTO Rooms (room_no, renter_name, arriving_date, advance_booking_amount, first_reading) VALUES (?, ?, ?, ?, ?)",
        (room_no, renter_name, arriving_date, advance_booking_amount, first_reading)
    )


def update_room(room_id, room_no, renter_name, arriving_date, advance_booking_amount, first_reading):
    return execute(
        "UPDATE Rooms SET room_no = ?, renter_name = ?, arriving_date = ?, advance_booking_amount = ?, first_reading = ? WHERE id = ?",
        (room_no, renter_name, arriving_date, advance_booking_amount, first_reading, room_id)
    )


def delete_room(room_id):
    return execute("DELETE FROM Rooms WHERE id = ?", (room_id,))
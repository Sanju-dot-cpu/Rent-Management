from database.db import fetch_all, fetch_one, execute, execute_return_id


def get_bills_by_room(room_id):
    return fetch_all(
        "SELECT * FROM Electricity WHERE room_id = ? ORDER BY Electricity.start_date DESC",
        (room_id,)
    )


def get_bill_by_id(bill_id):
    return fetch_one("SELECT * FROM Electricity WHERE id = ?", (bill_id,))


def create_bill(room_id, month, start_date, end_date, units, amount, paid_date, balance_amount, status):
    return execute_return_id(
        "INSERT INTO Electricity (room_id, month, start_date, end_date, units, amount, paid_date, balance_amount, status) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
        (room_id, month, start_date, end_date, units, amount, paid_date, balance_amount, status)
    )


def update_bill(bill_id, month, start_date, end_date, units, amount, paid_date, balance_amount, status):
    return execute(
        "UPDATE Electricity SET month = ?, start_date = ?, end_date = ?, units = ?, amount = ?, paid_date = ?, balance_amount = ?, status = ? WHERE id = ?",
        (month, start_date, end_date, units, amount, paid_date, balance_amount, status, bill_id)
    )


def delete_bill(bill_id):
    return execute("DELETE FROM Electricity WHERE id = ?", (bill_id,))
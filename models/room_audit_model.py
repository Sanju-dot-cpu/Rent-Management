from database.db import fetch_all, fetch_one, execute, execute_return_id


def get_audits_by_room(room_id):
    return fetch_all(
        "SELECT * FROM Room_Audit WHERE room_id = ? ORDER BY Room_Audit.start_date DESC",
        (room_id,)
    )


def get_audit_by_id(audit_id):
    return fetch_one("SELECT * FROM Room_Audit WHERE id = ?", (audit_id,))


def create_audit(room_id, month, start_date, end_date, amount, paid_date, balance_amount, status):
    return execute_return_id(
        "INSERT INTO Room_Audit (room_id, month, start_date, end_date, amount, paid_date, balance_amount, status) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
        (room_id, month, start_date, end_date, amount, paid_date, balance_amount, status)
    )


def update_audit(audit_id, month, start_date, end_date, amount, paid_date, balance_amount, status):
    return execute(
        "UPDATE Room_Audit SET month = ?, start_date = ?, end_date = ?, amount = ?, paid_date = ?, balance_amount = ?, status = ? WHERE id = ?",
        (month, start_date, end_date, amount, paid_date, balance_amount, status, audit_id)
    )


def delete_audit(audit_id):
    return execute("DELETE FROM Room_Audit WHERE id = ?", (audit_id,))
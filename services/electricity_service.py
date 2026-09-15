from models.electricity_model import (
    get_bills_by_room, get_bill_by_id, create_bill, update_bill, delete_bill
)
from utils.validators import is_empty, is_valid_amount, is_valid_int
from utils.date_helper import parse_date, add_one_month


def list_bills(room_id):
    return get_bills_by_room(room_id)


def get_bill(bill_id):
    return get_bill_by_id(bill_id)


def add_bill(room_id, month, start_date, units, amount, paid_date, balance_amount, status):
    if is_empty(month) or is_empty(start_date) or is_empty(amount) or is_empty(units):
        return {"success": False, "message": "Required fields missing"}
    if not is_valid_int(units):
        return {"success": False, "message": "Invalid units"}
    if not is_valid_amount(amount) or not is_valid_amount(balance_amount or 0):
        return {"success": False, "message": "Invalid amount"}
    if status not in ("Paid", "Pending"):
        return {"success": False, "message": "Status must be Paid or Pending"}

    sd = parse_date(start_date)
    ed = add_one_month(sd)
    amt = float(amount)
    bal = float(balance_amount or 0)

    bid = create_bill(room_id, month, sd, ed, int(units), amt, paid_date, bal, status)
    return {"success": True, "message": "Bill added", "id": bid}


def edit_bill(bill_id, month, start_date, units, amount, paid_date, balance_amount, status):
    if status not in ("Paid", "Pending"):
        return {"success": False, "message": "Status must be Paid or Pending"}

    sd = parse_date(start_date)
    ed = add_one_month(sd)
    amt = float(amount)
    bal = float(balance_amount or 0)

    update_bill(bill_id, month, sd, ed, int(units), amt, paid_date, bal, status)
    return {"success": True, "message": "Bill updated"}


def remove_bill(bill_id):
    delete_bill(bill_id)
    return {"success": True, "message": "Bill deleted"}
from models.room_audit_model import (
    get_audits_by_room, get_audit_by_id, create_audit, update_audit, delete_audit
)
from utils.validators import is_empty, is_valid_amount
from utils.date_helper import parse_date, add_one_month


def list_audits(room_id):
    return get_audits_by_room(room_id)


def get_audit(audit_id):
    return get_audit_by_id(audit_id)


def add_audit(room_id, month, start_date, amount, paid_date, balance_amount, status):
    if is_empty(month) or is_empty(start_date) or is_empty(amount):
        return {"success": False, "message": "Required fields missing"}
    if not is_valid_amount(amount) or not is_valid_amount(balance_amount or 0):
        return {"success": False, "message": "Invalid amount"}
    if status not in ("Paid", "Pending"):
        return {"success": False, "message": "Status must be Paid or Pending"}

    sd = parse_date(start_date)
    ed = add_one_month(sd)
    amt = float(amount)
    bal = float(balance_amount or 0)

    aid = create_audit(room_id, month, sd, ed, amt, paid_date, bal, status)
    return {"success": True, "message": "Audit added", "id": aid}


def edit_audit(audit_id, month, start_date, amount, paid_date, balance_amount, status):
    if is_empty(month) or is_empty(start_date) or is_empty(amount):
        return {"success": False, "message": "Required fields missing"}
    if status not in ("Paid", "Pending"):
        return {"success": False, "message": "Status must be Paid or Pending"}

    sd = parse_date(start_date)
    ed = add_one_month(sd)
    amt = float(amount)
    bal = float(balance_amount or 0)

    update_audit(audit_id, month, sd, ed, amt, paid_date, bal, status)
    return {"success": True, "message": "Audit updated"}


def remove_audit(audit_id):
    delete_audit(audit_id)
    return {"success": True, "message": "Audit deleted"}
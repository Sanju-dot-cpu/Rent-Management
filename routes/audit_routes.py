from flask import Blueprint, request
from utils.decorators import role_required
from services.audit_service import list_audits, add_audit, edit_audit, remove_audit, get_audit
from utils.response import success_response, error_response

from flask import send_file
from services.room_service import get_room
from services.pdf_service import audit_pdf

audit_bp = Blueprint("audit", __name__)


@audit_bp.route("/list/<int:room_id>", methods=["GET"])
@role_required("owner")
def api_list_audits(room_id):
    return success_response(list_audits(room_id))


@audit_bp.route("/get/<int:audit_id>", methods=["GET"])
@role_required("owner")
def api_get_audit(audit_id):
    audit = get_audit(audit_id)
    if not audit:
        return error_response("Audit not found", 404)
    return success_response(audit)


@audit_bp.route("/add", methods=["POST"])
@role_required("owner")
def api_add_audit():
    data = request.get_json() or request.form
    result = add_audit(
        data.get("room_id"),
        data.get("month"),
        data.get("start_date"),
        data.get("amount"),
        data.get("paid_date"),
        data.get("balance_amount"),
        data.get("status")
    )
    if not result["success"]:
        return error_response(result["message"], 400)
    return success_response(result, result["message"])


@audit_bp.route("/edit/<int:audit_id>", methods=["POST"])
@role_required("owner")
def api_edit_audit(audit_id):
    data = request.get_json() or request.form
    result = edit_audit(
        audit_id,
        data.get("month"),
        data.get("start_date"),
        data.get("amount"),
        data.get("paid_date"),
        data.get("balance_amount"),
        data.get("status")
    )
    if not result["success"]:
        return error_response(result["message"], 400)
    return success_response(result, result["message"])


@audit_bp.route("/delete/<int:audit_id>", methods=["POST"])
@role_required("owner")
def api_delete_audit(audit_id):
    result = remove_audit(audit_id)
    return success_response(result, result["message"])


@audit_bp.route("/download/<int:room_id>", methods=["GET"])
@role_required("owner")
def api_download_audit_pdf(room_id):
    room = get_room(room_id)
    if not room:
        return error_response("Room not found", 404)
    audits = list_audits(room_id)
    buf = audit_pdf(room, audits)
    return send_file(
        buf,
        as_attachment=True,
        download_name=f"audit_{room['room_no']}.pdf",
        mimetype="application/pdf"
    )
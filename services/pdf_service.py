from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet


def _build_pdf(title, headers, rows):
    buffer = BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        leftMargin=15 * mm,
        rightMargin=15 * mm,
        topMargin=15 * mm,
        bottomMargin=15 * mm
    )
    styles = getSampleStyleSheet()
    story = []

    story.append(Paragraph(f"<b>{title}</b>", styles["Title"]))
    story.append(Spacer(1, 8))

    data = [headers] + rows
    table = Table(data, repeatRows=1)

    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1e3a8a")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("ALIGN", (0, 0), (-1, -1), "LEFT"),
        ("GRID", (0, 0), (-1, -1), 0.4, colors.grey),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f1f5f9")]),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]))

    story.append(table)
    doc.build(story)
    buffer.seek(0)
    return buffer


def audit_pdf(room, audits):
    headers = ["Month", "Start", "End", "Amount", "Paid", "Balance", "Status"]
    rows = []
    for a in audits:
        rows.append([
            a.get("month") or "-",
            str(a.get("start_date") or "-"),
            str(a.get("end_date") or "-"),
            f"Rs.{a.get('amount', 0)}",
            str(a.get("paid_date") or "-"),
            f"Rs.{a.get('balance_amount', 0)}",
            a.get("status") or "-",
        ])
    title = f"Room Audit - {room.get('room_no')} | {room.get('renter_name')}"
    return _build_pdf(title, headers, rows)


def electricity_pdf(room, bills):
    headers = ["Month", "Start", "End", "Units", "Amount", "Paid", "Balance", "Status"]
    rows = []
    for b in bills:
        rows.append([
            b.get("month") or "-",
            str(b.get("start_date") or "-"),
            str(b.get("end_date") or "-"),
            str(b.get("units", 0)),
            f"Rs.{b.get('amount', 0)}",
            str(b.get("paid_date") or "-"),
            f"Rs.{b.get('balance_amount', 0)}",
            b.get("status") or "-",
        ])
    title = f"Electricity Bill - {room.get('room_no')} | {room.get('renter_name')}"
    return _build_pdf(title, headers, rows)


def renters_pdf(renters, rooms):
    headers = ["Renter Name", "Username", "Room No", "Password"]
    rows = []
    for r in renters:
        room = next((x for x in rooms if x["id"] == r.get("room_id")), None)
        rows.append([
            room["renter_name"] if room else "-",
            r.get("username") or "-",
            room["room_no"] if room else "-",
            r.get("password") or "-",
        ])
    return _build_pdf("Renters List", headers, rows)
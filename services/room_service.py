from models.room_model import (
    get_all_rooms, get_room_by_id, create_room, update_room, delete_room
)
from utils.validators import is_empty, is_valid_amount, is_valid_int


def list_rooms():
    return get_all_rooms()


def get_room(room_id):
    return get_room_by_id(room_id)


def add_room(room_no, renter_name, arriving_date, advance_booking_amount, first_reading):
    if is_empty(room_no) or is_empty(renter_name) or is_empty(arriving_date):
        return {"success": False, "message": "All fields required"}
    if not is_valid_amount(advance_booking_amount):
        return {"success": False, "message": "Invalid advance booking amount"}
    if not is_valid_int(first_reading):
        return {"success": False, "message": "Invalid first reading"}

    rid = create_room(
        room_no,
        renter_name,
        arriving_date,
        float(advance_booking_amount),
        int(first_reading)
    )
    return {"success": True, "message": "Room added", "id": rid}


def edit_room(room_id, room_no, renter_name, arriving_date, advance_booking_amount, first_reading):
    if is_empty(room_no) or is_empty(renter_name) or is_empty(arriving_date):
        return {"success": False, "message": "All fields required"}
    update_room(
        room_id,
        room_no,
        renter_name,
        arriving_date,
        float(advance_booking_amount),
        int(first_reading)
    )
    return {"success": True, "message": "Room updated"}


def remove_room(room_id):
    delete_room(room_id)
    return {"success": True, "message": "Room deleted"}
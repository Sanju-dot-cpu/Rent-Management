def is_empty(value):
    if value is None:
        return True
    if isinstance(value, str) and value.strip() == "":
        return True
    return False


def is_valid_amount(value):
    try:
        float(value)
        return True
    except (ValueError, TypeError):
        return False


def is_valid_int(value):
    try:
        int(value)
        return True
    except (ValueError, TypeError):
        return False
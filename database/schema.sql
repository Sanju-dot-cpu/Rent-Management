CREATE TABLE IF NOT EXISTS Users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    password TEXT NOT NULL,
    role TEXT NOT NULL,
    room_id INTEGER NULL
);

CREATE TABLE IF NOT EXISTS Rooms (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    room_no TEXT NOT NULL,
    renter_name TEXT NOT NULL,
    arriving_date TEXT NOT NULL,
    advance_booking_amount REAL NOT NULL,
    first_reading INTEGER NULL
);

CREATE TABLE IF NOT EXISTS Room_Audit (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    room_id INTEGER NOT NULL,
    month TEXT NOT NULL,
    start_date TEXT NOT NULL,
    end_date TEXT NOT NULL,
    amount REAL NOT NULL,
    paid_date TEXT NULL,
    balance_amount REAL NOT NULL,
    status TEXT NULL,
    FOREIGN KEY (room_id) REFERENCES Rooms(id)
);

CREATE TABLE IF NOT EXISTS Electricity (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    room_id INTEGER NOT NULL,
    month TEXT NOT NULL,
    start_date TEXT NOT NULL,
    end_date TEXT NOT NULL,
    units INTEGER NOT NULL,
    amount REAL NOT NULL,
    paid_date TEXT NULL,
    balance_amount REAL NOT NULL,
    status TEXT NULL,
    FOREIGN KEY (room_id) REFERENCES Rooms(id)
);
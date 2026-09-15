function goToRoom(roomId) {
    navigateTo(`/owner/room/${roomId}`);
}

function toggleCardMenu(e, roomId) {
    e.stopPropagation();
    const menu = document.getElementById(`menu-${roomId}`);
    document.querySelectorAll(".card-menu-dropdown").forEach(m => {
        if (m !== menu) m.style.display = "none";
    });
    menu.style.display = menu.style.display === "block" ? "none" : "block";
}

document.addEventListener("click", () => {
    document.querySelectorAll(".card-menu-dropdown").forEach(m => m.style.display = "none");
});

function openAddRoomModal() {
    document.getElementById("roomModalTitle").textContent = "Add New Room";
    document.getElementById("addRoomForm").reset();
    document.getElementById("room_id").value = "";
    document.getElementById("addRoomError").style.display = "none";
    document.getElementById("addRoomModal").style.display = "flex";
}

function closeAddRoomModal() {
    document.getElementById("addRoomModal").style.display = "none";
}

async function editRoom(roomId) {
    const res = await apiGet(`/owner/room/api/list`);
    if (!res.success) return alert("Failed to load rooms");

    const room = res.data.find(r => r.id === roomId);
    if (!room) return alert("Room not found");

    document.getElementById("roomModalTitle").textContent = "Edit Room";
    document.getElementById("room_id").value = room.id;
    document.getElementById("room_no").value = room.room_no;
    document.getElementById("renter_name").value = room.renter_name;
    document.getElementById("arriving_date").value = room.arriving_date;
    document.getElementById("advance_booking_amount").value = room.advance_booking_amount;
    document.getElementById("first_reading").value = room.first_reading || "";
    document.getElementById("addRoomError").style.display = "none";
    document.getElementById("addRoomModal").style.display = "flex";
}

async function deleteRoom(roomId) {
    if (!confirm("Delete this room? All its audit & electricity records will remain orphaned.")) return;
    const res = await apiPost(`/owner/room/api/delete/${roomId}`, {});
    if (res.success) {
        navigateTo("/owner/dashboard");
    } else {
        alert(res.message);
    }
}

document.getElementById("addRoomForm").addEventListener("submit", async (e) => {
    e.preventDefault();
    const errBox = document.getElementById("addRoomError");
    errBox.style.display = "none";

    const id = document.getElementById("room_id").value;
    const body = {
        room_no: document.getElementById("room_no").value.trim(),
        renter_name: document.getElementById("renter_name").value.trim(),
        arriving_date: document.getElementById("arriving_date").value,
        advance_booking_amount: document.getElementById("advance_booking_amount").value,
        first_reading: document.getElementById("first_reading").value
    };

    let res;
    if (id) res = await apiPost(`/owner/room/api/edit/${id}`, body);
    else res = await apiPost("/owner/room/api/add", body);

    if (res.success) {
        navigateTo("/owner/dashboard");
    } else {
        errBox.textContent = res.message;
        errBox.style.display = "block";
    }
});
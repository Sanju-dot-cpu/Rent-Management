function fmtDate(d) {
    if (!d) return "-";
    const dt = new Date(d);
    const m = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"];
    return `${String(dt.getDate()).padStart(2,"0")}-${m[dt.getMonth()]}-${dt.getFullYear()}`;
}

function statusBadge(status) {
    if (status === "Pending")
        return '<span style="color:#dc2626;font-weight:600;">Pending</span>';
    return '<span style="color:#16a34a;font-weight:600;">Paid</span>';
}

async function loadBills() {
    const res = await apiGet(`/owner/electricity/list/${ROOM_ID}`);
    const body = document.getElementById("billBody");
    if (!res.success || !res.data.length) {
        body.innerHTML = '<tr><td colspan="9" class="loading">No electricity records.</td></tr>';
        return;
    }
    body.innerHTML = res.data.map(b => `
        <tr>
            <td>${b.month}</td>
            <td>${fmtDate(b.start_date)}</td>
            <td>${fmtDate(b.end_date)}</td>
            <td>${b.units}</td>
            <td>₹${b.amount}</td>
            <td>${fmtDate(b.paid_date)}</td>
            <td>₹${b.balance_amount}</td>
            <td>${statusBadge(b.status)}</td>
            <td>
                <button class="btn-small" onclick="editBill(${b.id})">Edit</button>
                <button class="btn-small btn-danger" onclick="deleteBill(${b.id})">Delete</button>
            </td>
        </tr>`).join("");
}

function openAddBillModal() {
    document.getElementById("billModalTitle").textContent = "Add Bill Entry";
    document.getElementById("billForm").reset();
    document.getElementById("bill_id").value = "";
    document.getElementById("billError").style.display = "none";
    document.getElementById("billModal").style.display = "flex";
}

function closeBillModal() {
    document.getElementById("billModal").style.display = "none";
}

async function editBill(id) {
    const res = await apiGet(`/owner/electricity/get/${id}`);
    if (!res.success) return alert(res.message);
    const b = res.data;
    document.getElementById("billModalTitle").textContent = "Edit Bill Entry";
    document.getElementById("bill_id").value = b.id;
    document.getElementById("bill_month").value = b.month;
    document.getElementById("bill_start_date").value = b.start_date;
    document.getElementById("bill_units").value = b.units;
    document.getElementById("bill_amount").value = b.amount;
    document.getElementById("bill_paid_date").value = b.paid_date ?? "";
    document.getElementById("bill_balance_amount").value = b.balance_amount;
    document.getElementById("bill_status").value = b.status || "Paid";
    document.getElementById("billModal").style.display = "flex";
}

async function deleteBill(id) {
    if (!confirm("Delete this record?")) return;
    const res = await apiPost(`/owner/electricity/delete/${id}`, {});
    if (res.success) loadBills();
    else alert(res.message);
}

document.getElementById("billForm").addEventListener("submit", async (e) => {
    e.preventDefault();
    const id = document.getElementById("bill_id").value;
    const body = {
        room_id: ROOM_ID,
        month: document.getElementById("bill_month").value,
        start_date: document.getElementById("bill_start_date").value,
        units: document.getElementById("bill_units").value,
        amount: document.getElementById("bill_amount").value,
        paid_date: document.getElementById("bill_paid_date").value || null,
        balance_amount: document.getElementById("bill_balance_amount").value || 0,
        status: document.getElementById("bill_status").value
    };

    let res;
    if (id) res = await apiPost(`/owner/electricity/edit/${id}`, body);
    else res = await apiPost("/owner/electricity/add", body);

    if (res.success) {
        closeBillModal();
        loadBills();
    } else {
        const err = document.getElementById("billError");
        err.textContent = res.message;
        err.style.display = "block";
    }
});

loadBills();

function downloadBillPdf() {
    window.location.href = `/owner/electricity/download/${ROOM_ID}`;
}
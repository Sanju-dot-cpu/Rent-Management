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

async function loadAudits() {
    const res = await apiGet(`/owner/audit/list/${ROOM_ID}`);
    const body = document.getElementById("auditBody");
    if (!res.success || !res.data.length) {
        body.innerHTML = '<tr><td colspan="8" class="loading">No audit records.</td></tr>';
        return;
    }
    body.innerHTML = res.data.map(a => `
        <tr>
            <td>${a.month}</td>
            <td>${fmtDate(a.start_date)}</td>
            <td>${fmtDate(a.end_date)}</td>
            <td>₹${a.amount}</td>
            <td>${fmtDate(a.paid_date)}</td>
            <td>₹${a.balance_amount}</td>
            <td>${statusBadge(a.status)}</td>
            <td>
                <button class="btn-small" onclick="editAudit(${a.id})">Edit</button>
                <button class="btn-small btn-danger" onclick="deleteAudit(${a.id})">Delete</button>
            </td>
        </tr>`).join("");
}

function openAddAuditModal() {
    document.getElementById("auditModalTitle").textContent = "Add Rent Entry";
    document.getElementById("auditForm").reset();
    document.getElementById("audit_id").value = "";
    document.getElementById("auditError").style.display = "none";
    document.getElementById("auditModal").style.display = "flex";
}

function closeAuditModal() {
    document.getElementById("auditModal").style.display = "none";
}

async function editAudit(id) {
    const res = await apiGet(`/owner/audit/get/${id}`);
    if (!res.success) return alert(res.message);
    const a = res.data;
    document.getElementById("auditModalTitle").textContent = "Edit Rent Entry";
    document.getElementById("audit_id").value = a.id;
    document.getElementById("audit_month").value = a.month;
    document.getElementById("audit_start_date").value = a.start_date;
    document.getElementById("audit_amount").value = a.amount;
    document.getElementById("audit_paid_date").value = a.paid_date ?? "";
    document.getElementById("audit_balance_amount").value = a.balance_amount;
    document.getElementById("audit_status").value = a.status || "Paid";
    document.getElementById("auditModal").style.display = "flex";
}

async function deleteAudit(id) {
    if (!confirm("Delete this record?")) return;
    const res = await apiPost(`/owner/audit/delete/${id}`, {});
    if (res.success) loadAudits();
    else alert(res.message);
}

document.getElementById("auditForm").addEventListener("submit", async (e) => {
    e.preventDefault();
    const id = document.getElementById("audit_id").value;
    const body = {
        room_id: ROOM_ID,
        month: document.getElementById("audit_month").value,
        start_date: document.getElementById("audit_start_date").value,
        amount: document.getElementById("audit_amount").value,
        paid_date: document.getElementById("audit_paid_date").value || null,
        balance_amount: document.getElementById("audit_balance_amount").value || 0,
        status: document.getElementById("audit_status").value
    };

    let res;
    if (id) res = await apiPost(`/owner/audit/edit/${id}`, body);
    else res = await apiPost("/owner/audit/add", body);

    if (res.success) {
        closeAuditModal();
        loadAudits();
    } else {
        const err = document.getElementById("auditError");
        err.textContent = res.message;
        err.style.display = "block";
    }
});

loadAudits();

function downloadAuditPdf() {
    window.location.href = `/owner/audit/download/${ROOM_ID}`;
}
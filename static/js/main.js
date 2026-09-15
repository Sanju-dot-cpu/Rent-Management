async function apiGet(url) {
    try {
        const res = await fetch(url, {
            method: "GET",
            headers: { "Content-Type": "application/json" }
        });
        return await res.json();
    } catch (e) {
        return { success: false, message: "Network error" };
    }
}

async function apiPost(url, body) {
    try {
        const res = await fetch(url, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(body)
        });
        return await res.json();
    } catch (e) {
        return { success: false, message: "Network error" };
    }
}

// ✅ Step-by-step navigation helper — always use this
function navigateTo(url) {
    window.location.href = url;
}
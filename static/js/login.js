document.getElementById("loginForm").addEventListener("submit", async (e) => {
    e.preventDefault();
    const errBox = document.getElementById("loginError");
    errBox.style.display = "none";

    const username = document.getElementById("username").value.trim();
    const password = document.getElementById("password").value.trim();

    const res = await apiPost("/login", { username, password });

    if (res.success) {
        window.location.href = res.redirect;
    } else {
        errBox.textContent = res.message || "Login failed";
        errBox.style.display = "block";
    }
});
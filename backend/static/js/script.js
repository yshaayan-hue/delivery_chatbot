// ---------------- LOAD CHAT ---------------- //

window.onload = function () {
    const saved = localStorage.getItem("chatData");
    if (saved) {
        document.getElementById("chat-box").innerHTML = saved;
    }
};

// ---------------- SAVE CHAT ---------------- //

function saveChat() {
    const chatBox = document.getElementById("chat-box");
    localStorage.setItem("chatData", chatBox.innerHTML);
}

// ---------------- ADD MESSAGE ---------------- //

function addMessage(text, type) {
    const chatBox = document.getElementById("chat-box");

    const msg = document.createElement("div");
    msg.classList.add("chat-message", type);
    msg.innerText = text;

    chatBox.appendChild(msg);

    chatBox.scrollTo({
        top: chatBox.scrollHeight,
        behavior: "smooth"
    });

    saveChat();
}

// ---------------- ADD IMAGE ---------------- //

function addImage(url) {
    const chatBox = document.getElementById("chat-box");

    const img = document.createElement("img");
    img.src = url;
    img.style.maxWidth = "200px";

    chatBox.appendChild(img);
    saveChat();
}

// ---------------- QUICK ISSUE ---------------- //

function quickIssue(issue) {
    document.getElementById("issue").value = issue;
    addMessage(issue, "user");
}

// ---------------- SUBMIT ISSUE ---------------- //

async function submitIssue() {
    const issue = document.getElementById("issue").value;
    const orderId = document.getElementById("order_id").value;
    const file = document.getElementById("image").files[0];

    if (!issue || !orderId) {
        addMessage("⚠️ Fill all fields!", "bot");
        return;
    }

    addMessage(`Issue: ${issue}`, "user");
    addMessage(`Order ID: ${orderId}`, "user");

    const formData = new FormData();
    formData.append("issue", issue);
    formData.append("order_id", orderId);
    if (file) formData.append("image", file);

    try {
        const res = await fetch("/api/tickets", {
            method: "POST",
            body: formData
        });

        const data = await res.json();

        if (res.ok) {
            addMessage(`✅ Ticket ID: ${data.ticket_id}`, "bot");

            // ✅ SAVE LAST TICKET (memory retained)
            localStorage.setItem("lastTicket", data.ticket_id);

            // auto-fill tracker
            document.getElementById("track_id").value = data.ticket_id;

            if (data.image_url) {
                addImage(data.image_url);
            }
        } else {
            addMessage(`❌ ${data.error}`, "bot");
        }

    } catch (err) {
        addMessage("⚠️ Server error", "bot");
    }
}

// ---------------- CLEAR CHAT (SMART) ---------------- //

function clearChat() {
    const lastTicket = localStorage.getItem("lastTicket");

    // Clear only chat messages
    localStorage.setItem("chatData", "");

    const chatBox = document.getElementById("chat-box");

    chatBox.innerHTML = `
        <div class="chat-message bot">
            Hello! How can I help you today?
        </div>

        ${lastTicket ? `
        <div class="chat-message bot">
            📌 Last Ticket ID: ${lastTicket}
        </div>
        ` : ""}

        <div class="quick-actions">
            <button class="quick-btn" onclick="quickIssue('Missing Item')">
                Missing Item
            </button>

            <button class="quick-btn" onclick="quickIssue('Wrong Order')">
                Wrong Order
            </button>
        </div>
    `;
}

// ---------------- TRACK SECTION ---------------- //

function openTrack() {
    document.getElementById("chat-section").style.display = "none";
    document.getElementById("track-section").style.display = "block";
}

function closeTrack() {
    document.getElementById("track-section").style.display = "none";
    document.getElementById("chat-section").style.display = "flex";
}

async function trackTicket() {
    const id = document.getElementById("track_id").value;

    if (!id) {
        alert("Enter Ticket ID");
        return;
    }

    const res = await fetch(`/api/ticket/${id}`);
    const data = await res.json();

    const result = document.getElementById("result");

    if (res.ok) {
        result.innerHTML = `
            <p><b>Ticket ID:</b> ${data.ticket_id}</p>
            <p><b>Issue:</b> ${data.issue}</p>
            <p><b>Order ID:</b> ${data.order_id}</p>
            <p><b>Status:</b> ${data.status}</p>
            ${data.image_url ? `<img src="${data.image_url}" width="200">` : ""}
        `;
    } else {
        result.innerHTML = `<p style="color:red;">${data.error}</p>`;
    }
}